#!/usr/bin/env python
#-*- coding:utf-8 -*-

import logging
__doc__ = '''
# external usage: 
# import logger
# mylog = logger('/var/log/gplanets.log',"/var/log/gplanets.log")
# mylog.warning('info: xxx')
'''
class logger():
	def __init__(self,warningfile = '',infofile = ''):
		self.formatter = logging.Formatter('[%(asctime)s] %(message)s','%Y-%m-%d %H:%M:%S')
		self.wlogger = logging.getLogger('WARNING LOGGER')
		self.ilogger = logging.getLogger('INFO_LOGGER')
		if warningfile != '':
			self.warn_fd = logging.FileHandler(warningfile,encoding='utf-8',mode='a')	# mode=a才是插入!
			self.warn_fd.setFormatter(self.formatter)
			self.wlogger.addHandler(self.warn_fd)
		if infofile != '':
			self.info_fd = logging.FileHandler(infofile,encoding='utf-8',mode='a')
			self.info_fd.setFormatter(self.formatter)
			self.ilogger.addHandler(self.info_fd)
	def tounicode(self,msg):
		if type(msg) == type(u''):
			return msg
		try:
			return msg.decode('utf-8')
		except:
			return msg.decode('gbk')

	def info(self,msg):
		msg = self.tounicode(msg)
		self.ilogger.error(msg)
		self.info_fd.flush()
	def warning(self,msg):
		msg = self.tounicode(msg)
		self.wlogger.error(msg)
		self.warn_fd.flush()
	def close(self):
		try:
			self.wlogger.close()
			self.ilogger.close()
		except:
			pass
			

if __name__ == '__main__':
	warning_file = 'WARNING.log'
	info_file = 'INFO.log'
	ins = logger(warning_file,info_file)
	ins.warning('this is a warning log')
	ins.info('this is a info log')
