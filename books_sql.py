import sqlite3
from collections import namedtuple

connection = sqlite3.connect("./books.db")

cursor = connection.cursor()

Book = namedtuple("Book", "id title author published_year is_loaned")

def set_up_table():
    sql = """
        CREATE TABLE books(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            author TEXT,
            published_year INTEGER,
            is_loaned INTEGER
        )"""
    cursor.execute("DROP TABLE IF EXISTS books")
    cursor.execute(sql)
    connection.commit()

set_up_table()

def insert_book(title, author, published_year, is_loaned):
    sql = """
        INSERT INTO books (
            title,
            author,
            published_year,
            is_loaned
        )
        VALUES
        (
        "{}", "{}", {}, {}
        )
        """.format(title, author, published_year, is_loaned)
    cursor.execute(sql)
    connection.commit()

insert_book("The Grapes of Wrath", "John Steinbeck", 1939, 0)
insert_book("Misery", "Stephen King", 1987, 0)

def get_all_books():
    sql = "SELECT * FROM books"
    rows = cursor.execute(sql)
    book_rows = rows.fetchall()
    return [Book(*book_row) for book_row in book_rows]

def search_books(title):
    sql = "SELECT * FROM books WHERE title = '{}'".format(title)
    row = cursor.execute(sql)
    book_row = row.fetchone()
    return Book(*book_row)

def update_book_loaned_status(id, status):
    sql = "UPDATE books SET is_loaned = {} WHERE id = {}".format(status, id)
    cursor.execute(sql)
    connection.commit()

while True:
    print("""
        Select an Option:
        1. List all books
        2. Find book by title
        3. Borrow book
        4. Return book
        """)
    choice = input()

    if choice == "1":
        all_books = get_all_books()
        for book in all_books:
            print("Id: {}, Title: {}, Author: {}, Year Published: {}, Is Loaned {}".format(*book))

    elif choice == "2":
        print("""
            Please enter a book title:
            """)
        title = input()

        book = search_books(title)
        print("Id: {}, Title: {}, Author: {}, Year Published: {}, Is Loaned {}".format(*book))

    elif choice == "3":
        print("""
            Please enter a book title to borrow:
        """)
        title = input()

        book = search_books(title)

        if book is not None:
            if book.is_loaned == 0:
                update_book_loaned_status(book.id, 1)
                print(f"You have borrowed {book.title}")
            else:
                print("Book already loaned")
        else:
            print(f"{title} not found")

    elif choice == "4":
        print("""
            Please enter a book title to return:
        """)
        title = input()

        book = search_books(title)

        if book is not None:
            if book.is_loaned == 1:
                update_book_loaned_status(book.id, 0)
                print(f"You have successfully returned {book.title}")
            else:
                print("Book already returned")
        else:
            print(f"{title} not found")
