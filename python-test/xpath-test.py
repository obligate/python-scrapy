# _*_ coding: utf-8 _*_
# @Time     : 2020/10/27 17:24
# @Author   : Peter
# @File     : xpath-test.py

from lxml import html

etree = html.etree
html = etree.parse('./xpath.html')
# result = etree.tostring(html, pretty_print=True)
# print(result.decode('utf-8'))

# 1. 匹配所有带有code属性的属性值
# print(html.xpath('//@code'))
# 2. 多个匹配条件
# print(html.xpath('//div[@id="testid"]/h2/text() | //li[@data]/text()'))

# 3. Axes（轴）
# 1. child：选取当前节点的所有子元素
# print(html.xpath('//div[@id="testid"]/child::ul/li/text()'))   #child子节点定位
# print(html.xpath('//div[@id="testid"]/child::*'))              #child::*当前节点的所有子元素
# print(html.xpath('//div[@id="testid"]/child::ol/child::*/text()')) #定位某节点下为ol的子节点下的所有节点
# 2. attribute：选取当前节点的所有属性
# print(html.xpath('//div/attribute::id'))              # attribute定位id属性值)
# print(html.xpath('//div[@id="testid"]/attribute::*')) # 定位当前节点的所有属性)
# 3. ancestor：父辈元素 / ancestor-or-self：父辈元素及当前元素
#    descendant：后代 / descendant-or-self：后代及当前节点本身，使用方法同 ancestor
# print(html.xpath('//div[@id="testid"]/ancestor::div/@price'))  # 定位父辈div元素的price属性
# print(html.xpath('//div[@id="testid"]/ancestor::div'))         # 所有父辈div元素
# print(html.xpath('//div[@id="testid"]/ancestor-or-self::div')) # 所有父辈及当前节点div元素
# 4. following :选取文档中当前节点的结束标签之后的所有节点
# print(html.xpath('//div[@id="testid"]/following::div[not(@id)]/.//li[1]/text()')) #定位testid之后不包含id属性的div标签下所有的li中第一个li的text属性
# 5. namespace：选取当前节点的所有命名空间节点
# print(html.xpath('//div[@id="testid"]/namespace::*'))   # 选取命名空间节点
# 6. parent：选取当前节点的父节点
# print(html.xpath('//li[@data="one"]/parent::ol/li[last()]/text()')) # 选取data值为one的父节点的子节点中最后一个节点的值
# 7. preceding：选取文档中当前节点的开始标签之前的所有节点
# print(html.xpath('//div[@id="testid"]/preceding::div/ul/li[1]/text()')[0]) #记住是标签开始之前，同级前节点及其子节点
#下面这两条可以看到其顺序是靠近testid节点的优先
# print(html.xpath('//div[@id="testid"]/preceding::li[1]/text()')[0])
# print(html.xpath('//div[@id="testid"]/preceding::li[3]/text()')[0])
# 8. preceding-sibling：选取当前节点之前的所有同级节点
#记住只能是同级节点
# print(html.xpath('//div[@id="testid"]/preceding-sibling::div/ul/li[2]/text()')[0])
# print(html.xpath('//div[@id="testid"]/preceding-sibling::li')) #这里返回的就是空的了
# 9. self：选取当前节点
#选取带id属性值的div中包含data-h属性的标签的所有属性值
# print(html.xpath('//div[@id]/self::div[@data-h]/attribute::*'))
# 10. 组合拳
# 定位id值为testid下的ol下的li属性值data为two的父元素ol的兄弟前节点h2的text值
# print(html.xpath('//*[@id="testid"]/ol/li[@data="two"]/parent::ol/preceding-sibling::h2/text()')[0])


# 4. position定位
# print(html.xpath('//*[@id="testid"]/ol/li[position()=2]/text()')[0])

# 5. 条件
# 定位所有h2标签中text值为`这里是个小标题`
# print(html.xpath(u'//h2[text()="这里是个小标题"]/text()')[0])

# 6. 函数
# 1. count：统计
# print(html.xpath('count(//li[@data])'))   #节点统计
# 2. concat：字符串连接
# print(html.xpath('concat(//li[@data="one"]/text(),//li[@data="three"]/text())'))
# 3. string：解析当前节点下的字符
# string只能解析匹配到的第一个节点下的值，也就是作用于list时只匹配第一个
# print(html.xpath('string(//li)'))
# 4. local-name：解析节点名称
# print(html.xpath('local-name(//*[@id="testid"])')) # local-name解析节点名称
# 5. contains(string1,string2)：如果 string1 包含 string2，则返回 true，否则返回 false
# print(html.xpath('//h3[contains(text(),"H3")]/a/text()')[0]) #使用字符内容来辅助定位
#一记组合拳
# 匹配带有href属性的a标签的先辈节点中的div，其兄弟节点中前一个div节点下ul下li中text属性包含“务”字的节点的值
# print(html.xpath(u'//a[@href]/ancestor::div/preceding::div/ul/li[contains(text(),"务")]/text()')[0])
# 注意：兄弟节点后一个节点可以使用：following-sibling
# 6. not：布尔值（否）
# print(html.xpath('count(//li[not(@data)])')) #不包含data属性的li标签统计
# 7. string-length：返回指定字符串的长度
# string-length函数+local-name函数定位节点名长度小于2的元素
# print(html.xpath('//*[string-length(local-name())<2]/text()')[0])
# 8. 组合拳2
# contains函数+local-name函数定位节点名包含di的元素
# print(html.xpath('//div[@id="testid"]/following::div[contains(local-name(),"di")]'))
# 9. or：多条件匹配
# print(html.xpath('//li[@data="one" or @code="84"]/text()')) # or匹配多个条件
#也可使用|
# print(html.xpath('//li[@data="one"]/text() | //li[@code="84"]/text()')) # |匹配多个条件
# 10 .组合拳3：floor + div除法 + ceiling
#position定位+last+div除法，选取中间两个
# print(html.xpath('//div[@id="go"]/ul/li[position()=floor(last() div 2+0.5) or position()=ceiling(last() div 2+0.5)]/text()'))
# 11. 组合拳4隔行定位：position+mod取余
# position+取余运算隔行定位
# print(html.xpath('//div[@id="go"]/ul/li[position()=((position() mod 2)=0)]/text()'))
# 12. starts-with：以。。开始
#starts-with定位属性值以8开头的li元素
# print(html.xpath('//li[starts-with(@code,"8")]/text()')[0])


# 7.数值比较
# 1. <：小于
#所有li的code属性小于200的节点
# print(html.xpath('//li[@code<200]/text()'))
# 2. div：对某两个节点的属性值做除法
# print(html.xpath('//div[@id="testid"]/ul/li[3]/@code div //div[@id="testid"]/ul/li[1]/@code'))
# 3. 组合拳4：根据节点下的某一节点数量定位
# 选取所有ul下li节点数大于5的ul节点
# print(html.xpath('//ul[count(li)>5]/li/text()'))


# 8. 将对象还原为字符串
# s = html.xpath('//*[@id="testid"]')[0] #使用xpath定位一个节点
# print(s)
# s2 = etree.tostring(s) #还原这个对象为html字符串
# print(s2)


# 9. 选取一个属性中的多个值
# 举例：<div class="mp-city-list-container mp-privince-city" mp-role="provinceCityList">
# 选择这个div的方案网上有说用and的，但是似乎只能针对不同的属性的单个值
# 本次使用contains
# .xpath('div[contains(@class,"mp-city-list-container mp-privince-city")]')
# 当然也可以直接选取其属性的第二个值
# .xpath('div[contains(@class,"mp-privince-city")]')
# 重点是class需要添加一个@符号



