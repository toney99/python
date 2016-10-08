# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import json
import re
import mongo_db
from datetime import datetime
import time

url = "https://www.amazon.com/dp/"
headers = {
	'Accept':'image/webp,image/*,*/*;q=0.8',
	'Accept-Encoding':'gzip, deflate, sdch, br',
	'Accept-Language':'zh-CN,zh;q=0.8',
	'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.38 (KHTML, like Gecko) Chrome/52.0.2004.84 Safari/537.38',
}

# 根据商品的url地址获取排名、review
# url = 'https://www.amazon.com/MOOV-NOW-Fitness-Tracker-Workout/dp/B01CX26IEO/ref=sr_1_25/161-1087189-6435406?s=home-automation&srs=6563140011&ie=UTF8&qid=1473487034&sr=1-25'
def get_product_rank(asin, ip, num):
	url = "https://www.amazon.com/dp/" + asin
	print 'start time:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	proxies = {}
	proxies['http'] = ip
	try:
		# r = requests.get(url, headers=headers, proxies=proxies, timeout=10)
		r = requests.get(url, headers=headers, timeout=10)
		soup = BeautifulSoup(r.text, 'lxml')
	except:
		print "##### REQUEST URL ERROR", url, ip
		return False
	check_res = soup.select('div.a-box-inner > h4')
	if check_res:
		print "##### NEED VERIFICATION CODE: ", check_res, ip
		return False
	param = soup.select('table##productDetails_detailBullets_sections1 > tbody > tr > td > span > span')
	review = soup.select('span#acrCustomerReviewText')
	# params = soup.select('table#productDetails_detailBullets_sections1')
	# print len(params), params
	print num, datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	rank_list = []
	for p in param:
		rank_list.append(p.text)
		print asin, p.text
	vals = {
		'asin':asin,
		'rank':rank_list,
		'review': review and review[0].text.split(' ')[0] or 0,
	}
	print '*****ranking: ',vals
	print 'end time:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	print '=--=' * 40
	return True

# 从数据库抓取N条记录
def get_asin_from_db(limit=1000):
	sheet_tab = mongo_db.mongo_connect('amazon', 'product_asin')
	res = sheet_tab.find({'used':False}).limit(limit)
	vals = []
	for r in res:
		vals.append(r)
	return vals

def update_asin_to_true(fields):
	sheet_tab = mongo_db.mongo_connect('amazon', 'product_asin')
	sheet_tab.update({"_id":fields["_id"]}, {"used":False})
	return True

# 取代理IP
def get_proxy_ip():
	sheet_tab = mongo_db.mongo_connect('amazon', 'proxy_ip')
	res = sheet_tab.find({"used":False}).limit(1)
	if res:
		for r in res:
			print '**** ip: ', r['ip']
			sheet_tab.update({"_id":r["_id"]}, {"used":True})
			return r['ip']
	else:
		print "#### GET PROXY IP ERROR"
		return False
	return 

# 抓取排名
def get_ranking():
	num = 1
	while True:
		fields = get_asin_from_db()
		if not fields:
			return True
		# 取代理IP
		ip = get_proxy_ip()
		for f in fields:
			res = get_product_rank(f['asin'], ip, num)
			if not res:
				# 重新获取代理IP
				ip = get_proxy_ip()
			else:
				# 标记记录的used为True
				update_asin_to_true(f)
			time.sleep(3)

get_ranking()
