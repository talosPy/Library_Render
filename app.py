from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import hashlib


app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Set a secret key for session management


def check_password(member_name, password):
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute('SELECT password FROM Members WHERE member_name = ?', (member_name,))
    result = c.fetchone()
    conn.close()

    if result:
        stored_password = result[0]
        return hashlib.sha256(password.encode()).hexdigest() == stored_password
    return False



@app.route('/')
def index():
    if 'logged_in' in session and session['logged_in']:
        search_query = request.args.get('query', '')
        books = search_books_in_db(search_query)
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



@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        book_name = request.form.get('book_name')
        year = request.form.get('year')
        image = request.form.get('image')
        quantity = int(request.form.get('quantity'))

        if book_name and year and image and quantity:
            conn = sqlite3.connect('library.db')
            c = conn.cursor()
            c.execute('''
                INSERT INTO Books (book_name, year, image, quantity)
                VALUES (?, ?, ?, ?)
            ''', (book_name, year, image, quantity))
            conn.commit()
            conn.close()
            flash('Book added successfully', 'success')
            return redirect(url_for('index'))
        else:
            flash('Please fill in all fields', 'warning')

    return render_template('add_book.html')



@app.route('/edit_book/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    
    if request.method == 'POST':
        book_name = request.form.get('book_name')
        year = request.form.get('year')
        image = request.form.get('image')
        quantity = int(request.form.get('quantity'))

        if book_name and year and image and quantity:
            c.execute('''
                UPDATE Books
                SET book_name = ?, year = ?, image = ?, quantity = ?
                WHERE id = ?
            ''', (book_name, year, image, quantity, book_id))
            conn.commit()
            flash('Book updated successfully', 'success')
            return redirect(url_for('index'))
        else:
            flash('Please fill in all fields', 'warning')

    c.execute('SELECT * FROM Books WHERE id = ?', (book_id,))
    book = c.fetchone()
    conn.close()
    
    if book:
        return render_template('edit_book.html', book=book)
    else:
        flash('Book not found', 'danger')
        return redirect(url_for('index'))



@app.route('/delete_book/<int:book_id>')
def delete_book(book_id):
    conn = sqlite3.connect('library.db')
    c = conn.cursor()
    c.execute('DELETE FROM Books WHERE id = ?', (book_id,))
    conn.commit()
    conn.close()
    flash('Book deleted successfully', 'success')
    return redirect(url_for('index'))



@app.route('/search', methods=['GET'])
def search_books():
    query = request.args.get('query', '')
    books = search_books_in_db(query)
    return render_template('index.html', books=books)



def search_books_in_db(query):
    conn = sqlite3.connect('library.db', detect_types=sqlite3.PARSE_DECLTYPES)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute('SELECT * FROM Books WHERE book_name LIKE ?', ('%' + query + '%',))
    books = c.fetchall()
    conn.close()
    return books



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
