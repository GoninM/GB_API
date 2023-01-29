# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Homework8Item(scrapy.Item):
    vacancy_name = scrapy.Field()
    vacancy_description = scrapy.Field()
    vacancy_salary_amount = scrapy.Field()
    vacancy_positions_count = scrapy.Field()
    vacancy_salary_period = scrapy.Field()
    vacancy_state = scrapy.Field()
    vacancy_positions_last = scrapy.Field()
    vacancy_test_job = scrapy.Field()
    vacancy_city = scrapy.Field()
    vacancy_salary_min = scrapy.Field()
    vacancy_salary_max = scrapy.Field()
    company_name = scrapy.Field()
    company_contract_signed = scrapy.Field()
    company_name_description = scrapy.Field()
    _id = scrapy.Field()


