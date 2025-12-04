import sqlite3
from flask import Flask, render_template, sesion, request, redirect

app = Flask(__name_)

DB_FILE = "data.db"

db = sqlite3.connect(DB_FILE)
c = db.cursor()

c.execute("CREATE TABLE IF NOT EXISTS user_info(user TEXT, pw TEXT, bal INTEGER, game_history TEXT, WL_by_game TEXT);")

db.commit()
db.close()

@app.route('/', methods=["GET", "POST"])
def floor():
    pass

@app.route('/login', methods=["GET", "POST"])
def login():
    pass

@app.route('/profile', methods=["GET", "POST"])
def profile():
    pass

@app.route('/register', methods=["GET", "POST"])
def register():
    pass

if __name__ == "__main__":
    app.debug = True
    app.run()
