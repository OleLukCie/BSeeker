import os
import json
import hashlib
import re

from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class DuplicateFilterPipeline:
    def __init__(self):
        self.seen = set()

    def process_item(self, item):
        adapter = ItemAdapter(item)
        url = adapter.get('url', '')
        match = re.search(r'([\w-]+_\d+)', url)
        book_id = match.group(1) if match else url
        sig = hashlib.md5(book_id.encode('utf-8')).hexdigest()
        if sig in self.seen:
            raise DropItem('Duplicate: %s' % adapter.get('title'))
        self.seen.add(sig)
        return item


class CleanDataPipeline:
    def process_item(self, item):
        adapter = ItemAdapter(item)
        title = adapter.get('title', '')
        if title:
            adapter['title'] = title.strip()
        author = adapter.get('author', '')
        if author:
            adapter['author'] = author.strip()
        publisher = adapter.get('publisher', '')
        if publisher:
            adapter['publisher'] = publisher.strip()
        price = adapter.get('price', '')
        if price:
            p = re.sub(r'[^\d.]', '', str(price))
            try:
                adapter['price'] = float(p)
            except ValueError:
                adapter['price'] = 0.0
        rating = adapter.get('rating', '')
        if rating:
            r = str(rating).replace('分', '').strip()
            try:
                adapter['rating'] = float(r)
            except ValueError:
                adapter['rating'] = 0.0
        sales = adapter.get('sales', '')
        if sales:
            s = str(sales).replace('人购买', '').replace('+', '').replace(',', '').strip()
            try:
                adapter['sales'] = int(s)
            except ValueError:
                adapter['sales'] = 0
        return item


class SaveToJsonPipeline:
    def __init__(self):
        self.items = []
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        raw_path = os.path.join(base, 'data', 'raw')
        os.makedirs(raw_path, exist_ok=True)
        self.filepath = os.path.join(raw_path, 'books_raw.json')

    def process_item(self, item):
        self.items.append(dict(ItemAdapter(item)))
        return item

    def close_spider(self, spider):
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(self.items, f, ensure_ascii=False, indent=2)
        spider.logger.info('Saved %d items to %s' % (len(self.items), self.filepath))