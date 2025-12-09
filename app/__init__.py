import sqlite3, json, requests
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
        return redirect(url_for('login', text=text))
        #render_template('login.html', text=text)

@app.route("/logout")
def logout():
  session.pop('username', None)
  return redirect(url_for('startup'))

@app.route('/floor', methods=["GET", "POST"])
def floor():
    return render_template('floor.html', username=session['username'])

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

@app.route('/profile', methods=["GET", "POST"])
def profile():
    pass

'''
Concept:
- add a restart button
  - user selects 1 item from FOUNDATIONS, STOCK, WASTE, OR TABLEAU and calls the function
    -> if the one item is a hidden card at the top of a tableau, show the card
    -> if the one item is an ace at the top of a tableau, place it in foundation pile
    -> if the one item is a stock card, place it (not hidden) on top of the waste pile
    -> ELSE, record active card and reload page
      -> user selects an item from TOP OF FOUNDATIONS or TOP OF TABLEAU and calls the function
        -> if second item is a TABLEAU, check if tableau is empty
          -> if empty and active card is a King: move the King
          -> if empty and active card is not a King: INVALID MOVE
          -> is not empty and active card is (same color) OR (not next #): INVALID MOVE
          -> ELSE: move the item and all the cards beneath it
          -> AFTER ALL THESE IFS, IF ACTIVE CARD IS A FOUNDATION, SHOW THE NEXT FOUNDATION CARD
        -> if second item is a FOUNDATION:
          -> if foundation is empty, INVALID move
          -> if card on top of foundation is (different house) OR (not next #): INVALID move
          -> if active card is NOT top of pile: INVALID move
          -> ELSE: move card into foundation
'''
foundation_1=[]
foundation_2=[]
foundation_3=[]
foundation_4=[]
tableau_1=[]
tableau_2=[]
tableau_3=[]
tableau_4=[]
tableau_5=[]
tableau_6=[]
tableau_7=[]
stock_deck=[]
waste_deck=[]
foundation_decks=[foundation_1, foundation_2, foundation_3, foundation_4]
tableau_decks=[tableau_1, tableau_2, tableau_3, tableau_4, tableau_5, tableau_6, tableau_7]
game_deck=[stock_deck, waste_deck, foundation_decks, tableau_decks]

@app.route('/solitaire', methods=["GET", "POST"])
def solitaire():
    deck_json = new_deck()
    if deck_json["success"]:
        deck_id = deck_json["deck_id"]
        deck_size = deck_json["remaining"]
        abc = "id: " + deck_id + "deck size: " + str(deck_size)
    else:
        abc = 'deck creation failed'
    return render_template('solitaire.html',
        active = '',
        stock='', waste='',
        f1='', f2='', f3='', f4='',
        t1='', t2='', t3='', t4='', t5='', t6='', t7='',
        test_text=abc
    )

def new_deck():
    print ("ran newdeck")
    print (requests.get('https://deckofcardsapi.com/api/deck/new/shuffle/').json())
    return requests.get('https://deckofcardsapi.com/api/deck/new/shuffle/').json()

def new_pile(deck_id, name):
    return requests.get(f'https://deckofcardsapi.com/api/deck/{{deck_id}}/pile/{{name}}/add/?cards=')

if __name__ == "__main__":
    app.debug = True
    app.run()
