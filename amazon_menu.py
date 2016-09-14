# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import json
import re

url = "https://www.amazon.com/"
url_direct = "https://www.amazon.com/gp/site-directory/s"

headers = {
	'Accept':'image/webp,image/*,*/*;q=0.8',
	'Accept-Encoding':'gzip, deflate, sdch, br',
	'Accept-Language':'zh-CN,zh;q=0.8',
	'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36',
}

r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.text, 'lxml')
n = 0
# for i in soup.select('script'):
# 	print i
# 	print '={}='.format(n) * 60
# 	n = n + 1
menu_str = str(soup.select('script')[23])
pattern = re.compile('"url":"/(.+){30,80}"')
res = pattern.findall(menu_str)
# res.group()
for l in res:
	print l
	print "===" * 50
print type(res), len(res)
# j = json.loads(str(menu_str))
# print type(menu_str)