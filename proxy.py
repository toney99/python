# -*-coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import time, random
import mongo_db

m_url = "http://www.kuaidaili.com/free/outha/{}/"


headers = {
	'Accept':'image/webp,image/*,*/*;q=0.8',
	'Accept-Encoding':'gzip, deflate, sdch, br',
	'Accept-Language':'zh-CN,zh;q=0.8',
	'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36',
}
def get_proxy_id(m_url):
    try:
        r = requests.get(m_url, headers=headers)
        soup = BeautifulSoup(r.text, 'lxml')
    except:
        return
    sheet_tab = mongo_db.mongo_connect('amazon', 'proxy_ip')
    res = soup.select('tbody > tr')
    for i in res:
        ip = i.td.text
        port = i.find_all('td')[1].text
        ip_port = ip + ':' + port
        # print ip_port
        vals = {
            'ip': ip_port,
            'used': False,
        }
        if not sheet_tab.find({'ip':ip_port}).count():
            sheet_tab.insert_one(vals)
	    print ip_port
	else:
	    print ip_port + ' is exist...'
    return True

for n in range(1, 1000, 1):
    m_url = m_url.format(n)
    get_proxy_id(m_url)
    delay = random.random() * 10
    # print delay
    time.sleep(delay)
