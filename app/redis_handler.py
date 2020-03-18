"""
This module provides the functionality needed to interact with Redis cache collecting frequently accessed books.
"""
import json


def get_book_redis_by_title(redis_client, title):
    """
    Search in Redis for a book with the given title
    :param redis_client:
    :param title:
    :return: None if no book is stored, the book otherwise
    """
    book = redis_client.get(title)
    if book is None:
        return None
    return json.loads(book)


def add_book_redis(redis_client, book):
    """
    Store a book in Redis stringify-ing it.
    :param redis_client:
    :param book:
    :return: True if the update is successful, False otherwise
    """
    return redis_client.set(book['title'], json.dumps(book))
