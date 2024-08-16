from flask import Flask, render_template
import sqlite3


app = Flask(__name__)




def get_books():
    # Connect to the SQLite database
    conn = sqlite3.connect('library.db', detect_types=sqlite3.PARSE_DECLTYPES)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    # Fetch all books
    c.execute('SELECT * FROM Books')
    books = c.fetchall()
    
    # Close the connection
    conn.close()
    
    return books



@app.route('/')
def index():
    books = get_books()
    return render_template('index.html', books=books)





if __name__ == '__main__':
    app.run(debug=True)
