#!/usr/bin/env python
#-*- coding:utf-8 -*-
import sqlite3
import random
import thread

con = sqlite3.connect('testdb.db')
cu = con.cursor()
print cu.execute('create table if not exists test(id integer primary key,content text)')
i ='insert into test values(NULL,\'' + '1'*2000 +'\')'
print i
print type(i)
for i in range(200):
	cu.execute(str(i))
con.commit()
cu.close()
con.close()
