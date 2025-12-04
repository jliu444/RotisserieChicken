import sqlite3
from flask import Flask, render_template, session, request, redirect, url_for

app = Flask(__name__)

app.secret_key = "testing"
DB_FILE = "data.db"

db = sqlite3.connect(DB_FILE)
c = db.cursor()

c.execute("CREATE TABLE IF NOT EXISTS user_info(user TEXT, pw TEXT, bal INTEGER, game_history TEXT, WL_by_game TEXT);")

db.commit()
db.close()

@app.route('/')
def startup():
    if 'username' in session:
        return redirect(url_for('floor'))
    else:
        text = ""
        return render_template('login.html', text=text)

@app.route("/logout")
def logout():
  session.pop('username', None)
  return redirect(url_for('startup'))

@app.route('/floor', methods=["GET", "POST"])
def floor():
    return render_template('floor.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = sqlite3.connect(DB_FILE)
        c = db.cursor()
        cmd = f"SELECT * FROM user_info WHERE user = '{username}'"
        c.execute(cmd)
        user_data = c.fetchone()
        db.close()
        if user_data == None or user_data[1] != password:
            text = "login failed"
            return render_template('login.html', text=text)
        else:create basic login and register templates
            session['username'] = username
            return redirect(url_for('floor'))
    return render_template('login.html', text='')

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = sqlite3.connect(DB_FILE)
        c = db.cursor()
        #no repeats
        cmd = f"SELECT * FROM user_info WHERE user = '{username}'"
        c.execute(cmd)
        db_user = c.fetchone()
        if db_user:
            db.close()
            text = "duplicate username"
            return render_template('register.html', text=text)
        #proceed
        else:
            cmd = f"INSERT into user_info VALUES ('{username}', '{password}', '0', '', '')"
            c.execute(cmd)
            db.commit()
        db.close()
        session['username'] = username
        return redirect(url_for('floor'))
    return render_template('register.html', text='')

@app.route('/profile', methods=["GET", "POST"])
def profile():
    pass

if __name__ == "__main__":
    app.debug = True
    app.run()
