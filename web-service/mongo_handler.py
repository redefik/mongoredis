"""
This module provides the functionality needed to interact with Mongo database collecting
books.
"""


def add_book_mongo(mongo_client, book):
    """
    Adds a book into the Mongo database
    :return:
    """
    db = mongo_client.library
    books = db.books
    books.insert_one(book)
    book.pop('_id')
    return


def get_book_mongo_by_title(mongo_client, title):
    """
    Searches for the book with the given title and returns it
    :param mongo_client:
    :param title:
    :return: The dictionary representing the book, None otheriwse
    """
    db = mongo_client.library
    books = db.books
    book = books.find_one({'title': title})
    if book is None:
        return None
    book.pop('_id')
    return book
