# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ApipicturesItem(scrapy.Item):
    media = scrapy.Field()
    sectionTitle = scrapy.Field()
    pubDate = scrapy.Field()
    pageUrl = scrapy.Field()
    caption = scrapy.Field()
    location = scrapy.Field()
    author = scrapy.Field()
    credits = scrapy.Field()
    picture = scrapy.Field()
    pictureEditor = scrapy.Field()
