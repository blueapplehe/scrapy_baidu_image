import scrapy
import sys
from baidu.items import *
from scrapy_splash import SplashRequest
class ImageSpider(scrapy.Spider):
    name='image'
    start_urls=[]
    def start_requests(self):
        search_words=["杨幂"]
        for search_word in search_words:
            print(search_word)
            url='https://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word='+search_word
            request=scrapy.Request(url,callback=self.parse,meta={'search_word':search_word})#meta传递额外参数
            yield request
    def parse(self,response):
        arrs=response.xpath('//div[@id="imgid"]/ul[@class="imglist"]/li/a/img/@src').extract()
        details=response.xpath('//div[@id="imgid"]/ul[@class="imglist"]/li/a/@href').extract()
        search_word=response.meta['search_word']
        for key,one in enumerate(arrs):
            image_item=ImageItem()
            image_item["name"]=search_word.replace('外观', '')#过滤掉搜索词中不要的问题
            image_item["search_word"]=search_word
            image_item["image_url"]=one
            image_item["referer"]=response.url
            detail_url=response.urljoin(details[key])
            image_item["detail_url"]=detail_url
            if True:
                #抓取原图时，百度是先加载页面～～然后再延时执行js获取大图反正好坑，所以要设置获取页面后要检查是否已经获取到原图url
                request=scrapy.Request(detail_url,callback=self.parseDetail,meta={'item':image_item,'is_detail':1})#meta传递额外参数
                yield request
            else:
                yield image_item
        next_page=response.xpath('//a[text()="下一页"]/@href').extract_first()
        if next_page is not None:
            url=response.urljoin(next_page)
            request=scrapy.Request(url,callback=self.parse,meta={'search_word':search_word})#meta传递额外参数
            yield request

    def parseDetail(self,response):
        image_item=response.meta['item']
        detail_image_url=response.xpath('//img[@id="currentImg"]/@src').extract_first() 
        image_item["image_url"]=detail_image_url
        return image_item

        
