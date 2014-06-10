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
from Core import Universals
from Core.MyObjects import *
from Core import ReportBug

class ToolsBar(MToolBar):
    def __init__(self, _parent):
        MToolBar.__init__(self, _parent)
        _parent.addToolBar(Mt.TopToolBarArea,self)
        self.setWindowTitle(translate("ToolsBar", "Tools"))
        self.setObjectName(translate("ToolsBar", "Tools"))
        self.clearEmptyDirectories = MAction(MIcon("Images:clearEmptyDirectories.png"),
                                                translate("ToolsBar", "Clear Empty Directories"),self)
        self.clearEmptyDirectories.setObjectName(translate("ToolsBar", "Clear Empty Directories"))
        self.clearEmptyDirectories.setToolTip(translate("ToolsBar", "Clears the folder contents based on the criteria set."))
        if Variables.isActiveDirectoryCover:
            self.actCheckIcon = MAction(MIcon("Images:checkIcon.png"),
                                                translate("ToolsBar", "Check Icon"),self)
            self.actCheckIcon.setObjectName(translate("ToolsBar", "Check Icon"))
            self.actCheckIcon.setToolTip(translate("ToolsBar", "Checks the icon for the folder you are currently in."))
        self.actHash = MAction(MIcon("Images:hash.png"),
                                                translate("ToolsBar", "Hash"),self)
        self.actHash.setObjectName(translate("ToolsBar", "Hash"))
        self.actHash.setToolTip(translate("ToolsBar", "Hash manager"))
        self.actPack = MAction(MIcon("Images:pack.png"),
                                                translate("ToolsBar", "Pack"),self)
        self.actPack.setObjectName(translate("ToolsBar", "Pack"))
        self.actPack.setToolTip(translate("ToolsBar", "Packs the current folder."))
        self.actFileTree = MAction(MIcon("Images:fileTree.png"),
                                                translate("ToolsBar", "File Tree"),self)
        self.actFileTree.setObjectName(translate("ToolsBar", "File Tree"))
        self.actFileTree.setToolTip(translate("ToolsBar", "Get file tree of current folder."))
        self.actClear = MAction(MIcon("Images:clear.png"),
                                                translate("ToolsBar", "Clear"),self)
        self.actClear.setObjectName(translate("ToolsBar", "Clear"))
        self.actClear.setToolTip(translate("ToolsBar", "Clears the current folder."))
        self.actTextCorrector = MAction(MIcon("Images:textCorrector.png"),
                                                translate("ToolsBar", "Text Corrector"),self)
        self.actTextCorrector.setObjectName(translate("ToolsBar", "Text Corrector"))
        self.actTextCorrector.setToolTip(translate("ToolsBar", "Corrects text files."))
        self.actRemoveOnlySubFiles = MAction(MIcon("Images:removeOnlySubFiles.png"),
                                                translate("ToolsBar", "Remove Sub Files"),self)
        self.actRemoveOnlySubFiles.setObjectName(translate("ToolsBar", "Remove Sub Files"))
        self.actRemoveOnlySubFiles.setToolTip(translate("ToolsBar", "Remove only all sub files.Do not will remove directory and subfolders."))
        self.actSearch = MAction(MIcon("Images:search.png"),
                                                translate("ToolsBar", "Search"),self)
        self.actSearch.setObjectName(translate("ToolsBar", "Search"))
        self.actSearch.setToolTip(translate("ToolsBar", "Special search tool"))
        self.actScriptManager = MAction(MIcon("Images:scriptManager.png"),
                                                translate("ToolsBar", "Script Manager"),self)
        self.actScriptManager.setObjectName(translate("ToolsBar", "Script Manager"))
        self.actScriptManager.setToolTip(translate("ToolsBar", "You can do what you want."))
        if Universals.getBoolValue("isSaveActions"):
            self.actLastActions = MAction(MIcon("Images:lastActions.png"),
                                                    translate("ToolsBar", "Show Last Actions"),self)
            self.actLastActions.setObjectName(translate("ToolsBar", "Show Last Actions"))
            self.actLastActions.setToolTip(translate("ToolsBar", "You can see last actions."))
        if Variables.isActiveAmarok and Universals.getBoolValue("amarokIsUseHost")==False:
            self.actAmarokEmbeddedDBConfigurator = MAction(MIcon("Images:amarokEmbeddedDBConfigurator.png"),
                                                    translate("ToolsBar", "Amarok Embedded Database Configurator"),self)
            self.actAmarokEmbeddedDBConfigurator.setObjectName(translate("ToolsBar", "Amarok Embedded Database Configurator"))
            self.actAmarokEmbeddedDBConfigurator.setToolTip(translate("ToolsBar", "Packs the current folder."))
        self.addAction(self.actHash)
        self.addAction(self.actPack)
        self.addAction(self.actFileTree)
        self.addAction(self.actClear)
        self.addAction(self.actTextCorrector)
        self.addAction(self.actSearch)
        self.addAction(self.actScriptManager)
        if Universals.getBoolValue("isSaveActions"):
            self.addAction(self.actLastActions)
        if Variables.isActiveAmarok and Universals.getBoolValue("amarokIsUseHost")==False:
            self.addAction(self.actAmarokEmbeddedDBConfigurator)
        self.addSeparator()
        self.addAction(self.clearEmptyDirectories)
        self.addAction(self.actRemoveOnlySubFiles)
        if Variables.isActiveDirectoryCover:
            self.addAction(self.actCheckIcon)
        if Universals.windowMode==Variables.windowModeKeys[1]:
            self.setIconSize(MSize(16,16))
        else:
            self.setIconSize(MSize(32,32))
        Universals.MainWindow.Menu.mTools = MMenu(translate("MenuBar", "Tools"), self)
        Universals.MainWindow.Menu.mTools.setObjectName(translate("MenuBar", "Tools"))
        Universals.MainWindow.Menu.mTools.addAction(self.actHash)
        Universals.MainWindow.Menu.mTools.addAction(self.actPack)
        Universals.MainWindow.Menu.mTools.addAction(self.actFileTree)
        Universals.MainWindow.Menu.mTools.addAction(self.actClear)
        Universals.MainWindow.Menu.mTools.addAction(self.actTextCorrector)
        Universals.MainWindow.Menu.mTools.addAction(self.actSearch)
        Universals.MainWindow.Menu.mTools.addAction(self.actScriptManager)
        if Universals.getBoolValue("isSaveActions"):
            Universals.MainWindow.Menu.mTools.addAction(self.actLastActions)
        if Variables.isActiveAmarok and Universals.getBoolValue("amarokIsUseHost")==False:
            Universals.MainWindow.Menu.mTools.addAction(self.actAmarokEmbeddedDBConfigurator)
        Universals.MainWindow.Menu.mTools.addSeparator()
        Universals.MainWindow.Menu.mTools.addAction(self.clearEmptyDirectories)
        Universals.MainWindow.Menu.mTools.addAction(self.actRemoveOnlySubFiles)
        if Variables.isActiveDirectoryCover:
            Universals.MainWindow.Menu.mTools.addAction(self.actCheckIcon)
        Universals.MainWindow.Menu.insertMenu(Universals.MainWindow.Menu.mSettings.menuAction(), Universals.MainWindow.Menu.mTools)
        self.createScriptsMenu(_parent)
    
    def createScriptsMenu(self, _parent):
        Universals.MainWindow.Menu.mScripts = MMenu(translate("MenuBar", "Scripts"), self)
        Universals.MainWindow.Menu.mScripts.setObjectName(translate("MenuBar", "Scripts"))
        from Core import Scripts
        _parent.scriptList = Scripts.getScriptList()
        for scriptName in _parent.scriptList:
            actScript = MAction(trForUI(scriptName), Universals.MainWindow.Menu.mScripts)
            actScript.setObjectName(trForUI(scriptName))
            actScript.setToolTip(trForUI(str(translate("ToolsBar", "Execute \"%s\" Named Script")) % scriptName))
            Universals.MainWindow.Menu.mScripts.addAction(actScript)
        actScriptManager = MAction(MIcon("Images:scriptManager.png"),
                                                translate("ToolsBar", "Script Manager"),self)
        actScriptManager.setObjectName(translate("ToolsBar", "Script Manager"))
        actScriptManager.setToolTip(translate("ToolsBar", "You can do what you want."))
        Universals.MainWindow.Menu.mScripts.addAction(actScriptManager)
        Universals.MainWindow.Menu.insertMenu(Universals.MainWindow.Menu.mSettings.menuAction(), Universals.MainWindow.Menu.mScripts)
        
