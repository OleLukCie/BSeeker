# BSeeker\bseeker\pipelines.py
# J.C.  2026.5.14


import os   # file handling
import json     # JSON serialization
import hashlib  # hashing
import re       # regex

# Scrapy item adapter and exception for duplicate handling
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class DuplicateFilterPipeline:
    '''
    Scrapy Pipeline to filter and remove duplicate book items.
    Uses unique book ID extracted from URL to detect duplicates.
    Stores seen items in a set to prevent duplicates during crawling.
    '''
    def __init__(self):
        # Initialize a set to track unique item signatures
        self.seen = set()

    def process_item(self, item):
        '''
        Process each item to check for duplicates.
        Drops item if duplicate is detected.

        Args:
            item: Scrapy BookItem

        Returns:
            Original item if unique

        Raises:
            DropItem: If item is a duplicate
        '''
        adapter = ItemAdapter(item)
        # Get the book URL from item
        url = adapter.get('url', '')

        # Extract unique book ID from URL using regex
        match = re.search(r'([\w-]+_\d+)', url)
        book_id = match.group(1) if match else url

        # Create MD5 hash signature for the unique ID
        sig = hashlib.md5(book_id.encode('utf-8')).hexdigest()

        # Check if signature already exists
        if sig in self.seen:
            raise DropItem('Duplicate: %s' % adapter.get('title'))

        # Add new signature to the seen set
        self.seen.add(sig)
        return item


class CleanDataPipeline:
    '''
    Scrapy Pipeline to clean and standardize raw scraped data.
    - Trims whitespace from text fields
    - Converts price/rating/sales to proper numeric types
    - Remove extra symbols and text from numeric values
    '''
    def process_item(self, item):
        '''
        Clean all fields in the book items.
        '''
        adapter = ItemAdapter(item)

        # Clean title
        title = adapter.get('title', '')
        if title:
            adapter['title'] = title.strip()

        # Clean author
        author = adapter.get('author', '')
        if author:
            adapter['author'] = author.strip()

        # Clean publisher
        publisher = adapter.get('publisher', '')
        if publisher:
            adapter['publisher'] = publisher.strip()

        # Clean price
        price = adapter.get('price', '')
        if price:
            p = re.sub(r'[^\d.]', '', str(price))
            try:
                adapter['price'] = float(p)
            except ValueError:
                adapter['price'] = 0.0

        # Clean rating
        rating = adapter.get('rating', '')
        if rating:
            r = str(rating).replace('分', '').strip()
            try:
                adapter['rating'] = float(r)
            except ValueError:
                adapter['rating'] = 0.0

        # Clean sales
        sales = adapter.get('sales', '')
        if sales:
            s = str(sales).replace('人购买', '').replace('+', '').replace(',', '').strip()
            try:
                adapter['sales'] = int(s)
            except ValueError:
                adapter['sales'] = 0

        return item


class SaveToJsonPipeline:
    '''
    Scrapy Pipeline to collect all cleaned items and save them to a JSON file.
    Saves output to data/raw/books_raw.json when spider finishes.
    '''
    def __init__(self):
        # Initialize list to store all processed items
        self.items = []

        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        raw_path = os.path.join(base, 'data', 'raw')
        os.makedirs(raw_path, exist_ok=True)
        self.filepath = os.path.join(raw_path, 'books_raw.json')


    def process_item(self, item):
        '''
        Collect each processed item into a list
        '''
        self.items.append(dict(ItemAdapter(item)))
        return item


    def close_spider(self, spider):
        '''
        Save all collected items to JSON file when spider closes.
        Log the save result to the Scrapy logger.
        '''
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(self.items, f, ensure_ascii=False, indent=2)
        spider.logger.info('Saved %d items to %s' % (len(self.items), self.filepath))