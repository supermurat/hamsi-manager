## This file is part of HamsiManager.
## 
## Copyright (c) 2010 - 2013 Murat Demir <mopened@gmail.com>      
##
## Hamsi Manager is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
## 
## Hamsi Manager is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
## 
## You should have received a copy of the GNU General Public License
## along with HamsiManager; if not, write to the Free Software
## Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA


from Core import Universals as uni
import FileUtils as fu
from Databases import sqlite, getDefaultConnection, correctForSql, getAmendedSQLInsertOrUpdateQueries

tableName = "bookmarksOfDirectories"
tableVersion = 2
allForFetch = None

def fetchAll():
    global allForFetch
    if allForFetch==None:
        con = getDefaultConnection()
        cur = con.cursor()
        cur.execute("SELECT * FROM " + tableName)
        allForFetch = cur.fetchall()
    return allForFetch

def fetch(_id):
    con = getDefaultConnection()
    cur = con.cursor()
    cur.execute("SELECT * FROM " + tableName + " where id=" + str(int(_id)))
    return cur.fetchall()

def checkValues(_bookmark, _value, _type):
    if len(_bookmark)==0 or len(_value)==0:
        return False
    return True

def insert(_bookmark, _value, _type=""):
    global allForFetch
    if checkValues(_bookmark, _value, _type):
        allForFetch = None
        con = getDefaultConnection()
        cur = con.cursor()
        sqlQueries = getAmendedSQLInsertOrUpdateQueries(tableName, {"bookmark" : "'" + correctForSql(_bookmark) + "'", "value" : "'" + correctForSql(_value) + "'", "type" : "'" + correctForSql(_type) + "'"}, ["value"])
        cur.execute(sqlQueries[0])
        cur.execute(sqlQueries[1])
        con.commit()
        cur.execute("SELECT last_insert_rowid();")
        return cur.fetchall()[0][0]
    return None

def update(_id, _bookmark, _value, _type=""):
    global allForFetch
    if checkValues(_bookmark, _value, _type):
        allForFetch = None
        con = getDefaultConnection()
        cur = con.cursor()
        cur.execute(str("update " + tableName + " set bookmark='" + correctForSql(_bookmark) + "', value='" + correctForSql(_value) + "', type='" + correctForSql(_type) + "' where id=" + str(int(_id))))
        con.commit()

def delete(_id):
    global allForFetch
    allForFetch = None
    con = getDefaultConnection()
    cur = con.cursor()
    cur.execute("delete from " + tableName + " where id="+str(int(_id)))
    con.commit()

def getTableCreateQuery():
    return "CREATE TABLE IF NOT EXISTS " + tableName + " ('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,'bookmark' TEXT,'value' TEXT,'type' TEXT)"

def getDeleteTableQuery():
    return "DELETE FROM " + tableName

def getDefaultsQueries():
    sqlQueries = []
    sqlQueries += getAmendedSQLInsertOrUpdateQueries(tableName, {"bookmark" : "'Home'", "value" : "'"+fu.userDirectoryPath+"'", "type" : "''"}, ["value"])
    if uni.isWindows:
        sqlQueries += getAmendedSQLInsertOrUpdateQueries(tableName, {"bookmark" : "'C:\\'", "value" : "'C:\\'", "type" : "''"}, ["value"])
    else:
        sqlQueries += getAmendedSQLInsertOrUpdateQueries(tableName, {"bookmark" : "'MNT'", "value" : "'/mnt'", "type" : "''"}, ["value"])
        sqlQueries += getAmendedSQLInsertOrUpdateQueries(tableName, {"bookmark" : "'MEDIA'", "value" : "'/media'", "type" : "''"}, ["value"])
    return sqlQueries

def checkUpdates(_oldVersion):
    if _oldVersion<2:
        con = getDefaultConnection()
        cur = con.cursor()
        cur.execute(str("DROP TABLE " + tableName + ";"))
        con.commit()
        cur.execute(getTableCreateQuery())
        con.commit()
        for sqlCommand in getDefaultsQueries():
            cur = con.cursor()
            cur.execute(str(sqlCommand))
            con.commit()


    
    
