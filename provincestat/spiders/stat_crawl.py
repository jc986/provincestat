# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from provincestat.items import AreaItem


class StatCrawl(CrawlSpider):
    name = 'stat_crawl'
    allowed_domain = ['stats.gov.cn']
    start_urls = ['http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/']
    base_url = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2019/'

    rules = (
        Rule(LinkExtractor(allow=r'.+2019/index\.html'), callback='parse_prov', follow=True),
        Rule(LinkExtractor(allow=r'.+2019/\d{2}\.html'), callback='parse_city', follow=True),
        Rule(LinkExtractor(allow=r'.+2019/\d{2}/\d{4}\.html'), callback='parse_county', follow=False),
    )

    def parse_prov(self, response):
        """
               解析省份数据
               :param response:
               :return:
               """
        province_list = response.xpath('//tr[@class="provincetr"]')
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
                    # item['link'] = self.base_url + td.xpath('./a/@href').get()
                    print(item)
                    items.append(item)
                    # self.prov_items.append(item)
                    # self.items.append(item)
                    yield item

    def parse_city(self, response):
        city_list = response.css('.citytr')
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
                # item['link'] = self.base_url + c.xpath('./td/a/@href').get()
                items.append(item)
            elif (c.xpath('./td/text()').get(default='not-found') != 'not-found'):
                item['areaid'] = c.xpath('./td/text()').get()[0:4]
                item['level'] = 2
                item['pareaid'] = c.xpath('./td/text()').get()[0:2]
                item['areacode'] = c.xpath('./td/text()').get()
                item['areaname'] = c.xpath('./td[2]//text()').get()
                items.append(item)
            yield item

    def parse_county(self, response):
        '''
        解析县信息
        :param response:
        :param pitem:
        :return:
        '''
        county_list = response.css('.countytr')
        items = []
        for c in county_list:
            item = AreaItem()
            # 将上一级省节点添加到市节点中，以列表形式传给县节点
            # items.append(items)
            if (c.xpath('./td/a').get(default='not-found') != 'not-found'):
                item['areaid'] = c.xpath('./td/a/text()').get()[0:6]
                item['level'] = 3
                item['pareaid'] = item['areaid'][:4]
                item['areacode'] = c.xpath('./td/a/text()').get()
                item['areaname'] = c.xpath('./td[2]//text()').get()
                # item['link'] = self.base_url + c.xpath('./td/a/@href').get()
                items.append(item)
                # yield scrapy.Request(item['link'], callback=self.parse_county, cb_kwargs=dict(pitem=item, items=items))
            elif (c.xpath('./td/text()').get(default='not-found') != 'not-found'):
                item['areaid'] = c.xpath('./td/text()').get()[0:6]
                item['level'] = 3
                item['pareaid'] = item['areaid'][:4]
                item['areacode'] = c.xpath('./td/text()').get()
                item['areaname'] = c.xpath('./td[2]//text()').get()
                # print(item)
                items.append(item)
            yield item
