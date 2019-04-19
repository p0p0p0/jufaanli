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


class CollectSpider(scrapy.Spider):
    name = 'cancel'
    allowed_domains = ['www.jufaanli.com']
    custom_settings = {
        "LOG_LEVEL": "DEBUG",
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

    base_url = "https://www.jufaanli.com/home/Collection/cancelCollect"
    label_id = "undefined"

    def start_requests(self):
        crawled = self.r.smembers("jufaanli:crawled")
        for each in crawled:
            case_id = str(each, encoding="utf-8")
            payload = {"case_id": case_id, "label_id": self.label_id}
            yield Request(
                url=self.base_url,
                method="POST",
                body=urlencode(payload)
            )

    def parse(self, response):
        res = json.loads(response.body_as_unicode())
        if 0 != res:
            self.r.sadd("jufaanli:cancel_msg", res)
