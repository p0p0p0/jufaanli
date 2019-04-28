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
    name = 'login'
    allowed_domains = ['www.jufaanli.com']
    custom_settings = {
        "LOG_LEVEL": "DEBUG",
        "DEFAULT_REQUEST_HEADERS": {
            "accept": "application/json, text/javascript, */*; q=0.01",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
            "cache-control": "no-cache",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            # "cookie": "t=c898b92b5ed9d62c190b7d8773204f14; BJYSESSION=c01gc9cqd0l2d9tjc8jjdot9t5; is_remember=0; BJYSESSION=c01gc9cqd0l2d9tjc8jjdot9t5; login_time=2019-04-21+14%3A42%3A22; tf=1118fbe6be676182fd2238955f6b36da",
            "dnt": "1",
            "origin": "https://www.jufaanli.com",
            "pragma": "no-cache",
            "referer": "https://www.jufaanli.com/usercenter_collect",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3766.2 Safari/537.36",
            "x-requested-with": "XMLHttpRequest",
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
    user = os.getenv("USER", default="")
    # $env:USER=""

    login_url = "https://www.jufaanli.com/home/User/login"
    login_checksum = "https://www.jufaanli.com/home/User/checksumUser"
    login_checkin = "https://www.jufaanli.com/home/User/checkinLogin"
    base_url = "https://www.jufaanli.com/home/Collection/collectCases"
    label_id = None

    def start_requests(self):
        while True:
            # start = self.r.lpop("jufaanli:start")
            start = 1001
            for i in range(10):
                case_id = int(start)*1000 + i
                payload = {"case_id": str(case_id), "label_id": ""}
                yield FormRequest(
                    url=self.base_url,
                    meta={"cookiejar": True},
                    formdata=payload,
                )
            break
                
    def parse(self, response):
        res = json.loads(response.body_as_unicode())
        if 0 != res:
            self.r.sadd("jufaanli:collect_msg", res)
