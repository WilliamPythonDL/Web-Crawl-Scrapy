# -*- coding: utf-8 -*-
import scrapy
import time


class StocksSpider(scrapy.Spider):
    name = 'stocks'
    # allowed_domains = ['baidu.com']
    start_urls = ['http://quote.eastmoney.com/stocklist.html']


    def parse(self, response):
        count = 0
        for href in response.css('#quotesearch').css('a[href*=http]::attr(href)'):
            try:
                stock = href.extract().split('/')[-1]
                url = 'https://gupiao.baidu.com/stock/' + stock 
                yield scrapy.Request(url, callback=self.parse_stock)
                count = count + 1
                if count >= 30:
                    time.sleep(3)
                    count = 0
                else:
                    pass

            except:
                continue

        # for href in response.css('a::attr(href)').extract():
        #     try:
        #         stock = href.css('a::text').extract()[0]
        #         url = 'https://gupiao.baidu.com/stock/' + stock + '.html'
        #         yield scrapy.Request(url, callback=self.parse_stock)
        #     except:
        #         continue    

    def parse_stock(self, response):

        infoDict = {}
        # stockInfo = response.css('.stock-bets')

        stockInfo = response
        name = stockInfo.css('.bets-name::text').extract()[0].split()[0]
        nid = stockInfo.css('.bets-name span::text').extract()[0].split()[0]

        keyList = stockInfo.css('dt::text').extract()
        valueList = stockInfo.css('dd::text').extract()
        for i in range(len(keyList)):
            key = keyList[i]

            try:
                val = valueList[i]
            except:
                val = '--'
            infoDict[key] = val

        infoDict.update(
            {"股票名称": name + str(' ID:') + nid})
        yield infoDict

