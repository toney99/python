# -*- coding:utf-8 -*-
import logging, os
import time
 
class Logger:
	def __init__(self, path, clevel = logging.DEBUG, Flevel = logging.DEBUG):
		self.logger = logging.getLogger(path)
		self.logger.setLevel(logging.DEBUG)
		fmt = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')
		#设置CMD日志
		sh = logging.StreamHandler()
		sh.setFormatter(fmt)
		sh.setLevel(clevel)
		#设置文件日志
		fh = logging.FileHandler(path)
		fh.setFormatter(fmt)
		fh.setLevel(Flevel)
		self.logger.addHandler(sh)
		self.logger.addHandler(fh)
 
	def debug(self,message):
		self.logger.debug(message)
 
	def info(self,message):
		self.logger.info(message)
 
	def war(self,message):
		self.logger.warn(message)
 
	def error(self,message):
		self.logger.error(message)
 
	def cri(self,message):
		self.logger.critical(message)

# put_log = Logger('/var/amazon/amazon_log.log',logging.ERROR,logging.DEBUG)

# if __name__ =='__main__':
# 	put_log = Logger('/var/amazon/amazon_log.log',logging.ERROR,logging.DEBUG)
# 	put_log.debug('一个debug信息')
# 	put_log.info('一个info信息')
# 	put_log.war('一个warning信息')
# 	put_log.error('一个error信息')
# 	put_log.cri('一个致命critical信息')

