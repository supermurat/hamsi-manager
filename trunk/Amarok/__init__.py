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


from os import *
import sys
from time import gmtime
from Core.MyObjects import *
import FileUtils as fu
from Core import Dialogs
from Core import Organizer
from Core import Universals as uni
from Core import ReportBug
from Core import MyConfigure
from Core import Execute
isLoadedMysql = False
isCheckAgain = True
try:
    #import MySQLdb as mdb
    import _mysql as mdb
    isLoadedMysql = True
except:pass
MyDialog, MyDialogType, MyParent = getMyDialog()

isAskEmbeddedDBConfiguration = True
dbConnection = None

isStarted = False
isReadOnlyStarted = False

def getMySQLModule():
    if isLoadedMysql: return mdb
    return None

def checkAmarok(_isAlertIfNotAvailable=True, _isUseReadOnly=True):
    if isLoadedMysql and uni.isAvailableKDE4():
        if uni.getBoolValue("amarokIsUseHost"):
            if _isUseReadOnly or uni.getBoolValue("isReadOnlyAmarokDBHost")==False:
                return True
            else:
                if _isAlertIfNotAvailable:
                    answer = Dialogs.ask(translate("ToolsBar", "This Feature Is Not Usable"), translate("Amarok", "This feature is not usable with read only Amarok database. <br>Are you want to give permission to read and write for Amarok database?"))
                    if answer==Dialogs.Yes:
                        uni.setMySetting("isReadOnlyAmarokDBHost", False)
                        return True
        else:
            isAskEmbeddedDBConfiguration = True
            return checkEmbeddedDB()
    else:
        if _isAlertIfNotAvailable:
            Dialogs.showError(translate("ToolsBar", "Amarok Module Is Not Usable"), translate("Amarok", "Please run Amarok once."))
        return False
    return False

def checkEmbeddedDB():
    global isAskEmbeddedDBConfiguration
    if uni.getBoolValue("isReadOnlyAmarokDB"):
        if (fu.isDir(fu.pathOfSettingsDirectory+"/Amarok/mysqle/amarok") and
            fu.isDir(fu.pathOfSettingsDirectory+"/Amarok/mysqle/mysql") and
            fu.isFile(fu.pathOfSettingsDirectory+"/Amarok/my.cnf")):
            return startReadOnlyEmbeddedDB()
        else:
            if isAskEmbeddedDBConfiguration:
                isAskEmbeddedDBConfiguration = False
                answer = Dialogs.ask(translate("Amarok", "Amarok Database Must Be Configure"),
                                    translate("Amarok", "Amarok database must be configure for Hamsi Manager. Are you want to configure Amarok database?"))
                if answer==Dialogs.Yes:
                    ReadOnlyEmbeddedDBConfigurator()
            else:
                return False
    else:
        if (fu.isFile(uni.getKDE4HomePath() +"/share/apps/amarok/mysqle/mysql/db.frm") and
            fu.isFile(uni.getKDE4HomePath() +"/share/apps/amarok/mysqle/my.cnf")):
            return startEmbeddedDB()
        else:
            if isAskEmbeddedDBConfiguration:
                isAskEmbeddedDBConfiguration = False
                answer = Dialogs.ask(translate("Amarok", "Amarok Database Must Be Configure"),
                                    translate("Amarok", "Amarok database must be configure for Hamsi Manager. Are you want to configure Amarok database?"))
                if answer==Dialogs.Yes:
                    EmbeddedDBConfigurator()
            else:
                return False
    return checkEmbeddedDB()

def connectAndGetDB():
    global dbConnection
    if dbConnection==None:
        if uni.getBoolValue("amarokIsUseHost"):
            dbConnection = mdb.connect(host=uni.MySettings["amarokDBHost"], port=int(uni.MySettings["amarokDBPort"]), user=uni.MySettings["amarokDBUser"], passwd=uni.MySettings["amarokDBPass"], db=uni.MySettings["amarokDBDB"])
            dbConnection.set_character_set('utf8')
            dbConnection.query('SET NAMES utf8;')
            dbConnection.query('SET CHARACTER SET utf8;')
            dbConnection.query('SET character_set_connection=utf8;')
        else:
            if uni.getBoolValue("isReadOnlyAmarokDB"):
                dbConnection = mdb.connect(read_default_file=fu.pathOfSettingsDirectory+"/Amarok/my.cnf", read_default_group="client", db="amarok")
            else:
                dbConnection = mdb.connect(read_default_file=uni.getKDE4HomePath() +"/share/apps/amarok/mysqle/my.cnf", read_default_group="client", db="amarok")
    return dbConnection

def checkAndGetDB(_isNoAlertIfSuccesfully=True, _isReCheck=False):
    global isCheckAgain
    if _isReCheck:
        isCheckAgain = True
    if checkAmarok():
        try:
            db = connectAndGetDB()
            if db!=None:
                if isCheckAgain:
                    db.query("SELECT component,version FROM admin")
                    r = db.store_result()
                    if _isNoAlertIfSuccesfully==False:
                        Dialogs.show(translate("Amarok", "Connected To Database"), str(translate("Amarok", "Connected succesfully to \"%s\"")) % uni.MySettings["amarokDBDB"])
                isCheckAgain = False
                return db
            else:
                Dialogs.showError(translate("Amarok", "Amarok Database Is Not Usable"), translate("Amarok", "Amarok database is not accessible."))
            return None
        except:
            cla, error, trbk = sys.exc_info()
            if str(error).find("Unknown MySQL server host")!=-1:
                Dialogs.showError(translate("Amarok", "Not Connected To Database"), str(translate("Amarok", "Unknown MySQL server host \"%s\" <br><b>Details</b> : %s")) % (uni.MySettings["amarokDBHost"], str(error)))
            elif str(error).find("Access denied for user")!=-1:
                Dialogs.showError(translate("Amarok", "Not Connected To Database"), str(translate("Amarok", "Access denied for user \"%s\" <br><b>Details</b> : %s")) % (uni.MySettings["amarokDBUser"], str(error)))
            elif str(error).find("Unknown database")!=-1:
                Dialogs.showError(translate("Amarok", "Not Connected To Database"), str(translate("Amarok", "Unknown database \"%s\" <br><b>Details</b> : %s")) % (uni.MySettings["amarokDBDB"], str(error)))
            elif str(error).find("Can't connect to local MySQL server through socket")!=-1:
                Dialogs.showError(translate("Amarok", "Not Connected To Database"), str(translate("Amarok", "Can't connect to local MySQL server through socket \"%s\" <br><b>Details</b> : %s")) % (str(error).replace("(2002, \"Can't connect to local MySQL server through socket '", "").replace("' (2)\")", ""), str(error)))
            else:
                ReportBug.ReportBug()
            return None
    else:
        if isLoadedMysql==False:
            Dialogs.showError(translate("Amarok", "Amarok Module Is Not Usable"), translate("Amarok", "\"python-mysql\" (MySQLdb / _mysql) named module is not installed on your system. Please install this module and try again."))
        elif uni.isAvailableKDE4()==False:
            Dialogs.showError(translate("Amarok", "Amarok Module Is Not Usable"), translate("Amarok", "Please open user session with KDE4 once."))
        else:
            Dialogs.showError(translate("Amarok", "Amarok Module Is Not Usable"), translate("Amarok", "Please run Amarok once."))
        return None

def openEmbeddedDBConfigurator():
    if uni.getBoolValue("isReadOnlyAmarokDB"):
        ReadOnlyEmbeddedDBConfigurator()
    else:
        EmbeddedDBConfigurator()

def getTagSourceTypes():
    from Taggers import getTaggerTypesName
    tagSourceTypes = ["Amarok"]
    tagSourceTypes += getTaggerTypesName()
    return tagSourceTypes

def getTagTargetTypes():
    from Taggers import getTaggerTypesName
    tagTargetTypes = ["Amarok"]
    for tagerTypeName in getTaggerTypesName():
        tagTargetTypes.append("Amarok + " + tagerTypeName)
    tagTargetTypes += getTaggerTypesName()
    return tagTargetTypes

def getSelectedTagSourseType(_tableName="AmarokMusicTable"):
    tagSourceTypes = getTagSourceTypes()
    return uni.getValue("AmarokTagSourceType" + _tableName, tagSourceTypes[0])

def getSelectedTagTargetType(_tableName="AmarokMusicTable"):
    tagTargetTypes = getTagTargetTypes()
    return uni.getValue("AmarokTagTargetType" + _tableName, tagTargetTypes[1])

def setSelectedTagSourseType(_type, _tableName="AmarokMusicTable"):
    uni.setMySetting("AmarokTagSourceType" + _tableName, _type)
    if _type!="Amarok":
        from Taggers import setSelectedTaggerTypeForReadName
        setSelectedTaggerTypeForReadName(_type)

def setSelectedTagTargetType(_type, _tableName="AmarokMusicTable"):
    uni.setMySetting("AmarokTagTargetType" + _tableName, _type)


def configureEmbeddedDB(_isNoAlertIfSuccesfully=True):
    stopEmbeddedDB()
    backupEmbeddedDB()
    fu.copyDirContent(fu.HamsiManagerDirectory+"/Amarok/EmbeddedDBFiles/mysql", uni.getKDE4HomePath() +"/share/apps/amarok/mysqle/mysql")
    fu.copyFileOrDir(fu.HamsiManagerDirectory+"/Amarok/EmbeddedDBFiles/my.cnf", uni.getKDE4HomePath() +"/share/apps/amarok/mysqle/my.cnf")
    MyConfigure.reConfigureFile(uni.getKDE4HomePath() +"/share/apps/amarok/mysqle/my.cnf")
    if _isNoAlertIfSuccesfully==False:
        Dialogs.show(translate("EmbeddedDBCore", "Created Embedded Server"), translate("EmbeddedDBCore", "Embedded Amarok database server created and generated."))
    return True

def startEmbeddedDB(_isNoAlertIfSuccesfully=True):
    global isStarted
    if isStarted:
        return True
    if uni.checkMysqldSafe():
        Execute.executeWithThread([uni.MySettings["pathOfMysqldSafe"], "--defaults-file=" + uni.getKDE4HomePath() +"/share/apps/amarok/mysqle/my.cnf"])
        Dialogs.sleep(translate("EmbeddedDBCore", "Starting Embedded Server..."), 3)
        if _isNoAlertIfSuccesfully==False:
            Dialogs.show(translate("EmbeddedDBCore", "Started Embedded Server"), translate("EmbeddedDBCore", "Embedded Amarok database server started."))
        isStarted = True
        return True
    isStarted = False
    return False

def stopEmbeddedDB(_isNoAlertIfSuccesfully=True):
    global isStarted
    if isStarted==False:
        return True
    isStarted = False
    mysqldPID = getPID()
    if mysqldPID!=None:
        Execute.execute(["kill", "-TERM", str(mysqldPID)])
        Dialogs.sleep(translate("EmbeddedDBCore", "Stopping Embedded Server..."), 3)
    if _isNoAlertIfSuccesfully==False:
        Dialogs.show(translate("EmbeddedDBCore", "Stopped Embedded Server"), translate("EmbeddedDBCore", "Embedded Amarok database server stopped."))
    return True

def getPID():
    global isStarted
    if fu.isFile(uni.getKDE4HomePath() +"/share/apps/amarok/mysqle/mysqld.pid"):
        isStarted = True
        return fu.readFromFile(uni.getKDE4HomePath() +"/share/apps/amarok/mysqle/mysqld.pid").split("\n")[0]
    isStarted = False
    return None

def isRunning():
    global isStarted
    mysqldPID = getPID()
    if mysqldPID!=None:
        isStarted = True
        return True
    isStarted = False
    return False

def backupEmbeddedDB():
    if fu.isDir(uni.getKDE4HomePath() +"/share/apps/amarok/mysqle_backup_for_hamsi"):
        fu.removeFileOrDir(uni.getKDE4HomePath() +"/share/apps/amarok/mysqle_backup_for_hamsi")
    fu.copyFileOrDir(uni.getKDE4HomePath() +"/share/apps/amarok/mysqle", uni.getKDE4HomePath() +"/share/apps/amarok/mysqle_backup_for_hamsi")

def restoreEmbeddedDB():
    fu.copyDirContent(uni.getKDE4HomePath() +"/share/apps/amarok/mysqle_backup_for_hamsi", uni.getKDE4HomePath() +"/share/apps/amarok/mysqle")

def isHasEmbeddedDBBackup():
    return fu.isDir(uni.getKDE4HomePath() +"/share/apps/amarok/mysqle_backup_for_hamsi")


def createReadOnlyEmbeddedDB(_isNoAlertIfSuccesfully=True):
    stopReadOnlyEmbeddedDB()
    if fu.isDir(fu.pathOfSettingsDirectory+"/Amarok"):
        fu.removeFileOrDir(fu.pathOfSettingsDirectory+"/Amarok")
    fu.makeDirs(fu.pathOfSettingsDirectory+"/Amarok/mysqle")
    fu.copyFileOrDir(fu.HamsiManagerDirectory+"/Amarok/EmbeddedDBFiles/mysql", fu.pathOfSettingsDirectory+"/Amarok/mysqle/mysql", )
    fu.copyFileOrDir(fu.HamsiManagerDirectory+"/Amarok/EmbeddedDBFiles/my-readOnly.cnf", fu.pathOfSettingsDirectory+"/Amarok/my.cnf")
    MyConfigure.reConfigureFile(fu.pathOfSettingsDirectory+"/Amarok/my.cnf")
    fu.makeDirs(fu.pathOfSettingsDirectory+"/Amarok/mysqle/amarok")
    fu.copyFileOrDir(uni.getKDE4HomePath() +"/share/apps/amarok/mysqle/ib_logfile0", fu.pathOfSettingsDirectory+"/Amarok/mysqle/ib_logfile0")
    fu.copyFileOrDir(uni.getKDE4HomePath() +"/share/apps/amarok/mysqle/ib_logfile1", fu.pathOfSettingsDirectory+"/Amarok/mysqle/ib_logfile1")
    fu.copyFileOrDir(uni.getKDE4HomePath() +"/share/apps/amarok/mysqle/ibdata1", fu.pathOfSettingsDirectory+"/Amarok/mysqle/ibdata1")
    generateReadOnlyEmbeddedD()
    if _isNoAlertIfSuccesfully==False:
        Dialogs.show(translate("EmbeddedDBCore", "Created Embedded Server"), translate("EmbeddedDBCore", "Embedded Amarok database server created and generated."))
    return True

def generateReadOnlyEmbeddedD(_isNoAlertIfSuccesfully=True):
    stopReadOnlyEmbeddedDB()
    if fu.isExist(fu.pathOfSettingsDirectory+"/Amarok/mysqle/amarok"):
        fu.removeFileOrDir(fu.pathOfSettingsDirectory+"/Amarok/mysqle/amarok")
    fu.copyFileOrDir(uni.getKDE4HomePath() +"/share/apps/amarok/mysqle/amarok", fu.pathOfSettingsDirectory+"/Amarok/mysqle/amarok")
    if _isNoAlertIfSuccesfully==False:
        Dialogs.show(translate("EmbeddedDBCore", "Generated Embedded Server"), translate("EmbeddedDBCore", "Embedded Amarok database server generated."))
    return True

def startReadOnlyEmbeddedDB(_isNoAlertIfSuccesfully=True):
    global isReadOnlyStarted
    if isReadOnlyStarted:
        return True
    if uni.checkMysqldSafe():
        Execute.executeWithThread([uni.MySettings["pathOfMysqldSafe"], "--defaults-file=" + fu.pathOfSettingsDirectory+"/Amarok/my.cnf"])
        Dialogs.sleep(translate("EmbeddedDBCore", "Starting Embedded Server..."), 3)
        if _isNoAlertIfSuccesfully==False:
            Dialogs.show(translate("EmbeddedDBCore", "Started Embedded Server"), translate("EmbeddedDBCore", "Embedded Amarok database server started."))
        isReadOnlyStarted = True
        return True
    isReadOnlyStarted = False
    return False

def stopReadOnlyEmbeddedDB(_isNoAlertIfSuccesfully=True):
    global isReadOnlyStarted
    if isReadOnlyStarted==False:
        return True
    isReadOnlyStarted = False
    mysqldPID = getReadOnlyPID()
    if mysqldPID!=None:
        Execute.execute(["kill", "-TERM", str(mysqldPID)])
        Dialogs.sleep(translate("EmbeddedDBCore", "Stopping Embedded Server..."), 3)
    if _isNoAlertIfSuccesfully==False:
        Dialogs.show(translate("EmbeddedDBCore", "Stopped Embedded Server"), translate("EmbeddedDBCore", "Embedded Amarok database server stopped."))
    return True

def getReadOnlyPID():
    global isReadOnlyStarted
    if fu.isFile(fu.pathOfSettingsDirectory+"/Amarok/mysqld.pid"):
        isReadOnlyStarted = True
        return fu.readFromFile(fu.pathOfSettingsDirectory+"/Amarok/mysqld.pid").split("\n")[0]
    isReadOnlyStarted = False
    return None

def isReadOnlyRunning():
    global isReadOnlyStarted
    mysqldPID = getReadOnlyPID()
    if mysqldPID!=None:
        isReadOnlyStarted = True
        return True
    isReadOnlyStarted = False
    return False
        

class EmbeddedDBConfigurator(MyDialog):
    
    def __init__(self):
        MyDialog.__init__(self, MyParent)
        if MyDialogType=="MDialog":
            if isActivePyKDE4:
                self.setButtons(MyDialog.NoDefault)
        elif MyDialogType=="MMainWindow":
            self.setObjectName("EmbeddedDBConfigurator")
            setMainWindow(self)
        self.pbtnBackup = MPushButton(translate("EmbeddedDBConfigurator", "Backup"))
        self.pbtnRestore = MPushButton(translate("EmbeddedDBConfigurator", "Restore"))
        self.pbtnConfigureEmbeddedDB = MPushButton(translate("EmbeddedDBConfigurator", "Configure Embedded Database Files"))
        self.pbtnStartEmbeddedDB = MPushButton(translate("EmbeddedDBConfigurator", "Start Embedded Database Server"))
        self.pbtnStopEmbeddedDB = MPushButton(translate("EmbeddedDBConfigurator", "Stop Embedded Database Server"))
        self.pbtnIsRunning = MPushButton(translate("EmbeddedDBConfigurator", "Is Running?"))
        pnlMain = MWidget(self)
        vblMain = MVBoxLayout(pnlMain)
        vblMain.addWidget(self.pbtnBackup)
        vblMain.addWidget(self.pbtnRestore)
        vblMain.addWidget(self.pbtnConfigureEmbeddedDB)
        vblMain.addWidget(self.pbtnStartEmbeddedDB)
        vblMain.addWidget(self.pbtnStopEmbeddedDB)
        vblMain.addWidget(self.pbtnIsRunning)
        self.connect(self.pbtnBackup,SIGNAL("clicked()"),self.backup)
        self.connect(self.pbtnRestore,SIGNAL("clicked()"),self.restore)
        self.connect(self.pbtnConfigureEmbeddedDB,SIGNAL("clicked()"),self.configureEmbeddedDB)
        self.connect(self.pbtnStartEmbeddedDB,SIGNAL("clicked()"),self.startEmbeddedDB)
        self.connect(self.pbtnStopEmbeddedDB,SIGNAL("clicked()"),self.stopEmbeddedDB)
        self.connect(self.pbtnIsRunning,SIGNAL("clicked()"),self.isRunning)
        self.checkRunState()
        self.pbtnRestore.setEnabled(isHasEmbeddedDBBackup())
        if MyDialogType=="MDialog":
            if isActivePyKDE4:
                self.setMainWidget(pnlMain)
            else:
                self.setLayout(vblMain)
        elif MyDialogType=="MMainWindow":
            self.setCentralWidget(pnlMain)
            moveToCenter(self)
        self.setWindowTitle(translate("EmbeddedDBConfigurator", "Amarok Embedded Database Configurator"))
        self.setWindowIcon(MIcon("Images:amarokEmbeddedDBConfigurator.png"))
        self.show()
                        
    def closeEvent(self, _event):
        MApplication.setQuitOnLastWindowClosed(True)
        
    def checkRunState(self):
        if isRunning():
            self.pbtnConfigureEmbeddedDB.setEnabled(False)
            self.pbtnStartEmbeddedDB.setEnabled(False)
            self.pbtnStopEmbeddedDB.setEnabled(True)
        else:
            self.pbtnConfigureEmbeddedDB.setEnabled(True)
            self.pbtnStartEmbeddedDB.setEnabled(True)
            self.pbtnStopEmbeddedDB.setEnabled(False)
        
    def configureEmbeddedDB(self):
        try:
            configureEmbeddedDB(False)
            self.checkRunState()
        except:
            ReportBug.ReportBug()
        
    def startEmbeddedDB(self, _isNoAlertIfSuccesfully=False):
        try:
            startEmbeddedDB(_isNoAlertIfSuccesfully)
            self.checkRunState()
        except:
            ReportBug.ReportBug()
        
    def stopEmbeddedDB(self, _isNoAlertIfSuccesfully=False):
        try:
            stopEmbeddedDB(False)
            self.checkRunState()
        except:
            ReportBug.ReportBug()
            
    def isRunning(self):
        try:
            if isRunning():
                self.pbtnStopEmbeddedDB.setEnabled(True)
                self.pbtnStartEmbeddedDB.setEnabled(False)
                Dialogs.show(translate("EmbeddedDBConfigurator", "Running Embedded Server"), translate("EmbeddedDBConfigurator", "Embedded Amarok database server is running."))
            else:
                self.pbtnStopEmbeddedDB.setEnabled(False)
                self.pbtnStartEmbeddedDB.setEnabled(True)
                Dialogs.show(translate("EmbeddedDBConfigurator", "Not Running Embedded Server"), translate("EmbeddedDBConfigurator", "Embedded Amarok database server is not running."))
        except:
            ReportBug.ReportBug()
            
    def backup(self):
        backupEmbeddedDB()
        Dialogs.show(translate("EmbeddedDBConfigurator", "Backup Completed"), translate("EmbeddedDBConfigurator", "Backup successfully completed.<br> You can restore when you want. "))
        self.pbtnRestore.setEnabled(isHasEmbeddedDBBackup())
            
    def restore(self):
        answer = Dialogs.ask(translate("ToolsBar", "Restore Amarok Database"), translate("Amarok", "Are you want to restore backup database?"))
        if answer==Dialogs.Yes: 
            if isRunning():
                self.stopEmbeddedDB(True)
            Dialogs.show(translate("EmbeddedDBConfigurator", "Close Amarok"), translate("EmbeddedDBConfigurator", "Please close Amarok if it is running."))
            restoreEmbeddedDB()
            Dialogs.show(translate("EmbeddedDBConfigurator", "Restore Completed"), translate("EmbeddedDBConfigurator", "Restore successfully completed.<br> You can run Amarok now if you want."))
            self.checkRunState()

class ReadOnlyEmbeddedDBConfigurator(MyDialog):
    
    def __init__(self):
        MyDialog.__init__(self, MyParent)
        if MyDialogType=="MDialog":
            if isActivePyKDE4:
                self.setButtons(MyDialog.NoDefault)
        elif MyDialogType=="MMainWindow":
            self.setObjectName("ReadOnlyEmbeddedDBConfigurator")
            setMainWindow(self)
        self.pbtnCreateEmbeddedDB = MPushButton(translate("EmbeddedDBConfigurator", "Create Embedded Database Files"))
        self.pbtnGenerateEmbeddedDB = MPushButton(translate("EmbeddedDBConfigurator", "Generate Embedded Database From Amarok"))
        self.pbtnStartEmbeddedDB = MPushButton(translate("EmbeddedDBConfigurator", "Start Embedded Database Server"))
        self.pbtnStopEmbeddedDB = MPushButton(translate("EmbeddedDBConfigurator", "Stop Embedded Database Server"))
        self.pbtnIsRunning = MPushButton(translate("EmbeddedDBConfigurator", "Is Running?"))
        pnlMain = MWidget(self)
        vblMain = MVBoxLayout(pnlMain)
        vblMain.addWidget(self.pbtnCreateEmbeddedDB)
        vblMain.addWidget(self.pbtnGenerateEmbeddedDB)
        vblMain.addWidget(self.pbtnStartEmbeddedDB)
        vblMain.addWidget(self.pbtnStopEmbeddedDB)
        vblMain.addWidget(self.pbtnIsRunning)
        self.connect(self.pbtnCreateEmbeddedDB,SIGNAL("clicked()"),self.createReadOnlyEmbeddedDB)
        self.connect(self.pbtnGenerateEmbeddedDB,SIGNAL("clicked()"),self.generateReadOnlyEmbeddedD)
        self.connect(self.pbtnStartEmbeddedDB,SIGNAL("clicked()"),self.startReadOnlyEmbeddedDB)
        self.connect(self.pbtnStopEmbeddedDB,SIGNAL("clicked()"),self.stopReadOnlyEmbeddedDB)
        self.connect(self.pbtnIsRunning,SIGNAL("clicked()"),self.isReadOnlyRunning)
        self.checkRunState()
        if MyDialogType=="MDialog":
            if isActivePyKDE4:
                self.setMainWidget(pnlMain)
            else:
                self.setLayout(vblMain)
        elif MyDialogType=="MMainWindow":
            self.setCentralWidget(pnlMain)
            moveToCenter(self)
        self.setWindowTitle(translate("EmbeddedDBConfigurator", "Amarok Embedded Database Configurator"))
        self.setWindowIcon(MIcon("Images:amarokEmbeddedDBConfigurator.png"))
        self.show()
                        
    def closeEvent(self, _event):
        MApplication.setQuitOnLastWindowClosed(True)
        
    def checkRunState(self):
        if isReadOnlyRunning():
            self.pbtnCreateEmbeddedDB.setEnabled(False)
            self.pbtnGenerateEmbeddedDB.setEnabled(False)
            self.pbtnStartEmbeddedDB.setEnabled(False)
            self.pbtnStopEmbeddedDB.setEnabled(True)
        else:
            self.pbtnCreateEmbeddedDB.setEnabled(True)
            self.pbtnGenerateEmbeddedDB.setEnabled(True)
            self.pbtnStartEmbeddedDB.setEnabled(True)
            self.pbtnStopEmbeddedDB.setEnabled(False)
        
    def createReadOnlyEmbeddedDB(self):
        try:
            createReadOnlyEmbeddedDB(False)
            self.checkRunState()
        except:
            ReportBug.ReportBug()
        
    def generateReadOnlyEmbeddedD(self):
        try:
            generateReadOnlyEmbeddedD(False)
            self.checkRunState()
        except:
            ReportBug.ReportBug()
        
    def startReadOnlyEmbeddedDB(self):
        try:
            startReadOnlyEmbeddedDB(False)
            self.checkRunState()
        except:
            ReportBug.ReportBug()
        
    def stopReadOnlyEmbeddedDB(self):
        try:
            stopReadOnlyEmbeddedDB(False)
            self.checkRunState()
        except:
            ReportBug.ReportBug()
            
    def isReadOnlyRunning(self):
        try:
            if isReadOnlyRunning():
                self.pbtnStopEmbeddedDB.setEnabled(True)
                self.pbtnStartEmbeddedDB.setEnabled(False)
                Dialogs.show(translate("EmbeddedDBConfigurator", "Running Embedded Server"), translate("EmbeddedDBConfigurator", "Embedded Amarok database server is running."))
            else:
                self.pbtnStopEmbeddedDB.setEnabled(False)
                self.pbtnStartEmbeddedDB.setEnabled(True)
                Dialogs.show(translate("EmbeddedDBConfigurator", "Not Running Embedded Server"), translate("EmbeddedDBConfigurator", "Embedded Amarok database server is not running."))
        except:
            ReportBug.ReportBug()
