# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FilmItem(scrapy.Item):
    name = scrapy.Field()
    country = scrapy.Field()
    rating = scrapy.Field()
    duration = scrapy.Field()
    year = scrapy.Field()
    comments_count = scrapy.Field()
    genre = scrapy.Field()
    record_type = scrapy.Field()
    pass
