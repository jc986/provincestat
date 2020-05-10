# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AreaItem(scrapy.Item):
    # 北京11 浙江33
    areaid = scrapy.Field()
    #浙江330000000000
    areacode = scrapy.Field()
    areaname = scrapy.Field()
    link = scrapy.Field()
    #省份level=1 地市level=2 县level=3
    level = scrapy.Field()
    #上级areaid
    pareaid = scrapy.Field()