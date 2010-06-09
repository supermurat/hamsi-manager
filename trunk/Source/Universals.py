# -*- coding: utf-8 -*-

import sys
from os import path
from datetime import timedelta, datetime

class Universals():
    global MainWindow, HamsiManagerApp, MySettings, setMySetting, saveSettings, mplayerSoundDevices, isStartingSuccessfully, isDebugMode, fillMySettings, activeWindow, aboutOfHamsiManager, HamsiManagerDirectory, Catalog, validSentenceStructureKeys, fileReNamerTypeNamesKeys, fileExtesionIsKeys, userDirectoryPath, isShowVerifySettings, imageExtStringOnlyPNGAndJPG, themePath, executableHamsiManagerPath, getListFromStrint, changedDefaultValuesKeys, newSettingsKeys, isCanBeShowOnMainWindow, sourcePath, getDateValue, isActivePyKDE4, getKDE4HomePath, isLoadedMyObjects, getBoolValue, windowMode, windowModeKeys, isShowOldValues, isChangeAll, isChangeSelected, tableTypesNames, tableTypeIcons, tableType, getThisTableType, fillUIUniversals
    MainWindow = None 
    isStartingSuccessfully = False
    MySettings = {}
    isDebugMode = False
    aboutOfHamsiManager = ""
    HamsiManagerDirectory = sys.path[0]
    Catalog = "HamsiManager" 
    fileReNamerTypeNamesKeys = ["Personal Computer", "Web Server", "Removable Media"]
    validSentenceStructureKeys = ["Title", "All Small", "All Caps", "Sentence", "Don`t Change"]
    fileExtesionIsKeys = ["After The First Point", "After The Last Point"]
    userDirectoryPath = path.expanduser("~")
    isShowVerifySettings = False
    changedDefaultValuesKeys = []
    newSettingsKeys = []
    mplayerSoundDevices = ["alsa", "pulse", "oss", "jack", "arts", "esd", "sdl", "nas", "mpegpes", "v4l2", "pcm"]
    imageExtStringOnlyPNGAndJPG = "(*.png *.jpg *.jpeg *.PNG *.JPG *.JPEG)"
    sourcePath = HamsiManagerDirectory + "/Source"
    themePath = sourcePath + "/Themes/Default"
    executableHamsiManagerPath = str(sys.argv[0])
    isCanBeShowOnMainWindow = False
    isActivePyKDE4 = False
    isLoadedMyObjects = False
    windowMode = "Normal"
    windowModeKeys = ["Normal", "Mini"]
    isShowOldValues = None
    isChangeAll = None
    isChangeSelected = None
    tableTypeIcons = ["folderTable.png", "fileTable.png", "musicTable.png", "subFolderTable.png"]
    tableTypesNames = ["", "", "", ""]
    tableType = None
    if executableHamsiManagerPath.find("HamsiManager")==-1 or executableHamsiManagerPath.find("./HamsiManager")!=-1:
        executableHamsiManagerPath = HamsiManagerDirectory + "/HamsiManager.py"
    
    def __init__(self, _app, _main):
        global MainWindow, HamsiManagerApp
        HamsiManagerApp = _app
        MainWindow = _main
        
    def fillMySettings(_setAgain=False, _isCheckUpdate=True):
        global MySettings, isShowVerifySettings, themePath, changedDefaultValuesKeys, newSettingsKeys, isActivePyKDE4, windowMode, tableType, isShowOldValues, isChangeAll, isChangeSelected
        import Settings, InputOutputs
        sets = Settings.setting()
        settingVersion = str(sets.value("settingsVersion").toString())
        defaultValues = Settings.getDefaultValues()
        valueTypesAndValues = Settings.getValueTypesAndValues()
        for keyValue in Settings.keysOfSettings:
            value = sets.value(keyValue, defaultValues[keyValue].decode("utf-8")).toString()
            if MySettings.keys().count(keyValue)==0 or _setAgain:
                MySettings[keyValue] = str(Settings.emendValue(keyValue, value, defaultValues[keyValue], valueTypesAndValues[keyValue]))
        newSettingVersion = str(MySettings["settingsVersion"])
        if _isCheckUpdate:
            if newSettingVersion!=settingVersion:
                newSettingsKeys, changedDefaultValuesKeys = Settings.updateOldSettings(settingVersion)
                isShowVerifySettings = True
            Settings.checkDatabases()
        if getBoolValue("isActivePyKDE4"):
            try:
                import PyKDE4
            except:
                MySettings["isActivePyKDE4"] = "False"
        InputOutputs.systemsCharSet = MySettings["systemsCharSet"]
        if getBoolValue("isActivePyKDE4"):
            if isLoadedMyObjects==False:
                isActivePyKDE4 = True
                InputOutputs.isMoveToTrash = getBoolValue("isMoveToTrash")
        windowMode = MySettings["windowMode"]
        themePath = sourcePath + "/Themes/" + MySettings["themeName"]
        if tableType == None:
            tableType = int(MySettings["tableType"])
            if tableType<0 or tableType>=len(tableTypesNames) or tableType==3:
                tableType = 1
        if isShowOldValues == None:
            isShowOldValues = getBoolValue("isShowOldValues")
            isChangeAll = getBoolValue("isChangeAll")
            isChangeSelected = getBoolValue("isChangeSelected")
    
    def getListFromStrint(_listString):
        listString = eval(str(_listString))
        if len(listString)==1:
            if listString[0].strip()=="":
                return []
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
        from Settings import setting, keysOfSettings
        sets = setting()
        if _key==None:
            keys = keysOfSettings
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
        
    def getKDE4HomePath():
        try:
            from MyObjects import MStandardDirs
            return MStandardDirs().localkdedir()
        except:
            import InputOutputs
            if InputOutputs.isDir(userDirectoryPath + "/.kde4/"):
                return userDirectoryPath + "/.kde4/"
            else:
                return userDirectoryPath + "/.kde/"
    
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
        global tableTypesNames
        from MyObjects import translate
        tableTypesNames = [translate("Tables", "Folder Table"), 
                            translate("Tables", "File Table"), 
                            translate("Tables", "Music Table"), 
                            translate("Tables", "Subfolder Table")]
                            
                            
