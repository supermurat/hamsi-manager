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
from Core.MyObjects import *
import FileUtils as fu
from Databases import sqlite, getDefaultConnection, getAllDatabases, getDBPropertiesCreateQuery, reFillDatabases, getAmendedSQLInsertOrUpdateQueries, checkDatabases
from Databases import BookmarksOfDirectories, BookmarksOfSpecialTools, SearchAndReplaceTable, CompleterTable

def getSettings(_settingsFilePath):
    return MQtCore.QSettings(Universals.trForUI(_settingsFilePath), MQtCore.QSettings.IniFormat)

def setting():
    return getSettings(fu.joinPath(fu.pathOfSettingsDirectory, Universals.fileOfSettings))

def settingForPaths():
    return getSettings(fu.joinPath(fu.pathOfSettingsDirectory, "paths.ini"))

def universalSetting():
    return getSettings(fu.joinPath(fu.userDirectoryPath, ".HamsiApps", "universalSettings.ini"))

def checkSettings():
    if fu.isDir(fu.pathOfSettingsDirectory)==False:
        fu.makeDirs(fu.pathOfSettingsDirectory)
        reFillSettings()
        reFillDatabases()
    else:
        if fu.isFile(fu.joinPath(fu.pathOfSettingsDirectory, "database.sqlite"))==False:
            reFillDatabases()
        if fu.isFile(fu.joinPath(fu.pathOfSettingsDirectory, Universals.fileOfSettings))==False:
            reFillSettings()
        checkDatabases()

def saveUniversalSettings():
    from Core import Execute
    mySetting = universalSetting()
    keysOfUniversalSettings = ["HamsiManagerPath"]
    values = [Execute.findExecutablePath("HamsiManager")]
    for x, keyValue in enumerate(keysOfUniversalSettings):
        if Universals.trStr(mySetting.value(keyValue)) != values[x]:
            mySetting.setValue(keyValue, Universals.trQVariant(values[x]))

def getUniversalSetting(_key, _defaultValue):
    mySetting = universalSetting()
    value = str(Universals.trStr(mySetting.value(_key)))
    if value == "":
        value = _defaultValue
    return value

def setUniversalSetting(_key, _value):
    mySetting = universalSetting()
    mySetting.setValue(_key, Universals.trQVariant(_value))

def reFillSettings(_makeBackUp=False):
    if _makeBackUp==True:
        makeBackUp("Settings")
    mySetting = setting()
    mySetting.clear()

def emendValue(_keyOfSetting, _value, _defaultValue = None, _valueTypesAndValue = None):
    if _valueTypesAndValue==None:
        _valueTypesAndValue = Variables.getValueTypesAndValues()[_keyOfSetting]
    if _defaultValue==None:
        _defaultValue = Variables.getDefaultValues()[_keyOfSetting]
    if _valueTypesAndValue=="bool":
        try:
            eval(str(_value).title())
        except:
            return _defaultValue
    elif _valueTypesAndValue == "date":
        from datetime import datetime
        try:
            datetime.strptime(str(_value), "%Y %m %d %H %M %S")
        except:
            return _defaultValue
    elif _valueTypesAndValue=="list":
        try:
            value = "['"
            for x, ext in enumerate(Universals.getListFromListString(_value)):
                if ext!="":
                    if x!=0:
                        value += "','"
                    value += ext
            value+="']"
            _value = value
        except:
            return _defaultValue
    elif _valueTypesAndValue=="int":
        try:
            int(_value)
        except:
            return _defaultValue
    elif _valueTypesAndValue[0]=="int":
        try:
            if _valueTypesAndValue[1].index(int(_value))==-1:
                return _defaultValue
        except:
            return _defaultValue
    elif _valueTypesAndValue[0]=="intList":
        try:
            value = "['"
            for x, ext in enumerate(Universals.getListFromListString(_value)):
                if ext!="":
                    if _valueTypesAndValue[1].index(int(ext))!=-1:
                        if x!=0:
                            value += "','"
                        value += ext
            value+="']"
            _value = value
        except:
            return _defaultValue
    elif _valueTypesAndValue[0]=="intOptions":
        try:
            if _valueTypesAndValue[1].index(int(_value))==-1:
                return _defaultValue
        except:
            return _defaultValue
    elif _valueTypesAndValue[0]=="options":
        try:
            if _valueTypesAndValue[1].index(str(_value))==-1:
                return _defaultValue
        except:
            return _defaultValue
    return _value

def reFillAll(_makeBackUp=False):
    if _makeBackUp==True:
        makeBackUp("All")
    reFillDatabases()
    reFillSettings()

def makeBackUp(_settingType="All", _backUpDirectory="BackUps", _newFileName="mirror"):
    files = []
    if _settingType=="database" or _settingType=="All":
        files.append("database.sqlite")
    if _settingType=="Settings" or _settingType=="All":
        files.append(Universals.fileOfSettings)
    if fu.isDir(fu.joinPath(fu.pathOfSettingsDirectory, _backUpDirectory))==False:
        fu.makeDirs(fu.joinPath(fu.pathOfSettingsDirectory, _backUpDirectory))
    isReturn = False
    for file in files:
        if _newFileName=="mirror":
            newFileName = file
        elif _newFileName=="random":
            isReturn = True
            import random
            while 1==1:
                newFileName = file[:file.find(".")] +"_"+ str(random.randrange(0, 100000000))+file[file.find("."):]
                if fu.isFile(fu.joinPath(fu.pathOfSettingsDirectory, _backUpDirectory, newFileName))==False:
                    break
        else:
            newFileName = _newFileName
        if fu.isFile(fu.joinPath(fu.pathOfSettingsDirectory, _backUpDirectory, newFileName)):
            fu.removeFile(fu.joinPath(fu.pathOfSettingsDirectory, _backUpDirectory, newFileName))
        try:
            fu.copyFileOrDir(fu.joinPath(fu.pathOfSettingsDirectory, file), fu.joinPath(fu.pathOfSettingsDirectory, _backUpDirectory, newFileName))
            if isReturn==True:
                return newFileName
        except:pass

def restoreBackUp(_settingType="All", _isMakeBackUp=True):
    files = []
    isSuccesfully = True
    if _settingType=="database" or _settingType=="All":
        files.append("database.sqlite")
    if _settingType=="Settings" or _settingType=="All":
        files.append(Universals.fileOfSettings)
    for file in files:
        if _isMakeBackUp==True:
            oldInfo = fu.readFromFile(fu.joinPath(fu.pathOfSettingsDirectory, file))
        else:
            try:
                fu.removeFile(fu.joinPath(fu.pathOfSettingsDirectory, file))
            except:pass
        try:
            if fu.isFile(fu.joinPath(fu.pathOfSettingsDirectory, "BackUps", file)):
                fu.moveFileOrDir(fu.joinPath(fu.pathOfSettingsDirectory, "BackUps", file), fu.joinPath(fu.pathOfSettingsDirectory, file))
            else:
                isSuccesfully = False
        except:pass
        if _isMakeBackUp==True:
            fu.writeToFile(fu.joinPath(fu.pathOfSettingsDirectory, "BackUps", file), oldInfo)
    return isSuccesfully

def saveStateOfSettings(_file):
    from Core import MyConfigure
    newFile = makeBackUp("Settings", "SettingFiles", "random")
    info = MyConfigure.getConfiguredDesktopFileContent()
    newInfo = []
    for row in info.split("\n"):
        if row [:4]=="Exec":
            row  = row + " -s SettingFiles" + fu.sep + newFile
        newInfo.append(row )
    info = ""
    for row in newInfo:
        info += row + "\n"
    fu.writeToFile(_file, info)

def openStateOfSettings(_file):
    from Core import Execute
    for rowNo, row in enumerate(fu.readLinesFromFile(_file)):
        if row [:5]=="Exec=":
            t = Execute.executeStringCommand(row[5:])
            Universals.HamsiManagerApp.closeAllWindows()
            break

def updateOldSettings(_oldVersion, _newVersion):
    newSettingsKeys, changedDefaultValuesKeys = [], []
    try:
        oldVersion = int(_oldVersion)
    except:
        oldVersion = _newVersion
    if oldVersion<810:
        con = sqlite.connect(fu.joinPath(fu.pathOfSettingsDirectory, "searchAndReplaceTable.sqlite"))
        cur = con.cursor()
        cur.execute(str("ALTER TABLE searchAndReplaceTable RENAME TO tmpSearchAndReplaceTable;"))
        cur.execute(str("CREATE TABLE searchAndReplaceTable ('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,'searching' TEXT,'replacing' TEXT,'intIsActive' INTEGER,'intIsRegExp' INTEGER);"))
        cur.execute(str("INSERT INTO searchAndReplaceTable(searching,replacing,intIsActive,intIsRegExp) SELECT searching,replacing,1,0 FROM tmpSearchAndReplaceTable;"))
        cur.execute(str("DROP TABLE tmpSearchAndReplaceTable;"))
        con.commit()
    if oldVersion<811:
        con = sqlite.connect(fu.joinPath(fu.pathOfSettingsDirectory, "searchAndReplaceTable.sqlite"))
        cur = con.cursor()
        cur.execute(str("ALTER TABLE searchAndReplaceTable RENAME TO tmpSearchAndReplaceTable;"))
        cur.execute(str("CREATE TABLE searchAndReplaceTable ('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,'searching' TEXT,'replacing' TEXT,'intIsActive' INTEGER,'intIsCaseSensitive' INTEGER,'intIsRegExp' INTEGER);"))
        cur.execute(str("INSERT INTO searchAndReplaceTable(searching,replacing,intIsActive,intIsCaseSensitive,intIsRegExp) SELECT searching,replacing,1,1,0 FROM tmpSearchAndReplaceTable;"))
        cur.execute(str("DROP TABLE tmpSearchAndReplaceTable;"))
        con.commit()
    if oldVersion<818:
        newSettingsKeys = newSettingsKeys + ["isAutoCleanSubFolderWhenClear", "isClearEmptyDirectoriesWhenClear", "cleanerUnneededDirectories", "cleanerUnneededFiles", "cleanerUnneededFileExtensions"]
        changedDefaultValuesKeys = changedDefaultValuesKeys + ["packagerUnneededFileExtensions", "packagerUnneededFiles", "packagerUnneededDirectories"]
    if oldVersion<819:
        newSettingsKeys = newSettingsKeys + ["isClearEmptyDirectoriesWhenSave", "isClearEmptyDirectoriesWhenMoveOrChange", "isClearEmptyDirectoriesWhenCopyOrChange", "isClearEmptyDirectoriesWhenFileMove", "isAutoCleanSubFolderWhenSave", "isAutoCleanSubFolderWhenMoveOrChange", "isAutoCleanSubFolderWhenCopyOrChange", "isAutoCleanSubFolderWhenFileMove", "isAutoMakeIconToDirectoryWhenSave", "isAutoMakeIconToDirectoryWhenMoveOrChange", "isAutoMakeIconToDirectoryWhenCopyOrChange", "isAutoMakeIconToDirectoryWhenFileMove"]
    if oldVersion<820:
        if fu.isFile(fu.joinPath(fu.pathOfSettingsDirectory, "LastState")):
            fu.removeFile(fu.joinPath(fu.pathOfSettingsDirectory, "LastState"))
    if oldVersion<821:
        newSettingsKeys = newSettingsKeys + ["isDeleteEmptyDirectories", "isCleanerDeleteEmptyDirectories", "isPackagerDeleteEmptyDirectories"]
    if oldVersion<822:
        if Variables.isAvailableKDE4():
            KDE4HomePath = Variables.getKDE4HomePath()
            if fu.isFile(fu.joinPath(KDE4HomePath, "share", "config", "HamsiManagerrc")):
                fu.removeFile(fu.joinPath(KDE4HomePath, "share", "config", "HamsiManagerrc"))
    if oldVersion<840:
        try:
            con = sqlite.connect(fu.joinPath(fu.pathOfSettingsDirectory, "bookmarks.sqlite"))
            cur = con.cursor()
            cur.execute("SELECT * FROM dbProperties where keyName='version'")
            bookmarksDBVersion = int(cur.fetchall()[0][1])
        except:
            bookmarksDBVersion = 0
        try:
            con = sqlite.connect(fu.joinPath(fu.pathOfSettingsDirectory, "searchAndReplaceTable.sqlite"))
            cur = con.cursor()
            cur.execute("SELECT * FROM dbProperties where keyName='version'")
            searchAndReplaceTableDBVersion = int(cur.fetchall()[0][1])
        except:
            searchAndReplaceTableDBVersion = 0
        if bookmarksDBVersion<1:
            con = sqlite.connect(fu.joinPath(fu.pathOfSettingsDirectory, "bookmarks.sqlite"))
            cur = con.cursor()
            cur.execute(str("CREATE TABLE dbProperties ('keyName' TEXT NOT NULL,'value' TEXT);"))
            cur.execute(str("insert into dbProperties (keyName, value) values ('version', '1');"))
            con.commit()
        if searchAndReplaceTableDBVersion<1:
            con = sqlite.connect(fu.joinPath(fu.pathOfSettingsDirectory, "searchAndReplaceTable.sqlite"))
            cur = con.cursor()
            cur.execute(str("CREATE TABLE dbProperties ('keyName' TEXT NOT NULL,'value' TEXT);"))
            cur.execute(str("insert into dbProperties (keyName, value) values ('version', '1');"))
            con.commit()
    if oldVersion<853:
        newSettingsKeys = newSettingsKeys + ["isShowTransactionDetails"]
    if oldVersion<860:
        newSettingsKeys = newSettingsKeys + ["windowMode"]
    if oldVersion<867:
        newSettingsKeys = newSettingsKeys + ["isAskIfHasManyImagesInAlbumDirectory"]
        Universals.setMySetting("isShowReconfigureWizard", True)
    if oldVersion<890:
        con = sqlite.connect(fu.joinPath(fu.pathOfSettingsDirectory, "bookmarks.sqlite"))
        cur = con.cursor()
        cur.execute(str("insert into bookmarksOfSpecialTools (bookmark, value, label) values ('', 'Directory Name , Directory  ;right;102', 'cover')"))
        cur.execute(str("insert into bookmarksOfSpecialTools (bookmark, value, label) values ('', 'Source Cover , Current Cover  ;right;102', 'cover')"))
        cur.execute(str("insert into bookmarksOfSpecialTools (bookmark, value, label) values ('', 'Destination Cover , Source Cover  ;right;102', 'cover')"))
        cur.execute(str("insert into bookmarksOfSpecialTools (bookmark, value, label) values ('', 'Destination Cover , Current Cover  ;right;102', 'cover')"))
        con.commit()
    if oldVersion<905:
        conNewDB = getDefaultConnection()
        con = sqlite.connect(fu.joinPath(fu.pathOfSettingsDirectory, "bookmarks.sqlite"))
        cur = con.cursor()
        cur.execute("SELECT bookmark,value FROM bookmarksOfDirectories")
        for row in cur.fetchall():
            cur = conNewDB.cursor()
            sqlCommands = getAmendedSQLInsertOrUpdateQueries("bookmarksOfDirectories", {"bookmark" : "'" + row[0] + "'", "value" : "'" + row[1] + "'"}, ["value"])
            for sqlCommand in sqlCommands:
                cur.execute(str(sqlCommand))
            conNewDB.commit()
        con = sqlite.connect(fu.joinPath(fu.pathOfSettingsDirectory, "bookmarks.sqlite"))
        cur = con.cursor()
        cur.execute("SELECT bookmark,value,label FROM bookmarksOfSpecialTools")
        for row in cur.fetchall():
            cur = conNewDB.cursor()
            sqlCommands = getAmendedSQLInsertOrUpdateQueries("bookmarksOfSpecialTools", {"bookmark" : "'" + row[0] + "'", "value" : "'" + row[1] + "'", "type" : "'" + row[2] + "'"}, ["value"])
            for sqlCommand in sqlCommands:
                cur.execute(str(sqlCommand))
            conNewDB.commit()
        con = sqlite.connect(fu.joinPath(fu.pathOfSettingsDirectory, "/searchAndReplaceTable.sqlite"))
        cur = con.cursor()
        cur.execute("SELECT searching,replacing,intIsActive,intIsCaseSensitive,intIsRegExp FROM searchAndReplaceTable")
        for row in cur.fetchall():
            cur = conNewDB.cursor()
            sqlCommands = getAmendedSQLInsertOrUpdateQueries("searchAndReplaceTable", {"searching" : "'" + row[0] + "'", "replacing" : "'" + row[1] + "'", "intIsActive" : str(row[2]), "intIsCaseSensitive" : str(row[3]), "intIsRegExp" : str(row[4])}, ["searching", "replacing"])
            for sqlCommand in sqlCommands:
                cur.execute(str(sqlCommand))
            conNewDB.commit()
    if oldVersion<906:
        sets = setting()
        sets.setValue("fileSystemEncoding", Universals.trQVariant(Universals.trStr(sets.value("systemsCharSet"))))
    if oldVersion<907:
        newSettingsKeys = newSettingsKeys + ["isActiveCompleter", "isShowAllForCompleter"]
    if oldVersion<908:
        newSettingsKeys = newSettingsKeys + ["isActiveClearGeneral"]
    if oldVersion<961:
        newSettingsKeys = newSettingsKeys + ["colorSchemes", "isActiveAutoMakeIconToDirectory",
              "isDontDeleteFileAndDirectory", "pathOfDeletedFilesAndDirectories"]
    if oldVersion<962:
        newSettingsKeys = newSettingsKeys + ["isResizeTableColumnsToContents"]
    if oldVersion<990:
        newSettingsKeys = newSettingsKeys + ["validSentenceStructureForDirectory", "isShowHiddensInSubFolderTable", "isShowHiddensInFolderTable", "isShowHiddensInFileTable", "isShowHiddensInMusicTable", "isShowHiddensInCoverTable", "isShowHiddensInFileTree", "isAppendFileSizeToFileTree", "isAppendLastModifiedToFileTree"]
    if oldVersion<991:
        newSettingsKeys = newSettingsKeys + ["isDecodeURLStrings"]
    if oldVersion<1081:
        newSettingsKeys = newSettingsKeys + ["isCheckUnSavedValues"]
    if oldVersion<1082:
        con = sqlite.connect(fu.joinPath(fu.pathOfSettingsDirectory, "database.sqlite"))
        cur = con.cursor()
        cur.execute(str("ALTER TABLE searchAndReplaceTable RENAME TO tmpSearchAndReplaceTable;"))
        cur.execute(str("CREATE TABLE searchAndReplaceTable ('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,'label' TEXT,'searching' TEXT,'replacing' TEXT,'intIsActive' INTEGER,'intIsCaseSensitive' INTEGER,'intIsRegExp' INTEGER);"))
        cur.execute(str("INSERT INTO searchAndReplaceTable(label,searching,replacing,intIsActive,intIsCaseSensitive,intIsRegExp) SELECT searching,searching,replacing,intIsActive,intIsCaseSensitive,intIsRegExp FROM tmpSearchAndReplaceTable;"))
        cur.execute(str("DROP TABLE tmpSearchAndReplaceTable;"))
        con.commit()
        newSettingsKeys = newSettingsKeys + ["isCorrectValueWithSearchAndReplaceTable"]
    if oldVersion<1170:
        newSettingsKeys = newSettingsKeys + ["maxDeletedDirectorySize"]
    if oldVersion<1190:
        changedDefaultValuesKeys = changedDefaultValuesKeys + ["applicationStyle", "windowMode", "fileExtesionIs"]
    return newSettingsKeys, changedDefaultValuesKeys

