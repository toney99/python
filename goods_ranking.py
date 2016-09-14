# -*- coding:utf-8 -*-
import mongo_db
import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
import random

headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:34.0) Gecko/20100101 Firefox/34.0',
    'Cookie':'x-wl-uid=1i+sFIiUlv4DwDOUgOwSzI8PWuvTQ808T1gXnIPUCD35rNF63kWNqztLm2XT+LXKHUJ3xukNpE68jiPsHb7iwah3t+4E3CTT5qOibIhO7ui7EJw33TjHRxOuoYesj4FKRCj8pCaTu0bA=; session-id-time=2082787201l; session-id=187-4773038-6619813; ubid-main=186-3476072-7777706; session-token="aGq2cCBd/m1u84GaEh+wsSjtEOgcr1wibsTg1cNV0BbgZtmJ1FP0vg51Dp4zTF2wv7g17NLoNd5WaDpudT118xyfu18l4jOPWC8daBJildmzwAPfiUb43zDSyThptGuG3LR/YV219oQWfiTV7yI/pPLwuoBFn0lA3nCLwfG86DhVOmG82xUHe1dQUotfUEl+mpJt9jhb++tatFuer+ay9iCaKYnlRCFeGQTzpfbRZ9P2JhemDrRITu8tfFItZ9+WWmf5u4+GymkabChJgND30w=="; x-main="uLBaXiO1SiydNB2odX1tFgokySpmZfuxkZfVLLLUdv7eq?hvd9PIeZD7rvXisak7"; at-main="5|XA3UD0TCZXWBaQjUXXZMni/Oqp0tTxlipHMWFGOiwuLqcLII636P0AGu4986dhINgzvsX512PIy3fGYqLZLlWdsgFXEyNNXLNc743X7miIKtcyR4MKQjrHyDFX+yvL8MefKrZ1BrCutz/dYlOHNq2HqH//csOwC7XMh6elIrz3cIahAcSFAIRzwbpFw+pCRYecYQ4vsdwtPUw8fzr3cxlEy4Kw3BXW/1cCqFAkjVCCHG9kaJ/W3MpAjMRM+Q2Cs5SS2XA86QW10i+IMSM8ixQg=="; csm-hit=PVSRFAMYCQ11P59K0BJ1+s-PVSRFAMYCQ11P59K0BJ1|1472107830462',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept - Encoding': "gzip, deflate",
}

def get_ranking_list(name):
    sheet_tab = mongo_db.mongo_connect('amazon', 'goods_urls')
    num = 0
    coll = sheet_tab.find_one({'name':name})
    url = coll['url']
    name = coll['name']
    # print url
    ranking = []
    for i in range(1, 6, 1):
        # r_url = url + '#{}'.format(i)
        r_url = url + '?_encoding=UTF8&pg={}'.format(i)
        print r_url
        r = requests.get(r_url)
        soup = BeautifulSoup(r.text, 'lxml')
        for item in soup.select('div.zg_itemImmersion'):
            # print item
            num = num + 1
            vals = {}
            vals['rank'] = item.find('span').text[:-1]
            # vals['goods'] = item.find('a')['href'].strip()
            if item.find('a'):
                vals['goods'] = item.find('a')['href'].strip()
            else:
                vals['goods'] = 'None'
            # print vals
            print num, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), vals
            ranking.append(vals)
        time.sleep(3)
    return ranking
name = 'Unlocked Cell Phones'
while True:
    if int(datetime.now().strftime('%M'))%5 == 0:
        print datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ranking = get_ranking_list(name)
        # print datetime.now().strftime("%Y-%m-%d %H:%M:%S"), ranking
        time.sleep(60)
    else:
        pass
#     time.sleep(60)

