# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals


class BaiduSpiderMiddleware(object):
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

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class BaiduDownloaderMiddleware(object):
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
        spider.logger.info('Spider opened: %s' % spider.name)
        
from selenium import webdriver
from scrapy.http import HtmlResponse
import time
from selenium.webdriver.chrome.options import Options     
import pickle
class ChromeSpiderMiddleware(object):

    def __init__(self):
        option = Options()
        #option.add_argument('--headless')
        print("初始化浏览器")
        self.browser = webdriver.Chrome(executable_path="/usr/bin/chromedriver",chrome_options=option)
#         self.browser.get("https://image.baidu.com")
#         time.sleep(30)
#         pickle.dump( self.browser.get_cookies() , open("/data/cookies/cookies.pkl","wb"))
#         cookies = pickle.load(open("/data/cookies/cookies.pkl", "rb"))
#         print(cookies)
#         for cookie in cookies:
#             self.browser.add_cookie(cookie)

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.
        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        if request.meta.get("is_image"):
            print("存在is_image")#如果是图片就不进行渲染了
            return None
        else:
            self.browser.get(request.url)
            print("页面开始渲染")
            self.browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            #self.browser.execute_script("scroll(0, 1000);")
            if request.meta.get("wait_time"):
                time.sleep(request.meta.get("wait_time"))
            rendered_body = self.browser.page_source
            print("页面完成渲染")
            return HtmlResponse(request.url, body=rendered_body, encoding="utf-8",request=request)

    def spider_closed(self, spider, reason):
        print("关闭浏览器")
        self.browser.quit()
        
#from scrapy.http import HtmlResponse
        
# from selenium.common.exceptions import TimeoutException
# import time

# class SeleniumMiddleware(object):
#     def process_request(self, request, spider):
#         if spider.name == 'jingdong':
#             try:
#                 spider.browser.get(request.url)
#                 spider.browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
#             except TimeoutException as e:
#                 print('超时')
#                 spider.browser.execute_script('window.stop()')
#             time.sleep(2)
#             return HtmlResponse(url=spider.browser.current_url, body=spider.browser.page_source,
#                                 encoding="utf-8", request=request)

        
        
        
