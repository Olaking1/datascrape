import scrapy
import os
from scrapy.selector import Selector
from scrapy.http import HtmlResponse

class alterSpider(scrapy.Spider):
    name="technology"
    urls = []

    def start_requests(self):
        # firstUrls = ['http://tech.gmw.cn/node_4360.htm',
        #              'http://tech.gmw.cn/node_10249.htm',
        #              'http://tech.gmw.cn/node_10609.htm',
        #              'http://tech.gmw.cn/node_10606.htm',
        #              'http://tech.gmw.cn/node_9671.htm'
        #              'http://tech.gmw.cn/node_5557.htm',
        #              'http://tech.gmw.cn/node_10617.htm',
        #              'http://tech.gmw.cn/node_5618.htm',
        #              'http://tech.gmw.cn/node_4394.htm']
        firstUrls = ['http://tech.gmw.cn/newspaper/index.htm']
        startUrls = ['http://tech.gmw.cn/newspaper/index.htm']
        # startUrls = ['http://tech.gmw.cn/node_4360.htm',
        #              'http://tech.gmw.cn/node_10249.htm',
        #              'http://tech.gmw.cn/node_10609.htm',
        #              'http://tech.gmw.cn/node_10606.htm',
        #              'http://tech.gmw.cn/node_9671.htm'
        #              'http://tech.gmw.cn/node_5557.htm',
        #              'http://tech.gmw.cn/node_10617.htm',
        #              'http://tech.gmw.cn/node_4394.htm']
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
            url = 'http://tech.gmw.cn/newspaper/'+url
            yield scrapy.Request(url=url, callback=self.parsePages)

    def parsePages(self, response):
        subname = response.xpath('//h1[@id="articleTitle"]//text()').extract()
        if len(subname) >= 1:
            subname = (subname[0].replace(' ', ''))[2:-2]
            filename = '/Users/liyue/Documents/datasetsforguangming/technology/' + subname
            if(os.path.exists(filename) == False):
                content = response.xpath('//div[@id="contentMain"]//p//text()').extract()
                file = open(filename,mode='w',encoding='utf-8')
                file.writelines(content)