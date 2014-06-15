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


import sys,os
import time
from Core import Variables as var
from Core import Universals as uni
import FileUtils as fu
from Core import Dialogs
from Core import ReportBug
from Core.MyObjects import *
from datetime import timedelta, datetime

class UpdateControl(MDialog):
    def __init__(self,_parent, _isNotInstall=False, _isCloseParent=False):
        MDialog.__init__(self, _parent)
        QtWebKit = getMyObject("QtWebKit")
        if isActivePyKDE4:
            self.setButtons(MDialog.NoDefault)
        if _isNotInstall==False:
            if var.isUpdatable()==False:
                _isNotInstall = True
        self.isNotInstall = _isNotInstall
        self.pnlMain = MWidget()
        self.vblMain = MVBoxLayout(self.pnlMain)
        self.isDownloading=False
        self.lblInfo = MLabel("")
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
        self.pbtnCheckForDeveloperVersion = MPushButton(translate("UpdateControl", "Check For Developer Version"))
        self.pbtnCheckForDeveloperVersion.setVisible(False)
        self.connect(self.pbtnCheckForDeveloperVersion,SIGNAL("clicked()"),self.checkForDeveloperVersion)
        self.connect(self.pbtnCancel,SIGNAL("clicked()"), self.close)
        if _isCloseParent:
            self.connect(self.pbtnCancel,SIGNAL("clicked()"), self.parent().close)
        self.connect(self.pbtnDownloadAndInstall,SIGNAL("clicked()"),self.downloadAndInstall)
        self.connect(self.pbtnShowDetails,SIGNAL("toggled(bool)"),self.showDetails)
        self.connect(self.wvWeb,SIGNAL("loadProgress(int)"),self.loading)
        self.connect(self.wvWeb,SIGNAL("loadFinished(bool)"),self.loadFinished)
        self.vblMain.addWidget(self.prgbState)
        self.vblMain.addWidget(self.lblInfo)
        self.pbtnRemindMeLater = MPushButton(translate("UpdateControl", "Remind Me Later And Close"))
        self.cbRemindMeLater = MSpinBox()
        self.pbtnRemindMeLater.setVisible(False)
        self.cbRemindMeLater.setVisible(False)
        self.cbRemindMeLater.setRange(1, int(uni.MySettings["updateInterval"]))
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
        self.vblMain.addWidget(self.pbtnCheckForDeveloperVersion)
        self.vblMain.addLayout(hbox0)
        self.setWindowTitle(translate("UpdateControl", "Checking for the updates"))
        self.details = MLabel("")
        self.details.setWordWrap(True)
        self.details.setOpenExternalLinks(True)
        self.details.setMinimumHeight(220)
        self.vblMain.insertWidget(1,self.details)  
        self.details.setVisible(False)  
        self.pbtnDownloadAndInstall.setFixedWidth(180)
        self.setFixedWidth(400)
        self.setFixedHeight(130)   
        if isActivePyKDE4:
            self.setMainWidget(self.pnlMain)
        else:
            self.setLayout(self.vblMain)
        self.show()
        self.wvWeb.setUrl(MUrl("http://hamsiapps.com/ForMyProjects/UpdateControl.php?p=HamsiManager&v=" + str(var.intversion) + "&l=" + str(uni.MySettings["language"]) + "&machineType=" + var.machineType + "&os=" + var.osName + "&buildType=" + var.getBuildType()))
    
    def checkForDeveloperVersion(self):
        self.wvWeb.setUrl(MUrl("http://hamsiapps.com/ForMyProjects/UpdateControl.php?p=HamsiManager&v=" + str(var.intversion) + "&m=develop&l=" + str(uni.MySettings["language"]) + "&machineType=" + var.machineType + "&os=" + var.osName + "&buildType=" + var.getBuildType()))
    
    def remindMeLaterAndClose(self):
        uni.setMySetting("remindMeLaterForUpdate", self.cbRemindMeLater.value())
        uni.saveSettings()
        self.close()
    
    def loading(self, _value):
        self.prgbState.setValue(_value)
    
    def loadFinished(self, _bitti):
        try:
            if (_bitti):
                if self.isDownloading==False:
                    self.setFixedHeight(170)  
                    self.prgbState.setVisible(False)
                    self.pbtnShowDetails.setEnabled(True)
                    self.lblInfo.setVisible(True)
                    self.updateInformations=str(self.wvWeb.page().mainFrame().toPlainText()).split("\n")
                    if len(self.updateInformations)!=0:
                        if self.updateInformations[0][0]=="V":
                            self.pbtnRemindMeLater.setVisible(False)
                            self.cbRemindMeLater.setVisible(False)
                            self.pbtnDownloadAndInstall.setVisible(False)
                            self.pbtnCheckForDeveloperVersion.setVisible(False)
                            uni.setMySetting("remindMeLaterForUpdate", "-1")
                            uni.setMySetting("remindMeLaterShowDateForUpdate", datetime.now().strftime("%Y %m %d %H %M %S"))
                            uni.saveSettings()
                            try:
                                lastVersion = int(self.updateInformations[0].replace("V", "").replace(".", ""))
                            except:
                                lastVersion = var.intversion -1
                            if lastVersion > var.intversion:
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
                            elif lastVersion < var.intversion:
                                self.lblInfo.setText(str(str(translate("UpdateControl", "Lastest stable version is %s. You currently are using the version for developers.You can continue to use the current version.<br>For details: <a href='%s' target='_blank'>Hamsi Manager</a>")) % (self.updateInformations[0], self.updateInformations[2])))
                                self.pbtnDownloadAndInstall.setVisible(True)
                                if self.isNotInstall==False:
                                    self.pbtnDownloadAndInstall.setText(translate("UpdateControl", "Download and Install") + " (!)")
                                else:
                                    self.pbtnDownloadAndInstall.setText(translate("UpdateControl", "Download") + " (!)")
                                self.pbtnRemindMeLater.setVisible(True)
                                self.cbRemindMeLater.setVisible(True)
                                details = ""
                                for detail in self.updateInformations[4:]:
                                    details += detail+"<br>"
                                self.details.setText(str(str(translate("UpdateControl", "Lastest stable version is %s. You currently are using the version for developers.You can continue to use the current version.<br>If you want a more accurate version, please download and install this version.<br>%s For detailed information: <a href='%s' target='_blank'>Hamsi Manager</a><br>You can download from <a href='%s' target='_blank'>Hamsi Manager %s</a>")) % (self.updateInformations[0] + self.updateInformations[3], details, self.updateInformations[2], self.updateInformations[1], self.updateInformations[0])))
                                self.pbtnCancel.setText(translate("UpdateControl", "Ok"))
                                self.pbtnCheckForDeveloperVersion.setVisible(True)
                            else:
                                self.details.setText(str(translate("UpdateControl", "For detailed information: <a href='%s' target='_blank'>Hamsi Manager</a>"))%(self.updateInformations[2])) 
                                self.lblInfo.setText(translate("UpdateControl", "You are already using the latest release."))
                                self.pbtnCancel.setText(translate("UpdateControl", "Ok"))
                            uni.setMySetting("lastUpdateControlDate", datetime.now().strftime("%Y %m %d %H %M %S"))
                        else:
                            uni.setMySetting("lastUpdateControlDate", datetime.now().strftime("%Y %m %d %H %M %S"))
                            Dialogs.showError(translate("UpdateControl", "Cannot Fetch Release Information"), 
                                        translate("UpdateControl", "Cannot fetch release information. Please retry later.<br>If you are constantly receiving this error, please visit \"http://hamsiapps.com/HamsiManager\"."))
                            self.close()
                    else:
                        uni.setMySetting("lastUpdateControlDate", datetime.now().strftime("%Y %m %d %H %M %S"))
                        Dialogs.showError(translate("UpdateControl", "Cannot Fetch Release Information"), 
                                    translate("UpdateControl", "Cannot fetch release information. Please retry later.<br>If you are constantly receiving this error, please visit \"http://hamsiapps.com/HamsiManager\"."))
                        self.close()
                else:
                    self.lblInfo.setText(translate("UpdateControl", "Download complete."))
            else:
                uni.setMySetting("lastUpdateControlDate", datetime.now().strftime("%Y %m %d %H %M %S"))
                Dialogs.showError(translate("UpdateControl", "Cannot Fetch Release Information"), 
                            translate("UpdateControl", "Cannot fetch release information. Please retry later.<br>If you are constantly receiving this error, please visit \"http://hamsiapps.com/HamsiManager\"."))
                self.close()
        except:
            ReportBug.ReportBug()
            
    def showDetails(self, _value):
        if _value==True:
            self.details.setVisible(True) 
            self.setFixedHeight(330)    
        else:
            self.details.setVisible(False)  
            self.setFixedHeight(150)       
        
    def downloadAndInstall(self):
        try:
            if var.isBuilt() == False:
                if fu.isWritableFileOrDir(fu.HamsiManagerDirectory, True) == False:
                    from Core import Organizer
                    Dialogs.showError(translate("UpdateControl", "Access Denied"),
                            str(translate("UpdateControl", "\"%s\" : you do not have the necessary permissions to change this directory.<br />Please check your access controls and retry. <br />Note: You can run Hamsi Manager as root and try again.")) % Organizer.getLink(fu.HamsiManagerDirectory))
            self.setFixedHeight(130)   
            self.isDownloading=True
            self.prgbState.setVisible(True)
            self.lblInfo.setVisible(False)
            self.setWindowTitle(translate("UpdateControl", "Downloading Latest Release..."))
            self.request = MNetworkRequest(MUrl(self.updateInformations[1]))
            self.willDownload(self.request)
        except:
            ReportBug.ReportBug()
          
    def willDownload(self, _request):
        try:
            defaultFileName = str(MFileInfo(str(trStr(_request.url()))).fileName())
            fileDialogTitle = translate("UpdateControl", "You Can Click Cancel To Update Without Saving The Package.")
            if self.isNotInstall:
                fileDialogTitle = translate("UpdateControl", "Save New Version Of Hamsi Manager")
            fileName = Dialogs.getSaveFileName(fileDialogTitle, fu.joinPath(fu.getDirName(fu.HamsiManagerDirectory), defaultFileName))
            if self.isNotInstall==False or fileName is not None:
                if fileName is None:
                    import random
                    fileName = fu.joinPath(fu.getTempDir(), defaultFileName[:-7]+"-"+str(random.randrange(0, 1000000))+defaultFileName[-7:])
                self.pbtnDownloadAndInstall.setEnabled(False)
                newRequest = _request
                newRequest.setAttribute(MNetworkRequest.User,trQVariant(fileName))
                networkManager = self.wvWeb.page().networkAccessManager()
                reply = networkManager.get(newRequest)
                self.isFileExist = True
                self.connect(reply,SIGNAL("downloadProgress(qint64,qint64)"),self.downloading)
                self.connect(reply,SIGNAL("finished()"),self.downloaded)
                self.connect(reply,SIGNAL("error(QNetworkReply::NetworkError)"),self.errorOccurred)
        except:
            ReportBug.ReportBug()
        
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
                fileName = trStr(v)
                fu.writeToBinaryFile(fileName, reply.readAll())
                self.install(fileName)
        except:
            ReportBug.ReportBug()
        
    def install(self, _fileName):
        if self.isNotInstall==False and var.isBuilt():
            self.setWindowTitle(translate("UpdateControl", "Installing The Latest Release"))
            self.lblInfo.setText(translate("UpdateControl", "Latest release downloaded, initializing installation."))
            from Core.Execute import openWith
            openWith([str(_fileName)])
            self.close()
            self.parent().close()
        else:
            Dialogs.show(translate("UpdateControl", "The New Version Downloaded"), 
                        translate("UpdateControl", "New version of Hamsi Manager downloaded, you can install it manually."))
            self.close()

    @staticmethod
    def isMakeUpdateControl():
        lastUpdateControlTime = uni.getDateValue("lastUpdateControlDate")
        updateInterval = int(uni.MySettings["updateInterval"])
        if (lastUpdateControlTime + timedelta(days=updateInterval)).strftime("%Y%m%d%H%M%S") < datetime.now().strftime("%Y%m%d%H%M%S"):
            return True
        lastUpdateControlTime = uni.getDateValue("remindMeLaterShowDateForUpdate")
        updateInterval = int(uni.MySettings["remindMeLaterForUpdate"])
        if updateInterval!=-1:
            if (lastUpdateControlTime + timedelta(days=updateInterval)).strftime("%Y%m%d%H%M%S") < datetime.now().strftime("%Y%m%d%H%M%S"):
                return True
        return False
        
        
