#!/usr/bin/env python
#-*- coding:utf-8 -*-

import urllib
import time
from lxml import etree
import random
import urlparse
import sys
import hashlib
# my module
import db
import logger
import config
import spider
import downloader

# rewrite remote img_path from htmldata to local img_path && return the list of rename pic
# art_ori_content => originary html content
# ori_img_path => the list of pic path which need to replace in art_ori_content
# replace_img_path,re_path => 
# article_content,re_path = replace_img_path(art_ori_content, pic_list)		# 修改 html_content中的图片地址,返回修改后的html_content&图片名
global verbose 
verbose = 0

def replace_img_path(htmldata, ori_img_path):
	re_path = []
	re_content = htmldata
	for i in ori_img_path:
		name = time.strftime('%m%d%H%M%S',time.localtime(time.time())) + str(int(random.uniform(1000,9999))) + '.jpeg'
		re_content = re_content.replace(str(i), str(name))
		re_path.append(name)

	return re_content,re_path

# html_content	=> blog_article content
# art_link		=> article_link, in order to solve opposite path
# return a list contain absolute or opposite img path
def find_pic_addr(html_content):
	p = etree.HTML(html_content)
	retl = []
	sl = p.xpath(u'//img')

	for s in sl:		# 防止无 img 标签
		for i in range(len(s.keys())):					# 迭代s.key,直至找到 src 标签
			if s.keys()[i] == 'src':
				# to judge if it is absolute img path
				img_url = s.values()[i]					# 获得 <img xx src=''> 中的链接
				retl.append(img_url)
				break
	return retl

def main():
	# parse config
	configs = config.config
	logs = logger.logger(configs['log_path'])
	img_path = configs['img_path']
	sleep_time = configs['thread_sleep_time']
	rss_urls = configs['rss_url']
	hot_tag,plannels_manager,manager_mail = configs['hot_tag'],configs['admin_name'],configs['admin_mail']
	#connect to db
	sdb = db.db_con(configs['db_path'])
	download = downloader.downloader()		# p.down(img_url, save_name, refer)
	if config.config['redown_path'] != '':
		if verbose:
			print "trying to redown prev picture... ",
			download.redown()						# if we have some pic not down previou,now try it and remove redown.log
			print "done"
	# start craw =.=
	for rss_link in rss_urls:

		feedback = spider.spider_rss(rss_link)
		if feedback == False:
			continue
		header,datas = feedback

		lastest = sdb.sqlite_return_lastest(rss_link)
		if lastest == False:
			print "lastest is not int,check databases"
			continue
		max_lastest = lastest				# 计算最大的 gp_date 值,用于 updated
		for art_key in datas.keys():

			# 无author && newer
			art_tmp = datas[art_key]
			if (lastest == None) or (int(lastest) < int(art_tmp['article_date'])):
				if verbose == 1:
					print "\033[0;36m"+"inserting article \""+str(art_key)+"\"\033[0m"

				if art_tmp['article_date'] > max_lastest:
					max_lastest = art_tmp['article_date']
				article_content = sdb.toutf8(art_tmp['html_content'])[0]
				pic_list = find_pic_addr(article_content)	# img_path list 
				for i in range(len(pic_list)):
					pic_list[i] = sdb.toutf8(pic_list[i])[0]		# 为保证 image link 为utf-8

				if pic_list:			# html_content 中含有图片link
					article_content, re_path = replace_img_path(article_content, pic_list)		# 修改 html_content中的图片地址,返回修改后的html_content&图片名
					for img_url_n in range(len(pic_list)):		#判断是否相对路径,下载图片
						t_url = urlparse.urlparse(pic_list[img_url_n])
						if (not t_url.scheme) or (not t_url.hostname):	# None,str type is opposite path
							header = urlparse.urlparse(art_tmp['article_link'])
							img_url = header.scheme + '://' + header.hostname + header.path + art_tmp[img_url_n]
						else:
							img_url = pic_list[img_url_n]
						download.down(img_url,re_path[img_url_n],art_tmp['article_link']) #绝对路径,save_name,refer
						#is img absolute path or what
						#downloader.
					pic_list =  ''.join(x+'$' for x in re_path)
				else:
					pic_list = "none"
				article_content = urllib.quote(article_content)
				article_author  = urllib.quote(sdb.toutf8(art_tmp['article_author'])[0])
				article_link	= urllib.quote(sdb.toutf8(art_tmp['article_link'])[0])
				# update lastest !!!!!!

				sdb.insert_gp_post(article_content, art_key, article_author, hashlib.md5(article_content).hexdigest(),art_tmp['article_date'], pic_list, 'none',article_link)

				pass			# insert??
			else:
				# lastest ==			#执行全局查询,防漏
				print "article "+str(art_key)+"  << is up to date"
		if max_lastest > lastest:
			sdb.sqlite_insert_gp_lastest(article_author, max_lastest, rss_link)
	sdb.sqlite_insert_db_info(hot_tag, plannels_manager,manager_mail)

if __name__ == '__main__':
	print "gplanet version "+config.version
	print "bugger: \n"+config.bug
	print "for more verbose use -v"
	print "=*="*10
	for i in sys.argv:
		if i == '-v':
			print "[x] verbose mode"
			verbose = 1
	main()
