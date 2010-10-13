# -*- coding: utf-8 -*-

from os import *
import sys
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
    global checkAmarok, connectAndGetDB, checkAndGetDB, checkEmbeddedDB, configureEmbeddedDB, isAskAmarokEmbeddedDBConfiguration
    isAskAmarokEmbeddedDBConfiguration = True
    
    def checkAmarok():
        if isLoadedMysql:
            if Universals.getBoolValue("amarokIsUseHost"):
                return True
            else:
                isAskAmarokEmbeddedDBConfiguration = True
                return checkEmbeddedDB()
        else:
            return False
            
    def checkEmbeddedDB():
        global isAskAmarokEmbeddedDBConfiguration
        if (InputOutputs.isDir(Settings.pathOfSettingsDirectory+"/Amarok/mysqle/amarok") and
            InputOutputs.isDir(Settings.pathOfSettingsDirectory+"/Amarok/mysqle/mysql") and
            InputOutputs.isFile(Settings.pathOfSettingsDirectory+"/Amarok/my.cnf")):
            return True
        else:
            if isAskAmarokEmbeddedDBConfiguration:
                isAskAmarokEmbeddedDBConfiguration = False
                answer = Dialogs.ask(translate("HamsiManager", "Amarok Database Must Be Configure"),
                                    translate("HamsiManager", "Amarok database must be configure for Hamsi Manager. Are you want to configure Amarok database?"))
                if answer==Dialogs.Yes: 
                    AmarokEmbeddedDBConfigurator()
            else:
                return False
        return checkEmbeddedDB()
        
    def connectAndGetDB():
        if Universals.getBoolValue("amarokIsUseHost"):
            return mdb.connect(host=Universals.MySettings["amarokDBHost"], port=int(Universals.MySettings["amarokDBPort"]), user=Universals.MySettings["amarokDBUser"], passwd=Universals.MySettings["amarokDBPass"], db=Universals.MySettings["amarokDBDB"])
        else:
            return mdb.connect(read_default_file=Settings.pathOfSettingsDirectory+"/Amarok/my.cnf", read_default_group="client")
        
    def checkAndGetDB(_isNoAlertIfSuccesfully=True):
        global isCheckAgain
        if checkAmarok():
            try:
                db = connectAndGetDB()
                if db!=None:
                    if isCheckAgain:
                        db.query("""SELECT component,version FROM admin""")
                        r = db.store_result()
                        if _isNoAlertIfSuccesfully==False:
                            Dialogs.show(translate("Amarok", "Connected To Database"), str(translate("Amarok", "Connected succesfully to \"%s\"")) % Universals.MySettings["amarokDBDB"])
                    isCheckAgain = False
                    return db
                else:
                    Dialogs.show(translate("Amarok", "Amarok Database Is Not Usable"), translate("Amarok", "Amarok database is not accessible."))
                return None
            except:
                cla, error, trbk = sys.exc_info()
                if str(error).find("Unknown MySQL server host")!=-1:
                    Dialogs.show(translate("Amarok", "Not Connected To Database"), str(translate("Amarok", "Unknown MySQL server host \"%s\" <br><b>Details</b> : %s")) % (Universals.MySettings["amarokDBHost"], str(error)))
                elif str(error).find("Access denied for user")!=-1:
                    Dialogs.show(translate("Amarok", "Not Connected To Database"), str(translate("Amarok", "Access denied for user \"%s\" <br><b>Details</b> : %s")) % (Universals.MySettings["amarokDBUser"], str(error)))
                elif str(error).find("Unknown database")!=-1:
                    Dialogs.show(translate("Amarok", "Not Connected To Database"), str(translate("Amarok", "Unknown database \"%s\" <br><b>Details</b> : %s")) % (Universals.MySettings["amarokDBDB"], str(error)))
                elif str(error).find("Can't connect to local MySQL server through socket")!=-1:
                    Dialogs.show(translate("Amarok", "Not Connected To Database"), str(translate("Amarok", "Can't connect to local MySQL server through socket \"%s\" <br><b>Details</b> : %s")) % (str(error).replace("(2002, \"Can't connect to local MySQL server through socket '", "").replace("' (2)\")", ""), str(error)))
                else:
                    error = ReportBug.ReportBug()
                    error.show()
                return None
        else:
            if isLoadedMysql==False:
                Dialogs.show(translate("Amarok", "Amarok Module Is Not Usable"), translate("Amarok", "\"python-mysql\" (MySQLdb / _mysql) named module is not installed on your system. Please install this module and try again."))
            else:
                Dialogs.show(translate("Amarok", "Amarok Module Is Not Usable"), translate("Amarok", "Please run Amarok once."))
            return None
            
class AmarokEmbeddedDBConfigurator(MyDialog):
    def __init__(self):
        MyDialog.__init__(self, MyParent)
        if MyDialogType=="MDialog":
            if Universals.isActivePyKDE4==True:
                self.setButtons(MyDialog.None)
        elif MyDialogType=="MMainWindow":
            self.setObjectName("AmarokEmbeddedDBConfigurator")
            Universals.MainWindow = self
        pnlMain = MWidget(self)
        vblMain = MVBoxLayout(pnlMain)
        #FIXME: Add some controls to this form.
        vblMain.addWidget(MLabel("Developing Now. This is not usable."))
        if MyDialogType=="MDialog":
            if Universals.isActivePyKDE4==True:
                self.setMainWidget(pnlMain)
            else:
                self.setLayout(vblMain)
        elif MyDialogType=="MMainWindow":
            self.setCentralWidget(pnlMain)
            moveToCenter(self)
        self.setWindowTitle(translate("AmarokEmbeddedDBConfigurator", "Amarok Embedded Database Configurator"))
        #self.setWindowIcon(MIcon("Images:temp.png"))
        self.show()
                        
    def closeEvent(self, _event):
        MApplication.setQuitOnLastWindowClosed(True)
        
    def configureEmbeddedDB():
        return False
        
        
        
