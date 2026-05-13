import scrapy
import os
import sys

base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, base)

from bseeker.items import BookItem
from bseeker.utils.config import get, get_int


class BookSpider(scrapy.Spider):
    name = 'book_spider'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['https://books.toscrape.com/']

    custom_settings = {
        'CLOSESPIDER_PAGECOUNT': get_int('MAX_PAGES', 50),
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        ua = get('USER_AGENT')
        if ua:
            self.custom_settings['USER_AGENT'] = ua

    def parse(self, response):
        for book in response.css('article.product_pod'):
            item = BookItem()
            item['title'] = book.css('h3 a::attr(title)').get('')
            item['author'] = ''
            item['publisher'] = ''
            price_text = book.css('p.price_color::text').get('')
            item['price'] = price_text
            rating_class = book.css('p.star-rating::attr(class)').get('')
            rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
            rating_word = rating_class.split()[-1] if rating_class else 'Zero'
            item['rating'] = rating_map.get(rating_word, 0)
            item['sales'] = 0
            item['url'] = response.urljoin(book.css('h3 a::attr(href)').get(''))
            item['category'] = response.css('ul.breadcrumb li:nth-child(3) a::text').get('')
            yield item

        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
