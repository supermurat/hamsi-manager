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


from Core import Variables as var
from Core import Universals as uni
from Core.MyObjects import *
import FileUtils as fu
from Databases import sqlite, getDefaultConnection, reFillDatabases, getAmendedSQLInsertOrUpdateQueries, checkDatabases

def getSettings(_settingsFilePath):
    return MQtCore.QSettings(str(_settingsFilePath), MQtCore.QSettings.IniFormat)

def setting():
    return getSettings(fu.joinPath(fu.pathOfSettingsDirectory, uni.fileOfSettings))

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
        if fu.isFile(fu.joinPath(fu.pathOfSettingsDirectory, uni.fileOfSettings))==False:
            reFillSettings()
        checkDatabases()

def saveUniversalSettings():
    from Core import Execute
    mySetting = universalSetting()
    keysOfUniversalSettings = ["HamsiManagerPath"]
    values = [Execute.findExecutablePath("HamsiManager")]
    for x, keyValue in enumerate(keysOfUniversalSettings):
        if trStr(mySetting.value(keyValue)) != values[x]:
            mySetting.setValue(keyValue, trQVariant(values[x]))

def getUniversalSetting(_key, _defaultValue):
    mySetting = universalSetting()
    value = str(trStr(mySetting.value(_key)))
    if value == "":
        value = _defaultValue
    return value

def setUniversalSetting(_key, _value):
    mySetting = universalSetting()
    mySetting.setValue(_key, trQVariant(_value))

def reFillSettings(_makeBackUp=False):
    if _makeBackUp==True:
        makeBackUp("Settings")
    mySetting = setting()
    mySetting.clear()

def emendValue(_keyOfSetting, _value, _defaultValue = None, _valueTypesAndValue = None):
    if _valueTypesAndValue==None:
        _valueTypesAndValue = var.getValueTypesAndValues()[_keyOfSetting]
    if _defaultValue==None:
        _defaultValue = var.getDefaultValues()[_keyOfSetting]
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
            for x, ext in enumerate(uni.getListFromListString(_value)):
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
            for x, ext in enumerate(uni.getListFromListString(_value)):
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
        files.append(uni.fileOfSettings)
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
        files.append(uni.fileOfSettings)
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
            uni.HamsiManagerApp.closeAllWindows()
            break

def updateOldSettings(_oldVersion, _newVersion):
    newSettingsKeys, changedDefaultValuesKeys = [], []
    try:
        oldVersion = int(_oldVersion)
    except:
        oldVersion = _newVersion
    if oldVersion < 1000:
        reFillAll(True)
        return newSettingsKeys, changedDefaultValuesKeys
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
        changedDefaultValuesKeys = changedDefaultValuesKeys + ["applicationStyle", "windowMode", "fileExtensionIs"]
    if oldVersion < 1371:
        changedDefaultValuesKeys = changedDefaultValuesKeys + ["fileExtensionIs"]
    return newSettingsKeys, changedDefaultValuesKeys

