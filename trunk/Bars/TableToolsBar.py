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

class TableToolsBar(MToolBar):
    def __init__(self, _parent):
        MToolBar.__init__(self, _parent)
        _parent.addToolBar(Mt.TopToolBarArea,self)
        self.setWindowTitle(translate("TableToolsBar", "Table Tools"))
        self.setObjectName(translate("TableToolsBar", "Table Tools"))
        actgActionGroupTableTypes = MActionGroup(self)
        actgActionGroupTableTypes.setObjectName(translate("ToolsBar", "Table Types"))
        for x, name in enumerate(Variables.tableTypesNames):
            a = actgActionGroupTableTypes.addAction(MIcon("Images:"+Variables.tableTypeIcons[x]), name)
            a.setCheckable(True)
            a.setObjectName(name)
            if Universals.tableType==Universals.getThisTableType(name):
                a.setChecked(True)
        self.addActions(actgActionGroupTableTypes.actions())
        self.addSeparator()
        self.fileReNamerTypeNames = [str(translate("ToolsBar", "Personal Computer")), 
                                    str(translate("ToolsBar", "Web Server")), 
                                    str(translate("ToolsBar", "Removable Media"))]
        buttonIcons = ["personalComputer.png", "webServer.png", "removableMedia.png"]
        actgActionGroupReNamerTypes = MActionGroup(self)
        actgActionGroupReNamerTypes.setObjectName(translate("ToolsBar", "File Renamer Types"))
        self.actsFileReNamerTypes = []
        for x, name in enumerate(self.fileReNamerTypeNames):
            self.actsFileReNamerTypes.append(MAction(MIcon("Images:"+buttonIcons[x]),trForUI(name),actgActionGroupReNamerTypes))
            self.actsFileReNamerTypes[-1].setObjectName(trForUI(name))
            self.actsFileReNamerTypes[x].setToolTip(trForUI(str(translate("ToolsBar", "Renames files and folders in \"%s\" format.")) % (name)))
            self.actsFileReNamerTypes[x].setCheckable(True)
            actgActionGroupReNamerTypes.addAction(self.actsFileReNamerTypes[x])
            if Universals.MySettings["fileReNamerType"]==Variables.fileReNamerTypeNamesKeys[x]:
                self.actsFileReNamerTypes[x].setChecked(True)
        if Variables.fileReNamerTypeNamesKeys.count(str(Universals.MySettings["fileReNamerType"]))==0:
            self.actsFileReNamerTypes[0].setChecked(True)
        self.addActions(actgActionGroupReNamerTypes.actions())
        if Universals.windowMode==Variables.windowModeKeys[1]:
            self.setIconSize(MSize(16,16))
        else:
            self.setIconSize(MSize(32,32))
        Universals.MainWindow.Menu.mSpecialOptions = MMenu(translate("MenuBar", "Special Options"), self)
        Universals.MainWindow.Menu.mSpecialOptions.setObjectName(translate("MenuBar", "Special Options"))
        Universals.MainWindow.Menu.mSpecialOptions.setTitle(translate("MenuBar", "Special Options"))
        Universals.MainWindow.Menu.mTableTools = MMenu(translate("MenuBar", "Table Tools"), self)
        Universals.MainWindow.Menu.mTableTools.setObjectName(translate("MenuBar", "Table Tools"))
        Universals.MainWindow.Menu.mTableTools.addMenu(Universals.MainWindow.Menu.mSpecialOptions)
        Universals.MainWindow.Menu.mTableTools.addActions(actgActionGroupTableTypes.actions())
        Universals.MainWindow.Menu.mTableTools.addSeparator()
        Universals.MainWindow.Menu.mTableTools.addActions(actgActionGroupReNamerTypes.actions())
        Universals.MainWindow.Menu.insertMenu(Universals.MainWindow.Menu.mTools.menuAction(), Universals.MainWindow.Menu.mTableTools)
        #Universals.MainWindow.Menu.mView.addActions(actgActionGroupTableTypes.actions())
        