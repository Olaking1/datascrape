import scrapy
import os
from scrapy.selector import Selector
from scrapy.http import HtmlResponse

class alterSpider(scrapy.Spider):
    name="education"
    urls = []

    def start_requests(self):
        firstUrls = ['http://edu.gmw.cn/node_10810.htm',
                     'http://edu.gmw.cn/node_10602.htm',
                     'http://edu.gmw.cn/node_9717.htm',
                                 'http://edu.gmw.cn/node_9757.htm',
                     'http://edu.gmw.cn/node_9729.htm',
#                     'http://edu.gmw.cn/newspaper/index.htm',
                     'http://edu.gmw.cn/node_9746.htm',
                     'http://edu.gmw.cn/node_10603.htm',
                     'http://edu.gmw.cn/node_9742.htm']
        startUrls = ['http://edu.gmw.cn/node_10810.htm',
                     'http://edu.gmw.cn/node_10602.htm',
                     'http://edu.gmw.cn/node_9717.htm',
                     'http://edu.gmw.cn/node_9757.htm',
                     'http://edu.gmw.cn/node_9729.htm',
#                     'http://edu.gmw.cn/newspaper/index.htm',
                     'http://edu.gmw.cn/node_9746.htm',
                     'http://edu.gmw.cn/node_10603.htm',
                     'http://edu.gmw.cn/node_9742.htm']
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
            url = 'http://edu.gmw.cn/'+url
            yield scrapy.Request(url=url, callback=self.parsePages)

    def parsePages(self, response):
        subname = response.xpath('//h1[@id="articleTitle"]//text()').extract()
        if len(subname) >= 1:
            subname = (subname[0].replace(' ', ''))[2:-2]
            filename = '/Users/liyue/Documents/datasetsforguangming/education/' + subname
            if(os.path.exists(filename) == False):
                content = response.xpath('//div[@id="contentMain"]//p//text()').extract()
                file = open(filename,mode='w',encoding='utf-8')
                file.writelines(content)