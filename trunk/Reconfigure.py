#!/usr/bin/env python
## This file is part of HamsiManager.
## 
## Copyright (c) 2010 Murat Demir <mopened@gmail.com>      
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
if RoutineChecks.checkQt4Exist():
    from Core import Settings
    Universals.fillMySettings(False, False, False)
    Universals.isActivePyKDE4 = False
    from Core.MyObjects import *
    import InputOutputs
    from Core import Dialogs
    from Core import Execute
    defaultLangCode = str(MLocale().name())
    HamsiManagerApp = MApplication(sys.argv)
    MDir.setSearchPaths("Images", MStringList(trForM(Variables.HamsiManagerDirectory+"/Themes/Default/Images/")))
    StyleFile = open(Variables.HamsiManagerDirectory+"/Themes/Default/Style.qss") 
    HamsiManagerApp.setStyleSheet(StyleFile.read())
    languageFile = MTranslator()
    if InputOutputs.isFile(Variables.HamsiManagerDirectory+"/Languages/HamsiManagerWithQt_"+defaultLangCode+".qm"):
            languageFile.load(trForM(Variables.HamsiManagerDirectory+"/Languages/HamsiManagerWithQt_"+defaultLangCode+".qm"))
    elif InputOutputs.isFile(Variables.HamsiManagerDirectory+"/Languages/HamsiManager_"+defaultLangCode+".qm"):
            languageFile.load(trForM(Variables.HamsiManagerDirectory+"/Languages/HamsiManager_"+defaultLangCode+".qm"))
    HamsiManagerApp.installTranslator(languageFile)
    MTextCodec.setCodecForCStrings(MTextCodec.codecForName("utf-8"))
    MTextCodec.setCodecForTr(MTextCodec.codecForName("utf-8"))
    HamsiManagerApp.setWindowIcon(MIcon("Images:HamsiManager-128x128.png"))
    HamsiManagerApp.setApplicationName("ConfigureHamsiManager")
    HamsiManagerApp.setApplicationVersion(Variables.version)
    HamsiManagerApp.setOrganizationDomain("hamsiapps.com")
    HamsiManagerApp.setOrganizationName("Hamsi Apps")
    activePageNo = 0
    isOnlyRoot = False
    if len(sys.argv)>1:
        if sys.argv[1]=="--configurePage":
            activePageNo = 2
        if sys.argv[1]=="--pluginPage":
            activePageNo = 3
        for argv in sys.argv:
            if argv=="--onlyRoot":
                isOnlyRoot = True
    from Core import MyConfigure
    class Main(MMainWindow):
        def __init__(self, parent=None):
            MMainWindow.__init__(self, parent)
            Universals.setApp(HamsiManagerApp)
            Universals.setMainWindow(self)
            Universals.fillUIUniversals()
            self.isInstallFinised = False
            self.pageNo, self.pageSize = activePageNo, 4
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
            self.buttons = [MPushButton(MApplication.translate("Reconfigure", "Back")), 
                            MPushButton(MApplication.translate("Reconfigure", "Forward")), 
                            MPushButton(MApplication.translate("Reconfigure", "Reconfigure"))]
            self.hblButtons.addStretch(5)
            for btnNo, btn in enumerate(self.buttons):
                if btnNo==len(self.buttons)-1 or btnNo==0:
                    btn.setVisible(False)
                self.hblButtons.addWidget(btn, 1)
                self.connect(btn,SIGNAL("clicked()"),self.pageChanged)
            self.pbtnCancel = MPushButton(MApplication.translate("Reconfigure", "Cancel"))
            self.pbtnFinish = MPushButton(MApplication.translate("Reconfigure", "Finish"))
            self.pbtnFinish.setVisible(False)
            self.hblButtons.addWidget(self.pbtnCancel, 1)
            self.hblButtons.addWidget(self.pbtnFinish, 1)
            self.connect(self.pbtnCancel,SIGNAL("clicked()"),self.close)
            self.connect(self.pbtnFinish,SIGNAL("clicked()"),self.close)
            self.vblMain.addLayout(self.hblButtons)
            self.CentralWidget = MWidget()
            self.CentralWidget.setLayout(self.vblMain)
            self.setCentralWidget(self.CentralWidget)
            self.pageChanged(True)
        
        def createPage(self, _pageNo):
            pnlPage = MWidget()
            HBox = MHBoxLayout()
            pnlPage.setLayout(HBox)
            if _pageNo==0:
                if InputOutputs.isFile(Variables.HamsiManagerDirectory+"/Languages/About_"+defaultLangCode):
                    aboutFileContent = InputOutputs.readFromFile(Variables.HamsiManagerDirectory+"/Languages/About_"+defaultLangCode, "utf-8")
                else:
                    aboutFileContent = InputOutputs.readFromFile(Variables.HamsiManagerDirectory+"/Languages/About_en_GB", "utf-8")
                lblAbout = MLabel(trForUI(aboutFileContent))
                lblAbout.setWordWrap(True)
                HBox.addWidget(lblAbout)
            elif _pageNo==1:
                if InputOutputs.isFile(Variables.HamsiManagerDirectory+"/Languages/License_"+defaultLangCode):
                    lisenceFileContent = InputOutputs.readFromFile(Variables.HamsiManagerDirectory+"/Languages/License_"+defaultLangCode, "utf-8")
                else:
                    lisenceFileContent = InputOutputs.readFromFile(Variables.HamsiManagerDirectory+"/Languages/License_en_GB", "utf-8")
                teCopying = MTextEdit()
                teCopying.setPlainText(trForUI(lisenceFileContent))
                HBox.addWidget(teCopying)
            elif _pageNo==2:
                VBox = MVBoxLayout()
                VBox.addStretch(10)
                self.isCreateDesktopShortcut = None
                self.isCreateExecutableLink = None
                if Variables.isRunningAsRoot():
                    self.isCreateExecutableLink = MCheckBox(MApplication.translate("Reconfigure", "Add To The System"))
                    self.isCreateExecutableLink.setCheckState(Mt.Checked)
                    lblExecutableLink = MLabel(MApplication.translate("Reconfigure", "Executable Link Path : "))
                    self.leExecutableLink = MLineEdit(trForM(Settings.getUniversalSetting("pathOfExecutableHamsi", "/usr/bin/hamsi")))
                    self.connect(self.isCreateExecutableLink, SIGNAL("stateChanged(int)"),self.createExecutableLinkChanged)
                    VBox.addWidget(self.isCreateExecutableLink)
                    HBox1 = MHBoxLayout()
                    HBox1.addWidget(lblExecutableLink)
                    HBox1.addWidget(self.leExecutableLink, 10)
                    VBox.addLayout(HBox1)
                else:
                    self.isCreateDesktopShortcut = MCheckBox(MApplication.translate("Reconfigure", "Create Desktop Shortcut."))
                    self.isCreateDesktopShortcut.setCheckState(Mt.Checked)
                    VBox.addWidget(self.isCreateDesktopShortcut)
                VBox.addStretch(10)
                HBox.addLayout(VBox)
            elif _pageNo==3:
                import MyPlugins
                VBox = MVBoxLayout()
                VBox.addStretch(10)
                wPlugins = MyPlugins.MyPluginsForSystem(self)
                HBox.addWidget(wPlugins)
                VBox.addStretch(10)
                HBox.addLayout(VBox)
            return pnlPage
        
        def createExecutableLinkChanged(self, _value):
            if _value==0:
                self.leExecutableLink.setEnabled(False)
            else:
                self.leExecutableLink.setEnabled(True)
            
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
            self.buttons[1].setText(MApplication.translate("Reconfigure", "Forward"))
            if self.pageNo==0:
                self.buttons[1].setVisible(True)
            elif self.pageNo==1:
                self.buttons[1].setVisible(True)
                self.buttons[1].setText(MApplication.translate("Reconfigure", "Accept"))
            elif self.pageNo==2:
                self.buttons[0].setVisible(False)
                self.buttons[1].setVisible(False)
                self.buttons[2].setVisible(True)
                self.pbtnCancel.setVisible(True)
            elif self.pageNo==3:
                self.buttons[0].setVisible(False)
                self.buttons[1].setVisible(False)
                self.buttons[2].setVisible(False)
                self.pbtnCancel.setVisible(False)
                self.pbtnFinish.setVisible(True)
                self.isInstallFinised = True
            if _isRunningManual==False:
                if senderObject==self.buttons[2]:
                    self.reConfigure()
            
        def reConfigure(self):
            oldPathOfExecutableHamsi = Settings.getUniversalSetting("pathOfExecutableHamsi", "/usr/bin/hamsi")
            if InputOutputs.isFile(Variables.HamsiManagerDirectory + "/HamsiManager.desktop"):
                MyConfigure.reConfigureFile(Variables.HamsiManagerDirectory + "/HamsiManager.desktop", Variables.HamsiManagerDirectory)
            if self.isCreateDesktopShortcut!=None:
                if self.isCreateDesktopShortcut.checkState()==Mt.Checked:
                    from Core import Settings
                    desktopPath = Variables.getUserDesktopPath()
                    fileContent = MyConfigure.getConfiguredDesktopFileContent(Variables.HamsiManagerDirectory)
                    InputOutputs.writeToFile(desktopPath + "/HamsiManager.desktop", fileContent)
            executableLink = str(self.leExecutableLink)
            if self.isCreateExecutableLink!=None:
                if self.isCreateExecutableLink.checkState()==Mt.Checked:
                    if executableLink.strip()!="":
                        HamsiManagerFileName = Execute.findExecutableBaseName("HamsiManager")
                        InputOutputs.createSymLink(Variables.HamsiManagerDirectory+"/"+HamsiManagerFileName, executableLink)
                        Settings.setUniversalSetting("pathOfExecutableHamsi", executableLink)
                        if oldPathOfExecutableHamsi!=executableLink:
                            if InputOutputs.isFile(oldPathOfExecutableHamsi):
                                answer = Dialogs.ask(MApplication.translate("Reconfigure", "Other Hamsi Manager Was Detected"), 
                                    str(MApplication.translate("Reconfigure", "Other Hamsi Manager executable file was detected. Are you want to delete old executable file? You can delete this old executable file : \"%s\"")) % (oldPathOfExecutableHamsi))
                                if answer!=Dialogs.Yes:
                                    InputOutputs.removeFile(oldPathOfExecutableHamsi)
                    if InputOutputs.isDir("/usr/share/applications/"):
                        fileContent = MyConfigure.getConfiguredDesktopFileContent(Variables.HamsiManagerDirectory)
                        InputOutputs.writeToFile("/usr/share/applications/HamsiManager.desktop", fileContent)
            if Variables.isRunningAsRoot()==False:
                if InputOutputs.isDir(Variables.userDirectoryPath + "/.local/applications/")==False:
                    InputOutputs.makeDirs(Variables.userDirectoryPath + "/.local/applications/")
                fileContent = MyConfigure.getConfiguredDesktopFileContent(Variables.HamsiManagerDirectory)
                InputOutputs.writeToFile(Variables.userDirectoryPath + "/.local/applications/HamsiManager.desktop", fileContent)
            MyConfigure.installKDE4Languages()
            self.isInstallFinised = True
            
        def closeEvent(self, _event):
            if self.isInstallFinised==False:
                answer = Dialogs.ask(MApplication.translate("Reconfigure", "Finalizing Configuration"), 
                            MApplication.translate("Reconfigure", "Are You Sure You Want To Quit?"))
                if answer!=Dialogs.Yes:
                    _event.ignore()
            
    if Variables.isRunningAsRoot()==False and Variables.isRunableAsRoot():
        if isOnlyRoot:
            answer = Dialogs.askSpecial(MApplication.translate("Reconfigure", "Are You Want To Run As Root?"), MApplication.translate("Reconfigure", "Hamsi Manager Configure Tool is running with user privileges.<br>Do you want to run Hamsi Manager Configure Tool with root rights?<br>"), MApplication.translate("Reconfigure", "Yes"), MApplication.translate("Reconfigure", "No (Close)"), None)
        else:
            answer = Dialogs.askSpecial(MApplication.translate("Reconfigure", "Are You Want To Run As Root?"), MApplication.translate("Reconfigure", "Hamsi Manager Configure Tool is running with user privileges.<br>Do you want to run Hamsi Manager Configure Tool with root rights?<br>"), MApplication.translate("Reconfigure", "Yes"), MApplication.translate("Reconfigure", "No (Continue as is)"), None)
        if answer==MApplication.translate("Reconfigure", "Yes"):
            myParametres = []
            if len(sys.argv)>1:
                for x in sys.argv[1:]:
                    myParametres.append(x)
            NewApp = Execute.executeAsRootWithThread(myParametres, "Reconfigure")
            sys.exit()
        elif isOnlyRoot:
            sys.exit()
    MainWidget=Main()
    MainWidget.setWindowTitle(MApplication.translate("Reconfigure", "Hamsi Manager Configure Tool") + " " + MApplication.applicationVersion())
    MainWidget.setGeometry(300, 300, 650, 350)
    MainWidget.show()
    Universals.isStartingSuccessfully = True
    sys.exit(HamsiManagerApp.exec_())
else:
    sys.exit()
    
    
        
    
