# -*- coding: utf-8 -*-

import Variables
import Universals
import InputOutputs
from Databases import sqlite, getDefaultConnection, getAllDatabases, getDBPropertiesCreateQuery, reFillDatabases, getAmendedSQLInputQueries, checkDatabases
from Databases import BookmarksOfDirectories, BookmarksOfSpecialTools, SearchAndReplaceTable, CompleterTable
    
class Settings():
    global setting, saveUniversalSettings, emendValue, checkSettings, reFillSettings, reFillAll, makeBackUp, restoreBackUp, saveStateOfSettings, openStateOfSettings, updateOldSettings, universalSetting, getUniversalSetting, setUniversalSetting
    
    def setting():
        return Variables.MQtCore.QSettings((Universals.pathOfSettingsDirectory + "/" + Universals.fileOfSettings).decode("utf-8") ,Variables.MQtCore.QSettings.IniFormat)
    
    def universalSetting():
        return Variables.MQtCore.QSettings((Variables.userDirectoryPath+"/.HamsiApps/" + "universalSettings.ini").decode("utf-8") ,Variables.MQtCore.QSettings.IniFormat)
          
    def checkSettings():
        if InputOutputs.isDir(Universals.pathOfSettingsDirectory)==False:
            InputOutputs.makeDirs(Universals.pathOfSettingsDirectory)
            reFillSettings()
            reFillDatabases()
        else:
            if InputOutputs.isFile(Universals.pathOfSettingsDirectory + "/database.sqlite")==False:
                reFillDatabases()
            if InputOutputs.isFile(Universals.pathOfSettingsDirectory + "/" + Universals.fileOfSettings)==False:
                reFillSettings()
            checkDatabases()
        
    def saveUniversalSettings():
        mySetting = universalSetting()
        keysOfUniversalSettings = ["HamsiManagerPath"]
        values = [Variables.executableHamsiManagerPath]
        for x, keyValue in enumerate(keysOfUniversalSettings):
            if unicode(mySetting.value(keyValue).toString(), "utf-8") != values[x]:
                mySetting.setValue(keyValue,Variables.MQtCore.QVariant(values[x].decode("utf-8")))
                
    def getUniversalSetting(_key, _defaultValue):
        mySetting = universalSetting()
        value = unicode(mySetting.value(_key).toString(), "utf-8")
        if value == "":
            value = _defaultValue
        return value
    
    def setUniversalSetting(_key, _value):
        mySetting = universalSetting()
        mySetting.setValue(_key, Variables.MQtCore.QVariant(_value.decode("utf-8")))

    def reFillSettings(_makeBackUp=False):
        if _makeBackUp==True:
            makeBackUp("Settings")
        mySetting = Variables.MQtCore.QSettings((Universals.pathOfSettingsDirectory + "/" + Universals.fileOfSettings).decode("utf-8"), Variables.MQtCore.QSettings.IniFormat)
        defaultValues = Variables.getDefaultValues()
        for keyValue in Variables.keysOfSettings:
            mySetting.setValue(keyValue,Variables.MQtCore.QVariant(defaultValues[keyValue].decode("utf-8")))
    
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
        if InputOutputs.isDir(Universals.pathOfSettingsDirectory + "/" + _backUpDirectory)==False:
            InputOutputs.makeDirs(Universals.pathOfSettingsDirectory + "/" + _backUpDirectory)
        isReturn = False
        for file in files:
            if _newFileName=="mirror":
                newFileName = file
            elif _newFileName=="random":
                isReturn = True
                import random
                while 1==1:
                    newFileName = file[:file.find(".")] +"_"+ str(random.randrange(0, 100000000))+file[file.find("."):]
                    if InputOutputs.isFile(Universals.pathOfSettingsDirectory + "/" + _backUpDirectory+"/"+newFileName)==False:
                        break
            else:
                newFileName = _newFileName
            try:
                InputOutputs.removeFile(Universals.pathOfSettingsDirectory + "/" + _backUpDirectory+"/"+newFileName)
            except:pass
            try:
                InputOutputs.copyFileOrDir(Universals.pathOfSettingsDirectory + "/" + file, Universals.pathOfSettingsDirectory + "/" + _backUpDirectory+"/"+newFileName)
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
                oldInfo = InputOutputs.readFromFile(Universals.pathOfSettingsDirectory + "/" + file)
            else:
                try:
                    InputOutputs.removeFile(Universals.pathOfSettingsDirectory + "/" + file)
                except:pass
            try:
                if InputOutputs.isFile(Universals.pathOfSettingsDirectory + "/BackUps/"+file):
                    InputOutputs.moveFileOrDir(Universals.pathOfSettingsDirectory + "/BackUps/"+file, Universals.pathOfSettingsDirectory+file)
                else:
                    isSuccesfully = False
            except:pass
            if _isMakeBackUp==True:
                InputOutputs.writeToFile(Universals.pathOfSettingsDirectory + "/BackUps/"+file, oldInfo)
        return isSuccesfully

    def saveStateOfSettings(_file):
        import MyConfigure
        newFile = makeBackUp("Settings", "SettingFiles", "random")
        info = MyConfigure.getConfiguredDesktopFileContent(Variables.HamsiManagerDirectory)
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
        
    def updateOldSettings(_oldVersion):
        newSettingsKeys, changedDefaultValuesKeys = [], []
        try:
            oldVersion = int(_oldVersion)
        except:
            oldVersion = 807
        if oldVersion<810:
            con = sqlite.connect(Universals.pathOfSettingsDirectory + "/searchAndReplaceTable.sqlite")
            cur = con.cursor()
            cur.execute(str("ALTER TABLE searchAndReplaceTable RENAME TO tmpSearchAndReplaceTable;"))
            cur.execute(str("CREATE TABLE searchAndReplaceTable ('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,'searching' TEXT,'replacing' TEXT,'intIsActive' INTEGER,'intIsRegExp' INTEGER);"))
            cur.execute(str("INSERT INTO searchAndReplaceTable(searching,replacing,intIsActive,intIsRegExp) SELECT searching,replacing,1,0 FROM tmpSearchAndReplaceTable;"))
            cur.execute(str("DROP TABLE tmpSearchAndReplaceTable;"))
            con.commit()
        if oldVersion<811:
            con = sqlite.connect(Universals.pathOfSettingsDirectory + "/searchAndReplaceTable.sqlite")
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
            if InputOutputs.isFile(Universals.pathOfSettingsDirectory+"/LastState"):
                InputOutputs.removeFile(Universals.pathOfSettingsDirectory+"/LastState")
        if oldVersion<821:
            newSettingsKeys = newSettingsKeys + ["isDeleteEmptyDirectories", "isCleanerDeleteEmptyDirectories", "isPackagerDeleteEmptyDirectories"]
        if oldVersion<822:
            if Variables.isAvailableKDE4():
                if InputOutputs.isFile(Variables.getKDE4HomePath() + "/share/config/HamsiManagerrc"):
                    InputOutputs.removeFile(Variables.getKDE4HomePath() + "/share/config/HamsiManagerrc")
        if oldVersion<840:
            try:
                con = sqlite.connect(Universals.pathOfSettingsDirectory + "/bookmarks.sqlite")
                cur = con.cursor()
                cur.execute("SELECT * FROM dbProperties where keyName='version'")
                bookmarksDBVersion = int(cur.fetchall()[0][1])
            except:
                bookmarksDBVersion = 0
            try:
                con = sqlite.connect(Universals.pathOfSettingsDirectory + "/searchAndReplaceTable.sqlite")
                cur = con.cursor()
                cur.execute("SELECT * FROM dbProperties where keyName='version'")
                searchAndReplaceTableDBVersion = int(cur.fetchall()[0][1])
            except:
                searchAndReplaceTableDBVersion = 0
            if bookmarksDBVersion<1:
                con = sqlite.connect(Universals.pathOfSettingsDirectory + "/bookmarks.sqlite")
                cur = con.cursor()
                cur.execute(str("CREATE TABLE dbProperties ('keyName' TEXT NOT NULL,'value' TEXT);"))
                cur.execute(str("insert into dbProperties (keyName, value) values ('version', '1');"))
                con.commit()
            if searchAndReplaceTableDBVersion<1:
                con = sqlite.connect(Universals.pathOfSettingsDirectory + "/searchAndReplaceTable.sqlite")
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
            con = sqlite.connect(Universals.pathOfSettingsDirectory + "/bookmarks.sqlite")
            cur = con.cursor()
            cur.execute(str("insert into bookmarksOfSpecialTools (bookmark, value, label) values ('', 'Directory Name , Directory  ;right;102', 'cover')"))
            cur.execute(str("insert into bookmarksOfSpecialTools (bookmark, value, label) values ('', 'Source Cover , Current Cover  ;right;102', 'cover')"))
            cur.execute(str("insert into bookmarksOfSpecialTools (bookmark, value, label) values ('', 'Destination Cover , Source Cover  ;right;102', 'cover')"))
            cur.execute(str("insert into bookmarksOfSpecialTools (bookmark, value, label) values ('', 'Destination Cover , Current Cover  ;right;102', 'cover')"))
            con.commit()
        if oldVersion<905:
            conNewDB = getDefaultConnection()
            con = sqlite.connect(Universals.pathOfSettingsDirectory + "/bookmarks.sqlite")
            cur = con.cursor()
            cur.execute("SELECT bookmark,value FROM bookmarksOfDirectories")
            for row in cur.fetchall():
                cur = conNewDB.cursor()
                sqlCommands = getAmendedSQLInputQueries("bookmarksOfDirectories", {"bookmark" : "'" + row[0] + "'", "value" : "'" + row[1] + "'"}, ["value"])
                for sqlCommand in sqlCommands:
                    cur.execute(str(sqlCommand))
                conNewDB.commit()
            con = sqlite.connect(Universals.pathOfSettingsDirectory + "/bookmarks.sqlite")
            cur = con.cursor()
            cur.execute("SELECT bookmark,value,label FROM bookmarksOfSpecialTools")
            for row in cur.fetchall():
                cur = conNewDB.cursor()
                sqlCommands = getAmendedSQLInputQueries("bookmarksOfSpecialTools", {"bookmark" : "'" + row[0] + "'", "value" : "'" + row[1] + "'", "type" : "'" + row[2] + "'"}, ["value"])
                for sqlCommand in sqlCommands:
                    cur.execute(str(sqlCommand))
                conNewDB.commit()
            con = sqlite.connect(Universals.pathOfSettingsDirectory + "/searchAndReplaceTable.sqlite")
            cur = con.cursor()
            cur.execute("SELECT searching,replacing,intIsActive,intIsCaseSensitive,intIsRegExp FROM searchAndReplaceTable")
            for row in cur.fetchall():
                cur = conNewDB.cursor()
                sqlCommands = getAmendedSQLInputQueries("searchAndReplaceTable", {"searching" : "'" + row[0] + "'", "replacing" : "'" + row[1] + "'", "intIsActive" : str(row[2]), "intIsCaseSensitive" : str(row[3]), "intIsRegExp" : str(row[4])}, ["searching", "replacing"])
                for sqlCommand in sqlCommands:
                    cur.execute(str(sqlCommand))
                conNewDB.commit()
        if oldVersion<906:
            sets = setting()
            sets.setValue("fileSystemEncoding", Variables.MQtCore.QVariant(sets.value("systemsCharSet").toString()))
        if oldVersion<907:
            newSettingsKeys = newSettingsKeys + ["isActiveCompleter", "isShowAllForCompleter"]
        return newSettingsKeys, changedDefaultValuesKeys
        
