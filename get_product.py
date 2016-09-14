# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import json
import re
import mongo_db
from datetime import datetime

url = "https://www.amazon.com/dp/"
ASIN = ['B012CKVZ18', 'B00LBFFSNM','B00073HJG8','B002YQR2Y0']
headers = {
	'Accept':'image/webp,image/*,*/*;q=0.8',
	'Accept-Encoding':'gzip, deflate, sdch, br',
	'Accept-Language':'zh-CN,zh;q=0.8',
	'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36',
}

# 根据商品的url地址获取排名、review
url = 'https://www.amazon.com/MOOV-NOW-Fitness-Tracker-Workout/dp/B01CX26IEO/ref=sr_1_25/161-1087189-6435406?s=home-automation&srs=6563140011&ie=UTF8&qid=1473487034&sr=1-25'
def get_product_rank(asin, num):
	url = "https://www.amazon.com/dp/" + asin
	print 'start time:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	r = requests.get(url, headers=headers)
	soup = BeautifulSoup(r.text, 'lxml')
	param = soup.select('table#productDetails_detailBullets_sections1 > tr > td > span > span')
	# param = soup.select('table#productDetails_detailBullets_sections1')
	# param = soup.select('div#productDetails_db_sections')
	review = soup.select('span#acrCustomerReviewText')
	# print len(param), param
	print num, datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	for p in param:
		print asin, p.text
	print 'asin',asin ,'review',review and review[0].text.split(' ')[0] or 0
	print 'end time:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	print '=--=' * 40
	# span = param and param[-1].find('span').find('span')
	# print span
	# s = span.prettify()
	# rank = s.split('#')[1].split(' ')[0]
	# print int(rank.split(',')[0] + rank.split(',')[1])
# get_product_rank(url)
sheet_tab = mongo_db.mongo_connect('amazon', 'product_asin')
num = 1
asin_list = []
for i in sheet_tab.find():
	print num, i['asin']
	asin_list.append(i['asin'])
	# num = num + 1
	# if i and i.get('asin', False):
for asin in asin_list:
	get_product_rank(asin, num)
	num = num + 1
