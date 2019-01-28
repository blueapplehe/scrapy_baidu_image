import scrapy
import sys
from baidu.items import *
from scrapy_splash import SplashRequest
class ImageSpider(scrapy.Spider):
    name='image'
    start_urls=[]
    def start_requests(self):
        search_words=["雅阁外观","凯美瑞外观","天籁外观"]
        mod_names=["朗逸外观","捷达外观","迈腾外观","高尔夫外观","桑塔纳外观","帕萨特外观","途观外观",
          "思域外观","本田XR-V外观","本田CR-V外观","飞度外观","锋范外观","雅阁外观",
          "雷凌外观","威驰外观","凯美瑞外观","汉兰达外观","卡罗拉外观",
          "轩逸外观","天籁外观","骐达外观","奇骏外观",
          "宝马7系外观","宝马X6外观","宝马X1外观",
          "奥迪A3外观","奥迪A6L外观","奥迪A8外观",
          "奔驰A级外观","奔驰C级外观","奔驰E级外观","奔驰S级外观",
          "福克斯外观","福睿斯外观","蒙迪欧外观","金牛座外观","翼虎外观"]
        search_words=["轩逸外观","帕萨特外观","途观外观","高尔夫外观","福克斯外观","思域外观"]
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
            image_item["name"]=search_word.replace('外观', '')#过滤掉搜索词中不要的问题
            image_item["search_word"]=search_word
            image_item["image_url"]=one
            image_item["referer"]=response.url
            yield image_item
        next_page=response.xpath('//a[text()="下一页"]/@href').extract_first()
        if next_page is not None:
            url=response.urljoin(next_page)
            request=SplashRequest(url,callback=self.parse,meta={'search_word':search_word})#meta传递额外参数
            yield request
        
