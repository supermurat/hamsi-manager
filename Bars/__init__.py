# This file is part of HamsiManager.
#
# Copyright (c) 2010 - 2014 Murat Demir <mopened@gmail.com>
#
# Hamsi Manager is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Hamsi Manager is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with HamsiManager; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA


import Tables
import SpecialTools
from Core import Universals as uni
from Core import Dialogs
from Core.MyObjects import *
from Core import ReportBug
from Core import Organizer
from Core import Execute
from Core import Records
from Core import Settings
import FileUtils as fu
from Bars import PlayerBar


class Bars():
    def __init__(self):
        pass

    def click(self, _action):
        try:
            actionName = _action.objectName()
            if actionName == translate("MenuBar", "Open State"):
                f = Dialogs.getOpenFileName(translate("MenuBar", "Open State Of Hamsi Manager"),
                                            fu.userDirectoryPath,
                                            translate("MenuBar", "Application Runner") + " (*.desktop)")
                if f is not None:
                    Settings.openStateOfSettings(f)
            elif actionName == translate("MenuBar", "Save State"):
                f = Dialogs.getSaveFileName(translate("MenuBar", "Save State Of Hamsi Manager"),
                                            fu.joinPath(fu.userDirectoryPath, "HamsiManager.desktop"),
                                            translate("MenuBar", "Application Runner") + " (*.desktop)")
                if f is not None:
                    Settings.saveStateOfSettings(f)
                    Dialogs.show(translate("MenuBar", "Current State Saved"),
                                 translate("MenuBar",
                                           "Current state saved with preferences.<br>You can continue where you left off."))
            elif actionName == translate("MenuBar", "With This Profile (My Settings)"):
                if Execute.executeAsRootWithThread(["--sDirectoryPath", fu.pathOfSettingsDirectory], "HamsiManager"):
                    getMainWindow().close()
                else:
                    Dialogs.showError(translate("MenuBar", "Can Not Run As Root"),
                                      translate("MenuBar", "Hamsi Manager can not run as root."))
            elif actionName == translate("MenuBar", "With Root Profile (Own Settings)"):
                if Execute.executeAsRootWithThread([], "HamsiManager"):
                    getMainWindow().close()
                else:
                    Dialogs.showError(translate("MenuBar", "Can Not Run As Root"),
                                      translate("MenuBar", "Hamsi Manager can not run as root."))
            elif actionName == translate("MenuBar", "Quit"):
                getMainWindow().close()
            elif actionName == translate("MenuBar", "HTML Format"):
                if _action.parent().objectName() == translate("MenuBar", "Export To File"):
                    getMainWindow().Table.exportValues("file", "html", "title")
                elif _action.parent().objectName() == translate("MenuBar", "Show In New Window"):
                    getMainWindow().Table.exportValues("dialog", "html", "title")
                elif _action.parent().objectName() == translate("MenuBar", "Copy To Clipboard"):
                    getMainWindow().Table.exportValues("clipboard", "html", "title")
            elif actionName == translate("MenuBar", "Text Format"):
                if _action.parent().objectName() == translate("MenuBar", "Export To File"):
                    getMainWindow().Table.exportValues("file", "plainText", "title")
                elif _action.parent().objectName() == translate("MenuBar", "Show In New Window"):
                    getMainWindow().Table.exportValues("dialog", "plainText", "title")
                elif _action.parent().objectName() == translate("MenuBar", "Copy To Clipboard"):
                    getMainWindow().Table.exportValues("clipboard", "plainText", "title")
            elif actionName == translate("MenuBar", "HTML Format (File Tree)"):
                if _action.parent().objectName() == translate("MenuBar", "Export To File"):
                    fu.getFileTree((getMainWindow().FileManager.currentDirectory), 0, "file", "html", "fileTree",
                                   "title")
                elif _action.parent().objectName() == translate("MenuBar", "Show In New Window"):
                    fu.getFileTree((getMainWindow().FileManager.currentDirectory), 0, "dialog", "html", "fileTree",
                                   "title")
                elif _action.parent().objectName() == translate("MenuBar", "Copy To Clipboard"):
                    fu.getFileTree((getMainWindow().FileManager.currentDirectory), 0, "clipboard", "html", "fileTree",
                                   "title")
            elif actionName == translate("MenuBar", "Text Format (File Tree)"):
                if _action.parent().objectName() == translate("MenuBar", "Export To File"):
                    fu.getFileTree((getMainWindow().FileManager.currentDirectory), 0, "file", "plainText", "fileTree",
                                   "title")
                elif _action.parent().objectName() == translate("MenuBar", "Show In New Window"):
                    fu.getFileTree((getMainWindow().FileManager.currentDirectory), 0, "dialog", "plainText", "fileTree",
                                   "title")
                elif _action.parent().objectName() == translate("MenuBar", "Copy To Clipboard"):
                    fu.getFileTree((getMainWindow().FileManager.currentDirectory), 0, "clipboard", "plainText",
                                   "fileTree", "title")
            elif actionName == translate("MenuBar", "About QT"):
                if isActivePyKDE4:
                    QMessageBox.aboutQt(getMainWindow(), translate("MenuBar", "About QT"))
                else:
                    MMessageBox.aboutQt(getMainWindow(), translate("MenuBar", "About QT"))
            elif actionName == translate("MenuBar", "Options"):
                from Options import OptionsForm

                OptionsForm.OptionsForm(getMainWindow())
            elif actionName == translate("MenuBar", "My Plugins"):
                import MyPlugins

                MyPlugins.MyPlugins()
            elif actionName == translate("MenuBar", "Reconfigure"):
                from Tools import Configurator

                Configurator.Configurator("configurePage")
            elif actionName == translate("MenuBar", "My Plugins (System)"):
                Execute.execute(["--qm", "--plugins", "--runAsRoot"], "HamsiManager")
            elif actionName == translate("MenuBar", "Reconfigure (System)"):
                Execute.execute(["--qm", "--configurator", "--runAsRoot"], "HamsiManager")
            elif actionName == translate("MenuBar", "Update"):
                from Core import UpdateControl

                UpdateControl.UpdateControl(getMainWindow())
            elif actionName == translate("MenuBar", "Report Bug"):
                ReportBug.ReportBug(True)
            elif actionName == translate("MenuBar", "Suggest Idea"):
                from Core import SuggestIdea

                SuggestIdea.SuggestIdea()
            elif actionName == translate("MenuBar", "About Hamsi Manager"):
                if isActivePyKDE4 is False:
                    MMessageBox.about(getMainWindow(), translate("MenuBar", "About Hamsi Manager"),
                                      uni.aboutOfHamsiManager)
            elif actionName == translate("ToolsBar", "Check Icon"):
                getMainWindow().setEnabled(False)
                fu.checkIcon(getMainWindow().FileManager.getCurrentDirectoryPath())
                Dialogs.show(translate("ToolsBar", "Directory Icon Checked"),
                             translate("ToolsBar",
                                       "Current directory icon checked.<br>The default action based on the data is executed."))
                getMainWindow().setEnabled(True)
            elif actionName == translate("ToolsBar", "Clear Empty Directories"):
                if getMainWindow().Table.checkUnSavedValues() is False:
                    _action.setChecked(False)
                    return False
                answer = Dialogs.ask(translate("ToolsBar", "Empty Directories Will Be Removed"),
                                     str(translate("ToolsBar",
                                                   "Are you sure you want to remove empty directories based on the criteria you set in \"%s\"?")) % Organizer.getLink(
                                         getMainWindow().FileManager.getCurrentDirectoryPath()))
                if answer == Dialogs.Yes:
                    getMainWindow().setEnabled(False)
                    currentDirPath = getMainWindow().FileManager.getCurrentDirectoryPath()
                    if fu.isWritableFileOrDir(currentDirPath):
                        fu.checkEmptyDirectories(currentDirPath, True, True, True, True)
                        Dialogs.show(translate("ToolsBar", "Directory Cleaned"),
                                     translate("ToolsBar",
                                               "The current directory is cleaned based on the criteria you set."))
                    getMainWindow().setEnabled(True)
                    getMainWindow().FileManager.makeRefresh()
            elif actionName == translate("ToolsBar", "Pack"):
                from Tools import Packager

                Packager.Packager(getMainWindow().FileManager.getCurrentDirectoryPath())
            elif actionName == translate("ToolsBar", "Hash"):
                from Tools import Hasher

                Hasher.Hasher(getMainWindow().FileManager.getCurrentDirectoryPath())
            elif actionName == translate("ToolsBar", "Clear"):
                from Tools import Cleaner

                Cleaner.Cleaner(getMainWindow().FileManager.getCurrentDirectoryPath())
            elif actionName == translate("ToolsBar", "Text Corrector"):
                from Tools import TextCorrector

                TextCorrector.TextCorrector(getMainWindow().FileManager.getCurrentDirectoryPath())
            elif actionName == translate("ToolsBar", "File Tree"):
                from Tools import FileTreeBuilder

                FileTreeBuilder.FileTreeBuilder(getMainWindow().FileManager.getCurrentDirectoryPath())
            elif actionName == translate("ToolsBar", "Search"):
                from Tools import Searcher

                Searcher.Searcher([getMainWindow().FileManager.getCurrentDirectoryPath()])
            elif actionName == translate("ToolsBar", "Script Manager"):
                from Tools import ScriptManager

                if ScriptManager.ScriptManager.checkScriptManager():
                    ScriptManager.ScriptManager(getMainWindow())
            elif actionName == translate("ToolsBar", "Show Last Actions"):
                from Core import RecordsForm

                RecordsForm.RecordsForm(getMainWindow())
            elif actionName == translate("ToolsBar", "Remove Sub Files"):
                answer = Dialogs.ask(translate("ToolsBar", "All Files Will Be Removed"),
                                     str(translate("ToolsBar",
                                                   "Are you sure you want to remove only all files in \"%s\"?<br>Note:Do not will remove directory and subfolders.")) % Organizer.getLink(
                                         getMainWindow().FileManager.getCurrentDirectoryPath()))
                if answer == Dialogs.Yes:
                    getMainWindow().setEnabled(False)
                    fu.removeOnlySubFiles(getMainWindow().FileManager.getCurrentDirectoryPath())
                    getMainWindow().setEnabled(True)
                    Dialogs.show(translate("ToolsBar", "Removed Only All Files"),
                                 str(translate("ToolsBar",
                                               "Removed only all files in \"%s\".<br>Note:Do not removed directory and subfolders.")) % Organizer.getLink(
                                     getMainWindow().FileManager.getCurrentDirectoryPath()))
            elif actionName == translate("ToolsBar", "Amarok Embedded Database Configurator"):
                import Amarok

                if Amarok.checkAmarok():
                    Amarok.openEmbeddedDBConfigurator()
            elif _action.parent().objectName() == translate("ToolsBar", "Table Types"):
                self.changeTableType(_action)
            elif _action.parent().objectName() == translate("ToolsBar", "File Renamer Types"):
                self.changeReNamerType(_action)
            elif _action.parent().objectName() == translate("MenuBar", "Scripts"):
                from Core import Scripts

                Scripts.runScriptFile(fu.joinPath(Scripts.pathOfScripsDirectory, actionName))
            Records.saveAllRecords()
        except:
            ReportBug.ReportBug()

    def refreshBars(self):
        getMainWindow().Table = Tables.Tables(getMainWindow()).Table
        getMainWindow().SpecialTools = SpecialTools.SpecialTools(getMainWindow())
        if uni.tableType in ["2", "6", "8", "9"]:
            getMainWindow().PlayerBar = PlayerBar.PlayerBar(getMainWindow())
            getMainWindow().addToolBar(Mt.TopToolBarArea, getMainWindow().PlayerBar)
        getMainWindow().Menu.refreshForTableType()

    def changeTableTypeByType(self, _tableType):
        try:
            if uni.tableType != _tableType:
                if getMainWindow().Table.checkUnSavedValues() is False:
                    return False
                uni.setMySetting(getMainWindow().Table.hiddenTableColumnsSettingKey,
                                 getMainWindow().Table.hiddenTableColumns)
                if uni.tableType in ["2", "6", "8", "9"]:
                    getMainWindow().removeToolBar(getMainWindow().PlayerBar)
                    getMainWindow().PlayerBar.deleteLater()
                    getMainWindow().PlayerBar = None
                try: getMainWindow().removeDockWidget(getMainWindow().dckSpecialTools)
                except: pass
                getMainWindow().resetCentralWidget()
                uni.tableType = _tableType
                self.refreshBars()
                getMainWindow().FileManager.makeRefresh()
                MApplication.processEvents()
                return True
            else:
                return False
        except:
            ReportBug.ReportBug()
        return False

    def changeTableType(self, _action):
        try:
            selectedType = Tables.Tables.getThisTableType(_action.objectName())
            if _action.isChecked() and uni.tableType != selectedType:
                isChanged = self.changeTableTypeByType(selectedType)
                if isChanged is False:
                    _action.setChecked(False)
                    return False
            else:
                _action.setChecked(True)
        except:
            ReportBug.ReportBug()

    def getAllBarsStyleFromMySettings(self):
        getMainWindow().TableToolsBar.setToolButtonStyle(int(uni.MySettings["TableToolsBarButtonStyle"]))
        getMainWindow().ToolsBar.setToolButtonStyle(int(uni.MySettings["ToolsBarButtonStyle"]))
        if uni.tableType in ["2", "6", "8", "9"]:
            getMainWindow().PlayerBar.setToolButtonStyle(int(uni.MySettings["PlayerBarButtonStyle"]))

    def setAllBarsStyleToMySettings(self):
        uni.setMySetting("TableToolsBarButtonStyle", getMainWindow().TableToolsBar.toolButtonStyle())
        uni.setMySetting("ToolsBarButtonStyle", getMainWindow().ToolsBar.toolButtonStyle())
        if uni.tableType in ["2", "6", "8", "9"]:
            uni.setMySetting("PlayerBarButtonStyle", getMainWindow().PlayerBar.toolButtonStyle())

    def changeReNamerType(self, _action):
        try:
            if getMainWindow().Table.checkUnSavedValues() is False:
                _action.setChecked(False)
                for x, typeName in enumerate(uni.fileReNamerTypeNamesKeys):
                    if typeName == uni.MySettings["fileReNamerType"]:
                        getMainWindow().TableToolsBar.actsFileReNamerTypes[x].setChecked(True)
                return False
            for x, typeName in enumerate(uni.fileReNamerTypeNamesKeys):
                if getMainWindow().TableToolsBar.actsFileReNamerTypes[x].isChecked():
                    uni.setMySetting("fileReNamerType", typeName)
            getMainWindow().FileManager.makeRefresh()
            MApplication.processEvents()
        except:
            ReportBug.ReportBug()
        
