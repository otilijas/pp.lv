import json

import scrapy
from pplv.items import PplvItem
from scrapy.loader import ItemLoader


class PplvSpider(scrapy.Spider):
    name = 'pplv'
    start_urls = ['https://apipub.pp.lv/lv/api_user/v1/categories/2/lots?orderColumn=publishDate&orderDirection=DESC&currentPage=1&itemsPerPage=20']
    page_number = 1

    def parse(self, response):
        data = json.loads(response.body)
        vehicles = data['content']['data']

        for vehicle in vehicles:
            l = ItemLoader(item=PplvItem(), selector=vehicle)

            l.add_value('brand', vehicle['category']['slug']['en'])
            l.add_value('model', vehicle['category']['name'])
            l.add_value('year', vehicle['adFilterValues'])
            l.add_value('miles', vehicle['adFilterValues'])
            l.add_value('vin', vehicle['adFilterValues'])
            l.add_value('plate', vehicle['adFilterValues'])

            yield l.load_item()

        self.page_number += 1
        next_page = f'https://apipub.pp.lv/lv/api_user/v1/categories/2/lots?orderColumn=publishDate&orderDirection=DESC&currentPage={self.page_number}&itemsPerPage=20'
        if len(vehicles):
            yield response.follow(next_page, callback=self.parse)
