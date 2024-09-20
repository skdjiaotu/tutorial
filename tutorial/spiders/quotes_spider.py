from pathlib import Path

import scrapy

from tutorial.items import TutorialItem

# scrapy crawl quotes
class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ['toscrape.com']
    def start_requests(self):
        urls = [
            # "https://quote.eastmoney.com/center/boardlist.html#boards-BK05001",
            "https://quotes.toscrape.com/page/1/",
            "https://quotes.toscrape.com/page/2/",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # for quote in response.css("div.quote"):
        #     print({
        #         "text": quote.css("span.text::text").get(),
        #         "author": quote.css("small.author::text").get(),
        #         "tags": quote.css("div.tags a.tag::text").getall(),
        #     })
        print("sdfsdfsdfsdf")
        print(response)

        for quote in response.xpath('//*[@id="table_wrapper-table"]/tbody/tr'):
            print(quote)
            print({
                "code": quote.xpath('./td[2]').extract_first(),
                "name": quote.xpath('./td[3]').extract_first(),
                "price": quote.xpath('./td[5]').extract_first(),
                "gain_fall_price_ratio": quote.xpath('./td[6]').extract_first(),
                "gain_fall_price": quote.xpath('./td[7]').extract_first(),
                "turnover": quote.xpath('./td[8]').extract_first()
            })
