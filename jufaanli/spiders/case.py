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
        "DEFAULT_REQUEST_HEADERS": {
            'Charset': 'UTF-8',
            'User-Agent': 'jufaanli/3.0.1 (iPhone; iOS 10.3.2; Scale/2.00)v',
            'Accept-Encoding': 'gzip, deflate',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Connection': 'keep-alive',
            'Cookie': 'tf=2971f014c92d530eb10cc6412c9a979f; t=8c36a7c25995731e57250bf357929467; BJYSESSION=1td6ku7qdjifphb18pib6qav40',
            'Accept-Language': 'zh-Hans-CN;q=1, en-US;q=0.9',

        },
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

    base_url = "https://www.jufaanli.com/JuFaMobile/User/collect?sign=14463aceb56ff73945004523425d4230&version_no=3.0.1"

    def start_requests(self):
        for i in range(2,3):
            payload = {
                "page": i,
                "uid": "175648",
                "version_no": "3.0.1",
		    }
            yield Request(
                url=self.base_url,
                method="POST",
                body=urlencode(payload),
            )

    def parse(self, response):
        res = json.loads(response.body_as_unicode())
        print(res)
        code = res.get("code", 0)
        if 200 == code:
            data = res.get("data", None)
            for case in data:
                yield CaseItem(case=case)