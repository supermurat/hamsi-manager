# -*- coding: utf-8 -*-

import sys
from os import path
from datetime import timedelta, datetime
import Variables

class Universals():
    global MainWindow, HamsiManagerApp, MySettings, setMySetting, saveSettings, isStartingSuccessfully, isDebugMode, fillMySettings, activeWindow, isShowVerifySettings, themePath, getListFromStrint, changedDefaultValuesKeys, newSettingsKeys, isCanBeShowOnMainWindow, getDateValue, isActivePyKDE4, isLoadedMyObjects, getBoolValue, windowMode, isShowOldValues, isChangeAll, isChangeSelected, tableTypesNames, tableType, getThisTableType, fillUIUniversals, isDeveloperMode, clearAllChilds, threadActionState, startThreadAction, cancelThreadAction, finishThreadAction, isContinueThreadAction, printForDevelopers, isStartedCloseProcces, getStrintFromList, iconNameFormatLabels, checkMysqldSafe, pathOfSettingsDirectory, fileOfSettings, setPathOfSettingsDirectory, recordFilePath, translate
    MainWindow = None 
    isStartingSuccessfully = False
    isStartedCloseProcces = False
    MySettings = {}
    isDebugMode = False
    isDeveloperMode = False
    isShowVerifySettings = False
    changedDefaultValuesKeys = []
    newSettingsKeys = []
    themePath = Variables.HamsiManagerDirectory + "/Themes/Default"
    isCanBeShowOnMainWindow = False
    isActivePyKDE4 = False
    isLoadedMyObjects = False
    windowMode = "Normal"
    isShowOldValues = None
    isChangeAll = None
    isChangeSelected = None
    threadActionState = None
    tableTypesNames = ["", "", "", "", ""]
    tableType = None
    iconNameFormatLabels = Variables.iconNameFormatKeys
    pathOfSettingsDirectory = Variables.userDirectoryPath+"/.HamsiApps/HamsiManager"
    fileOfSettings = "mySettings.ini"
    recordFilePath = pathOfSettingsDirectory + "/logs.txt"
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
        try:return Variables.MQtGui.MApplication.translate(_p, _s)
        except:
            try:return _s.decode("utf-8")
            except: return _s
        
    def fillMySettings(_setAgain=False, _isCheckUpdate=True, _isActiveKDE4=None):
        global MySettings, isShowVerifySettings, themePath, changedDefaultValuesKeys, newSettingsKeys, isActivePyKDE4, windowMode, tableType, isShowOldValues, isChangeAll, isChangeSelected
        import Settings, InputOutputs
        sets = Settings.setting()
        settingVersion = str(sets.value("settingsVersion").toString())
        defaultValues = Variables.getDefaultValues()
        valueTypesAndValues = Variables.getValueTypesAndValues()
        for keyValue in Variables.keysOfSettings:
            value = sets.value(keyValue, Variables.MQtCore.QVariant(defaultValues[keyValue].decode("utf-8"))).toString()
            if MySettings.keys().count(keyValue)==0 or _setAgain:
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
                InputOutputs.isMoveToTrash = getBoolValue("isMoveToTrash")
        windowMode = MySettings["windowMode"]
        themePath = Variables.HamsiManagerDirectory + "/Themes/" + MySettings["themeName"]
        if tableType == None:
            tableType = int(MySettings["tableType"])
            if tableType<0 or tableType>=len(tableTypesNames) or tableType==3:
                tableType = 1
        if isShowOldValues == None:
            isShowOldValues = getBoolValue("isShowOldValues")
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
        from MyObjects import MVariant
        from Settings import setting
        sets = setting()
        if _key==None:
            keys = Variables.keysOfSettings
        else:
            keys = [_key]
        for value in keys:
            sets.setValue(value,MVariant(MySettings[value].decode("utf-8")))

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
        global tableTypesNames, tableType, iconNameFormatLabels
        tableTypesNames = [translate("Tables", "Folder Table"), 
                            translate("Tables", "File Table"), 
                            translate("Tables", "Music Table"), 
                            translate("Tables", "Subfolder Table"), 
                            translate("Tables", "Cover Table")]
        iconNameFormatLabels = [translate("Universals", "%Artist%"), 
                            translate("Universals", "%Album%"), 
                            translate("Universals", "%Year%"), 
                            translate("Universals", "%Genre%")]
        from InputOutputs import IA #For first import
            
    def clearAllChilds(_object):
        from MyObjects import MWidget
        childs = _object.findChildren(MWidget)
        for child in childs:
            clearAllChilds(child)
            try:child.hide()
            except:pass
            child.deleteLater()
                            
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
        if isDebugMode or isDeveloperMode:
            print (str(_message))
        
    def checkMysqldSafe(_isAskIfNotFound=True):
        import InputOutputs, Dialogs
        from MyObjects import translate
        if InputOutputs.isFile(MySettings["pathOfMysqldSafe"])==False and InputOutputs.isFile("/usr/bin/" + MySettings["pathOfMysqldSafe"])==False:
            if _isAskIfNotFound:
                answer = Dialogs.ask(translate("AmarokEmbeddedDBCore", "\"mysqld_safe\" Not Found"),
                        translate("AmarokEmbeddedDBCore", "Executable \"mysqld_safe\" file is not found. Are you want to set path of this file?<br><b>Note :</b> \"mysql-common\" must be installed on your system."))
                if answer==Dialogs.Yes: 
                    import Options
                    Options.Options(MainWindow, _focusTo="pathOfMysqldSafe")
            else:
                return False
        else:
            return True
        
