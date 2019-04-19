# -*- coding: utf-8 -*-
import scrapy


class CollectSpider(scrapy.Spider):
    name = 'collect'
    allowed_domains = ['jufaanli.com']
    start_urls = ['http://jufaanli.com/']

    def parse(self, response):
        pass
