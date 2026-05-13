import os
import sys

base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, base)

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from database.db import init_db, get_stats, get_all_books, get_price_distribution, get_rating_distribution

app = Flask(__name__, static_folder='.')
CORS(app)


@app.route('/')
def index():
    return send_from_directory('.', 'index.html')


@app.route('/api/stats')
def api_stats():
    init_db()
    return jsonify(get_stats())


@app.route('/api/books')
def api_books():
    init_db()
    limit = request.args.get('limit', 100, type=int)
    offset = request.args.get('offset', 0, type=int)
    return jsonify(get_all_books(limit=limit, offset=offset))


@app.route('/api/price_distribution')
def api_price_distribution():
    init_db()
    return jsonify(get_price_distribution())


@app.route('/api/rating_distribution')
def api_rating_distribution():
    init_db()
    return jsonify(get_rating_distribution())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)