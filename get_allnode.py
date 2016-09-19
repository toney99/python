# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import json
import re
from random import random,randint
import get_two_menu
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

selector = [
	'div.categoryRefinementsSection > ul > li > a',
	'ul.refinementNodeChildren > li > a',
	'ol.a-carousel > li > a',
]


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
	# selector = [
	# 	'div.categoryRefinementsSection > ul > li',
	# 	'ul.refinementNodeChildren > li > a',
	# 	'ol.a-carousel > li > a',
	# ]
	vals = {
		'parent_name':parent_name,
		'name':name,
		'url':ch_url,
		'final_node':False,
		'level':1,
		'count':0,
		'used':False,
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
# for name in parent_name_list:
# 	check_direct_name(name)

sheet_tab = mongo_db.mongo_connect('amazon', 'select_url')
level = 1
res = sheet_tab.find({'level':level, 'soup':True, 'final_node':False, 'used':False})
while res.count():
	sheet_tab_n = mongo_db.mongo_connect('amazon', 'select_url')
	url_list = []
	for s in res:
		vals = {
			'parent_name':s['name'],
			'level':s['level'] + 1,
		}
		url = s['url']
		try:
			r = requests.get(url, headers=headers)
			soup = BeautifulSoup(r.text, 'lxml')
		except:
			print "#####get page error"
			continue
		# sheet_tab.update({'url':url}, {'$set':{'used':True}})
		for sel in selector:
			node = soup.select(sel)
			if node:
				for n in node:
					url_c = str(n['href']).strip()
					# 去掉url中的/162-3723623-3232876?
					if len(url_c.split('?')[0].split('/')[-1].split('-')) != 3:
						continue
					else:
						url_c = "/".join(url_c.split('/')[0:-1]) + '?' + url_c.split('?')[-1]
						# continue
					vals['url'] = base + url_c
					vals['count'] = 0
					vals['name'] = 'my_name'
					vals['used'] = False
					span = n.find_all('span')
					# 判断soup有无span标签。若无，则说明不是子菜单
					if not span:
						continue
					# 是否是最底层的菜单
					if vals['parent_name'] == vals['url']:
						vals['soup'] = False
						vals['final_node'] = True
						print "******This is ths final node...........#####################################"
					else:
						vals['soup'] = True
						vals['final_node'] = False
					if not sheet_tab_n.find({'url':vals['url']}).count() and vals['url'] not in url_list:
						url_list.append(vals)
						# sheet_tab_n.insert(vals)
					page = get_two_menu.get_page_num(vals['url'])
					if page:
						sheet_tab_page = mongo_db.mongo_connect('amazon', 'page_urls')
						sheet_tab_page.insert(page)
					print "####parent_name:", vals['parent_name'] 
					print vals['level'], vals['url']
					print '####span:', len(span), span
					# for p in span:
					# 	print p.text
					print '+++++++++++++++++++this is useful+++++++++++++++++++++'
				break
			else:
				pass

		if not node:
			print '#######this is the final node'
	# sheet_tab.insert(url_list)
	level = level + 1

