# -*- coding: utf-8 -*-

import Variables
import Universals
from Databases import sqlite, correctForSql, getDefaultConnection

class SearchAndReplaceTable:
    global fetchAll, fetch, insert, update, delete
        
    def fetchAll():
        con = getDefaultConnection()
        cur = con.cursor()
        cur.execute("SELECT * FROM searchAndReplaceTable")
        return cur.fetchall()
    
    def fetch(_id):
        con = getDefaultConnection()
        cur = con.cursor()
        cur.execute("SELECT * FROM searchAndReplaceTable where id=" + str(int(_id)))
        return cur.fetchall()
    
    def insert(_searching, _replacing, _intIsActive, _intIsCaseSensitive, _intIsRegExp):
        con = getDefaultConnection()
        cur = con.cursor()
        cur.execute("insert into searchAndReplaceTable(searching, replacing, intIsActive, intIsCaseSensitive, intIsRegExp) values('" + correctForSql(_searching) + "','" + correctForSql(_replacing) + "','" + correctForSql(_intIsActive) + "','" + correctForSql(_intIsCaseSensitive) + "','" + correctForSql(_intIsRegExp) + "')")
        con.commit()
        cur.execute("SELECT last_insert_rowid();")
        return cur.fetchall()[0][0]
    
    def update(_id, _searching, _replacing, _intIsActive, _intIsCaseSensitive, _intIsRegExp):
        con = getDefaultConnection()
        cur = con.cursor()
        cur.execute(str("update searchAndReplaceTable set searching='" + correctForSql(_searching) + "', replacing='" + correctForSql(_replacing) + "', intIsActive='" + correctForSql(_intIsActive) + "', intIsCaseSensitive='" + correctForSql(_intIsCaseSensitive) + "', intIsRegExp='" + correctForSql(_intIsRegExp) + "' where id=" + str(int(_id))))
        con.commit()
    
    def delete(_id):
        con = getDefaultConnection()
        cur = con.cursor()
        cur.execute("delete from searchAndReplaceTable where id="+str(int(_id)))
        con.commit()
        
    
