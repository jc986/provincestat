# -*- coding: utf-8 -*-

import json


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class ProvincestatPipeline:
    def __init__(self):
        self.files = {}
        self.pset = set()

    def open_spider(self, spider):
        print(spider.name + " json exporter open spider")
        file = open("{}.json".format(spider.name), "w", encoding='utf-8')
        self.files[spider.name] = file
        self.file = file

    def process_item(self, item, spider):
        #防止重复数据插入
        if (item['areaid'] not in self.pset):
            self.pset.add(item['areaid'])
            # ensure_ascii=False 确保dump出来的中文不是ascii字符， 而是真正中文
            line = json.dumps(dict(item), ensure_ascii=False, separators=(',', ':')) + "\n"
            # print(line)
            self.file.write(line)
        return item

    def close_spider(self, spider):
        file = self.files.pop(spider.name)
        file.close()
        print(spider.name + " json exporter colse spider")
