'''
  Jake Liu, Cindy Liu, Veronika Duvanova, Robert Chen
  RotisserieChicken
  SoftDev
  P01
  2025-12-20
  time spent: 4h
'''
import sqlite3, json, requests
from flask import Flask, render_template, session, request, redirect, url_for
from solitaire import Solitaire
#from blackjack import Blackjack
import poker
from tarot import Tarot

app = Flask(__name__)

app.secret_key = "testing"
DB_FILE = "data.db"

poker_game: poker.Poker = None
poker_deal_amts = [3, 1, 1]
solitaire_deck = None
tarot_deck = Tarot()

db = sqlite3.connect(DB_FILE)
c = db.cursor()

c.execute("CREATE TABLE IF NOT EXISTS user_info(user TEXT, pw TEXT, bal INTEGER, game_history TEXT);")

db.commit()
db.close()

@app.route('/')
def startup():
    if 'username' in session:
        return redirect(url_for('floor'))
    else:
        text = ""
        return redirect(url_for('login', text=text))
        # return render_template('login.html', text=text)

@app.route("/logout")
def logout():
    session.pop('username', None)
    global poker_game
    poker_game = None
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
    msg = ""
    if request.method == "POST":
        print("in11")
        if request.form.get("withdraw") != None:
            print("in")
            try:
                withdraw_amt = int(request.form.get("withdraw"))
                username=session['username']
                db = sqlite3.connect(DB_FILE)
                c = db.cursor()
                cmd = "UPDATE user_info SET bal=bal + ? WHERE user =?"
                c.execute(cmd, (withdraw_amt, username))
                db.commit()
                db.close()
                msg = f"Successfully withdrew ${withdraw_amt}"
            except ValueError:
                msg = "Withdraw amount must be an integer value!"
    return render_template('charge.html', username=session['username'], msg=msg)

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
def poker_page():
    if 'username' not in session:
        return redirect(url_for('login'))

    global poker_game
    if poker_game == None:
        poker_game = poker.Poker(0)

    is_betting = False
    error = ""


    if not poker_game.is_game_active:
        username=session['username']
        db = sqlite3.connect(DB_FILE)
        c = db.cursor()
        cmd = "SELECT * FROM user_info WHERE user =?"
        c.execute(cmd, (username,))
        user_data = c.fetchone()
        db.close()
        poker_game.set_chips(user_data[2])

    if poker_game.is_game_active and \
        poker_game.player_to_move == poker_game.OPPONENT:
        poker_game.check_or_call() # placeholder

    if poker_game.is_betting_round_over():
        if len(poker_game.board_cards) >= 5:
            poker_game.showdown()
    
            if poker_game.winner == poker_game.PLAYER:
                username=session['username']
                db = sqlite3.connect(DB_FILE)
                c = db.cursor()
                cmd = "UPDATE user_info SET bal=bal + ? WHERE user =?"
                c.execute(cmd, (sum(poker_game.stakes), username))
                db.commit()
                db.close()
        else: 
            poker_game.burn_card()
            poker_game.deal_board(poker_deal_amts[poker_game.round])   

    if request.method == 'POST':
        if request.form.get('start_game') == 'DEAL':
            poker_game.is_game_active = True
            poker_game.deal_hole()

        if not poker_game.is_game_over and \
            poker_game.player_to_move == poker_game.PLAYER:
            action = request.form.get('player_action')
            if action == 'FOLD':
                poker_game.fold()
            elif action == 'CHECK':
                poker_game.check_or_call()
            elif action == 'BET':
                is_betting = True

            if request.form.get("bet_amt") != None:
                try:
                    bet_amt = int(request.form.get("bet_amt"))
                    error = poker_game.make_bet_or_raise_to(bet_amt)

                    username=session['username']
                    db = sqlite3.connect(DB_FILE)
                    c = db.cursor()
                    cmd = "UPDATE user_info SET bal=bal - ? WHERE user =?"
                    c.execute(cmd, (bet_amt, username))
                    db.commit()
                    db.close()
                except ValueError:
                    error = "Bet size must be an integer value!"
        if poker_game.is_game_over:
            if request.form.get('player_action') == 'RESTART':
                username=session['username']
                db = sqlite3.connect(DB_FILE)
                c = db.cursor()
                cmd = "SELECT * FROM user_info WHERE user =?"
                c.execute(cmd, (username,))
                user_data = c.fetchone()
                db.close()
                poker_game.reset_game(user_data[2])

    username=session['username']
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    cmd = "SELECT * FROM user_info WHERE user =?"
    c.execute(cmd, (username,))
    user_data = c.fetchone()
    db.close()
               
    return render_template(
        'poker.html',
        is_game_active=poker_game.is_game_active,
        opponent_hand=poker_game.hole_cards[1],
        player_hand=poker_game.hole_cards[0],
        board=poker_game.board_cards,
        is_player_turn=(poker_game.player_to_move == poker_game.PLAYER),
        is_betting=is_betting,
        pot=sum(poker_game.stakes),
        error=error,
        final_hand=poker_game.final_hands,
        is_game_over=poker_game.is_game_over,
        winner=poker_game.winner,
        balance=user_data[2]
    )

@app.route('/reset_tarot', methods=["GET", "POST"])
def reset_tarot():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    tarot_deck.deck = tarot_deck.generate_deck(4)
    tarot_deck.active_card_ids = [None, None]

    active_info = []
    for idx in tarot_deck.active_card_ids:
        if idx is None:
            active_info.append(["", "", "", ""])
        else:
            active_info.append(tarot_deck.display_info(tarot_deck.deck[idx]))

    return render_template('tarot.html', username=session['username'], deck=tarot_deck.deck, active_cards=active_info, active_indices=tarot_deck.active_card_ids, game_won=False)


@app.route('/tarot', methods=["GET", "POST"])
def tarot():
    if 'username' not in session:
        return redirect(url_for('login'))
        
    if request.method == 'POST':
        card_input = request.form.get('card')

        if card_input is not None and card_input.isdigit():
            card_index = int(card_input)

            if (tarot_deck.active_card_ids[0] is None) or (None not in tarot_deck.active_card_ids):
                tarot_deck.active_card_ids = [None, None]
                tarot_deck.active_card_ids[0] = card_index
            elif tarot_deck.active_card_ids[1] is None and tarot_deck.active_card_ids[0] is not card_index:
                tarot_deck.active_card_ids[1] = card_index
    
    i1, i2 = tarot_deck.active_card_ids
    if i1 is not None and i2 is not None:
        if tarot_deck.deck[i1]["name"] == tarot_deck.deck[i2]["name"]:
            tarot_deck.deck[i1]["matched"] = True
            tarot_deck.deck[i2]["matched"] = True
            tarot_deck.active_card_ids = [None, None]

    active_info = []
    for idx in tarot_deck.active_card_ids:
        if idx is None:
            active_info.append(["", "", "", ""])
        else:
            active_info.append(tarot_deck.display_info(tarot_deck.deck[idx]))

    game_won = tarot_deck.all_matched()

    return render_template('tarot.html', username=session['username'], deck=tarot_deck.deck, active_cards=active_info, active_indices=tarot_deck.active_card_ids, game_won=game_won)

@app.route('/solitaire_setup', methods=["GET", "POST"])
def solitaire_setup():
    # replace the deck used for solitaire with a new one
    global solitaire_deck
    solitaire_deck = Solitaire()
    test_text = solitaire_deck.card_dict
    print('re-setup')
    return redirect(url_for('solitaire',
        deck=solitaire_deck,
        test_text=test_text,
        active_deck=''))

def string_to_list(string):
    parts = string.strip("[]").split(", ")
    return [p.strip("'") for p in parts]

@app.route('/solitaire', methods=["GET", "POST"])
def solitaire():
    if request.method == 'POST':
        if solitaire_deck.active_pile != '':
            solitaire_deck.active_pile2 = request.form.get('pile')
            solitaire_deck.active_card2 = string_to_list(request.form.get('card'))
        else:
            solitaire_deck.active_pile = request.form.get('pile')
            solitaire_deck.active_card = string_to_list(request.form.get('card'))
            print(solitaire_deck.active_card)
        solitaire_deck.play()
    else:
        solitaire_deck.active_deck = ''
    test_text = solitaire_deck.card_dict
    test_text2 = [solitaire_deck.active_pile, solitaire_deck.active_card, solitaire_deck.active_pile2, solitaire_deck.active_card2]
    return render_template('solitaire.html',
        deck=solitaire_deck,
        test_text=test_text,
        test_text2=test_text2,
        active_deck='')

@app.route('/solitaire_cheat', methods=["GET", "POST"])
def solitaire_cheat():
    insult=requests.get('https://evilinsult.com/generate_insult.php?lang=en&type=json').json()["insult"]
    return render_template('solitaire_cheat.html', insult=insult)

@app.route('/blackjack', methods=["GET", "POST"])
def blackjack():
    if 'username' not in session:
        return redirect(url_for('login'))

    return render_template('blackjack.html')

if __name__ == "__main__":
    app.debug = True
    app.run()
