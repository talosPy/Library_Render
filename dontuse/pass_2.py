import sqlite3
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def alter_table_and_update_password():
    # Connect to the SQLite database
    conn = sqlite3.connect('library.db')
    c = conn.cursor()

    try:
        # Alter the Members table to add the password column
        c.execute('ALTER TABLE Members ADD COLUMN password TEXT')
    except sqlite3.OperationalError as e:
        if "duplicate column name: password" in str(e):
            print("Column 'password' already exists.")
        else:
            raise

    # Hash the password '123456' for Talos
    hashed_password = hash_password('123456')

    # Update the password for Talos
    c.execute('''
        UPDATE Members
        SET password = ?
        WHERE member_name = ?
    ''', (hashed_password, 'Talos'))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

    print("Password for Talos has been updated successfully.")

if __name__ == '__main__':
    alter_table_and_update_password()
