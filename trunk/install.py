#!/usr/bin/env python
## This file is part of HamsiManager.
##
## Copyright (c) 2010 - 2014 Murat Demir <mopened@gmail.com>
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

try:
    if float(sys.version[:3]) < 3.0:
        reload(sys)
        sys.setdefaultencoding("utf-8")
except: pass

import Core

if Core.checkMandatoryModules():
    from Core.MyObjects import *
    import FileUtils as fu

    fu.initStartupVariables()
    from Core import Universals as uni
    from Core import Settings

    uni.fillMySettings(False, False)
    isActivePyKDE4 = False
    from Core import Dialogs
    from Core import Execute

    defaultLangCode = str(QLocale().name())
    HamsiManagerApp = MApplication(sys.argv)
    MDir.setSearchPaths("Images", MStringList(str(fu.joinPath(fu.themePath, "Images"))))
    StyleFile = open(fu.joinPath(fu.themePath, "Style.qss"))
    HamsiManagerApp.setStyleSheet(StyleFile.read())
    languageFile = MTranslator()
    if fu.isFile(fu.joinPath(fu.HamsiManagerDirectory, "Languages", "HamsiManagerWithQt_" + defaultLangCode + ".qm")):
        languageFile.load(
            str(fu.joinPath(fu.HamsiManagerDirectory, "Languages", "HamsiManagerWithQt_" + defaultLangCode + ".qm")))
    elif fu.isFile(fu.joinPath(fu.HamsiManagerDirectory, "Languages", "HamsiManager_" + defaultLangCode + ".qm")):
        languageFile.load(
            str(fu.joinPath(fu.HamsiManagerDirectory, "Languages", "HamsiManager_" + defaultLangCode + ".qm")))
    HamsiManagerApp.installTranslator(languageFile)
    MTextCodec.setCodecForCStrings(MTextCodec.codecForName("utf-8"))
    MTextCodec.setCodecForTr(MTextCodec.codecForName("utf-8"))
    HamsiManagerApp.setWindowIcon(MIcon("Images:hamsi.png"))
    HamsiManagerApp.setApplicationName("InstallHamsiManager")
    HamsiManagerApp.setApplicationVersion(uni.version)
    HamsiManagerApp.setOrganizationDomain("hamsiapps.com")
    HamsiManagerApp.setOrganizationName("Hamsi Apps")
    from Core import MyConfigure

    class Main(MMainWindow):
        def __init__(self, parent=None):
            MMainWindow.__init__(self, parent)
            setApplication(HamsiManagerApp)
            setMainWindow(self)
            self.isInstallFinished = False
            self.pageNo, self.pageSize = 0, 5
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
                if pageNo != self.pageNo:
                    self.pages[-1].setVisible(False)
                self.hblMain.addWidget(self.pages[-1])
            self.vblMain.addLayout(self.hblMain, 20)
            self.hblButtons = MHBoxLayout()
            self.buttons = [MPushButton(translate("Install", "Back")),
                            MPushButton(translate("Install", "Forward")),
                            MPushButton(translate("Install", "Install"))]
            self.hblButtons.addStretch(5)
            for btnNo, btn in enumerate(self.buttons):
                if btnNo == len(self.buttons) - 1 or btnNo == 0:
                    btn.setVisible(False)
                self.hblButtons.addWidget(btn, 1)
                self.connect(btn, SIGNAL("clicked()"), self.pageChanged)
            self.pbtnCancel = MPushButton(translate("Install", "Cancel"))
            self.pbtnCheckUpdate = MPushButton(translate("Install", "Check Update"))
            self.hblButtons.insertWidget(0, self.pbtnCheckUpdate, 1)
            self.hblButtons.addWidget(self.pbtnCancel, 1)
            self.connect(self.pbtnCancel, SIGNAL("clicked()"), self.close)
            self.connect(self.pbtnCheckUpdate, SIGNAL("clicked()"), self.checkUpdate)
            self.pbtnFinish = MPushButton(translate("Install", "OK"))
            self.hblButtons.addWidget(self.pbtnFinish, 1)
            self.connect(self.pbtnFinish, SIGNAL("clicked()"), self.finish)
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
            if _pageNo == 0:
                if fu.isFile(fu.joinPath(fu.HamsiManagerDirectory, "Languages", "About_" + defaultLangCode)):
                    aboutFileContent = fu.readFromFile(
                        fu.joinPath(fu.HamsiManagerDirectory, "Languages", "About_" + defaultLangCode), "utf-8")
                else:
                    aboutFileContent = fu.readFromFile(
                        fu.joinPath(fu.HamsiManagerDirectory, "Languages", "About_en_GB"), "utf-8")
                lblAbout = MLabel(str(aboutFileContent))
                lblAbout.setWordWrap(True)
                HBox.addWidget(lblAbout)
            elif _pageNo == 1:
                if fu.isFile(fu.joinPath(fu.HamsiManagerDirectory, "Languages", "License_" + defaultLangCode)):
                    licenceFileContent = fu.readFromFile(
                        fu.joinPath(fu.HamsiManagerDirectory, "Languages", "License_" + defaultLangCode), "utf-8")
                else:
                    licenceFileContent = fu.readFromFile(
                        fu.joinPath(fu.HamsiManagerDirectory, "Languages", "License_en_GB"), "utf-8")
                teCopying = MTextEdit()
                teCopying.setPlainText(str(licenceFileContent))
                HBox.addWidget(teCopying)
            elif _pageNo == 2:
                lblPleaseSelect = MLabel(translate("Install", "Please Select A Folder For Installation."))
                installationDirPath = str(Settings.getUniversalSetting("HamsiManagerPath", str(
                    fu.joinPath(fu.getDirName(fu.HamsiManagerDirectory), "Hamsi"))))
                self.leInstallationDirectory = MLineEdit(
                    str(Settings.getUniversalSetting("pathOfInstallationDirectory", str(installationDirPath))))
                self.pbtnSelectInstallationDirectory = MPushButton(translate("Install", "Browse"))
                self.connect(self.pbtnSelectInstallationDirectory, SIGNAL("clicked()"),
                             self.selectInstallationDirectory)
                VBox = MVBoxLayout()
                VBox.addStretch(10)
                VBox.addWidget(lblPleaseSelect)
                HBox1 = MHBoxLayout()
                HBox1.addWidget(self.leInstallationDirectory)
                HBox1.addWidget(self.pbtnSelectInstallationDirectory)
                VBox.addLayout(HBox1)
                VBox.addStretch(10)
                HBox.addLayout(VBox)
            elif _pageNo == 3:
                VBox = MVBoxLayout()
                self.lblActions = MLabel("")
                self.prgbState = MProgressBar()
                VBox.addWidget(self.lblActions)
                VBox.addWidget(self.prgbState)
                HBox.addLayout(VBox)
            elif _pageNo == 4:
                VBox = MVBoxLayout()
                self.lblFinished = MLabel(translate("Install", "Installation Complete."))
                VBox.addStretch(10)
                VBox.addWidget(self.lblFinished)
                self.isCreateDesktopShortcut = None
                self.isCreateExecutableLink = None
                if uni.isRunningAsRoot():
                    self.isCreateExecutableLink = MCheckBox(translate("Install", "Add To The System"))
                    self.isCreateExecutableLink.setCheckState(Mt.Checked)
                    lblExecutableLink = MLabel(translate("Install", "Executable Link Path : "))
                    self.leExecutableLink = MLineEdit(
                        str(Settings.getUniversalSetting("HamsiManagerExecutableLinkPath", "/usr/bin/hamsi")))
                    self.connect(self.isCreateExecutableLink, SIGNAL("stateChanged(int)"),
                                 self.createExecutableLinkChanged)
                    VBox.addWidget(self.isCreateExecutableLink)
                    HBox1 = MHBoxLayout()
                    HBox1.addWidget(lblExecutableLink)
                    HBox1.addWidget(self.leExecutableLink)
                    VBox.addLayout(HBox1)
                else:
                    self.isCreateDesktopShortcut = MCheckBox(translate("Install", "Create Desktop Shortcut."))
                    self.isCreateDesktopShortcut.setCheckState(Mt.Checked)
                    VBox.addWidget(self.isCreateDesktopShortcut)
                VBox.addStretch(10)
                HBox.addLayout(VBox)
            return pnlPage

        def createExecutableLinkChanged(self, _value):
            if _value == 0:
                self.leExecutableLink.setEnabled(False)
            else:
                self.leExecutableLink.setEnabled(True)

        def selectInstallationDirectory(self):
            insDir = Dialogs.getExistingDirectory(translate("Install", "Please select a folder for installation."),
                                                  self.leInstallationDirectory.text())
            if insDir is not None:
                self.leInstallationDirectory.setText(str(insDir))

        def pageChanged(self, _isRunningManual=False):
            try:
                senderObject = None
                if _isRunningManual is False:
                    senderObject = self.sender()
                    if senderObject == self.buttons[1]:
                        self.pageNo += 1
                    elif senderObject == self.buttons[0]:
                        self.pageNo -= 1
                    elif senderObject == self.buttons[2]:
                        self.pageNo += 1
                for pageNo, pnlPage in enumerate(self.pages):
                    if pageNo != self.pageNo:
                        pnlPage.setVisible(False)
                    else:
                        pnlPage.setVisible(True)
                self.buttons[0].setVisible(False)
                self.buttons[1].setVisible(False)
                self.buttons[2].setVisible(False)
                self.pbtnCheckUpdate.setVisible(False)
                self.buttons[1].setText(translate("Install", "Forward"))
                if self.pageNo == 0:
                    self.buttons[1].setVisible(True)
                    self.pbtnCheckUpdate.setVisible(True)
                elif self.pageNo == 1:
                    self.buttons[1].setVisible(True)
                    self.buttons[1].setText(translate("Install", "Accept"))
                    self.pbtnCheckUpdate.setVisible(True)
                elif self.pageNo == 2:
                    self.buttons[0].setVisible(True)
                    self.buttons[2].setVisible(True)
                elif self.pageNo == 3:
                    pass
                elif self.pageNo == 4:
                    self.buttons[0].setVisible(False)
                    self.buttons[1].setVisible(False)
                    self.buttons[2].setVisible(False)
                    self.pbtnCancel.setVisible(False)
                    self.pbtnFinish.setVisible(True)
                if _isRunningManual is False:
                    if senderObject == self.buttons[2]:
                        self.install()
            except:
                from Core import ReportBug

                ReportBug.ReportBug()

        def install(self):
            try:
                MApplication.processEvents()
                self.installationDirectory = str(self.leInstallationDirectory.text())
                if len(self.installationDirectory) > 0:
                    if self.installationDirectory[-1] == fu.sep:
                        self.installationDirectory = self.installationDirectory[:-1]
                    if self.installationDirectory == fu.HamsiManagerDirectory:
                        self.pageNo -= 1
                        self.lblActions.setText("")
                        Dialogs.showError(translate("Install", "The path you selected is not valid."),
                                          translate("Install",
                                                    "The selected path is Hamsi Manager source directory.<br>Please choose a valid installation path."))
                    elif fu.isFile(self.installationDirectory) is False:
                        isMakeInstall = True
                        if fu.isDir(self.installationDirectory) is False:
                            self.lblActions.setText(translate("Install", "Creating Installation Folder..."))
                            fu.makeDirs(self.installationDirectory)
                        elif len(fu.listDir(self.installationDirectory)) > 0:
                            currenctAnswer = Dialogs.askSpecial(
                                translate("Install", "The Installation Path You Selected Is Not Empty."),
                                translate("Install",
                                          "If the path you selected is an \"Hamsi Manager\" installation path, <b>I recommend you to delete the older files.</b><br>Do you want me to clear the installation path/folder for you?<br><b>Note: </b> Your personal settings are <b>never deleted</b>."),
                                translate("Install", "Yes (Recommended)"),
                                translate("Install", "No (Overwrite)"),
                                translate("Install", "Cancel"))
                            if currenctAnswer == translate("Install", "Yes (Recommended)"):
                                self.lblActions.setText(translate("Install", "Clearing Installation Path..."))
                                fu.removeFileOrDir(self.installationDirectory)
                                fu.makeDirs(self.installationDirectory)
                                isMakeInstall = True
                            elif currenctAnswer == translate("Install", "No (Overwrite)"):
                                isMakeInstall = True
                            else:
                                isMakeInstall = False
                        if isMakeInstall:
                            Settings.setUniversalSetting("pathOfInstallationDirectory", self.installationDirectory)
                            directoriesAndFiles = fu.readDirectoryWithSubDirectories(fu.HamsiManagerDirectory)
                            self.prgbState.setRange(0, len(directoriesAndFiles))
                            self.lblActions.setText(translate("Install", "Copying Files And Folders..."))
                            installFileName = Execute.findExecutableBaseName("HamsiManagerInstaller")
                            for fileNo, fileName in enumerate(directoriesAndFiles):
                                MApplication.processEvents()
                                newFileName = self.installationDirectory + fileName.replace(fu.HamsiManagerDirectory,
                                                                                            "")
                                if fu.isDir(fileName):
                                    try: fu.makeDirs(newFileName)
                                    except: pass
                                elif fu.isFile(fileName) and fu.getBaseName(
                                    fileName) != "install.py" and fu.getBaseName(fileName) != installFileName:
                                    try:
                                        fu.copyFileOrDir(fileName, newFileName)
                                    except:
                                        fileContent = fu.readFromBinaryFile(fileName)
                                        fu.writeToBinaryFile(newFileName, fileContent)
                                self.prgbState.setValue(fileNo + 1)
                            self.pageNo += 1
                            MyConfigure.installKDE4Languages()
                        else:
                            self.pageNo -= 1
                    else:
                        self.pageNo -= 1
                        self.lblActions.setText("")
                        Dialogs.showError(translate("Install", "The path you selected is not valid."),
                                          translate("Install",
                                                    "The selected path points to a file not a folder.<br>Please choose a valid installation path."))
                else:
                    self.pageNo -= 1
                    self.lblActions.setText("")
                    Dialogs.showError(translate("Install", "The path you selected is not valid."),
                                      translate("Install",
                                                "The selected path points to a file not a folder.<br>Please choose a valid installation path."))
                self.pageChanged(True)
            except:
                from Core import ReportBug

                ReportBug.ReportBug()

        def closeEvent(self, _event):
            if self.isInstallFinished is False:
                currentAnswer = Dialogs.ask(translate("Install", "Finalizing Installation"),
                                     translate("Install", "Are You Sure You Want To Quit?"))
                if currentAnswer != Dialogs.Yes:
                    _event.ignore()

        def finish(self):
            try:
                if fu.isFile(fu.joinPath(self.installationDirectory, "HamsiManager.desktop")):
                    MyConfigure.reConfigureFile(fu.joinPath(self.installationDirectory, "HamsiManager.desktop"),
                                                self.installationDirectory)
                if self.isCreateDesktopShortcut is not None:
                    if self.isCreateDesktopShortcut.checkState() == Mt.Checked:
                        desktopPath = uni.getUserDesktopPath()
                        if uni.isWindows:
                            MyConfigure.createShortCutFile(fu.joinPath(desktopPath, "Hamsi Manager.lnk"),
                                                           self.installationDirectory)
                        else:
                            fileContent = MyConfigure.getConfiguredDesktopFileContent(self.installationDirectory)
                            fu.writeToFile(fu.joinPath(desktopPath, "HamsiManager.desktop"), fileContent)
                if self.isCreateExecutableLink is not None:
                    executableLink = str(self.leExecutableLink.text())
                    if self.isCreateExecutableLink.checkState() == Mt.Checked:
                        if executableLink.strip() != "":
                            executableLink = fu.checkNewDestination(executableLink)
                            if executableLink:
                                HamsiManagerFileName = Execute.findExecutableBaseName("HamsiManager")
                                fu.createSymLink(fu.joinPath(self.installationDirectory, HamsiManagerFileName),
                                                 executableLink)
                                Settings.setUniversalSetting("HamsiManagerExecutableLinkPath", executableLink)
                        if fu.isDir("/usr/share/applications/"):
                            fileContent = MyConfigure.getConfiguredDesktopFileContent(self.installationDirectory)
                            fu.writeToFile("/usr/share/applications/HamsiManager.desktop", fileContent)
                if uni.isRunningAsRoot() is False:
                    if fu.isDir(fu.joinPath(fu.userDirectoryPath, ".local", "applications")) is False:
                        fu.makeDirs(fu.joinPath(fu.userDirectoryPath, ".local", "applications"))
                    fileContent = MyConfigure.getConfiguredDesktopFileContent(self.installationDirectory)
                    fu.writeToFile(fu.joinPath(fu.userDirectoryPath, ".local", "applications", "HamsiManager.desktop"),
                                   fileContent)
                self.isInstallFinished = True
                self.close()
            except:
                from Core import ReportBug

                ReportBug.ReportBug()

    if uni.isRunningAsRoot() is False and uni.isRunableAsRoot():
        answer = Dialogs.askSpecial(translate("Install", "Are You Want To Run As Root?"), translate("Install",
                                                                                                    "Hamsi Manager Installer is running with user privileges.<br>Do you want to run Hamsi Manager installer with root rights?<br><b>Note: </b>The other users on your system has to inherit these permissions and install the program to a location other than their /home directories."),
                                    translate("Install", "Yes"), translate("Install", "No (Continue as is)"), None)
        if answer == translate("Install", "Yes"):
            NewApp = Execute.executeAsRootWithThread([], "HamsiManagerInstaller")
            sys.exit()
    try:
        MainWidget = Main()
        MainWidget.setWindowTitle(translate("Install", "Hamsi Manager Installer") + " " + uni.version)
        MainWidget.setGeometry(300, 300, 650, 350)
        MainWidget.show()
        uni.isStartingSuccessfully = True
    except:
        from Core import ReportBug

        ReportBug.ReportBug()
    sys.exit(HamsiManagerApp.exec_())
else:
    sys.exit()
    
    
        
    
