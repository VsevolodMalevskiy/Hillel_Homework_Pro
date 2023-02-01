from flask import Flask, request
import sqlite3 as sq
from serializers import serialize_book

app = Flask(__name__)


def all_books():
    with sq.connect("books.db") as data_base:
        cur = data_base.cursor()
        response = cur.execute("select * from books").fetchall()
        data_base.commit()
        books_representation = []
        for item in response:
            books_representation.append(serialize_book(item))
        cur.close()
        return books_representation

def create_book():
    body = request.json

    book_name = body["name"]

    if book_name == "":
        return {"error": "Book name cannot be empty"}, 400
    with sq.connect("books.db") as data_base:
        cur = data_base.cursor()
        cur.execute(f"insert into books (name) values ('{book_name}')")
        data_base.commit()
        cur.close()
    return "OK"


def get_book(book_id):
    with sq.connect("books.db") as data_base:
        cur = data_base.cursor()
        response = cur.execute(f"select * from books where books_id={book_id}")
        book_representation = response.fetchone()
        data_base.commit()
        cur.close()

    if book_representation is None:
        return {"error": "Book not found"}, 404

    return serialize_book(book_representation)


def delete_book(book_id):
    with sq.connect("books.db") as data_base:
        cur = data_base.cursor()
        cur.execute(f"delete from books where books_id={book_id}")
        data_base.commit()
        cur.close()

    # No Content
    return "", 204


def rename_book(book_id):
    body = request.json
    book_name = body["name"]
    if book_name == "":
        return {"error": "Book name cannot be empty"}, 400

    with sq.connect("books.db") as data_base:
        cur = data_base.cursor()
        # Запрос на все находящиеся в БД книги для проверки на совпадение
        match_check = cur.execute(f"select Name from books").fetchall()
        # Поиск книги по id
        response = cur.execute(f"select * from books where books_id={book_id}").fetchone()
        data_base.commit()
    if response is None:
        return {"error": "Book not found"}, 404
    # проверка на отсутствия книги в БД
    else:
        if (book_name,) in match_check:
            return {"error": "a book with that name exists"}
        else:
            cur.execute(f"UPDATE books set Name = '{book_name}' WHERE books_id = {book_id}")
            data_base.commit()
            return {"good": f"{match_check}"}

# Вариант 2. Создание БД с уникальными занчениями книг (creation_db_unique.db)
# def rename_book(book_id):
#     body = request.json
#     book_name = body["name"]
#     if book_name == "":
#         return {"error": "Book name cannot be empty"}, 400
#
#     with sq.connect("books.db") as data_base:
#         cur = data_base.cursor()
#         response = cur.execute(f"select * from books where books_id={book_id}").fetchone()
#         data_base.commit()
#     if response is None:
#         return {"error": "Book not found"}, 404
#     else:
#         try:
#             cur.execute(f"UPDATE books set Name = '{book_name}' WHERE books_id = {book_id}")
#             data_base.commit()
#             return {"good": "The book has been updated"}
#         except:
#             return {"error": "There is a book with the same name in the database"}


@app.route("/books", methods=["GET", "POST"])
def books():
    try:
        if request.method == "GET":
            return all_books()
        elif request.method == "POST":
            return create_book()
    finally:
        pass


@app.route("/books/<int:book_id>", methods=["GET", "PUT", "PATCH", "DELETE"])
def book(book_id):

    if request.method == "GET":
        return get_book(book_id)
    elif request.method == "PUT":
        return rename_book(book_id)
    elif request.method == "PATCH":
        return "book partial update will be there"
    elif request.method == "DELETE":
        return delete_book(book_id)


if __name__ == "__main__":
    app.run(port=5001, debug=True)
