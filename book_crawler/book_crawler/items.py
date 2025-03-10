import scrapy

class BookItem(scrapy.Item):
    title = scrapy.Field()  # Required
    author = scrapy.Field()  # Optional
    description = scrapy.Field()  # Optional
    price_amount = scrapy.Field()  # Optional
    price_currency = scrapy.Field()  # Optional
    rating_value = scrapy.Field()  # Optional
    rating_count = scrapy.Field()  # Optional
    publication_year = scrapy.Field()  # Required
    isbn = scrapy.Field()  # Required
    pages_cnt = scrapy.Field()  # Required
    publisher = scrapy.Field()  # Optional
    book_cover = scrapy.Field()  # Optional
    source_url = scrapy.Field()  # Required
