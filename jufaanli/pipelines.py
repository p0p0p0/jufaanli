# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json


class CasePipeline(object):
    def process_item(self, item, spider):
        case = item['case']
        case_id = case['id']
        spider.r.sadd("jufaanli:case", json.dumps(case, ensure_ascii=False))
        spider.r.sadd("jufaanli:crawled", case_id)
        return item
