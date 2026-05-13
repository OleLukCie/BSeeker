import scrapy


class BookItem(scrapy.Item):
    title = scrapy.Field()
    author = scrapy.Field()
    publisher = scrapy.Field()
    price = scrapy.Field()
    rating = scrapy.Field()
    sales = scrapy.Field()
    url = scrapy.Field()
    category = scrapy.Field()
