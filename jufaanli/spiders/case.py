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
from jufaanli.conf import pages

class CollectSpider(scrapy.Spider):
    name = 'case'
    allowed_domains = ['www.jufaanli.com']
    custom_settings = {
        "LOG_LEVEL": "DEBUG",
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
            'Cookie': 't=1755391248282a65ba557d3c070ae712; BJYSESSION=5ndtuujjt00r8qjo80li5pgi50; BJYSESSION=5ndtuujjt00r8qjo80li5pgi50; is_remember=0; login_time=2019-04-20+21%3A30%3A28; tf=f94bf7f1be58053a124089c543b5051b',
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

    def start_requests(self):
        while True:
            for i, sign in enumerate(pages, start=1):
                url = f"https://www.jufaanli.com/JuFaMobile/User/collect?sign={sign}&version_no=3.0.1"
                payload = {
                    "page": i,
                    "uid": "176745",
                    "version_no": "3.0.1",
                }
                yield Request(
                    url=url,
                    method="POST",
                    body=urlencode(payload),
                    dont_filter=True
                )
            while True:
                if 0 < self.r.scard("jufaanli:crawled"):
                    sleep(1)
                else:
                    break

    def parse(self, response):
        res = json.loads(response.body_as_unicode())
        code = res.get("code", 0)
        if 200 == code:
            data = res.get("data", None)
            for case in data:
                yield CaseItem(case=case)
