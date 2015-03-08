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


def clickedAnAction(_action):
    try:
        actionName = _action.objectName()
        if actionName == "Open State":
            f = Dialogs.getOpenFileName(translate("MenuBar", "Open State Of Hamsi Manager"),
                                        fu.userDirectoryPath,
                                        translate("MenuBar", "Application Runner") + " (*.desktop)")
            if f is not None:
                Settings.openStateOfSettings(f)
        elif actionName == "Save State":
            f = Dialogs.getSaveFileName(translate("MenuBar", "Save State Of Hamsi Manager"),
                                        fu.joinPath(fu.userDirectoryPath, "HamsiManager.desktop"),
                                        translate("MenuBar", "Application Runner") + " (*.desktop)")
            if f is not None:
                Settings.saveStateOfSettings(f)
                Dialogs.show(translate("MenuBar", "Current State Saved"),
                             translate("MenuBar",
                                       "Current state saved with preferences.<br>You can continue where you left off."))
        elif actionName == "With This Profile (My Settings)":
            if Execute.executeAsRootWithThread(["--sDirectoryPath", fu.pathOfSettingsDirectory], "HamsiManager"):
                getMainWindow().close()
            else:
                Dialogs.showError(translate("MenuBar", "Can Not Run As Root"),
                                  translate("MenuBar", "Hamsi Manager can not run as root."))
        elif actionName == "With Root Profile (Own Settings)":
            if Execute.executeAsRootWithThread([], "HamsiManager"):
                getMainWindow().close()
            else:
                Dialogs.showError(translate("MenuBar", "Can Not Run As Root"),
                                  translate("MenuBar", "Hamsi Manager can not run as root."))
        elif actionName == "Quit":
            getMainWindow().close()
        elif actionName == "HTML Format":
            if _action.parent().objectName() == "Export To File":
                getMainTable().exportValues("file", "html", "title")
            elif _action.parent().objectName() == "Show In New Window":
                getMainTable().exportValues("dialog", "html", "title")
            elif _action.parent().objectName() == "Copy To Clipboard":
                getMainTable().exportValues("clipboard", "html", "title")
        elif actionName == "Text Format":
            if _action.parent().objectName() == "Export To File":
                getMainTable().exportValues("file", "plainText", "title")
            elif _action.parent().objectName() == "Show In New Window":
                getMainTable().exportValues("dialog", "plainText", "title")
            elif _action.parent().objectName() == "Copy To Clipboard":
                getMainTable().exportValues("clipboard", "plainText", "title")
        elif actionName == "HTML Format (File Tree)":
            if _action.parent().objectName() == "Export To File":
                fu.getFileTree((getMainWindow().FileManager.currentDirectory), 0, "file", "html", "fileTree",
                               "title")
            elif _action.parent().objectName() == "Show In New Window":
                fu.getFileTree((getMainWindow().FileManager.currentDirectory), 0, "dialog", "html", "fileTree",
                               "title")
            elif _action.parent().objectName() == "Copy To Clipboard":
                fu.getFileTree((getMainWindow().FileManager.currentDirectory), 0, "clipboard", "html", "fileTree",
                               "title")
        elif actionName == "Text Format (File Tree)":
            if _action.parent().objectName() == "Export To File":
                fu.getFileTree((getMainWindow().FileManager.currentDirectory), 0, "file", "plainText", "fileTree",
                               "title")
            elif _action.parent().objectName() == "Show In New Window":
                fu.getFileTree((getMainWindow().FileManager.currentDirectory), 0, "dialog", "plainText", "fileTree",
                               "title")
            elif _action.parent().objectName() == "Copy To Clipboard":
                fu.getFileTree((getMainWindow().FileManager.currentDirectory), 0, "clipboard", "plainText",
                               "fileTree", "title")
        elif actionName == "About QT":
            if isActivePyKDE4:
                QMessageBox.aboutQt(getMainWindow(), translate("MenuBar", "About QT"))
            else:
                MMessageBox.aboutQt(getMainWindow(), translate("MenuBar", "About QT"))
        elif actionName == "Options":
            from Options import OptionsForm

            OptionsForm.OptionsForm(getMainWindow())
        elif actionName == "My Plugins":
            import MyPlugins

            MyPlugins.MyPlugins()
        elif actionName == "Reconfigure":
            from Tools import Configurator

            Configurator.Configurator("configurePage")
        elif actionName == "My Plugins (System)":
            Execute.execute(["--qm", "--plugins", "--runAsRoot"], "HamsiManager")
        elif actionName == "Reconfigure (System)":
            Execute.execute(["--qm", "--configurator", "--runAsRoot"], "HamsiManager")
        elif actionName == "Update":
            from Core import UpdateControl

            UpdateControl.UpdateControl(getMainWindow())
        elif actionName == "Report Bug":
            ReportBug.ReportBug(True)
        elif actionName == "Suggest Idea":
            from Core import SuggestIdea

            SuggestIdea.SuggestIdea()
        elif actionName == "About Hamsi Manager":
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
        elif actionName == "Clear Empty Directories":
            if getMainTable().checkUnSavedValues() is False:
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
        elif actionName == "Pack":
            from Tools import Packager

            Packager.Packager(getMainWindow().FileManager.getCurrentDirectoryPath())
        elif actionName == "Hash":
            from Tools import Hasher

            Hasher.Hasher(getMainWindow().FileManager.getCurrentDirectoryPath())
        elif actionName == "Clear":
            from Tools import Cleaner

            Cleaner.Cleaner(getMainWindow().FileManager.getCurrentDirectoryPath())
        elif actionName == "Text Corrector":
            from Tools import TextCorrector

            TextCorrector.TextCorrector(getMainWindow().FileManager.getCurrentDirectoryPath())
        elif actionName == "File Tree":
            from Tools import FileTreeBuilder

            FileTreeBuilder.FileTreeBuilder(getMainWindow().FileManager.getCurrentDirectoryPath())
        elif actionName == "Search":
            from Tools import Searcher

            Searcher.Searcher([getMainWindow().FileManager.getCurrentDirectoryPath()])
        elif actionName == "Script Manager":
            from Tools import ScriptManager

            if ScriptManager.ScriptManager.checkScriptManager():
                ScriptManager.ScriptManager(getMainWindow())
        elif actionName == "Show Last Actions":
            from Core import RecordsForm

            RecordsForm.RecordsForm(getMainWindow())
        elif actionName == "Remove Sub Files":
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
        elif actionName == "Amarok Embedded Database Configurator":
            import Amarok

            if Amarok.checkAmarok():
                Amarok.openEmbeddedDBConfigurator()
        elif _action.parent().objectName() == "Table Types":
            changeTableType(_action)
        elif _action.parent().objectName() == "File Renamer Types":
            changeReNamerType(_action)
        elif _action.parent().objectName() == "Scripts":
            from Core import Scripts

            Scripts.runScriptFile(fu.joinPath(Scripts.pathOfScripsDirectory, actionName))
        Records.saveAllRecords()
    except:
        ReportBug.ReportBug()


def refreshBars():
    setMainTable(Tables.Tables(getMainWindow()).Table)
    getMainWindow().SpecialTools = SpecialTools.SpecialTools(getMainWindow())
    if uni.tableType in ["2", "6", "8", "9"]:
        from Bars import PlayerBar

        getMainWindow().PlayerBar = PlayerBar.PlayerBar(getMainWindow())
        getMainWindow().addToolBar(Mt.TopToolBarArea, getMainWindow().PlayerBar)
    getMainWindow().Menu.refreshForTableType()


def changeTableTypeByType(_tableType):
    try:
        if uni.tableType != _tableType:
            if getMainTable().checkUnSavedValues() is False:
                return False
            uni.setMySetting(getMainTable().hiddenTableColumnsSettingKey,
                             getMainTable().hiddenTableColumns)
            if uni.tableType in ["2", "6", "8", "9"]:
                getMainWindow().removeToolBar(getMainWindow().PlayerBar)
                getMainWindow().PlayerBar.deleteLater()
                getMainWindow().PlayerBar = None
            try: getMainWindow().removeDockWidget(getMainWindow().dckSpecialTools)
            except: pass
            getMainWindow().resetCentralWidget()
            uni.tableType = _tableType
            refreshBars()
            getMainWindow().FileManager.makeRefresh()
            MApplication.processEvents()
            return True
        else:
            return False
    except:
        ReportBug.ReportBug()
    return False


def changeTableType(_action):
    try:
        selectedType = Tables.Tables.getThisTableType(_action.objectName())
        if _action.isChecked() and uni.tableType != selectedType:
            isChanged = changeTableTypeByType(selectedType)
            if isChanged is False:
                _action.setChecked(False)
                return False
        else:
            _action.setChecked(True)
    except:
        ReportBug.ReportBug()


def getAllBarsStyleFromMySettings():
    getMainWindow().TableToolsBar.setToolButtonStyle(int(uni.MySettings["TableToolsBarButtonStyle"]))
    getMainWindow().ToolsBar.setToolButtonStyle(int(uni.MySettings["ToolsBarButtonStyle"]))
    if uni.tableType in ["2", "6", "8", "9"]:
        getMainWindow().PlayerBar.setToolButtonStyle(int(uni.MySettings["PlayerBarButtonStyle"]))


def setAllBarsStyleToMySettings():
    uni.setMySetting("TableToolsBarButtonStyle", getMainWindow().TableToolsBar.toolButtonStyle())
    uni.setMySetting("ToolsBarButtonStyle", getMainWindow().ToolsBar.toolButtonStyle())
    if uni.tableType in ["2", "6", "8", "9"]:
        uni.setMySetting("PlayerBarButtonStyle", getMainWindow().PlayerBar.toolButtonStyle())


def changeReNamerType(_action):
    try:
        if getMainTable().checkUnSavedValues() is False:
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


def getCopyOfMAction(_action):
    a = MAction(MIcon(_action.icon()), _action.text(), _action.parent())
    a.setObjectName(_action.objectName())
    a.setToolTip(_action.toolTip())
    return a