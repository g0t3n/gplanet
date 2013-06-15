#!/usr/bin/env python
#-*- coding:utf-8 -*-

# all configure are define here, leave black to disable 
config = {  'img_path' : './datas/images/',
			'log_path' : './datas/logger.log',		# db-loger
			'spider_log':'./datas/spider.log',
			'download_log':'./datas/down_error.log',
			'redown_path' : './datas/redown.log',
			'thread_num' : 0,
			'thread_sleep_time' : 0,
			'download_sleep_time':0,
			# db_path ,point to the db file, exm: /var/db/article.db
			'db_path' : './datas/article.db',
			# rss_url, remember add http://
			'rss_url':[	'http://xiaoxia.org/feed/',
					'http://blog.csdn.net/cnbird2008/rss/list',
					'http://blog.csdn.net/dog250/rss/list',
					'http://eindbazen.net/feed/',			# a web with many ctf writeup
					'http://leetmore.ctf.su/feed/',			# ctf too
					'http://blog.squareroots.de/en/feed/',
					'http://coolshell.cn/feed',
					'http://basiccoder.com/feed',
					'https://www.sunchangming.com/blog/?feed=rss',
					'http://blog.w4kfu.com/?feed=atom',
					'http://www.blue-lotus.net/feed/',
					'http://blog.codingnow.com/atom.xml',
					'http://shell-storm.org/rss.xml'
						],
			'hot_tag':'linux;geek;hack;test',
			'admin_name':'g0t3n',
			'admin_mail':'vinxiaohua@gmail.com'
		}

UserAgent = [ 'Mozilla/5.0 (Windows NT 6.1; rv:9.0) Gecko/20100101 Firefox/9.0',
				'Mozilla/5.0 AppleWebKit/537.11  Chrome/23.0.1271.97 Safari/537.11',
				'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0)',
				'Mozilla/5.0  AppleWebKit/420.1 (KHTML, like Gecko) Version/3.0 Mobile/4A93 Safari/419.3']
version = "0.1 beta"
bug = "0. downloader not consummate\n"
