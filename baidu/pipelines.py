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
import time
from scrapy.conf import settings
import shutil
class BaiduPipeline(ImageItem):
    def process_item(self, item, spider):
        return item
        
class DownloadImagePipeline(ImagesPipeline):
    def get_media_requests(self,item,info):
        image_url=item["image_url"]
        yield scrapy.Request(url=image_url,meta={'is_image': True})

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            #raise DropItem("Item contains no images")
            return item
        IMAGES_STORE=settings.get('IMAGES_STORE')
        if image_paths[0]:
            target_path="/data/baidu"
            name_dir=target_path+"/"+item["name"]
            if not os.path.exists(name_dir):
                os.mkdir(name_dir)
            origin_file=IMAGES_STORE+"/"+image_paths[0]
            filename = os.path.basename(origin_file)
            ext=filename.split(".")[1]
            ext=ext.lower()
            if ext!="jpg" and ext!="png" and ext!="jpeg":
                item["img_path"]=""
                return item 
            target_file=name_dir+"/"+filename
            shutil.copyfile(origin_file,target_file)
            item['img_path'] = target_file
            return item
        
class MyDownloadImagePipeline(object):
    def process_item(self, item, spider):
        img_path="/data/baidu"
        image_url=item["image_url"]
        referer=item["referer"]
        referer=referer.encode("utf8")
        filename = os.path.basename(image_url)
        ext=filename.split(".")[1]
        if ext!="jpg" :
            item["img_path"]=""
            return item 
        new_name=""
        h1 = hashlib.md5(image_url.encode("utf8"))
        new_name=h1.hexdigest()
        new_name+="."+ext
        name_dir=img_path+"/"+item["name"]
        if not os.path.exists(name_dir):
            os.mkdir(name_dir)
        file_full_name = name_dir+"/"+new_name #拼接图片名   
        if os.path.exists(file_full_name):
            print("图片已经存在,不进行下载:"+file_full_name)
            item["img_path"]=file_full_name
            return item
        else:
            try:
                req = urllib.request.Request(image_url)      
                req.add_header('Referer', referer)
                f = urllib.request.urlopen(req, timeout=3)
                pic = f.read()
                fp = open(file_full_name ,'wb')
                fp.write(pic) #写入图片   
                item["img_path"]=file_full_name
            except Exception as e:
                print(e)
                item["img_path"]=""
            return item
          
class MongoDBPipeline(ImageItem):
    def process_item(self, item, spider):
        conn = MongoClient('127.0.0.1', 27017)
        db = conn.baidu
        image = db.image
        name=item['name']
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
    