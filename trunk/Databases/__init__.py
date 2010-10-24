# -*- coding: utf-8 -*-

import sys
if float(sys.version[:3])>=2.6:
    import sqlite3 as sqlite
else:
    from pysqlite2 import dbapi2 as sqlite
import Universals
from Databases import *
    
class Databases:
    global defaultConnection, getDefaultConnection, getAllDatabases, getDBPropertiesCreateQuery, reFillDatabases, correctForSql, getAmendedSQLInputQueries, checkDatabases
    defaultConnection = None
        
    def getDefaultConnection():
        global defaultConnection
        if defaultConnection==None:
            defaultConnection = sqlite.connect(Universals.pathOfSettingsDirectory + "/database.sqlite")
        return defaultConnection
    
    def getAllDatabases():
        return [BookmarksOfDirectories, BookmarksOfSpecialTools, SearchAndReplaceTable, CompleterTable]
    
    def getDBPropertiesCreateQuery():
        return "CREATE TABLE IF NOT EXISTS dbProperties ('keyName' TEXT NOT NULL,'value' TEXT)"
        
    def reFillDatabases(_table="All", _actionType="dropAndInsert", _makeBackUp=False):
        if _makeBackUp==True:
            makeBackUp(_table)
        tableCreateQueries, sqlCommands, tableInsertImportantQueries = [], [], []
        tableCreateQueries.append(getDBPropertiesCreateQuery())
        for database in getAllDatabases():
            if _table==database.tableName or _table=="All":
                tableCreateQueries.append(database.getTableCreateQuery())
                if _actionType=="dropAndInsert":
                    sqlCommands.append(database.getDeleteTableQuery())
                sqlCommands += database.getDefaultsQueries()
                tableInsertImportantQueries += getAmendedSQLInputQueries("dbProperties", {"keyName" : "'" + database.tableName + "_Version'", "value" : "'" + str(database.tableVersion) + "'"}, ["keyName"])
        con = getDefaultConnection()
        for sqlCommand in tableCreateQueries:
            cur = con.cursor()
            cur.execute(str(sqlCommand))
            con.commit()
        for sqlCommand in tableInsertImportantQueries:
            cur = con.cursor()
            cur.execute(str(sqlCommand))
            con.commit()
        for sqlCommand in sqlCommands:
            cur = con.cursor()
            cur.execute(str(sqlCommand))
            con.commit()
    
    def correctForSql(_string):
        return str(_string).replace("'", "''")
    
    def getAmendedSQLInputQueries(_table, _columnNamesAndValues, _primaryColumns):
        sqlString0 = "INSERT INTO " + _table + "("
        sqlString1 = ") SELECT "
        sqlString2 = " WHERE (SELECT COUNT(*) FROM " + _table + " WHERE "
        sqlString3 = "UPDATE " + _table + " SET "
        sqlString4 = " WHERE "
        i, j = 0, 0
        for key, value in _columnNamesAndValues.items():
            if i>0:
                sqlString0 += ","
                sqlString1 += ","
                sqlString3 += ","
            sqlString0 += key
            sqlString1 += str(value)
            sqlString3 += key + "=" + str(value)
            if _primaryColumns.count(key)>0:
                if j>0:
                    sqlString2 += " AND "
                    sqlString4 += " AND "
                sqlString2 += key + "=" + str(value)
                sqlString4 += key + "=" + str(value)
                j +=1
            i +=1
        return [sqlString0 + sqlString1 + sqlString2 + ")=0;" , sqlString3 + sqlString4 + ";"]
        
    def checkDatabases():
        try:
            con = getDefaultConnection()
            cur = con.cursor()
            cur.execute("SELECT * FROM dbProperties")
            tableCreateQueries, sqlCommands, tableInsertImportantQueries = [], [], []
            for database in getAllDatabases():
                cur = con.cursor()
                cur.execute("SELECT * FROM dbProperties where keyName='" + database.tableName + "_Version'")
                tableVersion = int(cur.fetchall()[0][1])
                if tableVersion<database.tableVersion:
                    tableCreateQueries.append(database.getTableCreateQuery())
                    sqlCommands += database.getDefaultsQueries()
                    tableInsertImportantQueries += getAmendedSQLInputQueries("dbProperties", {"keyName" : "'" + database.tableName + "_Version'", "value" : "'" + str(database.tableVersion) + "'"}, ["keyName"])
            for sqlCommand in tableCreateQueries:
                cur = con.cursor()
                cur.execute(str(sqlCommand))
                con.commit()
            for sqlCommand in tableInsertImportantQueries:
                cur = con.cursor()
                cur.execute(str(sqlCommand))
                con.commit()
            for sqlCommand in sqlCommands:
                cur = con.cursor()
                cur.execute(str(sqlCommand))
                con.commit()
                
#            try:
#                cur.execute("SELECT * FROM dbProperties where keyName='bookmarksOfDirectories_Version'")
#                bookmarksOfDirectoriesVersion = int(cur.fetchall()[0][1])
#            except:
#                bookmarksOfDirectoriesVersion = 0
#            try:
#                cur.execute("SELECT * FROM dbProperties where keyName='bookmarksOfSpecialTools_Version'")
#                bookmarksOfSpecialToolsVersion = int(cur.fetchall()[0][1])
#            except:
#                bookmarksOfSpecialToolsVersion = 0
#            try:
#                cur.execute("SELECT * FROM dbProperties where keyName='searchAndReplaceTable_Version'")
#                searchAndReplaceTableVersion = int(cur.fetchall()[0][1])
#            except:
#                searchAndReplaceTableVersion = 0
#            if bookmarksOfDirectoriesVersion<x:
#                pass
#            if bookmarksOfSpecialToolsVersion<x:
#                pass
#            if searchAndReplaceTableVersion<x:
#                pass
        except:
            reFillDatabases()
    
        


