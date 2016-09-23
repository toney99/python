# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import json
import re
from random import random,randint
import direct_menu
import mongo_db
import time
import logging, os
from Logger import Logger
logger = Logger('/var/amazon/amazon_log.log',logging.ERROR,logging.DEBUG)

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

# 解析路径
selector = [
	'div.categoryRefinementsSection > ul > li > a',
	'ul.refinementNodeChildren > li > a',
	'ol.a-carousel > li > a',
]

# 需要爬取的大类名称
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

# 读取https://www.amazon.com/gp/site-directory/中的所有的二级菜单的地址
# 根据二级菜单的地址获取该菜单下所有子节点的url地址
# 每个二级菜单下的子菜单位于不同的位置，需要按每个菜单的特点进行解析
def save_allnode(ch_url, name, parent_name):
	try:
		r = requests.get(ch_url, headers=headers)
		soup = BeautifulSoup(r.text, 'lxml')
	except:
		print 'requests error'
		logger.info('save_allnode # request error {}'.format(ch_url))
		return
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
	# sheet_tab_error = mongo_db.mongo_connect('amazon', 'select_url_error')
	# 通过一组页面结构来解析获取子菜单url
	for s in selector:
		node = soup.select(s)
		if node:
			if not sheet_tab.find({'url':ch_url}).count():
				vals['soup'] = True   # soup = True表示该url能通过解析器解析
				sheet_tab.insert(vals)
				print 'ch_url', ch_url, vals['soup']
				logger.info('save_allnode # good soup ' + ch_url + vals['soup'])
			return True
		else:
			pass
	if not node:
		vals['soup'] = False
		if not sheet_tab.find({'url':ch_url}).count():
			sheet_tab.insert(vals)
			print 'ch_url', ch_url, vals['soup']
			logger.info('save_allnode # bad soup ' + ch_url + vals['soup'])
	return True

# 获取direct菜单下指定一级菜单的二级菜单，默认为所有direct菜单的所有二级菜单
def check_direct_name(name=''):
	sheet_tab = mongo_db.mongo_connect('amazon', 'main_menu_url')
	# 默认查找所有一级菜单的子菜单，查找一级菜单名name的子菜单是否能被解析
	if name:
		res = sheet_tab.find({'parent_name':name})
	else:
		res = sheet_tab.find()
	print '####' * 40
	print 'main_url_url len(res)', res.count()
	print '####' * 40
	logger.info('check_direct_name # res.count():' + res.count())

	for r in res:
		# 替换url中的这串随机数
		# s_num = str(randint(100, 999)) + '-' + str(randint(1000000, 9999999)) + '-' + str(randint(1000000, 9999999))
		# s[-1] = s_num + "?" + str(s[-1].split('?')[-1])
		
		# 去掉url中的/162-7223763-2234523？这串数字
		s = r['url'].split('/')
		s[-1] = "?" + str(s[-1].split('?')[-1])
		url = "/".join(s)

		# 保存/site-directory/一级菜单下的所有子菜单
		save_allnode(url, r['name'], r['parent_name'])

	return True



# 检查有没有保存主菜单，没有则保存
sheet_tab = mongo_db.mongo_connect('amazon', 'main_menu_url')
if not sheet_tab.find().count():
	direct_menu.save_directory_url(url)

# 检查有没有检查二级菜单
sheet_tab = mongo_db.mongo_connect('amazon', 'select_url')
if not sheet_tab.find().count():
	for name in parent_name_list:
		check_direct_name(name)
	
# 统计没有解析的url的数量
def check_used(res):
	count = 0
	for r in res:
		if not r['used']:
			count = count + 1
		else:
			pass
	# print 'not use count:', count
	logger.debug('count_used # count:' + str(count))
	return count

# res = [{
# 	'parent_name':'parent_name',
# 	'name':'name',
# 	'url':'https://www.amazon.com/Camera-Photo-Film-Canon-Sony/b/ref=sd_allcat_p?ie=UTF8&node=502394',
# 	'final_node':False,
# 	'level':1,
# 	'count':0,
# 	'used':False,
# }]

# 取出单个节点下的所有子菜单
def loop_look_node(s, node):
	url_list = []
	flag = 0
	for n in node:
		_vals = {}
		_vals['parent_name'] = s['name']
		_vals['level'] = s['level'] + 1
		# 通过a标签中第一个span的class的属性数量来判断是否是子菜单
		# 上级菜单的span中包含srSprite backArrow
		# 子菜单中的span中包含refinementLink
		# print n
		if not n.find('span'):
			continue
		name = str(n.find('span').text).encode('utf-8')
		print '###name', name, type(name)
		span = n.find_all('span')
		first_span = span and span[0]['class'] or []
		if len(first_span) > 1:
			continue
		flag = flag + 1
		url_c = str(n['href']).strip()
		# 去掉url中的/162-3723623-3232876?,检查是否含有这串数字
		if len(url_c.split('?')[0].split('/')[-1].split('-')) != 3:
			print '### url not contain num:', base + url_c
			logger.info('loop_look_node # not contain num:' + base + url_c)
			# continue
		else:
			url_c = "/".join(url_c.split('/')[0:-1]) + '?' + url_c.split('?')[-1]
		_vals['url'] = base + url_c
		_vals['count'] = 0
		_vals['name'] = name
		_vals['soup'] = True
		_vals['final_node'] = False
		_vals['used'] = False
		v = [k.get('url', False) for k in url_list]
		if _vals['url'] not in v:
			url_list.append(_vals)
			# print '++++++++++++++++++++++++++++++++++++++++++++++++++++++'
			# print _vals['level'], _vals['url']
			logger.info('check_direct_name # useful url :' + str(_vals['level']) + _vals['url'])
			# print '+++++++++++++++++++this is useful+++++++++++++++++++++'
		else:
			pass
	return url_list, flag

def get_final_node(res):
	level = 1
	# for i in range(1, 100):
	while True:
		pages = []
		for s in res:
			count = check_used(res)
			if not count:
				continue
			if s['used']:
				continue
			print 'count:', count
			url = s['url']
			try:
				r = requests.get(url, headers=headers)
				soup = BeautifulSoup(r.text, 'lxml')
			except:
				print "##################get page error",url
				logger.debug('@get_final_node # request page error:' + url)
				continue
			s['used'] = True
			for sel in selector:
				node = soup.select(sel)
				print sel
				if node:
					url_list, flag = loop_look_node(s, node)
					pages = pages + url_list
					if not flag:
						# print "####################This is ths final node...#####################################"
						s['final_node'] = True
						# print s['url']
						logger.info('****get_final_node**** final node:{}'.format(s['url']))
					break
				else:
					pass
			if not node:
				pass
				print "#######this node can't delivery########",url
			print 'parent name:', s['parent_name']
			print 'name:', s['name']
			print "name pages total:", len(pages)
			logger.info('****get_fina_node**** # parent_name: {} name {}'.format(s['parent_name'], s['name']))
			logger.info('****get_fina_node**** # name pages total:'.format(len(pages)))
		res = res + pages
		# time.sleep(5)

	return True

# 保存子节点
def save_final_node():
	sheet_tab = mongo_db.mongo_connect('amazon', 'select_url')
	sheet_final = mongo_db.mongo_connect('amazon', 'final_url')
	for s in sheet_tab.find({'soup':True}):
		print s
		res = get_final_node([s])
		print "####" * 40
		print "{} 大类 {} final节点 {}".format(s['parent_name'], s['name'], len(res))
		logger.info('### save_final_node # final node:' + s['parent_name'] + ' ' + s['name'] + str(len(res)))
		print "####" * 40
		for r in res:
			if r['final_node'] and not sheet_final.find({'url':r['url']}).count():
				sheet_final.insert(r)
			else:
				pass
	return True

# try:
# 	save_final_node()
# except Exception, e:
# 	msg = '### python run error: {}'.format(e)
	# logger.debug(msg)

save_final_node()
