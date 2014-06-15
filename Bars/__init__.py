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


from Core import Variables as var
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
from Options import QuickOptions
from Taggers import getTaggerTypesName, getSelectedTaggerTypeForReadName, setSelectedTaggerTypeForReadName, getSelectedTaggerTypeForWriteName, setSelectedTaggerTypeForWriteName
from Bars import SubDirectoryOptionsBar, PlayerBar, MusicOptionsBar, CoverOptionsBar, AmarokMusicOptionsBar, AmarokCopyOptionsBar

class Bars():
    def __init__(self):
        uni.MainWindow.MusicOptionsBar = None
        uni.MainWindow.AmarokMusicOptionsBar = None
        uni.MainWindow.AmarokCopyOptionsBar = None
        uni.MainWindow.SubDirectoryOptionsBar = None
        uni.MainWindow.CoverOptionsBar = None
        
    def click(self, _action):
        try:
            actionName = _action.objectName()
            if actionName==translate("MenuBar", "Open State"):
                f = Dialogs.getOpenFileName(translate("MenuBar", "Open State Of Hamsi Manager"),
                                    fu.userDirectoryPath,translate("MenuBar", "Application Runner") + " (*.desktop)")
                if f is not None:
                    Settings.openStateOfSettings(f)
            elif actionName==translate("MenuBar", "Save State"):
                f = Dialogs.getSaveFileName(translate("MenuBar", "Save State Of Hamsi Manager"), fu.joinPath(fu.userDirectoryPath, "HamsiManager.desktop"),translate("MenuBar", "Application Runner") + " (*.desktop)")
                if f is not None:
                    Settings.saveStateOfSettings(f)
                    Dialogs.show(translate("MenuBar", "Current State Saved"), 
                            translate("MenuBar", "Current state saved with preferences.<br>You can continue where you left off."))
            elif actionName==translate("MenuBar", "With This Profile (My Settings)"):
                if Execute.executeAsRootWithThread(["--sDirectoryPath", fu.pathOfSettingsDirectory], "HamsiManager"):
                    uni.MainWindow.close()
                else:
                    Dialogs.showError(translate("MenuBar", "Can Not Run As Root"), translate("MenuBar", "Hamsi Manager can not run as root."))
            elif actionName==translate("MenuBar", "With Root Profile (Own Settings)"):
                if Execute.executeAsRootWithThread([], "HamsiManager"):
                    uni.MainWindow.close()
                else:
                    Dialogs.showError(translate("MenuBar", "Can Not Run As Root"), translate("MenuBar", "Hamsi Manager can not run as root."))
            elif actionName==translate("MenuBar", "Quit"):
                uni.MainWindow.close()
            elif actionName==translate("MenuBar", "HTML Format"):
                if _action.parent().objectName()==translate("MenuBar", "Export To File"):
                    uni.MainWindow.Table.exportValues("file", "html", "title")
                elif _action.parent().objectName()==translate("MenuBar", "Show In New Window"):
                    uni.MainWindow.Table.exportValues("dialog", "html", "title")
                elif _action.parent().objectName()==translate("MenuBar", "Copy To Clipboard"):
                    uni.MainWindow.Table.exportValues("clipboard", "html", "title")
            elif actionName==translate("MenuBar", "Text Format"):
                if _action.parent().objectName()==translate("MenuBar", "Export To File"):
                    uni.MainWindow.Table.exportValues("file", "plainText", "title")
                elif _action.parent().objectName()==translate("MenuBar", "Show In New Window"):
                    uni.MainWindow.Table.exportValues("dialog", "plainText", "title")
                elif _action.parent().objectName()==translate("MenuBar", "Copy To Clipboard"):
                    uni.MainWindow.Table.exportValues("clipboard", "plainText", "title")
            elif actionName==translate("MenuBar", "HTML Format (File Tree)"):
                if _action.parent().objectName()==translate("MenuBar", "Export To File"):
                    fu.getFileTree((uni.MainWindow.FileManager.currentDirectory), 0, "file", "html", "fileTree", "title")
                elif _action.parent().objectName()==translate("MenuBar", "Show In New Window"):
                    fu.getFileTree((uni.MainWindow.FileManager.currentDirectory), 0, "dialog", "html", "fileTree", "title")
                elif _action.parent().objectName()==translate("MenuBar", "Copy To Clipboard"):
                    fu.getFileTree((uni.MainWindow.FileManager.currentDirectory), 0, "clipboard", "html", "fileTree", "title")
            elif actionName==translate("MenuBar", "Text Format (File Tree)"):
                if _action.parent().objectName()==translate("MenuBar", "Export To File"):
                    fu.getFileTree((uni.MainWindow.FileManager.currentDirectory), 0, "file", "plainText", "fileTree", "title")
                elif _action.parent().objectName()==translate("MenuBar", "Show In New Window"):
                    fu.getFileTree((uni.MainWindow.FileManager.currentDirectory), 0, "dialog", "plainText", "fileTree", "title")
                elif _action.parent().objectName()==translate("MenuBar", "Copy To Clipboard"):
                    fu.getFileTree((uni.MainWindow.FileManager.currentDirectory), 0, "clipboard", "plainText", "fileTree", "title")
            elif actionName==translate("MenuBar", "About QT"):
                if isActivePyKDE4:
                    QMessageBox.aboutQt(uni.MainWindow, translate("MenuBar", "About QT"))
                else:
                    MMessageBox.aboutQt(uni.MainWindow, translate("MenuBar", "About QT"))
            elif actionName==translate("MenuBar", "Options"):
                from Options import OptionsForm
                OptionsForm.OptionsForm(uni.MainWindow)
            elif actionName==translate("MenuBar", "My Plugins"):
                import MyPlugins
                MyPlugins.MyPlugins()
            elif actionName==translate("MenuBar", "Reconfigure"):
                from Tools import Configurator
                Configurator.Configurator("configurePage")
            elif actionName==translate("MenuBar", "My Plugins (System)"):
                Execute.execute(["--qm", "--plugins", "--runAsRoot"], "HamsiManager")
            elif actionName==translate("MenuBar", "Reconfigure (System)"):
                Execute.execute(["--qm", "--configurator", "--runAsRoot"], "HamsiManager")
            elif actionName==translate("MenuBar", "Update"):
                from Core import UpdateControl
                UpdateControl.UpdateControl(uni.MainWindow)
            elif actionName==translate("MenuBar", "Report Bug"):
                ReportBug.ReportBug(True)
            elif actionName==translate("MenuBar", "Suggest Idea"):
                from Core import SuggestIdea
                SuggestIdea.SuggestIdea()
            elif actionName==translate("MenuBar", "About Hamsi Manager"):
                if isActivePyKDE4==False:
                    MMessageBox.about(uni.MainWindow, translate("MenuBar", "About Hamsi Manager"), var.aboutOfHamsiManager)
            elif actionName==translate("ToolsBar", "Check Icon"):
                uni.MainWindow.setEnabled(False)
                fu.checkIcon(uni.MainWindow.FileManager.getCurrentDirectoryPath())
                Dialogs.show(translate("ToolsBar", "Directory Icon Checked"),
                        translate("ToolsBar", "Current directory icon checked.<br>The default action based on the data is executed."))
                uni.MainWindow.setEnabled(True)
            elif actionName==translate("ToolsBar", "Clear Empty Directories"):
                if uni.MainWindow.Table.checkUnSavedValues()==False:
                    _action.setChecked(False)
                    return False
                answer = Dialogs.ask(translate("ToolsBar", "Empty Directories Will Be Removed"),
                        str(translate("ToolsBar", "Are you sure you want to remove empty directories based on the criteria you set in \"%s\"?")) % Organizer.getLink(uni.MainWindow.FileManager.getCurrentDirectoryPath()))
                if answer==Dialogs.Yes:
                    uni.MainWindow.setEnabled(False)
                    currentDirPath = uni.MainWindow.FileManager.getCurrentDirectoryPath()
                    if fu.isWritableFileOrDir(currentDirPath):
                        fu.checkEmptyDirectories(currentDirPath, True, True, True, True)
                        Dialogs.show(translate("ToolsBar", "Directory Cleaned"),
                            translate("ToolsBar", "The current directory is cleaned based on the criteria you set."))
                    uni.MainWindow.setEnabled(True)
                    uni.MainWindow.FileManager.makeRefresh()
            elif actionName==translate("ToolsBar", "Pack"):
                from Tools import Packager
                Packager.Packager(uni.MainWindow.FileManager.getCurrentDirectoryPath())
            elif actionName==translate("ToolsBar", "Hash"):
                from Tools import Hasher
                Hasher.Hasher(uni.MainWindow.FileManager.getCurrentDirectoryPath())
            elif actionName==translate("ToolsBar", "Clear"):
                from Tools import Cleaner
                Cleaner.Cleaner(uni.MainWindow.FileManager.getCurrentDirectoryPath())
            elif actionName==translate("ToolsBar", "Text Corrector"):
                from Tools import TextCorrector
                TextCorrector.TextCorrector(uni.MainWindow.FileManager.getCurrentDirectoryPath())
            elif actionName==translate("ToolsBar", "File Tree"):
                from Tools import FileTreeBuilder
                FileTreeBuilder.FileTreeBuilder(uni.MainWindow.FileManager.getCurrentDirectoryPath())
            elif actionName==translate("ToolsBar", "Search"):
                from Tools import Searcher
                Searcher.Searcher([uni.MainWindow.FileManager.getCurrentDirectoryPath()])
            elif actionName==translate("ToolsBar", "Script Manager"):
                from Tools import ScriptManager
                if ScriptManager.ScriptManager.checkScriptManager():
                    ScriptManager.ScriptManager(uni.MainWindow)
            elif actionName==translate("ToolsBar", "Show Last Actions"):
                from Core import RecordsForm
                RecordsForm.RecordsForm(uni.MainWindow)
            elif actionName==translate("ToolsBar", "Remove Sub Files"):
                answer = Dialogs.ask(translate("ToolsBar", "All Files Will Be Removed"),
                        str(translate("ToolsBar", "Are you sure you want to remove only all files in \"%s\"?<br>Note:Do not will remove directory and subfolders.")) % Organizer.getLink(uni.MainWindow.FileManager.getCurrentDirectoryPath()))
                if answer==Dialogs.Yes:
                    uni.MainWindow.setEnabled(False)
                    fu.removeOnlySubFiles(uni.MainWindow.FileManager.getCurrentDirectoryPath())
                    uni.MainWindow.setEnabled(True)
                    Dialogs.show(translate("ToolsBar", "Removed Only All Files"),
                        str(translate("ToolsBar", "Removed only all files in \"%s\".<br>Note:Do not removed directory and subfolders.")) % Organizer.getLink(uni.MainWindow.FileManager.getCurrentDirectoryPath()))
            elif actionName==translate("ToolsBar", "Amarok Embedded Database Configurator"):
                import Amarok
                if Amarok.checkAmarok():
                    Amarok.openEmbeddedDBConfigurator()
            elif _action.parent().objectName()==translate("ToolsBar", "Table Types"):
                self.changeTableType(_action)
            elif _action.parent().objectName()==translate("ToolsBar", "File Renamer Types"):
                self.changeReNamerType(_action)
            elif _action.parent().objectName()==translate("MenuBar", "Scripts"):
                from Core import Scripts
                Scripts.runScriptFile(fu.joinPath(Scripts.pathOfScripsDirectory, actionName))
            Records.saveAllRecords()
        except:
            ReportBug.ReportBug()
    
    def refreshBars(self):
        uni.MainWindow.Table = Tables.Tables(uni.MainWindow)
        uni.MainWindow.SpecialTools = SpecialTools.SpecialTools(uni.MainWindow)
        uni.MainWindow.Menu.mSpecialOptions.clear()
        if uni.tableType=="2":
            uni.MainWindow.PlayerBar = PlayerBar.PlayerBar(uni.MainWindow)
            uni.MainWindow.addToolBar(Mt.TopToolBarArea,uni.MainWindow.PlayerBar)
            uni.MainWindow.MusicOptionsBar = MusicOptionsBar.MusicOptionsBar(uni.MainWindow)
            uni.MainWindow.addToolBar(Mt.TopToolBarArea,uni.MainWindow.MusicOptionsBar)
            uni.MainWindow.MusicOptionsBar.getSpecialOptions(uni.MainWindow.Menu.mSpecialOptions)
        elif uni.tableType=="3":
            uni.MainWindow.SubDirectoryOptionsBar = SubDirectoryOptionsBar.SubDirectoryOptionsBar(uni.MainWindow)
            uni.MainWindow.addToolBar(Mt.TopToolBarArea,uni.MainWindow.SubDirectoryOptionsBar)
            uni.MainWindow.SubDirectoryOptionsBar.getSpecialOptions(uni.MainWindow.Menu.mSpecialOptions)
        elif uni.tableType=="4":
            uni.MainWindow.CoverOptionsBar = CoverOptionsBar.CoverOptionsBar(uni.MainWindow)
            uni.MainWindow.addToolBar(Mt.TopToolBarArea,uni.MainWindow.CoverOptionsBar)
            uni.MainWindow.CoverOptionsBar.getSpecialOptions(uni.MainWindow.Menu.mSpecialOptions)
        elif uni.tableType=="6":
            uni.MainWindow.PlayerBar = PlayerBar.PlayerBar(uni.MainWindow)
            uni.MainWindow.addToolBar(Mt.TopToolBarArea,uni.MainWindow.PlayerBar)
            uni.MainWindow.AmarokMusicOptionsBar = AmarokMusicOptionsBar.AmarokMusicOptionsBar(uni.MainWindow)
            uni.MainWindow.addToolBar(Mt.TopToolBarArea,uni.MainWindow.AmarokMusicOptionsBar)
            uni.MainWindow.AmarokMusicOptionsBar.getSpecialOptions(uni.MainWindow.Menu.mSpecialOptions)
        elif uni.tableType=="8":
            uni.MainWindow.PlayerBar = PlayerBar.PlayerBar(uni.MainWindow)
            uni.MainWindow.addToolBar(Mt.TopToolBarArea,uni.MainWindow.PlayerBar)
            uni.MainWindow.AmarokCopyOptionsBar = AmarokCopyOptionsBar.AmarokCopyOptionsBar(uni.MainWindow)
            uni.MainWindow.addToolBar(Mt.TopToolBarArea,uni.MainWindow.AmarokCopyOptionsBar)
            uni.MainWindow.AmarokCopyOptionsBar.getSpecialOptions(uni.MainWindow.Menu.mSpecialOptions)
        elif uni.tableType=="9":
            uni.MainWindow.PlayerBar = PlayerBar.PlayerBar(uni.MainWindow)
            uni.MainWindow.addToolBar(Mt.TopToolBarArea,uni.MainWindow.PlayerBar)
            uni.MainWindow.MusicOptionsBar = MusicOptionsBar.MusicOptionsBar(uni.MainWindow)
            uni.MainWindow.addToolBar(Mt.TopToolBarArea,uni.MainWindow.MusicOptionsBar)
            uni.MainWindow.MusicOptionsBar.getSpecialOptions(uni.MainWindow.Menu.mSpecialOptions)
            uni.MainWindow.SubDirectoryOptionsBar = SubDirectoryOptionsBar.SubDirectoryOptionsBar(uni.MainWindow)
            uni.MainWindow.addToolBar(Mt.TopToolBarArea,uni.MainWindow.SubDirectoryOptionsBar)
            uni.MainWindow.SubDirectoryOptionsBar.getSpecialOptions(uni.MainWindow.Menu.mSpecialOptions)
        if len(uni.MainWindow.Menu.mSpecialOptions.actions())==0:
            uni.MainWindow.Menu.mSpecialOptions.setEnabled(False)
        else:
            uni.MainWindow.Menu.mSpecialOptions.setEnabled(True)
        uni.MainWindow.Menu.refreshForTableType()
        
    def changeTableTypeByType(self, _tableType):
        try:
            if uni.tableType != _tableType:
                if uni.MainWindow.Table.checkUnSavedValues()==False:
                    return False
                uni.setMySetting(uni.MainWindow.Table.SubTable.hiddenTableColumnsSettingKey,uni.MainWindow.Table.hiddenTableColumns)
                if uni.tableType=="2":
                    uni.MainWindow.removeToolBar(uni.MainWindow.PlayerBar)
                    uni.MainWindow.PlayerBar.deleteLater()
                    uni.MainWindow.PlayerBar = None
                    uni.MainWindow.removeToolBar(uni.MainWindow.MusicOptionsBar)
                    uni.MainWindow.MusicOptionsBar.deleteLater()
                    uni.MainWindow.MusicOptionsBar = None
                elif uni.tableType=="3":
                    uni.MainWindow.removeToolBar(uni.MainWindow.SubDirectoryOptionsBar)
                    uni.MainWindow.SubDirectoryOptionsBar.deleteLater()
                    uni.MainWindow.SubDirectoryOptionsBar = None
                elif uni.tableType=="4":
                    uni.MainWindow.removeToolBar(uni.MainWindow.CoverOptionsBar)
                    uni.MainWindow.CoverOptionsBar.deleteLater()
                    uni.MainWindow.CoverOptionsBar = None
                elif uni.tableType=="6":
                    uni.MainWindow.removeToolBar(uni.MainWindow.PlayerBar)
                    uni.MainWindow.PlayerBar.deleteLater()
                    uni.MainWindow.PlayerBar = None
                    uni.MainWindow.removeToolBar(uni.MainWindow.AmarokMusicOptionsBar)
                    uni.MainWindow.AmarokMusicOptionsBar.deleteLater()
                    uni.MainWindow.AmarokMusicOptionsBar = None
                elif uni.tableType=="8":
                    uni.MainWindow.removeToolBar(uni.MainWindow.PlayerBar)
                    uni.MainWindow.PlayerBar.deleteLater()
                    uni.MainWindow.PlayerBar = None
                    uni.MainWindow.removeToolBar(uni.MainWindow.AmarokCopyOptionsBar)
                    uni.MainWindow.AmarokCopyOptionsBar.deleteLater()
                    uni.MainWindow.AmarokCopyOptionsBar = None
                elif uni.tableType=="9":
                    uni.MainWindow.removeToolBar(uni.MainWindow.PlayerBar)
                    uni.MainWindow.PlayerBar.deleteLater()
                    uni.MainWindow.PlayerBar = None
                    uni.MainWindow.removeToolBar(uni.MainWindow.MusicOptionsBar)
                    uni.MainWindow.MusicOptionsBar.deleteLater()
                    uni.MainWindow.MusicOptionsBar = None
                    uni.MainWindow.removeToolBar(uni.MainWindow.SubDirectoryOptionsBar)
                    uni.MainWindow.SubDirectoryOptionsBar.deleteLater()
                    uni.MainWindow.SubDirectoryOptionsBar = None
                try:uni.MainWindow.removeDockWidget(uni.MainWindow.dckSpecialTools)
                except:pass
                uni.MainWindow.resetCentralWidget()
                uni.tableType = _tableType
                self.refreshBars()
                uni.MainWindow.FileManager.makeRefresh()
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
                if isChanged==False:
                    _action.setChecked(False)
                    return False
            else:
                _action.setChecked(True)
        except:
            ReportBug.ReportBug()
    
    def getAllBarsStyleFromMySettings(self):
        uni.MainWindow.TableToolsBar.setToolButtonStyle(int(uni.MySettings["TableToolsBarButtonStyle"]))
        uni.MainWindow.ToolsBar.setToolButtonStyle(int(uni.MySettings["ToolsBarButtonStyle"]))
        if uni.tableType=="2":
            uni.MainWindow.PlayerBar.setToolButtonStyle(int(uni.MySettings["PlayerBarButtonStyle"]))
            uni.MainWindow.MusicOptionsBar.setToolButtonStyle(int(uni.MySettings["MusicOptionsBarButtonStyle"]))
        elif uni.tableType=="3":
            uni.MainWindow.SubDirectoryOptionsBar.setToolButtonStyle(int(uni.MySettings["SubDirectoryOptionsBarButtonStyle"]))
        elif uni.tableType=="4":
            uni.MainWindow.CoverOptionsBar.setToolButtonStyle(int(uni.MySettings["CoverOptionsBarButtonStyle"]))
        elif uni.tableType=="6":
            uni.MainWindow.PlayerBar.setToolButtonStyle(int(uni.MySettings["PlayerBarButtonStyle"]))
            uni.MainWindow.AmarokMusicOptionsBar.setToolButtonStyle(int(uni.MySettings["AmarokMusicOptionsBarButtonStyle"]))
        elif uni.tableType=="8":
            uni.MainWindow.PlayerBar.setToolButtonStyle(int(uni.MySettings["PlayerBarButtonStyle"]))
            uni.MainWindow.AmarokCopyOptionsBar.setToolButtonStyle(int(uni.MySettings["AmarokCopyOptionsBarButtonStyle"]))
        elif uni.tableType=="9":
            uni.MainWindow.PlayerBar.setToolButtonStyle(int(uni.MySettings["PlayerBarButtonStyle"]))
            uni.MainWindow.MusicOptionsBar.setToolButtonStyle(int(uni.MySettings["MusicOptionsBarButtonStyle"]))
            uni.MainWindow.SubDirectoryOptionsBar.setToolButtonStyle(int(uni.MySettings["SubDirectoryOptionsBarButtonStyle"]))
        
    def setAllBarsStyleToMySettings(self):
        uni.setMySetting("TableToolsBarButtonStyle", uni.MainWindow.TableToolsBar.toolButtonStyle())
        uni.setMySetting("ToolsBarButtonStyle", uni.MainWindow.ToolsBar.toolButtonStyle())
        if uni.tableType=="2":
            uni.setMySetting("PlayerBarButtonStyle", uni.MainWindow.PlayerBar.toolButtonStyle())
            uni.setMySetting("MusicOptionsBarButtonStyle", uni.MainWindow.MusicOptionsBar.toolButtonStyle())
        elif uni.tableType=="3":
            uni.setMySetting("SubDirectoryOptionsBarButtonStyle", uni.MainWindow.SubDirectoryOptionsBar.toolButtonStyle())
        elif uni.tableType=="4":
            uni.setMySetting("CoverOptionsBarButtonStyle", uni.MainWindow.CoverOptionsBar.toolButtonStyle())
        elif uni.tableType=="6":
            uni.setMySetting("PlayerBarButtonStyle", uni.MainWindow.PlayerBar.toolButtonStyle())
            uni.setMySetting("AmarokMusicOptionsBarButtonStyle", uni.MainWindow.AmarokMusicOptionsBar.toolButtonStyle())
        elif uni.tableType=="8":
            uni.setMySetting("PlayerBarButtonStyle", uni.MainWindow.PlayerBar.toolButtonStyle())
            uni.setMySetting("AmarokCopyOptionsBarButtonStyle", uni.MainWindow.AmarokCopyOptionsBar.toolButtonStyle())
        elif uni.tableType=="9":
            uni.setMySetting("PlayerBarButtonStyle", uni.MainWindow.PlayerBar.toolButtonStyle())
            uni.setMySetting("MusicOptionsBarButtonStyle", uni.MainWindow.MusicOptionsBar.toolButtonStyle())
            uni.setMySetting("SubDirectoryOptionsBarButtonStyle", uni.MainWindow.SubDirectoryOptionsBar.toolButtonStyle())
        
    def changeReNamerType(self, _action):
        try:
            if uni.MainWindow.Table.checkUnSavedValues()==False:
                _action.setChecked(False)
                for x, typeName in enumerate(var.fileReNamerTypeNamesKeys):
                    if typeName == uni.MySettings["fileReNamerType"]:
                        MainWindow.TableToolsBar.actsFileReNamerTypes[x].setChecked(True)
                return False
            for x, typeName in enumerate(var.fileReNamerTypeNamesKeys):
                if MainWindow.TableToolsBar.actsFileReNamerTypes[x].isChecked():
                    uni.setMySetting("fileReNamerType", typeName)
            uni.MainWindow.FileManager.makeRefresh()
            MApplication.processEvents()
        except:
            ReportBug.ReportBug()
        
