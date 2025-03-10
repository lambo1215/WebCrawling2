from scrapy.spiders import SitemapSpider
from book_crawler.items import BookItem
import re

class ChitaiGorodSpider(SitemapSpider):
    name = 'chitai_gorod'
    allowed_domains = ['chitai-gorod.ru']
    
    # Use the sitemap to find book URLs
    sitemap_urls = ['https://www.chitai-gorod.ru/sitemap.xml']
    
    # Only follow book product pages
    sitemap_rules = [
        ('/product/', 'parse_book'),
    ]

    def parse_book(self, response):
        item = BookItem()
        
        # Extract required fields using XPath
        item['title'] = response.xpath('//h1[@itemprop="name"]/text()').get()
        item['isbn'] = response.xpath('//span[@itemprop="isbn"]/text()').get()
        item['source_url'] = response.url
        
        # Extract publication year from various possible locations
        year_text = response.xpath('//span[contains(text(), "Год издания")]/following-sibling::span/text()').get()
        if year_text:
            item['publication_year'] = re.search(r'\d{4}', year_text).group(0)
        
        # Extract pages count
        pages_text = response.xpath('//span[contains(text(), "Количество страниц")]/following-sibling::span/text()').get()
        if pages_text:
            item['pages_cnt'] = re.search(r'\d+', pages_text).group(0)
        
        # Extract optional fields
        item['author'] = response.xpath('//a[@itemprop="author"]/text()').get()
        item['description'] = response.xpath('//div[@itemprop="description"]//text()').getall()
        
        item['price_amount'] = response.xpath('//span[@itemprop="price"]/@content').get()
        item['price_currency'] = response.xpath('//span[@itemprop="priceCurrency"]/@content').get()
        
        item['rating_value'] = response.xpath('//meta[@itemprop="ratingValue"]/@content').get()
        item['rating_count'] = response.xpath('//meta[@itemprop="reviewCount"]/@content').get()
        
        item['publisher'] = response.xpath('//span[contains(text(), "Издательство")]/following-sibling::span/a/text()').get()
        item['book_cover'] = response.xpath('//img[@itemprop="image"]/@src').get()
        
        yield item
