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


import sys
import os
import platform
from datetime import timedelta, datetime
import FileUtils as fu
from Core.MyObjects import *

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
installedLanguagesCodes, installedLanguagesNames, libPath = None, None, None
osName = os.name
machineType = platform.machine()
isPython3k = float(sys.version[:3]) >= 3.0
isWindows = os.name == "nt"
Catalog = "HamsiManager"
version = "1.3.7"
intversion = 1372
settingVersion = "1372"
aboutOfHamsiManager = ""
fileReNamerTypeNamesKeys = ["Personal Computer", "Web Server", "Removable Media"]
validSentenceStructureKeys = ["Title", "All Small", "All Caps", "Sentence", "Don`t Change"]
fileExtensionIsKeys = ["After The First Point", "After The Last Point", "Be Smart"]
mplayerSoundDevices = ["alsa", "pulse", "oss", "jack", "arts", "esd", "sdl", "nas", "mpegpes", "v4l2", "pcm"]
imageExtStringOnlyPNGAndJPG = "(*.png *.jpg *.jpeg *.PNG *.JPG *.JPEG)"
windowModeKeys = ["Normal", "Mini"]
tableTypeIcons = {"0": "folderTable.png",
                  "1": "fileTable.png",
                  "2": "musicTable.png",
                  "3": "subFolderTable.png",
                  "4": "coverTable.png",
                  "5": "amarokCoverTable.png",
                  "6": "amarokMusicTable.png",
                  "7": "amarokMusicTable.png",
                  "8": "amarokCopyTable.png",
                  "9": "subFolderMusicTable.png"}
iconNameFormatKeys = ["%Artist%", "%Album%", "%Year%", "%Genre%"]
iconNameFormatLabels = [translate("Variables", "%Artist%"),
                        translate("Variables", "%Album%"),
                        translate("Variables", "%Year%"),
                        translate("Variables", "%Genre%")]
willNotReportSettings = ["amarokDBHost", "amarokDBPort", "amarokDBUser", "amarokDBPass", "amarokDBDB"]

isActiveDirectoryCover = True
isActiveAmarok = True

if isWindows == "nt":
    isActiveDirectoryCover = False
    isActiveAmarok = False

tableTypesNames = {"0": translate("Tables", "Folder Table"),
                   "1": translate("Tables", "File Table"),
                   "2": translate("Tables", "Music Table"),
                   "3": translate("Tables", "Subfolder Table"),
                   "9": translate("Tables", "Subfolder Music Table")}
if isActiveDirectoryCover:
    tableTypesNames.update({"4": translate("Tables", "Cover Table")})
if isActiveAmarok:
    tableTypesNames.update({"5": translate("Tables", "Amarok Cover Table"),
                            "6": translate("Tables", "Amarok Music Table"),
                            "7": translate("Tables", "Amarok Artist Table"),
                            "8": translate("Tables", "Amarok Copy Table")})


def setPathOfSettingsDirectory(_path):
    _path = str(_path)
    if _path[-1] == os.sep:
        _path = _path[:-1]
    fu.pathOfSettingsDirectory = _path


def trUnicode(_s, _e="utf-8"):
    if isPython3k:
        return _s
    if isinstance(_s, unicode):
        return _s
    return unicode(_s, _e)


def trDecode(_s, _e="utf-8", _p="strict"):
    if isPython3k:
        return _s
    return _s.decode(_e, _p)


def trDecodeList(_s, _e="utf-8", _p="strict"):
    if isPython3k:
        return _s
    sList = []
    for x in _s:
        sList.append(trDecode(x, _e, _p))
    return sList


def trEncode(_s, _e="utf-8", _p="strict"):
    if isPython3k:
        return _s
    return _s.encode(_e, _p)


def trEncodeList(_s, _e="utf-8", _p="strict"):
    if isPython3k:
        return _s
    sList = []
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
        if _key == "replacementChars":
            return {}
        else:
            if isPython3k:
                return ""
            else:
                return unicode("")


def fillMySettings(_setAgain=False, _isCheckUpdate=True):
    global MySettings, isShowVerifySettings, changedDefaultValuesKeys, newSettingsKeys, windowMode, tableType
    from Core import Settings

    sets = Settings.setting()
    settingVersion = trStr(sets.value("settingsVersion"))
    defaultValues = Settings.getDefaultValues()
    valueTypesAndValues = Settings.getValueTypesAndValues()
    for keyValue in Settings.getKeysOfSettings():
        value = trStr(sets.value(keyValue, trQVariant(defaultValues[keyValue])))
        if keyValue not in MySettings.keys() or _setAgain:
            MySettings[keyValue] = str(
                Settings.emendValue(keyValue, value, defaultValues[keyValue], valueTypesAndValues[keyValue]))
    for keyValue in sets.allKeys():
        keyValue = str(keyValue)
        if keyValue not in MySettings.keys():
            value = trStr(sets.value(keyValue, trQVariant("")))
            MySettings[keyValue] = str(Settings.emendValue(keyValue, value, "", "str"))
    newSettingVersion = str(MySettings["settingsVersion"])
    if _isCheckUpdate:
        if newSettingVersion != settingVersion:
            newSettingsKeys, changedDefaultValuesKeys = Settings.updateOldSettings(settingVersion, newSettingVersion)
            isShowVerifySettings = True
    fu.fileSystemEncoding = MySettings["fileSystemEncoding"]
    windowMode = MySettings["windowMode"]
    fu.themePath = fu.joinPath(fu.HamsiManagerDirectory, "Themes", MySettings["themeName"])
    if tableType == None:
        tableType = MySettings["tableType"]
        if tableType not in tableTypesNames:
            tableType = "1"
    if getBoolValue("isInstalledKDE4Language") == False:
        from Core import MyConfigure

        MyConfigure.installKDE4Languages()


def getListFromListString(_listString, _splitter=None):
    if _splitter is None:
        listString = eval(str(_listString))
    else:
        listString = str(_listString).split(_splitter)
    if len(listString) == 1:
        if listString[0].strip() == "":
            return []
    return listString


def getStringFromList(_list, _splitter=None):
    if _splitter is None:
        return str(_list)
    else:
        if isinstance(_list, (list, tuple, dict)):
            listString = ""
            for x, value in enumerate(_list):
                if x != 0:
                    listString += _splitter
                listString += value
            return listString
        else:
            return str(_list)


def getValue(_key, _defaultValue=""):
    try:
        return MySettings[_key]
    except:
        from Core import Settings

        sets = Settings.setting()
        MySettings[_key] = str(trStr(sets.value(_key, trQVariant(_defaultValue))))
        return MySettings[_key]


def getDateValue(_key):
    return datetime.strptime(getValue(_key), "%Y %m %d %H %M %S")


def getBoolValue(_key, _defaultValue=""):
    value = str(getValue(_key, _defaultValue)).title()
    if value == "True" or value == "1" or value == "2":
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
    if _key == None:
        keys = MySettings.keys()
    else:
        keys = [_key]
    for value in keys:
        sets.setValue(value, trQVariant(MySettings[value]))


def startThreadAction():
    global threadActionState
    threadActionState = True


def cancelThreadAction():
    global threadActionState
    from Core import Dialogs

    answer = Dialogs.ask(translate("Universals", "Are You Sure?"),
                         translate("Universals", "Are you want to cancel these transactions?"))
    if answer == Dialogs.Yes:
        threadActionState = False


def finishThreadAction():
    global threadActionState
    threadActionState = None


def isContinueThreadAction():
    return threadActionState


def printForDevelopers(_message):
    import logging

    if loggingLevel == logging.DEBUG:
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
    if _isUseLastPathKeyType == 0: pass
    elif _isUseLastPathKeyType == 1: pathKey = _caption
    elif _isUseLastPathKeyType == 2: pathKey = _caption + " - " + _directory
    elif _isUseLastPathKeyType == 3: pathKey = _directory
    elif _isUseLastPathKeyType == 4 and _lastPathKey is not None: pathKey = _caption + " - " + _lastPathKey
    elif _isUseLastPathKeyType == 5 and _lastPathKey is not None: pathKey = _caption + " - " + _directory + " - " + _lastPathKey
    elif _isUseLastPathKeyType == 6 and _lastPathKey is not None: pathKey = _directory + " - " + _lastPathKey
    else: pathKey = _isUseLastPathKeyType
    return pathKey


def isBuilt():
    return fu.isFile(fu.joinPath(fu.HamsiManagerDirectory, "HamsiManagerHasBeenBuilt"))


def isUpdatable():
    if isBuilt():
        buildType = getBuildType()
        if buildType in ["rpm", "msi"]:
            return True
    return False


def isAvailableKDE4():
    if fu.isFile("/usr/bin/kde4"):
        return True
    else:
        return False


def isAvailableSymLink():
    try:
        from os import symlink

        return True
    except:
        return False


def isRunableAsRoot():
    try:
        if fu.isFile(fu.joinPath(getLibraryDirectoryPath(), "kde4", "libexec", "kdesu")):
            if isRunningAsRoot():
                return False
            return True
        return False
    except:
        return False


def isRunningAsRoot():
    if fu.userDirectoryPath == "/root":
        return True
    return False


def getBuildType():
    if fu.isFile(fu.joinPath(fu.HamsiManagerDirectory, "HamsiManagerHasBeenBuilt")):
        firstRow = fu.readLinesFromFile(fu.joinPath(fu.HamsiManagerDirectory, "HamsiManagerHasBeenBuilt"))[0]
        if firstRow.find("bdist_rpm") > -1:
            return "rpm"
        elif firstRow.find("bdist_msi") > -1:
            return "msi"
        elif firstRow.find("bdist") > -1:
            return "bdist"
        elif firstRow.find("install_exe") > -1:
            return "install_exe"
        elif firstRow.find("install") > -1:
            return "install"
        elif firstRow.find("build_exe") > -1:
            return "build_exe"
        elif firstRow.find("build") > -1:
            return "build"
    return str(None)


def getAvailablePlayers():
    playerNames = ["Mplayer"]
    try:
        import tkSnack

        playerNames.append("tkSnack")
    except: pass
    try:
        from PySide.phonon import Phonon

        playerNames.append("Phonon (PySide)")
    except: pass
    try:
        from PyQt4.phonon import Phonon

        playerNames.append("Phonon")
    except: pass
    return playerNames


def getCharSets():
    from encodings import aliases

    charSets = []
    for k, v in aliases.aliases.items():
        key = v.replace("_", "-")
        if v.find("iso") > -1 and v.find("iso-") == -1:
            key = key.replace("iso", "iso-")
        if charSets.count(key) == 0:
            charSets.append(key)
    charSets.sort()
    return charSets


def getStyles():
    styles = [""]
    for stil in MQtGui.QStyleFactory.keys():
        styles.append(str(stil))
    return styles


def getColorSchemesAndPath():
    from Core import Settings

    colorSchemes, colorSchemePaths = [], []
    colorSchemes.append("Default")
    colorSchemePaths.append("")
    if isActivePyKDE4:
        from PyKDE4.kdecore import KStandardDirs, KGlobal

        schemeFiles = KGlobal.dirs().findAllResources("data", "color-schemes/*.colors", KStandardDirs.NoDuplicates)
        for scheme in schemeFiles:
            sets = Settings.getSettings(scheme)
            colorSchemes.append(trStr(sets.value("Name", fu.getBaseName(scheme))))
            colorSchemePaths.append(scheme)
    return colorSchemes, colorSchemePaths


def getScreenSize():
    if getMainWindow() != None:
        return MQtGui.QDesktopWidget().screenGeometry()
    else:
        return None


def getUserDesktopPath():
    if isActivePyKDE4:
        from PyKDE4.kdeui import KGlobalSettings

        desktopPath = str(KGlobalSettings.desktopPath())
    elif isAvailableKDE4():
        from Core import Execute

        desktopPath = Execute.getCommandResult(["kde4-config", "--userpath", "desktop"])[:-2]
    elif isWindows:
        from win32com.shell import shell, shellcon

        desktopPath = shell.SHGetFolderPath(0, shellcon.CSIDL_DESKTOP, 0, 0)
    else:
        desktopNames = [str(translate("Variables", "Desktop")), "Desktop"]
        for dirName in desktopNames:
            if fu.isDir(fu.joinPath(fu.userDirectoryPath, dirName)):
                desktopPath = fu.joinPath(fu.userDirectoryPath, dirName)
                break
            else:
                desktopPath = fu.userDirectoryPath
    return desktopPath


def getKDE4HomePath():
    if isAvailableKDE4():
        try:
            if isActivePyKDE4:
                from PyKDE4.kdecore import KStandardDirs

                kdedirPath = str(KStandardDirs().localkdedir())
                if kdedirPath[-1] == os.sep:
                    kdedirPath = kdedirPath[:-1]
            else:
                from Core import Execute

                kdedirPath = Execute.getCommandResult(["kde4-config", "--localprefix"])[:-2]
            return kdedirPath
        except: pass
    if fu.isDir(fu.joinPath(fu.userDirectoryPath, ".kde4", "share", "config")):
        return fu.joinPath(fu.userDirectoryPath, ".kde4")
    else:
        return fu.joinPath(fu.userDirectoryPath, ".kde")


def getLibraryDirectoryPath():
    global libPath
    if libPath == None:
        if isActivePyKDE4:
            from PyKDE4 import pykdeconfig

            libPath = pykdeconfig._pkg_config["kdelibdir"]
        else:
            try:
                from Core import Execute

                libPath = Execute.getCommandResult(["kde4-config", "--path", "lib"]).split(":")[1][:-2]
            except:
                if fu.isDir("/usr/lib64"):
                    libPath = "/usr/lib64"
                else:
                    libPath = "/usr/lib"
    return libPath


def getSearchEnginesNames():
    engines = []
    for name in fu.readDirectoryAll(fu.joinPath(fu.HamsiManagerDirectory, "SearchEngines")):
        try:
            moduleName = name.split(".")[0]
            moduleNameExt = name.split(".")[1]
            if engines.count(moduleName) == 0:
                if name[:1] != "." and moduleName != "__init__" and ["py", "pyc", "pyd"].count(
                    moduleNameExt) == 1 and fu.isFile(fu.joinPath(fu.HamsiManagerDirectory, "SearchEngines", name)):
                    engines.append(moduleName)
        except: pass
    return engines


def getTaggersNames():
    taggers = []
    for name in fu.readDirectoryAll(fu.joinPath(fu.HamsiManagerDirectory, "Taggers")):
        try:
            moduleName = name.split(".")[0]
            moduleNameExt = name.split(".")[1]
            if taggers.count(moduleName) == 0:
                if name[:1] != "." and moduleName != "__init__" and ["py", "pyc", "pyd"].count(
                    moduleNameExt) == 1 and fu.isFile(fu.joinPath(fu.HamsiManagerDirectory, "Taggers", name)):
                    taggers.append(moduleName)
        except: pass
    return taggers


def getMyPluginsNames():
    plugins = []
    for name in fu.readDirectoryAll(fu.joinPath(fu.HamsiManagerDirectory, "MyPlugins")):
        try:
            if name[:1] != "." and name[:2] != "__" and name[-2:] != "__" and fu.isDir(
                fu.joinPath(fu.HamsiManagerDirectory, "MyPlugins", name)):
                plugins.append(name)
        except: pass
    return plugins


def getInstalledThemes():
    themes = []
    for name in fu.readDirectoryAll(fu.joinPath(fu.HamsiManagerDirectory, "Themes")):
        try:
            if name[:1] != "." and name[:2] != "__" and name[-2:] != "__" and fu.isDir(
                fu.joinPath(fu.HamsiManagerDirectory, "Themes", name)):
                themes.append(name)
        except: pass
    return themes


def getDefaultLanguageCode():
    if getInstalledLanguagesCodes().count(str(MQtCore.QLocale.system().name())) > 0:
        return str(MQtCore.QLocale.system().name())
    return "en_GB"


def getInstalledLanguagesCodes():
    global installedLanguagesCodes
    if installedLanguagesCodes == None:
        languages = []
        for name in fu.readDirectoryAll(fu.joinPath(fu.HamsiManagerDirectory, "Languages")):
            if fu.isFile(fu.joinPath(fu.HamsiManagerDirectory, "Languages", name)) and name[-3:] == ".qm":
                langCode = name[-8:-3]
                if languages.count(langCode) == 0:
                    languages.append(langCode)
        if languages.count("en_GB") == 0:
            languages.append("en_GB")
        installedLanguagesNames = languages
    return installedLanguagesNames


def getInstalledLanguagesNames():
    global installedLanguagesNames
    if installedLanguagesNames == None:
        languages = []
        for name in fu.readDirectoryAll(fu.joinPath(fu.HamsiManagerDirectory, "Languages")):
            if fu.isFile(fu.joinPath(fu.HamsiManagerDirectory, "Languages", name)) and name[-3:] == ".qm":
                langCode = name[-8:-3]
                if languages.count(str(MQtCore.QLocale.languageToString(MQtCore.QLocale(langCode).language()))) == 0:
                    languages.append(str(MQtCore.QLocale.languageToString(MQtCore.QLocale(langCode).language())))
        if languages.count("English") == 0:
            languages.append("English")
        installedLanguagesNames = languages
    return installedLanguagesNames


def getHashTypes():
    return ["MD5", "SHA1", "SHA224", "SHA256", "SHA384", "SHA512"]


def checkMysqldSafe(_isAskIfNotFound=True):
    from Core import Dialogs

    if fu.isFile(MySettings["pathOfMysqldSafe"]) == False and fu.isFile(
            "/usr/bin/" + MySettings["pathOfMysqldSafe"]) == False:
        if _isAskIfNotFound:
            answer = Dialogs.ask(translate("EmbeddedDBCore", "\"mysqld_safe\" Not Found"),
                                 translate("EmbeddedDBCore",
                                           "Executable \"mysqld_safe\" file is not found. Are you want to set path of this file?<br><b>Note :</b> \"mysql-common\" must be installed on your system."))
            if answer == Dialogs.Yes:
                from Options import OptionsForm

                OptionsForm.OptionsForm(getMainWindow(), _focusTo="pathOfMysqldSafe")
        else:
            return False
    else:
        return True






