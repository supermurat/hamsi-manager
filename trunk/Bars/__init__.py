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


from Core import Variables
import Tables
import SpecialTools
from Core import Universals
from Core import Dialogs
from Core.MyObjects import *
from Core import ReportBug
from Core import Organizer
from Core import Execute
from Core import Records
from Core import Settings
import InputOutputs
from Options import QuickOptions
from Taggers import getTaggerTypesName, getSelectedTaggerTypeForReadName, setSelectedTaggerTypeForReadName, getSelectedTaggerTypeForWriteName, setSelectedTaggerTypeForWriteName
from Bars import SubDirectoryOptionsBar, PlayerBar, MusicOptionsBar, CoverOptionsBar, AmarokMusicOptionsBar, AmarokCopyOptionsBar

class Bars():
    def __init__(self):
        Universals.MainWindow.MusicOptionsBar = None
        Universals.MainWindow.AmarokMusicOptionsBar = None
        Universals.MainWindow.AmarokCopyOptionsBar = None
        Universals.MainWindow.SubDirectoryOptionsBar = None
        Universals.MainWindow.CoverOptionsBar = None
        
    def click(self, _action):
        try:
            global Universals
            actionName = _action.objectName()
            if actionName==translate("MenuBar", "Open State"):
                f = Dialogs.getOpenFileName(translate("MenuBar", "Open State Of Hamsi Manager"),
                                    InputOutputs.userDirectoryPath,translate("MenuBar", "Application Runner") + " (*.desktop)")
                if f is not None:
                    Settings.openStateOfSettings(f)
            elif actionName==translate("MenuBar", "Save State"):
                f = Dialogs.getSaveFileName(translate("MenuBar", "Save State Of Hamsi Manager"), InputOutputs.joinPath(InputOutputs.userDirectoryPath, "HamsiManager.desktop"),translate("MenuBar", "Application Runner") + " (*.desktop)")
                if f is not None:
                    Settings.saveStateOfSettings(f)
                    Dialogs.show(translate("MenuBar", "Current State Saved"), 
                            translate("MenuBar", "Current state saved with preferences.<br>You can continue where you left off."))
            elif actionName==translate("MenuBar", "With This Profile (My Settings)"):
                if Execute.executeAsRootWithThread(["--sDirectoryPath", InputOutputs.pathOfSettingsDirectory], "HamsiManager"):
                    Universals.MainWindow.close()
                else:
                    Dialogs.showError(translate("MenuBar", "Can Not Run As Root"), translate("MenuBar", "Hamsi Manager can not run as root."))
            elif actionName==translate("MenuBar", "With Root Profile (Own Settings)"):
                if Execute.executeAsRootWithThread([], "HamsiManager"):
                    Universals.MainWindow.close()
                else:
                    Dialogs.showError(translate("MenuBar", "Can Not Run As Root"), translate("MenuBar", "Hamsi Manager can not run as root."))
            elif actionName==translate("MenuBar", "Quit"):
                Universals.MainWindow.close()
            elif actionName==translate("MenuBar", "HTML Format"):
                if _action.parent().objectName()==translate("MenuBar", "Export To File"):
                    Universals.MainWindow.Table.exportValues("file", "html", "title")
                elif _action.parent().objectName()==translate("MenuBar", "Show In New Window"):
                    Universals.MainWindow.Table.exportValues("dialog", "html", "title")
                elif _action.parent().objectName()==translate("MenuBar", "Copy To Clipboard"):
                    Universals.MainWindow.Table.exportValues("clipboard", "html", "title")
            elif actionName==translate("MenuBar", "Text Format"):
                if _action.parent().objectName()==translate("MenuBar", "Export To File"):
                    Universals.MainWindow.Table.exportValues("file", "plainText", "title")
                elif _action.parent().objectName()==translate("MenuBar", "Show In New Window"):
                    Universals.MainWindow.Table.exportValues("dialog", "plainText", "title")
                elif _action.parent().objectName()==translate("MenuBar", "Copy To Clipboard"):
                    Universals.MainWindow.Table.exportValues("clipboard", "plainText", "title")
            elif actionName==translate("MenuBar", "HTML Format (File Tree)"):
                if _action.parent().objectName()==translate("MenuBar", "Export To File"):
                    InputOutputs.getFileTree((Universals.MainWindow.FileManager.currentDirectory), 0, "file", "html", "fileTree", "title")
                elif _action.parent().objectName()==translate("MenuBar", "Show In New Window"):
                    InputOutputs.getFileTree((Universals.MainWindow.FileManager.currentDirectory), 0, "dialog", "html", "fileTree", "title")
                elif _action.parent().objectName()==translate("MenuBar", "Copy To Clipboard"):
                    InputOutputs.getFileTree((Universals.MainWindow.FileManager.currentDirectory), 0, "clipboard", "html", "fileTree", "title")
            elif actionName==translate("MenuBar", "Text Format (File Tree)"):
                if _action.parent().objectName()==translate("MenuBar", "Export To File"):
                    InputOutputs.getFileTree((Universals.MainWindow.FileManager.currentDirectory), 0, "file", "plainText", "fileTree", "title")
                elif _action.parent().objectName()==translate("MenuBar", "Show In New Window"):
                    InputOutputs.getFileTree((Universals.MainWindow.FileManager.currentDirectory), 0, "dialog", "plainText", "fileTree", "title")
                elif _action.parent().objectName()==translate("MenuBar", "Copy To Clipboard"):
                    InputOutputs.getFileTree((Universals.MainWindow.FileManager.currentDirectory), 0, "clipboard", "plainText", "fileTree", "title")
            elif actionName==translate("MenuBar", "About QT"):
                if isActivePyKDE4==True:
                    QMessageBox.aboutQt(Universals.MainWindow, translate("MenuBar", "About QT"))
                else:
                    MMessageBox.aboutQt(Universals.MainWindow, translate("MenuBar", "About QT"))
            elif actionName==translate("MenuBar", "Options"):
                from Options import OptionsForm
                OptionsForm.OptionsForm(Universals.MainWindow)
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
                UpdateControl.UpdateControl(Universals.MainWindow)
            elif actionName==translate("MenuBar", "Report Bug"):
                ReportBug.ReportBug(True)
            elif actionName==translate("MenuBar", "Suggest Idea"):
                from Core import SuggestIdea
                SuggestIdea.SuggestIdea()
            elif actionName==translate("MenuBar", "About Hamsi Manager"):
                if isActivePyKDE4==False:
                    MMessageBox.about(Universals.MainWindow, translate("MenuBar", "About Hamsi Manager"), Variables.aboutOfHamsiManager)
            elif actionName==translate("ToolsBar", "Check Icon"):
                Universals.MainWindow.setEnabled(False)
                InputOutputs.checkIcon(Universals.MainWindow.FileManager.getCurrentDirectoryPath())
                Dialogs.show(translate("ToolsBar", "Directory Icon Checked"),
                        translate("ToolsBar", "Current directory icon checked.<br>The default action based on the data is executed."))
                Universals.MainWindow.setEnabled(True)
            elif actionName==translate("ToolsBar", "Clear Empty Directories"):
                if Universals.MainWindow.Table.checkUnSavedValues()==False:
                    _action.setChecked(False)
                    return False
                answer = Dialogs.ask(translate("ToolsBar", "Empty Directories Will Be Removed"),
                        str(translate("ToolsBar", "Are you sure you want to remove empty directories based on the criteria you set in \"%s\"?")) % Organizer.getLink(Universals.MainWindow.FileManager.getCurrentDirectoryPath()))
                if answer==Dialogs.Yes:
                    Universals.MainWindow.setEnabled(False)
                    currentDirPath = Universals.MainWindow.FileManager.getCurrentDirectoryPath()
                    if InputOutputs.isWritableFileOrDir(currentDirPath):
                        InputOutputs.checkEmptyDirectories(currentDirPath, True, True, True, True)
                        Dialogs.show(translate("ToolsBar", "Directory Cleaned"),
                            translate("ToolsBar", "The current directory is cleaned based on the criteria you set."))
                    Universals.MainWindow.setEnabled(True)
                    Universals.MainWindow.FileManager.makeRefresh()
            elif actionName==translate("ToolsBar", "Pack"):
                from Tools import Packager
                Packager.Packager(Universals.MainWindow.FileManager.getCurrentDirectoryPath())
            elif actionName==translate("ToolsBar", "Hash"):
                from Tools import Hasher
                Hasher.Hasher(Universals.MainWindow.FileManager.getCurrentDirectoryPath())
            elif actionName==translate("ToolsBar", "Clear"):
                from Tools import Cleaner
                Cleaner.Cleaner(Universals.MainWindow.FileManager.getCurrentDirectoryPath())
            elif actionName==translate("ToolsBar", "Text Corrector"):
                from Tools import TextCorrector
                TextCorrector.TextCorrector(Universals.MainWindow.FileManager.getCurrentDirectoryPath())
            elif actionName==translate("ToolsBar", "File Tree"):
                from Tools import FileTreeBuilder
                FileTreeBuilder.FileTreeBuilder(Universals.MainWindow.FileManager.getCurrentDirectoryPath())
            elif actionName==translate("ToolsBar", "Search"):
                from Tools import Searcher
                Searcher.Searcher([Universals.MainWindow.FileManager.getCurrentDirectoryPath()])
            elif actionName==translate("ToolsBar", "Script Manager"):
                from Tools import ScriptManager
                if ScriptManager.checkScriptManager():
                    ScriptManager.ScriptManager(Universals.MainWindow)
            elif actionName==translate("ToolsBar", "Show Last Actions"):
                from Core import RecordsForm
                RecordsForm.RecordsForm(Universals.MainWindow)
            elif actionName==translate("ToolsBar", "Remove Sub Files"):
                answer = Dialogs.ask(translate("ToolsBar", "All Files Will Be Removed"),
                        str(translate("ToolsBar", "Are you sure you want to remove only all files in \"%s\"?<br>Note:Do not will remove directory and subfolders.")) % Organizer.getLink(Universals.MainWindow.FileManager.getCurrentDirectoryPath()))
                if answer==Dialogs.Yes:
                    Universals.MainWindow.setEnabled(False)
                    InputOutputs.removeOnlySubFiles(Universals.MainWindow.FileManager.getCurrentDirectoryPath())
                    Universals.MainWindow.setEnabled(True)
                    Dialogs.show(translate("ToolsBar", "Removed Only All Files"),
                        str(translate("ToolsBar", "Removed only all files in \"%s\".<br>Note:Do not removed directory and subfolders.")) % Organizer.getLink(Universals.MainWindow.FileManager.getCurrentDirectoryPath()))
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
                Scripts.runScriptFile(InputOutputs.joinPath(Scripts.pathOfScripsDirectory, actionName))
            Records.saveAllRecords()
        except:
            ReportBug.ReportBug()
    
    def refreshBars(self):
        Universals.MainWindow.Table = Tables.Tables(Universals.MainWindow)
        Universals.MainWindow.SpecialTools = SpecialTools.SpecialTools(Universals.MainWindow)
        Universals.MainWindow.Menu.mSpecialOptions.clear()
        if Universals.tableType=="2":
            Universals.MainWindow.PlayerBar = PlayerBar.PlayerBar(Universals.MainWindow)
            Universals.MainWindow.addToolBar(Mt.TopToolBarArea,Universals.MainWindow.PlayerBar)
            Universals.MainWindow.MusicOptionsBar = MusicOptionsBar.MusicOptionsBar(Universals.MainWindow)
            Universals.MainWindow.addToolBar(Mt.TopToolBarArea,Universals.MainWindow.MusicOptionsBar)
            Universals.MainWindow.MusicOptionsBar.getSpecialOptions(Universals.MainWindow.Menu.mSpecialOptions)
        elif Universals.tableType=="3":
            Universals.MainWindow.SubDirectoryOptionsBar = SubDirectoryOptionsBar.SubDirectoryOptionsBar(Universals.MainWindow)
            Universals.MainWindow.addToolBar(Mt.TopToolBarArea,Universals.MainWindow.SubDirectoryOptionsBar)
            Universals.MainWindow.SubDirectoryOptionsBar.getSpecialOptions(Universals.MainWindow.Menu.mSpecialOptions)
        elif Universals.tableType=="4":
            Universals.MainWindow.CoverOptionsBar = CoverOptionsBar.CoverOptionsBar(Universals.MainWindow)
            Universals.MainWindow.addToolBar(Mt.TopToolBarArea,Universals.MainWindow.CoverOptionsBar)
            Universals.MainWindow.CoverOptionsBar.getSpecialOptions(Universals.MainWindow.Menu.mSpecialOptions)
        elif Universals.tableType=="6":
            Universals.MainWindow.PlayerBar = PlayerBar(Universals.MainWindow)
            Universals.MainWindow.addToolBar(Mt.TopToolBarArea,Universals.MainWindow.PlayerBar)
            Universals.MainWindow.AmarokMusicOptionsBar = AmarokMusicOptionsBar.AmarokMusicOptionsBar(Universals.MainWindow)
            Universals.MainWindow.addToolBar(Mt.TopToolBarArea,Universals.MainWindow.AmarokMusicOptionsBar)
            Universals.MainWindow.AmarokMusicOptionsBar.getSpecialOptions(Universals.MainWindow.Menu.mSpecialOptions)
        elif Universals.tableType=="8":
            Universals.MainWindow.PlayerBar = PlayerBar(Universals.MainWindow)
            Universals.MainWindow.addToolBar(Mt.TopToolBarArea,Universals.MainWindow.PlayerBar)
            Universals.MainWindow.AmarokCopyOptionsBar = AmarokCopyOptionsBar.AmarokCopyOptionsBar(Universals.MainWindow)
            Universals.MainWindow.addToolBar(Mt.TopToolBarArea,Universals.MainWindow.AmarokCopyOptionsBar)
            Universals.MainWindow.AmarokCopyOptionsBar.getSpecialOptions(Universals.MainWindow.Menu.mSpecialOptions)
        if len(Universals.MainWindow.Menu.mSpecialOptions.actions())==0:
            Universals.MainWindow.Menu.mSpecialOptions.setEnabled(False)
        else:
            Universals.MainWindow.Menu.mSpecialOptions.setEnabled(True)
        Universals.MainWindow.Menu.refreshForTableType()
        
    def changeTableTypeByType(self, _tableType):
        try:
            if Universals.tableType != _tableType:
                if Universals.MainWindow.Table.checkUnSavedValues()==False:
                    return False
                Universals.setMySetting(Universals.MainWindow.Table.SubTable.hiddenTableColumnsSettingKey,Universals.MainWindow.Table.hiddenTableColumns)
                if Universals.tableType=="2":
                    Universals.MainWindow.removeToolBar(Universals.MainWindow.PlayerBar)
                    Universals.MainWindow.PlayerBar.deleteLater()
                    Universals.MainWindow.PlayerBar = None
                    Universals.MainWindow.removeToolBar(Universals.MainWindow.MusicOptionsBar)
                    Universals.MainWindow.MusicOptionsBar.deleteLater()
                    Universals.MainWindow.MusicOptionsBar = None
                elif Universals.tableType=="3":
                    Universals.MainWindow.removeToolBar(Universals.MainWindow.SubDirectoryOptionsBar)
                    Universals.MainWindow.SubDirectoryOptionsBar.deleteLater()
                    Universals.MainWindow.SubDirectoryOptionsBar = None
                elif Universals.tableType=="4":
                    Universals.MainWindow.removeToolBar(Universals.MainWindow.CoverOptionsBar)
                    Universals.MainWindow.CoverOptionsBar.deleteLater()
                    Universals.MainWindow.CoverOptionsBar = None
                elif Universals.tableType=="6":
                    Universals.MainWindow.removeToolBar(Universals.MainWindow.PlayerBar)
                    Universals.MainWindow.PlayerBar.deleteLater()
                    Universals.MainWindow.PlayerBar = None
                    Universals.MainWindow.removeToolBar(Universals.MainWindow.AmarokMusicOptionsBar)
                    Universals.MainWindow.AmarokMusicOptionsBar.deleteLater()
                    Universals.MainWindow.AmarokMusicOptionsBar = None
                elif Universals.tableType=="8":
                    Universals.MainWindow.removeToolBar(Universals.MainWindow.PlayerBar)
                    Universals.MainWindow.PlayerBar.deleteLater()
                    Universals.MainWindow.PlayerBar = None
                    Universals.MainWindow.removeToolBar(Universals.MainWindow.AmarokCopyOptionsBar)
                    Universals.MainWindow.AmarokCopyOptionsBar.deleteLater()
                    Universals.MainWindow.AmarokCopyOptionsBar = None
                try:Universals.MainWindow.removeDockWidget(Universals.MainWindow.dckSpecialTools)
                except:pass
                Universals.MainWindow.resetCentralWidget()
                Universals.tableType = _tableType
                self.refreshBars()
                Universals.MainWindow.FileManager.makeRefresh()
                MApplication.processEvents()
                return True
            else:
                return False
        except:
            ReportBug.ReportBug()
        return False
    
    def changeTableType(self, _action):
        try:
            selectedType = Universals.getThisTableType(_action.objectName())
            if _action.isChecked() and Universals.tableType != selectedType:
                isChanged = self.changeTableTypeByType(selectedType)
                if isChanged==False:
                    _action.setChecked(False)
                    return False
            else:
                _action.setChecked(True)
        except:
            ReportBug.ReportBug()
    
    def getAllBarsStyleFromMySettings(self):
        Universals.MainWindow.TableToolsBar.setToolButtonStyle(int(Universals.MySettings["TableToolsBarButtonStyle"]))
        Universals.MainWindow.ToolsBar.setToolButtonStyle(int(Universals.MySettings["ToolsBarButtonStyle"]))
        if Universals.tableType=="2":
            Universals.MainWindow.PlayerBar.setToolButtonStyle(int(Universals.MySettings["PlayerBarButtonStyle"]))
            Universals.MainWindow.MusicOptionsBar.setToolButtonStyle(int(Universals.MySettings["MusicOptionsBarButtonStyle"]))
        elif Universals.tableType=="3":
            Universals.MainWindow.SubDirectoryOptionsBar.setToolButtonStyle(int(Universals.MySettings["SubDirectoryOptionsBarButtonStyle"]))
        elif Universals.tableType=="4":
            Universals.MainWindow.CoverOptionsBar.setToolButtonStyle(int(Universals.MySettings["CoverOptionsBarButtonStyle"]))
        elif Universals.tableType=="6":
            Universals.MainWindow.PlayerBar.setToolButtonStyle(int(Universals.MySettings["PlayerBarButtonStyle"]))
            Universals.MainWindow.AmarokMusicOptionsBar.setToolButtonStyle(int(Universals.MySettings["AmarokMusicOptionsBarButtonStyle"]))
        elif Universals.tableType=="8":
            Universals.MainWindow.PlayerBar.setToolButtonStyle(int(Universals.MySettings["PlayerBarButtonStyle"]))
            Universals.MainWindow.AmarokCopyOptionsBar.setToolButtonStyle(int(Universals.MySettings["AmarokCopyOptionsBarButtonStyle"]))
        
    def setAllBarsStyleToMySettings(self):
        Universals.setMySetting("TableToolsBarButtonStyle", Universals.MainWindow.TableToolsBar.toolButtonStyle())
        Universals.setMySetting("ToolsBarButtonStyle", Universals.MainWindow.ToolsBar.toolButtonStyle())
        if Universals.tableType=="2":
            Universals.setMySetting("PlayerBarButtonStyle", Universals.MainWindow.PlayerBar.toolButtonStyle())
            Universals.setMySetting("MusicOptionsBarButtonStyle", Universals.MainWindow.MusicOptionsBar.toolButtonStyle())
        elif Universals.tableType=="3":
            Universals.setMySetting("SubDirectoryOptionsBarButtonStyle", Universals.MainWindow.SubDirectoryOptionsBar.toolButtonStyle())
        elif Universals.tableType=="4":
            Universals.setMySetting("CoverOptionsBarButtonStyle", Universals.MainWindow.CoverOptionsBar.toolButtonStyle())
        elif Universals.tableType=="6":
            Universals.setMySetting("PlayerBarButtonStyle", Universals.MainWindow.PlayerBar.toolButtonStyle())
            Universals.setMySetting("AmarokMusicOptionsBarButtonStyle", Universals.MainWindow.AmarokMusicOptionsBar.toolButtonStyle())
        elif Universals.tableType=="8":
            Universals.setMySetting("PlayerBarButtonStyle", Universals.MainWindow.PlayerBar.toolButtonStyle())
            Universals.setMySetting("AmarokCopyOptionsBarButtonStyle", Universals.MainWindow.AmarokCopyOptionsBar.toolButtonStyle())
        
    def changeReNamerType(self, _action):
        try:
            if Universals.MainWindow.Table.checkUnSavedValues()==False:
                _action.setChecked(False)
                for x, typeName in enumerate(Variables.fileReNamerTypeNamesKeys):
                    if typeName == Universals.MySettings["fileReNamerType"]:
                        MainWindow.TableToolsBar.actsFileReNamerTypes[x].setChecked(True)
                return False
            for x, typeName in enumerate(Variables.fileReNamerTypeNamesKeys):
                if MainWindow.TableToolsBar.actsFileReNamerTypes[x].isChecked():
                    Universals.setMySetting("fileReNamerType", typeName)
            Universals.MainWindow.FileManager.makeRefresh()
            MApplication.processEvents()
        except:
            ReportBug.ReportBug()
        
