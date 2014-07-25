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
from Core.MyObjects import *
import FileUtils as fu
from Core import Universals as uni
from Core import Settings
from Core import FileManager
import Bars
from Bars import TableToolsBar, ToolsBar, StatusBar, MenuBar
from Core import ReportBug
from Core import Records
from Core import Dialogs
from Options import OptionsForm
from Details import MusicDetails, TextDetails, CoverDetails


class MyMainWindow(MMainWindow):
    def __init__(self):
        MMainWindow.__init__(self, None)
        uni.printForDevelopers("Started __init__")
        self.setObjectName("RealMainWindow")
        setMainWindow(self)
        self.isLockedMainForm = False
        self.Menu = None
        self.Table = None
        self.CentralWidget = MWidget()
        self.createMainLayout()
        uni.printForDevelopers("Before Bars.Bars")
        self.Bars = Bars.Bars()
        uni.printForDevelopers("Before Bars.StatusBar")
        self.StatusBar = StatusBar.StatusBar(self)
        uni.printForDevelopers("Before Bars.MenuBar")
        self.Menu = MenuBar.MenuBar(self)
        uni.printForDevelopers("Before Bars.ToolsBar")
        self.ToolsBar = ToolsBar.ToolsBar(self)
        uni.printForDevelopers("Before Bars.TableToolsBar")
        self.TableToolsBar = TableToolsBar.TableToolsBar(self)
        uni.printForDevelopers("Before Bars.refreshBars")
        self.Bars.refreshBars()
        uni.printForDevelopers("Before FileManager.FileManager")
        self.FileManager = FileManager.FileManager(self)
        uni.printForDevelopers("After FileManager.FileManager")
        self.setMainLayout()
        self.setCentralWidget(self.CentralWidget)
        self.setMenuBar(self.Menu)
        self.setStatusBar(self.StatusBar)
        uni.printForDevelopers("Before Menu.refreshForTableType")
        self.Menu.refreshForTableType()
        uni.printForDevelopers("Before Bars.getAllBarsStyleFromMySettings")
        self.Bars.getAllBarsStyleFromMySettings()
        self.setCorner(Mt.TopLeftCorner, Mt.LeftDockWidgetArea)
        self.setCorner(Mt.BottomLeftCorner, Mt.LeftDockWidgetArea)
        uni.printForDevelopers("End of __init__")

    def createMainLayout(self):
        self.MainLayout = MVBoxLayout()

    def setMainLayout(self):
        self.CentralWidget.setLayout(self.MainLayout)

    def resetCentralWidget(self):
        clearAllChildren(self.CentralWidget)
        self.MainLayout = self.CentralWidget.layout()
        if self.MainLayout is None:
            self.createMainLayout()
            self.setMainLayout()

    def lockForm(self):
        self.CentralWidget.setEnabled(False)
        for wid in self.findChildren(MDockWidget):
            wid.setEnabled(False)
        for wid in self.findChildren(MToolBar):
            wid.setEnabled(False)
        for wid in self.findChildren(MMenuBar):
            wid.setEnabled(False)
        self.isLockedMainForm = True

    def unlockForm(self):
        self.CentralWidget.setEnabled(True)
        for wid in self.findChildren(MDockWidget):
            wid.setEnabled(True)
        for wid in self.findChildren(MToolBar):
            wid.setEnabled(True)
        for wid in self.findChildren(MMenuBar):
            wid.setEnabled(True)
        self.isLockedMainForm = False

    def doAfterRunProcessesStep1(self):
        if str(fu.defaultFileSystemEncoding) != str(uni.MySettings["fileSystemEncoding"]):
            answer = Dialogs.ask(
                translate("HamsiManager", "Your System's \"File System Encoding\" Type Different"),
                translate("HamsiManager",
                          "Your system's \"File System Encoding\" type different from the settings you select. Are you sure you want to continue?If you are not sure press the \"No\"."),
                False, "Your System's \"File System Encoding\" Type Different")
            if answer == Dialogs.No:
                OptionsForm.OptionsForm(self, _focusTo="fileSystemEncoding")
        if uni.getBoolValue("isMakeAutoDesign"):
            self.TableToolsBar.setVisible(False)
            self.ToolsBar.setVisible(False)
            if isActivePyKDE4:
                self.Browser.setVisible(False)
                self.TreeBrowser.setVisible(False)
                self.FileManager.urlNavigator.setMinimumWidth(150)
                self.FileManager.tbarBrowserToolsFull.setVisible(False)
                self.tabifyDockWidget(self.Browser, self.Places)
                self.tabifyDockWidget(self.Browser, self.TreeBrowser)
                self.tabifyDockWidget(self.Browser, self.DirOperator)
            geometries = uni.getListValue("MainWindowGeometries")
            self.setGeometry(int(geometries[0]), int(geometries[1]), 900, 600)
            uni.setMySetting("isMakeAutoDesign", "False")
        if uni.isShowVerifySettings and (uni.changedDefaultValuesKeys != [] or uni.newSettingsKeys != []):
            answer = Dialogs.ask(translate("HamsiManager", "Added New Options And New Features"),
                                 translate("HamsiManager",
                                           "New options and new features added to Hamsi Manager. Are you want to change or verify new options?"),
                                 False, "Added New Options And New Features")
            if answer == Dialogs.Yes:
                newOrChangedKeys = uni.newSettingsKeys + uni.changedDefaultValuesKeys
                OptionsForm.OptionsForm(self, "Normal", None, newOrChangedKeys)
        elif uni.getBoolValue("isShowReconfigureWizard") and uni.isBuilt() is False:
            from Tools import Configurator

            Configurator.Configurator()
            uni.setMySetting("isShowReconfigureWizard", "False")

    def doAfterRunProcessesStep2(self):
        for command in uni.runAfter:
            action = command["action"]
            action(*command["args"], **command["kwargs"])
            uni.printForDevelopers(str(command))

    def closeEvent(self, _event):
        try:
            if uni.isRaisedAnError is False:
                if uni.isContinueThreadAction():
                    uni.cancelThreadAction()
                    _event.ignore()
            uni.isStartedCloseProcess = True
            uni.printForDevelopers("Started closeEvent")
            MApplication.setQuitOnLastWindowClosed(True)
            try:
                self.PlayerBar.MusicPlayer.stop()
            except:
                pass
            MusicDetails.MusicDetails.closeAllMusicDialogs()
            TextDetails.TextDetails.closeAllTextDialogs()
            CoverDetails.CoverDetails.closeAllCoverDialogs()
            uni.printForDevelopers("Closed Dialogs")
            if uni.isRaisedAnError is False:
                if self.Table.checkUnSavedValues() is False:
                    uni.isStartedCloseProcess = False
                    uni.printForDevelopers("Close ignored")
                    _event.ignore()
            uni.printForDevelopers("Before self.doBeforeCloseProcesses")
            if self.doBeforeCloseProcesses() is False:
                _event.ignore()
                return None
            uni.printForDevelopers("After self.doBeforeCloseProcesses")
            if isActivePyKDE4:
                uni.printForDevelopers("Before Save KDE Configs")
                kconf = MGlobal.config()
                kconfGroup = MConfigGroup(kconf, "DirectoryOperator")
                self.FileManager.dirOperator.writeConfig(kconfGroup)
                self.FileManager.actCollection.writeSettings(kconfGroup)
                uni.printForDevelopers("After Save KDE Configs")
            uni.printForDevelopers("Before Save Configs")
            uni.setMySetting(self.Table.hiddenTableColumnsSettingKey,
                             self.Table.hiddenTableColumns)
            self.Bars.setAllBarsStyleToMySettings()
            Records.setRecordType(1)
            fu.writeToBinaryFile(
                fu.joinPath(fu.pathOfSettingsDirectory, "LastState"), self.saveState())
            Records.restoreRecordType()
            geometry = [self.geometry().x(), self.geometry().y(), self.geometry().width(),
                        self.geometry().height()]
            uni.setMySetting("MainWindowGeometries", geometry)
            uni.setMySetting("lastDirectory", self.FileManager.currentDirectory)
            uni.setMySetting("isMainWindowMaximized", self.isMaximized())
            uni.setMySetting("isShowAdvancedSelections", self.SpecialTools.isShowAdvancedSelections)
            uni.setMySetting("tableType", uni.tableType)
            uni.setMySetting("activeTabNoOfSpecialTools", self.SpecialTools.tabwTabs.currentIndex())
            uni.saveSettings()
            Settings.saveUniversalSettings()
            if uni.isActiveAmarok and uni.getBoolValue("amarokIsUseHost") is False:
                import Amarok

                uni.printForDevelopers("Before Amarok.stopEmbeddedDB")
                Amarok.stopEmbeddedDB()
                uni.printForDevelopers("After Amarok.stopEmbeddedDB")
            uni.printForDevelopers("After Save Configs")
            uni.printForDevelopers("Before self.doAfterCloseProcesses")
            self.doAfterCloseProcesses()
            uni.printForDevelopers("After self.doAfterCloseProcesses")
        except:
            if ReportBug.isClose is False:
                ReportBug.ReportBug()
                _event.ignore()

    def doBeforeCloseProcesses(self):
        from Core import UpdateControl

        if uni.getBoolValue("isDontDeleteFileAndDirectory"):
            fu.checkSizeOfDeletedFiles()
        if UpdateControl.UpdateControl.isMakeUpdateControl():
            UpdateControl.UpdateControl(self, _isCloseParent=True)
            return False
        return True

    def doAfterCloseProcesses(self):
        Records.saveAllRecords()
        Records.checkSize()


