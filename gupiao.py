# -*- coding:utf-8 -*-

import urllib.request
from lxml import etree
import time
import configparser
import queue
import os

config = configparser.ConfigParser()
cr = config.read("config.ini")
headers = {"User-Agent ":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1"}
q = queue.Queue(20)
i = 0
def selecturl():
	url_number = config.get("select_url","url_number")
	a = list(map(int,url_number.split(' ')))

	for num in a:
		global q
		q.put(num)
	global i
	i = q.qsize()
	while True:
		try:
			page = q.get(False)
			global url
			url = 'http://fund.eastmoney.com/'+str(page)+'.html?spm=search'
			#print(url)
			spider()
		except:
			time.sleep(3)
			os.system('cls')
			selecturl()

def spider():
	request = urllib.request.Request(url, headers=headers)
	html = urllib.request.urlopen(request).read()
	content = etree.HTML(html)
	bloger = content.xpath('//dl[@class="floatleft fundZdf"]//span[@id="gz_gszzl"]')
	bloger2 = content.xpath('//div[@class="fundDetail-tit"]')

	info4 = bloger[0].xpath('string(.)').encode('utf-8').strip()
	info2 = bloger2[0].xpath('string(.)').encode('utf-8').strip()

	info3 = info2.decode('UTF-8', 'strict')
	info = info4.decode('UTF-8', 'strict')
	info7 = info3 + "目前净值估算为："
	all = info7 + info
	print(all)

	#如需保持到特定文档 则解注释如下代码
	'''with open('C:\\Users\Administrator\\Desktop\\' + '实时涨跌' + '.txt','a+') as f:
			f.write(a)
			f.write('\n')'''



if __name__ == '__main__':
	selecturl()
















