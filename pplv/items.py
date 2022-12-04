import re

import scrapy
from itemloaders.processors import TakeFirst, MapCompose, Compose


def split_url_to_brand(value):
    return value.split("/")[2]


def find_year(value):
    for property_info in value:
        if property_info['filter']['name'] == 'Izlaiduma gads':
            year = property_info['value']['displayValue']
            return int(re.sub(r'[^0-9]', '', year))


def find_miles(value):
    for property_info in value:
        if property_info['filter']['name'] == 'Nobraukums, km':
            miles = property_info['textValue']
            return int(re.sub(r'[^0-9]', '', miles))


def find_vin(value):
    for property_info in value:
        if property_info['filter']['name'] == 'VIN kods':
            return property_info['textValue']


def find_plate(value):
    for property_info in value:
        if property_info['filter']['name'] == 'Auto numurs':
            return property_info['textValue']


class PplvItem(scrapy.Item):
    brand = scrapy.Field(input_processor=MapCompose(split_url_to_brand), output_processor=TakeFirst())
    model = scrapy.Field(output_processor=TakeFirst())
    year = scrapy.Field(input_processor=Compose(find_year), output_processor=TakeFirst())
    miles = scrapy.Field(input_processor=Compose(find_miles), output_processor=TakeFirst())
    vin = scrapy.Field(input_processor=Compose(find_vin), output_processor=TakeFirst())
    plate = scrapy.Field(input_processor=Compose(find_plate), output_processor=TakeFirst())
