# This file is part of HamsiManager.
#
# Copyright (c) 2010 - 2014 Murat Demir <mopened@gmail.com>
#
# Hamsi Manager is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Hamsi Manager is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with HamsiManager; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA


from Core import Universals as uni
from Databases import sqlite, getDefaultConnection, correctForSql, getAmendedSQLInsertOrUpdateQueries

tableName = "completerTable"
tableVersion = 1
allForFetch, allForFetchByObjectName = None, {}


def fetchAll():
    global allForFetch
    if allForFetch is None:
        con = getDefaultConnection()
        cur = con.cursor()
        cur.execute("SELECT * FROM " + tableName)
        allForFetch = cur.fetchall()
    return allForFetch


def fetchAllByObjectName(_objectName=None):
    global allForFetchByObjectName
    if _objectName is None:
        _objectName = "%*%"
    if _objectName not in allForFetchByObjectName or allForFetchByObjectName[_objectName] is None:
        con = getDefaultConnection()
        cur = con.cursor()
        if _objectName == "%*%":
            cur.execute("SELECT DISTINCT value FROM " + tableName)
        else:
            cur.execute(
                "SELECT DISTINCT value FROM " + tableName + " where objectName='" + _objectName + "' or objectName='*'")
        myValues = []
        for myval in cur.fetchall():
            myValues.append(myval[0])
        allForFetchByObjectName[_objectName] = myValues
    return allForFetchByObjectName[_objectName]


def checkValues(_objectName, _value):
    if len(_objectName.strip()) == 0 or len(_value.strip()) == 0:
        return False
    return True


def insert(_objectName, _value):
    _objectName = str(_objectName)
    _value = str(_value)
    global allForFetch, allForFetchByObjectName
    if checkValues(_objectName, _value):
        allForFetch, allForFetchByObjectName[_objectName], allForFetchByObjectName["%*%"] = None, None, None
        con = getDefaultConnection()
        cur = con.cursor()
        sqlQueries = getAmendedSQLInsertOrUpdateQueries(tableName,
                                                        {"objectName": "'" + correctForSql(_objectName) + "'",
                                                         "value": "'" + correctForSql(_value) + "'"},
                                                        ["objectName", "value"])
        cur.execute(sqlQueries[0])
        # cur.execute(sqlQueries[1]) # does not need update query
        con.commit()
    return None


def getTableCreateQuery():
    return "CREATE TABLE IF NOT EXISTS " + tableName + " ('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,'objectName' TEXT,'value' TEXT)"


def getDeleteTableQuery():
    return "DELETE FROM " + tableName


def getDefaultsQueries():
    sqlQueries = []
    sqlQueries += getAmendedSQLInsertOrUpdateQueries(tableName, {"objectName": "'*'", "value": "'Hamsi'"},
                                                     ["objectName", "value"])
    return sqlQueries


def checkUpdates(_oldVersion):
    if _oldVersion < 1:
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




