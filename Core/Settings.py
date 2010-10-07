# -*- coding: utf-8 -*-

import os, sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
#from PySide.QtGui import *
#from PySide.QtCore import *
from datetime import datetime
if float(sys.version[:3])>=2.6:
    import sqlite3 as sqlite
else:
    from pysqlite2 import dbapi2 as sqlite

try:defaultFileSystemEncoding = sys.getfilesystemencoding().lower()
except:defaultFileSystemEncoding = sys.getdefaultencoding().lower()

from encodings import aliases
def checkEncoding(_isSetUTF8=False):
    global defaultFileSystemEncoding
    if [str(v).lower().replace("_", "-") for k, v in aliases.aliases.iteritems()].count(defaultFileSystemEncoding)==0:
        if _isSetUTF8:
            defaultFileSystemEncoding = "utf-8"
        else:
            defaultFileSystemEncoding = sys.getdefaultencoding().lower()
            checkEncoding(True)
checkEncoding()

import Universals
import InputOutputs
import RoutineChecks
    
class Settings():
    global setting, bookmarksOfDirectories, bookmarksOfSpecialTools, searchAndReplaceTable, saveUniversalSettings, reFillDatabases, getCharSets, getStyles, emendValue, getDefaultValues, getValueTypesAndValues, checkSettings, reFillSettings, reFillAll, isMakeBackUp, makeBackUp, restoreBackUp, keysOfSettings, codesOfUser, reFillCodesOfUser, fileOfSettings, saveStateOfSettings, openStateOfSettings, getAvailablePlayers, getMyObjectsNames, isAvailablePyKDE4, pathOfSettingsDirectory, setPathOfSettingsDirectory, getUserDesktopPath, updateOldSettings, recordFilePath, universalSetting, checkDatabases, getScreenSize, getUniversalSetting, setUniversalSetting
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
                  "mplayerAudioDevice", "isSaveActions", "systemsCharSet", 
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
                  "amarokDBHost", "amarokDBPort", "amarokDBUser", "amarokDBPass", "amarokDBDB"
                  ]
    fileOfSettings = "mySettings.ini"
    pathOfSettingsDirectory = Universals.userDirectoryPath+"/.HamsiApps/HamsiManager/"
    recordFilePath = pathOfSettingsDirectory + "logs.txt"
    
    def setPathOfSettingsDirectory(_path):
        global pathOfSettingsDirectory
        _path = str(_path)
        if _path[-1]!="/":
            _path = _path + "/"
        pathOfSettingsDirectory = _path
    
    def setting():
        return QSettings((pathOfSettingsDirectory + fileOfSettings).decode("utf-8") ,QSettings.IniFormat)
    
    def universalSetting():
        return QSettings((Universals.userDirectoryPath+"/.HamsiApps/" + "universalSettings.ini").decode("utf-8") ,QSettings.IniFormat)
          
    def bookmarksOfDirectories(_action="read", _value0="", _value1="", _value2="", _value3=""):
        con = sqlite.connect(pathOfSettingsDirectory + "bookmarks.sqlite")
        cur = con.cursor()
        if _action=="read":
            try:
                cur.execute("SELECT * FROM bookmarksOfDirectories")
                return cur.fetchall()
            except: return []
        elif _action=="readOneRecord":
            try:
                cur.execute("SELECT * FROM bookmarksOfDirectories where id="+str(_value0))
                return cur.fetchall()
            except: return []
        elif _action=="add":
            _value0 = _value0.replace("'", "''")
            _value1 = _value1.replace("'", "''")
            _value2 = _value2.replace("'", "''")
            cur.execute("insert into bookmarksOfDirectories(bookmark,value,label) values('"+_value0+"','" + _value1+"','"+_value2+"')")
        elif _action=="delete":
            cur.execute("delete from bookmarksOfDirectories where id="+str(_value0))
        elif _action=="update":
            _value1 = _value1.replace("'", "''")
            _value2 = _value2.replace("'", "''")
            cur.execute(str("update bookmarksOfDirectories set bookmark='"+_value1+"', value='"+_value2+"', label='"+_value3+"' where id="+str(_value0)))
        con.commit()
        
    def bookmarksOfSpecialTools(_action="read", _value0="", _value1="", _value2="", _value3=""):
        con = sqlite.connect(pathOfSettingsDirectory + "bookmarks.sqlite")
        cur = con.cursor()
        import Organizer
        requirement = Universals.MainWindow.Table.specialTollsBookmarkPointer
        if _action=="read":
            try:
                cur.execute("SELECT * FROM bookmarksOfSpecialTools where label='"+requirement+"'")
                myBookmarks = []
                for mybm in cur.fetchall():
                    tempT = mybm[2]
                    tempString = tempT.split(";")
                    tempT = ""
                    for t in tempString[:-2]:
                        tempT+=t
                    newText  = Organizer.whatDoesSpecialCommandDo("-",
                                    tempString[-2],
                                    tempT, False, True)
                    myBookmarks.append([mybm[0], newText, mybm[2], mybm[3]])
                return myBookmarks
            except: return []
        if _action=="add":
            _value0 = _value0.replace("'", "''")
            _value1 = _value1.replace("'", "''")
            cur.execute("insert into bookmarksOfSpecialTools(bookmark,value,label) values('"+_value0+"','"+_value1+"','"+requirement+"')")
        if _action=="delete":
            cur.execute("delete from bookmarksOfSpecialTools where value='"+_value0+"' and label='"+requirement+"'")
        if _action=="update":
            _value1 = _value1.replace("'", "''")
            _value2 = _value2.replace("'", "''")
            cur.execute(str("update bookmarksOfSpecialTools set bookmark='"+_value1+"', value='"+_value2+"' where id="+str(_value0)))
        con.commit()
        
    def searchAndReplaceTable(_action="read", _value0="", _value1="", _value2="", _value3="", _value4="", _value5=""):
        con = sqlite.connect(pathOfSettingsDirectory + "searchAndReplaceTable.sqlite")
        cur = con.cursor()
        if _action=="read":
            try:
                cur.execute("SELECT * FROM searchAndReplaceTable")
                return cur.fetchall()
            except: return []
        if _action=="add":
            _value0 = _value0.replace("'", "''")
            _value1 = _value1.replace("'", "''")
            cur.execute("insert into searchAndReplaceTable(searching,replacing,intIsActive,intIsCaseSensitive,intIsRegExp) values('"+_value0+"','"+_value1+"',"+str(_value2)+","+str(_value3)+","+str(_value4)+")")
            cur.execute("SELECT last_insert_rowid();")
            con.commit()
            return cur.fetchall()[0][0]
        if _action=="delete":
            cur.execute("delete from searchAndReplaceTable where id="+str(_value0))
        if _action=="update":
            _value1 = _value1.replace("'", "''")
            _value2 = _value2.replace("'", "''")
            cur.execute(str("update searchAndReplaceTable set searching='"+_value1+"', replacing='"+_value2+"', intIsActive="+str(_value3)+", intIsCaseSensitive="+str(_value4)+", intIsRegExp="+str(_value5)+" where id="+str(_value0)))
        con.commit()
    
    def checkSettings():
        if os.path.isdir(os.path.dirname(pathOfSettingsDirectory[:-1]))==False:
            os.mkdir(os.path.dirname(pathOfSettingsDirectory[:-1]))
        if os.path.isdir(pathOfSettingsDirectory[:-1])==False:
            os.mkdir(pathOfSettingsDirectory[:-1])
            os.mkdir(pathOfSettingsDirectory + "SettingFiles")
            os.mkdir(pathOfSettingsDirectory + "BackUps")
            reFillSettings()
            reFillDatabases("All")
            reFillCodesOfUser()
        else:
            if os.path.isfile(pathOfSettingsDirectory + "bookmarks.sqlite")==False:
                reFillDatabases("bookmarks")
            if os.path.isfile(pathOfSettingsDirectory + "searchAndReplaceTable.sqlite")==False:
                reFillDatabases("searchAndReplaceTable")
            if os.path.isfile(pathOfSettingsDirectory + "codesOfUser.py")==False:
                reFillCodesOfUser()
            if os.path.isfile(pathOfSettingsDirectory + fileOfSettings)==False:
                reFillSettings()
        
    def saveUniversalSettings():
        mySetting = universalSetting()
        keysOfUniversalSettings = ["HamsiManagerPath"]
        values = [Universals.executableHamsiManagerPath]
        for x, keyValue in enumerate(keysOfUniversalSettings):
            if unicode(mySetting.value(keyValue).toString(), "utf-8") != values[x]:
                mySetting.setValue(keyValue,QVariant(values[x].decode("utf-8")))
                
    def getUniversalSetting(_key, _defaultValue):
        mySetting = universalSetting()
        value = unicode(mySetting.value(_key).toString(), "utf-8")
        if value == "":
            value = _defaultValue
        return value
    
    def setUniversalSetting(_key, _value):
        mySetting = universalSetting()
        mySetting.setValue(_key, QVariant(_value.decode("utf-8")))

    def reFillSettings(_askMakeBackUp=False, _makeBackUp=False):
        if _askMakeBackUp==True:
            isMakeBackUp("Settings")
        elif _makeBackUp==True:
            makeBackUp("Settings")
        mySetting = QSettings((pathOfSettingsDirectory + fileOfSettings).decode("utf-8"), QSettings.IniFormat)
        defaultValues = getDefaultValues()
        for keyValue in keysOfSettings:
            mySetting.setValue(keyValue,QVariant(defaultValues[keyValue].decode("utf-8")))
    
    def getDefaultValues():
        if InputOutputs.getInstalledLanguagesCodes().count(str(QLocale.system().name()))>0:
            insLangCode = str(QLocale.system().name())
        else:
            insLangCode = "en_GB"
        myStyle , PlayerName, myObjectsName = "Plastique", getAvailablePlayers().pop(), getMyObjectsNames()[0]
        for stil in QStyleFactory.keys():
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
                "systemsCharSet": defaultFileSystemEncoding, 
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
                "settingsVersion": RoutineChecks.__settingVersion__, 
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
                "amarokDBDB": "amarokdb"
                }
                
    def getValueTypesAndValues():
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
                "systemsCharSet": ["options", getCharSets()], 
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
                "settingsVersion": ["options", [RoutineChecks.__settingVersion__]], 
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
                "amarokDBDB": "str"
                }
   
    def emendValue(_keyOfSetting, _value, _defaultValue = None, _valueTypesAndValue = None):
        if _valueTypesAndValue==None:
            _valueTypesAndValue = getValueTypesAndValues()[_keyOfSetting]
        if _defaultValue==None:
            _defaultValue = getDefaultValues()[_keyOfSetting]
        if _valueTypesAndValue=="bool":
            try:
                eval(str(_value).title())
            except: 
                return _defaultValue
        elif _valueTypesAndValue == "date":
            try:
                datetime.strptime(str(_value), "%Y %m %d %H %M %S")
            except: 
                return _defaultValue
        elif _valueTypesAndValue=="list":
            try:
                value = "['"
                for x, ext in enumerate(Universals.getListFromStrint(_value)):
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
                for x, ext in enumerate(Universals.getListFromStrint(_value)):
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
        
    def reFillDatabases(_table="", _askMakeBackUp=False, _makeBackUp=False):
        if _askMakeBackUp==True:
            isMakeBackUp(_table)
        elif _makeBackUp==True:
            makeBackUp(_table)
        sqlCommands , databaseFiles= [], []
        if _table=="bookmarksOfDirectories" or _table=="bookmarks" or _table=="All":
            sqlCommands.append(["CREATE TABLE bookmarksOfDirectories ('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,'bookmark' TEXT,'value' TEXT,'label' TEXT)", 
                                "insert into bookmarksOfDirectories(bookmark,value,label) values('Home','"+Universals.userDirectoryPath+"','')", 
                                "insert into bookmarksOfDirectories(bookmark,value,label) values('MNT','/mnt','')", 
                                "insert into bookmarksOfDirectories(bookmark,value,label) values('MEDIA','/media','')"])
            databaseFiles.append("bookmarks.sqlite")
        if _table=="bookmarksOfSpecialTools" or _table=="bookmarks" or _table=="All":
            if len(sqlCommands)==0:
                sqlCommands.append(["SELECT 'control'"])
            sqlCommands[-1] += ["CREATE TABLE bookmarksOfSpecialTools ('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,'bookmark' TEXT,'value' TEXT,'label' TEXT)", 
                                "insert into bookmarksOfSpecialTools (bookmark, value, label) values ('', 'File Name , Artist - Title ;right;113', 'music')",
                                "insert into bookmarksOfSpecialTools (bookmark, value, label) values ('', 'Artist - Title , File Name  ;left;113', 'music')",
                                "insert into bookmarksOfSpecialTools (bookmark, value, label) values ('', 'Track No - Title , File Name  ;left;113', 'music')",
                                "insert into bookmarksOfSpecialTools (bookmark, value, label) values ('', 'Artist - Album , Directory  ;left;113', 'music')",
                                "insert into bookmarksOfSpecialTools (bookmark, value, label) values ('', 'File Name , Title  ;right;102', 'music')",
                                "insert into bookmarksOfSpecialTools (bookmark, value, label) values ('', 'Title , File Name  ;right;102', 'music')",
                                "insert into bookmarksOfSpecialTools (bookmark, value, label) values ('', 'Year , Album  ;right;102', 'music')",
                                "insert into bookmarksOfSpecialTools (bookmark, value, label) values ('', 'Lyrics , Artist - Title  ;right;113', 'music')",
                                "insert into bookmarksOfSpecialTools (bookmark, value, label) values ('', 'Directory - File Name , Directory  ;left;113', 'file')",
                                "insert into bookmarksOfSpecialTools (bookmark, value, label) values ('', 'Artist - Album - Title , File Name  ;left;124', 'music')",
                                "insert into bookmarksOfSpecialTools (bookmark, value, label) values ('', 'Directory , File/Directory Name  ;right;102', 'directory')",
                                "insert into bookmarksOfSpecialTools (bookmark, value, label) values ('', 'File/Directory Name , Directory  ;right;102', 'directory')",
                                "insert into bookmarksOfSpecialTools (bookmark, value, label) values ('', 'Directory , File Name  ;right;102', 'subfolder')",
                                "insert into bookmarksOfSpecialTools (bookmark, value, label) values ('', 'File Name , Directory  ;right;102', 'subfolder')",
                                "insert into bookmarksOfSpecialTools (bookmark, value, label) values ('', 'Directory , File Name  ;right;102', 'file')",
                                "insert into bookmarksOfSpecialTools (bookmark, value, label) values ('', 'File Name , Directory  ;right;102', 'file')", 
                                "insert into bookmarksOfSpecialTools (bookmark, value, label) values ('', 'Directory Name , Directory  ;right;102', 'cover')", 
                                "insert into bookmarksOfSpecialTools (bookmark, value, label) values ('', 'Source Cover , Current Cover  ;right;102', 'cover')", 
                                "insert into bookmarksOfSpecialTools (bookmark, value, label) values ('', 'Destination Cover , Source Cover  ;right;102', 'cover')", 
                                "insert into bookmarksOfSpecialTools (bookmark, value, label) values ('', 'Destination Cover , Current Cover  ;right;102', 'cover')"]
        if _table=="bookmarksOfDirectories" or _table=="bookmarksOfSpecialTools" or _table=="bookmarks" or _table=="All":
            sqlCommands[-1] += ["CREATE TABLE dbProperties ('keyName' TEXT NOT NULL,'value' TEXT)", 
                                "insert into dbProperties (keyName, value) values ('version', '1')"]
        if _table=="searchAndReplaceTable" or _table=="All":
            sqlCommands.append(["CREATE TABLE searchAndReplaceTable ('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,'searching' TEXT,'replacing' TEXT,'intIsActive' INTEGER,'intIsCaseSensitive' INTEGER,'intIsRegExp' INTEGER)", 
                                "insert into searchAndReplaceTable (searching,replacing,intIsActive,intIsCaseSensitive,intIsRegExp) values('http://','',1,1,0)", 
                                "insert into searchAndReplaceTable (searching,replacing,intIsActive,intIsCaseSensitive,intIsRegExp) values('www','',1,1,0)",
                                "CREATE TABLE dbProperties ('keyName' TEXT NOT NULL,'value' TEXT)", 
                                "insert into dbProperties (keyName, value) values ('version', '1')"])
            databaseFiles.append("searchAndReplaceTable.sqlite")
        for sqlCommandNo, sqlCommand in enumerate(sqlCommands):
            try:InputOutputs.removeFile(pathOfSettingsDirectory+databaseFiles[sqlCommandNo])
            except:pass
            con = sqlite.connect(pathOfSettingsDirectory+databaseFiles[sqlCommandNo])
            for s in sqlCommand:
                cur = con.cursor()
                cur.execute(str(s))
                con.commit()
                
    def reFillAll(_askMakeBackUp=False, _makeBackUp=False):
        if _askMakeBackUp==True:
            isMakeBackUp()
        elif _makeBackUp==True:
            makeBackUp("All")
        reFillDatabases("All")
        reFillSettings()
        
    def isMakeBackUp(_settingType="All"):
        import Dialogs
        from MyObjects import translate
        answer = Dialogs.ask(translate("Settings", "Do You Want To Back Up?"),
                    translate("Settings", "Do you want to back up current data?"))
        if answer==Dialogs.Yes:
            makeBackUp(_settingType)
        
    def makeBackUp(_settingType="All", _backUpDirectory="BackUps", _newFileName="mirror"):
        files = []
        if _settingType=="bookmarks" or _settingType=="All":
            files.append("bookmarks.sqlite")
        if _settingType=="searchAndReplaceTable" or _settingType=="All":
            files.append("searchAndReplaceTable")
        if _settingType=="Settings" or _settingType=="All":
            files.append(fileOfSettings)
        try:
            InputOutputs.makeDirs(pathOfSettingsDirectory+_backUpDirectory)
        except:pass
        isReturn = False
        for file in files:
            if _newFileName=="mirror":
                newFileName = file
            elif _newFileName=="random":
                isReturn = True
                import random
                while 1==1:
                    newFileName = file[:file.find(".")] +"_"+ str(random.randrange(0, 100000000))+file[file.find("."):]
                    if InputOutputs.isFile(pathOfSettingsDirectory+_backUpDirectory+"/"+newFileName)==False:
                        break
            else:
                newFileName = _newFileName
            try:
                InputOutputs.removeFile(pathOfSettingsDirectory+_backUpDirectory+"/"+newFileName)
            except:pass
            try:
                InputOutputs.copyFileOrDir(pathOfSettingsDirectory+file, pathOfSettingsDirectory+_backUpDirectory+"/"+newFileName)
                if isReturn==True:
                    return newFileName
            except:pass
        
    def restoreBackUp(_settingType="All"):
        import Dialogs
        from MyObjects import translate
        answer = Dialogs.ask(translate("Settings", "Do You Want To Back Up Current Data?"),
                        translate("Settings", "Do you want to back up current data before restoring?"), True)
        isMake = False
        if answer==Dialogs.Yes:
            isMake = True
        elif answer==Dialogs.Cancel:
            return False
        files = []
        if _settingType=="bookmarks" or _settingType=="All":
            files.append("bookmarks.sqlite")
        if _settingType=="searchAndReplaceTable" or _settingType=="All":
            files.append("searchAndReplaceTable.sqlite")
        if _settingType=="Settings" or _settingType=="All":
            files.append(fileOfSettings)
        for file in files:
            if isMake==True:
                oldInfo = InputOutputs.readFromFile(pathOfSettingsDirectory+file)
            else:
                try:
                    InputOutputs.removeFile(pathOfSettingsDirectory+file)
                except:pass
            try:
                if InputOutputs.isFile(pathOfSettingsDirectory + "BackUps/"+file):
                    InputOutputs.moveFileOrDir(pathOfSettingsDirectory + "BackUps/"+file, pathOfSettingsDirectory+file)
                else:
                    Dialogs.showError("There Is No Back Up", "No back up file found to restore.")
                    return False
            except:pass
            if isMake==True:
                InputOutputs.writeToFile(pathOfSettingsDirectory + "BackUps/"+file, oldInfo)
        return True
    
    def codesOfUser(_codes=""):
        if _codes=="":
            return InputOutputs.readFromFile(pathOfSettingsDirectory + "codesOfUser.py")
        else:
            InputOutputs.writeToFile(pathOfSettingsDirectory + "codesOfUser.py", _codes)
            
    def reFillCodesOfUser():
        f = open(pathOfSettingsDirectory + "codesOfUser.py", "w")
        f.write("#!/usr/bin/env python\n" +
                            "# -*- coding: utf-8 -*-\n"+
                            "\n"+
                            "#You can type and execute the commands you wish to run here.\n"+
                            "#You can get detailed information from our official website.\n"+
                            "import Dialogs\nDialogs.show(\"This is an example\",\"You can develop the examples as you wish.\")"+
                            "\n\n\n\n\n\n\n\n\n")
        f.close()


    def saveStateOfSettings(_file):
        import MyConfigure
        newFile = makeBackUp("Settings", "SettingFiles", "random")
        info = MyConfigure.getConfiguredDesktopFileContent(Universals.HamsiManagerDirectory)
        newInfo = []
        for rowNo, row in enumerate(info):
            if row [:4]=="Exec":
                row  = row[:-1] + " -s " + newFile + "\n"
            newInfo.append(row )
        info = ""
        for row  in newInfo:
            info += row 
        InputOutputs.writeToFile(_file, info)
        
    def openStateOfSettings(_file):
        import Execute
        for rowNo, row in enumerate(InputOutputs.readLinesFromFile(_file)):
            if row [:5]=="Exec=":
                t = Execute.execute(row[5:])
                Universals.HamsiManagerApp.closeAllWindows()
                break
        
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
        charSets = []
        for k, v in aliases.aliases.iteritems():
            if charSets.count(v.replace("_", "-"))==0:
                charSets.append(v.replace("_", "-"))
        charSets.sort()
        return charSets
        
    def getStyles():
        styles = []
        for stil in QStyleFactory.keys(): 
            styles.append(str(stil))
        return styles
        
    def getScreenSize():
        if Universals.MainWindow!=None:
            return QDesktopWidget().screenGeometry()
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
        
    def updateOldSettings(_oldVersion):
        newSettingsKeys, changedDefaultValuesKeys = [], []
        try:
            oldVersion = int(_oldVersion)
        except:
            oldVersion = 807
        if oldVersion<810:
            con = sqlite.connect(pathOfSettingsDirectory + "searchAndReplaceTable.sqlite")
            cur = con.cursor()
            cur.execute(str("ALTER TABLE searchAndReplaceTable RENAME TO tmpSearchAndReplaceTable;"))
            cur.execute(str("CREATE TABLE searchAndReplaceTable ('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,'searching' TEXT,'replacing' TEXT,'intIsActive' INTEGER,'intIsRegExp' INTEGER);"))
            cur.execute(str("INSERT INTO searchAndReplaceTable(searching,replacing,intIsActive,intIsRegExp) SELECT searching,replacing,1,0 FROM tmpSearchAndReplaceTable;"))
            cur.execute(str("DROP TABLE tmpSearchAndReplaceTable;"))
            con.commit()
        if oldVersion<811:
            con = sqlite.connect(pathOfSettingsDirectory + "searchAndReplaceTable.sqlite")
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
            if InputOutputs.isFile(pathOfSettingsDirectory+"LastState"):
                InputOutputs.removeFile(pathOfSettingsDirectory+"LastState")
        if oldVersion<821:
            newSettingsKeys = newSettingsKeys + ["isDeleteEmptyDirectories", "isCleanerDeleteEmptyDirectories", "isPackagerDeleteEmptyDirectories"]
        if oldVersion<822:
            if InputOutputs.isFile(Universals.getKDE4HomePath() + "share/config/HamsiManagerrc"):
                InputOutputs.removeFile(Universals.getKDE4HomePath() + "share/config/HamsiManagerrc")
        if oldVersion<840:
            try:
                con = sqlite.connect(pathOfSettingsDirectory + "bookmarks.sqlite")
                cur = con.cursor()
                cur.execute("SELECT * FROM dbProperties where keyName='version'")
                bookmarksDBVersion = int(cur.fetchall()[0][1])
            except:
                bookmarksDBVersion = 0
            try:
                con = sqlite.connect(pathOfSettingsDirectory + "searchAndReplaceTable.sqlite")
                cur = con.cursor()
                cur.execute("SELECT * FROM dbProperties where keyName='version'")
                searchAndReplaceTableDBVersion = int(cur.fetchall()[0][1])
            except:
                searchAndReplaceTableDBVersion = 0
            if bookmarksDBVersion<1:
                con = sqlite.connect(pathOfSettingsDirectory + "bookmarks.sqlite")
                cur = con.cursor()
                cur.execute(str("CREATE TABLE dbProperties ('keyName' TEXT NOT NULL,'value' TEXT);"))
                cur.execute(str("insert into dbProperties (keyName, value) values ('version', '1');"))
                con.commit()
            if searchAndReplaceTableDBVersion<1:
                con = sqlite.connect(pathOfSettingsDirectory + "searchAndReplaceTable.sqlite")
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
            con = sqlite.connect(pathOfSettingsDirectory + "bookmarks.sqlite")
            cur = con.cursor()
            cur.execute(str("insert into bookmarksOfSpecialTools (bookmark, value, label) values ('', 'Directory Name , Directory  ;right;102', 'cover')"))
            cur.execute(str("insert into bookmarksOfSpecialTools (bookmark, value, label) values ('', 'Source Cover , Current Cover  ;right;102', 'cover')"))
            cur.execute(str("insert into bookmarksOfSpecialTools (bookmark, value, label) values ('', 'Destination Cover , Source Cover  ;right;102', 'cover')"))
            cur.execute(str("insert into bookmarksOfSpecialTools (bookmark, value, label) values ('', 'Destination Cover , Current Cover  ;right;102', 'cover')"))
            con.commit()
        return newSettingsKeys, changedDefaultValuesKeys
        
    def checkDatabases():
        try:
            con = sqlite.connect(pathOfSettingsDirectory + "bookmarks.sqlite")
            cur = con.cursor()
            cur.execute("SELECT * FROM bookmarksOfDirectories")
        except:
            reFillDatabases("bookmarksOfDirectories")
        try:
            con = sqlite.connect(pathOfSettingsDirectory + "bookmarks.sqlite")
            cur = con.cursor()
            cur.execute("SELECT * FROM bookmarksOfSpecialTools")
        except:
            reFillDatabases("bookmarksOfSpecialTools")
        try:
            con = sqlite.connect(pathOfSettingsDirectory + "searchAndReplaceTable.sqlite")
            cur = con.cursor()
            cur.execute("SELECT * FROM searchAndReplaceTable")
        except:
            reFillDatabases("searchAndReplaceTable")
        try:
            con = sqlite.connect(pathOfSettingsDirectory + "bookmarks.sqlite")
            cur = con.cursor()
            cur.execute("SELECT * FROM dbProperties where keyName='version'")
            bookmarksDBVersion = int(cur.fetchall()[0][1])
        except:
            bookmarksDBVersion = 0
        try:
            con = sqlite.connect(pathOfSettingsDirectory + "searchAndReplaceTable.sqlite")
            cur = con.cursor()
            cur.execute("SELECT * FROM dbProperties where keyName='version'")
            searchAndReplaceTableDBVersion = int(cur.fetchall()[0][1])
        except:
            searchAndReplaceTableDBVersion = 0
            try:
                con = sqlite.connect(pathOfSettingsDirectory + "searchAndReplaceTable.sqlite")
                cur = con.cursor()
                cur.execute("SELECT id,searching,replacing,intIsActive,intIsCaseSensitive,intIsRegExp FROM searchAndReplaceTable")
            except:
                con = sqlite.connect(pathOfSettingsDirectory + "searchAndReplaceTable.sqlite")
                cur = con.cursor()
                cur.execute(str("ALTER TABLE searchAndReplaceTable RENAME TO tmpSearchAndReplaceTable;"))
                cur.execute(str("CREATE TABLE searchAndReplaceTable ('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,'searching' TEXT,'replacing' TEXT,'intIsActive' INTEGER,'intIsCaseSensitive' INTEGER,'intIsRegExp' INTEGER);"))
                cur.execute(str("INSERT INTO searchAndReplaceTable(searching,replacing,intIsActive,intIsCaseSensitive,intIsRegExp) SELECT searching,replacing,1,1,0 FROM tmpSearchAndReplaceTable;"))
                cur.execute(str("DROP TABLE tmpSearchAndReplaceTable;"))
                con.commit()
        if bookmarksDBVersion<1:
            con = sqlite.connect(pathOfSettingsDirectory + "bookmarks.sqlite")
            cur = con.cursor()
            cur.execute(str("CREATE TABLE dbProperties ('keyName' TEXT NOT NULL,'value' TEXT);"))
            cur.execute(str("insert into dbProperties (keyName, value) values ('version', '1');"))
            con.commit()
        if searchAndReplaceTableDBVersion<1:
            con = sqlite.connect(pathOfSettingsDirectory + "searchAndReplaceTable.sqlite")
            cur = con.cursor()
            cur.execute(str("CREATE TABLE dbProperties ('keyName' TEXT NOT NULL,'value' TEXT);"))
            cur.execute(str("insert into dbProperties (keyName, value) values ('version', '1');"))
            con.commit()
