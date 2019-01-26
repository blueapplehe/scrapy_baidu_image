# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
from baidu.items import *
import sys
import os
import requests
from scrapy_splash import SplashRequest
import urllib.request
import random
import hashlib
from pymongo import MongoClient
class BaiduPipeline(ImageItem):
    def process_item(self, item, spider):
        return item

class DownloadImagePipeline(ImagesPipeline):
    def get_media_requests(self,item,info):
        image_url=item["image_url"]
        yield scrapy.Request(image_url)
        
class MyDownloadImagePipeline(object):
    def process_item(self, item, spider):
        img_path="/data/baidu"
        image_url=item["image_url"]
        referer=item["referer"]
        referer=referer.encode("utf8")
        filename = os.path.basename(image_url)
        new_name=""
        h1 = hashlib.md5(image_url.encode("utf8"))
        new_name=h1.hexdigest()
        new_name+=".jpg"
        search_word_dir=img_path+"/"+item["search_word"]
        file_full_name = img_path+"/"+new_name #拼接图片名   
        if os.path.exists(file_full_name):
            print("图片已经存在,不进行下载:"+file_full_name)
            item["img_path"]=file_full_name
            return item
        else:
            try:
                req = urllib.request.Request(image_url)
                req.add_header('Referer', referer)
                f = urllib.request.urlopen(req)
                pic = f.read()
                fp = open(file_full_name ,'wb')
                fp.write(pic) #写入图片   
                item["img_path"]=file_full_name
            except:
                item["img_path"]=""
            return item
          
class MongoDBPipeline(ImageItem):
    def process_item(self, item, spider):
        conn = MongoClient('127.0.0.1', 27017)
        db = conn.baidu
        image = db.image
        name=item['search_word']
        search_word=item['search_word']
        img_path=item["img_path"]
        image_url=item["image_url"]
        if img_path !="":
            isFind=image.find_one({"image_url":image_url})
            if isFind is None:
                image.insert_one({"name":name,"image_url":image_url,"search_word":search_word,"img_path":img_path})
                print("插入数据："+image_url)
            else:
                print("已经存在，不进行数据插入:"+image_url)
            return item
        else:
            print("img_path为空"+image_url)
    