from pathlib import Path

import scrapy

from tutorial.items import TutorialItem

# scrapy crawl quotes
class QuotesSpider(scrapy.Spider):
    name = "quotes"
    # allowed_domains = ['eastmoney.com']
    def start_requests(self):
        urls = [
            "https://quote.eastmoney.com/center/boardlist.html#boards-BK05001",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for quote in response.xpath('//*[@id="table_wrapper-table"]/tbody/tr'):
            yield {
                "code": quote.xpath('./td[2]/a/text()').extract_first(),
                "name": quote.xpath('./td[3]/a/text()').extract_first(),
                "price": quote.xpath('./td[5]/span/text()').extract_first(),
                "gain_fall_price_ratio": quote.xpath('./td[6]/span/text()').extract_first(),
                "gain_fall_price": quote.xpath('./td[7]/span/text()').extract_first(),
                "turnover": quote.xpath('./td[8]/text()').extract_first()
            }

