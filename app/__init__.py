import sqlite3, json, requests
from flask import Flask, render_template, session, request, redirect, url_for
from solitaire import Solitaire
from blackjack import Blackjack
from poker import Poker

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
        #return redirect(url_for('login', text=text))
        return render_template('login.html', text=text)

@app.route("/logout")
def logout():
  session.pop('username', None)
  return redirect(url_for('startup'))

@app.route('/floor', methods=["GET", "POST"])
def floor():
    return render_template('floor.html', username=session['username'])




@app.route('/profile', methods=["GET", "POST"])
def profile():
    return render_template('profile.html', username=session['username'])

@app.route('/change', methods=["GET", "POST"])
def change():
    return render_template('change.html', username=session['username'])

@app.route('/charge', methods=["GET", "POST"])
def charge():
    return render_template('charge.html', username=session['username'])




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
        else:
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

@app.route('/tarot', methods=["GET", "POST"])
def tarot():
    return render_template('tarot.html', username=session['username'])


@app.route('/solitaire', methods=["GET", "POST"])
def solitaire():
    deck = Solitaire()
    test_text = deck.show_pile()
    return render_template('solitaire.html', test_text='')


if __name__ == "__main__":
    app.debug = True
    app.run()
