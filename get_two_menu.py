# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import json
import re
import save_asin 
import mongo_db

url = "https://www.amazon.com/gp/site-directory/"
# ch_url = "https://www.amazon.com/home-automation-smarthome/b/ref=sd_allcat_homaut?ie=UTF8&node=6563140011"
ch_url = "https://www.amazon.com/Kitchen-and-Bath-Fixtures/b/ref=sd_allcat_kbf?ie=UTF8&node=3754161"
base = "https://www.amazon.com"
rank_url = "https://www.amazon.com/s/srs=6563140011&page=1&ie=UTF8"

product_url = "https://www.amazon.com/s/ref=sr_pg_2?srs=6563140011&rh=n%3A2335752011&page=2&ie=UTF8&qid=1473382114"

headers = {
	'Accept':'image/webp,image/*,*/*;q=0.8',
	'Accept-Encoding':'gzip, deflate, sdch, br',
	'Accept-Language':'zh-CN,zh;q=0.8',
	'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36',
}

# 获取指定二级菜单下面所有的菜单地址

# sheet_tab = mongo_db.mongo_connect('amazon', 'main_menu_url')
# res = sheet_tab.find({'url':'https://www.amazon.com/home-automation-smarthome/b/ref=sd_allcat_homaut?ie=UTF8&node=6563140011'})
# print res
node = '/s/ref=lp_6563140011_nr_scat_2407755011_ln/159-1954806-9758418?srs=6563140011&rh=n%3A2407755011&ie=UTF8&qid=1473493363&scn=2407755011&h=273bcaf49054ff8b282158c9d4b8c786907bd6d9'
page_base = "https://www.amazon.com/s/ref=sr_pg_{}/?{}&page={}&ie=UTF8"

# 获取每页商品的地址、title
def get_product_list(url):
	try:
		r = requests.get(url, headers=headers)
		soup = BeautifulSoup(r.text, 'lxml')
	except:
		print "#######get error:", url
		return False
	# one_page_urls =[]
	product = soup.select('a.a-link-normal.s-access-detail-page.a-text-normal')
	print "****page_product_list:", len(product)
	for p in product:
		url = p['href']     # 商品的url地址
		title = p['title']  # 商品的title
		# print 'one_of_list_product:',url, title
		save_asin.save_asin_by_url(url)
		# one_page_urls.append(url)
	return True

# 根据final url获取改菜单总的页数
def get_page_num(final_url):
	try:
		r = requests.get(final_url, headers=headers)
		soup = BeautifulSoup(r.text, 'lxml')
	except:
		print '######## GET PAGE NUM ERROR:', final_url
		return False
	page_num = soup.select('span.pagnDisabled')  # 获取总的页数

	page = []
	# 获取总的页数，如果没有总的页数，取最后一页的数
	if not page_num: 
		page_num = soup.select('span.pagnLink > a')
		page_num = page_num and page_num[-1].text or 1
	else:
		page_num = page_num and page_num[0].text or 1
	page = soup.select('span.pagnLink > a')
	page_url_node = page and page[-1]['href']  # 取其中一页的url，解析其中的srs、rh、qid、ran_num的值
	print '****one_page_url_node', page_url_node  
	if not page_url_node:
		print '######page node Not Found#####',page
		return False
	# page_url_node 
	# /s/ref=lp_7242007011_pg_3/166-1338711-6776612?rh=n%3A172282%2Cn%3A%21493964%2Cn%3A502394%2Cn%3A172435%2Cn%3A7242007011&page=3&ie=UTF8&qid=1474521868
	# /s/ref=lp_165993011_pg_3?rh=n%3A165793011%2Cn%3A%21165795011%2Cn%3A165993011&page=3&ie=UTF8&qid=1474522127&spIA=B01HV562AI,B01HKU0TBC,B01FZTWY5Y
	# 取出url中的rh用来拼接新的地址
	split_eq = page_url_node.split('?')
	rh = split_eq[-1].split('&')[0]	
	# srs = split_eq[2].split('&')[0]
	# qid = split_eq[-1]
	# ran_num = split_eq[1].split('/')[1].split('?')[0]

	print '****page_all_num:', page_num
	for num in range(1, int(page_num), 1):
		page_url = page_base.format(int(num), rh, int(num))
		page.append(page_url)
		get_product_list(page_url)
		print '----page_url_with_num:', page_url
		print '++++' * 40
	print '====' * 40
	return page

def save_page_from_final_node():
	sheet_final = mongo_db.mongo_connect('amazon', 'final_url')
	for s in sheet_final.find():
		get_page_num(s['url'])

	return True

save_page_from_final_node()