# BSeeker\database\db.py
# J.C.  2026.5.14

import os
import sqlite3
import json
from datetime import datetime # date operation


def get_db_path():
    '''
    Get the full path to the SQLite database file.
    Creates the database directory if it does not exist.

    Returns: str: Full path to bseeker.db
    '''
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_dir = os.path.join(base, 'data', 'db')
    os.makedirs(db_dir, exist_ok=True)
    return os.path.join(db_dir, 'bseeker.db')


def get_connection():
    '''
    Create and return a connection to the SQLite database.
    Uses sqlite3.Row to access columns by name.

    Returns: sqlite3.Connection: Database connection object
    '''
    conn = sqlite3.connect(get_db_path())
    # Enable row name access for easier query handling
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    '''
    Initialize the database by creating required tables and indexes.
    Creates: books table, crawl_logs table, and performance indexes.
    '''
    conn = get_connection()
    cursor = conn.cursor()

    # Main books table to store all book data
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT,
            publisher TEXT,
            price REAL DEFAULT 0,
            rating REAL DEFAULT 0,
            sales INTEGER DEFAULT 0,
            url TEXT,
            category TEXT,
            source TEXT DEFAULT 'scrapy',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Table to log crawling job history and statistics
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS crawl_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            crawl_time TEXT DEFAULT CURRENT_TIMESTAMP,
            total_pages INTEGER DEFAULT 0,
            total_items INTEGER DEFAULT 0,
            finish_reason TEXT,
            stats TEXT
        )
    ''')

    # Create indexes to speed up frequent queries
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_books_title ON books(title)
    ''')
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_books_category ON books(category)
    ''')
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_books_price ON books(price)
    ''')

    # Save changes and close connection
    conn.commit()
    conn.close()


def import_from_json(json_path=None):
    '''
    Import book data from the raw JSON file into the SQLite database.
    Uses INSERT OR IGNORE to avoid duplicate entries.

    Args:
        json_path (str): Custom path to JSON file (uses default if None)

    Returns:
        int: Number of new books inserted into the database
    '''
    # Use default JSON path if none is provided
    if json_path is None:
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        json_path = os.path.join(base, 'data', 'raw', 'books_raw.json')

    # Return 0 if JSON file does not exist
    if not os.path.exists(json_path):
        return 0

    # Load book data from JSON file
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)


    conn = get_connection()
    cursor = conn.cursor()
    inserted = 0

    # Insert each book item into the database
    for item in data:
        cursor.execute('''
            INSERT OR IGNORE INTO books (title, author, publisher, price, rating, sales, url, category, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            item.get('title', ''),
            item.get('author', ''),
            item.get('publisher', ''),
            item.get('price', 0),
            item.get('rating', 0),
            item.get('sales', 0),
            item.get('url', ''),
            item.get('category', ''),
            'scrapy'
        ))
        # Count successful insertions
        if cursor.rowcount > 0:
            inserted += 1

    # Save changes and close connection
    conn.commit()
    conn.close()
    return inserted


def get_all_books(limit=100, offset=0):
    '''
    Fetch a paginated list of all books from the database, sorted by newest first.

    Args:
        limit (int): Max number of books to return
        offset (int): Pagination offset

    Returns:
        list: List of book dictionaries
    '''
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM books ORDER BY id DESC LIMIT ? OFFSET ?', (limit, offset))
    rows = cursor.fetchall()
    conn.close()
    # Convert sqlite3.Row objects to standard dictionaries
    return [dict(row) for row in rows]


def get_book_by_id(book_id):
    '''
    Fetch a single book by its database ID.

    Args:
        book_id (int): ID of the book

    Returns:
        dict or None
    '''
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM books WHERE id = ?', (book_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def get_stats():
    '''
    Get overall statistics for the book database.

    Returns:
        dict: Total books, average price, average rating, top categories, top publishers
    '''
    conn = get_connection()
    cursor = conn.cursor()

    # Total number of books
    cursor.execute('SELECT COUNT(*) as total FROM books')
    total = cursor.fetchone()['total']

    # Average book price
    cursor.execute('SELECT AVG(price) as avg_price FROM books')
    avg_price = cursor.fetchone()['avg_price']

    # Average book rating
    cursor.execute('SELECT AVG(rating) as avg_rating FROM books')
    avg_rating = cursor.fetchone()['avg_rating']

    # Top 10 categories by book count
    cursor.execute('SELECT category, COUNT(*) as count FROM books GROUP BY category ORDER BY count DESC LIMIT 10')
    categories = [dict(row) for row in cursor.fetchall()]

    # Top 10 publishers by book count (exclude empty values)
    cursor.execute('SELECT publisher, COUNT(*) as count FROM books WHERE publisher != "" GROUP BY publisher ORDER BY count DESC LIMIT 10')
    publishers = [dict(row) for row in cursor.fetchall()]

    conn.close()

    # Return formatted statistics
    return {
        'total_books': total,
        'avg_price': round(avg_price, 2) if avg_price else 0,
        'avg_rating': round(avg_rating, 2) if avg_rating else 0,
        'top_categories': categories,
        'top_publishers': publishers
    }


def get_price_distribution():
    '''
    Calculate and return book price distribution grouped by price ranges.

    Returns:
        list: List of dictionaries with price range and book count
    '''
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT 
            CASE 
                WHEN price < 10 THEN '0-10'
                WHEN price < 20 THEN '10-20'
                WHEN price < 30 THEN '20-30'
                WHEN price < 40 THEN '30-40'
                WHEN price < 50 THEN '40-50'
                ELSE '50+'
            END as range,
            COUNT(*) as count
        FROM books
        GROUP BY range
        ORDER BY range
    ''')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_rating_distribution():
    '''
    Get the count of books for each rating value.

    Returns:
        list: List of dictionaries with rating and count
    '''
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT rating, COUNT(*) as count FROM books GROUP BY rating ORDER BY rating')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def delete_all_books():
    # Delete all book records from the database
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM books')
    conn.commit()
    conn.close()


# Run database initialization and import when this script is executed directly
if __name__ == '__main__':
    init_db()
    count = import_from_json()
    print('Imported %d books' % count)