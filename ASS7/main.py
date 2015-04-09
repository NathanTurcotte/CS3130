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

def init_database():
    with closing(connect_database()) as db:
        with app.open_resource('schema.sql',mode ='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

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

@app.route('/show')
def show_entries():
    cur = g.db.execute('select id, fname, lname, department from employees order by id desc')
    entries = [dict(ID=row[0], fname=row[1], lname=row[2], department=row[3]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    #perform error checking
    g.db.execute('insert into employees (id, fname, lname, department) values (?, ?, ?, ?)',
                 [request.form['id'], request.form['fname'], request.form['lname'], request.form['department']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

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

@app.route('/', methods = ['GET', 'POST'])
def options():
    if not session.get('logged_in'):
        return render_template('login.html', error="You must log in to view this page")
    if request.form['choice'] == 'add':
        return render_template('add.html')
    elif request.form['choice'] == 'search':
        return render_template('search.html')
    elif request.form['choice'] == 'remove':
        return render_template('options.html', error="unavailable")
    else:
        return render_template('options.html', error="Please select an option")
    
@app.route('/search', methods = ['POST'])
def search():
    if not session.get('logged_in'):
        return render_template('login.html')
    cur = g.db.execute('select id from employees where id = (?)', ['55'])
    entries = [dict(ID=row[0], fname=row[1], lname=row[2], department=row[3]) for row in cur.fetchall()]
    return render_template('show_entries.html', entries=entries)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

if __name__ == '__main__':
    app.run()
