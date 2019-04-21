# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BaiduItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ImageItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    search_word = scrapy.Field()
    image_url=scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    referer=scrapy.Field()
    img_path=scrapy.Field()
    detail_url=scrapy.Field()
    pass

class ImageItemDetail(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    search_word = scrapy.Field()
    image_url=scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    referer=scrapy.Field()
    img_path=scrapy.Field()
    detail_url=scrapy.Field()
    pass