import sqlite3, json, requests
from flask import Flask, render_template, session, request, redirect, url_for
from solitaire import Solitaire
#from blackjack import Blackjack
import poker

app = Flask(__name__)

app.secret_key = "testing"
DB_FILE = "data.db"

poker_game = poker.Poker(0)

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

@app.route("/change_username", methods=["GET", "POST"])
def change_username():
    new_username = request.form['username']
    username=session['username']
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    #no repeats
    cmd = "SELECT * FROM user_info WHERE user =?"
    c.execute(cmd, (new_username,))
    db_user = c.fetchone()
    if db_user:
        db.close()
        text = "duplicate username"
        return render_template('change.html', text=text)
    #proceed
    else:
        cmd = "UPDATE user_info SET user=? WHERE user =?"
        c.execute(cmd, (new_username, username))
        db.commit()
        session['username'] = new_username
    db.close()
    return redirect(url_for('profile'))

@app.route("/clear_history", methods=["GET", "POST"])
def clear_history():
    username=session['username']
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    cmd = "UPDATE user_info SET game_history='' WHERE user =?"
    c.execute(cmd, (username))
    db.close()
    return redirect(url_for('profile'))

@app.route('/floor', methods=["GET", "POST"])
def floor():
    return render_template('floor.html', username=session['username'])

@app.route('/profile', methods=["GET", "POST"])
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))

    else:
        username=session['username']
        db = sqlite3.connect(DB_FILE)
        c = db.cursor()
        cmd = "SELECT * FROM user_info WHERE user =?"
        c.execute(cmd, (username,))
        user_data = c.fetchone()
        db.close()

        return render_template('profile.html', username=username, balance=user_data[2], game_history=user_data[3])


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
        cmd = "SELECT * FROM user_info WHERE user =?"
        c.execute(cmd, (username,))
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
        cmd = "SELECT * FROM user_info WHERE user =?"
        c.execute(cmd, (username,))
        db_user = c.fetchone()
        if db_user:
            db.close()
            text = "duplicate username"
            return render_template('register.html', text=text)
        #proceed
        else:
            cmd = f"INSERT into user_info VALUES (?, ?, ?, ?, ?)"
            c.execute(cmd, (username, password, '0', '', ''))
            db.commit()
        db.close()
        session['username'] = username
        return redirect(url_for('floor'))
    return render_template('register.html', text='')

@app.route('/poker', methods=["GET", "POST"])
def poker():
    if 'username' not in session:
        return redirect(url_for('login'))

    username=session['username']
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    cmd = "SELECT * FROM user_info WHERE user =?"
    c.execute(cmd, (username,))
    user_data = c.fetchone()
    db.close()

    poker_game.set_chips(user_data[2])


    return render_template('poker.html')

@app.route('/tarot', methods=["GET", "POST"])
def tarot():
    return render_template('tarot.html', username=session['username'])

# create solitaire game variable to prevent deck resets
solitaire_deck = Solitaire()

@app.route('/solitaire_setup', methods=["GET", "POST"])
def solitaire_setup():
    solitaire_deck = Solitaire()
    test_text = solitaire_deck.card_dict
    return redirect(url_for('solitaire',
        deck=solitaire_deck,
        test_text=test_text,
        active_deck=''))

@app.route('/solitaire', methods=["GET", "POST"])
def solitaire():
    if request.method == 'POST':
        print("place 1 ")
        if solitaire_deck.active_pile != '':
            print("place 2 ")
            solitaire_deck.active_pile2 = request.form.get('pile')
            solitaire_deck.active_card2 = request.form.get('card')
        else:
            print("place 3 ")
            solitaire_deck.active_pile = request.form.get('pile')
            solitaire_deck.active_card = request.form.get('card')
        solitaire_deck.play()
    else:
        print("place 4 ")
        solitaire_deck.active_deck = ''
    test_text = solitaire_deck.card_dict
    test_text2 = [solitaire_deck.active_pile, solitaire_deck.active_card, solitaire_deck.active_pile2, solitaire_deck.active_card2]
    return render_template('solitaire.html',
        deck=solitaire_deck,
        test_text=test_text,
        test_text2=test_text2,
        active_deck='')

if __name__ == "__main__":
    app.debug = True
    app.run()
