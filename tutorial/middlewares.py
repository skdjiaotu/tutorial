# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import random
import time

from scrapy import signals
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tutorial.settings import USER_AGENTS_LIST
from tutorial.settings import PROXY_LIST

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class TutorialSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class TutorialDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class SeleniumMiddleware(object):
    """
        下载器中间件
    """

    def __init__(self, timeout=50):
        print("这个地方是中间件1 ")
        # options = Options()
        # options.add_argument("--headless")
        # options.add_argument("--disable-gpu")
        self.browser = webdriver.Chrome()
        self.timeout = timeout
        self.wait = WebDriverWait(self.browser, self.timeout)

    def __del__(self):
        self.browser.close()

    def process_request(self, request, spider):
        # 不需要渲染的可以不经过 self.browser 请求就行
        self.browser.get(request.url)
        # # 延时等待
        # self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'recruit-list-link')))
        time.sleep(3)
        body = self.browser.page_source
        # 返回响应的html页面  不经过下载器
        return HtmlResponse(url=request.url, body=body, request=request, encoding='utf-8')


class UserAgentMiddleware(object):
    """
        下载器中间件
    """

    def __init__(self, timeout=50):
        print("这个地方是中间件UserAgentMiddleware ")
        self.browser = webdriver.Chrome()
        self.timeout = timeout
        self.wait = WebDriverWait(self.browser, self.timeout)

    def __del__(self):
        self.browser.quit()

    def process_request(self, request, spider):
        print("这个地方是中间件 ")
        request.headers['User-Agent'] = random.choice(USER_AGENTS_LIST)


class ProxyMiddleware(object):
    """
        下载器中间件
    """

    def process_request(self, request, spider):
        print("这个地方是ProxyMiddleware中间件 ")
        request.meta['proxy'] = random.choice(PROXY_LIST)
        print(request.meta['proxy'])
