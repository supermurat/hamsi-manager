#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
reload(sys)
sys.setdefaultencoding("utf-8")
if str(sys.path[0])=="":
    sys.path.insert(0, sys.path[1])
sys.path.insert(1,sys.path[0]+"/Core")
import RoutineChecks
if RoutineChecks.checkPyQt4Exist():
    import Universals
    Universals.fillMySettings(False, False, False)
    Universals.isActivePyKDE4 = False
    from MyObjects import *
    import InputOutputs
    import Dialogs
    defaultLangCode = str(MLocale().name())
    HamsiManagerApp = MApplication(sys.argv)
    MDir.setSearchPaths("Images", MStringList((Universals.HamsiManagerDirectory+"/Themes/Default/Images/").decode("utf-8")))
    StyleFile = open(Universals.HamsiManagerDirectory+"/Themes/Default/Style.qss") 
    HamsiManagerApp.setStyleSheet(StyleFile.read())
    languageFile = MTranslator()
    if InputOutputs.isFile(Universals.HamsiManagerDirectory+"/Languages/" + str("HamsiManagerWithQt_"+defaultLangCode+".qm")):
            languageFile.load((Universals.HamsiManagerDirectory+"/Languages/" + str("HamsiManagerWithQt_"+defaultLangCode+".qm")).decode("utf-8"))
    elif InputOutputs.isFile(Universals.HamsiManagerDirectory+"/Languages/" + str("HamsiManager_"+defaultLangCode+".qm")):
            languageFile.load((Universals.HamsiManagerDirectory+"/Languages/" + str("HamsiManager_"+defaultLangCode+".qm")).decode("utf-8"))
    HamsiManagerApp.installTranslator(languageFile)
    HamsiManagerApp.setWindowIcon(MIcon("Images:HamsiManager.png"))
    HamsiManagerApp.setApplicationName("ConfigureHamsiManager")
    HamsiManagerApp.setApplicationVersion(RoutineChecks.__version__)
    HamsiManagerApp.setOrganizationDomain("hamsiapps.com")
    HamsiManagerApp.setOrganizationName("Hamsi Apps")
    activePageNo = 0
    if len(sys.argv)>1:
        if sys.argv[1]=="-configurePage":
            activePageNo = 2
    import MyConfigure
    class Main(MWidget):
        def __init__(self, parent=None):
            MWidget.__init__(self, parent)
            Universals.MainWindow = self
            self.isInstallFinised = False
            self.pageNo, self.pageSize = activePageNo, 3
            self.vblMain = MVBoxLayout()
            self.hblMain = MHBoxLayout()
            self.lblLeftImage = MLabel()
            self.pmapLeftImage = MPixmap("Images:HamsiManager.png")
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
            self.buttons = [MPushButton(MApplication.translate("ReConfigure", "Back")), 
                            MPushButton(MApplication.translate("ReConfigure", "Forward")), 
                            MPushButton(MApplication.translate("ReConfigure", "Re Configure"))]
            self.hblButtons.addStretch(5)
            for btnNo, btn in enumerate(self.buttons):
                if btnNo==len(self.buttons)-1 or btnNo==0:
                    btn.setVisible(False)
                self.hblButtons.addWidget(btn, 1)
                self.connect(btn,SIGNAL("clicked()"),self.pageChanged)
            self.pbtnCancel = MPushButton(MApplication.translate("ReConfigure", "Cancel"))
            self.hblButtons.addWidget(self.pbtnCancel, 1)
            self.connect(self.pbtnCancel,SIGNAL("clicked()"),self.close)
            self.vblMain.addLayout(self.hblButtons)
            self.setLayout(self.vblMain)
        
        def createPage(self, _pageNo):
            pnlPage = MWidget()
            HBox = MHBoxLayout()
            pnlPage.setLayout(HBox)
            if _pageNo==0:
                try:f = open(Universals.HamsiManagerDirectory+"/Languages/About_"+defaultLangCode)
                except:f = open(Universals.HamsiManagerDirectory+"/Languages/About_en_GB")
                lblAbout = MLabel(f.read().decode("utf-8"))
                lblAbout.setWordWrap(True)
                HBox.addWidget(lblAbout)
            elif _pageNo==1:
                try:f = open(Universals.HamsiManagerDirectory+"/Languages/License_"+defaultLangCode)
                except:f = open(Universals.HamsiManagerDirectory+"/Languages/License_en_GB")
                teCopying = MTextEdit()
                teCopying.setPlainText(f.read().decode("utf-8"))
                HBox.addWidget(teCopying)
            elif _pageNo==2:
                VBox = MVBoxLayout()
                self.isCreateDesktopShortcut = MCheckBox(MApplication.translate("ReConfigure", "Create Desktop Shortcut."))
                self.isCreateDesktopShortcut.setCheckState(Mt.Checked)
                self.lblFinished = MLabel(MApplication.translate("ReConfigure", "Installation Complete."))
                VBox.addStretch(10)
                VBox.addWidget(self.lblFinished)
                VBox.addWidget(self.isCreateDesktopShortcut)
                if Execute.isRunningAsRoot():
                    self.isCreateExecutableLink = MCheckBox(MApplication.translate("ReConfigure", "Add To The System"))
                    self.isCreateExecutableLink.setCheckState(Mt.Checked)
                    lblExecutableLink = MLabel(MApplication.translate("ReConfigure", "Executable Link Path : "))
                    self.leExecutableLink = MLineEdit(u"/usr/bin/hamsi")
                    self.connect(self.isCreateExecutableLink, SIGNAL("stateChanged(int)"),self.createExecutableLinkChanged)
                    VBox.addWidget(self.isCreateExecutableLink)
                    HBox1 = MHBoxLayout()
                    HBox1.addWidget(lblExecutableLink)
                    HBox1.addWidget(self.leExecutableLink)
                    VBox.addLayout(HBox1)
                else:
                    self.isCreateExecutableLink = None
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
            self.buttons[1].setText(MApplication.translate("ReConfigure", "Forward"))
            if self.pageNo==0:
                self.buttons[1].setVisible(True)
            elif self.pageNo==1:
                self.buttons[1].setVisible(True)
                self.buttons[1].setText(MApplication.translate("ReConfigure", "Accept"))
            elif self.pageNo==2:
                self.buttons[0].setVisible(False)
                self.buttons[1].setVisible(False)
                self.buttons[2].setVisible(True)
                self.pbtnCancel.setVisible(True)
            if _isRunningManual==False:
                if senderObject==self.buttons[2]:
                    self.reConfigure()
            
        def reConfigure(self):
            if InputOutputs.isFile(Universals.HamsiManagerDirectory + "/HamsiManager.desktop"):
                MyConfigure.reConfigureFile(Universals.HamsiManagerDirectory + "/HamsiManager.desktop", Universals.HamsiManagerDirectory)
            if self.isCreateDesktopShortcut.checkState()==Mt.Checked:
                import Settings
                desktopPath = Settings.getUserDesktopPath()
                fileContent = MyConfigure.getConfiguredDesktopFileContent(Universals.HamsiManagerDirectory)
                InputOutputs.writeToFile(desktopPath + "/HamsiManager.desktop", fileContent)
            executableLink = str(self.leExecutableLink)
            if self.isCreateExecutableLink!=None and executableLink.strip()!="":
                if self.isCreateExecutableLink.checkState()==Mt.Checked:
                    InputOutputs.createSymLink(Universals.HamsiManagerDirectory+"/HamsiManager.py", executableLink)
            self.isInstallFinised = True
            self.close()
            
        def closeEvent(self, _event):
            if self.isInstallFinised==False:
                answer = Dialogs.ask(MApplication.translate("ReConfigure", "Finalizing Configuration"), 
                            MApplication.translate("ReConfigure", "Are You Sure You Want To Quit?"))
                if answer!=Dialogs.Yes:
                    _event.ignore()
            
    import Execute
    if Execute.isRunningAsRoot()==False and Execute.isRunableAsRoot():
        answer = Dialogs.askSpecial(MApplication.translate("ReConfigure", "Are You Want To Run As Root?"), MApplication.translate("ReConfigure", "Hamsi Manager Configure Tool is running with user privileges.<br>Do you want to run Hamsi Manager Configure Tool with root rights?<br>"), MApplication.translate("ReConfigure", "Yes"), MApplication.translate("ReConfigure", "No (Continue as is)"), None)
        if answer==MApplication.translate("ReConfigure", "Yes"):
            myParametres = ""
            if len(sys.argv)>1:
                for x in sys.argv[1:]:
                    myParametres += x + " "
            NewApp = Execute.executeReConfigureAsRoot(myParametres)
            sys.exit()
    MainWidget=Main()
    MainWidget.setWindowTitle(MApplication.translate("ReConfigure", "Hamsi Manager Configure Tool") + " " + MApplication.applicationVersion())
    MainWidget.setGeometry(300, 300, 650, 350)
    MainWidget.show()
    Universals.isStartingSuccessfully = True
    sys.exit(HamsiManagerApp.exec_())
else:
    sys.exit()
    
    
        
    
