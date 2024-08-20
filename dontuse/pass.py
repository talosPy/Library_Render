import sqlite3

def add_password_column():
    # Connect to the SQLite database
    conn = sqlite3.connect('library.db')
    c = conn.cursor()

    # Add the password column to the Members table
    c.execute('''
        ALTER TABLE Members
        ADD COLUMN password TEXT
    ''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

if __name__ == '__main__':
    add_password_column()
