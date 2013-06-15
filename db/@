#!/usr/bin/env python
#-*- coding:utf-8 -*-
import sqlite3
import traceback

# use logger,
LOGGER = 0
LOGGERPATH = './DB.LOG'
try:
	import sys
	sys.path.append('../')
	import logger
	import config
	if config.config['log_path']:
		LOGGER = 1
except:
	print traceback.format_exc()

# article_date => 对方 post 的文章日期
# article_img_name => 本地日期+随机数
initdb_gp_post = '''
CREATE TABLE IF NOT EXISTS gp_post(
	article_id integer PRIMARY KEY,
	article_content text,
	article_title text not null,
	article_hash text unique,
	article_author text not null,
	article_date integer unique,
	article_img_name text ,
	article_tag text,
	article_ori_link text);
'''
# 只有一行，update hot_tag,gp_admin,gp_admin_mail
# total_article=文章总数

initdb_db_info = '''
create table if not exists db_info(
total_article int ,
total_author text,
hot_tag text,
gp_admin_name text,
gp_admin_mail text);
'''
# 每个作者最新的情况
# gp_author_rsslink => 
# go_update 为最新文章作者 post 的日期为准
initdb_gp_lastest = '''
create table if not exists gp_lastest(
	gp_author text not null,
	gp_update int not null,	
	gp_author_rsslink text not null
);
'''

# use 'con' to return cursor
# sqlite3 fetchall() return struct like this: [(select1,select2), (select1,select2)]
class db_con:
	def __init__(self, db_file):
		self.con = sqlite3.connect(db_file)
		cur = self.con.cursor()
		if sqlite3.threadsafety != 1:
			print "warning! your sqlite is not threadsafe"
		try:
			cur.execute(initdb_db_info)
			cur.execute(initdb_gp_post)
			cur.execute(initdb_gp_lastest)
		except Exception as E:
			print traceback.format_exc()
			print "db_init() error,exception: " + str(E)
			os.exit(1)
		if LOGGER:
			self.logit = logger.logger(config.config['log_path'])
		self.con.commit()
		cur.close()

	# in order to change any encoding to utf-8 
	@staticmethod
	def toutf8(ilist):
		olist =[]
		if type(ilist) != type([]):
			ilist = [ilist]
		for i in ilist:
			if type(i) == type(u''):
				olist.append(i.encode('utf-8'))
				continue
			try:
				olist.append(unicode(i,'utf-8').encode('utf-8'))	# utf-8
			except:
				olist.append(i.decode('gbk').encode('utf-8'))		# gbk
		return olist

	# 由于某些blog主会不定期改名，所以应以 gp_author_rsslink 来做判断
	def sqlite_insert_gp_lastest(self,gp_author, gp_update,  gp_author_rsslink):
		cur = self.con.cursor()
		gp_update = int(gp_update)
		# encoding argv
		slist = [gp_author, gp_author_rsslink]
		(gp_author, gp_author_rsslink) = db_con.toutf8(slist)

		try:
			# fb = cur.execute('select gp_author from gp_lastest;')   # feedback

			# if already exist gp_author, then  update again
			#if fb != []:
			# no mather if exist gp_author, we delete it
			cur.execute('delete from gp_lastest where gp_author_rsslink="'+str(gp_author_rsslink)+'"')
			cur.execute('insert into gp_lastest values("' + gp_author + '",' + str(gp_update) + ',"' +gp_author_rsslink+'")')
		except:
			print traceback.format_exc()
			print "insert sql stament: "+'insert into gp_lastest values("' + gp_author + '",' + str(gp_update) + ',"' +gp_author_rsslink+'")'
			self.logit.warning("error while execute "+"insert sql stament: "+'insert into gp_author("' + gp_author + '",' + str(gp_update) + ',"' +gp_author_rsslink+'")')
			self.con.rollback()		# rollback and unlock db
		finally:
			cur.close()
		self.con.commit()
	# return None means none this record
	# return 20060101246060
	def sqlite_return_lastest(self, gp_author_rsslink):
		cur = self.con.cursor()
		[gp_author_rsslink] = db_con.toutf8([gp_author_rsslink])
		# if gp_update which store in db is less then gp_update which in arguement,this means article is newer
		# if no gp_author fiel in gp_lasters,this means we need insert it later
		try:
			p = cur.execute('select gp_update from gp_lastest where gp_author_rsslink="'+str(gp_author_rsslink)+'";').fetchone()
			if p == None:
				return None
			updated = p[0]
			return int(updated)
		except:
			print traceback.format_exc()
			self.logit.warning('error while db function<sqlite_return_lastest>,traceback:'+str(traceback.format_exc()))
			return False
		#finally:
		#	return False


	def sqlite_insert_db_info(self, hot_tag='none', gp_admin_name='admin', gp_admin_mail='admin@gmail.com'):
		cur = self.con.cursor()
		slist = [hot_tag,gp_admin_name,gp_admin_mail]
		(hot_tag,gp_admin_name,gp_admin_mail) = db_con.toutf8(slist)
		print hot_tag,gp_admin_name,gp_admin_mail
		try:
			total_art = cur.execute('select count(article_title) from gp_post').fetchone()[0]
			tmp_author = cur.execute('select distinct article_author from gp_post').fetchall()
			total_author = ''
			for i in tmp_author:
				total_author += i[0].encode('utf-8') + ';'		# all author is encoding as unicode
			feedback = cur.execute('select count(*) from db_info;').fetchone()[0]

			if int(feedback) != 0:	# this means db_info == null, we use insert
				cur.execute('delete from db_info;')
			cur.execute('insert into db_info values (' + str(total_art)+', "'+total_author+'","' + str(hot_tag)+'","' + str(gp_admin_name) + '","' + str(gp_admin_mail) +'");')
			print 'insert into db_info values (' + str(total_art)+', "'+total_author+'","' + str(hot_tag)+'","' + str(gp_admin_name) + '","' + str(gp_admin_mail)   + '");'
			#else:
			#	cur.execute('UPDATE db_info SET total_article=' + str(total_art)+', total_author="'+total_author+'","' + str(hot_tag)+'"","'+str(gp_admin_name)+'","'+str(gp_admin_mail)+'");')
		except:
			print "sqlite_insert_db_info error,exception:"
			print traceback.format_exc()
			self.logit.warning("error function<sqlite_insert_db_info>: "+'insert into db_info values (' + str(total_art)+', "'+total_author+'","' + str(hot_tag)+'","' + str(gp_admin_name) + '","' + str(gp_admin_mail)   + '");'+'\n traceback: '+str(traceback.format_exc()))
			self.con.rollback()
		finally:
			cur.close()
		self.con.commit()

	def insert_gp_post(self, article_content, article_title,  article_author, article_hash='none',article_date=00000000, article_img_name='none', article_tag='none',gp_ori_link='none'):
		cur = self.con.cursor()
		# encoding argv	
		slist = [article_content, article_title, article_author,  article_img_name, article_tag, gp_ori_link]
		(article_content, article_title, article_author,  article_img_name, article_tag, gp_ori_link) = db_con.toutf8(slist)
		try:										# article_id
			cur.execute('insert into gp_post values(null'+ ',"' + article_content + '","' +article_title + '","' + article_hash + '","' + article_author + '",' + str(article_date) + ',"' + article_img_name + '","' + article_tag + '","'+gp_ori_link + '")')
		except:
			print "sql stament is: "+'insert into gp_post values(null ' +  ',"' + article_content + '","' +article_title + '","' + article_hash + '","' + article_author + '",' + str(article_date)+ ',"' + article_img_name + '","' + article_tag + '","'+gp_ori_link + '")'
			print traceback.format_exc()
			self.logit.warning('error function<insert_gp_post>: '+"sql stament is: "+'insert into gp_post values(null ' +  ',"' + article_content + '","' +article_title + '","' + article_hash + '","' + article_author + '",' + str(article_date)+ ',"' + article_img_name + '","' + article_tag + '","'+gp_ori_link + '")'+'\ntraceback:'+str(traceback.format_exc()))
			self.con.commit()
		finally:
			cur.close()
		self.con.commit()


if __name__ == '__main__':
	db = db_con('test.db')
	db.sqlite_insert_db_info()
	db.insert_gp_post('this is content','this is title','this is hash','g0t3n',20121212)
