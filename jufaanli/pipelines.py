# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from urllib.parse import urlencode
import logging

from scrapy import Request


headers = {
    "accept": "application/json, text/javascript, */*; q=0.01",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
    "cache-control": "no-cache",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "cookie": "t=786c59fca9efb3deca7fa740e544fdf7; BJYSESSION=39qh046364mhugnk7vb565k3u2; is_remember=0; BJYSESSION=39qh046364mhugnk7vb565k3u2; login_time=2019-04-19+20%3A34%3A32; keywords=%E7%A6%BB%E5%A9%9A; tf=0d89f28163e5819e410aa9326a19e483",
    "dnt": "1",
    "origin": "https://www.jufaanli.com",
    "pragma": "no-cache",
    "referer": "https://www.jufaanli.com/",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3766.2 Safari/537.36",
    "x-requested-with": "XMLHttpRequest",
}


class CasePipeline(object):

    def __init__(self, crawler):
        self.crawler = crawler

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_item(self, item, spider):
        case = item['case']
        case_id = case['case_id']
        spider.r.sadd("jufaanli:case", json.dumps(case, ensure_ascii=False))
        payload = {"case_id": case_id, "label_id": "undefined"}

        self.crawler.engine.crawl(Request(
                    url="https://www.jufaanli.com/home/Collection/cancelCollect",
                    method="POST",
                    body=urlencode(payload),
                    dont_filter=True,
                    callback=self.parse_cancel,
                    headers=headers
                ),
                spider,
        )
        return item

    def parse_cancel(self, response):
        pass
