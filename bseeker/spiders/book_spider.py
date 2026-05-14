# BSeeker\spiders\book_spider.py
# J.C.  2026.5.14

import scrapy
import os
import sys

# Add the project root directory to Python's module search path
# This allows importing custom modules from the bseeker package
base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, base)

# Import custom item definition and config utilities
from bseeker.items import BookItem
from bseeker.utils.config import get, get_int


class BookSpider(scrapy.Spider):
    '''
    Extracts: title, author, publisher, price, rating, sales, URL, and category
    '''

    name = 'book_spider'

    # Restrict crawling to this domain only
    allowed_domains = ['books.toscrape.com']

    # First URL to start crawling from
    start_urls = ['https://books.toscrape.com/']

    # Custom Scrapy settings for this spider
    custom_settings = {
        # Stop crawling after reaching the maximum page limit (from config or default 50)
        'CLOSESPIDER_PAGECOUNT': get_int('MAX_PAGES', 50),
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Load custom User-Agent from configuration if available
        ua = get('USER_AGENT')
        if ua:
            self.custom_settings['USER_AGENT'] = ua

    def parse(self, response):
        '''
        Extract book data from the current page
        and follow pagination links to continue crawling

        Args: response: Scrapy response object containing page HTML
        Yields: BookItem: Extracted book data item
        '''

        # Loop through all book products on the current page
        for book in response.css('article.product_pod'):
            # Initialize a new BookItem to store extracted data
            item = BookItem()

            # Extract book title
            item['title'] = book.css('h3 a::attr(title)').get('')

            # Author and publisher fields not available on this site - set empty defaults
            item['author'] = ''
            item['publisher'] = ''

            # Extract raw price text (includes currency symbol)
            price_text = book.css('p.price_color::text').get('')
            item['price'] = price_text

            # Convert star rating text to numeric value
            rating_class = book.css('p.star-rating::attr(class)').get('')
            rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
            rating_word = rating_class.split()[-1] if rating_class else 'Zero'
            item['rating'] = rating_map.get(rating_word, 0)

            # Sales data not available - set default to 0
            item['sales'] = 0

            # Build full book detail URL
            item['url'] = response.urljoin(book.css('h3 a::attr(href)').get(''))

            # Extract book category
            item['category'] = response.css('ul.breadcrumb li:nth-child(3) a::text').get('')

            # Yield the completed book item
            yield item

        # Handle pagination: find and follow the next page link
        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
