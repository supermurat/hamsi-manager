# # This file is part of HamsiManager.
# #
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
from Core.MyObjects import *
from Databases import sqlite, getDefaultConnection, correctForSql, getAmendedSQLInsertOrUpdateQueries

tableName = "bookmarksOfSpecialTools"
tableVersion = 4
allForFetch, allForFetchByType = None, {}


def fetchAll():
    global allForFetch
    if allForFetch == None:
        con = getDefaultConnection()
        cur = con.cursor()
        cur.execute("SELECT * FROM " + tableName)
        allForFetch = cur.fetchall()
    return allForFetch


def fetchAllByType(_type=None):
    global allForFetchByType
    if _type == None:
        _type = getMainWindow().Table.keyName
    if _type not in allForFetchByType or allForFetchByType[_type] == None:
        from SpecialTools import SpecialActions

        con = getDefaultConnection()
        cur = con.cursor()
        cur.execute("SELECT * FROM " + tableName + " where type='" + _type + "'")
        myBookmarks = []
        for mybm in cur.fetchall():
            newText = SpecialActions.whatDoesSpecialCommandDo(eval(str(mybm[1])), False, True)
            myBookmarks.append([mybm[0], newText, mybm[1], mybm[2]])
        allForFetchByType[_type] = myBookmarks
    return allForFetchByType[_type]


def fetch(_id):
    con = getDefaultConnection()
    cur = con.cursor()
    cur.execute("SELECT * FROM " + tableName + " where id=" + str(int(_id)))
    return cur.fetchall()


def checkValues(_value, _type):
    if len(_value) == 0:
        return False
    return True


def insert(_value, _type=None):
    global allForFetch, allForFetchByType
    if _type == None:
        _type = getMainWindow().Table.keyName
    if checkValues(_value, _type):
        allForFetch, allForFetchByType[_type] = None, None
        con = getDefaultConnection()
        cur = con.cursor()
        sqlQueries = getAmendedSQLInsertOrUpdateQueries(tableName, {"value": "'" + correctForSql(_value) + "'",
                                                                    "type": "'" + correctForSql(_type) + "'"},
                                                        ["value"])
        cur.execute(sqlQueries[0])
        cur.execute(sqlQueries[1])
        con.commit()
        cur.execute("SELECT last_insert_rowid();")
        return cur.fetchall()[0][0]
    return None


def update(_id, _value, _type=None):
    global allForFetch, allForFetchByType
    if _type == None:
        _type = getMainWindow().Table.keyName
    if checkValues(_value, _type):
        allForFetch, allForFetchByType[_type] = None, None
        con = getDefaultConnection()
        cur = con.cursor()
        cur.execute(str("update " + tableName + " set value='" + correctForSql(_value) + "', type='" + correctForSql(
            _type) + "' where id=" + str(int(_id))))
        con.commit()


def delete(_id, _type=None):
    if _type == None:
        _type = getMainWindow().Table.keyName
    global allForFetch, allForFetchByType
    allForFetch, allForFetchByType[_type] = None, None
    con = getDefaultConnection()
    cur = con.cursor()
    cur.execute("delete from " + tableName + " where id=" + str(int(_id)))
    con.commit()


def getTableCreateQuery():
    return "CREATE TABLE IF NOT EXISTS " + tableName + " ('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,'value' TEXT,'type' TEXT)"


def getDeleteTableQuery():
    return "DELETE FROM " + tableName


def getDefaultsQueries():
    sqlQueries = []
    sqlQueries += getAmendedSQLInsertOrUpdateQueries(tableName, {
        "value": "'" + correctForSql("['File Name~|~-', '~||~', 'Artist~|~', 'Title~|~']") + "'", "type": "'music'"},
                                                     ["value"])
    sqlQueries += getAmendedSQLInsertOrUpdateQueries(tableName, {
        "value": "'" + correctForSql(
            "['Track No~|~', 'Concatenate-0~|~ - ', 'Title~|~', '~||~', 'File Name~|~']") + "'",
        "type": "'music'"}, ["value"])
    sqlQueries += getAmendedSQLInsertOrUpdateQueries(tableName, {
        "value": "'" + correctForSql("['Album~|~', '~||~', 'Directory~|~']") + "'", "type": "'music'"}, ["value"])
    sqlQueries += getAmendedSQLInsertOrUpdateQueries(tableName, {
        "value": "'" + correctForSql("['Directory~|~', '~||~', 'Album~|~']") + "'", "type": "'music'"}, ["value"])
    sqlQueries += getAmendedSQLInsertOrUpdateQueries(tableName, {
        "value": "'" + correctForSql("['Directory~|~-', '~||~', 'Artist~|~', 'Album~|~']") + "'", "type": "'music'"},
                                                     ["value"])
    sqlQueries += getAmendedSQLInsertOrUpdateQueries(tableName, {
        "value": "'" + correctForSql("['Directory~|~-', '~||~', 'Year~|~', 'Album~|~']") + "'", "type": "'music'"},
                                                     ["value"])
    sqlQueries += getAmendedSQLInsertOrUpdateQueries(tableName, {
        "value": "'" + correctForSql("['File Name~|~-', '~||~', 'Track No~|~', 'Title~|~']") + "'", "type": "'music'"},
                                                     ["value"])
    sqlQueries += getAmendedSQLInsertOrUpdateQueries(tableName, {
        "value": "'" + correctForSql("['Artist~|~', 'Concatenate-0~|~ + ', 'Title~|~', '~||~', 'File Name~|~']") + "'",
        "type": "'music'"}, ["value"])
    sqlQueries += getAmendedSQLInsertOrUpdateQueries(tableName, {
        "value": "'" + correctForSql("['File Name~|~', '~||~', 'Directory~|~']") + "'", "type": "'file'"}, ["value"])
    sqlQueries += getAmendedSQLInsertOrUpdateQueries(tableName, {
        "value": "'" + correctForSql("['Directory~|~', '~||~', 'File Name~|~']") + "'", "type": "'file'"}, ["value"])
    sqlQueries += getAmendedSQLInsertOrUpdateQueries(tableName, {
        "value": "'" + correctForSql("['Directory~|~', '~||~', 'File/Directory Name~|~']") + "'",
        "type": "'directory'"},
                                                     ["value"])
    sqlQueries += getAmendedSQLInsertOrUpdateQueries(tableName, {
        "value": "'" + correctForSql("['File/Directory Name~|~', '~||~', 'Directory~|~']") + "'",
        "type": "'directory'"},
                                                     ["value"])
    sqlQueries += getAmendedSQLInsertOrUpdateQueries(tableName, {
        "value": "'" + correctForSql("['Current Cover~|~', '~||~', 'Source Cover~|~']") + "'", "type": "'cover'"},
                                                     ["value"])
    sqlQueries += getAmendedSQLInsertOrUpdateQueries(tableName, {
        "value": "'" + correctForSql("['Current Cover~|~', '~||~', 'Destination Cover~|~']") + "'", "type": "'cover'"},
                                                     ["value"])
    sqlQueries += getAmendedSQLInsertOrUpdateQueries(tableName, {
        "value": "'" + correctForSql("['Directory Name~|~', '~||~', 'Destination Cover~|~']") + "'", "type": "'cover'"},
                                                     ["value"])
    return sqlQueries


def checkUpdates(_oldVersion):
    if _oldVersion < 4:
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

