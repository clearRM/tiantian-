# -*- coding:utf-8 -*-
import urllib.request
from lxml import etree
import time
import configparser
import queue
import os

config = configparser.ConfigParser()
# 读取配置文件里输入的股票代码
cr = config.read("config.ini")
headers = {"User-Agent ":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1"}
q = queue.Queue(20)
def selecturl():
	url_number = config.get("select_url","url_number")
	# 将配置文件里的股票代码取出 保存到列表list1
	list1 = list(map(int,url_number.split(' ')))
	# 读取列表里的股票代码 并存入到队列
	for num in list1:
		global q
		q.put(num)
	# 这里利用队列取尽时的异常 来判断是否取尽 取尽则停止三秒 并清空控制台输出
	while True:
		try:
			page = q.get(False)
			global url
			# 拼接目标url
			url = 'http://fund.eastmoney.com/'+str(page)+'.html?spm=search'
			spider()
		except:
			time.sleep(3)
			# 清空控制台输出
			os.system('cls')
			selecturl()

def spider():
	# 构造请求
	request = urllib.request.Request(url, headers=headers)
	# 发送请求
	html = urllib.request.urlopen(request).read()
	# 构造一个XPath解析对象（也对html文本进行自动修正）
	content = etree.HTML(html)
	# 通过设置xpath规则来提取目标数据
	# 获取股票的变化情况
	change = content.xpath('//dl[@class="floatleft fundZdf"]//span[@id="gz_gszzl"]')
	# 获取代码对应页面对应股票的名称
	name = content.xpath('//div[@class="fundDetail-tit"]')
	# 进行编码为utf8格式 并去掉首尾的空格
	change1 = change[0].xpath('string(.)').encode('utf-8').strip()
	name1 = name[0].xpath('string(.)').encode('utf-8').strip()
	# 解码
	name_final = name1.decode('UTF-8', 'strict')
	change_final = change1.decode('UTF-8', 'strict')
	# 合并字符串
	name_merge = name_final + "目前净值估算为："
	info = name_merge + change_final
	print(info)

	#如需保持到特定文档 则解注释如下代码
	'''with open('C:\\Users\Administrator\\Desktop\\' + '实时涨跌' + '.txt','a+') as f:
			f.write(a)
			f.write('\n')'''



if __name__ == '__main__':
	selecturl()
















