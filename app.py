import sqlite3
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
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

if __name__ == '__main__':
    init_db()
    app.run(debug=True)