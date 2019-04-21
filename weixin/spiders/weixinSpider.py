import scrapy
import sys
from weixin.items import *
from scrapy_splash import SplashRequest
class WeixinSpider(scrapy.Spider):
    name='weixin'
    start_urls=[]
    def start_requests(self):
        search_words=["易美居"]
        for search_word in search_words:
            print(search_word)
            url="https://www.sogou.com/web?query="+search_word+"微信公众号"
            request=scrapy.Request(url,callback=self.parse,meta={'search_word':search_word})#meta传递额外参数
            yield request
    def parse(self,response):
        url=response.xpath('//div[@class="wx-table"]//div[@class="wx-name"]/span/a/@href').extract_first()
        search_word=response.meta['search_word']
        request=scrapy.Request(url,callback=self.parseList,meta={'search_word':search_word})#meta传递额外参数
        yield request

    def parseList(self,response):
        search_word=response.meta['search_word']
        urls=response.xpath('//div[@class="weui_media_bd"]/h4[@class="weui_media_title"]/@hrefs').extract() 
        for url in urls:
            url=response.urljoin(url)
            request=scrapy.Request(url,callback=self.parseDetail,meta={'search_word':search_word})#meta传递额外参数
            yield request

    def parseDetail(self,response):
        search_word=response.meta['search_word']
        title=response.xpath('//div[@id="img-content"]//h2[@id="activity-name"]/text()').extract_first()
        publish_time=response.xpath('//em[@id="publish_time"]/text()').extract_first()
        js_name=response.xpath('//div[@id="meta_content"]//a[@id="js_name"]/text()').extract_first()
        content=response.xpath('//div[@id="js_content"]').extract_first()
        
        title=title.replace('\n','').strip(' ')
        js_name=js_name.replace('\n','').strip(' ')
        publish_time=publish_time.strip('\n').strip(' ')
        article=ArticleItem()
        article["search_word"]=search_word
        article["title"]=title
        article["js_name"]=js_name
        article["publish_time"]=publish_time
        article["content"]=content
        yield article

        
