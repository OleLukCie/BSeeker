import os
import sys

base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, base)

# Import Flask core utilities and CORS for cross-origin support
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

# Import database functions for book data and statistics
from database.db import init_db, get_stats, get_all_books, get_price_distribution, get_rating_distribution

# Initialize Flask application: serve static files from the current directory
app = Flask(__name__, static_folder='.')

# Enable Cross-Origin Resource Sharing (CORS) to allow frontend requests
CORS(app)


@app.route('/')
def index():
    '''
    Serve the main frontend HTML page (index.html)
    Returns:
        The index.html file from the static directory
    '''
    return send_from_directory('.', 'index.html')


@app.route('/api/stats')
def api_stats():
    '''
    API endpoint to get overall book statistics (total books, avg price, avg rating, top categories, etc.)
    
    Returns:
        JSON: Book statistics data
    '''
    init_db() # Ensure database is initialized
    return jsonify(get_stats()) # Fetch stats and return as JSON response


@app.route('/api/books')
def api_books():
    '''
    API endpoint to fetch paginated list of all books
    
    Query Parameters:
        limit (int): Max number of books to return (default: 100)
        offset (int): Pagination offset (default: 0)
    
    Returns:
        JSON: List of books
    '''
    init_db()
    # Get pagination parameters from request URL
    limit = request.args.get('limit', 100, type=int)
    offset = request.args.get('offset', 0, type=int)
    # Return paginated books as JSON
    return jsonify(get_all_books(limit=limit, offset=offset))


@app.route('/api/price_distribution')
def api_price_distribution():
    '''
    API endpoint to get book price distribution by range (0-10, 10-20, etc.)
    
    Returns:
        JSON: Price distribution data
    '''
    init_db()
    return jsonify(get_price_distribution())


@app.route('/api/rating_distribution')
def api_rating_distribution():
    '''
    API endpoint to get book rating distribution (count per rating value)
    
    Returns:
        JSON: Rating distribution data
    '''
    init_db()
    return jsonify(get_rating_distribution())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)