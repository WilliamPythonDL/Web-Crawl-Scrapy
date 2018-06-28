# -*- coding: utf-8 -*-
import scrapy


class StocksSpider(scrapy.Spider):
    name = 'stocks'
    # allowed_domains = ['baidu.com']
    start_urls = ['http://quote.eastmoney.com/stocklist.html']


    def parse(self, response):

        # sels = response.xpath('//div[@id="quotesearch"]/ul/li/a[contains(@href, "http")]/@href').extract()
        sels = response.xpath('//div[@id="quotesearch"]')
        a_tag = sels.xpath('.//a[contains(@href, "http")]/@href').extract()
        for href in a_tag:       
            try:
                stock = href.split('/')[-1]
                url = 'https://gupiao.baidu.com/stock/' + stock 
                yield scrapy.Request(url, callback=self.parse_stock)                
            except:
                continue
        # for href in response.css('#quotesearch').css('a[href*=http]::attr(href)').extract():
        #     try:
        #         stock = href.split('/')[-1]
        #         url = 'https://gupiao.baidu.com/stock/' + stock 
        #         yield scrapy.Request(url, callback=self.parse_stock)
        #     except:
        #         continue   

    def parse_stock(self, response):
    
        infoDict = {}
        # # stockInfo = response.xpath('//div[@class="stock-bets"]')    
        # name = stockInfo.xpath('//a[@class="bets-name"]/text()').extract()[0].split()[0]
        # nid = stockInfo.xpath('//a[@class="bets-name"]/span/text()').extract()[0].split()[0]

        # keyList = stockInfo.xpath('//dt/text()').extract()
        # valueList = stockInfo.xpath('//dd/text()').extract()

  
        name = response.xpath('//a[@class="bets-name"]/text()').extract()[0].split()[0]
        nid = response.xpath('//a[@class="bets-name"]/span/text()').extract()[0].split()[0]

        keyList = response.xpath('//dt/text()').extract()
        valueList = response.xpath('//dd/text()').extract()
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

        # infoDict = {}
        # stockInfo = response.css('.stock-bets')
        # name = stockInfo.css('.bets-name::text').extract()[0].split()[0]
        # nid = stockInfo.css('.bets-name span::text').extract()[0].split()[0]

        # keyList = stockInfo.css('dt::text').extract()
        # valueList = stockInfo.css('dd::text').extract()
        # for i in range(len(keyList)):
        #     key = keyList[i]

        #     try:
        #         val = valueList[i]
        #     except:
        #         val = '--'
        #     infoDict[key] = val

        # infoDict.update(
        #     {"股票名称": name + str(' ID:') + nid})
        # yield infoDict

