#!/usr/bin/env python
#coding=utf-8
import MySQLdb as mysql

class DB():
    def __init__(self,db,host,user,passwd):
        self.db = db
        self.host = host
        self.user = user
        self.passwd = passwd
        self.connect()
    def connect(self):
        self.con = mysql.connect(db=self.db,host=self.host,user=self.user,passwd=self.passwd,charset='utf8')
        self.cursor = self.con.cursor()
        self.con.autocommit(True)
    def execute(self,sql):
#        print sql
        try:
            self.cursor.execute(sql)
        except Exception,e:
#            print e
            try:
                self.con.close()
                self.cursor.close()
            except:
                pass
            self.connect()
            self.cursor.execute(sql)
        res =self.cursor.fetchall()
#        print res
        return res

