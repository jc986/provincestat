## 介绍
通过scrapy爬取国家统计局 http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/ 上全国省市县三级地区代码数据。数据格式为
```angular2html
## json格式
{"areaid":"11","level":1,"pareaid":"0","areacode":"110000000000","areaname":"北京市"}
```

```angular2html
csv 格式
areacode,areaid,areaname,level,link,pareaid
110000000000,11,北京市,1,,0
```
* areacode : 地区12位代码
* areadid: 地区缩写代码，如果是省则为前2位，地市前4位
* areaname：地区名称
* level：级别，1：省份 2：地市 3：县域
* pareaid：上一级地区缩写代码

## 工程结构
#### provincestat目录
* start.py: 程序启动脚本
* stat_province.py : 通过嵌套链接方式进行爬取
* stat_crawl. : 通过crawl规则进行爬取
* stat_crawl.json：获取的数据json文件
* stat_crawl.csv：获取的数据csv文件

