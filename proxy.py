# -*-coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import time, random
import mongo_db

m_url = "http://www.kuaidaili.com/free/outha/{}/"

# <tr class="">
# <td class="country"><img alt="In" src="http://fs.xicidaili.com/images/flag/in.png"/></td>
# <td>123.201.99.211</td>
# <td>8080</td>
# <td>
#         印度
#       </td>
# <td class="country">高匿</td>
# <td>HTTP</td>
# <td class="country">
# <div class="bar" title="4.968秒">
# <div class="bar_inner medium" style="width:84%">
# </div>
# </div>
# </td>
# <td class="country">
# <div class="bar" title="0.993秒">
# <div class="bar_inner fast" style="width:99%">
# </div>
# </div>
# </td>
# <td>1小时</td>
# <td>16-09-14 21:39</td>
# </tr>


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
    # print r.text
    for i in res:
        ip = i.td.text
        port = i.find_all('td')[1].text
        print ip + ':' + port
        vals = {
            'ip': ip + ':' + port,
            'used': False,
        }
        sheet_tab.insert_one(vals)
    return True

for n in range(1, 200, 1):
    m_url = m_url.format(n)
    get_proxy_id(m_url)
    delay = random.random() * 10
    # print delay
    time.sleep(delay)