# scrapy_baidu_image
爬取百度图片的scrapy爬虫实现
说明
1选取了'http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word='+search_word地址搜索图片，该地址有返回页码，比较容易遍历图片
2百度图片使用了ajax动态获取数据，因此scrapy选用了splash做js动态渲染，splash怎么安装请自行百度
3下载图片，没有采用官方的ImagesPipeline模块，而是自实现了下载pipelines，在baidu.pipelines.MyDownloadImagePipeline位置
4存在图片搜索名称和图片路径使用mongodb存储，在baidu.pipelines.MongoDBPipeline中实现



