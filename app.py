from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import hashlib

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Set a secret key for session management

def check_password(member_name, password):
    # Connect to the SQLite database
    conn = sqlite3.connect('library.db')
    c = conn.cursor()

    # Retrieve the hashed password for the member
    c.execute('SELECT password FROM Members WHERE member_name = ?', (member_name,))
    result = c.fetchone()
    conn.close()

    if result:
        stored_password = result[0]
        # Check if the hashed password matches
        return hashlib.sha256(password.encode()).hexdigest() == stored_password
    return False

@app.route('/')
def index():
    if 'logged_in' in session and session['logged_in']:
        books = get_books()
        return render_template('index.html', books=books)
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        member_name = request.form.get('member_name')
        password = request.form.get('password')

        if member_name and password:
            if check_password(member_name, password):
                session['logged_in'] = True
                session['member_name'] = member_name
                flash('Login successful', 'success')
                return redirect(url_for('index'))
            else:
                flash('Invalid login credentials', 'danger')
        else:
            flash('Please fill in both fields', 'warning')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('member_name', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

def get_books():
    conn = sqlite3.connect('library.db', detect_types=sqlite3.PARSE_DECLTYPES)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT * FROM Books')
    books = c.fetchall()
    conn.close()
    return books

if __name__ == '__main__':
    app.run(debug=True)
