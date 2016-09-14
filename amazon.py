# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import time
import pymongo

# Best ellers主页面
# url = 'https://www.amazon.com/Best-Sellers/zgbs/'
# url2 = 'https://www.amazon.com/gp/bestsellers'
URL_LIST = [{
    'url' : 'https://www.amazon.com/gp/bestsellers/',
    'name' : 'root',
    'parents' : 0,
    'level' : 0,
    'isused' : False,
}]

# 连接mongodb
def connect_mongo(table_name, sheet_name):
    client = pymongo.MongoClient('localhost', 27017)
    amazon = client[table_name]
    sheet_tab = amazon[sheet_name]
    return sheet_tab

def get_deep_child_item(url_list=[], deep=5):
    sheet_tab = connect_mongo('amazon', 'goods_urls')
    if sheet_tab.find().count() == 0:
        for v in URL_LIST:
            sheet_tab.insert_one(v)
    count = 0
    for i in range(0, deep, 1):
        # print i
        selector = "ul#zg_browseRoot  > {}li > a".format('ul > ' * (i + 1))
        print selector
        for p in sheet_tab.find({'level':i}):
            print p['level'],p['name'], p['isused'], i
            if p['level'] == i and not p['isused']:
                r = requests.get(p['url'])
                soup = BeautifulSoup(r.text, 'lxml')
                for u in soup.select(selector):
                    vals = {
                        'url' : u['href'],
                        'name' : u.text.encode('utf-8'),
                        'parents' : p['name'],
                        'level' : i+1,
                        'isused' : False,
                    }
                    print count, vals
                    count = count + 1
                    if not sheet_tab.find_one({'url':u['href']}):
                        sheet_tab.insert_one(vals)
                    else:
                        print 'url is exsit!'
                sheet_tab.update({'_id':p['_id']}, {'$set':{'isused':True}})

    return True



# 获取主页面下分类信息的item, url
def get_item_url(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    for i in soup.select('ul#zg_browseRoot  > ul > li > a'):
        item_url = i['href']
        item_name = i.text.encode('utf-8')
        print item_url, type(item_url)
        print item_name, type(item_name)
    return True

def get_child_item_url(url):
    item_url = 'https://www.amazon.cn/gp/bestsellers/wireless'

    # item_url = 'https://www.amazon.com/Best-Sellers-Clothing/zgbs/apparel'
    # item_url = 'https://www.amazon.com/Best-Sellers-Clothing-Men/zgbs/apparel/1040658'
    # item_url = 'https://www.amazon.com/Best-Sellers-Clothing-Men-Dresses/zgbs/apparel/1040658'
    r = requests.get(item_url)
    soup = BeautifulSoup(r.text, 'lxml')
    for i in soup.select('ul#zg_browseRoot > ul >  ul > li > a'):
        item_url = i['href']
        item_name = i.text.encode('utf-8')
        print item_url, item_name

# 获取排名
def get_ranking(url):
    r = requests.get(item_url)
    soup = BeautifulSoup(r.text, 'lxml')
    for item in soup.select('div.zg_itemImmersion > div > div.zg_title > a'):
        print item['href'].strip(), item.text.encode('utf-8')

# get_item_url(url)
# get_child_item_url(url)
# get_deep_child_item_url(item_url)
get_deep_child_item(URL_LIST)