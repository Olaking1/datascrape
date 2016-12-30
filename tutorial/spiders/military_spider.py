import scrapy
import os
from scrapy.selector import Selector
from scrapy.http import HtmlResponse

class alterSpider(scrapy.Spider):
    name="military"
    urls = []

    def start_requests(self):
        firstUrls = ['http://mil.gmw.cn/node_8981.htm',
                     'http://mil.gmw.cn/node_11179.htm',
                     'http://mil.gmw.cn/node_11177.htm',
                     'http://mil.gmw.cn/node_11178.htm',
                     'http://mil.gmw.cn/node_8978.htm',
                     'http://mil.gmw.cn/node_8979.htm',
                     'http://mil.gmw.cn/node_9664.htm',
                     'http://mil.gmw.cn/node_8986.htm']
        startUrls = ['http://mil.gmw.cn/node_8981.htm',
                     'http://mil.gmw.cn/node_11179.htm',
                     'http://mil.gmw.cn/node_11177.htm',
                     'http://mil.gmw.cn/node_11178.htm',
                     'http://mil.gmw.cn/node_8978.htm',
                     'http://mil.gmw.cn/node_8979.htm',
                     'http://mil.gmw.cn/node_9664.htm',
                     'http://mil.gmw.cn/node_8986.htm']
        for i in range(2,11):
            for j in range(len(firstUrls)):
                tempUrl = firstUrls[j][0:-4]+'_'+str(i)+'.htm'
                startUrls.append(tempUrl)
        for url in startUrls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        urlSet = response.xpath('//div[@class="main_list"]//h1[@class="title"]//@href').extract()
        if(len(urlSet) == 0):
            urlSet = response.xpath('//ul[@class="channel-newsGroup"]//@href').extract()
        for url in urlSet:
            url = 'http://mil.gmw.cn/'+url
            yield scrapy.Request(url=url, callback=self.parsePages)

    def parsePages(self, response):
        subname = response.xpath('//h1[@id="articleTitle"]//text()').extract()
        if len(subname) >= 1:
            subname = (subname[0].replace(' ', ''))[2:-2]
            filename = '/Users/liyue/Documents/datasetsforguangming/military/' + subname
            if(os.path.exists(filename) == False):
                content = response.xpath('//div[@id="contentMain"]//p//text()').extract()
                file = open(filename,mode='w',encoding='utf-8')
                file.writelines(content)