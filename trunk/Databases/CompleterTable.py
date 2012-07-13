## This file is part of HamsiManager.
## 
## Copyright (c) 2010 - 2012 Murat Demir <mopened@gmail.com>      
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

class CompleterTable:
    global fetchAll, fetchAllByObjectName, fetch, checkValues, insert, update, delete
    global getTableCreateQuery, getDeleteTableQuery, getDefaultsQueries
    global tableName, tableVersion, allForFetch, allForFetchByObjectName
    tableName = "completerTable"
    tableVersion = 1
    allForFetch, allForFetchByObjectName = None, {}
        
    def fetchAll():
        global allForFetch
        if allForFetch==None:
            con = getDefaultConnection()
            cur = con.cursor()
            cur.execute("SELECT * FROM " + tableName)
            allForFetch = cur.fetchall()
        return allForFetch
        
    def fetchAllByObjectName(_objectName=None):
        global allForFetchByObjectName
        if _objectName==None:
            _objectName = "%*%"
        if _objectName not in allForFetchByObjectName or allForFetchByObjectName[_objectName]==None:
            con = getDefaultConnection()
            cur = con.cursor()
            if _objectName=="%*%":
                cur.execute("SELECT DISTINCT value FROM " + tableName)
            else:
                cur.execute("SELECT DISTINCT value FROM " + tableName + " where objectName='" + _objectName + "' or objectName='*'")
            myValues = []
            for myval in cur.fetchall():
                myValues.append(myval[0])
            allForFetchByObjectName[_objectName] = myValues
        return allForFetchByObjectName[_objectName]
    
    def fetch(_id):
        con = getDefaultConnection()
        cur = con.cursor()
        cur.execute("SELECT * FROM " + tableName + " where id=" + str(int(_id)))
        return cur.fetchall()
    
    def checkValues(_objectName, _value):
        if len(_objectName)==0 or len(_value)==0:
            return False
        return True
    
    def insert(_objectName, _value):
        global allForFetch, allForFetchByObjectName
        if checkValues(_objectName, _value):
            allForFetch, allForFetchByObjectName[_objectName], allForFetchByObjectName["%*%"] = None, None, None
            con = getDefaultConnection()
            cur = con.cursor()
            sqlQueries = getAmendedSQLInsertOrUpdateQueries(tableName, {"objectName" : "'" + correctForSql(_objectName) + "'", "value" : "'" + correctForSql(_value) + "'"}, ["objectName", "value"])
            cur.execute(sqlQueries[0])
            cur.execute(sqlQueries[1])
            con.commit()
            cur.execute("SELECT last_insert_rowid();")
            return cur.fetchall()[0][0]
        return None
    
    def update(_id, _objectName, _value):
        global allForFetch, allForFetchByObjectName
        if checkValues(_objectName, _value):
            allForFetch, allForFetchByObjectName[_objectName], allForFetchByObjectName["%*%"] = None, None, None
            con = getDefaultConnection()
            cur = con.cursor()
            cur.execute(str("update " + tableName + " set objectName='" + correctForSql(_objectName) + "', value='" + correctForSql(_value) + "' where id=" + str(int(_id))))
            con.commit()
    
    def delete(_id):
        global allForFetch, allForFetchByObjectName
        allForFetch, allForFetchByObjectName = None, {}
        con = getDefaultConnection()
        cur = con.cursor()
        cur.execute("delete from " + tableName + " where id="+str(int(_id)))
        con.commit()
        
    def getTableCreateQuery():
        return "CREATE TABLE IF NOT EXISTS " + tableName + " ('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,'objectName' TEXT,'value' TEXT)"
        
    def getDeleteTableQuery():
        return "DELETE FROM " + tableName
        
    def getDefaultsQueries():
        sqlQueries = []
        sqlQueries += getAmendedSQLInsertOrUpdateQueries(tableName, {"objectName" : "'*'", "value" : "'Hamsi'"}, ["objectName", "value"])
        return sqlQueries
        
    
    
    
