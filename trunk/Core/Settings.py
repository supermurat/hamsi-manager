# -*- coding: utf-8 -*-

import os, sys
from datetime import datetime
if float(sys.version[:3])>=2.6:
    import sqlite3 as sqlite
else:
    from pysqlite2 import dbapi2 as sqlite

import Variables
import Universals
import InputOutputs
import RoutineChecks
    
class Settings():
    global setting, bookmarksOfDirectories, bookmarksOfSpecialTools, searchAndReplaceTable, saveUniversalSettings, reFillDatabases, emendValue, checkSettings, reFillSettings, reFillAll, isMakeBackUp, makeBackUp, restoreBackUp, fileOfSettings, saveStateOfSettings, openStateOfSettings, updateOldSettings, recordFilePath, universalSetting, checkDatabases, getUniversalSetting, setUniversalSetting, getAmendedSQLInputQueries
    fileOfSettings = "mySettings.ini"
    recordFilePath = Universals.pathOfSettingsDirectory + "/logs.txt"
    
    def setting():
        return Variables.MQtCore.QSettings((Universals.pathOfSettingsDirectory + "/" + fileOfSettings).decode("utf-8") ,Variables.MQtCore.QSettings.IniFormat)
    
    def universalSetting():
        return Variables.MQtCore.QSettings((Variables.userDirectoryPath+"/.HamsiApps/" + "universalSettings.ini").decode("utf-8") ,Variables.MQtCore.QSettings.IniFormat)
          
    def bookmarksOfDirectories(_action="read", _value0="", _value1="", _value2="", _value3=""):
        con = sqlite.connect(Universals.pathOfSettingsDirectory + "/database.sqlite")
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
            cur.execute("insert into bookmarksOfDirectories(bookmark,value,type) values('"+_value0+"','" + _value1+"','"+_value2+"')")
        elif _action=="delete":
            cur.execute("delete from bookmarksOfDirectories where id="+str(_value0))
        elif _action=="update":
            _value1 = _value1.replace("'", "''")
            _value2 = _value2.replace("'", "''")
            cur.execute(str("update bookmarksOfDirectories set bookmark='"+_value1+"', value='"+_value2+"', type='"+_value3+"' where id="+str(_value0)))
        con.commit()
        
    def bookmarksOfSpecialTools(_action="read", _value0="", _value1="", _value2="", _value3=""):
        con = sqlite.connect(Universals.pathOfSettingsDirectory + "/database.sqlite")
        cur = con.cursor()
        import Organizer
        requirement = Universals.MainWindow.Table.specialTollsBookmarkPointer
        if _action=="read":
            try:
                cur.execute("SELECT * FROM bookmarksOfSpecialTools where type='"+requirement+"'")
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
            cur.execute("insert into bookmarksOfSpecialTools(bookmark,value,type) values('"+_value0+"','"+_value1+"','"+requirement+"')")
        if _action=="delete":
            cur.execute("delete from bookmarksOfSpecialTools where value='"+_value0+"' and type='"+requirement+"'")
        if _action=="update":
            _value1 = _value1.replace("'", "''")
            _value2 = _value2.replace("'", "''")
            cur.execute(str("update bookmarksOfSpecialTools set bookmark='"+_value1+"', value='"+_value2+"' where id="+str(_value0)))
        con.commit()
        
    def searchAndReplaceTable(_action="read", _value0="", _value1="", _value2="", _value3="", _value4="", _value5=""):
        con = sqlite.connect(Universals.pathOfSettingsDirectory + "/database.sqlite")
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
        if InputOutputs.isDir(Universals.pathOfSettingsDirectory)==False:
            InputOutputs.makeDirs(Universals.pathOfSettingsDirectory)
            reFillSettings()
            reFillDatabases("All")
        else:
            if InputOutputs.isFile(Universals.pathOfSettingsDirectory + "/database.sqlite")==False:
                reFillDatabases("All")
            if InputOutputs.isFile(Universals.pathOfSettingsDirectory + "/" + fileOfSettings)==False:
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

    def reFillSettings(_askMakeBackUp=False, _makeBackUp=False):
        if _askMakeBackUp==True:
            isMakeBackUp("Settings")
        elif _makeBackUp==True:
            makeBackUp("Settings")
        mySetting = Variables.MQtCore.QSettings((Universals.pathOfSettingsDirectory + "/" + fileOfSettings).decode("utf-8"), Variables.MQtCore.QSettings.IniFormat)
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
        
    def reFillDatabases(_table="", _actionType="dropAndInsert", _askMakeBackUp=False, _makeBackUp=False):
        if _askMakeBackUp==True:
            isMakeBackUp(_table)
        elif _makeBackUp==True:
            makeBackUp(_table)
        tableCreateQueries = ["CREATE TABLE IF NOT EXISTS dbProperties ('keyName' TEXT NOT NULL,'value' TEXT)",
            "CREATE TABLE IF NOT EXISTS bookmarksOfDirectories ('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,'bookmark' TEXT,'value' TEXT,'type' TEXT)", 
            "CREATE TABLE IF NOT EXISTS bookmarksOfSpecialTools ('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,'bookmark' TEXT,'value' TEXT,'type' TEXT)", 
            "CREATE TABLE IF NOT EXISTS searchAndReplaceTable ('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,'searching' TEXT,'replacing' TEXT,'intIsActive' INTEGER,'intIsCaseSensitive' INTEGER,'intIsRegExp' INTEGER)"]
        tableInsertImportantQueries, sqlCommands = [], []
        tableInsertImportantQueries += getAmendedSQLInputQueries("dbProperties", {"keyName" : "'bookmarksOfDirectories_Version'", "value" : "'2'"}, ["keyName"])
        tableInsertImportantQueries += getAmendedSQLInputQueries("dbProperties", {"keyName" : "'bookmarksOfSpecialTools_Version'", "value" : "'2'"}, ["keyName"])
        tableInsertImportantQueries += getAmendedSQLInputQueries("dbProperties", {"keyName" : "'searchAndReplaceTable_Version'", "value" : "'2'"}, ["keyName"])
        if _table=="bookmarksOfDirectories" or _table=="All":
            if _actionType=="dropAndInsert":
                sqlCommands.append("DELETE FROM bookmarksOfDirectories")
            sqlCommands += getAmendedSQLInputQueries("bookmarksOfDirectories", {"bookmark" : "'Home'", "value" : "'"+Variables.userDirectoryPath+"'", "type" : "''"}, ["value"])
            sqlCommands += getAmendedSQLInputQueries("bookmarksOfDirectories", {"bookmark" : "'MNT'", "value" : "'/mnt'", "type" : "''"}, ["value"])
            sqlCommands += getAmendedSQLInputQueries("bookmarksOfDirectories", {"bookmark" : "'MEDIA'", "value" : "'/media'", "type" : "''"}, ["value"])
        if _table=="bookmarksOfSpecialTools" or _table=="All":
            if _actionType=="dropAndInsert":
                sqlCommands.append("DELETE FROM bookmarksOfSpecialTools")
            sqlCommands += getAmendedSQLInputQueries("bookmarksOfSpecialTools", {"bookmark" : "''", "value" : "'File Name , Artist - Title ;right;113'", "type" : "'music'"}, ["value"])
            sqlCommands += getAmendedSQLInputQueries("bookmarksOfSpecialTools", {"bookmark" : "''", "value" : "'Artist - Title , File Name  ;left;113'", "type" : "'music'"}, ["value"])
            sqlCommands += getAmendedSQLInputQueries("bookmarksOfSpecialTools", {"bookmark" : "''", "value" : "'Track No - Title , File Name  ;left;113'", "type" : "'music'"}, ["value"])
            sqlCommands += getAmendedSQLInputQueries("bookmarksOfSpecialTools", {"bookmark" : "''", "value" : "'Artist - Album , Directory  ;left;113'", "type" : "'music'"}, ["value"])
            sqlCommands += getAmendedSQLInputQueries("bookmarksOfSpecialTools", {"bookmark" : "''", "value" : "'File Name , Title  ;right;102'", "type" : "'music'"}, ["value"])
            sqlCommands += getAmendedSQLInputQueries("bookmarksOfSpecialTools", {"bookmark" : "''", "value" : "'Title , File Name  ;right;102'", "type" : "'music'"}, ["value"])
            sqlCommands += getAmendedSQLInputQueries("bookmarksOfSpecialTools", {"bookmark" : "''", "value" : "'Year , Album  ;right;102'", "type" : "'music'"}, ["value"])
            sqlCommands += getAmendedSQLInputQueries("bookmarksOfSpecialTools", {"bookmark" : "''", "value" : "'Lyrics , Artist - Title  ;right;113'", "type" : "'music'"}, ["value"])
            sqlCommands += getAmendedSQLInputQueries("bookmarksOfSpecialTools", {"bookmark" : "''", "value" : "'Artist - Album - Title , File Name  ;left;124'", "type" : "'music'"}, ["value"])
            sqlCommands += getAmendedSQLInputQueries("bookmarksOfSpecialTools", {"bookmark" : "''", "value" : "'Directory - File Name , Directory  ;left;113'", "type" : "'file'"}, ["value"])
            sqlCommands += getAmendedSQLInputQueries("bookmarksOfSpecialTools", {"bookmark" : "''", "value" : "'Directory , File Name  ;right;102'", "type" : "'file'"}, ["value"])
            sqlCommands += getAmendedSQLInputQueries("bookmarksOfSpecialTools", {"bookmark" : "''", "value" : "'File Name , Directory  ;right;102'", "type" : "'file'"}, ["value"])
            sqlCommands += getAmendedSQLInputQueries("bookmarksOfSpecialTools", {"bookmark" : "''", "value" : "'Directory , File/Directory Name  ;right;102'", "type" : "'directory'"}, ["value"])
            sqlCommands += getAmendedSQLInputQueries("bookmarksOfSpecialTools", {"bookmark" : "''", "value" : "'File/Directory Name , Directory  ;right;102'", "type" : "'directory'"}, ["value"])
            sqlCommands += getAmendedSQLInputQueries("bookmarksOfSpecialTools", {"bookmark" : "''", "value" : "'Directory , File Name  ;right;102'", "type" : "'subfolder'"}, ["value"])
            sqlCommands += getAmendedSQLInputQueries("bookmarksOfSpecialTools", {"bookmark" : "''", "value" : "'File Name , Directory  ;right;102'", "type" : "'subfolder'"}, ["value"])
            sqlCommands += getAmendedSQLInputQueries("bookmarksOfSpecialTools", {"bookmark" : "''", "value" : "'Directory Name , Directory  ;right;102'", "type" : "'cover'"}, ["value"])
            sqlCommands += getAmendedSQLInputQueries("bookmarksOfSpecialTools", {"bookmark" : "''", "value" : "'Source Cover , Current Cover  ;right;102'", "type" : "'cover'"}, ["value"])
            sqlCommands += getAmendedSQLInputQueries("bookmarksOfSpecialTools", {"bookmark" : "''", "value" : "'Destination Cover , Source Cover  ;right;102'", "type" : "'cover'"}, ["value"])
            sqlCommands += getAmendedSQLInputQueries("bookmarksOfSpecialTools", {"bookmark" : "''", "value" : "'Destination Cover , Current Cover  ;right;102'", "type" : "'cover'"}, ["value"])
        if _table=="searchAndReplaceTable" or _table=="All":
            if _actionType=="dropAndInsert":
                sqlCommands.append("DELETE FROM searchAndReplaceTable")
            sqlCommands += getAmendedSQLInputQueries("searchAndReplaceTable", {"searching" : "'http://'", "replacing" : "''", "intIsActive" : "1", "intIsCaseSensitive" : "1", "intIsRegExp" : "0"}, ["searching", "replacing"])
            sqlCommands += getAmendedSQLInputQueries("searchAndReplaceTable", {"searching" : "'www'", "replacing" : "''", "intIsActive" : "1", "intIsCaseSensitive" : "1", "intIsRegExp" : "0"}, ["searching", "replacing"])
        con = sqlite.connect(Universals.pathOfSettingsDirectory + "/database.sqlite")
        for sqlCommand in tableCreateQueries:
            cur = con.cursor()
            cur.execute(str(sqlCommand))
            con.commit()
        for sqlCommand in tableInsertImportantQueries:
            cur = con.cursor()
            cur.execute(str(sqlCommand))
            con.commit()
        for sqlCommand in sqlCommands:
            cur = con.cursor()
            cur.execute(str(sqlCommand))
            con.commit()
    
    def getAmendedSQLInputQueries(_table, _columnNamesAndValues, _primaryColumns):
        sqlString0 = "INSERT INTO " + _table + "("
        sqlString1 = ") SELECT "
        sqlString2 = " WHERE (SELECT COUNT(*) FROM " + _table + " WHERE "
        sqlString3 = "UPDATE " + _table + " SET "
        sqlString4 = " WHERE "
        i, j = 0, 0
        for key, value in _columnNamesAndValues.iteritems():
            if i>0:
                sqlString0 += ","
                sqlString1 += ","
                sqlString3 += ","
            sqlString0 += key
            sqlString1 += str(value)
            sqlString3 += key + "=" + str(value)
            if _primaryColumns.count(key)>0:
                if j>0:
                    sqlString2 += " AND "
                    sqlString4 += " AND "
                sqlString2 += key + "=" + str(value)
                sqlString4 += key + "=" + str(value)
                j +=1
            i +=1
        return [sqlString0 + sqlString1 + sqlString2 + ")=0;" , sqlString3 + sqlString4 + ";"]
    
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
        if _settingType=="database" or _settingType=="All":
            files.append("database.sqlite")
        if _settingType=="Settings" or _settingType=="All":
            files.append(fileOfSettings)
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
        if _settingType=="database" or _settingType=="All":
            files.append("database.sqlite")
        if _settingType=="Settings" or _settingType=="All":
            files.append(fileOfSettings)
        for file in files:
            if isMake==True:
                oldInfo = InputOutputs.readFromFile(Universals.pathOfSettingsDirectory + "/" + file)
            else:
                try:
                    InputOutputs.removeFile(Universals.pathOfSettingsDirectory + "/" + file)
                except:pass
            try:
                if InputOutputs.isFile(Universals.pathOfSettingsDirectory + "/BackUps/"+file):
                    InputOutputs.moveFileOrDir(Universals.pathOfSettingsDirectory + "/BackUps/"+file, Universals.pathOfSettingsDirectory+file)
                else:
                    Dialogs.showError("There Is No Back Up", "No back up file found to restore.")
                    return False
            except:pass
            if isMake==True:
                InputOutputs.writeToFile(Universals.pathOfSettingsDirectory + "/BackUps/"+file, oldInfo)
        return True

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
            conNewDB = sqlite.connect(Universals.pathOfSettingsDirectory + "/database.sqlite")
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
            sets.setValue("fileSystemEncoding", Variables.MQtCore.QVariant(sets.value("settingsVersion").toString()))
        return newSettingsKeys, changedDefaultValuesKeys
        
    def checkDatabases():
        try:
            con = sqlite.connect(Universals.pathOfSettingsDirectory + "/database.sqlite")
            cur = con.cursor()
            cur.execute("SELECT * FROM dbProperties")
            #Bottom lines for new versions
#            try:
#                cur.execute("SELECT * FROM dbProperties where keyName='bookmarksOfDirectories_Version'")
#                bookmarksOfDirectoriesVersion = int(cur.fetchall()[0][1])
#            except:
#                bookmarksOfDirectoriesVersion = 0
#            try:
#                cur.execute("SELECT * FROM dbProperties where keyName='bookmarksOfSpecialTools_Version'")
#                bookmarksOfSpecialToolsVersion = int(cur.fetchall()[0][1])
#            except:
#                bookmarksOfSpecialToolsVersion = 0
#            try:
#                cur.execute("SELECT * FROM dbProperties where keyName='searchAndReplaceTable_Version'")
#                searchAndReplaceTableVersion = int(cur.fetchall()[0][1])
#            except:
#                searchAndReplaceTableVersion = 0
#            if bookmarksOfDirectoriesVersion<x:
#                pass
#            if bookmarksOfSpecialToolsVersion<x:
#                pass
#            if searchAndReplaceTableVersion<x:
#                pass
        except:
            reFillDatabases("All")
        