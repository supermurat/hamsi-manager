# -*- coding: utf-8 -*-

import Variables
import Universals
from Databases import sqlite, getDefaultConnection, correctForSql, getAmendedSQLInputQueries

class BookmarksOfDirectories:
    global fetchAll, fetch, insert, update, delete
    global getTableCreateQuery, getDeleteTableQuery, getDefaultsQueries
    global tableName, tableVersion, allForFetch
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
    
    def insert(_bookmark, _value, _type=""):
        global allForFetch
        allForFetch = None
        con = getDefaultConnection()
        cur = con.cursor()
        cur.execute("insert into " + tableName + " (bookmark,value,type) values('" + correctForSql(_bookmark) + "','" + correctForSql(_value) + "','" + correctForSql(_type) + "')")
        con.commit()
        cur.execute("SELECT last_insert_rowid();")
        return cur.fetchall()[0][0]
    
    def update(_id, _bookmark, _value, _type=""):
        global allForFetch
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
        sqlQueries += getAmendedSQLInputQueries(tableName, {"bookmark" : "'Home'", "value" : "'"+Variables.userDirectoryPath+"'", "type" : "''"}, ["value"])
        sqlQueries += getAmendedSQLInputQueries(tableName, {"bookmark" : "'MNT'", "value" : "'/mnt'", "type" : "''"}, ["value"])
        sqlQueries += getAmendedSQLInputQueries(tableName, {"bookmark" : "'MEDIA'", "value" : "'/media'", "type" : "''"}, ["value"])
        return sqlQueries
        
    
    
    
