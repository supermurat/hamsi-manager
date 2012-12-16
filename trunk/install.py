#!/usr/bin/env python
## This file is part of HamsiManager.
## 
## Copyright (c) 2010 - 2012 Murat Demir <mopened@gmail.com>      
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
    MDir.setSearchPaths("Images", MStringList(trForM(InputOutputs.joinPath(Universals.themePath, "Images"))))
    StyleFile = open(InputOutputs.joinPath(Universals.themePath, "Style.qss"))
    HamsiManagerApp.setStyleSheet(StyleFile.read())
    languageFile = MTranslator()
    if InputOutputs.isFile(InputOutputs.joinPath(Variables.HamsiManagerDirectory, "Languages", "HamsiManagerWithQt_"+defaultLangCode+".qm")):
            languageFile.load(trForM(InputOutputs.joinPath(Variables.HamsiManagerDirectory, "Languages", "HamsiManagerWithQt_"+defaultLangCode+".qm")))
    elif InputOutputs.isFile(InputOutputs.joinPath(Variables.HamsiManagerDirectory, "Languages", "HamsiManager_"+defaultLangCode+".qm")):
            languageFile.load(trForM(InputOutputs.joinPath(Variables.HamsiManagerDirectory, "Languages", "HamsiManager_"+defaultLangCode+".qm")))
    HamsiManagerApp.installTranslator(languageFile)
    MTextCodec.setCodecForCStrings(MTextCodec.codecForName("utf-8"))
    MTextCodec.setCodecForTr(MTextCodec.codecForName("utf-8"))
    HamsiManagerApp.setWindowIcon(MIcon("Images:HamsiManager-128x128.png"))
    HamsiManagerApp.setApplicationName("InstallHamsiManager")
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
            self.isInstallFinised = False
            self.pageNo, self.pageSize = 0, 5
            self.vblMain = MVBoxLayout()
            self.hblMain = MHBoxLayout()
            self.lblLeftImage = MLabel()
            self.pmapLeftImage = MPixmap("Images:HamsiManager-128x176.png")
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
            self.buttons = [MPushButton(MApplication.translate("Install", "Back")), 
                            MPushButton(MApplication.translate("Install", "Forward")), 
                            MPushButton(MApplication.translate("Install", "Install"))]
            self.hblButtons.addStretch(5)
            for btnNo, btn in enumerate(self.buttons):
                if btnNo==len(self.buttons)-1 or btnNo==0:
                    btn.setVisible(False)
                self.hblButtons.addWidget(btn, 1)
                self.connect(btn,SIGNAL("clicked()"),self.pageChanged)
            self.pbtnCancel = MPushButton(MApplication.translate("Install", "Cancel"))
            self.pbtnCheckUpdate = MPushButton(translate("Install", "Check Update"))
            self.hblButtons.insertWidget(0, self.pbtnCheckUpdate, 1)
            self.hblButtons.addWidget(self.pbtnCancel, 1)
            self.connect(self.pbtnCancel,SIGNAL("clicked()"),self.close)
            self.connect(self.pbtnCheckUpdate,SIGNAL("clicked()"), self.checkUpdate)
            self.pbtnFinish = MPushButton(MApplication.translate("Install", "OK"))
            self.hblButtons.addWidget(self.pbtnFinish, 1)
            self.connect(self.pbtnFinish,SIGNAL("clicked()"),self.finish)
            self.pbtnFinish.setVisible(False)
            self.vblMain.addLayout(self.hblButtons)
            self.CentralWidget = MWidget()
            self.CentralWidget.setLayout(self.vblMain)
            self.setCentralWidget(self.CentralWidget)
        
        def checkUpdate(self):
            from Core import UpdateControl
            UpdateControl.UpdateControl(self, True)
        
        def createPage(self, _pageNo):
            pnlPage = MWidget()
            HBox = MHBoxLayout()
            pnlPage.setLayout(HBox)
            if _pageNo==0:
                if InputOutputs.isFile(InputOutputs.joinPath(Variables.HamsiManagerDirectory, "Languages", "About_"+defaultLangCode)):
                    aboutFileContent = InputOutputs.readFromFile(InputOutputs.joinPath(Variables.HamsiManagerDirectory, "Languages", "About_"+defaultLangCode), "utf-8")
                else:
                    aboutFileContent = InputOutputs.readFromFile(InputOutputs.joinPath(Variables.HamsiManagerDirectory, "Languages", "About_en_GB"), "utf-8")
                lblAbout = MLabel(trForUI(aboutFileContent))
                lblAbout.setWordWrap(True)
                HBox.addWidget(lblAbout)
            elif _pageNo==1:
                if InputOutputs.isFile(InputOutputs.joinPath(Variables.HamsiManagerDirectory, "Languages", "License_"+defaultLangCode)):
                    lisenceFileContent = InputOutputs.readFromFile(InputOutputs.joinPath(Variables.HamsiManagerDirectory, "Languages", "License_"+defaultLangCode), "utf-8")
                else:
                    lisenceFileContent = InputOutputs.readFromFile(InputOutputs.joinPath(Variables.HamsiManagerDirectory, "Languages", "License_en_GB"), "utf-8")
                teCopying = MTextEdit()
                teCopying.setPlainText(trForUI(lisenceFileContent))
                HBox.addWidget(teCopying)
            elif _pageNo==2:
                lblPleaseSelect = MLabel(MApplication.translate("Install", "Please Select A Folder For Installation."))
                installationDirPath = InputOutputs.getDirName(trForM(Settings.getUniversalSetting("HamsiManagerPath", trForUI(InputOutputs.joinPath(InputOutputs.getDirName(Variables.HamsiManagerDirectory), "HamsiManager")))))
                self.leInstallationDirectory = MLineEdit(trForM(Settings.getUniversalSetting("pathOfInstallationDirectory", trForUI(installationDirPath))))
                self.pbtnSelectInstallationDirectory = MPushButton(MApplication.translate("Install", "Browse"))
                self.connect(self.pbtnSelectInstallationDirectory,SIGNAL("clicked()"),self.selectInstallationDirectory)
                HBox.addWidget(self.leInstallationDirectory)
                HBox.addWidget(self.pbtnSelectInstallationDirectory)
            elif _pageNo==3:
                VBox = MVBoxLayout()
                self.lblActions =MLabel("")
                self.prgbState = MProgressBar()
                VBox.addWidget(self.lblActions)
                VBox.addWidget(self.prgbState)
                HBox.addLayout(VBox)
            elif _pageNo==4:
                VBox = MVBoxLayout()
                self.lblFinished = MLabel(MApplication.translate("Install", "Installation Complete."))
                VBox.addStretch(10)
                VBox.addWidget(self.lblFinished)
                self.isCreateDesktopShortcut = None
                self.isCreateExecutableLink = None
                if Variables.isRunningAsRoot():
                    self.isCreateExecutableLink = MCheckBox(MApplication.translate("Install", "Add To The System"))
                    self.isCreateExecutableLink.setCheckState(Mt.Checked)
                    lblExecutableLink = MLabel(MApplication.translate("Install", "Executable Link Path : "))
                    self.leExecutableLink = MLineEdit(trForM(Settings.getUniversalSetting("HamsiManagerExecutableLinkPath", "/usr/bin/hamsi")))
                    self.connect(self.isCreateExecutableLink, SIGNAL("stateChanged(int)"),self.createExecutableLinkChanged)
                    VBox.addWidget(self.isCreateExecutableLink)
                    HBox1 = MHBoxLayout()
                    HBox1.addWidget(lblExecutableLink)
                    HBox1.addWidget(self.leExecutableLink)
                    VBox.addLayout(HBox1)
                else:
                    self.isCreateDesktopShortcut = MCheckBox(MApplication.translate("Install", "Create Desktop Shortcut."))
                    self.isCreateDesktopShortcut.setCheckState(Mt.Checked)
                    VBox.addWidget(self.isCreateDesktopShortcut)
                VBox.addStretch(10)
                HBox.addLayout(VBox)
            return pnlPage
        
        def createExecutableLinkChanged(self, _value):
            if _value==0:
                self.leExecutableLink.setEnabled(False)
            else:
                self.leExecutableLink.setEnabled(True)
        
        def selectInstallationDirectory(self):
            dizin = QFileDialog.getExistingDirectory(self,MApplication.translate("Install", "Please select a folder for installation."),self.leInstallationDirectory.text())
            if dizin!="":
                self.leInstallationDirectory.setText(dizin)
            
        def pageChanged(self, _isRunningManual=False):
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
            self.pbtnCheckUpdate.setVisible(False)
            self.buttons[1].setText(MApplication.translate("Install", "Forward"))
            if self.pageNo==0:
                self.buttons[1].setVisible(True)
                self.pbtnCheckUpdate.setVisible(True)
            elif self.pageNo==1:
                self.buttons[1].setVisible(True)
                self.buttons[1].setText(MApplication.translate("Install", "Accept"))
                self.pbtnCheckUpdate.setVisible(True)
            elif self.pageNo==2:
                self.buttons[0].setVisible(True)
                self.buttons[2].setVisible(True)
            elif self.pageNo==3:
                pass
            elif self.pageNo==4:
                self.buttons[0].setVisible(False)
                self.buttons[1].setVisible(False)
                self.buttons[2].setVisible(False)
                self.pbtnCancel.setVisible(False)
                self.pbtnFinish.setVisible(True)
            if _isRunningManual==False:
                if senderObject==self.buttons[2]:
                    self.install()
                
        def install(self):
            MApplication.processEvents()
            self.installationDirectory = str(self.leInstallationDirectory.text())
            if self.installationDirectory[-1]==InputOutputs.sep:
                self.installationDirectory = self.installationDirectory[:-1]
            if self.installationDirectory==Variables.HamsiManagerDirectory:
                self.pageNo-=1
                self.lblActions.setText("")
                Dialogs.showError(MApplication.translate("Install", "The path you selected is not valid."),
                            MApplication.translate("Install", "The selected path is Hamsi Manager source directory.<br>Please choose a valid installation path."))
            elif InputOutputs.isFile(self.installationDirectory)==False:
                isMakeInstall=True
                if InputOutputs.isDir(self.installationDirectory)==False:
                    self.lblActions.setText(MApplication.translate("Install", "Creating Installation Folder..."))
                    InputOutputs.makeDirs(self.installationDirectory)
                elif len(InputOutputs.listDir(self.installationDirectory))>0:
                        answer = Dialogs.askSpecial(MApplication.translate("Install", "The Installation Path You Selected Is Not Empty."),
                                    MApplication.translate("Install", "If the path you selected is an \"Hamsi Manager\" installation path, <b>I recommend you to delete the older files.</b><br>Do you want me to clear the installation path/folder for you?<br><b>Note: </b> Your personal settings are <b>never deleted</b>."), 
                                    MApplication.translate("Install", "Yes (Recommended)"), 
                                    MApplication.translate("Install", "No (Overwrite)"), 
                                    MApplication.translate("Install", "Cancel"))
                        if answer==MApplication.translate("Install", "Yes (Recommended)"):
                            self.lblActions.setText(MApplication.translate("Install", "Clearing Installation Path..."))
                            InputOutputs.removeFileOrDir(self.installationDirectory, True)
                            InputOutputs.makeDirs(self.installationDirectory)
                            isMakeInstall=True
                        elif answer==MApplication.translate("Install", "No (Overwrite)"):
                            isMakeInstall=True
                        else:
                            isMakeInstall=False
                if isMakeInstall==True:
                    Settings.setUniversalSetting("pathOfInstallationDirectory", self.installationDirectory)
                    directoriesAndFiles = InputOutputs.readDirectoryWithSubDirectories(Variables.HamsiManagerDirectory)
                    self.prgbState.setRange(0,len(directoriesAndFiles))
                    self.lblActions.setText(MApplication.translate("Install", "Copying Files And Folders..."))
                    installFileName = Execute.findExecutableBaseName("HamsiManagerInstaller")
                    for fileNo, fileName in enumerate(directoriesAndFiles):
                        MApplication.processEvents()
                        newFileName = self.installationDirectory + fileName.replace(Variables.HamsiManagerDirectory, "")
                        if InputOutputs.isDir(fileName):
                            try:InputOutputs.makeDirs(newFileName)
                            except:pass
                        elif InputOutputs.isFile(fileName) and InputOutputs.getBaseName(fileName)!="install.py" and InputOutputs.getBaseName(fileName)!=installFileName:
                            try:
                                InputOutputs.copyFileOrDir(fileName, newFileName)
                            except:
                                fileContent = InputOutputs.readFromFile(fileName)
                                InputOutputs.writeToFile(newFileName, fileContent)
                        self.prgbState.setValue(fileNo+1)
                    self.pageNo+=1
                    if InputOutputs.isFile(InputOutputs.joinPath(self.installationDirectory, "ConfigureUpdate.py")):
                        InputOutputs.moveFileOrDir(InputOutputs.joinPath(self.installationDirectory, "ConfigureUpdate.py"), InputOutputs.joinPath(self.installationDirectory, "Update.py"))
                    else:
                        configureUpdateFileName = Execute.findExecutableBaseName("ConfigureUpdate")
                        if configureUpdateFileName!=None:
                            if InputOutputs.isFile(InputOutputs.joinPath(self.installationDirectory, configureUpdateFileName)):
                                extOfFile = ""
                                if configureUpdateFileName.find(".")!=-1:
                                    extOfFile = "." + (configureUpdateFileName.split(".")[1])
                                InputOutputs.moveFileOrDir(InputOutputs.joinPath(self.installationDirectory, configureUpdateFileName), InputOutputs.joinPath(self.installationDirectory, "Update" + extOfFile))
                    MyConfigure.installKDE4Languages()
                else:
                    self.pageNo-=1
            else:
                self.pageNo-=1
                self.lblActions.setText("")
                Dialogs.showError(MApplication.translate("Install", "The path you selected is not valid."),
                            MApplication.translate("Install", "The selected path points to a file not a folder.<br>Please choose a valid installation path."))
            self.pageChanged(True)
        
        def closeEvent(self, _event):
            if self.isInstallFinised==False:
                answer = Dialogs.ask(MApplication.translate("Install", "Finalizing Installation"), 
                            MApplication.translate("Install", "Are You Sure You Want To Quit?"))
                if answer!=Dialogs.Yes:
                    _event.ignore()
            
        def finish(self):
            Settings.setUniversalSetting("isUpdatable", "True")
            if InputOutputs.isFile(InputOutputs.joinPath(self.installationDirectory, "HamsiManager.desktop")):
                MyConfigure.reConfigureFile(InputOutputs.joinPath(self.installationDirectory, "HamsiManager.desktop"), self.installationDirectory)
            if self.isCreateDesktopShortcut!=None:
                if self.isCreateDesktopShortcut.checkState()==Mt.Checked:
                    desktopPath = Variables.getUserDesktopPath()
                    if Variables.isWindows:
                        MyConfigure.createShortCutFile(InputOutputs.joinPath(desktopPath, "Hamsi Manager.lnk"))
                    else:
                        fileContent = MyConfigure.getConfiguredDesktopFileContent(self.installationDirectory)
                        InputOutputs.writeToFile(InputOutputs.joinPath(desktopPath, "HamsiManager.desktop"), fileContent)
            if self.isCreateExecutableLink!=None:
                executableLink = str(self.leExecutableLink.text())
                if self.isCreateExecutableLink.checkState()==Mt.Checked:
                    if executableLink.strip()!="":
                        HamsiManagerFileName = Execute.findExecutableBaseName("HamsiManager")
                        InputOutputs.createSymLink(InputOutputs.joinPath(self.installationDirectory, HamsiManagerFileName), executableLink)
                        Settings.setUniversalSetting("HamsiManagerExecutableLinkPath", executableLink)
                    if InputOutputs.isDir("/usr/share/applications/"):
                        fileContent = MyConfigure.getConfiguredDesktopFileContent(self.installationDirectory)
                        InputOutputs.writeToFile("/usr/share/applications/HamsiManager.desktop", fileContent)
            if Variables.isRunningAsRoot()==False:
                if InputOutputs.isDir(InputOutputs.joinPath(Variables.userDirectoryPath, ".local", "applications"))==False:
                    InputOutputs.makeDirs(InputOutputs.joinPath(Variables.userDirectoryPath, ".local", "applications"))
                fileContent = MyConfigure.getConfiguredDesktopFileContent(self.installationDirectory)
                InputOutputs.writeToFile(InputOutputs.joinPath(Variables.userDirectoryPath, ".local", "applications", "HamsiManager.desktop"), fileContent)
            self.isInstallFinised = True
            self.close()
            
    if Variables.isRunningAsRoot()==False and Variables.isRunableAsRoot():
        answer = Dialogs.askSpecial(MApplication.translate("Install", "Are You Want To Run As Root?"), MApplication.translate("Install", "Hamsi Manager Installer is running with user privileges.<br>Do you want to run Hamsi Manager installer with root rights?<br><b>Note: </b>The other users on your system has to inherit these permissions and install the program to a location other than their /home directories."), MApplication.translate("Install", "Yes"), MApplication.translate("Install", "No (Continue as is)"), None)
        if answer==MApplication.translate("Install", "Yes"):
            NewApp = Execute.executeAsRootWithThread([], "HamsiManagerInstaller")
            sys.exit()
    MainWidget=Main()
    MainWidget.setWindowTitle(MApplication.translate("Install", "Hamsi Manager Installer") + " " + Variables.version)
    MainWidget.setGeometry(300, 300, 650, 350)
    MainWidget.show()
    Universals.isStartingSuccessfully = True
    sys.exit(HamsiManagerApp.exec_())
else:
    sys.exit()
    
    
        
    
