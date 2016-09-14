# -*- coding:utf-8 -*-
import mongo_db
import re

def save_asin(asin):
	sheet_tab = mongo_db.mongo_connect('amazon', 'product_asin')
	res = sheet_tab.find({'asin': asin}).count()
	if not res:
		sheet_tab.insert_one({'asin':asin})
	return True
# save_asin('B00IWHDAKA')
url = "https://www.amazon.com/KETCL-OT2301-CHR-Buckshot-Waterproof-Super-Portable/dp/B01HC2FZLM/ref=sr_1_72/162-7486134-3314738?s=home-automation&srs=6563140011&ie=UTF8&qid=1473496109&sr=1-72"
def save_asin_by_url(url):
	if url.split('/') > 5:
		asin = url.split('/')[5]
		save_asin(asin)
	else:
		print '######save asin error######', url
	return True
# save_asin_by_url(url)

