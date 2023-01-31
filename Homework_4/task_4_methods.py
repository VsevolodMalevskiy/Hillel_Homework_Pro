from flask import Flask, request
import sqlite3 as sq
from serializers import serialize_book

app = Flask(__name__)


@app.route("/books", methods=["GET", "POST"])
def books():
    with sq.connect("books.db") as data_base:
        try:
            if request.method == "GET":
                cur = data_base.cursor()
                response = cur.execute("select * from books").fetchall()
                data_base.commit()
                books_representation = []
                for item in response:
                    books_representation.append(serialize_book(item))
                return books_representation

            elif request.method == "POST":
                cur = data_base.cursor()
                response = cur.execute("select * from books").fetchall()
                data_base.commit()
                books_representation = []
                for item in response:
                    books_representation.append(serialize_book(item))
                return books_representation
        finally:
            cur.close()



if __name__ == "__main__":
    app.run(port=5001, debug=True)