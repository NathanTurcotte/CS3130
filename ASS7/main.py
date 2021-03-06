import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing

DATABASE = '/tmp/employees.db'
DEBUG = True
SECRET_KEY = 'secret'
USERNAME = 'default'
PASSWORD = 'admin'

app = Flask(__name__)
app.config.from_object(__name__)

"""
    Initialized database. Call once for lifetime of the program
"""
def init_database():
    with closing(connect_database()) as db:
        with app.open_resource('schema.sql',mode ='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
"""
    Connects to database file specified in global named DATABASE
"""
def connect_database():
    return sqlite3.connect(app.config['DATABASE'])

@app.before_request
def before_request():
    g.db = connect_database()
@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

"""
    renders the show_entries.html page, giving it a dictionary of all entries in the database to display
"""
@app.route('/show')
def show_entries():
    cur = g.db.execute('select id, fname, lname, department from employees order by id desc')
    entries = [dict(ID=row[0], fname=row[1], lname=row[2], department=row[3]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)

"""
    removes the id specified by request.form["ID"] received from remove.html, from the database
"""
@app.route('/remove', methods=['POST'])
def remove():
    if not session.get('logged_in'):
        return render_template("login.html", error="You must be logged in to remove employees")
    g.db.execute("delete from employees where id=(?)",[request.form['id']])
    g.db.commit()
    return render_template("options.html")

"""
    attempts to add an employee to the database
    Receives input from add.html :
        request.form['id'], must be a number and unique
        request.form['fname'], must be alphabetical
        request.form['lname'], must be alphabetical 
        request.form['department'], must be alphabetical
"""
@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    #perform error checking
    #digit/alpha check
    #if a malformed field is found, flash the error and toggle valid to false
    valid = True
    try:
        if request.form['id'].isdigit():
            pass
        else:
            flash("ID must be a number", "error")
            valid = False
        if request.form['fname'].isalpha():
            pass
        else:
            flash("First name must only contain alphabetical characters", "error")
            valid = False
        if request.form['lname'].isalpha():
            pass
        else:
            flash("Last name must only contain alphabetical characters", "error")
        if request.form['department'].isalpha():
            pass
        else:
            flash("Department must only contain alphabetical characters", "error")
        if not valid:
            return render_template("add.html")
        g.db.execute('insert into employees (id, fname, lname, department) values (?, ?, ?, ?)',
                 [request.form['id'], request.form['fname'], request.form['lname'], request.form['department']])
        g.db.commit()
    #catch attempt to add a previously existing ID into the database
    except sqlite3.IntegrityError:
        flash('Employee ID allready exist', 'error')
        return render_template('add.html')
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


"""
    Login using credentials specified in globals USERNAME and PASSWORD
"""
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return render_template('options.html')
    return render_template('login.html', error=error)

"""
    redirects to the options.html page, if not logged in prompts user to do so
"""
@app.route('/gotoOptions')
def gotoOptions():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('options.html')

"""
    Receives input from the options.html page (radio buttons)
    redirects towards the proper page based on value of request.form['choice']
"""
@app.route('/options', methods = ['GET', 'POST'])
def options():
    if not session.get('logged_in'):
        return render_template('login.html', error="You must log in to view this page")
    if request.form['choice'] == 'add':
        return render_template('add.html')
    elif request.form['choice'] == 'search':
        return render_template('search.html')
    elif request.form['choice'] == 'remove':
        cur = g.db.execute('select id, fname, lname, department from employees order by id desc')
        entries = [dict(ID=row[0], fname=row[1], lname=row[2], department=row[3]) for row in cur.fetchall()]
        return render_template('remove.html', entries=entries)
    elif request.form['choice'] == 'display':
        return show_entries()
    else:
        return render_template('options.html', error="Please select an option")
    
"""
    Receives input from the search.html page
    Attempts to find an employee with the id passed by request.form['ID'] (through a textbox)
"""
@app.route('/search', methods = ['POST'])
def search():
    if not session.get('logged_in'):
        return render_template('login.html')
    cur = g.db.execute('select id,fname,lname,department from employees where id = (?)', [request.form['ID']])
    entries = [dict(ID=row[0], fname=row[1], lname=row[2], department=row[3]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)

"""
    Logout routine
"""
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

if __name__ == '__main__':
    app.run()
