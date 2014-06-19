# # This file is part of HamsiManager.
# #
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


from Core.MyObjects import *
from Core import Universals as uni
from Core import Dialogs
from Core import Settings
from Core import MyConfigure
from Core import Execute
import FileUtils as fu
from Core import ReportBug

MyDialog, MyDialogType, MyParent = getMyDialog()


class Configurator(MyDialog):
    def __init__(self, _page=None):
        MyDialog.__init__(self, MyParent)
        if MyDialogType == "MDialog":
            if isActivePyKDE4:
                self.setButtons(MyDialog.NoDefault)
        elif MyDialogType == "MMainWindow":
            self.setObjectName("Cleaner")
            setMainWindow(self)
        activePageNo = 0
        if _page == "configurePage":
            activePageNo = 2
        elif _page == "pluginPage":
            activePageNo = 3
        self.isInstallFinised = False
        self.pageNo, self.pageSize = activePageNo, 4
        self.pnlMain = MWidget(self)
        self.vblMain = MVBoxLayout(self.pnlMain)
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
        self.buttons = [MPushButton(translate("Reconfigure", "Back")),
                        MPushButton(translate("Reconfigure", "Forward")),
                        MPushButton(translate("Reconfigure", "Configure"))]
        self.hblButtons.addStretch(5)
        for btnNo, btn in enumerate(self.buttons):
            if btnNo == len(self.buttons) - 1 or btnNo == 0:
                btn.setVisible(False)
            self.hblButtons.addWidget(btn, 1)
            self.connect(btn, SIGNAL("clicked()"), self.pageChanged)
        self.pbtnCancel = MPushButton(translate("Reconfigure", "Cancel"))
        self.pbtnFinish = MPushButton(translate("Reconfigure", "Finish"))
        self.pbtnFinish.setVisible(False)
        self.hblButtons.addWidget(self.pbtnCancel, 1)
        self.hblButtons.addWidget(self.pbtnFinish, 1)
        self.connect(self.pbtnCancel, SIGNAL("clicked()"), self.close)
        self.connect(self.pbtnFinish, SIGNAL("clicked()"), self.close)
        self.vblMain.addLayout(self.hblButtons)
        self.pageChanged(True)
        if MyDialogType == "MDialog":
            if isActivePyKDE4:
                self.setMainWidget(self.pnlMain)
            else:
                self.setLayout(self.vblMain)
        elif MyDialogType == "MMainWindow":
            self.setCentralWidget(self.pnlMain)
            moveToCenter(self)
        self.setWindowTitle(translate("Reconfigure", "Hamsi Manager Configurator") + " " + uni.version)
        self.setWindowIcon(MIcon("Images:hamsi.png"))
        self.setMinimumWidth(650)
        self.setMinimumHeight(350)
        self.show()

    def closeEvent(self, _event):
        if self.isInstallFinised == False:
            answer = Dialogs.ask(translate("Reconfigure", "Finalizing Configuration"),
                                 translate("Reconfigure", "Are You Sure You Want To Quit?"))
            if answer != Dialogs.Yes:
                _event.ignore()
        MApplication.setQuitOnLastWindowClosed(True)

    def createPage(self, _pageNo):
        pnlPage = MWidget()
        HBox = MHBoxLayout()
        pnlPage.setLayout(HBox)
        defaultLangCode = uni.getDefaultLanguageCode()
        if _pageNo == 0:
            if fu.isFile(fu.joinPath(fu.HamsiManagerDirectory, "Languages", "About_" + defaultLangCode)):
                aboutFileContent = fu.readFromFile(
                    fu.joinPath(fu.HamsiManagerDirectory, "Languages", "About_" + defaultLangCode), "utf-8")
            else:
                aboutFileContent = fu.readFromFile(fu.joinPath(fu.HamsiManagerDirectory, "Languages", "About_en_GB"),
                                                   "utf-8")
            lblAbout = MLabel(str(aboutFileContent))
            lblAbout.setWordWrap(True)
            HBox.addWidget(lblAbout)
        elif _pageNo == 1:
            if fu.isFile(fu.joinPath(fu.HamsiManagerDirectory, "Languages", "License_" + defaultLangCode)):
                lisenceFileContent = fu.readFromFile(
                    fu.joinPath(fu.HamsiManagerDirectory, "Languages", "License_" + defaultLangCode), "utf-8")
            else:
                lisenceFileContent = fu.readFromFile(
                    fu.joinPath(fu.HamsiManagerDirectory, "Languages", "License_en_GB"), "utf-8")
            teCopying = MTextEdit()
            teCopying.setPlainText(str(lisenceFileContent))
            HBox.addWidget(teCopying)
        elif _pageNo == 2:
            VBox = MVBoxLayout()
            VBox.addStretch(10)
            self.isCreateDesktopShortcut = None
            self.isCreateExecutableLink = None
            self.wAvailableModules = MWidget(self)
            VBox.addWidget(self.wAvailableModules)
            self.vblAvailableModules = MVBoxLayout()
            self.checkAvailableModules()
            VBox.addStretch(1)
            if uni.isRunningAsRoot():
                self.isCreateExecutableLink = MCheckBox(translate("Reconfigure", "Add To The System"))
                self.isCreateExecutableLink.setCheckState(Mt.Checked)
                lblExecutableLink = MLabel(translate("Reconfigure", "Executable Link Path : "))
                self.leExecutableLink = MLineEdit(
                    str(Settings.getUniversalSetting("HamsiManagerExecutableLinkPath", "/usr/bin/hamsi")))
                self.connect(self.isCreateExecutableLink, SIGNAL("stateChanged(int)"), self.createExecutableLinkChanged)
                VBox.addWidget(self.isCreateExecutableLink)
                HBox1 = MHBoxLayout()
                HBox1.addWidget(lblExecutableLink)
                HBox1.addWidget(self.leExecutableLink, 10)
                VBox.addLayout(HBox1)
            else:
                self.isCreateDesktopShortcut = MCheckBox(translate("Reconfigure", "Create Desktop Shortcut."))
                self.isCreateDesktopShortcut.setCheckState(Mt.Checked)
                VBox.addWidget(self.isCreateDesktopShortcut)
            VBox.addStretch(10)
            HBox.addLayout(VBox)
        elif _pageNo == 3:
            import MyPlugins

            VBox = MVBoxLayout()
            VBox.addStretch(10)
            wPlugins = MyPlugins.MyPluginsForSystem(self)
            HBox.addWidget(wPlugins)
            VBox.addStretch(10)
            HBox.addLayout(VBox)
        return pnlPage

    def createExecutableLinkChanged(self, _value):
        if _value == 0:
            self.leExecutableLink.setEnabled(False)
        else:
            self.leExecutableLink.setEnabled(True)

    def checkAvailableModules(self):
        try:
            eyeD3IsAvailable = False
            mysqlIsAvailable = False
            musicbrainzIsAvailable = False
            scintillaIsAvailable = False
            pywin32IsAvailable = False
            try:
                import eyeD3

                eyeD3IsAvailable = True
            except: pass
            try:
                import _mysql as mdb

                mysqlIsAvailable = True
            except: pass
            try:
                from musicbrainz2 import webservice, model, utils
                from musicbrainz2.webservice import Query, ArtistFilter, WebServiceError, ReleaseFilter, TrackFilter

                musicbrainzIsAvailable = True
            except: pass
            try:
                from PyQt4.Qsci import QsciScintilla

                scintillaIsAvailable = True
            except: pass
            if uni.isWindows:
                try:
                    import win32api, win32con, win32com

                    pywin32IsAvailable = True
                except: pass

            clearAllChildren(self.wAvailableModules)

            if eyeD3IsAvailable == False:
                lblEyeD3 = MLabel(translate("Reconfigure",
                                            "<a href='http://eyed3.nicfit.net/'>'eyeD3'</a> (python-eyed3) named module has NOT installed in your system."))
                lblEyeD3.setOpenExternalLinks(True)
                self.vblAvailableModules.addWidget(lblEyeD3)
            if mysqlIsAvailable == False:
                lblMysql = MLabel(translate("Reconfigure",
                                            "<a href='https://sourceforge.net/projects/mysql-python/'>'MySQL'</a> (python-mysql) named module has NOT installed on your system."))
                lblMysql.setOpenExternalLinks(True)
                self.vblAvailableModules.addWidget(lblMysql)
            if musicbrainzIsAvailable == False:
                lblMusicbrainz = MLabel(translate("Reconfigure",
                                                  "<a href='http://musicbrainz.org/doc/python-musicbrainz2'>'Music Brainz'</a> (python-musicbrainz2) named module has NOT installed on your system."))
                lblMusicbrainz.setOpenExternalLinks(True)
                self.vblAvailableModules.addWidget(lblMusicbrainz)
            if scintillaIsAvailable == False:
                lblScintilla = MLabel(translate("Reconfigure",
                                                "<a href='http://www.riverbankcomputing.com/software/qscintilla/download'>'QScintilla'</a> (python-qt4-qscintilla) named module has NOT installed on your system."))
                lblScintilla.setOpenExternalLinks(True)
                self.vblAvailableModules.addWidget(lblScintilla)
            if uni.isWindows:
                if pywin32IsAvailable == False:
                    lblPywin32 = MLabel(translate("Reconfigure",
                                                  "<a href='https://sourceforge.net/projects/pywin32/'>'Python for Windows Extensions'</a> (pywin32) named module has NOT installed on your system."))
                    lblPywin32.setOpenExternalLinks(True)
                    self.vblAvailableModules.addWidget(lblPywin32)

            if eyeD3IsAvailable == False or mysqlIsAvailable == False or musicbrainzIsAvailable == False or scintillaIsAvailable == False or (
                    uni.isWindows and (mysqlIsAvailable == False)):
                lblAlert = MLabel(translate("Reconfigure",
                                            "<b>You have to install above modules to use some features.<br>If you don't want to use all features, you can continue without these modules.</b>"))
                self.vblAvailableModules.addWidget(lblAlert)
                btnCheckAvailableModules = MPushButton(translate("Reconfigure", "Check Again"))
                self.vblAvailableModules.addWidget(btnCheckAvailableModules)
                self.connect(btnCheckAvailableModules, SIGNAL("clicked()"), self.checkAvailableModules)

            self.wAvailableModules.setLayout(self.vblAvailableModules)
        except:
            ReportBug.ReportBug()

    def pageChanged(self, _isRunningManual=False):
        try:
            if _isRunningManual == False:
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
            self.buttons[1].setText(translate("Reconfigure", "Forward"))
            if self.pageNo == 0:
                self.buttons[1].setVisible(True)
            elif self.pageNo == 1:
                self.buttons[1].setVisible(True)
                self.buttons[1].setText(translate("Reconfigure", "Accept"))
            elif self.pageNo == 2:
                self.buttons[0].setVisible(False)
                self.buttons[1].setVisible(False)
                self.buttons[2].setVisible(True)
                self.pbtnCancel.setVisible(True)
            elif self.pageNo == 3:
                self.buttons[0].setVisible(False)
                self.buttons[1].setVisible(False)
                self.buttons[2].setVisible(False)
                self.pbtnCancel.setVisible(False)
                self.pbtnFinish.setVisible(True)
                self.isInstallFinised = True
            if _isRunningManual == False:
                if senderObject == self.buttons[2]:
                    self.reConfigure()
        except:
            ReportBug.ReportBug()

    def reConfigure(self):
        try:
            oldPathOfExecutableHamsi = Settings.getUniversalSetting("HamsiManagerExecutableLinkPath", "/usr/bin/hamsi")
            if fu.isFile(fu.joinPath(fu.HamsiManagerDirectory, "HamsiManager.desktop")):
                if fu.isWritableFileOrDir(fu.joinPath(fu.HamsiManagerDirectory, "HamsiManager.desktop")):
                    MyConfigure.reConfigureFile(fu.joinPath(fu.HamsiManagerDirectory, "HamsiManager.desktop"))
            if self.isCreateDesktopShortcut != None:
                if self.isCreateDesktopShortcut.checkState() == Mt.Checked:
                    desktopPath = uni.getUserDesktopPath()
                    if uni.isWindows:
                        MyConfigure.createShortCutFile(fu.joinPath(desktopPath, "Hamsi Manager.lnk"))
                    else:
                        fileContent = MyConfigure.getConfiguredDesktopFileContent()
                        fu.writeToFile(fu.joinPath(desktopPath, "HamsiManager.desktop"), fileContent)
            if uni.isRunningAsRoot():
                executableLink = str(self.leExecutableLink.text())
                if self.isCreateExecutableLink != None:
                    if self.isCreateExecutableLink.checkState() == Mt.Checked:
                        if executableLink.strip() != "":
                            HamsiManagerFileName = Execute.findExecutableBaseName("HamsiManager")
                            if fu.isFile(executableLink):
                                fu.removeFileOrDir(executableLink)
                            fu.createSymLink(fu.joinPath(fu.HamsiManagerDirectory, HamsiManagerFileName),
                                             executableLink)
                            Settings.setUniversalSetting("HamsiManagerExecutableLinkPath", executableLink)
                            if oldPathOfExecutableHamsi != executableLink:
                                if fu.isFile(oldPathOfExecutableHamsi):
                                    answer = Dialogs.ask(translate("Reconfigure", "Other Hamsi Manager Was Detected"),
                                                         str(translate("Reconfigure",
                                                                       "Other Hamsi Manager executable file was detected. Are you want to delete old executable file? You can delete this old executable file : \"%s\"")) % (
                                                             oldPathOfExecutableHamsi))
                                    if answer != Dialogs.Yes:
                                        fu.removeFile(oldPathOfExecutableHamsi)
                        if fu.isDir("/usr/share/applications/"):
                            fileContent = MyConfigure.getConfiguredDesktopFileContent()
                            fu.writeToFile("/usr/share/applications/HamsiManager.desktop", fileContent)
            if uni.isRunningAsRoot() == False:
                if fu.isDir(fu.joinPath(fu.userDirectoryPath, ".local", "applications")) == False:
                    fu.makeDirs(fu.joinPath(fu.userDirectoryPath, ".local", "applications"))
                fileContent = MyConfigure.getConfiguredDesktopFileContent()
                fu.writeToFile(fu.joinPath(fu.userDirectoryPath, ".local", "applications", "HamsiManager.desktop"),
                               fileContent)
            MyConfigure.installKDE4Languages()
            self.isInstallFinised = True
        except:
            ReportBug.ReportBug()
    
    
                
