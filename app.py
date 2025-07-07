from flask import Flask, render_template, request, redirect, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # change this to something secure

# Initialize database if not exists
def init_db():
    if not os.path.exists('database.db'):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)')
        conn.commit()
        conn.close()

init_db()

# Homepage
@app.route('/')
def index():
    return render_template('index.html')

# Login or Register
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
        user = c.fetchone()

        if user:
            session['username'] = username
        else:
            c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            conn.commit()
            session['username'] = username

        conn.close()
        return redirect('/main')

    return render_template('login.html')

# Main Page
@app.route('/main')
def main():
    if 'username' in session:
        return render_template('main.html', username=session['username'])
    return redirect('/')

# Logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/')

# Secret Admin Page
@app.route('/admin')
def admin():
    code = request.args.get('code')
    if code == 'gwapo1':  # secret code
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users")
        users = c.fetchall()
        conn.close()
        return render_template('admin.html', users=users)
    else:
        return "Access Denied", 403

if __name__ == '__main__':
    app.run(debug=True)