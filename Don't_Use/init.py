import sqlite3
from datetime import datetime, timedelta

# Custom adapter and converter for DATE type
def adapt_date(date_obj):
    return date_obj.isoformat()

def convert_date(date_bytes):
    return datetime.strptime(date_bytes.decode(), "%Y-%m-%d").date()

# Register the adapters and converters
sqlite3.register_adapter(datetime, adapt_date)
sqlite3.register_converter("DATE", convert_date)

def init_db():
    # Connect to the SQLite database
    conn = sqlite3.connect('library.db', detect_types=sqlite3.PARSE_DECLTYPES)
    c = conn.cursor()

    # Create the Books table with quantity
    c.execute('''
        CREATE TABLE IF NOT EXISTS Books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_name TEXT NOT NULL,
            year TEXT NOT NULL,
            image TEXT,
            quantity INTEGER NOT NULL
        )
    ''')

    # Create the Members table
    c.execute('''
        CREATE TABLE IF NOT EXISTS Members (
            id INTEGER PRIMARY KEY,
            member_name TEXT NOT NULL,
            email TEXT UNIQUE
        )
    ''')

    # Create the Loans table
    c.execute('''
        CREATE TABLE IF NOT EXISTS Loans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER NOT NULL,
            member_id INTEGER NOT NULL,
            loan_date DATE NOT NULL,
            due_date DATE NOT NULL,
            return_date DATE,
            FOREIGN KEY (book_id) REFERENCES Books(id),
            FOREIGN KEY (member_id) REFERENCES Members(id)
        )
    ''')

    # Insert initial data into Books table
    books = [
        {
            "id": 1,
            "book_name": "Rich Dad, Poor Dad",
            "year": "1998",
            "image": "https://upload.wikimedia.org/wikipedia/en/thumb/b/b9/Rich_Dad_Poor_Dad.jpg/220px-Rich_Dad_Poor_Dad.jpg",
            "quantity": 5
        },
        {
            "id": 2,
            "book_name": "Harry Potter",
            "year": "2005",
            "image": "https://upload.wikimedia.org/wikipedia/en/thumb/b/b5/Harry_Potter_and_the_Half-Blood_Prince_cover.png/220px-Harry_Potter_and_the_Half-Blood_Prince_cover.png",
            "quantity": 3
        },
        {
            "id": 3,
            "book_name": "Everything is Fucked",
            "year": "2012",
            "image": "https://upload.wikimedia.org/wikipedia/en/thumb/b/b6/Book_cover_for_Everything_is_Fucked_a_Book_about_Hope_by_Mark_Manson.jpeg/220px-Book_cover_for_Everything_is_Fucked_a_Book_about_Hope_by_Mark_Manson.jpeg",
            "quantity": 7
        },
        {
            "id": 4,
            "book_name": "How to not give a Fuck",
            "year": "2015",
            "image": "https://upload.wikimedia.org/wikipedia/en/thumb/b/bd/The_Subtle_Art_of_Not_Giving_a_F%2Ack_by_Mark_Manson_-_Book_Cover.png/220px-The_Subtle_Art_of_Not_Giving_a_F%2Ack_by_Mark_Manson_-_Book_Cover.png",
            "quantity": 2
        }
    ]
    c.executemany('''
        INSERT INTO Books (id, book_name, year, image, quantity)
        VALUES (?, ?, ?, ?, ?)
    ''', [(book['id'], book['book_name'], book['year'], book['image'], book['quantity']) for book in books])

    # Insert initial data into Members table
    members = [
        {
            "id": 1,
            "member_name": "Talos",
            "email": "Talos@example.com"
        },
        {
            "id": 2,
            "member_name": "Bob",
            "email": "bob@example.com"
        },
        {
            "id": 3,
            "member_name": "Charlie",
            "email": "charlie@example.com"
        },
        {
            "id": 4,
            "member_name": "Diana",
            "email": "diana@example.com"
        }
    ]
    c.executemany('''
        INSERT INTO Members (id, member_name, email)
        VALUES (?, ?, ?)
    ''', [(member['id'], member['member_name'], member['email']) for member in members])

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

def add_loan(book_id, member_id):
    # Connect to the SQLite database
    conn = sqlite3.connect('library.db', detect_types=sqlite3.PARSE_DECLTYPES)
    c = conn.cursor()

    # Calculate the loan_date as today's date and due_date as 10 days later
    loan_date = datetime.now().date()
    due_date = loan_date + timedelta(days=10)

    # Check if there are available copies of the book
    c.execute('SELECT quantity FROM Books WHERE id = ?', (book_id,))
    result = c.fetchone()
    
    if result is None or result[0] <= 0:
        print("No available copies of the book.")
        conn.close()
        return

    # Insert the loan record
    c.execute('''
        INSERT INTO Loans (book_id, member_id, loan_date, due_date)
        VALUES (?, ?, ?, ?)
    ''', (book_id, member_id, loan_date, due_date))

    # Update the quantity of the book
    c.execute('''
        UPDATE Books
        SET quantity = quantity - 1
        WHERE id = ?
    ''', (book_id,))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()

    # Example usage: Adding a loan for book_id 1 and member_id 1
    add_loan(1, 1)
