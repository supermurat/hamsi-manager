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


import os, sys, platform
from Core.MyObjects import *
import InputOutputs

class Variables():
    global getAvailablePlayers, getCharSets, getStyles, getScreenSize, getUserDesktopPath, getDefaultValues, getValueTypesAndValues, getKDE4HomePath, isAvailableKDE4, getSearchEnginesNames, getTaggersNames, getMyPluginsNames, getInstalledThemes, getInstalledLanguagesCodes, getInstalledLanguagesNames, isAvailableSymLink, getHashTypes, isRunableAsRoot, isRunningAsRoot, getColorSchemesAndPath, isPython3k, checkMysqldSafe, isUpdatable, isWindows
    global keysOfSettings, willNotReportSettings, mplayerSoundDevices, imageExtStringOnlyPNGAndJPG, windowModeKeys, tableTypeIcons, iconNameFormatKeys
    global osName, machineType, version, intversion, settingVersion, Catalog, aboutOfHamsiManager, fileReNamerTypeNamesKeys, validSentenceStructureKeys, fileExtesionIsKeys, installedLanguagesCodes, installedLanguagesNames, libPath, getLibraryDirectoryPath, isBuilt, getBuildType, getDefaultLanguageCode
    installedLanguagesCodes, installedLanguagesNames, libPath = None, None, None
    osName = os.name
    machineType = platform.machine()
    isPython3k = float(sys.version[:3])>=3.0
    isWindows = os.name=="nt"
    Catalog = "HamsiManager" 
    version = "1.3.2"
    intversion = 1320
    settingVersion = "1300"
    aboutOfHamsiManager = ""
    fileReNamerTypeNamesKeys = ["Personal Computer", "Web Server", "Removable Media"]
    validSentenceStructureKeys = ["Title", "All Small", "All Caps", "Sentence", "Don`t Change"]
    fileExtesionIsKeys = ["After The First Point", "After The Last Point", "Be Smart"]
    mplayerSoundDevices = ["alsa", "pulse", "oss", "jack", "arts", "esd", "sdl", "nas", "mpegpes", "v4l2", "pcm"]
    imageExtStringOnlyPNGAndJPG = "(*.png *.jpg *.jpeg *.PNG *.JPG *.JPEG)"
    windowModeKeys = ["Normal", "Mini"]
    tableTypeIcons = ["folderTable.png", "fileTable.png", "musicTable.png", "subFolderTable.png", "coverTable.png", "amarokCoverTable.png", "amarokMusicTable.png", "amarokMusicTable.png", "amarokCopyTable.png"]
    iconNameFormatKeys = ["%Artist%", "%Album%", "%Year%", "%Genre%"]
    keysOfSettings = ["lastDirectory", "isMainWindowMaximized", "isShowAdvancedSelections", 
                  "isRunOnDoubleClick", "isChangeSelected", 
                  "isChangeAll", "isOpenDetailsInNewWindow", "hiddenFolderTableColumns", 
                  "hiddenFileTableColumns", "hiddenMusicTableColumns", "hiddenSubFolderTableColumns", 
                  "hiddenCoverTableColumns", "hiddenAmarokMusicTableColumns", "hiddenAmarokCoverTableColumns", 
                  "hiddenAmarokArtistTableColumns", "hiddenAmarokCopyTableColumns", 
                  "isPlayNow", "MainWindowGeometries", "tableType", 
                  "activeTabNoOfSpecialTools", "unneededFiles", "ignoredFiles", 
                  "imageExtensions", "musicExtensions", "priorityIconNames", 
                  "unneededFileExtensions","ignoredFileExtensions", "fileReNamerType", 
                  "validSentenceStructure", 
                  "mplayerPath", "mplayerArgs", "mplayerAudioDevicePointer",
                  "mplayerAudioDevice", "isSaveActions", "fileSystemEncoding", 
                  "applicationStyle", "playerName", "isMinimumWindowMode", 
                  "packagerUnneededFileExtensions", "packagerUnneededFiles", "packagerUnneededDirectories", 
                  "lastUpdateControlDate", "updateInterval", 
                  "isCloseOnCleanAndPackage", 
                  "TableToolsBarButtonStyle", "ToolsBarButtonStyle", "PlayerBarButtonStyle", 
                  "MusicOptionsBarButtonStyle", "SubDirectoryOptionsBarButtonStyle", 
                  "CoverOptionsBarButtonStyle", "AmarokMusicOptionsBarButtonStyle", "AmarokCopyOptionsBarButtonStyle", 
                  "language", "isShowQuickMakeWindow", "isChangeExistIcon", 
                  "isClearFirstAndLastSpaceChars", "isEmendIncorrectChars", "validSentenceStructureForFile", "validSentenceStructureForDirectory", 
                  "validSentenceStructureForFileExtension", "isCorrectFileNameWithSearchAndReplaceTable", "isCorrectValueWithSearchAndReplaceTable",  
                  "isCorrectDoubleSpaceChars", "fileExtesionIs", "settingsVersion", "subDirectoryDeep", 
                  "maxRecordFileSize", "themeName", 
                  "unneededDirectories", "ignoredDirectories", 
                  "unneededDirectoriesIfIsEmpty",  
                  "isClearEmptyDirectoriesWhenPath", "isAutoCleanSubFolderWhenPath", 
                  "cleanerUnneededFileExtensions", "cleanerUnneededFiles", "cleanerUnneededDirectories", 
                  "isClearEmptyDirectoriesWhenClear", "isAutoCleanSubFolderWhenClear", 
                  "isClearEmptyDirectoriesWhenSave", "isClearEmptyDirectoriesWhenMoveOrChange", 
                  "isClearEmptyDirectoriesWhenCopyOrChange", "isClearEmptyDirectoriesWhenFileMove", 
                  "isAutoCleanSubFolderWhenSave", "isAutoCleanSubFolderWhenMoveOrChange", 
                  "isAutoCleanSubFolderWhenCopyOrChange", "isAutoCleanSubFolderWhenFileMove", 
                  "isAutoMakeIconToDirectoryWhenSave", "isAutoMakeIconToDirectoryWhenMoveOrChange", 
                  "isAutoMakeIconToDirectoryWhenCopyOrChange", "isAutoMakeIconToDirectoryWhenFileMove", 
                  "isDeleteEmptyDirectories", 
                  "isCleanerDeleteEmptyDirectories", "isPackagerDeleteEmptyDirectories", 
                  "remindMeLaterForUpdate", "remindMeLaterShowDateForUpdate", 
                  "isShowTransactionDetails", "windowMode", "isInstalledKDE4Language", 
                  "isShowWindowModeSuggestion", "isMakeAutoDesign", "isShowReconfigureWizard", 
                  "isAskIfHasManyImagesInAlbumDirectory", "isDeleteOtherImages", 
                  "CoversSubDirectoryDeep", 
                  "amarokDBHost", "amarokDBPort", "amarokDBUser", 
                  "amarokDBPass", "amarokDBDB", "amarokIsUseHost", 
                  "iconNameFormat", "iconFileType", "pathOfMysqldSafe", 
                  "isActiveCompleter", "isShowAllForCompleter", "isActiveClearGeneral", 
                  "colorSchemes", "isActiveAutoMakeIconToDirectory", 
                  "isDontDeleteFileAndDirectory", "pathOfDeletedFilesAndDirectories", 
                  "isReadOnlyAmarokDB", "isReadOnlyAmarokDBHost", "isResizeTableColumnsToContents", 
                  "AmarokFilterAmarokCoverTable", "AmarokFilterAmarokCopyTable", "AmarokFilterArtistTable", "AmarokFilterAmarokMusicTable", 
                  "isAppendFileSizeToFileTree", "isAppendLastModifiedToFileTree", 
                  "isMusicTableValuesChangeInAmarokDB", "isSubFolderTableValuesChangeInAmarokDB", 
                  "isFileTableValuesChangeInAmarokDB", "isFolderTableValuesChangeInAmarokDB", 
                  "isShowHiddensInSubFolderTable", "isShowHiddensInFolderTable", "isShowHiddensInFileTable", 
                  "isShowHiddensInMusicTable", "isShowHiddensInCoverTable", "isShowHiddensInFileTree", 
                  "isDecodeURLStrings", "isCheckUnSavedValues", "isAutoSaveScripts", "maxDeletedDirectorySize"]
    willNotReportSettings = ["amarokDBHost", "amarokDBPort", "amarokDBUser", 
                  "amarokDBPass", "amarokDBDB"]
    
    def isBuilt():
        return InputOutputs.isFile(joinPath(InputOutputs.HamsiManagerDirectory, "HamsiManagerHasBeenBuilt"))
                   
    def isUpdatable():
        if isBuilt():
            buildType = getBuildType()
            if buildType in ["rpm", "msi"]:
                return True
        return False
        
    def isAvailableKDE4():
        if InputOutputs.isFile("/usr/bin/kde4"):
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
            if InputOutputs.isFile(InputOutputs.joinPath(getLibraryDirectoryPath(), "kde4", "libexec", "kdesu")):
                if isRunningAsRoot():
                    return False
                return True
            return False
        except:
            return False
        
    def isRunningAsRoot():
        if InputOutputs.userDirectoryPath=="/root":
            return True
        return False
        
    def getBuildType():
        if InputOutputs.isFile(InputOutputs.joinPath(InputOutputs.HamsiManagerDirectory, "HamsiManagerHasBeenBuilt")):
            firstRow = InputOutputs.readLinesFromFile(InputOutputs.joinPath(InputOutputs.HamsiManagerDirectory, "HamsiManagerHasBeenBuilt"))[0]
            if firstRow.find("bdist_rpm")>-1:
                return "rpm"
            elif firstRow.find("bdist_msi")>-1:
                return "msi"
            elif firstRow.find("bdist")>-1:
                return "bdist"
            elif firstRow.find("install_exe")>-1:
                return "install_exe"
            elif firstRow.find("install")>-1:
                return "install"
            elif firstRow.find("build_exe")>-1:
                return "build_exe"
            elif firstRow.find("build")>-1:
                return "build"
        return str(None)

    def getDefaultValues():
        from datetime import datetime
        if getInstalledLanguagesCodes().count(str(MQtCore.QLocale.system().name()))>0:
            insLangCode = str(MQtCore.QLocale.system().name())
        else:
            insLangCode = "en_GB"
        myStyle , PlayerName = "", getAvailablePlayers().pop()
        if isWindows: myStyle = "Plastique"
        return {
                "lastDirectory": str(InputOutputs.userDirectoryPath), 
                "isMainWindowMaximized": "False", 
                "isShowAdvancedSelections": "False", 
                "isRunOnDoubleClick": "False", 
                "isChangeSelected": "False", 
                "isChangeAll": "True", 
                "isOpenDetailsInNewWindow": "False", 
                "hiddenFolderTableColumns": str([]), 
                "hiddenFileTableColumns": str([]), 
                "hiddenMusicTableColumns": str([]), 
                "hiddenSubFolderTableColumns": str([]), 
                "hiddenCoverTableColumns": str([]),
                "hiddenAmarokMusicTableColumns": str([]),
                "hiddenAmarokCoverTableColumns": str([]),
                "hiddenAmarokArtistTableColumns": str([]),
                "hiddenAmarokCopyTableColumns": str([]),
                "isPlayNow": "False", 
                "MainWindowGeometries": str([50, 50, 850, 533]), 
                "tableType": "1", 
                "activeTabNoOfSpecialTools": "0", 
                "unneededFiles": str(['Thumbs.db']), 
                "ignoredFiles": str(['.directory']), 
                "imageExtensions": str(['png', 'gif', 'jpeg', 'jpg']), 
                "musicExtensions": str(['mp3', 'ogg']), 
                "priorityIconNames": str(['cover']), 
                "unneededFileExtensions": str([]), 
                "ignoredFileExtensions": str(['m3u']), 
                "fileReNamerType": "Personal Computer", 
                "validSentenceStructure": "Title", 
                "mplayerPath": "mplayer", 
                "mplayerArgs": "-slave -quiet", 
                "mplayerAudioDevicePointer": "-ao",
                "mplayerAudioDevice": mplayerSoundDevices[0], 
                "isSaveActions": "True", 
                "fileSystemEncoding": InputOutputs.defaultFileSystemEncoding, 
                "applicationStyle": myStyle, 
                "playerName": PlayerName, 
                "isMinimumWindowMode": "False", 
                "packagerUnneededFileExtensions": str(['pyc', 'py~', 'e4p', 'pro', 'pro.user', 'kdev4', 'kdevelop', 'kdevelop.pcs', 'kdevses', 'ts', 'anjuta']), 
                "packagerUnneededFiles": str(['.directory', '.project', '.bzrignore']), 
                "packagerUnneededDirectories": str(['.eric4project', '.svn', '.git', 'CVS', '.bzr', '.cache', '.settings']), 
                "lastUpdateControlDate": datetime.now().strftime("%Y %m %d %H %M %S"), 
                "updateInterval": "14", 
                "isCloseOnCleanAndPackage": "True", 
                "TableToolsBarButtonStyle": "0", 
                "ToolsBarButtonStyle": "0", 
                "PlayerBarButtonStyle": "0", 
                "MusicOptionsBarButtonStyle": "0", 
                "SubDirectoryOptionsBarButtonStyle": "0",
                "CoverOptionsBarButtonStyle": "0",
                "AmarokMusicOptionsBarButtonStyle": "0", 
                "AmarokCopyOptionsBarButtonStyle": "0", 
                "language": insLangCode, 
                "isShowQuickMakeWindow": "True", 
                "isChangeExistIcon": "False", 
                "isClearFirstAndLastSpaceChars": "True", 
                "isEmendIncorrectChars": "True", 
                "validSentenceStructureForFile": "Title", 
                "validSentenceStructureForDirectory": "Don`t Change", 
                "validSentenceStructureForFileExtension": "All Small", 
                "isCorrectFileNameWithSearchAndReplaceTable": "True", 
                "isCorrectValueWithSearchAndReplaceTable": "True", 
                "isCorrectDoubleSpaceChars": "True", 
                "fileExtesionIs": "Be Smart", 
                "settingsVersion": settingVersion,
                "subDirectoryDeep": "-1", 
                "maxRecordFileSize": "256", 
                "themeName": "Default", 
                "unneededDirectories": str([]),
                "ignoredDirectories": str([]), 
                "unneededDirectoriesIfIsEmpty": str([]), 
                "isClearEmptyDirectoriesWhenPath": "True", 
                "isAutoCleanSubFolderWhenPath": "True", 
                "cleanerUnneededFileExtensions": str(['pyc', 'py~', 'e4p', 'pro', 'pro.user', 'kdev4', 'kdevelop', 'kdevelop.pcs', 'kdevses', 'ts', 'anjuta']),
                "cleanerUnneededFiles": str(['.directory', '.project', '.bzrignore']),
                "cleanerUnneededDirectories": str(['.eric4project', '.svn', '.git', 'CVS', '.bzr', '.cache', '.settings']),
                "isClearEmptyDirectoriesWhenClear": "True",
                "isAutoCleanSubFolderWhenClear": "True", 
                "isClearEmptyDirectoriesWhenSave": "True", 
                "isClearEmptyDirectoriesWhenMoveOrChange": "True", 
                "isClearEmptyDirectoriesWhenCopyOrChange": "True", 
                "isClearEmptyDirectoriesWhenFileMove": "True", 
                "isAutoCleanSubFolderWhenSave": "True", 
                "isAutoCleanSubFolderWhenMoveOrChange": "True", 
                "isAutoCleanSubFolderWhenCopyOrChange": "True", 
                "isAutoCleanSubFolderWhenFileMove": "True", 
                "isAutoMakeIconToDirectoryWhenSave": "True", 
                "isAutoMakeIconToDirectoryWhenMoveOrChange": "True", 
                "isAutoMakeIconToDirectoryWhenCopyOrChange": "True", 
                "isAutoMakeIconToDirectoryWhenFileMove": "True", 
                "isDeleteEmptyDirectories": "True", 
                "isCleanerDeleteEmptyDirectories": "True", 
                "isPackagerDeleteEmptyDirectories": "True", 
                "remindMeLaterForUpdate": "-1", 
                "remindMeLaterShowDateForUpdate": datetime.now().strftime("%Y %m %d %H %M %S"), 
                "isShowTransactionDetails": "False", 
                "windowMode": windowModeKeys[1], 
                "isInstalledKDE4Language": "False", 
                "isShowWindowModeSuggestion": "True", 
                "isMakeAutoDesign": "True", 
                "isShowReconfigureWizard": "True", 
                "isAskIfHasManyImagesInAlbumDirectory": "True", 
                "isDeleteOtherImages": "False", 
                "CoversSubDirectoryDeep": "-1", 
                "amarokDBHost": "localhost", 
                "amarokDBPort": "3306", 
                "amarokDBUser": "amarokuser", 
                "amarokDBPass": "amarokpassword", 
                "amarokDBDB": "amarokdb", 
                "amarokIsUseHost": "False", 
                "iconNameFormat": "%Album%", 
                "iconFileType": "png", 
                "pathOfMysqldSafe": "mysqld_safe", 
                "isActiveCompleter": "True", 
                "isShowAllForCompleter": "True", 
                "isActiveClearGeneral": "False", 
                "colorSchemes": "", 
                "isActiveAutoMakeIconToDirectory": "True", 
                "isDontDeleteFileAndDirectory": "False", 
                "pathOfDeletedFilesAndDirectories": InputOutputs.joinPath(InputOutputs.userDirectoryPath, ".HamsiApps", "HamsiManager", "Deleted"), 
                "isReadOnlyAmarokDB": "False", 
                "isReadOnlyAmarokDBHost": "False", 
                "isResizeTableColumnsToContents": "False", 
                "AmarokFilterAmarokCoverTable": "", 
                "AmarokFilterAmarokCopyTable": "", 
                "AmarokFilterArtistTable": "", 
                "AmarokFilterAmarokMusicTable": "", 
                "isAppendFileSizeToFileTree": "True", 
                "isAppendLastModifiedToFileTree": "False", 
                "isMusicTableValuesChangeInAmarokDB": "False", 
                "isSubFolderTableValuesChangeInAmarokDB": "False", 
                "isFileTableValuesChangeInAmarokDB": "False", 
                "isFolderTableValuesChangeInAmarokDB": "False", 
                "isShowHiddensInSubFolderTable": "False", 
                "isShowHiddensInFolderTable": "False", 
                "isShowHiddensInFileTable": "False", 
                "isShowHiddensInMusicTable": "False", 
                "isShowHiddensInCoverTable": "False", 
                "isShowHiddensInFileTree": "False", 
                "isDecodeURLStrings": "True", 
                "isCheckUnSavedValues": "False", 
                "isAutoSaveScripts": "True", 
                "maxDeletedDirectorySize" : "2048"
                }
            
                
    def getValueTypesAndValues(_isAfterDefineApplication=False):
        myStyleContent = "str"
        if _isAfterDefineApplication:
            myStyleContent = ["options", getStyles()]
        return {
                "lastDirectory": "str", 
                "isMainWindowMaximized": "bool", 
                "isShowAdvancedSelections": "bool", 
                "isRunOnDoubleClick": "bool", 
                "isChangeSelected": "bool", 
                "isChangeAll": "bool", 
                "isOpenDetailsInNewWindow": "bool", 
                "hiddenFolderTableColumns": ["intList", list(range(0, 2))], 
                "hiddenFileTableColumns": ["intList", list(range(0, 2))], 
                "hiddenMusicTableColumns": ["intList", list(range(0, 10))], 
                "hiddenSubFolderTableColumns": ["intList", list(range(0, 2))], 
                "hiddenCoverTableColumns": ["intList", list(range(0, 2))], 
                "hiddenAmarokMusicTableColumns": ["intList", list(range(0, 10))], 
                "hiddenAmarokCoverTableColumns": ["intList", list(range(0, 2))], 
                "hiddenAmarokArtistTableColumns": ["intList", list(range(0, 2))], 
                "hiddenAmarokCopyTableColumns": ["intList", list(range(0, 10))], 
                "isPlayNow": "bool", 
                "MainWindowGeometries": ["intStaticListLen", 4], 
                "tableType": ["int", list(range(0, 9))], 
                "activeTabNoOfSpecialTools": ["int", list(range(0, 7))], 
                "unneededFiles": "list", 
                "ignoredFiles": "list", 
                "imageExtensions": "list", 
                "musicExtensions": "list", 
                "priorityIconNames": "list", 
                "unneededFileExtensions": "list", 
                "ignoredFileExtensions": "list", 
                "fileReNamerType": ["options", fileReNamerTypeNamesKeys], 
                "validSentenceStructure": ["options", validSentenceStructureKeys], 
                "mplayerPath": "str", 
                "mplayerArgs": "str", 
                "mplayerAudioDevicePointer": "str",
                "mplayerAudioDevice": ["options", mplayerSoundDevices], 
                "isSaveActions": "bool", 
                "fileSystemEncoding": ["options", getCharSets()], 
                "applicationStyle": myStyleContent, 
                "playerName": ["options", getAvailablePlayers()], 
                "isMinimumWindowMode": "bool", 
                "packagerUnneededFileExtensions": "list", 
                "packagerUnneededFiles": "list", 
                "packagerUnneededDirectories": "list", 
                "lastUpdateControlDate": "date", 
                "updateInterval": ["int", list(range(0, 32))], 
                "isCloseOnCleanAndPackage": "bool", 
                "TableToolsBarButtonStyle": ["int", list(range(0, 4))], 
                "ToolsBarButtonStyle": ["int", list(range(0, 4))], 
                "PlayerBarButtonStyle": ["int", list(range(0, 4))], 
                "MusicOptionsBarButtonStyle": ["int", list(range(0, 4))], 
                "SubDirectoryOptionsBarButtonStyle": ["int", list(range(0, 4))], 
                "CoverOptionsBarButtonStyle": ["int", list(range(0, 4))], 
                "AmarokMusicOptionsBarButtonStyle": ["int", list(range(0, 4))], 
                "AmarokCopyOptionsBarButtonStyle": ["int", list(range(0, 4))], 
                "language": ["options", getInstalledLanguagesCodes()], 
                "isShowQuickMakeWindow": "bool", 
                "isChangeExistIcon": "bool", 
                "isClearFirstAndLastSpaceChars": "bool", 
                "isEmendIncorrectChars": "bool", 
                "validSentenceStructureForFile": ["options", validSentenceStructureKeys], 
                "validSentenceStructureForDirectory": ["options", validSentenceStructureKeys], 
                "validSentenceStructureForFileExtension": ["options", validSentenceStructureKeys], 
                "isCorrectFileNameWithSearchAndReplaceTable": "bool", 
                "isCorrectValueWithSearchAndReplaceTable": "bool", 
                "isCorrectDoubleSpaceChars": "bool", 
                "fileExtesionIs": ["options", fileExtesionIsKeys], 
                "settingsVersion": ["options", [settingVersion]],
                "subDirectoryDeep": ["int", list(range(-1, 10))], 
                "maxRecordFileSize": "int", 
                "themeName": ["options", getInstalledThemes()], 
                "unneededDirectories": "list", 
                "ignoredDirectories": "list", 
                "unneededDirectoriesIfIsEmpty": "list", 
                "isClearEmptyDirectoriesWhenPath": "bool", 
                "isAutoCleanSubFolderWhenPath": "bool", 
                "cleanerUnneededFileExtensions": "list",
                "cleanerUnneededFiles": "list",
                "cleanerUnneededDirectories": "list",
                "isClearEmptyDirectoriesWhenClear": "bool",
                "isAutoCleanSubFolderWhenClear": "bool", 
                "isClearEmptyDirectoriesWhenSave": "bool", 
                "isClearEmptyDirectoriesWhenMoveOrChange": "bool", 
                "isClearEmptyDirectoriesWhenCopyOrChange": "bool", 
                "isClearEmptyDirectoriesWhenFileMove": "bool", 
                "isAutoCleanSubFolderWhenSave": "bool", 
                "isAutoCleanSubFolderWhenMoveOrChange": "bool", 
                "isAutoCleanSubFolderWhenCopyOrChange": "bool", 
                "isAutoCleanSubFolderWhenFileMove": "bool", 
                "isAutoMakeIconToDirectoryWhenSave": "bool", 
                "isAutoMakeIconToDirectoryWhenMoveOrChange": "bool", 
                "isAutoMakeIconToDirectoryWhenCopyOrChange": "bool", 
                "isAutoMakeIconToDirectoryWhenFileMove": "bool", 
                "isDeleteEmptyDirectories": "bool", 
                "isCleanerDeleteEmptyDirectories": "bool", 
                "isPackagerDeleteEmptyDirectories": "bool", 
                "remindMeLaterForUpdate": ["int", list(range(-1, 7))], 
                "remindMeLaterShowDateForUpdate": "date", 
                "isShowTransactionDetails": "bool", 
                "windowMode": ["options", windowModeKeys], 
                "isInstalledKDE4Language": "bool", 
                "isShowWindowModeSuggestion": "bool", 
                "isMakeAutoDesign": "bool", 
                "isShowReconfigureWizard": "bool", 
                "isAskIfHasManyImagesInAlbumDirectory": "bool", 
                "isDeleteOtherImages": "bool", 
                "CoversSubDirectoryDeep": ["int", [ x for x in range(-1, 10) if x!=0 ]], 
                "amarokDBHost": "str", 
                "amarokDBPort": "int", 
                "amarokDBUser": "str", 
                "amarokDBPass": "str", 
                "amarokDBDB": "str", 
                "amarokIsUseHost": "bool", 
                "iconNameFormat": "str", 
                "iconFileType": ["options", ["png", "jpg"]], 
                "pathOfMysqldSafe": "str", 
                "isActiveCompleter": "bool", 
                "isShowAllForCompleter": "bool", 
                "isActiveClearGeneral": "bool", 
                "colorSchemes": "Default", 
                "isActiveAutoMakeIconToDirectory": "bool", 
                "isDontDeleteFileAndDirectory": "bool", 
                "pathOfDeletedFilesAndDirectories": "str", 
                "isReadOnlyAmarokDB": "bool", 
                "isReadOnlyAmarokDBHost": "bool", 
                "isResizeTableColumnsToContents": "bool", 
                "AmarokFilterAmarokCoverTable": "str", 
                "AmarokFilterAmarokCopyTable": "str", 
                "AmarokFilterArtistTable": "str", 
                "AmarokFilterAmarokMusicTable": "str", 
                "isAppendFileSizeToFileTree": "bool", 
                "isAppendLastModifiedToFileTree": "bool", 
                "isMusicTableValuesChangeInAmarokDB": "bool", 
                "isSubFolderTableValuesChangeInAmarokDB": "bool", 
                "isFileTableValuesChangeInAmarokDB": "bool", 
                "isFolderTableValuesChangeInAmarokDB": "bool", 
                "isShowHiddensInSubFolderTable": "bool", 
                "isShowHiddensInFolderTable": "bool", 
                "isShowHiddensInFileTable": "bool", 
                "isShowHiddensInMusicTable": "bool", 
                "isShowHiddensInCoverTable": "bool", 
                "isShowHiddensInFileTree": "bool", 
                "isDecodeURLStrings": "bool", 
                "isCheckUnSavedValues": "bool", 
                "isAutoSaveScripts": "bool", 
                "maxDeletedDirectorySize": "int"
                }

    def getAvailablePlayers():
        playerNames = ["Mplayer"]
        try:
            import tkSnack
            playerNames.append("tkSnack")
        except:pass
        try:
            from PySide.phonon import Phonon
            playerNames.append("Phonon (PySide)")
        except:pass
        try:
            from PyQt4.phonon import Phonon
            playerNames.append("Phonon")
        except:pass
        return playerNames
       
    def getCharSets():
        from encodings import aliases
        charSets = []
        for k, v in aliases.aliases.items():
            key = v.replace("_", "-")
            if v.find("iso")>-1 and v.find("iso-")==-1:
                key = key.replace("iso", "iso-")
            if charSets.count(key)==0:
                charSets.append(key)
        charSets.sort()
        return charSets
        
    def getStyles():
        styles = [""]
        for stil in MQtGui.QStyleFactory.keys(): 
            styles.append(str(stil))
        return styles
        
    def getColorSchemesAndPath():
        from Core import Settings, Universals
        colorSchemes, colorSchemePaths = [], []
        colorSchemes.append("Default")
        colorSchemePaths.append("")
        if isActivePyKDE4:
            from PyKDE4.kdecore import KStandardDirs, KGlobal
            schemeFiles = KGlobal.dirs().findAllResources("data", "color-schemes/*.colors", KStandardDirs.NoDuplicates)
            for scheme in schemeFiles:
                sets = Settings.getSettings(scheme)
                colorSchemes.append(Universals.trStr(sets.value("Name", InputOutputs.getBaseName(scheme))))
                colorSchemePaths.append(scheme)
        return colorSchemes, colorSchemePaths
        
    def getScreenSize():
        from Core import Universals
        if Universals.MainWindow!=None:
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
            desktopPath = shell.SHGetFolderPath (0, shellcon.CSIDL_DESKTOP, 0, 0)
        else:
            desktopNames = [str(translate("Variables", "Desktop")), "Desktop"]
            for dirName in desktopNames:
                if InputOutputs.isDir(InputOutputs.joinPath(InputOutputs.userDirectoryPath, dirName)):
                    desktopPath = InputOutputs.joinPath(InputOutputs.userDirectoryPath, dirName)
                    break
                else:
                    desktopPath = InputOutputs.userDirectoryPath
        return desktopPath
    
    def getKDE4HomePath():
        if isAvailableKDE4():
            try:
                if isActivePyKDE4:
                    from PyKDE4.kdecore import KStandardDirs
                    kdedirPath = str(KStandardDirs().localkdedir())
                    if kdedirPath[-1]==os.sep:
                        kdedirPath = kdedirPath[:-1]
                else:
                    from Core import Execute
                    kdedirPath = Execute.getCommandResult(["kde4-config", "--localprefix"])[:-2]
                return kdedirPath
            except:pass
        if InputOutputs.isDir(InputOutputs.joinPath(InputOutputs.userDirectoryPath, ".kde4", "share", "config")):
            return InputOutputs.joinPath(InputOutputs.userDirectoryPath, ".kde4")
        else:
            return InputOutputs.joinPath(InputOutputs.userDirectoryPath, ".kde")
        
    def getLibraryDirectoryPath():
        global libPath
        if libPath==None:
            if isActivePyKDE4:
                from PyKDE4 import pykdeconfig
                libPath = pykdeconfig._pkg_config["kdelibdir"]
            else:
                try:
                    from Core import Execute
                    libPath = Execute.getCommandResult(["kde4-config", "--path", "lib"]).split(":")[1][:-2]
                except:
                    if InputOutputs.isDir("/usr/lib64"):
                        libPath = "/usr/lib64"
                    else: 
                        libPath = "/usr/lib"
        return libPath
                
    def getSearchEnginesNames():
        engines = []
        for name in InputOutputs.readDirectoryAll(InputOutputs.joinPath(InputOutputs.HamsiManagerDirectory, "SearchEngines")):
            try:
                moduleName = name.split(".")[0]
                moduleNameExt = name.split(".")[1]
                if engines.count(moduleName)==0:
                    if name[:1] != "." and moduleName!="__init__" and ["py", "pyc", "pyd"].count(moduleNameExt)==1 and InputOutputs.isFile(InputOutputs.joinPath(InputOutputs.HamsiManagerDirectory, "SearchEngines", name)):
                        engines.append(moduleName)
            except:pass
        return engines
    
    def getTaggersNames():
        taggers = []
        for name in InputOutputs.readDirectoryAll(InputOutputs.joinPath(InputOutputs.HamsiManagerDirectory, "Taggers")):
            try:
                moduleName = name.split(".")[0]
                moduleNameExt = name.split(".")[1]
                if taggers.count(moduleName)==0:
                    if name[:1] != "." and moduleName!="__init__" and ["py", "pyc", "pyd"].count(moduleNameExt)==1 and InputOutputs.isFile(InputOutputs.joinPath(InputOutputs.HamsiManagerDirectory, "Taggers", name)):
                        taggers.append(moduleName)
            except:pass
        return taggers
        
    def getMyPluginsNames():
        plugins = []
        for name in InputOutputs.readDirectoryAll(InputOutputs.joinPath(InputOutputs.HamsiManagerDirectory, "MyPlugins")):
            try:
                if name[:1] != "." and name[:2] != "__" and name[-2:] != "__" and InputOutputs.isDir(InputOutputs.joinPath(InputOutputs.HamsiManagerDirectory, "MyPlugins", name)):
                    plugins.append(name)
            except:pass
        return plugins
        
    def getInstalledThemes():
        themes = []
        for name in InputOutputs.readDirectoryAll(InputOutputs.joinPath(InputOutputs.HamsiManagerDirectory, "Themes")):
            try:
                if name[:1] != "." and name[:2] != "__" and name[-2:] != "__" and InputOutputs.isDir(InputOutputs.joinPath(InputOutputs.HamsiManagerDirectory, "Themes", name)):
                    themes.append(name)
            except:pass
        return themes
        
    def getDefaultLanguageCode():
        if getInstalledLanguagesCodes().count(str(MQtCore.QLocale.system().name()))>0:
            return str(MQtCore.QLocale.system().name())
        return "en_GB"
    
    def getInstalledLanguagesCodes():
        global installedLanguagesCodes
        if installedLanguagesCodes==None:
            languages = []
            for name in InputOutputs.readDirectoryAll(InputOutputs.joinPath(InputOutputs.HamsiManagerDirectory, "Languages")):
                if InputOutputs.isFile(InputOutputs.joinPath(InputOutputs.HamsiManagerDirectory, "Languages", name)) and name[-3:]==".qm":
                    langCode = name[-8:-3]
                    if languages.count(langCode)==0:
                        languages.append(langCode)
            if languages.count("en_GB")==0:
                languages.append("en_GB")
            installedLanguagesNames = languages
        return installedLanguagesNames
        
    def getInstalledLanguagesNames():
        global installedLanguagesNames
        if installedLanguagesNames==None:
            languages = []
            for name in InputOutputs.readDirectoryAll(InputOutputs.joinPath(InputOutputs.HamsiManagerDirectory, "Languages")):
                if InputOutputs.isFile(InputOutputs.joinPath(InputOutputs.HamsiManagerDirectory, "Languages", name)) and name[-3:]==".qm":
                    langCode = name[-8:-3]
                    if languages.count(str(MQtCore.QLocale.languageToString(MQtCore.QLocale(langCode).language())))==0:
                        languages.append(str(MQtCore.QLocale.languageToString(MQtCore.QLocale(langCode).language())))
            if languages.count("English")==0:
                languages.append("English")
            installedLanguagesNames = languages
        return installedLanguagesNames
        
    def getHashTypes():
        try:
            import hashlib
            return ["MD5", "SHA1", "SHA224", "SHA256", "SHA384", "SHA512"]
        except:
            #for x < python 2.5
            hashTypes = []
            try:
                import md5
                hashTypes.append("MD5")
            except:pass
            try:
                import md5
                hashTypes.append("SHA1")
            except:pass
            return hashTypes

        
    def checkMysqldSafe(_isAskIfNotFound=True):
        from Core import Dialogs, Universals
        if InputOutputs.isFile(Universals.MySettings["pathOfMysqldSafe"])==False and InputOutputs.isFile("/usr/bin/" + Universals.MySettings["pathOfMysqldSafe"])==False:
            if _isAskIfNotFound:
                answer = Dialogs.ask(translate("EmbeddedDBCore", "\"mysqld_safe\" Not Found"),
                        translate("EmbeddedDBCore", "Executable \"mysqld_safe\" file is not found. Are you want to set path of this file?<br><b>Note :</b> \"mysql-common\" must be installed on your system."))
                if answer==Dialogs.Yes:
                    from Options import OptionsForm
                    OptionsForm.OptionsForm(Universals.MainWindow, _focusTo="pathOfMysqldSafe")
            else:
                return False
        else:
            return True
    
                
