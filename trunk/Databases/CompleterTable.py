# -*- coding: utf-8 -*-

import Variables
import Universals
from Databases import sqlite, getDefaultConnection, correctForSql, getAmendedSQLInputQueries

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
            _objectName = "*"
        if _objectName not in allForFetchByObjectName or allForFetchByObjectName[_objectName]==None:
            con = getDefaultConnection()
            cur = con.cursor()
            cur.execute("SELECT value FROM " + tableName + " where objectName='" + _objectName + "' or objectName='*'")
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
            allForFetch, allForFetchByObjectName[_objectName] = None, None
            con = getDefaultConnection()
            cur = con.cursor()
            sqlQueries = getAmendedSQLInputQueries(tableName, {"objectName" : "'" + correctForSql(_objectName) + "'", "value" : "'" + correctForSql(_value) + "'"}, ["objectName", "value"])
            cur.execute(sqlQueries[0])
            cur.execute(sqlQueries[1])
            con.commit()
            cur.execute("SELECT last_insert_rowid();")
            return cur.fetchall()[0][0]
        return None
    
    def update(_id, _objectName, _value):
        global allForFetch, allForFetchByObjectName
        if checkValues(_objectName, _value):
            allForFetch, allForFetchByObjectName[_objectName] = None, None
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
        sqlQueries += getAmendedSQLInputQueries(tableName, {"objectName" : "'*'", "value" : "'Hamsi'"}, ["objectName", "value"])
        return sqlQueries
        
    
    
    
