# -*- coding: utf-8 -*-

from os import *
import sys
import Variables
import InputOutputs
from MyObjects import *
from time import gmtime
import Dialogs
import Organizer
import Universals
import ReportBug
import Settings
isLoadedMysql = False
isCheckAgain = True
try:
    import _mysql as mdb
    isLoadedMysql = True
except:pass
MyDialog, MyDialogType, MyParent = getMyDialog()

class Amarok:
    global checkAmarok, connectAndGetDB, checkAndGetDB, checkEmbeddedDB, isAskAmarokEmbeddedDBConfiguration, dbConnection
    isAskAmarokEmbeddedDBConfiguration = True
    dbConnection = None
    
    def checkAmarok(_isAlertIfNotAvailable=True):
        if isLoadedMysql and Variables.isAvailableKDE4():
            if Universals.getBoolValue("amarokIsUseHost"):
                return True
            else:
                isAskAmarokEmbeddedDBConfiguration = True
                return checkEmbeddedDB()
        else:
            if _isAlertIfNotAvailable:
                Dialogs.showError(translate("ToolsBar", "Amarok Module Is Not Usable"), translate("Amarok", "Please run Amarok once."))
            return False
            
    def checkEmbeddedDB():
        global isAskAmarokEmbeddedDBConfiguration
        if (InputOutputs.IA.isDir(Universals.pathOfSettingsDirectory+"/Amarok/mysqle/amarok") and
            InputOutputs.IA.isDir(Universals.pathOfSettingsDirectory+"/Amarok/mysqle/mysql") and
            InputOutputs.IA.isFile(Universals.pathOfSettingsDirectory+"/Amarok/my.cnf")):
            return startEmbeddedDB()
        else:
            if isAskAmarokEmbeddedDBConfiguration:
                isAskAmarokEmbeddedDBConfiguration = False
                answer = Dialogs.ask(translate("Amarok", "Amarok Database Must Be Configure"),
                                    translate("Amarok", "Amarok database must be configure for Hamsi Manager. Are you want to configure Amarok database?"))
                if answer==Dialogs.Yes: 
                    AmarokEmbeddedDBConfigurator()
            else:
                return False
        return checkEmbeddedDB()
        
    def connectAndGetDB():
        global dbConnection
        if dbConnection==None:
            if Universals.getBoolValue("amarokIsUseHost"):
                dbConnection = mdb.connect(host=Universals.MySettings["amarokDBHost"], port=int(Universals.MySettings["amarokDBPort"]), user=Universals.MySettings["amarokDBUser"], passwd=Universals.MySettings["amarokDBPass"], db=Universals.MySettings["amarokDBDB"])
            else:
                dbConnection = mdb.connect(read_default_file=Universals.pathOfSettingsDirectory+"/Amarok/my.cnf", read_default_group="client", db="amarok")
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
                            Dialogs.show(translate("Amarok", "Connected To Database"), str(translate("Amarok", "Connected succesfully to \"%s\"")) % Universals.MySettings["amarokDBDB"])
                    isCheckAgain = False
                    return db
                else:
                    Dialogs.showError(translate("Amarok", "Amarok Database Is Not Usable"), translate("Amarok", "Amarok database is not accessible."))
                return None
            except:
                cla, error, trbk = sys.exc_info()
                if str(error).find("Unknown MySQL server host")!=-1:
                    Dialogs.showError(translate("Amarok", "Not Connected To Database"), str(translate("Amarok", "Unknown MySQL server host \"%s\" <br><b>Details</b> : %s")) % (Universals.MySettings["amarokDBHost"], str(error)))
                elif str(error).find("Access denied for user")!=-1:
                    Dialogs.showError(translate("Amarok", "Not Connected To Database"), str(translate("Amarok", "Access denied for user \"%s\" <br><b>Details</b> : %s")) % (Universals.MySettings["amarokDBUser"], str(error)))
                elif str(error).find("Unknown database")!=-1:
                    Dialogs.showError(translate("Amarok", "Not Connected To Database"), str(translate("Amarok", "Unknown database \"%s\" <br><b>Details</b> : %s")) % (Universals.MySettings["amarokDBDB"], str(error)))
                elif str(error).find("Can't connect to local MySQL server through socket")!=-1:
                    Dialogs.showError(translate("Amarok", "Not Connected To Database"), str(translate("Amarok", "Can't connect to local MySQL server through socket \"%s\" <br><b>Details</b> : %s")) % (str(error).replace("(2002, \"Can't connect to local MySQL server through socket '", "").replace("' (2)\")", ""), str(error)))
                else:
                    error = ReportBug.ReportBug()
                    error.show()
                return None
        else:
            if isLoadedMysql==False:
                Dialogs.showError(translate("Amarok", "Amarok Module Is Not Usable"), translate("Amarok", "\"python-mysql\" (MySQLdb / _mysql) named module is not installed on your system. Please install this module and try again."))
            elif Variables.isAvailableKDE4()==False:
                Dialogs.showError(translate("Amarok", "Amarok Module Is Not Usable"), translate("Amarok", "Please open user session with KDE4 once."))
            else:
                Dialogs.showError(translate("Amarok", "Amarok Module Is Not Usable"), translate("Amarok", "Please run Amarok once."))
            return None

class AmarokEmbeddedDBCore():
    global createEmbeddedDB, generateEmbeddedDB, startEmbeddedDB, stopEmbeddedDB, getPID, isRunning, isStarted
    isStarted = False
        
    def createEmbeddedDB(_isNoAlertIfSuccesfully=True):
        stopEmbeddedDB()
        import MyConfigure
        if InputOutputs.IA.isDir(Universals.pathOfSettingsDirectory+"/Amarok"):
            InputOutputs.IA.removeFileOrDir(Universals.pathOfSettingsDirectory+"/Amarok", True)
        InputOutputs.IA.makeDirs(Universals.pathOfSettingsDirectory+"/Amarok/mysqle")
        InputOutputs.IA.copyFileOrDir(Variables.HamsiManagerDirectory+"/Amarok/EmbeddedDBFiles/mysqle/mysql", Universals.pathOfSettingsDirectory+"/Amarok/mysqle/mysql", )
        InputOutputs.IA.copyFileOrDir(Variables.HamsiManagerDirectory+"/Amarok/EmbeddedDBFiles/my.cnf", Universals.pathOfSettingsDirectory+"/Amarok/my.cnf")
        MyConfigure.reConfigureFile(Universals.pathOfSettingsDirectory+"/Amarok/my.cnf")
        InputOutputs.IA.makeDirs(Universals.pathOfSettingsDirectory+"/Amarok/mysqle/amarok")
        InputOutputs.IA.copyFileOrDir(Variables.getKDE4HomePath() +"/share/apps/amarok/mysqle/ib_logfile0", Universals.pathOfSettingsDirectory+"/Amarok/mysqle/ib_logfile0")
        InputOutputs.IA.copyFileOrDir(Variables.getKDE4HomePath() +"/share/apps/amarok/mysqle/ib_logfile1", Universals.pathOfSettingsDirectory+"/Amarok/mysqle/ib_logfile1")
        InputOutputs.IA.copyFileOrDir(Variables.getKDE4HomePath() +"/share/apps/amarok/mysqle/ibdata1", Universals.pathOfSettingsDirectory+"/Amarok/mysqle/ibdata1")
        generateEmbeddedDB()
        if _isNoAlertIfSuccesfully==False:
            Dialogs.show(translate("AmarokEmbeddedDBCore", "Created Embedded Server"), translate("AmarokEmbeddedDBCore", "Embedded Amarok database server created and generated."))
        return True
        
    def generateEmbeddedDB(_isNoAlertIfSuccesfully=True):
        stopEmbeddedDB()
        InputOutputs.IA.removeFileOrDir(Universals.pathOfSettingsDirectory+"/Amarok/mysqle/amarok", True)
        InputOutputs.IA.copyFileOrDir(Variables.getKDE4HomePath() +"/share/apps/amarok/mysqle/amarok", Universals.pathOfSettingsDirectory+"/Amarok/mysqle/amarok")
        if _isNoAlertIfSuccesfully==False:
            Dialogs.show(translate("AmarokEmbeddedDBCore", "Generated Embedded Server"), translate("AmarokEmbeddedDBCore", "Embedded Amarok database server generated."))
        return True
        
    def startEmbeddedDB(_isNoAlertIfSuccesfully=True):
        global isStarted
        if Universals.checkMysqldSafe():
            import Execute
            Execute.executeAsThread(Universals.MySettings["pathOfMysqldSafe"] + " --defaults-file=\"" + Universals.pathOfSettingsDirectory+"/Amarok/my.cnf" + "\"")
            Dialogs.sleep(translate("AmarokEmbeddedDBCore", "Starting Embedded Server..."), 3)
            if _isNoAlertIfSuccesfully==False:
                Dialogs.show(translate("AmarokEmbeddedDBCore", "Started Embedded Server"), translate("AmarokEmbeddedDBCore", "Embedded Amarok database server started."))
            isStarted = True
            return True
        isStarted = False
        return False
        
    def stopEmbeddedDB(_isNoAlertIfSuccesfully=True):
        global isStarted
        isStarted = False
        mysqldPID = getPID()
        if mysqldPID!=None:
            import Execute
            Execute.execute("kill -TERM " + mysqldPID)
            Dialogs.sleep(translate("AmarokEmbeddedDBCore", "Stopping Embedded Server..."), 3)
        if _isNoAlertIfSuccesfully==False:
            Dialogs.show(translate("AmarokEmbeddedDBCore", "Stopped Embedded Server"), translate("AmarokEmbeddedDBCore", "Embedded Amarok database server stopped."))
        return True
        
    def getPID():
        global isStarted
        if InputOutputs.IA.isFile(Universals.pathOfSettingsDirectory+"/Amarok/mysqld.pid"):
            isStarted = True
            return InputOutputs.IA.readFromFile(Universals.pathOfSettingsDirectory+"/Amarok/mysqld.pid")
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

class AmarokEmbeddedDBConfigurator(MyDialog):
    
    def __init__(self):
        MyDialog.__init__(self, MyParent)
        if MyDialogType=="MDialog":
            if Universals.isActivePyKDE4==True:
                self.setButtons(MyDialog.None)
        elif MyDialogType=="MMainWindow":
            self.setObjectName("AmarokEmbeddedDBConfigurator")
            Universals.MainWindow = self
        self.pbtnCreateEmbeddedDB = MPushButton(translate("AmarokEmbeddedDBConfigurator", "Create Embedded Database Files"))
        self.pbtnGenerateEmbeddedDB = MPushButton(translate("AmarokEmbeddedDBConfigurator", "Generate Embedded Database From Amarok"))
        self.pbtnStartEmbeddedDB = MPushButton(translate("AmarokEmbeddedDBConfigurator", "Start Embedded Database Server"))
        self.pbtnStopEmbeddedDB = MPushButton(translate("AmarokEmbeddedDBConfigurator", "Stop Embedded Database Server"))
        self.pbtnIsRunning = MPushButton(translate("AmarokEmbeddedDBConfigurator", "Is Running"))
        pnlMain = MWidget(self)
        vblMain = MVBoxLayout(pnlMain)
        vblMain.addWidget(self.pbtnCreateEmbeddedDB)
        vblMain.addWidget(self.pbtnGenerateEmbeddedDB)
        vblMain.addWidget(self.pbtnStartEmbeddedDB)
        vblMain.addWidget(self.pbtnStopEmbeddedDB)
        vblMain.addWidget(self.pbtnIsRunning)
        self.connect(self.pbtnCreateEmbeddedDB,SIGNAL("clicked()"),self.createEmbeddedDB)
        self.connect(self.pbtnGenerateEmbeddedDB,SIGNAL("clicked()"),self.generateEmbeddedDB)
        self.connect(self.pbtnStartEmbeddedDB,SIGNAL("clicked()"),self.startEmbeddedDB)
        self.connect(self.pbtnStopEmbeddedDB,SIGNAL("clicked()"),self.stopEmbeddedDB)
        self.connect(self.pbtnIsRunning,SIGNAL("clicked()"),self.isRunning)
        self.checkRunState()
        if MyDialogType=="MDialog":
            if Universals.isActivePyKDE4==True:
                self.setMainWidget(pnlMain)
            else:
                self.setLayout(vblMain)
        elif MyDialogType=="MMainWindow":
            self.setCentralWidget(pnlMain)
            moveToCenter(self)
        self.setWindowTitle(translate("AmarokEmbeddedDBConfigurator", "Amarok Embedded Database Configurator"))
        self.setWindowIcon(MIcon("Images:amarokEmbeddedDBConfigurator.png"))
        self.show()
                        
    def closeEvent(self, _event):
        MApplication.setQuitOnLastWindowClosed(True)
        
    def checkRunState(self):
        if isRunning():
            self.pbtnStartEmbeddedDB.setEnabled(False)
            self.pbtnStopEmbeddedDB.setEnabled(True)
        else:
            self.pbtnStartEmbeddedDB.setEnabled(True)
            self.pbtnStopEmbeddedDB.setEnabled(False)
        
    def createEmbeddedDB(self):
        try:
            createEmbeddedDB(False)
            self.checkRunState()
        except:
            error = ReportBug.ReportBug()
            error.show()
        
    def generateEmbeddedDB(self):
        try:
            generateEmbeddedDB(False)
            self.checkRunState()
        except:
            error = ReportBug.ReportBug()
            error.show()
        
    def startEmbeddedDB(self):
        try:
            startEmbeddedDB(False)
            self.checkRunState()
        except:
            error = ReportBug.ReportBug()
            error.show()
        
    def stopEmbeddedDB(self):
        try:
            stopEmbeddedDB(False)
            self.checkRunState()
        except:
            error = ReportBug.ReportBug()
            error.show()
            
    def isRunning(self):
        try:
            if isRunning():
                self.pbtnStopEmbeddedDB.setEnabled(True)
                self.pbtnStartEmbeddedDB.setEnabled(False)
                Dialogs.show(translate("AmarokEmbeddedDBConfigurator", "Running Embedded Server"), translate("AmarokEmbeddedDBConfigurator", "Embedded Amarok database server is running."))
            else:
                self.pbtnStopEmbeddedDB.setEnabled(False)
                self.pbtnStartEmbeddedDB.setEnabled(True)
                Dialogs.show(translate("AmarokEmbeddedDBConfigurator", "Not Running Embedded Server"), translate("AmarokEmbeddedDBConfigurator", "Embedded Amarok database server is not running."))
        except:
            error = ReportBug.ReportBug()
            error.show()
