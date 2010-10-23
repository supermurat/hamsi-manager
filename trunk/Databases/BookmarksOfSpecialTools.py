# -*- coding: utf-8 -*-

import Variables
import Universals
from Databases import sqlite, correctForSql, getDefaultConnection

class BookmarksOfSpecialTools:
    global fetchAll, fetchAllByType, fetch, insert, update, delete
        
    def fetchAll():
        con = getDefaultConnection()
        cur = con.cursor()
        cur.execute("SELECT * FROM bookmarksOfSpecialTools")
        return cur.fetchall()
        
    def fetchAllByType(_type=None):
        import Organizer
        if _type==None:
            _type = Universals.MainWindow.Table.specialTollsBookmarkPointer
        con = getDefaultConnection()
        cur = con.cursor()
        cur.execute("SELECT * FROM bookmarksOfSpecialTools where type='" + _type + "'")
        myBookmarks = []
        for mybm in cur.fetchall():
            tempT = mybm[2]
            tempString = tempT.split(";")
            tempT = ""
            for t in tempString[:-2]:
                tempT+=t
            newText  = Organizer.whatDoesSpecialCommandDo("-",
                            tempString[-2],
                            tempT, False, True)
            myBookmarks.append([mybm[0], newText, mybm[2], mybm[3]])
        return myBookmarks
        return myBookmarks
    
    def fetch(_id):
        con = getDefaultConnection()
        cur = con.cursor()
        cur.execute("SELECT * FROM bookmarksOfSpecialTools where id=" + str(int(_id)))
        return cur.fetchall()
    
    def insert(_bookmark, _value, _type=None):
        if _type==None:
            _type = Universals.MainWindow.Table.specialTollsBookmarkPointer
        con = getDefaultConnection()
        cur = con.cursor()
        cur.execute("insert into bookmarksOfSpecialTools(bookmark,value,type) values('" + correctForSql(_bookmark) + "','" + correctForSql(_value) + "','" + correctForSql(_type) + "')")
        con.commit()
        cur.execute("SELECT last_insert_rowid();")
        return cur.fetchall()[0][0]
    
    def update(_id, _bookmark, _value, _type=None):
        if _type==None:
            _type = Universals.MainWindow.Table.specialTollsBookmarkPointer
        con = getDefaultConnection()
        cur = con.cursor()
        cur.execute(str("update bookmarksOfSpecialTools set bookmark='" + correctForSql(_bookmark) + "', value='" + correctForSql(_value) + "', type='" + correctForSql(_type) + "' where id=" + str(int(_id))))
        con.commit()
    
    def delete(_id):
        con = getDefaultConnection()
        cur = con.cursor()
        cur.execute("delete from bookmarksOfSpecialTools where id="+str(int(_id)))
        con.commit()
        
        
