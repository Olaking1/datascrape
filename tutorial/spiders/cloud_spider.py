import scrapy
import os
from scrapy.selector import Selector
from scrapy.http import HtmlResponse

class alterSpider(scrapy.Spider):
    name="cloud"
    urls = []

    def start_requests(self):
        firstUrls = ['http://blog.csdn.net/column/list.html?q=hadoop']
        startUrls = []
        for i in range(1,2):
            for j in range(len(firstUrls)):
                tempUrl = firstUrls[j]+'&page='+str(i)
                # tempUrl = firstUrls[j]+'?&page='+str(i)
                startUrls.append(tempUrl)
        for url in startUrls:
            yield scrapy.Request(url=url, callback=self.parseFirst)

    def parseFirst(self, response):
        urlSet = response.xpath('//div[@class="column_index clearfix"]//'
                                'div[@class="column_wrap clearfix"]//div[@class="column_list "]//a//@href').extract()
        for url in urlSet:
            url = "http://blog.csdn.net/" + url
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # urlSet = response.xpath('//div[@id="article_list"]//div[@class="list_item article_item"]//div//h1//span//a//@href').extract()
        urlSet = response.xpath('//ul[@class="detail_list"]//li//h4//a//@href').extract()
        for url in urlSet:
            # url = "http://blog.csdn.net/"+url
            yield scrapy.Request(url=url, callback=self.parsePages)

    def parsePages(self, response):
        subname = response.xpath('//div[@class="article_title"]//span//a//text()').extract()
        if len(subname) >= 1:
            subname = (subname[0].replace(' ', ''))[2:-2]
            filename = '/Users/liyue/Documents/datasets/csdn_after//Hadoop/' + subname
            if(os.path.exists(filename)):
                os.remove(filename)
            content = ""
            contentList = response.xpath('//div[@id="article_content"]//text()').extract()
            for subContent in contentList:
                content += subContent.replace(u'\\xa0', u'').strip()
            file = open(filename,mode='w',encoding='utf-8')
            file.writelines(content)