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


@app.route("/books", methods=["GET", "POST"])
def books():
    try:
        if request.method == "GET":
            return all_books()
        elif request.method == "POST":
            return all_books()
    finally:
        pass


if __name__ == "__main__":
    app.run(port=5001, debug=True)