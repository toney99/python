# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import json
import re
import get_product,save_asin, mongo_db

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
page_base = "https://www.amazon.com/s/ref=sr_pg_{}/{}?srs={}&rh={}&page={}&ie=UTF8&qid={}"

# 获取每页商品的地址、title
def get_product_list(url):
	r = requests.get(url, headers=headers)
	soup = BeautifulSoup(r.text, 'lxml')
	one_page_urls =[]
	product = soup.select('a.a-link-normal.s-access-detail-page.a-text-normal')
	for p in product:
		url = p['href']     # 商品的url地址
		title = p['title']  # 商品的title
		print 'one_of_list_product:',url, title
		save_asin.save_asin_by_url(url)
		one_page_urls.append(url)
	return True

# 根据菜单的url获取改菜单总的页数
def get_page_num(tre_url):
	r = requests.get(tre_url, headers=headers)
	soup = BeautifulSoup(r.text, 'lxml')
	page_num = soup.select('span.pagnDisabled')  # 获取总的页数
	if not page_num: # 如果没有总的页数，取最后一页的数
		page_num = soup.select('span.pagnLink > a')
		page_num = page_num and page_num[-1].text or 1
	else:
		page_num = page_num and page_num[0].text or 1
	page = soup.select('span.pagnLink > a')
	page_url_node = page and page[-1]['href']  # 取其中一页的url，解析其中的srs、rh、qid、ran_num的值
	print 'page_url_node', page_url_node  
	if not page_url_node:
		print '######page node Not Found#####',page
		return 
	split_eq = page_url_node.split('=')
	srs = split_eq[2].split('&')[0]
	rh = split_eq[3].split('&')[0]	
	qid = split_eq[-1]
	ran_num = split_eq[1].split('/')[1].split('?')[0]

	print 'page_num', page_num
	for num in range(1, int(page_num), 1):
		page_url = page_base.format(int(num), ran_num, srs, rh, int(num),qid)
		print 'page_url_new', page_url
		get_product_list(page_url)
		print '-=-=' * 40
	print '====' * 40
	return True

# 根据二级菜单获取三级菜单的地址
def get_tre_menu(ch_url):
	r = requests.get(ch_url, headers=headers)
	soup = BeautifulSoup(r.text, 'lxml')
	# res = soup.select('div.categoryRefinementsSection > ul > li > a')
	# res = soup.select('ul.forExpando > li > a')
	node_children = soup.select('ul.refinementNodeChildren > li > a')
	for r in node_children:
		url =  r['href']
		name = r.find('span').text
		print 'node_children', url, name
		get_page_num(base+url)
	return True

# sheet_tab = mongo_db.mongo_connect('amazon', 'main_menu_url')
# res = sheet_tab.find({'parent_name':'Home, Garden & Tools'})
# for r in res:
# 	print r['url']
# 	get_tre_menu(r['url'])
# 	print '====' * 40
# 	print '****' * 40
# 	print '====' * 40

# tre_url = base + get_tre_menu(ch_url)
# url =base + get_page_num(tre_url)


# n = 0
# for i in get_product_list(url):
# 	print n, i
# 	get_product.get_product_rank(i)
# 	n = n + 1




# div.a-row.a-spacing-small > a