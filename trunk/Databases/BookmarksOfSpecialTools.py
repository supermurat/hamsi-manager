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


from Core import Variables
from Core import Universals
from Databases import sqlite, getDefaultConnection, correctForSql, getAmendedSQLInsertOrUpdateQueries

class BookmarksOfSpecialTools:
    global fetchAll, fetchAllByType, fetch, checkValues, insert, update, delete
    global getTableCreateQuery, getDeleteTableQuery, getDefaultsQueries
    global tableName, tableVersion, allForFetch, allForFetchByType
    tableName = "bookmarksOfSpecialTools"
    tableVersion = 2
    allForFetch, allForFetchByType = None, {}
        
    def fetchAll():
        global allForFetch
        if allForFetch==None:
            con = getDefaultConnection()
            cur = con.cursor()
            cur.execute("SELECT * FROM " + tableName)
            allForFetch = cur.fetchall()
        return allForFetch
        
    def fetchAllByType(_type=None):
        global allForFetchByType
        if _type==None:
            _type = Universals.MainWindow.Table.SubTable.keyName
        if _type not in allForFetchByType or allForFetchByType[_type]==None:
            from Core import Organizer
            con = getDefaultConnection()
            cur = con.cursor()
            cur.execute("SELECT * FROM " + tableName + " where type='" + _type + "'")
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
            allForFetchByType[_type] = myBookmarks
        return allForFetchByType[_type]
    
    def fetch(_id):
        con = getDefaultConnection()
        cur = con.cursor()
        cur.execute("SELECT * FROM " + tableName + " where id=" + str(int(_id)))
        return cur.fetchall()
    
    def checkValues(_bookmark, _value, _type):
        if len(_value)==0:
            return False
        return True
    
    def insert(_bookmark, _value, _type=None):
        global allForFetch, allForFetchByType
        if _type==None:
            _type = Universals.MainWindow.Table.SubTable.keyName
        if checkValues(_bookmark, _value, _type):
            allForFetch, allForFetchByType[_type] = None, None
            con = getDefaultConnection()
            cur = con.cursor()
            sqlQueries = getAmendedSQLInsertOrUpdateQueries(tableName, {"bookmark" : "'" + correctForSql(_bookmark) + "'", "value" : "'" + correctForSql(_value) + "'", "type" : "'" + correctForSql(_type) + "'"}, ["value"])
            cur.execute(sqlQueries[0])
            cur.execute(sqlQueries[1])
            con.commit()
            cur.execute("SELECT last_insert_rowid();")
            return cur.fetchall()[0][0]
        return None
    
    def update(_id, _bookmark, _value, _type=None):
        global allForFetch, allForFetchByType
        if _type==None:
            _type = Universals.MainWindow.Table.SubTable.keyName
        if checkValues(_bookmark, _value, _type):
            allForFetch, allForFetchByType[_type] = None, None
            con = getDefaultConnection()
            cur = con.cursor()
            cur.execute(str("update " + tableName + " set bookmark='" + correctForSql(_bookmark) + "', value='" + correctForSql(_value) + "', type='" + correctForSql(_type) + "' where id=" + str(int(_id))))
            con.commit()
    
    def delete(_id, _type=None):
        if _type==None:
            _type = Universals.MainWindow.Table.SubTable.keyName
        global allForFetch, allForFetchByType
        allForFetch, allForFetchByType[_type] = None, None
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
        sqlQueries += getAmendedSQLInsertOrUpdateQueries(tableName, {"bookmark" : "''", "value" : "'File Name , Artist - Title ;right;113'", "type" : "'music'"}, ["value"])
        sqlQueries += getAmendedSQLInsertOrUpdateQueries(tableName, {"bookmark" : "''", "value" : "'Artist - Title , File Name  ;left;113'", "type" : "'music'"}, ["value"])
        sqlQueries += getAmendedSQLInsertOrUpdateQueries(tableName, {"bookmark" : "''", "value" : "'Track No - Title , File Name  ;left;113'", "type" : "'music'"}, ["value"])
        sqlQueries += getAmendedSQLInsertOrUpdateQueries(tableName, {"bookmark" : "''", "value" : "'Artist - Album , Directory  ;left;113'", "type" : "'music'"}, ["value"])
        sqlQueries += getAmendedSQLInsertOrUpdateQueries(tableName, {"bookmark" : "''", "value" : "'File Name , Title  ;right;102'", "type" : "'music'"}, ["value"])
        sqlQueries += getAmendedSQLInsertOrUpdateQueries(tableName, {"bookmark" : "''", "value" : "'Title , File Name  ;right;102'", "type" : "'music'"}, ["value"])
        sqlQueries += getAmendedSQLInsertOrUpdateQueries(tableName, {"bookmark" : "''", "value" : "'Year , Album  ;right;102'", "type" : "'music'"}, ["value"])
        sqlQueries += getAmendedSQLInsertOrUpdateQueries(tableName, {"bookmark" : "''", "value" : "'Lyrics , Artist - Title  ;right;113'", "type" : "'music'"}, ["value"])
        sqlQueries += getAmendedSQLInsertOrUpdateQueries(tableName, {"bookmark" : "''", "value" : "'Artist - Album - Title , File Name  ;left;124'", "type" : "'music'"}, ["value"])
        sqlQueries += getAmendedSQLInsertOrUpdateQueries(tableName, {"bookmark" : "''", "value" : "'Directory - File Name , Directory  ;left;113'", "type" : "'file'"}, ["value"])
        sqlQueries += getAmendedSQLInsertOrUpdateQueries(tableName, {"bookmark" : "''", "value" : "'Directory , File Name  ;right;102'", "type" : "'file'"}, ["value"])
        sqlQueries += getAmendedSQLInsertOrUpdateQueries(tableName, {"bookmark" : "''", "value" : "'File Name , Directory  ;right;102'", "type" : "'file'"}, ["value"])
        sqlQueries += getAmendedSQLInsertOrUpdateQueries(tableName, {"bookmark" : "''", "value" : "'Directory , File/Directory Name  ;right;102'", "type" : "'directory'"}, ["value"])
        sqlQueries += getAmendedSQLInsertOrUpdateQueries(tableName, {"bookmark" : "''", "value" : "'File/Directory Name , Directory  ;right;102'", "type" : "'directory'"}, ["value"])
        sqlQueries += getAmendedSQLInsertOrUpdateQueries(tableName, {"bookmark" : "''", "value" : "'Directory , File Name  ;right;102'", "type" : "'subfolder'"}, ["value"])
        sqlQueries += getAmendedSQLInsertOrUpdateQueries(tableName, {"bookmark" : "''", "value" : "'File Name , Directory  ;right;102'", "type" : "'subfolder'"}, ["value"])
        sqlQueries += getAmendedSQLInsertOrUpdateQueries(tableName, {"bookmark" : "''", "value" : "'Directory Name , Directory  ;right;102'", "type" : "'cover'"}, ["value"])
        sqlQueries += getAmendedSQLInsertOrUpdateQueries(tableName, {"bookmark" : "''", "value" : "'Source Cover , Current Cover  ;right;102'", "type" : "'cover'"}, ["value"])
        sqlQueries += getAmendedSQLInsertOrUpdateQueries(tableName, {"bookmark" : "''", "value" : "'Destination Cover , Source Cover  ;right;102'", "type" : "'cover'"}, ["value"])
        sqlQueries += getAmendedSQLInsertOrUpdateQueries(tableName, {"bookmark" : "''", "value" : "'Destination Cover , Current Cover  ;right;102'", "type" : "'cover'"}, ["value"])
        return sqlQueries
        
        
