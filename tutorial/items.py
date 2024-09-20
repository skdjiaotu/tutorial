# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    code = scrapy.Field()
    price = scrapy.Field()
    gain_fall_price_ratio = scrapy.Field()
    gain_fall_price = scrapy.Field()
    turnover = scrapy.Field()
    pass
