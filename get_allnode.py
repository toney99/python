# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import json
import re
# import get_product,save_asin, get_two_menu
import mongo_db

url = "https://www.amazon.com/gp/site-directory/"
# ch_url = "https://www.amazon.com/home-automation-smarthome/b/ref=sd_allcat_homaut?ie=UTF8&node=6563140011"
ch_url = "https://www.amazon.com/Kitchen-and-Bath-Fixtures/b/ref=sd_allcat_kbf?ie=UTF8&node=3754161"
base = "https://www.amazon.com"

headers = {
	'Accept':'image/webp,image/*,*/*;q=0.8',
	'Accept-Encoding':'gzip, deflate, sdch, br',
	'Accept-Language':'zh-CN,zh;q=0.8',
	'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36',
}

# 读取https://www.amazon.com/gp/site-directory/中的所有的二级菜单的地址
# 根据二级菜单的地址获取该菜单下所有子节点的url地址
# 每个二级菜单下的子菜单位于不同的位置，需要按每个菜单的特点进行解析
def get_allnode(ch_url, name, parent_name):
	try:
		r = requests.get(ch_url, headers=headers)
		soup = BeautifulSoup(r.text, 'lxml')
	except:
		print 'requests error'
		pass
	# res = soup.select('div.categoryRefinementsSection > ul > li > a')
	# res = soup.select('ul.forExpando > li > a')
	selector = [
		'div.categoryRefinementsSection > ul > li'
		'ul.refinementNodeChildren > li > a',
		'ol.a-carousel > li > a',
	]
	for s in selector:
		node = soup.select(s)
		if node:
			# for n in node:
			# 	print n['href']
			print name
			break
		else:
			pass
	if not node:
		print parent_name, name, ch_url
	# 	r = requests.get(ch_url, headers=headers)
	# 	soup = BeautifulSoup(r.text, 'lxml')
	# 	if not soup.select('div#refinements'):
	# 		# print '#??#' * 40
	# 		print ch_url
	# 		# print '#??#' * 40
	# 	return
	# for r in node_children:
	# 	url =  base + r['href']
	# 	name = r.find('span') and r.find('span').text or ''
	# 	print 'node_children', url, name
	# 	get_two_menu.get_page_num(url)
	return True

# 获取direct菜单下指定一级菜单的二级菜单，默认为所有direct菜单的所有二级菜单
def check_direct_name(name=''):
	sheet_tab = mongo_db.mongo_connect('amazon', 'main_menu_url')
	if name:
		res = sheet_tab.find({'parent_name':name})
	else:
		res = sheet_tab.find()
	for r in res:
		# print '****' * 40
		# print res.count(), r['parent_name'], r['url']
		# print '****' * 40
		get_allnode(r['url'], r['name'], r['parent_name'])

# check_direct_name('Home, Garden & Tools')
parent_name_list = [
	'Electronics & Computers',
	'Home, Garden & Tools',
	'Beauty, Health & Grocery',
	'Toys, Kids & Baby',
	'Clothing, Shoes & Jewelry',
	'Sports & Outdoors',
	'Automotive & Industrial',
	'Handmade',
]
for name in parent_name_list:
	check_direct_name(name)

