# -*- coding: utf-8 -*-
from scrapy.exporters import CsvItemExporter


class CSVPipline(object):
    def __init__(self):
        self.files = {}
        self.pset = set()

    def open_spider(self, spider):
        print(spider.name + " csv exporter open spider")
        file = open("{}.csv".format(spider.name), "wb")
        self.files[spider.name] = file
        self.exporter = CsvItemExporter(file)
        self.exporter.fileds_to_exporter = ['areaid', 'areacode', 'areaname', 'pareaid', 'level']
        self.exporter.start_exporting()

    def process_item(self, item, spider):
        if (item['areaid'] not in self.pset):
            self.pset.add(item['areaid'])
            self.exporter.export_item(item)
        return item

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider.name)
        file.close()
        print(spider.name + " csv exporter colse spider")
