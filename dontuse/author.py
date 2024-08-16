import sqlite3

def update_books_data():
    # Connect to the SQLite database
    conn = sqlite3.connect('library.db')
    c = conn.cursor()

    # Define the data to be updated
    books = [
        (1, "Robert Kiyosaki"),
        (2, "J.K. Rowling"),
        (3, "Mark Manson"),
        (4, "Mark Manson")
    ]

    # Update the Books table with author information
    c.executemany('''
        UPDATE Books
        SET author = ?
        WHERE id = ?
    ''', [(author, book_id) for book_id, author in books])

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

if __name__ == '__main__':
    update_books_data()
