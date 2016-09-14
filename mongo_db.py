# -*- coding:utf-8 -*-
import pymongo

# 连接mongodb
def mongo_connect(table_name, sheet_name):
    client = pymongo.MongoClient('localhost', 27017)
    amazon = client[table_name]
    sheet_tab = amazon[sheet_name]
    return sheet_tab
