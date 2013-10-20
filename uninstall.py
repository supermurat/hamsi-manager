#!/usr/bin/env python
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

import sys
import os
from Core import Variables
try: 
    if float(sys.version[:3])<3.0: 
        reload(sys)
        sys.setdefaultencoding("utf-8")
except:pass
Variables.checkStartupVariables()
from Core import Universals
from Core import RoutineChecks
if RoutineChecks.checkMandatoryModules():
    from Core import Settings
    Universals.fillMySettings(False, False, False)
    Universals.isActivePyKDE4 = False
    from Core.MyObjects import *
    import InputOutputs
    from Core import Dialogs
    from Core import Execute
    defaultLangCode = str(QLocale().name())
    HamsiManagerApp = MApplication(sys.argv)
    MDir.setSearchPaths("Images", MStringList(trForUI(InputOutputs.joinPath(Universals.themePath, "Images"))))
    StyleFile = open(InputOutputs.joinPath(Universals.themePath, "Style.qss"))
    HamsiManagerApp.setStyleSheet(StyleFile.read())
    languageFile = MTranslator()
    if InputOutputs.isFile(InputOutputs.joinPath(Variables.HamsiManagerDirectory, "Languages", "HamsiManagerWithQt_"+defaultLangCode+".qm")):
            languageFile.load(trForUI(InputOutputs.joinPath(Variables.HamsiManagerDirectory, "Languages", "HamsiManagerWithQt_"+defaultLangCode+".qm")))
    elif InputOutputs.isFile(InputOutputs.joinPath(Variables.HamsiManagerDirectory, "Languages", "HamsiManager_"+defaultLangCode+".qm")):
            languageFile.load(trForUI(InputOutputs.joinPath(Variables.HamsiManagerDirectory, "Languages", "HamsiManager_"+defaultLangCode+".qm")))
    HamsiManagerApp.installTranslator(languageFile)
    MTextCodec.setCodecForCStrings(MTextCodec.codecForName("utf-8"))
    MTextCodec.setCodecForTr(MTextCodec.codecForName("utf-8"))
    HamsiManagerApp.setWindowIcon(MIcon("Images:hamsi.png"))
    HamsiManagerApp.setApplicationName("UninstallHamsiManager")
    HamsiManagerApp.setApplicationVersion(Variables.version)
    HamsiManagerApp.setOrganizationDomain("hamsiapps.com")
    HamsiManagerApp.setOrganizationName("Hamsi Apps")
    from Core import MyConfigure
    class Main(MMainWindow):
        def __init__(self, parent=None):
            MMainWindow.__init__(self, parent)
            Universals.setApp(HamsiManagerApp)
            Universals.setMainWindow(self)
            Universals.fillRemainderUniversals()
            self.isUninstallFinised = False
            self.pageNo, self.pageSize = 0, 3
            self.vblMain = MVBoxLayout()
            self.hblMain = MHBoxLayout()
            self.lblLeftImage = MLabel()
            self.pmapLeftImage = MPixmap("Images:HamsiManager-256x256-1.png")
            self.lblLeftImage.setPixmap(self.pmapLeftImage)
            self.vblLeftColumn = MVBoxLayout()
            self.vblLeftColumn.addStretch(1)
            self.vblLeftColumn.addWidget(self.lblLeftImage)
            self.vblLeftColumn.addStretch(5)
            self.hblMain.addLayout(self.vblLeftColumn)
            self.pages = []
            for pageNo in range(self.pageSize):
                self.pages.append(self.createPage(pageNo))
                if pageNo!=self.pageNo:
                    self.pages[-1].setVisible(False)
                self.hblMain.addWidget(self.pages[-1])
            self.vblMain.addLayout(self.hblMain, 20)
            self.hblButtons = MHBoxLayout()
            self.buttons = [MPushButton(MApplication.translate("Uninstall", "Back")), 
                            MPushButton(MApplication.translate("Uninstall", "Forward")), 
                            MPushButton(MApplication.translate("Uninstall", "Uninstall"))]
            self.hblButtons.addStretch(5)
            for btnNo, btn in enumerate(self.buttons):
                if btnNo==len(self.buttons)-1 or btnNo==0:
                    btn.setVisible(False)
                self.hblButtons.addWidget(btn, 1)
                self.connect(btn,SIGNAL("clicked()"),self.pageChanged)
            self.pbtnCancel = MPushButton(MApplication.translate("Uninstall", "Cancel"))
            self.hblButtons.addWidget(self.pbtnCancel, 1)
            self.connect(self.pbtnCancel,SIGNAL("clicked()"),self.close)
            self.pbtnFinish = MPushButton(MApplication.translate("Uninstall", "OK"))
            self.hblButtons.addWidget(self.pbtnFinish, 1)
            self.connect(self.pbtnFinish,SIGNAL("clicked()"),self.finish)
            self.pbtnFinish.setVisible(False)
            self.vblMain.addLayout(self.hblButtons)
            self.CentralWidget = MWidget()
            self.CentralWidget.setLayout(self.vblMain)
            self.setCentralWidget(self.CentralWidget)
        
        def createPage(self, _pageNo):
            pnlPage = MWidget()
            HBox = MHBoxLayout()
            pnlPage.setLayout(HBox)
            if _pageNo==0:
                VBox = MVBoxLayout()
                self.lblAreYouSure = MLabel(MApplication.translate("Uninstall", "Are you sure you want to uninstall Hamsi Manager?"))
                VBox.addStretch(10)
                VBox.addWidget(self.lblAreYouSure)
                VBox.addStretch(10)
                HBox.addLayout(VBox)
            if _pageNo==1:
                lblPleaseSelect = MLabel(MApplication.translate("Uninstall", "Please Select Directory Of Hamsi Manager To Uninstall."))
                UninstallationDirPath = InputOutputs.getDirName(trForUI(Settings.getUniversalSetting("HamsiManagerPath", trForUI(Variables.HamsiManagerDirectory))))
                self.leUninstallationDirectory = MLineEdit(trForUI(Settings.getUniversalSetting("pathOfInstallationDirectory", trForUI(UninstallationDirPath))))
                self.pbtnSelectUninstallationDirectory = MPushButton(MApplication.translate("Uninstall", "Browse"))
                self.connect(self.pbtnSelectUninstallationDirectory,SIGNAL("clicked()"),self.selectUninstallationDirectory)
                VBox = MVBoxLayout()
                VBox.addStretch(2)
                VBox.addWidget(lblPleaseSelect)
                HBox1 = MHBoxLayout()
                HBox1.addWidget(self.leUninstallationDirectory)
                HBox1.addWidget(self.pbtnSelectUninstallationDirectory)
                VBox.addLayout(HBox1)
                VBox.addStretch(2)
                HBox.addLayout(VBox)
            elif _pageNo==2:
                import MyPlugins
                self.lblFinished = MLabel(MApplication.translate("Uninstall", "Uninstallation Completed."))
                VBox = MVBoxLayout()
                VBox.addStretch(2)
                VBox.addWidget(self.lblFinished)
                VBox.addStretch(2)
                wPlugins = MyPlugins.MyPluginsForSystem(pnlPage, "uninstall")
                VBox.addWidget(wPlugins)
                VBox.addStretch(2)
                HBox.addLayout(VBox)
            return pnlPage
        
        def selectUninstallationDirectory(self):
            insDir = Dialogs.getExistingDirectory(MApplication.translate("Uninstall", "Please Select Directory Of Hamsi Manager To Uninstall."),self.leUninstallationDirectory.text())
            if insDir is not None:
                self.leUninstallationDirectory.setText(trForUI(insDir))
            
        def pageChanged(self, _isRunningManual=False):
            try:
                if _isRunningManual==False:
                    senderObject = self.sender()
                    if senderObject==self.buttons[1]:
                        self.pageNo+=1
                    elif senderObject==self.buttons[0]:
                        self.pageNo-=1
                    elif senderObject==self.buttons[2]:
                        self.pageNo+=1
                for pageNo, pnlPage in enumerate(self.pages):
                    if pageNo!=self.pageNo:
                        pnlPage.setVisible(False)
                    else:
                        pnlPage.setVisible(True)
                self.buttons[0].setVisible(False)
                self.buttons[1].setVisible(False)
                self.buttons[2].setVisible(False)
                self.buttons[1].setText(MApplication.translate("Uninstall", "Forward"))
                if self.pageNo==0:
                    self.buttons[1].setVisible(True)
                    self.buttons[1].setText(MApplication.translate("Uninstall", "Yes"))
                elif self.pageNo==1:
                    self.buttons[1].setVisible(False)
                    self.buttons[2].setVisible(True)
                elif self.pageNo==2:
                    self.buttons[0].setVisible(False)
                    self.buttons[1].setVisible(False)
                    self.buttons[2].setVisible(False)
                    self.pbtnCancel.setVisible(False)
                    self.pbtnFinish.setVisible(True)
                if _isRunningManual==False:
                    if senderObject==self.buttons[2]:
                        self.uninstall()
            except:
                from Core import ReportBug
                ReportBug.ReportBug()
                
        def uninstall(self):
            try:
                MApplication.processEvents()
                self.UninstallationDirectory = str(self.leUninstallationDirectory.text())
                if len(self.UninstallationDirectory)>0:
                    if self.UninstallationDirectory[-1]==InputOutputs.sep:
                        self.UninstallationDirectory = self.UninstallationDirectory[:-1]
                    if self.UninstallationDirectory==Variables.HamsiManagerDirectory:
                        self.pageNo-=1
                        Dialogs.showError(MApplication.translate("Uninstall", "The path you selected is not valid."),
                                    MApplication.translate("Uninstall", "The selected path is Hamsi Manager source directory.<br>Please choose a valid uninstallation path."))
                    elif InputOutputs.isDir(self.UninstallationDirectory):
                        InputOutputs.removeFileOrDir(self.UninstallationDirectory)
                        self.pageNo+=1
                    else:
                        self.pageNo-=1
                        Dialogs.showError(MApplication.translate("Uninstall", "The path you selected is not valid."),
                                    MApplication.translate("Uninstall", "The selected path points to a file not a folder.<br>Please choose a valid Uninstallation path."))
                else:
                    self.pageNo-=1
                    Dialogs.showError(MApplication.translate("Uninstall", "The path you selected is not valid."),
                                MApplication.translate("Uninstall", "The selected path points to a file not a folder.<br>Please choose a valid Uninstallation path."))
                self.pageChanged(True)
            except:
                from Core import ReportBug
                ReportBug.ReportBug()
            
        def finish(self):
            try:
                if Variables.isRunningAsRoot():
                    executableLink = Settings.getUniversalSetting("HamsiManagerExecutableLinkPath", trForUI("/usr/bin/hamsi"))
                    if InputOutputs.isFile(executableLink) or InputOutputs.isLink(executableLink):
                        InputOutputs.removeFileOrDir(executableLink)
                else:
                    desktopPath = Variables.getUserDesktopPath()
                    if Variables.isWindows:
                        if InputOutputs.isFile(InputOutputs.joinPath(desktopPath, "Hamsi Manager.lnk")):
                            InputOutputs.removeFileOrDir(InputOutputs.joinPath(desktopPath, "Hamsi Manager.lnk"))
                    else:
                        if InputOutputs.isFile(InputOutputs.joinPath(desktopPath, "HamsiManager.desktop")):
                            InputOutputs.removeFileOrDir(InputOutputs.joinPath(desktopPath, "HamsiManager.desktop"))
                    if InputOutputs.isFile(InputOutputs.joinPath(Variables.userDirectoryPath, ".local", "applications", "HamsiManager.desktop")):
                        InputOutputs.removeFileOrDir(InputOutputs.joinPath(Variables.userDirectoryPath, ".local", "applications", "HamsiManager.desktop"))
                self.isUninstallFinised = True
                self.close()
            except:
                from Core import ReportBug
                ReportBug.ReportBug()
            
    if Variables.isRunningAsRoot()==False and Variables.isRunableAsRoot():
        answer = Dialogs.askSpecial(MApplication.translate("Uninstall", "Are You Want To Run As Root?"), MApplication.translate("Uninstall", "Hamsi Manager Uninstaller is running with user privileges.<br>Do you want to run Hamsi Manager Uninstaller with root rights?"), MApplication.translate("Uninstall", "Yes"), MApplication.translate("Uninstall", "No (Continue as is)"), None)
        if answer==MApplication.translate("Uninstall", "Yes"):
            NewApp = Execute.executeAsRootWithThread([], "HamsiManagerUninstaller")
            sys.exit()
    try:
        MainWidget=Main()
        MainWidget.setWindowTitle(MApplication.translate("Uninstall", "Hamsi Manager Uninstaller") + " " + Variables.version)
        MainWidget.setGeometry(300, 300, 650, 350)
        MainWidget.show()
        Universals.isStartingSuccessfully = True
    except:
        from Core import ReportBug
        ReportBug.ReportBug()
    sys.exit(HamsiManagerApp.exec_())
else:
    sys.exit()
    
    
        
    
