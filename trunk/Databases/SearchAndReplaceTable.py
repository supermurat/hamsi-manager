# -*- coding: utf-8 -*-

import Variables
import Universals
from Databases import sqlite, getDefaultConnection, correctForSql, getAmendedSQLInputQueries

class SearchAndReplaceTable:
    global fetchAll, fetch, insert, update, delete
    global getTableCreateQuery, getDeleteTableQuery, getDefaultsQueries
    global tableName, tableVersion, allForFetch
    tableName = "searchAndReplaceTable"
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
    
    def insert(_searching, _replacing, _intIsActive, _intIsCaseSensitive, _intIsRegExp):
        global allForFetch
        allForFetch = None
        con = getDefaultConnection()
        cur = con.cursor()
        cur.execute("insert into " + tableName + " (searching, replacing, intIsActive, intIsCaseSensitive, intIsRegExp) values('" + correctForSql(_searching) + "','" + correctForSql(_replacing) + "','" + correctForSql(_intIsActive) + "','" + correctForSql(_intIsCaseSensitive) + "','" + correctForSql(_intIsRegExp) + "')")
        con.commit()
        cur.execute("SELECT last_insert_rowid();")
        return cur.fetchall()[0][0]
    
    def update(_id, _searching, _replacing, _intIsActive, _intIsCaseSensitive, _intIsRegExp):
        global allForFetch
        allForFetch = None
        con = getDefaultConnection()
        cur = con.cursor()
        cur.execute(str("update " + tableName + " set searching='" + correctForSql(_searching) + "', replacing='" + correctForSql(_replacing) + "', intIsActive='" + correctForSql(_intIsActive) + "', intIsCaseSensitive='" + correctForSql(_intIsCaseSensitive) + "', intIsRegExp='" + correctForSql(_intIsRegExp) + "' where id=" + str(int(_id))))
        con.commit()
    
    def delete(_id):
        global allForFetch
        allForFetch = None
        con = getDefaultConnection()
        cur = con.cursor()
        cur.execute("delete from " + tableName + " where id="+str(int(_id)))
        con.commit()
        
    def getTableCreateQuery():
        return "CREATE TABLE IF NOT EXISTS " + tableName + " ('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,'searching' TEXT,'replacing' TEXT,'intIsActive' INTEGER,'intIsCaseSensitive' INTEGER,'intIsRegExp' INTEGER)"
        
    def getDeleteTableQuery():
        return "DELETE FROM " + tableName
        
    def getDefaultsQueries():
        sqlQueries = []
        sqlQueries += getAmendedSQLInputQueries(tableName, {"searching" : "'http://'", "replacing" : "''", "intIsActive" : "1", "intIsCaseSensitive" : "1", "intIsRegExp" : "0"}, ["searching", "replacing"])
        sqlQueries += getAmendedSQLInputQueries(tableName, {"searching" : "'www'", "replacing" : "''", "intIsActive" : "1", "intIsCaseSensitive" : "1", "intIsRegExp" : "0"}, ["searching", "replacing"])
        return sqlQueries
        
    
