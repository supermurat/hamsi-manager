# -*- coding: utf-8 -*-

import Variables
import Universals
from Databases import sqlite, correctForSql, getDefaultConnection

class BookmarksOfDirectories:
    global fetchAll, fetch, insert, update, delete
        
    def fetchAll():
        con = getDefaultConnection()
        cur = con.cursor()
        cur.execute("SELECT * FROM bookmarksOfDirectories")
        return cur.fetchall()
    
    def fetch(_id):
        con = getDefaultConnection()
        cur = con.cursor()
        cur.execute("SELECT * FROM bookmarksOfDirectories where id=" + str(int(_id)))
        return cur.fetchall()
    
    def insert(_bookmark, _value, _type=""):
        con = getDefaultConnection()
        cur = con.cursor()
        cur.execute("insert into bookmarksOfDirectories(bookmark,value,type) values('" + correctForSql(_bookmark) + "','" + correctForSql(_value) + "','" + correctForSql(_type) + "')")
        con.commit()
        cur.execute("SELECT last_insert_rowid();")
        return cur.fetchall()[0][0]
    
    def update(_id, _bookmark, _value, _type=""):
        con = getDefaultConnection()
        cur = con.cursor()
        cur.execute(str("update bookmarksOfDirectories set bookmark='" + correctForSql(_bookmark) + "', value='" + correctForSql(_value) + "', type='" + correctForSql(_type) + "' where id=" + str(int(_id))))
        con.commit()
    
    def delete(_id):
        con = getDefaultConnection()
        cur = con.cursor()
        cur.execute("delete from bookmarksOfDirectories where id="+str(int(_id)))
        con.commit()
        
    
