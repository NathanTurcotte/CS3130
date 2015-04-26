Nathan Turcotte
5027975
CS3130
Term Project

Found in directory Project of
    https://github.com/NathanTurcotte/CS3130.git

Requires the Flask library

To Execute :
    call init_database() of main.py once
    To do so, write the following two lines in the python3 interpreter
        1-from main import init_database
        2-init_database()
    Then execute the program using
        python3 main.py
    Access using a web browser and the given address, in my case 127.0.0.1:5000
    Note : You may need to add /login to the address to be redirected to a proper page
    
    Step 1 : Create accounts using the Create Account link
    Step 2 : Add a friend using the Add Friend link
    Step 3 : Select the friend you wish to communicate with using the drop down menu
    Step 4 : Click the submit button.
    Step 5 : Write your message in the text box, click submit, (the one to the right) to send 
        Note:
            -Usernames and passwords are case sensitive!
            -You can send messages to a friend that has not friended you, he will receive all messages
                once he befriends you.
            -You must use the refresh link, located in the left side-bar and only avaiable when
                a converation is chosen , to view new messages, the webpage does not auto-update.
            -Do not refresh the webpage as it will require forms to be resubmitted, resulting in
                repeated messages
    

Provides a web browser interface and database storage to the messaging System.

Scripts :
    main.py : interacts with database, provides proper web pages and feedback (error messages) using flask.
Templates :
    schema.db : database schema
        tables:
            employees (username, password)
            messages  (sender's username, receiver's username, message)
            friends   (username, friends username)
    layout.html : provides basic layout of html components. All previous files extend layout.html
    createAccount.html : provides account creation forms
    friendFinder.html : provides form to find a friend
    login.html : provides form to login
    menu.html : provides links to add friends, choose friends.
                displays messages related to current conversation

    

        

