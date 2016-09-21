# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import json
import re
import mongo_db

url = "https://www.amazon.com/gp/site-directory/"
base = "https://www.amazon.com"

headers = {
	'Accept':'image/webp,image/*,*/*;q=0.8',
	'Accept-Encoding':'gzip, deflate, sdch, br',
	'Accept-Language':'zh-CN,zh;q=0.8',
	'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36',
}
# 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0',
# 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
# 'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
# 'Accept-Encoding': 'gzip, deflate, br',

# 根据directory这个url，拿到所有分类菜单的url
def save_directory_url(url):
	r = requests.get(url, headers=headers)
	soup = BeautifulSoup(r.text, 'lxml')
	n = 0
	all_urls = []
	sheet_tab = mongo_db.mongo_connect('amazon', 'main_menu_url')
	for i in soup.select('div.fsdDeptBox'):
		parent_name =  i.find('h3').text
		url_list = i.select('div.fsdDeptCol > a')
		for u in url_list:
			print u['href'], u.text
			vals = {}
			child_url = str(u['href']).strip()
			if child_url[:1] == '/':
				vals['name'] = u.text
				vals['url'] = base + child_url
				vals['parent_name'] = parent_name
				vals['if_next'] = False
				sheet_tab.insert(vals)
				all_urls.append(child_url)
		n = n + 1
	return all_urls

	
# save_directory_url(url)
# 
# all_urls = save_directory_url(url)


# main_url = 'https://www.amazon.com'
# n = 0
# print 'There is {} '.format(len(all_urls))
# for r in all_urls:
# 	url = main_url + r
# 	r = requests.get(url, headers=headers)
# 	soup = BeautifulSoup(r.text, 'lxml')
# 	# print url
# 	if not soup.select('div.categoryRefinementsSection'):
# 		print url
# 		print '==={}==='.format(n)*20
# 	# print soup.select('div.categoryRefinementsSection')
# 		n = n+1