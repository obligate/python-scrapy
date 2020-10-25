[TOC]

## 1准备
### 1.1 虚拟环境
`mkvirtualenv --python D:\Software\Python\3.7.3\python.exe article_spider`

### 1.2 安装scrapy
`pip install  -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com  scrapy`
> windows如果安装scrapy报错，可以参考 `https://www.lfd.uci.edu/~gohlke/pythonlibs/` 下载对应的windows下需要的文件
>`pip install  -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com  lxml‑4.6.1‑cp37‑cp37m‑win_amd64.whl`

### 1.3 体验
```
scrapy startproject ArticleSpider
cd ArticleSpider
scrapy genspider cnblogs news.cnblogs.com
scrapy crawl cnblogs                   #  启动爬虫
```
### 1.4如何在pycharm中debug scrapy
```
例如： cd ArticleSpider，在ArticleSpider目录创建一个main.py
# 1. 需要把当前文件所在的根目录添加到环境变量才可以进行debug
sys.path.append(os.path.dirname(os.path.abspath(__file__))) 
# 2. 使用execute执行命令
execute(['scrapy', 'crawl', 'cnblogs'])
# 3. 就可以在spider中，添加断点，进行debug
```
### 1.5 scrapy shell 调试
```
进入cmd命令，进入虚拟环境所在文件夹
执行命令 activate
(venv-scrapy) E:\venv-scrapy\Scripts> scrapy shell https://news.cnblogs.com/n/675731/
>>> response.css('#news_title a::text').extract_first("")
'McAfee 30年沉浮录：行业黄金时代一去不复返？'
```
![demo3](doc-imgs/31.png)
![demo3](doc-imgs/32.png)
### 1.6 chrome xpath 
- 打开`开发者工具`
- 选择`Console`选项卡
- 使用`$x()`测试`xpath`脚本
```
# 获取节点的文本我们用text()或者.innerText
$x('//div[@id="news_title"]/a/text()')[0]
$x('//div[@id="news_title"]/a')[0].innerText
```
![demo2](doc-imgs/2.png)

或者再控制ctrl + F 输入 //div[@id="news_title"]/a  看是否支持xpath匹配
![demo1](doc-imgs/1.png)
## 2. xpath
### 2.1 xpath简介
+ 1. xpath使用路径表达式在xml和html中进行导航
+ 2. xpath包含标准函数库
+ 3. xpath是一个w3c的标准

### 2.2 xpath术语
+ 1. 父节点
+ 2. 子节点
+ 3. 同胞节点
+ 4. 先辈节点
+ 5. 后代节点

### 2.3 xpath语法
```
# url = response.xpath('//*[@id="entry_675694"]/div[2]/h2/a/@href').extract_first("")
# url = response.xpath('//div[@id="news_list"]/div[1]/div[2]/h2/a/@href').extract_first("")
url = response.xpath('//div[@id="news_list"]//h2[@class="news_entry"]/a/@href').extract_first("")
```
#### 2.3.1 语法1

| **表达式**   | **说明**                                                     |
| ------------ | ------------------------------------------------------------ |
| article      | 选取所有article元素的所有子节点                              |
| /article     | 选取根元素article                                            |
| article/a    | 选取所有属于article的子元素的a元素                           |
| //div        | 选取所有div子元素(不论出现在文档任何地方)                    |
| article//div | 选取所有属于article元素的后代的div元素，不管它出现在article之下的任何位置 |
| //@class     | 选取所有名为class的属性                                      |

#### 2.3.2 语法2

| **表达式**             | **说明**                                 |
| ---------------------- | ---------------------------------------- |
| /article/div[1]        | 选取属于article子元素的第一个div元素     |
| /article/div[last()]   | 选取属于article子元素的最后一个div元素   |
| /article/div[last()-1] | 选取属于article子元素的倒数第二个div元素 |
| //div[@lang]           | 选取所有拥有lang属性的div元素            |
| //div[@lang='eng']     | 选取所有lang属性为eng的div元素           |

#### 2.3.3 语法3

| **表达式**             | **说明**                                                     |
| ---------------------- | ------------------------------------------------------------ |
| /div/*                 | 选取属于div元素的所有子节点                                  |
| //*                    | 选取所有元素                                                 |
| //div[@*]              | 选取所有带属性的title元素                                    |
| //div/a \| //div/p     | 选取所有div元素的a和p元素                                    |
| //span \| //ul         | 选取文档中的span和ul元素                                     |
| article/div/p\| //span | 选取所有属于article元素的div元素的p元素 以及文档中所有的span元素 |

## 3. css
`url = response.css('div#news_list h2.news_entry a::attr(href)').extract()`
### 3.1 css选择器1

| **表达式**          | **说明**                               |
| ------------------- | -------------------------------------- |
| *                   | 选择所有节点                           |
| #container          | 选择id为container的节点                |
| .container          | 选取所有class包含container的节点       |
| li  a               | 选取所有li下的所有a节点                |
| ul  + p             | 选择ul后面的第一个p元素                |
| div#container  > ul | 选取id为container的div的第一个ul子元素 |

### 3.2 css选择器2

| **表达式**                   | **说明**                               |
| ---------------------------- | -------------------------------------- |
| ul  ~ p                      | 选取与ul相邻的所有p元素                |
| a[title]                     | 选取所有有title属性的a元素             |
| a[href=“http://jobbole.com”] | 选取所有href属性为jobbole.com值的a元素 |
| a[href*=”jobole”]            | 选取所有href属性包含jobbole的a元素     |
| a[href^=“http”]              | 选取所有href属性值以http开头的a元素    |
| a[href$=“.jpg”]              | 选取所有href属性值以.jpg结尾的a元素    |
| input[type=radio]:checked    | 选择选中的radio的元素                  |

### 3.3 css选择器3

| **表达式**          | **说明**                       |
| ------------------- | ------------------------------ |
| div:not(#container) | 选取所有id非container的div属性 |
| li:nth-child(3)     | 选取第三个li元素               |
| tr:nth-child(2n)    | 第偶数个tr                     |

### 3.4 总结
```
# 1.xpath
# url = response.xpath('//*[@id="entry_675694"]/div[2]/h2/a/@href').extract_first("")
# url = response.xpath('//div[@id="news_list"]/div[1]/div[2]/h2/a/@href').extract_first("")
# url = response.xpath('//div[@id="news_list"]//h2[@class="news_entry"]/a/@href').extract_first("")

# 2. css selector
# url = response.css('div#news_list h2.news_entry a::attr(href)').extract()

# 3.通过Selector来实现，需要导入from scrapy import Selector,主要是为了自己使用方便，建议还是使用1,2
sel = Selector(text=response.text)
url = response.css('div#news_list h2.news_entry a::attr(href)').extract()
```

## 4. http code

| **code** | **说明**                  |
| -------- | ------------------------- |
| 200      | 请求被成功处理            |
| 301/302  | 永久性重定向/临时性重定向 |
| 403      | 没有权限访问              |
| 404      | 表示没有对应的资源        |
| 500      | 服务器错误                |
| 503      | 服务器停机或正在维护      |

## yield

## 获取ajax请求的数据
```
pip install -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com requests
# 获取数据
import requests
import json
response = requests.get('https://news.cnblogs.com/NewsAjax/GetAjaxNewsInfo?contentId=675731')
print(response.text)
j_data = json.loads(response.text)
print(j_data['TotalView'])
```

## 图片的下载配置
- [media-pipeline](https://docs.scrapy.org/en/latest/topics/media-pipeline.html)
```
1.需要在settings.py中设置image pipeline，默认的
ITEM_PIPELINES = {
   'scrapy.pipelines.images.ImagesPipeline': 1,
}
2. 需要配置image的store和字段IMAGES_URLS_FIELD
IMAGES_URLS_FIELD = "front_image_url"
project_dir = os.path.abspath(os.path.dirname(__file__))
IMAGES_STORE = os.path.join(project_dir, 'images')
3. 需要安装pillow模块
pip install -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com pillow
4. 如果需要获取真实的存储路径，需要重新pipeline的item_completed方法
class ArticleImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        if "front_image_url" in item:
            for ok, value in results:
                image_file_path = value["path"]
            item["front_image_path"] = image_file_path

        return item
需要在setting.py中设置
'ArticleSpider.pipelines.ArticleImagePipeline': 1,
```
## mysql 保存
```
1. 安装mysql驱动
pip install -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com mysqlclient
2. 需要提供一个pipeline
class MysqlPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect('127.0.0.1', 'root', 'root', 'article_spider', charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """
            insert into cnblogs_article(title, url, create_date, fav_nums)
            VALUES (%s, %s, %s, %s)
        """
        self.cursor.execute(insert_sql, (item["title"], item["url"], item["create_date"], item["fav_nums"]))
        self.cursor.execute(insert_sql, (item.get("title", ""), item["url"], item["create_date"], item["fav_nums"]))
        self.conn.commit()
3.需要在setting.py中设置
'ArticleSpider.pipelines.MysqlPipeline': 4,
```
## refer

- [python extension packages for window](https://www.lfd.uci.edu/~gohlke/pythonlibs/)
- [英文](https://docs.scrapy.org/en/latest/) https://docs.scrapy.org/en/latest/
- [中文](https://www.osgeo.cn/scrapy/) https://www.osgeo.cn/scrapy/
- [xpath函数](https://www.w3school.com.cn/xpath/xpath_functions.asp)