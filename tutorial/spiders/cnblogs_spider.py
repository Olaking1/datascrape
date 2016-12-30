import scrapy
import os
from scrapy.selector import Selector
from scrapy.http import HtmlResponse

class cnblogsSpider(scrapy.Spider):
    name="cnblogs"
    urls = []

    def start_requests(self):
        firstUrls = ['http://zzk.cnblogs.com/s/blogpost?Keywords=docker']
        startUrls = []
        for i in range(1,51):
            for j in range(len(firstUrls)):
                tempUrl = firstUrls[j]+'&pageindex='+str(i)
                # tempUrl = firstUrls[j]+'?&page='+str(i)
                startUrls.append(tempUrl)
        for url in startUrls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        urlSet = response.xpath('//div[@id="searchResult"]//div[@class="forflow"]//div[@class="searchItem"]//h3//a//@href').extract()
        for url in urlSet:
            # url = "http://blog.csdn.net/"+url
            yield scrapy.Request(url=url, callback=self.parsePages)

    def parsePages(self, response):
        subname = response.xpath('//div[@id="topics"]//div[@class="post"]//h1[@class="postTitle"]//a//text()').extract()
        if len(subname) >= 1:
            subname = (subname[0].replace(' ', ''))[2:]
            filename = '/Users/liyue/Documents/datasets/csdn_after//Docker/' + subname
            if(os.path.exists(filename) == False):
                content = ""
                contentList = response.xpath('//div[@class="postBody"]//div[@id="cnblogs_post_body"]//p//text()').extract()
                for subContent in contentList:
                    content += subContent.replace(u'\\xa0', u'').strip()
                file = open(filename,mode='w',encoding='utf-8')
                file.writelines(content)
                file.close()