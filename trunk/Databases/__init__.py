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


import sys
if float(sys.version[:3])>=2.6:
    import sqlite3 as sqlite
else:
    from pysqlite2 import dbapi2 as sqlite
from Core import Universals
import InputOutputs
from Databases import *
    
class Databases:
    global defaultConnection, getDefaultConnection, getAllDatabases, getDBPropertiesCreateQuery, reFillDatabases, correctForSql, getAmendedSQLInsertOrUpdateQueries, checkDatabases, getAmendedSQLSelectOrInsertAndSelectQueries, correctForUser
    defaultConnection = None
        
    def getDefaultConnection():
        global defaultConnection
        if defaultConnection==None:
            defaultConnection = sqlite.connect(InputOutputs.joinPath(Universals.pathOfSettingsDirectory, "database.sqlite"))
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
                tableInsertImportantQueries += getAmendedSQLInsertOrUpdateQueries("dbProperties", {"keyName" : "'" + database.tableName + "_Version'", "value" : "'" + str(database.tableVersion) + "'"}, ["keyName"])
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
    
    def correctForSql(_string, _type="varchar"):
        if _type=="int":
            stringInt = "NULL"
            try:stringInt = str(int(_string))
            except:pass
            return stringInt
        return str(_string).replace("'", "''")
    
    def correctForUser(_string):
        if _string is None or str(_string).upper()=="NULL" or str(_string).upper()=="NONE":
            return ""
        return str(_string).replace("'", "''")
    
    def getAmendedSQLInsertOrUpdateQueries(_table, _columnNamesAndValues, _primaryColumns):
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
    
    def getAmendedSQLSelectOrInsertAndSelectQueries(_table, _selectedColumn, _columnNamesAndValues):
        sqlString0 = "SELECT " + _selectedColumn + " FROM " + _table + " WHERE " 
        sqlString1 = "INSERT INTO " + _table + "("
        sqlString2 = ") VALUES ("
        sqlString3 = ") ON DUPLICATE KEY UPDATE " 
        j = 0
        for key, value in _columnNamesAndValues.items():
            if j>0:
                sqlString1 += ","
                sqlString2 += ","
            sqlString1 += key
            sqlString2 += str(value)
            if j>0:
                sqlString0 += " AND "
                sqlString3 += " , "
            sqlString0 += key + "=" + str(value)
            sqlString3 += key + "=" + key
            j +=1
        return [sqlString1 + sqlString2 + sqlString3, sqlString0]
        
    def checkDatabases():
        try:
            con = getDefaultConnection()
            cur = con.cursor()
            cur.execute("SELECT * FROM dbProperties")
            tableCreateQueries, sqlCommands, tableInsertImportantQueries = [], [], []
            for database in getAllDatabases():
                try:
                    cur = con.cursor()
                    cur.execute("SELECT * FROM dbProperties where keyName='" + database.tableName + "_Version'")
                    tableVersion = int(cur.fetchall()[0][1])
                except:
                    tableVersion = 0
                if tableVersion<database.tableVersion:
                    tableCreateQueries.append(database.getTableCreateQuery())
                    sqlCommands += database.getDefaultsQueries()
                    tableInsertImportantQueries += getAmendedSQLInsertOrUpdateQueries("dbProperties", {"keyName" : "'" + database.tableName + "_Version'", "value" : "'" + str(database.tableVersion) + "'"}, ["keyName"])
                    
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
        except:
            reFillDatabases()
    
        


