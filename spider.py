#!/usr/bin/env python
#-*- coding:utf-8 -*-

import feedparser
import datetime
import time
# my module
import config
try:
	import logger
	print 'spider: logger load'
except:
		pass

def toutf8(datas):
	if type(datas) == type(u''):
		return datas.encode('utf-8')
	try:
		p = datas.decode('utf-8').encode('utf-8')
		return p
	except:
		return datas.decode('gbk').encode('utf8')
# @xml_data : xml_data to process
# return False
# return [ (rsstitle,rssdescription,blog_link),											# a tuple descript rss info
#		{'html_title1':{'html_content':"xxx",'article_date':"xxx",'article_author':"xxx",'article_link':"xxx"}, \ # a dict descript the data
#			'html_title2':{'html_content','article_date','article_author','article_link'}}]

def spider_rss(rss_url, log_file = ""):
	if log_file != "":
		logit = logger.logger(log_file)
		logit.warning("spider start " +" rss addr: "+rss_url)
	if config.config['spider_log'] != '':
		logit = logger.logger(config.config['spider_log'])
		logit.warning("spider start " +" rss addr: "+rss_url)
	# title & description like this
	# /rss/channel/title /rss/channel/description
	rsstitle = ""
	rssdescription = ""
	result = {}
	d = feedparser.parse(rss_url)

	if not d.feed.has_key('title'):
		d = feedparser.parse(rss_url)		# try another time
	if d.feed.has_key('title'):
		rsstitle = toutf8(d.feed.title)
	if d.feed.has_key('subtitle'):
		rssdescription = toutf8(d.feed.subtitle)
	if d.feed.has_key('link'):
		blog_link = toutf8(d.feed.link)
	#lastbuild = d.feed.updated_parsed		# x.feed.updated_parsed

	if len(d.entries) == 0:
		if log_file != "":
			logit.warning("spider found error at rss address "+rss_url+" or feedparse can't produce it. now exit.")
		return False

	for i in d.entries:
		art_title = art_link = art_updated = art_summary = art_author = "none"
		art_link  = "none"
		if i.has_key('title'):
			art_title = i.title
		if i.has_key('link'):
			art_link = i.link
		#if i.has_key('updated'):
		#	art_updated = i.updated
		if i.has_key('summary'):
			art_summary = i.summary
		if i.has_key('updated_parsed'):
			t = i.updated_parsed		# art_date
			# format: 199101022412, str
			art_updated = '%d%.2d%.2d%.2d%.2d%.2d' % (t.tm_year,t.tm_mon,t.tm_mday,t.tm_hour,t.tm_min,t.tm_sec)
		#########################################
		# this is a really poor code,cause the mother fucker csdn rss is not standard,  i.updated_parsed is broken
		# you really should delete it
		# csdn type: In [28]: csdn.entries[0].updated
		#			 Out[28]: u'2013-1-3 12:39:15'
		# wordpress like standard:  In [27]: wp.entries[0].updated
		#			Out[27]: u'Tue, 18 Dec 2012 06:23:37 +0000'
		# feedparser make some wrong in csdn like none stardand,[hour,minute,second]will be zero 
		if i.has_key('updated') and int(art_updated[-6:]) == 0:
			try:					#	=> is csdn type?
				tmp_date = toutf8(i.updated)
				int(tmp_date[0:3])
				if ((tmp_date.find('-')!=-1) and (tmp_date.find(' ')!=-1) and (tmp_date.find(':')!=-1)):
				# 20130201000000
					import datetime
					p = datetime.datetime.strptime(tmp_date,'%Y-%m-%d %H:%M:%S')
					tmp_date = '%d%.2d%.2d%.2d%.2d%.2d' % (p.year,p.month,p.day,p.hour,p.minute,p.second)
					art_updated = tmp_date
				#print "debug: art_updated_parsed=>"+str(art_updated_parsed)
			except:
				#print "exception"
				pass
		################################################
		if i.has_key('content'):					# 参考 planet 代码,发现 content 标签需要用 for 改写以下代码
			#print "i content is len(i.content):"+str(len(i.content))+" len(summary) is :"+str(len(art_summary))
			#print i.content
			tmp_content = i.content
			if type(tmp_content) == type([]):
				tmp_values = ''
				for k in tmp_content:
					tmp_values += k.value
			if len(toutf8(tmp_values))> len(toutf8(art_summary)):
				art_summary = tmp_values
		if i.has_key('author'):
			art_author = i.author
	#	result[toutf8(art_title)] = {"html_content":toutf8(art_summary),"article_date":toutf8(art_updated_parsed),"article_author":toutf8(art_author),"article_link":toutf8(art_link)}
		result[toutf8(art_title)] = {"html_content":toutf8(art_summary),"article_date":art_updated,"article_author":toutf8(art_author),"article_link":toutf8(art_link)}
	if log_file != "":
		logit.warning("spider success craw " + rss_url+" now exit")
	return (rsstitle,rssdescription,blog_link),result

# for test
if __name__ == '__main__':
	s = [u'慢慢de，编码问题我想死了',u'慢慢de，编码问题我想死了'.encode('utf-8'),u'慢慢de，编码问题我想死了'.encode('gbk')]
	for i in s:
		print toutf8(i)
	test_urls = [ 'http://xiaoxia.org/feed/', 'http://xi4oyu.blogbus.com/index.rdf' ,'http://blog.csdn.net/cnbird2008/rss/list' ]
#	process_config()
	for i in test_urls:
		spider_rss(i)
