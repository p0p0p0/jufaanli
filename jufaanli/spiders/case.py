# -*- coding: utf-8 -*-
import json
from urllib.parse import urlencode
from time import time, sleep
import base64
import random
import os

import scrapy
from scrapy import Request, FormRequest
from scrapy.utils.project import get_project_settings
from scrapy.exceptions import CloseSpider
from redis import Redis, ConnectionPool

from jufaanli.items import CaseItem


class CollectSpider(scrapy.Spider):
    name = 'case'
    allowed_domains = ['www.jufaanli.com']
    custom_settings = {
        # "LOG_LEVEL": "DEBUG",
        # "DOWNLOADER_MIDDLEWARES": {
        #     # "jufaanli.middlewares.ProxyMiddleware": 543,
        #     # "jufaanli.middlewares.JufaanliDownloaderMiddleware": 534
        # },
        "ITEM_PIPELINES": {
            'jufaanli.pipelines.CasePipeline': 300,
        }
    }
    settings = get_project_settings()
    redis_host = settings.get("REDIS_HOST")
    redis_port = settings.get("REDIS_PORT")
    proxy_server = settings.get("PROXY_SERVER")
    proxy_user = settings.get("PROXY_USER")
    proxy_pass = settings.get("PROXY_PASS")
    proxy_auth = "Basic " + base64.urlsafe_b64encode(bytes((proxy_user + ":" + proxy_pass), "ascii")).decode("utf8")
    pool = ConnectionPool(host=redis_host, port=redis_port, db=0)
    r = Redis(connection_pool=pool)

    base_url = "https://www.jufaanli.com/home/Collection/showAllCollection"

    def start_requests(self):
        for i in range(100):
            payload = {"page": i+1}
            yield Request(
                url=self.base_url,
                method="POST",
                body=urlencode(payload),
            )

    def parse(self, response):
        res = json.loads(response.body_as_unicode())
        case_list = res.get("case_list", None)
        for case in case_list:
            yield CaseItem(case=case)
