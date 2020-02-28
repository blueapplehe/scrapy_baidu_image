# scrapy_baidu_image
爬取百度图片的scrapy爬虫实现

说明

1选取了'http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word='月季花'     地址搜索图片，该地址有返回页码，比较容易遍历图片

2百度图片使用了ajax动态获取数据，因此scrapy选用了chromedriver做js动态渲染

3存在图片搜索关键字和图片路径使用mongodb存储，在baidu.pipelines.MongoDBPipeline中实现

4配置中禁用了robots，修改了USER_AGENT，爬取图片时加上referer，这些是绕过百度拦截爬虫和防止盗链必须的。

主要代码实现位置：

/baidu/spiders/imageSpider.py

/baidu/pipelines.py


需要安装的库：

  pip install scrapy==1.6 -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
  
  pip install selenium -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
  
  pip install scrapy_splash -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
  
  pip install pillow -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
  
  pip install requests -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
  
  pip install pymongo -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
 
 chrome驱动下载地址
 
 https://npm.taobao.org/mirrors/chromedriver/
 
 下载和自己浏览器版本对应的驱动
 
 修改middlewares.py文件中的
 
 self.browser = webdriver.Chrome(executable_path="D:/scrapy_baidu_image/chromedriver.exe",chrome_options=option)
 
 executable_path指向你为你下载的chromedriver.exe的目录文件路径
 
 

做该爬虫主要是本人做神经网络研究时使用，所以分享出来给大家了，轮子还是不错，实现简洁，2019年1月还是可以正常使用，以后每月更新一次

最后说明，请文明爬取数据，不要太频繁，给对方服务器造成压力。

本文仅供大家学习使用



