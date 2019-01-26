import scrapy
import sys
from baidu.items import *
from scrapy_splash import SplashRequest
class ImageSpider(scrapy.Spider):
    name='image'
    start_urls=[]
    def start_requests(self):
        search_words=["月季花","蝴蝶兰","桂花","九里香","米仔兰"]
        for search_word in search_words:
            print(search_word)
            url='http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word='+search_word
            request=SplashRequest(url,callback=self.parse,meta={'search_word':search_word})#meta传递额外参数
            yield request
    def parse(self,response):
        arrs=response.xpath('//div[@id="imgid"]/ul[@class="imglist"]/li/a/img/@src').extract()
        search_word=response.meta['search_word']
        for one in arrs:
            image_item=ImageItem()
            image_item["search_word"]=search_word
            image_item["image_url"]=one
            image_item["referer"]=response.url
            yield image_item
        next_page=response.xpath('//a[text()="下一页"]/@href').extract_first()
        if next_page is not None:
            url=response.urljoin(next_page)
            request=SplashRequest(url,callback=self.parse,meta={'search_word':search_word})#meta传递额外参数
            yield request
        
