"""
Simple Web Service that exposes two entry point:
POST /book adds a book with the given author and title
GET /book/:title returns the book with the given title
The title is assumed to identify uniquely the book.
"""
import os

import pymongo as pymongo
from flask import Flask, request, jsonify
from pymongo.errors import PyMongoError

from mongo_handler import add_book_mongo, get_book_mongo_by_title

app = Flask(__name__)
mongo_client = pymongo.MongoClient(os.getenv('MONGO_URL', 'localhost:27017'))


@app.route('/book', methods=['POST'])
def post_book():
    try:
        book = {'title': request.json['title'], 'author': request.json['author']}
        add_book_mongo(mongo_client, book)
        return jsonify(book), 201  # Created
    except PyMongoError:
        return '', 500  # Internal Server Error


@app.route('/book/<title>', methods=['GET'])
def get_book(title):
    try:
        book = get_book_mongo_by_title(mongo_client, title)
        if book is None:
            return '', 404  # Not Found
        return jsonify(book)  # Ok
    except PyMongoError:
        return '', 500  # Internal Server Error


if __name__ == '__main__':
    host = os.getenv('LISTEN_IP', '0.0.0.0')
    port = int(os.getenv('LISTEN_PORT', '5000'))
    app.run(host=host, port=port, threaded=True)
