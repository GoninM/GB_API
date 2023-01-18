# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst, Compose


def process_name(value):
    name = ''
    if value:
        name = value[0].replace('\n', '')
        name = name.rstrip().lstrip()
    return name


def process_price(value):
    price = 0
    currency = ''

    if value:
        price = int(value[0].replace(' ', ''))
        currency = value[1]

    return {'price': price, 'currency': currency}


def process_params(value):
    params = {}

    if value:
        for i in range(0, len(value), 2):
            param_key = value[i].replace('\n', '').rstrip().lstrip()
            param_value = value[i+1].replace('\n', '').rstrip().lstrip()
            params[param_key] = param_value

    return params

#как вытащить полноразмерную картинку:
#https://www.castorama.ru/upload/iblock/1e6/butpiupbeeeing18mx8ncahg1oq0pbal/1001437941_1.jpg
#https://www.castorama.ru/upload/resize_cache/iblock/1e6/butpiupbeeeing18mx8ncahg1oq0pbal/80_80_1/1001437941_1.jpg
# править но потребовалось оказывается подгружается и большая картинка в карусель. но мелкие тоже получается.


def process_photos(value):
    start_url = 'https://www.castorama.ru'
    result = []

    if value:
        for v in value:
            result.append(start_url + v)

    return result


class Homework6Item(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(input_processor=Compose(process_name), output_processor=TakeFirst())
    price = scrapy.Field(input_processor=Compose(process_price), output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    params = scrapy.Field(input_processor=Compose(process_params), output_processor=TakeFirst())
    photos = scrapy.Field(input_processor=Compose(process_photos))

    price_raw = scrapy.Field()
