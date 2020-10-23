## 准备
### 虚拟环境
`mkvirtualenv --python D:\Software\Python\3.7.3\python.exe article_spider`

### 安装scrapy
`pip install  -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com  scrapy`
> windows如果安装scrapy报错，可以参考 `https://www.lfd.uci.edu/~gohlke/pythonlibs/` 下载对应的windows下需要的文件
>`pip install  -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com  lxml‑4.6.1‑cp37‑cp37m‑win_amd64.whl`

### 体验
```
scrapy startproject ArticleSpider
cd ArticleSpider
scrapy genspider cnblogs news.cnblogs.com
scrapy crawl cnblogs                   #  启动爬虫
```
## xpath


## refer
- [python extension packages for window](https://www.lfd.uci.edu/~gohlke/pythonlibs/)
- [英文](https://docs.scrapy.org/en/latest/) https://docs.scrapy.org/en/latest/
- [中文](https://www.osgeo.cn/scrapy/) https://www.osgeo.cn/scrapy/