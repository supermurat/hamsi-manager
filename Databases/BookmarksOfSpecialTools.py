# -*- coding: utf-8 -*-

import Variables
import Universals
from Databases import sqlite, getDefaultConnection, correctForSql, getAmendedSQLInputQueries

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
            _type = Universals.MainWindow.Table.specialTollsBookmarkPointer
        if _type not in allForFetchByType or allForFetchByType[_type]==None:
            import Organizer
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
        if len(_bookmark)==0 or len(_value)==0:
            return False
        return True
    
    def insert(_bookmark, _value, _type=None):
        global allForFetch, allForFetchByType
        if _type==None:
            _type = Universals.MainWindow.Table.specialTollsBookmarkPointer
        if checkValues(_bookmark, _value, _type):
            allForFetch, allForFetchByType[_type] = None, None
            con = getDefaultConnection()
            cur = con.cursor()
            sqlQueries = getAmendedSQLInputQueries(tableName, {"bookmark" : "'" + correctForSql(_bookmark) + "'", "value" : "'" + correctForSql(_value) + "'", "type" : "'" + correctForSql(_type) + "'"}, ["value"])
            cur.execute(sqlQueries[0])
            cur.execute(sqlQueries[1])
            con.commit()
            cur.execute("SELECT last_insert_rowid();")
            return cur.fetchall()[0][0]
        return None
    
    def update(_id, _bookmark, _value, _type=None):
        global allForFetch, allForFetchByType
        if _type==None:
            _type = Universals.MainWindow.Table.specialTollsBookmarkPointer
        if checkValues(_bookmark, _value, _type):
            allForFetch, allForFetchByType[_type] = None, None
            con = getDefaultConnection()
            cur = con.cursor()
            cur.execute(str("update " + tableName + " set bookmark='" + correctForSql(_bookmark) + "', value='" + correctForSql(_value) + "', type='" + correctForSql(_type) + "' where id=" + str(int(_id))))
            con.commit()
    
    def delete(_id, _type=None):
        if _type==None:
            _type = Universals.MainWindow.Table.specialTollsBookmarkPointer
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
        sqlQueries += getAmendedSQLInputQueries(tableName, {"bookmark" : "''", "value" : "'File Name , Artist - Title ;right;113'", "type" : "'music'"}, ["value"])
        sqlQueries += getAmendedSQLInputQueries(tableName, {"bookmark" : "''", "value" : "'Artist - Title , File Name  ;left;113'", "type" : "'music'"}, ["value"])
        sqlQueries += getAmendedSQLInputQueries(tableName, {"bookmark" : "''", "value" : "'Track No - Title , File Name  ;left;113'", "type" : "'music'"}, ["value"])
        sqlQueries += getAmendedSQLInputQueries(tableName, {"bookmark" : "''", "value" : "'Artist - Album , Directory  ;left;113'", "type" : "'music'"}, ["value"])
        sqlQueries += getAmendedSQLInputQueries(tableName, {"bookmark" : "''", "value" : "'File Name , Title  ;right;102'", "type" : "'music'"}, ["value"])
        sqlQueries += getAmendedSQLInputQueries(tableName, {"bookmark" : "''", "value" : "'Title , File Name  ;right;102'", "type" : "'music'"}, ["value"])
        sqlQueries += getAmendedSQLInputQueries(tableName, {"bookmark" : "''", "value" : "'Year , Album  ;right;102'", "type" : "'music'"}, ["value"])
        sqlQueries += getAmendedSQLInputQueries(tableName, {"bookmark" : "''", "value" : "'Lyrics , Artist - Title  ;right;113'", "type" : "'music'"}, ["value"])
        sqlQueries += getAmendedSQLInputQueries(tableName, {"bookmark" : "''", "value" : "'Artist - Album - Title , File Name  ;left;124'", "type" : "'music'"}, ["value"])
        sqlQueries += getAmendedSQLInputQueries(tableName, {"bookmark" : "''", "value" : "'Directory - File Name , Directory  ;left;113'", "type" : "'file'"}, ["value"])
        sqlQueries += getAmendedSQLInputQueries(tableName, {"bookmark" : "''", "value" : "'Directory , File Name  ;right;102'", "type" : "'file'"}, ["value"])
        sqlQueries += getAmendedSQLInputQueries(tableName, {"bookmark" : "''", "value" : "'File Name , Directory  ;right;102'", "type" : "'file'"}, ["value"])
        sqlQueries += getAmendedSQLInputQueries(tableName, {"bookmark" : "''", "value" : "'Directory , File/Directory Name  ;right;102'", "type" : "'directory'"}, ["value"])
        sqlQueries += getAmendedSQLInputQueries(tableName, {"bookmark" : "''", "value" : "'File/Directory Name , Directory  ;right;102'", "type" : "'directory'"}, ["value"])
        sqlQueries += getAmendedSQLInputQueries(tableName, {"bookmark" : "''", "value" : "'Directory , File Name  ;right;102'", "type" : "'subfolder'"}, ["value"])
        sqlQueries += getAmendedSQLInputQueries(tableName, {"bookmark" : "''", "value" : "'File Name , Directory  ;right;102'", "type" : "'subfolder'"}, ["value"])
        sqlQueries += getAmendedSQLInputQueries(tableName, {"bookmark" : "''", "value" : "'Directory Name , Directory  ;right;102'", "type" : "'cover'"}, ["value"])
        sqlQueries += getAmendedSQLInputQueries(tableName, {"bookmark" : "''", "value" : "'Source Cover , Current Cover  ;right;102'", "type" : "'cover'"}, ["value"])
        sqlQueries += getAmendedSQLInputQueries(tableName, {"bookmark" : "''", "value" : "'Destination Cover , Source Cover  ;right;102'", "type" : "'cover'"}, ["value"])
        sqlQueries += getAmendedSQLInputQueries(tableName, {"bookmark" : "''", "value" : "'Destination Cover , Current Cover  ;right;102'", "type" : "'cover'"}, ["value"])
        return sqlQueries
        
        
