# -*- coding: utf-8 -*-

import scrapy
from scrapy.crawler import Crawler
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from provincestat.items import AreaItem
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class ProvinceSpider(scrapy.Spider):
    name = "province_spider"
    allowed_domain = ['stats.gov.cn']
    start_urls = ['http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2019/']
    items = []
    prov_items = []
    city_items = []
    county_items = []
    base_url = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2019/'

    def start_requests(self):
        """
        启动函数
        :return:
        """
        yield scrapy.Request(self.start_urls[0], callback=self.parse_province)

    def parse_province(self, response):
        """
        解析省份数据
        :param response:
        :return:
        """
        sel = scrapy.selector.Selector(response)
        province_list = sel.css('.provincetr')
        items = []
        for p in province_list:
            td_list = p.xpath('./td')
            for td in td_list:
                item = AreaItem()
                # 个别td的内容为空
                if (td.xpath('./a').get(default='not-found') != 'not-found' or td.xpath('./text()').get(
                        default='not-found') != 'not-found'):
                    item['areaid'] = td.xpath('./a/@href').get()[:2]
                    item['level'] = 1
                    item['pareaid'] = '0'
                    item['areacode'] = td.xpath('./a/@href').get()[:2].ljust(12, '0')
                    item['areaname'] = td.xpath('./a/text()').get()
                    item['link'] = self.base_url + td.xpath('./a/@href').get()
                    print(item)
                    items.append(item)
                    self.prov_items.append(item)
                    self.items.append(item)
                    yield item
                    yield scrapy.Request(item['link'], callback=self.parse_city)

    def parse_city(self, response):
        '''
        解析市信息
        :param response:
        :param pitem:
        :return:
        '''
        sel = scrapy.selector.Selector(response)
        city_list = sel.css('.citytr')
        # items.append(pitem)
        for c in city_list:
            item = AreaItem()
            items = []
            # 将上一级省节点添加到市节点中，以列表形式传给县节点
            if (c.xpath('./td/a').get(default='not-found') != 'not-found'):
                item['areaid'] = c.xpath('./td/a/@href').get()[3:7]
                item['level'] = 2
                item['pareaid'] = c.xpath('./td/a/@href').get()[3:5]
                item['areacode'] = c.xpath('./td/a/text()').get()
                item['areaname'] = c.xpath('./td[2]//text()').get()
                item['link'] = self.base_url + c.xpath('./td/a/@href').get()
                items.append(item)
                print(item)
                self.items.append(item)
            elif (c.xpath('./td/text()').get(default='not-found') != 'not-found'):
                item['areaid'] = c.xpath('./td/text()').get()[0:4]
                item['level'] = 2
                item['pareaid'] = c.xpath('./td/text()').get()[0:2]
                item['areacode'] = c.xpath('./td/text()').get()
                item['areaname'] = c.xpath('./td[2]//text()').get()
                items.append(item)
                print(item)
                self.items.append(item)
            yield item
                # yield scrapy.Request(item['link'], callback=self.parse_county, cb_kwargs=dict(pitem=item, pitems=items))

    def parse_county(self, response, pitem, pitems):
        '''
        解析县信息
        :param response:
        :param pitem:
        :return:
        '''
        sel = scrapy.selector.Selector(response)
        county_list = sel.css('.countytr')
        items = []
        items.extend(pitems)
        for c in county_list:
            item = AreaItem()
            # 将上一级省节点添加到市节点中，以列表形式传给县节点
            # items.append(items)
            if (c.xpath('./td/a').get(default='not-found') != 'not-found'):
                item['areaid'] = c.xpath('./td/a/text()').get()[0:6]
                item['level'] = 3
                item['pareaid'] = pitem['areaid']
                item['areacode'] = c.xpath('./td/a/text()').get()
                item['areaname'] = c.xpath('./td[2]//text()').get()
                item['link'] = self.base_url + c.xpath('./td/a/@href').get()
                items.append(item)
                # yield scrapy.Request(item['link'], callback=self.parse_county, cb_kwargs=dict(pitem=item, items=items))
            elif (c.xpath('./td/text()').get(default='not-found') != 'not-found'):
                item['areaid'] = c.xpath('./td/text()').get()[0:6]
                item['level'] = 3
                item['pareaid'] = pitem['areaid']
                item['areacode'] = c.xpath('./td/text()').get()
                item['areaname'] = c.xpath('./td[2]//text()').get()
                # print(item)
                items.append(item)
        return items


'''
以下为单独运行scrapy
'''

''' 方式一 
configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
runner = CrawlerRunner(get_project_settings())

d = runner.crawl(ProvinceSpider)
d.addBoth(lambda _: reactor.stop())
reactor.run() # the script will block here until the crawling is finished
'''

''' 方式二 twisted.internet.error.ReactorNotRestartable
process = CrawlerProcess(get_project_settings())
process.crawl(ProvinceSpider)
process.start() # the script will block here until the crawling is finished
'''
