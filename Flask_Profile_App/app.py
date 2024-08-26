# app.py
# Flask Profile App

from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import re
 
app = Flask(__name__)
app.secret_key = "I always enjoy studying at a library."
 
@app.route('/', methods=['GET', 'POST'])
def index():
    if 'loggedin' in session:
        msg = "Logged in successfully."
        active = True
    else:
        msg = ""
        active = False
    if request.method == 'GET':
        return render_template('index.html', msg=msg, active=active)
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect("./data/database.db")
        curs = conn.cursor()
        user = list(curs.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password,)))

        if user:
            session['loggedin'] = True
            session['id'] = user[0][0]
            session['username'] = user[0][1]
            msg = 'Logged in successfully!'
            active = True
        else:
            msg = 'Incorrect username/password!'
            active = False
        return render_template('index.html', msg=msg, active=active)

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        city = request.form['city']
        state = request.form['state']
       
        conn = sqlite3.connect("./data/database.db")
        curs = conn.cursor()
        user = curs.execute("SELECT * FROM users WHERE username = ?", (username, )).fetchone()
        if user:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address.'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers.'
        else:
            curs.execute("INSERT INTO users(username, password, email, city, state) VALUES(?, ?, ?, ?, ?)", (username, password, email, city, state, ))
            conn.commit()
            conn.close()
            msg = 'You have successfully registered.'
            return redirect(url_for('profile'))
    elif request.method == 'GET':
        msg = 'Please fill out the form.'
    return render_template('register.html', msg=msg)
 
@app.route("/profile")
def profile():
    if 'loggedin' in session:
        conn = sqlite3.connect("./data/database.db")
        curs = conn.cursor()
        user = curs.execute('SELECT * FROM users WHERE id = ?', (session['id'], )).fetchone()

        return render_template("profile.html", user=user)
    else:
        msg = "User not logged in."
        active = False

        return render_template("index.html", msg=msg, active=active)
 
@app.route("/update", methods=['GET', 'POST'])
def update():
    msg = ''
    if 'loggedin' in session:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']
            city = request.form['city']
            state = request.form['state']
          
            conn = sqlite3.connect("./data/database.db")
            curs = conn.cursor()
            user = curs.execute("SELECT * FROM users WHERE username = ?",(username, )).fetchone()
            if user:
                msg = 'Account already exists !'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                msg = 'Invalid email address !'
            elif not re.match(r'[A-Za-z0-9]+', username):
                msg = 'name must contain only characters and numbers !'
            else:
                curs.execute('''UPDATE users SET username = ?, password = ?,
                               email = ?, city = ?, state = ? WHERE id = ?''', (
                    username, password, email, city, state, session['id'],))
                conn.commit()
                user = curs.execute("SELECT * FROM users WHERE username = ?",(username, )).fetchone()
                conn.commit()
                conn.close()

                msg = 'You have successfully updated your profile info.'
                return render_template("profile.html", msg=msg, user=user)
    elif request.method == 'POST':
        msg = 'Please fill out the form.'
    return render_template("update.html", msg=msg)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    msg = "You have been successfully logged out."
    return render_template("index.html", msg=msg)

@app.route('/about')
def about():
    return render_template("about.html")
 
 
if __name__ == "__main__":
    app.run(debug=True)

