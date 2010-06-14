# -*- coding: utf-8 -*-

import sys,os
import time
import Universals
import InputOutputs
import Dialogs
import ReportBug
import RoutineChecks
from MyObjects import *
from datetime import timedelta, datetime

class UpdateControl(MDialog):
    global isMakeUpdateControl
    def __init__(self,_parent, _isNotInstall=False):
        MDialog.__init__(self, _parent)
        if Universals.isActivePyKDE4==True:
            self.setButtons(MDialog.None)
        self.isNotInstall = _isNotInstall
        self.pnlMain = MWidget()
        self.vblMain = MVBoxLayout(self.pnlMain)
        self.isDownloading=False
        self.lblInfo = MLabel(u"")
        self.lblInfo.setVisible(False)
        self.lblInfo.setWordWrap(True)
        self.lblInfo.setOpenExternalLinks(True)
        self.pbtnCancel = MPushButton(translate("UpdateControl", "Cancel"))
        if self.isNotInstall==False:
            self.pbtnDownloadAndInstall = MPushButton(translate("UpdateControl", "Download and Install"))
        else:
            self.pbtnDownloadAndInstall = MPushButton(translate("UpdateControl", "Download"))
        self.pbtnDownloadAndInstall.setVisible(False)
        self.pbtnShowDetails = MPushButton(translate("UpdateControl", "Details"))
        self.pbtnShowDetails.setCheckable(True)
        self.pbtnShowDetails.setEnabled(False)
        self.wvWeb = QtWebKit.QWebView()
        self.prgbState = MProgressBar()
        self.prgbState.setRange(0,100)
        self.connect(self.pbtnCancel,SIGNAL("clicked()"),self.close)
        self.connect(self.pbtnDownloadAndInstall,SIGNAL("clicked()"),self.downloadAndInstall)
        self.connect(self.pbtnShowDetails,SIGNAL("toggled(bool)"),self.showDetails)
        self.connect(self.wvWeb,SIGNAL("loadProgress(int)"),self.loading)
        self.connect(self.wvWeb,SIGNAL("loadFinished(bool)"),self.loadFinished)
        self.vblMain.addWidget(self.prgbState)
        self.vblMain.addWidget(self.lblInfo)
        self.pbtnRemindMeLater = MPushButton(MApplication.translate("UpdateControl", "Remind Me Later And Close"))
        self.cbRemindMeLater = MSpinBox()
        self.pbtnRemindMeLater.setVisible(False)
        self.cbRemindMeLater.setVisible(False)
        self.cbRemindMeLater.setRange(1, int(Universals.MySettings["updateInterval"]))
        self.cbRemindMeLater.setValue(1) 
        self.connect(self.pbtnRemindMeLater,SIGNAL("clicked()"),self.remindMeLaterAndClose)
        HBoxRemindMeLater = MHBoxLayout()
        HBoxRemindMeLater.addWidget(self.cbRemindMeLater)
        HBoxRemindMeLater.addWidget(self.pbtnRemindMeLater)
        self.vblMain.addLayout(HBoxRemindMeLater)
        hbox0 = MHBoxLayout()
        hbox0.addWidget(self.pbtnShowDetails,1)
        hbox0.addStretch(1)
        hbox0.addWidget(self.pbtnDownloadAndInstall,1)
        hbox0.addStretch(1)
        hbox0.addWidget(self.pbtnCancel,1)
        self.vblMain.addLayout(hbox0)
        self.setWindowTitle(translate("UpdateControl", "Checking for the updates"))
        self.details = MLabel(u"")
        self.details.setWordWrap(True)
        self.details.setOpenExternalLinks(True)
        self.details.setMinimumHeight(220)
        self.vblMain.insertWidget(1,self.details)  
        self.details.setVisible(False)  
        self.pbtnDownloadAndInstall.setFixedWidth(180)
        self.setFixedWidth(400)
        self.setFixedHeight(130)   
        if Universals.isActivePyKDE4==True:
            self.setMainWidget(self.pnlMain)
        else:
            self.setLayout(self.vblMain)
        self.show()
        self.wvWeb.setUrl(MUrl("http://hamsiapps.com/ForMyProjects/UpdateControl.php?p=HamsiManager&v="+str(RoutineChecks.__intversion__)+"&l="+str(Universals.MySettings["language"])))
    
    def remindMeLaterAndClose(self):
        Universals.setMySetting("remindMeLaterForUpdate", self.cbRemindMeLater.value())
        Universals.saveSettings()
        self.close()
    
    def loading(self, _value):
        self.prgbState.setValue(_value)
    
    def loadFinished(self, _bitti):
        try:
            if (_bitti):
                if self.isDownloading==False:
                    self.setFixedHeight(150)  
                    self.prgbState.setVisible(False)
                    self.pbtnShowDetails.setEnabled(True)
                    self.lblInfo.setVisible(True)
                    self.updateInformations=unicode(self.wvWeb.page().mainFrame().toPlainText(), "utf-8").split("\n")
                    if len(self.updateInformations)!=0:
                        if self.updateInformations[0][0]=="V":
                            Universals.setMySetting("remindMeLaterForUpdate", "-1")
                            Universals.setMySetting("remindMeLaterShowDateForUpdate", datetime.now().strftime("%Y %m %d %H %M %S"))
                            Universals.saveSettings()
                            try:
                                lastVersion = int(self.updateInformations[0])
                            except:
                                lastVersion = RoutineChecks.__intversion__ -1
                            if lastVersion > RoutineChecks.__intversion__:
                                self.lblInfo.setText(str(translate("UpdateControl", "New release is available. Please download and install.<br>"+
                                                    "For details: <a href='%s' target='_blank'>Hamsi Manager</a>")) % (self.updateInformations[2]))
                                self.pbtnDownloadAndInstall.setVisible(True)
                                self.pbtnRemindMeLater.setVisible(True)
                                self.cbRemindMeLater.setVisible(True)
                                details = ""
                                for detail in self.updateInformations[4:]:
                                    details += detail+"<br>"
                                self.details.setText(str(translate("UpdateControl", "Version %s is available. Please download and install the new release.<br>"+
                                                      "%s For detailed information: <a href='%s' target='_blank'>Hamsi Manager</a><br>You can download from <a href='%s' target='_blank'>Hamsi Manager %s</a>")) % (self.updateInformations[0] + self.updateInformations[3], details, self.updateInformations[2], self.updateInformations[1], self.updateInformations[0]))
                            elif lastVersion < RoutineChecks.__intversion__:
                                self.lblInfo.setText(str(translate("UpdateControl", "Lastest stable version is %s. You currently are using the version for developers.You can continue to use the current version.<br>"+
                                                    "For details: <a href='%s' target='_blank'>Hamsi Manager</a>")) % (self.updateInformations[0], self.updateInformations[2]))
                                self.pbtnDownloadAndInstall.setVisible(True)
                                self.pbtnRemindMeLater.setVisible(True)
                                self.cbRemindMeLater.setVisible(True)
                                details = ""
                                for detail in self.updateInformations[4:]:
                                    details += detail+"<br>"
                                self.details.setText(str(translate("UpdateControl", "Lastest stable version is %s. You currently are using the version for developers.You can continue to use the current version.<br>If you want a more accurate version, please download and install this version.<br>"+
                                                      "%s For detailed information: <a href='%s' target='_blank'>Hamsi Manager</a><br>You can download from <a href='%s' target='_blank'>Hamsi Manager %s</a>")) % (self.updateInformations[0] + self.updateInformations[3], details, self.updateInformations[2], self.updateInformations[1], self.updateInformations[0]))
                            else:
                                self.details.setText(str(translate("UpdateControl", "For detailed information: <a href='%s' target='_blank'>Hamsi Manager</a>"))%(self.updateInformations[2])) 
                                self.lblInfo.setText(translate("UpdateControl", "You are already using the latest release."))
                                self.pbtnCancel.setText(translate("UpdateControl", "Ok"))
                            Universals.setMySetting("lastUpdateControlDate", datetime.now().strftime("%Y %m %d %H %M %S"))
                        else:
                            Dialogs.showError(translate("UpdateControl", "Cannot Fetch Release Information"), 
                                        translate("UpdateControl", "Cannot fetch release information. Please retry later.<br>If you are constantly receiving this error, please visit \"http://hamsiapps.com/HamsiManager\"."))
                            self.close()
                    else:
                        Dialogs.showError(translate("UpdateControl", "Cannot Fetch Release Information"), 
                                    translate("UpdateControl", "Cannot fetch release information. Please retry later.<br>If you are constantly receiving this error, please visit \"http://hamsiapps.com/HamsiManager\"."))
                        self.close()
                else:
                    self.lblInfo.setText(translate("UpdateControl", "Download complete."))
            else:
                Dialogs.showError(translate("UpdateControl", "Cannot Fetch Release Information"), 
                            translate("UpdateControl", "Cannot fetch release information. Please retry later.<br>If you are constantly receiving this error, please visit \"http://hamsiapps.com/HamsiManager\"."))
                self.close()
        except:
            error = ReportBug.ReportBug()
            error.show()  
            
    def showDetails(self, _value):
        if _value==True:
            self.details.setVisible(True) 
            self.setFixedHeight(330)    
        else:
            self.details.setVisible(False)  
            self.setFixedHeight(150)       
        
    def downloadAndInstall(self):
        try:
            self.setFixedHeight(130)   
            self.isDownloading=True
            self.prgbState.setVisible(True)
            self.lblInfo.setVisible(False)
            self.setWindowTitle(translate("UpdateControl", "Downloading Latest Release..."))
            self.request = MNetworkRequest(MUrl(self.updateInformations[1]))
            self.willDownload(self.request)
        except:
            error = ReportBug.ReportBug()
            error.show()  
          
    def willDownload(self, _request):
        try:
            defaultFileName = MFileInfo(_request.url().toString()).fileName()
            fileDialogTitle = translate("UpdateControl", "You Can Click Cancel To Update Without Saving The Package.")
            if self.isNotInstall:
                fileDialogTitle = translate("UpdateControl", "Save As")
            fileName = MFileDialog.getSaveFileName(self, fileDialogTitle,InputOutputs.getDirName(InputOutputs.getDirName(Universals.sourcePath))+"/"+defaultFileName)
            if fileName== "":
                import random, tempfile
                fileName = tempfile.gettempdir() + "/" + defaultFileName[:-7]+"-"+str(random.randrange(0, 1000000))+defaultFileName[-7:]
            self.pbtnDownloadAndInstall.setEnabled(False)
            newRequest = _request
            newRequest.setAttribute(MNetworkRequest.User,MVariant(fileName))
            networkManager = self.wvWeb.page().networkAccessManager()
            reply = networkManager.get(newRequest)
            self.isFileExist = True
            self.connect(reply,SIGNAL("downloadProgress(qint64,qint64)"),self.downloading)
            self.connect(reply,SIGNAL("finished()"),self.downloaded)
            self.connect(reply,SIGNAL("error(QNetworkReply::NetworkError)"),self.errorOccurred)
        except:
            error = ReportBug.ReportBug()
            error.show()  
        
    def downloading(self, _value, _maxValue):
        self.prgbState.setRange(0, _maxValue)
        self.prgbState.setValue(_value)
    
    def errorOccurred(self):
        self.isFileExist = False
        Dialogs.showError(translate("UpdateControl", "Cannot Read Source."), 
                    translate("UpdateControl", "Cannot read source package. Please retry later."))
        self.close()
        
    def downloaded(self):
        try:
            if self.isFileExist==True:
                self.prgbState.setVisible(False)
                self.pbtnDownloadAndInstall.setEnabled(False)
                self.pbtnCancel.setEnabled(False)
                reply = self.sender()
                request = reply.request()
                v = request.attribute(MNetworkRequest.User)
                fileName = v.toString()
                InputOutputs.writeToFile(fileName, reply.readAll())
                if self.isNotInstall==False:
                    self.setWindowTitle(translate("UpdateControl", "Installing The Latest Release"))
                    self.lblInfo.setText(translate("UpdateControl", "Latest release downloaded, initializing installation."))
                    self.install(fileName)
        except:
            error = ReportBug.ReportBug()
            error.show()  
        
    def install(self, _fileName):
        from Execute import executeWithPython
        Dialogs.show(translate("UpdateControl", "Update Will Be Complete"),
                        translate("UpdateControl", "Please restart Hamsi Manager now."),
                        translate("UpdateControl", "Restart"))
        if InputOutputs.isFile(Universals.HamsiManagerDirectory+"/Update.py")==False:
            if InputOutputs.isFile(Universals.HamsiManagerDirectory+"/ConfigureUpdate.py"):
                InputOutputs.moveFileOrDir(Universals.HamsiManagerDirectory+"/ConfigureUpdate.py", Universals.HamsiManagerDirectory+"/Update.py")
        executeWithPython(Universals.HamsiManagerDirectory+"/Update.py "+str(_fileName))
        self.close()
        self.parent().close()
        
    def isMakeUpdateControl():
        lastUpdateControlTime = Universals.getDateValue("lastUpdateControlDate")
        updateInterval = int(Universals.MySettings["updateInterval"])
        if (lastUpdateControlTime + timedelta(days=updateInterval)).strftime("%Y%m%d%H%M%S") < datetime.now().strftime("%Y%m%d%H%M%S"):
            return True
        lastUpdateControlTime = Universals.getDateValue("remindMeLaterShowDateForUpdate")
        updateInterval = int(Universals.MySettings["remindMeLaterForUpdate"])
        if updateInterval!=-1:
            if (lastUpdateControlTime + timedelta(days=updateInterval)).strftime("%Y%m%d%H%M%S") < datetime.now().strftime("%Y%m%d%H%M%S"):
                return True
        return False
        
        
