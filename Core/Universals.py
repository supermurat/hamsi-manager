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
import os
from datetime import timedelta, datetime
from Core import Variables as var
import FileUtils as fu
from Core.MyObjects import *

MainWindow = None
isStartingSuccessfully = False
isStartedCloseProcess = False
MySettings = {}
loggingLevel = False
isShowVerifySettings = False
changedDefaultValuesKeys = []
newSettingsKeys = []
isCanBeShowOnMainWindow = False
windowMode = "Normal"
threadActionState = None
tableType = None
fileOfSettings = "mySettings.ini"
isRaisedAnError = False
Utf8Contents = {}

def __init__(self):
    pass

def setApp(_app):
    global HamsiManagerApp
    HamsiManagerApp = _app

def setMainWindow(_mainWindow):
    global MainWindow
    MainWindow = _mainWindow
    MainWindow.StateDialog = None
    MainWindow.StateDialogStateBar = None
    MainWindow.StateDialogTitle = None
    MainWindow.Menu = None
    MainWindow.Bars = None
    MainWindow.StatusBar = None
    MainWindow.ToolsBar = None
    MainWindow.TableToolsBar = None
    MainWindow.FileManager = None
    MainWindow.CentralWidget = None

def setPathOfSettingsDirectory(_path):
    _path = str(_path)
    if _path[-1]==os.sep:
        _path = _path[:-1]
    fu.pathOfSettingsDirectory = _path

def trUnicode(_s, _e = "utf-8"):
    if var.isPython3k:
        return _s
    if isinstance(_s, unicode):
        return _s
    return unicode(_s, _e)

def trDecode(_s, _e = "utf-8", _p = "strict"):
    if var.isPython3k:
        return _s
    return _s.decode(_e, _p)

def trDecodeList(_s, _e = "utf-8", _p = "strict"):
    if var.isPython3k:
        return _s
    sList =[]
    for x in _s:
        sList.append(trDecode(x, _e, _p))
    return sList

def trEncode(_s, _e = "utf-8", _p = "strict"):
    if var.isPython3k:
        return _s
    return _s.encode(_e, _p)

def trEncodeList(_s, _e = "utf-8", _p = "strict"):
    if var.isPython3k:
        return _s
    sList =[]
    for x in _s:
        sList.append(trEncode(x, _e, _p))
    return sList

def getUtf8Data(_key):
    global Utf8Contents
    try:
        if _key in Utf8Contents.keys():
            return Utf8Contents[_key]
        from Core import Utf8Content
        Utf8Contents[_key] = Utf8Content.getUtf8Data(_key)
        return Utf8Contents[_key]
    except Exception as err:
        printForDevelopers(str(err))
        if _key=="replacementChars":
            return {}
        else:
            if var.isPython3k:
                return ""
            else:
                return unicode("")

def fillMySettings(_setAgain=False, _isCheckUpdate=True):
    global MySettings, isShowVerifySettings, changedDefaultValuesKeys, newSettingsKeys, windowMode, tableType
    from Core import Settings
    sets = Settings.setting()
    settingVersion = trStr(sets.value("settingsVersion"))
    defaultValues = var.getDefaultValues()
    valueTypesAndValues = var.getValueTypesAndValues()
    for keyValue in var.keysOfSettings:
        value = trStr(sets.value(keyValue, trQVariant(defaultValues[keyValue])))
        if keyValue not in MySettings.keys() or _setAgain:
            MySettings[keyValue] = str(Settings.emendValue(keyValue, value, defaultValues[keyValue], valueTypesAndValues[keyValue]))
    for keyValue in sets.allKeys():
        keyValue = str(keyValue)
        if keyValue not in MySettings.keys():
            value = trStr(sets.value(keyValue, trQVariant("")))
            MySettings[keyValue] = str(Settings.emendValue(keyValue, value, "", "str"))
    newSettingVersion = str(MySettings["settingsVersion"])
    if _isCheckUpdate:
        if newSettingVersion!=settingVersion:
            newSettingsKeys, changedDefaultValuesKeys = Settings.updateOldSettings(settingVersion, newSettingVersion)
            isShowVerifySettings = True
    fu.fileSystemEncoding = MySettings["fileSystemEncoding"]
    windowMode = MySettings["windowMode"]
    fu.themePath = fu.joinPath(fu.HamsiManagerDirectory, "Themes", MySettings["themeName"])
    if tableType == None:
        tableType = MySettings["tableType"]
        if tableType not in var.tableTypesNames:
            tableType = "1"
    if getBoolValue("isInstalledKDE4Language")==False:
        from Core import MyConfigure
        MyConfigure.installKDE4Languages()

def getListFromListString(_listString, _splitter=None):
    if _splitter is None:
        listString = eval(str(_listString))
    else:
        listString = str(_listString).split(_splitter)
    if len(listString)==1:
        if listString[0].strip()=="":
            return []
    return listString

def getStringFromList(_list, _splitter=None):
    if _splitter is None:
        return str(_list)
    else:
        if isinstance(_list, (list, tuple, dict)):
            listString = ""
            for x, value in enumerate(_list):
                if x!=0:
                    listString += _splitter
                listString += value
            return listString
        else:
            return str(_list)

def getValue(_key, _defaultValue = ""):
    try:
        return MySettings[_key]
    except:
        from Core import Settings
        sets = Settings.setting()
        MySettings[_key] = str(trStr(sets.value(_key, trQVariant(_defaultValue))))
        return MySettings[_key]

def getDateValue(_key):
    return datetime.strptime(getValue(_key), "%Y %m %d %H %M %S")

def getBoolValue(_key, _defaultValue = ""):
    value = str(getValue(_key, _defaultValue)).title()
    if value=="True" or value=="1" or value=="2":
        return True
    return False

def getListValue(_key):
    return getListFromListString(getValue(_key))

def setMySetting(_key, _value):
    global MySettings
    MySettings[_key] = str(_value)

def saveSettings(_key=None):
    from Core.Settings import setting
    sets = setting()
    if _key==None:
        keys = MySettings.keys()
    else:
        keys = [_key]
    for value in keys:
        sets.setValue(value,trQVariant(MySettings[value]))

def activeWindow():
    if MApplication.activeModalWidget()!=None:
        return MApplication.activeModalWidget()
    else:
        return MainWindow

def startThreadAction():
    global threadActionState
    threadActionState = True

def cancelThreadAction():
    global threadActionState
    from Core import Dialogs
    answer = Dialogs.ask(translate("Universals", "Are You Sure?"),
                        translate("Universals", "Are you want to cancel these transactions?"))
    if answer==Dialogs.Yes:
        threadActionState = False

def finishThreadAction():
    global threadActionState
    threadActionState = None

def isContinueThreadAction():
    return threadActionState

def printForDevelopers(_message):
    import logging
    if loggingLevel==logging.DEBUG:
        print (str(_message))

def getLastPathByEvent(_keyPath, _defaultPath):
    from Core import Settings
    sets = Settings.settingForPaths()
    return str(trStr(sets.value(_keyPath, trQVariant(_defaultPath))))

def setLastPathByEvent(_keyPath, _path):
    from Core import Settings
    sets = Settings.settingForPaths()
    sets.setValue(_keyPath, trQVariant(_path))

def getLastPathKey(_caption, _directory, _filter, _isUseLastPathKeyType=1, _lastPathKey=None):
    pathKey = None
    if _isUseLastPathKeyType==0: pass
    elif _isUseLastPathKeyType==1: pathKey = _caption
    elif _isUseLastPathKeyType==2: pathKey = _caption + " - " + _directory
    elif _isUseLastPathKeyType==3: pathKey = _directory
    elif _isUseLastPathKeyType==4 and _lastPathKey is not None: pathKey = _caption + " - " + _lastPathKey
    elif _isUseLastPathKeyType==5 and _lastPathKey is not None: pathKey = _caption + " - " + _directory + " - " + _lastPathKey
    elif _isUseLastPathKeyType==6 and _lastPathKey is not None: pathKey = _directory + " - " + _lastPathKey
    else: pathKey = _isUseLastPathKeyType
    return pathKey






