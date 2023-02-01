import sqlite3 as sq


def creation_db(data_books):
    with sq.connect("books.db") as data_base:
        cur = data_base.cursor()


        cur.execute("""CREATE TABLE IF NOT EXISTS books(
            books_id INTEGER PRIMARY KEY AUTOINCREMENT,
            Name NVARCHAR(30) UNIQUE NOT NULL         
        );""")
        data_base.commit()

    table_insert = """INSERT INTO books (Name)
                  VALUES (?);"""

    cur.executemany(table_insert, data_books)
    data_base.commit()
    cur.close()


books = [("Mr. Bean In Town",), ("The Million Pound Bank Note",), ("The Picture of Dorian Gray",), ("Forrest Gump",),
         (" Three Men In a Boat",), ("Dracula",)]

creation_db(books)
