"""
This module implements a trivial Flask-based web service with two entry points:
POST /book adds a book with the given author and title
GET /book/:title returns the book with the given title
The title is assumed to identify uniquely the book.
"""
import os
import redis
import pymongo as pymongo
from flask import Flask, request, jsonify
from pymongo.errors import PyMongoError

from mongo_handler import add_book_mongo, get_book_mongo_by_title
from redis_handler import get_book_redis_by_title, add_book_redis

app = Flask(__name__)
#  Establish connection with the storage layer of the application
mongo_client = pymongo.MongoClient(os.getenv('MONGO_URL', 'localhost:27017'))
redis_client = redis.Redis(host=os.getenv('REDIS_HOST', 'localhost'), port=os.getenv('REDIS_PORT', '6379'),
                           decode_responses=True)


@app.route('/book', methods=['POST'])
def post_book():
    """
    Create a book document and stores it in the Mongo database
    :return: An HTTP Code representing the outcome of the creation
    """
    try:
        book = {'title': request.json['title'], 'author': request.json['author']}
        add_book_mongo(mongo_client, book)
        return jsonify(book), 201  # Created
    except PyMongoError:
        return '', 500  # Internal Server Error


@app.route('/book/<title>', methods=['GET'])
def get_book(title):
    """
    Search for a book with the given title. Namely, at first the Redis cached is searched. If no book is found inside
    Redis, the book is searched in the Mongo database.
    :param title:
    :return: An HTTP Code representing the outcome of the research.
    """
    try:
        book = get_book_redis_by_title(redis_client, title)
        if book is None:  # Cache miss: search for book in Mongo
            book = get_book_mongo_by_title(mongo_client, title)
            if book is None:
                return '', 404  # Not Found
            else:  # Book found in Mongo: cache update
                add_book_redis(redis_client, book)
                return jsonify(book)
        else:  # Cache hit: the book is returned to the client
            return jsonify(book)
    except PyMongoError:
        return '', 500  # Internal Server Error


if __name__ == '__main__':
    host = os.getenv('LISTEN_IP', '0.0.0.0')
    port = int(os.getenv('LISTEN_PORT', '5000'))
    app.run(host=host, port=port, threaded=True)
