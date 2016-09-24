# -*- coding:utf-8 -*-
import mongo_db

def save_asin(asin):
	sheet_tab = mongo_db.mongo_connect('amazon', 'product_asin')
	if not sheet_tab.find({'asin':asin}).count():
		vals = {
			'asin':asin,
			'used':False,
			'count':0,
		}
		sheet_tab.insert(vals)

	return True

def save_asin_by_url(url):
	s = url.split('/')
	if len(s) > 5:
		asin = s[5]
		save_asin(asin)
	else:
		pass
		print "######SAVE_ASIN_BY_URL_ERROR:", url

	return True