import sqlite3

def add_author_column():
    # Connect to the SQLite database
    conn = sqlite3.connect('library.db')
    c = conn.cursor()

    # Add the author column to the Books table
    c.execute('''
        ALTER TABLE Books
        ADD COLUMN author TEXT
    ''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

if __name__ == '__main__':
    add_author_column()
