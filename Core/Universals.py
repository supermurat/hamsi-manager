## This file is part of HamsiManager.
## 
## Copyright (c) 2010 Murat Demir <mopened@gmail.com>      
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
from os import path
from datetime import timedelta, datetime
import Variables

class Universals():
    global MainWindow, HamsiManagerApp, MySettings, setMySetting, saveSettings, isStartingSuccessfully, loggingLevel, fillMySettings, activeWindow, isShowVerifySettings, themePath, getListFromStrint, changedDefaultValuesKeys, newSettingsKeys, isCanBeShowOnMainWindow, getDateValue, isActivePyKDE4, isLoadedMyObjects, getBoolValue, windowMode, isChangeAll, isChangeSelected, tableTypesNames, tableType, getThisTableType, fillUIUniversals, clearAllChilds, threadActionState, startThreadAction, cancelThreadAction, finishThreadAction, isContinueThreadAction, printForDevelopers, isStartedCloseProcces, getStrintFromList, iconNameFormatLabels, pathOfSettingsDirectory, fileOfSettings, setPathOfSettingsDirectory, recordFilePath, translate, isRaisedAnError, trForM, trStr, trQVariant, getUtf8Data, trUnicode, trDecode, trEncode, getValue
    MainWindow = None 
    isStartingSuccessfully = False
    isStartedCloseProcces = False
    MySettings = {}
    loggingLevel = False
    isShowVerifySettings = False
    changedDefaultValuesKeys = []
    newSettingsKeys = []
    themePath = Variables.HamsiManagerDirectory + "/Themes/Default"
    isCanBeShowOnMainWindow = False
    isActivePyKDE4 = False
    isLoadedMyObjects = False
    windowMode = "Normal"
    isChangeAll = None
    isChangeSelected = None
    threadActionState = None
    tableTypesNames = ["0", "1", "2", "3", "4", "5", "6"]
    tableType = None
    iconNameFormatLabels = Variables.iconNameFormatKeys
    pathOfSettingsDirectory = Variables.userDirectoryPath+"/.HamsiApps/HamsiManager"
    fileOfSettings = "mySettings.ini"
    recordFilePath = pathOfSettingsDirectory + "/logs.txt"
    isRaisedAnError = False
    if Variables.executableHamsiManagerPath.find("HamsiManager")==-1 or Variables.executableHamsiManagerPath.find("./HamsiManager")!=-1:
        Variables.executableHamsiManagerPath = Variables.HamsiManagerDirectory + "/HamsiManager.py"
    
    def __init__(self, _app, _main):
        global MainWindow, HamsiManagerApp
        HamsiManagerApp = _app
        MainWindow = _main
    
    def setPathOfSettingsDirectory(_path):
        global pathOfSettingsDirectory
        _path = str(_path)
        if _path[-1]=="/":
            _path = _path[:-1]
        pathOfSettingsDirectory = _path
    
    def translate(_p, _s):
        try:
            return Variables.MQtGui.QApplication.translate(_p, _s)
        except:
            try:return _s.decode("utf-8")
            except: return _s
            
    def trForM(_s):
        _s = str(_s)
        return _s
        
    def trStr(_s):
        if Variables.isPython3k:
            return _s
        return _s.toString()
        
    def trUnicode(_s, _e = "utf-8"):
        if Variables.isPython3k:
            return _s
        if isinstance(_s, unicode):
            return _s
        return unicode(_s, _e)
        
    def trDecode(_s, _e = "utf-8", _p = "strict"):
        if Variables.isPython3k:
            return _s
        return _s.decode(_e, _p)
        
    def trEncode(_s, _e = "utf-8", _p = "strict"):
        if Variables.isPython3k:
            return _s
        return _s.encode(_e, _p)
        
    def getUtf8Data(_key):
        try:
            import Utf8Content
            return Utf8Content.getUtf8Data(_key)
        except Exception as err:
            printForDevelopers(str(err))
            if _key=="replacementChars":
                return {}
            else:
                if Variables.isPython3k:
                    return ""
                else:
                    return unicode("")
        
    def trQVariant(_s):
        if Variables.isPython3k:
            return _s
        return Variables.MQtCore.QVariant(_s)
        
    def fillMySettings(_setAgain=False, _isCheckUpdate=True, _isActiveKDE4=None):
        global MySettings, isShowVerifySettings, themePath, changedDefaultValuesKeys, newSettingsKeys, isActivePyKDE4, windowMode, tableType, isChangeAll, isChangeSelected
        import Settings, InputOutputs
        sets = Settings.setting()
        settingVersion = trStr(sets.value("settingsVersion"))
        defaultValues = Variables.getDefaultValues()
        valueTypesAndValues = Variables.getValueTypesAndValues()
        for keyValue in Variables.keysOfSettings:
            value = trStr(sets.value(keyValue, trQVariant(trForM(defaultValues[keyValue]))))
            if keyValue not in MySettings.keys() or _setAgain:
                MySettings[keyValue] = str(Settings.emendValue(keyValue, value, defaultValues[keyValue], valueTypesAndValues[keyValue]))
        newSettingVersion = str(MySettings["settingsVersion"])
        if _isCheckUpdate:
            if newSettingVersion!=settingVersion:
                newSettingsKeys, changedDefaultValuesKeys = Settings.updateOldSettings(settingVersion)
                isShowVerifySettings = True
        if _isActiveKDE4!=False:
            InputOutputs.fileSystemEncoding = MySettings["fileSystemEncoding"]
            if Variables.isAvailableKDE4():
                if getBoolValue("isActivePyKDE4"):
                    if Variables.isAvailablePyKDE4():
                        if isLoadedMyObjects==False:
                            isActivePyKDE4 = True
                    else:
                        MySettings["isActivePyKDE4"] = "False"
        windowMode = MySettings["windowMode"]
        themePath = Variables.HamsiManagerDirectory + "/Themes/" + MySettings["themeName"]
        if tableType == None:
            tableType = int(MySettings["tableType"])
            if tableType<0 or tableType>=len(tableTypesNames) or tableType==3:
                tableType = 1
        if isChangeAll == None:
            isChangeAll = getBoolValue("isChangeAll")
            isChangeSelected = getBoolValue("isChangeSelected")
        if getBoolValue("isInstalledKDE4Language")==False:
            import MyConfigure
            MyConfigure.installKDE4Languages()
    
    def getListFromStrint(_listString):
        listString = eval(str(_listString))
        if len(listString)==1:
            if listString[0].strip()=="":
                return []
        return listString
        
    def getStrintFromList(_list):
        listString = ""
        for x, value in enumerate(_list):
            if value!=0:
                listString += ";"
            listString += value
        return listString
        
    def getValue(_key, _valueList = None, _defaultValue = ""):
        try:
            return MySettings[_key]
        except:
            import Settings
            sets = Settings.setting()
            MySettings[_key] = str(trStr(sets.value(_key, trQVariant(trForM(_defaultValue)))))
            if _valueList != None:
                if MySettings[_key] in _valueList:
                    return MySettings[_key]
                else:
                    if _defaultValue!="":
                        MySettings[_key] = str(_defaultValue)
                        return MySettings[_key]
                    else:
                        MySettings[_key] = str(_valueList[0])
                        return MySettings[_key]
            else:
                return MySettings[_key]
    
    def getDateValue(_key):
        return datetime.strptime(MySettings[_key], "%Y %m %d %H %M %S")
    
    def getBoolValue(_key):
        if eval(MySettings[_key].title())==True:
            return True
        return False
     
    def setMySetting(_key, _value):
        global MySettings
        MySettings[_key] = str(_value)
        
    def saveSettings(_key=None):
        from Settings import setting
        sets = setting()
        if _key==None:
            keys = MySettings.keys()
        else:
            keys = [_key]
        for value in keys:
            sets.setValue(value,trQVariant(trForM(MySettings[value])))

    def activeWindow():
        from MyObjects import MApplication
        if MApplication.activeModalWidget()!=None:
            return MApplication.activeModalWidget()
        else:
            return MainWindow
        
    def getThisTableType(_tableType):
        try:
            tt = int(_tableType)
            if tt<0 or tt>=len(tableTypesNames):
                tt = 1
        except:
            try:
                for x, name in enumerate(tableTypesNames):
                    if str(name) == str(_tableType):
                        return x
                tt = 1
            except:
                    tt = 1
        return tt
        
    def fillUIUniversals():
        global tableTypesNames, iconNameFormatLabels
        from MyObjects import translate
        tableTypesNames = [translate("Tables", "Folder Table"), 
                            translate("Tables", "File Table"), 
                            translate("Tables", "Music Table"), 
                            translate("Tables", "Subfolder Table"), 
                            translate("Tables", "Cover Table"), 
                            translate("Tables", "Amarok Cover Table"), 
                            translate("Tables", "Amarok Music Table")
                            ]
        iconNameFormatLabels = [translate("Universals", "%Artist%"), 
                            translate("Universals", "%Album%"), 
                            translate("Universals", "%Year%"), 
                            translate("Universals", "%Genre%")]
        from InputOutputs import IA #For first import
            
    def clearAllChilds(_object, _isClearThis=False):
        childs = _object.children()
        for child in childs:
            clearAllChilds(child, True)
        if _isClearThis:
            try:
                _object.hide()
                _object.deleteLater()
            except:pass
                            
    def startThreadAction():
        global threadActionState
        threadActionState = True
        
    def cancelThreadAction():
        global threadActionState
        import Dialogs
        from MyObjects import translate
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
        
    
        
        
        
        
        
        
