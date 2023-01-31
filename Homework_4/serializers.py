def serialize_book(book_db_representation):
    return {
        "id": book_db_representation[0],
        "name": book_db_representation[1]
    }
