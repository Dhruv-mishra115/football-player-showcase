import sqlite3
from flask import Flask, render_template, request , redirect, session 
from flask import session, redirect

app = Flask(__name__)
app.secret_key = "secret123"

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT
)
""")

conn.commit()
conn.close()

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/register', methods=['GET', 'POST'])
def register():

    # 🔒 ADD THIS (just 2 lines)
    if 'user' not in session:
        return redirect('/login')

    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        position = request.form['position']
        contact = request.form['contact']
        video = request.form['video']
        
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO players (name, age, position, contact, video)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, age, position, contact, video))

        conn.commit()
        conn.close()

        return render_template("success.html")

    return render_template("register.html")

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            position TEXT,
            contact TEXT,
            video TEXT
        )
    ''')

    conn.commit()
    conn.close()

@app.route('/players')
def players():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM players")
    all_players = cursor.fetchall()

    conn.close()

    return render_template("players.html", players=all_players)

@app.route('/player/<int:id>')
def player(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM players WHERE id = ?", (id,))
    player = cursor.fetchone()

    conn.close()

    return render_template("player.html", player=player)

from flask import request, redirect, render_template

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))

        conn.commit()
        conn.close()

        return redirect('/login')

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()

        conn.close()

        if user:
            session['user'] = username
            return redirect('/')
        else:
            return "Invalid Credentials"

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)