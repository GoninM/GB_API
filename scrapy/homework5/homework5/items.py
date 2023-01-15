# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Homework5Item(scrapy.Item):
    name = scrapy.Field()

    url = scrapy.Field()

    salary_min = scrapy.Field()
    salary_max = scrapy.Field()
    salary_currency = scrapy.Field()
    salary_tax = scrapy.Field()
    salary_raw = scrapy.Field()

    company_name = scrapy.Field()
    company_name_raw = scrapy.Field()

    _id = scrapy.Field()
