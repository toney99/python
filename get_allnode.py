# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import json
import re
from random import random,randint
# import get_product,save_asin, get_two_menu
import mongo_db
import time

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
		# print soup.select('div#refinements')
		# print soup.select('div.shoppingEngineSectionHeaders')
		# print soup.select('div.categoryRefinementsSection')
		# return
	except:
		print 'requests error'
		return
	selector = [
		'div.categoryRefinementsSection > ul > li',
		'ul.refinementNodeChildren > li > a',
		'ol.a-carousel > li > a',
	]
	vals = {
		'parent_name':parent_name,
		'name':name,
		'url':ch_url,
	}
	sheet_tab = mongo_db.mongo_connect('amazon', 'select_url')
	for s in selector:
		node = soup.select(s)
		if node:
			print name
			vals['soup'] = True
			if not sheet_tab.find({'url':ch_url}).count():
				sheet_tab.insert(vals)
			break
		else:
			pass
	if not node:
		print parent_name, name, ch_url
		print '****' * 40
		vals['soup'] = False
		if not sheet_tab.find({'url':ch_url}).count():
			sheet_tab.insert(vals)
		# time.sleep(30)
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
		# print res.count(), r['parent_name'], r['url'].split('/')
		s_num = str(randint(100, 999)) + '-' + str(randint(1000000, 9999999)) + '-' + str(randint(1000000, 9999999))
		s = r['url'].split('/')
		# s[-1] = s_num + "?" + str(s[-1].split('?')[-1])
		s[-1] = "?" + str(s[-1].split('?')[-1])
		url = "/".join(s)
		# print '****' * 40
		get_allnode(url, r['name'], r['parent_name'])

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
# url = "https://www.amazon.com/Camera-Photo-Film-Canon-Sony/b/ref=sd_allcat_p/?ie=UTF8&node=502394"
# get_allnode(url, 'name', 'parent_name')
