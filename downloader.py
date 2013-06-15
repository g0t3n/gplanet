#!/usr/bin/env python
#-*- coding:utf-8 -*-

import urllib2
import urllib
import signal
import multiprocessing
import sys
import os
import random
import time
import socket
import PIL.Image
import StringIO
# my module
import config
import logger
__doc__ = '''
# exm:
# import downloader
# p = downloader.downloader()
# p.down(img_url, save_name, refer)
# when out:  p.killchild()		# useless
'''
class downloader:
	def __init__(self):
		if (config.config['download_log'] != ''):
			try:
				self.logit = open(config.config['download_log'], 'w+')
			except:
				print "warning! can't open config.config['download_log']"
		if (config.config['redown_path'] != '' ):
			try:
				self.redownlog = open(config.config['redown_path'], 'r')
			except:
				self.redownlog = None

		if not os.path.isdir(config.config['img_path']):
			try:
				os.mkdir(config.config['img_path'])
			except:
				print "warning! not img_path: "+str(config.config['img_path'])

		# 记住必须先创建 Queue
		self.mainqueue = multiprocessing.Queue()
		self.pid = os.fork()
		if self.pid == 0:								# child
			self.failqueue = multiprocessing.Queue()	# 图片下载失败后加入到这个队列，从新下载
			self.retry = 3							# 最多重复次数

			signal.signal(signal.SIGINT, self.cleanup)
			signal.signal(signal.SIGHUP, self.cleanup)
			signal.signal(signal.SIGTERM, self.cleanup)
			self.childloop(False)

		# father here:
		time.sleep(1)								# sleep for child to "init queue"


	def dolog(self, pic_name, url, refer):
		self.logit.write(urllib2.quote(pic_name)+' '+urllib2.quote(url)+' '+urllib2.quote(refer)+'\n')

	def down(self,img_url, save_name, refer=''):	# 用这个来获得下载队列
		self.mainqueue.put([img_url, save_name, refer])
		#return False

	def killchild(self):
		os.kill(self.pid, signal.SIGINT)
		pass
	def redown(self):

		if self.redownlog != None:
			print "[+] found redown.log, now try redown it"
			for line in self.redownlog:
				s = line.strip().split(' ')
				self.try_down(img_url, save_name, refer)
			self.redownlog.close()
			self.redownlog = open(config.config['redown_path'],'w')			# clean it
		
	# 死循环会耗费 cpu,适当加sleep能节约资源
	def childloop(self,isexit=False):
		sleeptime = 3
		while True:
			if not self.mainqueue.empty():
				img_url,  save_name, refer = self.mainqueue.get()
				if self.try_down(img_url, save_name, refer) == False:
					self.failqueue.put([img_url,  save_name, refer])	
			if self.failqueue.empty() != True:
				img_url, save_name, refer = self.failqueue.get()
				if self.try_down(img_url, save_name, refer) == False:
					if self.logit != None:
						self.dolog(save_name, img_url, refer)
					if self.redownlog != None:
						self.redownlog.write(urllib2.quote(img_url)+" "+urllib.quote(save_name)+' '+urllib.quote(refer)+'\n')						# markdown redown info 
			if os.getppid() == 1:				# 检查父进程是否为 init.
				isexit = True
			time.sleep(sleeptime)
			if self.mainqueue.empty() and self.failqueue.empty() and isexit:
				sys.exit()

	# try download mainqueue and failqueue,then exit child
	def cleanup(self,signum, frame):
		self.childloop(True)
	
	def try_down(self, img_url, save_name, refer='',proxy=''):
		save_path = config.config['img_path']
		UserAgent = config.UserAgent
		ua = UserAgent[int(random.uniform(0,int(len(UserAgent))))]
		myheader = { 'User-Agent' : ua,
					'Accept' : '*/*;'
				}
		socket.setdefaulttimeout(20)
		if refer != '':
			myheader['Referer'] = refer
		try:
			req = urllib2.Request(img_url, headers=myheader)
			response = urllib2.urlopen(req)
			# this may be error
			# timeout here?
			content =  response.read()
		except:
			#print traceback.format_exc()
			#print "error download img_url = "+str(img_url)
			return False
		pic_data = StringIO.StringIO(content)
		try:
			fd = PIL.Image.open(pic_data)
			if fd.mode != "RGB":
				fd = fd.convert("RGB")
			fd.save(str(save_path)+str(save_name))
		except:
			fd = open(str(save_path)+str(save_name),'wb')
			fd.write(content)
			fd.close()
		return True

## this is test code
if __name__ == '__main__':
	p = downloader()

	p.down('http://localhost:8080/','temp','http://localhost')
	p.down('http://localhost/2','temp1','http://localhost')
	p.down('http://localhost3/','temp3','http://localhost')
	p.down('http://localhost/4','temp4','http://localhost')
