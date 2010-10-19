# -*- coding: utf-8 -*-

import os, sys

class Variables():
    global checkStartupVariables, checkEncoding, getAvailablePlayers, getCharSets, getStyles, getScreenSize, getMyObjectsNames, isAvailablePyKDE4, getUserDesktopPath, getDefaultValues, getValueTypesAndValues
    global MQtGui, MQtCore, MObjectName, isQt4Exist, defaultFileSystemEncoding, keysOfSettings, willNotReportSettings
    global version, intversion, settingVersion
    MQtGui, MQtCore, isQt4Exist, MObjectName = None, None, False, ""
    version = "0.9.06"
    intversion = 906
    settingVersion = "906"
    defaultFileSystemEncoding = sys.getfilesystemencoding().lower()
    keysOfSettings = ["lastDirectory", "isMainWindowMaximized", "isShowAdvancedSelections", 
                  "isShowOldValues", "isRunOnDoubleClick", "isChangeSelected", 
                  "isChangeAll", "isOpenDetailsInNewWindow", "hiddenFolderTableColumns", 
                  "hiddenFileTableColumns", "hiddenMusicTableColumns", "hiddenSubFolderTableColumns", 
                  "hiddenCoverTableColumns", 
                  "isPlayNow", "MainWindowGeometries", "tableType", 
                  "activeTabNoOfSpecialTools", "unneededFiles", "ignoredFiles", 
                  "imageExtensions", "musicExtensions", "priorityIconNames", 
                  "unneededFileExtensions","ignoredFileExtensions", "fileReNamerType", 
                  "validSentenceStructure", 
                  "mplayerPath", "mplayerArgs", "mplayerAudioDevicePointer",
                  "mplayerAudioDevice", "isSaveActions", "fileSystemEncoding", 
                  "applicationStyle", "playerName", "musicTagType", "isMinimumWindowMode", 
                  "packagerUnneededFileExtensions", "packagerUnneededFiles", "packagerUnneededDirectories", 
                  "lastUpdateControlDate", "updateInterval", 
                  "NeededObjectsName", "isActivePyKDE4", "isCloseOnCleanAndPackage", 
                  "TableToolsBarButtonStyle", "ToolsBarButtonStyle", "PlayerBarButtonStyle", 
                  "MusicOptionsBarButtonStyle", "SubDirectoryOptionsBarButtonStyle", 
                  "CoverOptionsBarButtonStyle",
                  "language", "isShowQuickMakeWindow", "isChangeExistIcon", 
                  "isClearFirstAndLastSpaceChars", "isEmendIncorrectChars", "validSentenceStructureForFile", 
                  "validSentenceStructureForFileExtension", "isCorrectFileNameWithSearchAndReplaceTable", 
                  "isCorrectDoubleSpaceChars", "fileExtesionIs", "settingsVersion", "subDirectoryDeep", 
                  "isMoveToTrash", "maxRecordFileSize", "themeName", 
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
                  "iconNameFormat", "iconFileType", "pathOfMysqldSafe"
                  ]
    willNotReportSettings = ["amarokDBHost", "amarokDBPort", "amarokDBUser", 
                  "amarokDBPass", "amarokDBDB"]
        
    def checkStartupVariables():
        global MQtGui, MQtCore, isQt4Exist, MObjectName
        try:
            from PyQt4 import QtGui
            from PyQt4 import QtCore
            MObjectName = "PyQt4"
        except:
            try:
                from PySide import QtGui
                from PySide import QtCore
                MObjectName = "PySide"
            except:
                isQt4Exist = False
                return False
        MQtGui, MQtCore = QtGui, QtCore
        if MQtGui!=None and MQtCore!=None:
            isQt4Exist=True
            checkEncoding()

    def checkEncoding(_isSetUTF8=False):
        global defaultFileSystemEncoding
        from encodings import aliases
        if [str(v).lower().replace("_", "-") for k, v in aliases.aliases.iteritems()].count(defaultFileSystemEncoding)==0:
            if _isSetUTF8:
                defaultFileSystemEncoding = "utf-8"
            else:
                defaultFileSystemEncoding = sys.getdefaultencoding().lower()
                checkEncoding(True)

    def getDefaultValues():
        from datetime import datetime
        import Universals, InputOutputs
        if InputOutputs.getInstalledLanguagesCodes().count(str(MQtCore.QLocale.system().name()))>0:
            insLangCode = str(MQtCore.QLocale.system().name())
        else:
            insLangCode = "en_GB"
        myStyle , PlayerName, myObjectsName = "Plastique", getAvailablePlayers().pop(), getMyObjectsNames()[0]
        for stil in MQtGui.QStyleFactory.keys():
            if stil == "Oxygen":
                myStyle = str(stil)
                break
        return {
                "lastDirectory": unicode(Universals.userDirectoryPath).encode("utf-8"), 
                "isMainWindowMaximized": "False", 
                "isShowAdvancedSelections": "False", 
                "isShowOldValues": "False", 
                "isRunOnDoubleClick": "False", 
                "isChangeSelected": "False", 
                "isChangeAll": "True", 
                "isOpenDetailsInNewWindow": "False", 
                "hiddenFolderTableColumns": str([]), 
                "hiddenFileTableColumns": str([]), 
                "hiddenMusicTableColumns": str([]), 
                "hiddenSubFolderTableColumns": str([]), 
                "hiddenCoverTableColumns": str([]),
                "isPlayNow": "False", 
                "MainWindowGeometries": str([50, 50, 850, 533]), 
                "tableType": "2", 
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
                "mplayerAudioDevice": Universals.mplayerSoundDevices[0], 
                "isSaveActions": "True", 
                "fileSystemEncoding": defaultFileSystemEncoding, 
                "applicationStyle": myStyle, 
                "playerName": PlayerName, 
                "musicTagType": "ID3 V2", 
                "isMinimumWindowMode": "False", 
                "packagerUnneededFileExtensions": str(['pyc', 'py~', 'e4p', 'pro', 'pro.user', 'kdev4', 'kdevelop', 'kdevelop.pcs', 'kdevses', 'ts', 'anjuta']), 
                "packagerUnneededFiles": str(['.directory', '.project', '.bzrignore']), 
                "packagerUnneededDirectories": str(['.eric4project', '.svn', '.git', 'CVS', '.bzr', '.cache', '.settings']), 
                "lastUpdateControlDate": datetime.now().strftime("%Y %m %d %H %M %S"), 
                "updateInterval": "7", 
                "NeededObjectsName": myObjectsName, 
                "isActivePyKDE4": str(isAvailablePyKDE4()), 
                "isCloseOnCleanAndPackage": "True", 
                "TableToolsBarButtonStyle": "0", 
                "ToolsBarButtonStyle": "0", 
                "PlayerBarButtonStyle": "0", 
                "MusicOptionsBarButtonStyle": "0", 
                "SubDirectoryOptionsBarButtonStyle": "0",
                "CoverOptionsBarButtonStyle": "0",
                "language": insLangCode, 
                "isShowQuickMakeWindow": "True", 
                "isChangeExistIcon": "False", 
                "isClearFirstAndLastSpaceChars": "True", 
                "isEmendIncorrectChars": "True", 
                "validSentenceStructureForFile": "Title", 
                "validSentenceStructureForFileExtension": "All Small", 
                "isCorrectFileNameWithSearchAndReplaceTable": "True", 
                "isCorrectDoubleSpaceChars": "True", 
                "fileExtesionIs": "After The Last Point", 
                "settingsVersion": settingVersion,
                "subDirectoryDeep": "-1", 
                "isMoveToTrash": "False", 
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
                "windowMode": Universals.windowModeKeys[0], 
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
                "pathOfMysqldSafe": "mysqld_safe"
                }
                
    def getValueTypesAndValues():
        from datetime import datetime
        import Universals, InputOutputs
        return {
                "lastDirectory": "str", 
                "isMainWindowMaximized": "bool", 
                "isShowAdvancedSelections": "bool", 
                "isShowOldValues": "bool", 
                "isRunOnDoubleClick": "bool", 
                "isChangeSelected": "bool", 
                "isChangeAll": "bool", 
                "isOpenDetailsInNewWindow": "bool", 
                "hiddenFolderTableColumns": ["intList", range(0, 2)], 
                "hiddenFileTableColumns": ["intList", range(0, 2)], 
                "hiddenMusicTableColumns": ["intList", range(0, 10)], 
                "hiddenSubFolderTableColumns": ["intList", range(0, 2)], 
                "hiddenCoverTableColumns": ["intList", range(0, 2)], 
                "isPlayNow": "bool", 
                "MainWindowGeometries": ["intStaticListLen", 4], 
                "tableType": ["int", range(0, 5)], 
                "activeTabNoOfSpecialTools": ["int", range(0, 5)], 
                "unneededFiles": "list", 
                "ignoredFiles": "list", 
                "imageExtensions": "list", 
                "musicExtensions": "list", 
                "priorityIconNames": "list", 
                "unneededFileExtensions": "list", 
                "ignoredFileExtensions": "list", 
                "fileReNamerType": ["options", Universals.fileReNamerTypeNamesKeys], 
                "validSentenceStructure": ["options", Universals.validSentenceStructureKeys], 
                "mplayerPath": "str", 
                "mplayerArgs": "str", 
                "mplayerAudioDevicePointer": "str",
                "mplayerAudioDevice": ["options", Universals.mplayerSoundDevices], 
                "isSaveActions": "bool", 
                "fileSystemEncoding": ["options", getCharSets()], 
                "applicationStyle": ["options", getStyles()], 
                "playerName": ["options", getAvailablePlayers()], 
                "musicTagType": ["options", ["ID3 V1", "ID3 V2"]], 
                "isMinimumWindowMode": "bool", 
                "packagerUnneededFileExtensions": "list", 
                "packagerUnneededFiles": "list", 
                "packagerUnneededDirectories": "list", 
                "lastUpdateControlDate": "date", 
                "updateInterval": ["int", range(0, 32)], 
                "NeededObjectsName": ["options", ["PyQt4"]], 
                "isActivePyKDE4": "bool", 
                "isCloseOnCleanAndPackage": "bool", 
                "TableToolsBarButtonStyle": ["int", range(0, 4)], 
                "ToolsBarButtonStyle": ["int", range(0, 4)], 
                "PlayerBarButtonStyle": ["int", range(0, 4)], 
                "MusicOptionsBarButtonStyle": ["int", range(0, 4)], 
                "SubDirectoryOptionsBarButtonStyle": ["int", range(0, 4)], 
                "CoverOptionsBarButtonStyle": ["int", range(0, 4)], 
                "language": ["options", InputOutputs.getInstalledLanguagesCodes()], 
                "isShowQuickMakeWindow": "bool", 
                "isChangeExistIcon": "bool", 
                "isClearFirstAndLastSpaceChars": "bool", 
                "isEmendIncorrectChars": "bool", 
                "validSentenceStructureForFile": ["options", Universals.validSentenceStructureKeys], 
                "validSentenceStructureForFileExtension": ["options", Universals.validSentenceStructureKeys], 
                "isCorrectFileNameWithSearchAndReplaceTable": "bool", 
                "isCorrectDoubleSpaceChars": "bool", 
                "fileExtesionIs": ["options", Universals.fileExtesionIsKeys], 
                "settingsVersion": ["options", [settingVersion]],
                "subDirectoryDeep": ["int", range(-1, 10)], 
                "isMoveToTrash": "bool", 
                "maxRecordFileSize": "int", 
                "themeName": ["options", InputOutputs.getInstalledThemes()], 
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
                "remindMeLaterForUpdate": ["int", range(-1, 7)], 
                "remindMeLaterShowDateForUpdate": "date", 
                "isShowTransactionDetails": "bool", 
                "windowMode": ["options", Universals.windowModeKeys], 
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
                "pathOfMysqldSafe": "str"
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
        for k, v in aliases.aliases.iteritems():
            if charSets.count(v.replace("_", "-"))==0:
                charSets.append(v.replace("_", "-"))
        charSets.sort()
        return charSets
        
    def getStyles():
        styles = []
        for stil in MQtGui.QStyleFactory.keys(): 
            styles.append(str(stil))
        return styles
        
    def getScreenSize():
        if Universals.MainWindow!=None:
            return MQtGui.QDesktopWidget().screenGeometry()
        else:
            return None
        
    def getMyObjectsNames():
        myObjectsName = []
        try:
            import PyQt4
            myObjectsName.append("PyQt4")
        except:pass
        try:
            import PySide
            myObjectsName.append("PySide")
        except:pass
        return myObjectsName
        
    def isAvailablePyKDE4():
        try:
            import PyKDE4
            return True
        except:
            return False
        
    def getUserDesktopPath():
        import Universals
        if isAvailablePyKDE4():
            from PyKDE4.kdeui import KGlobalSettings
            desktopPath = str(KGlobalSettings.desktopPath())
        else:
            from MyObjects import translate
            desktopNames = [str(translate("Install","Desktop")), "Desktop"]
            for dirName in desktopNames:
                if InputOutputs.isDir(Universals.userDirectoryPath + "/" + dirName):
                    desktopPath = Universals.userDirectoryPath + "/" + dirName
                    break
                else:
                    desktopPath = Universals.userDirectoryPath
        return desktopPath
