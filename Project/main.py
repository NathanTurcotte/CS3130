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


"""
    Performs query, designated by query with values specified by args.
    returns None if no elements are found in database
    if one=True:
        return only one element
    else:
        return all elements
"""
def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    if rv and one:
        return rv[0]
    elif rv and not one:
        return rv
    elif not rv:
        return None
    #return (rv[0] if rv else None) if one else rv


@app.before_request
def before_request():
    g.db = connect_database()
@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()
"""
    Entry point of website interface
"""
@app.route('/')
def main():
    #present login interface if user is not logged in, otherwise display the menu
    if not session.get('logged_in'):
        return render_template("login.html")
    else:
        return render_template("menu.html") 

"""
    Called when user clicks submit to send a message.
    session["username"] = username of user who wishes to send a message
    session["conversation"] = username of user who should receive the message
    request.form['message'] = message written in menu.html text area
"""
@app.route('/sendMessage', methods=['POST'])
def sendMessage():
    #redirect to login if user is not logged in
    if not session.get('logged_in'):
        flash("You are not logged in")
        return render_template("login.html")
    #promt user to select a conversation before attempting to send a message
    if session.get('conversation') == "":
        flash("Choose a friend before starting a conversation", category="error")
        return renderUserPage()
    #enter message into database
    g.db.execute("insert into messages (sender, receiver, message) values (?,?,?)", [session["username"], session["conversation"], request.form['message']])
    print("Message sent from " + session["username"] + " to " + session['conversation'])
    g.db.commit()
    return renderUserPage()

"""
    Called when user clicks submit in the left side bar. (changes the intended conversation)
    session['conversation'] = username of whoever the user chooses
"""
@app.route('/chooseConversation', methods=['POST'])
def chooseConversation():
    #redirect to login screen if not logged int
    if not session.get('logged_in'):
        flash("Please log in")
        return render_template("login.html")
    #set session['conversation'] to selected user
    session['conversation'] = request.form['friends']
    return renderUserPage()

"""
    Redirects to createAccount display
"""
@app.route('/createAccount')
def createAccount():
    #ask user to logout before creating an account
    if session.get('logged_in'):
        flash("Please log out before creating another account")
        return render_template("menu.html")
    else:
        return render_template("createAccount.html")

"""
    Create account with given credentials
        request.form['username'] = desired username
        request.form['password1'] = password
        request.form['password2'] = password verification
"""
@app.route('/addAccount', methods=['POST'])
def addAccount():
    #prompt user to logout before creating an account
    if session.get('logged_in'):
        flash ("Please log out before creating another account")
        return render_template("menu.html")
    valid = query_db("select username from users where username = (?)", [request.form['username']], one = True)
    #check if the username allready exist by querying the database
    if valid is not None:
        flash("Username unavailable", category="error")
        return render_template("createAccount.html")
    #first check if both passwords match
    if request.form['password1'] == request.form['password2']:
        pass
    else:
        flash("Passwords do not match", category = "error")
        return render_template("createAccount.html")
    #usernames can only contain characters
    if not request.form['username'].isalpha():
        flash("Usernames must only contain letters (a-z or A-Z)", category="error")
        return render_template("createAccount.html")
    #make sure a password is between 8 and 20 characters
    if not len(request.form['password1']) > 7 and len(request.form['password1']) < 21:
        flash("Password must be between 8 and 20 characters long. (inclusive)", category="error")
        return render_template("createAccount.html")
    g.db.execute("insert into users (username, password) values (?,?)",[request.form['username'], request.form['password1']])
    g.db.commit()
    flash("Account Created")
    return render_template("login.html")

"""
    redirect to friend finder display
"""
@app.route('/findFriend')
def findFriend():
    #redirect to login if not logged in
    if not session.get('logged_in'):
        return render_template("login.html")
    else:
        return render_template("friendFinder.html")
"""
    Attempt to add a friend with information in POST
        request.form['username'] = desired friend
"""
@app.route('/addFriend', methods=['POST'])
def addFriend():
    #first check : check if desired friend exist
    fr = query_db("select username from users where username = (?)", [request.form['username']], one = True)
    if fr is None:
        flash("Unable to find Friend", category="error")
        return renderUserPage()
    #second check : check if desired friend is allready marked as a friend
    fr = query_db("select friend from friends where owner = (?) and friend =(?)", [session['username'], request.form['username']], one = True)
    if fr is not None:
        flash("You may not add the same friend twice!")
        return renderUserPage()
    #if both checks fail (ie : a legitimate request) and the new friend in friends table
    g.db.execute("insert into friends (owner, friend) values (?,?)", [session['username'], request.form['username']])
    g.db.commit()
    return renderUserPage()
   
"""
    Attempt to login with credentials in POST
        request.form['username'] = username
        request.form['password'] password
"""
@app.route('/login', methods=['POST'])
def login():
    #query database for user with matching password and username
    credentials = query_db('select username from users where username = (?) and password = (?)', [request.form['username'], request.form['password']], one = True)
    #if no entries exist, deny access
    if credentials is None:
        flash("Invalid Login",category="error")
        return render_template("login.html")
    #login process
    else:
        session['logged_in'] = True
        session['username'] = credentials[0]
        session['conversation'] = ""
        return renderUserPage()

"""
    Refresh Conversation. Called when clicking refresh in the left side bar(only shown when displaying a conversation)
        Note : refreshing the webpage using the browser will cause forms to be resubmitted, resulting in repeated messages
"""
@app.route('/refreshConversation')
def refreshConversation():
    entries = [];
    #find all friends of the current user
    fr = g.db.execute('select friend from friends where owner = (?)', [session['username']])
    entries = [dict(friend=row[0]) for row in fr.fetchall()]
    #find all messages between the current use and user maked by session['conversation']
    m = g.db.execute("select sender, receiver, message from messages where (sender = (?) and receiver = (?)) or (sender = (?) and receiver = (?))",[session['username'],session['conversation'], session
    ['conversation'],session['username']])
    messages = [dict(s=row[0], r=row[1], m=row[2]) for row in m.fetchall()]
    #render menu with the conversation messages and found friends
    return render_template("menu.html", entries=entries, messages=messages)

"""
    Same as above, called by other functions
    renders menu page with the current users friends and messages coresponding to the current conversation, may be none
"""
def renderUserPage():
    entries = [];
    fr = g.db.execute('select friend from friends where owner = (?)', [session['username']])
    entries = [dict(friend=row[0]) for row in fr.fetchall()]
    m = g.db.execute("select sender, receiver, message from messages where (sender = (?) and receiver = (?)) or (sender = (?) and receiver = (?))",[session['username'],session['conversation'], session['conversation'],session['username']])
    messages = [dict(s=row[0], r=row[1], m=row[2]) for row in m.fetchall()]
    return render_template("menu.html", entries=entries, messages=messages)

@app.route('/logout')
def logout():
    session['logged_in'] = False
    session['username'] = ""
    session['conversation'] = ""
    flash('You were logged out')
    return render_template("login.html")

if __name__ == '__main__':
    app.run()
