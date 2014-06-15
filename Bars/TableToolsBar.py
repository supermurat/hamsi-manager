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
from Core import Universals as uni
from Core.MyObjects import *
from Core import ReportBug
import Tables

class TableToolsBar(MToolBar):
    def __init__(self, _parent):
        MToolBar.__init__(self, _parent)
        _parent.addToolBar(Mt.TopToolBarArea,self)
        self.setWindowTitle(translate("TableToolsBar", "Table Tools"))
        self.setObjectName(translate("TableToolsBar", "Table Tools"))
        actgActionGroupTableTypes = MActionGroup(self)
        actgActionGroupTableTypes.setObjectName(translate("ToolsBar", "Table Types"))
        for (x, name) in var.tableTypesNames.items():
            a = actgActionGroupTableTypes.addAction(MIcon("Images:"+var.tableTypeIcons[x]), name)
            a.setCheckable(True)
            a.setObjectName(name)
            if uni.tableType== Tables.Tables.getThisTableType(name):
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
            self.actsFileReNamerTypes.append(MAction(MIcon("Images:"+buttonIcons[x]),str(name),actgActionGroupReNamerTypes))
            self.actsFileReNamerTypes[-1].setObjectName(str(name))
            self.actsFileReNamerTypes[x].setToolTip(str(str(translate("ToolsBar", "Renames files and folders in \"%s\" format.")) % (name)))
            self.actsFileReNamerTypes[x].setCheckable(True)
            actgActionGroupReNamerTypes.addAction(self.actsFileReNamerTypes[x])
            if uni.MySettings["fileReNamerType"]==var.fileReNamerTypeNamesKeys[x]:
                self.actsFileReNamerTypes[x].setChecked(True)
        if var.fileReNamerTypeNamesKeys.count(str(uni.MySettings["fileReNamerType"]))==0:
            self.actsFileReNamerTypes[0].setChecked(True)
        self.addActions(actgActionGroupReNamerTypes.actions())
        if uni.windowMode==var.windowModeKeys[1]:
            self.setIconSize(MSize(16,16))
        else:
            self.setIconSize(MSize(32,32))
        uni.MainWindow.Menu.mSpecialOptions = MMenu(translate("MenuBar", "Special Options"), self)
        uni.MainWindow.Menu.mSpecialOptions.setObjectName(translate("MenuBar", "Special Options"))
        uni.MainWindow.Menu.mSpecialOptions.setTitle(translate("MenuBar", "Special Options"))
        uni.MainWindow.Menu.mTableTools = MMenu(translate("MenuBar", "Table Tools"), self)
        uni.MainWindow.Menu.mTableTools.setObjectName(translate("MenuBar", "Table Tools"))
        uni.MainWindow.Menu.mTableTools.addMenu(uni.MainWindow.Menu.mSpecialOptions)
        uni.MainWindow.Menu.mTableTools.addActions(actgActionGroupTableTypes.actions())
        uni.MainWindow.Menu.mTableTools.addSeparator()
        uni.MainWindow.Menu.mTableTools.addActions(actgActionGroupReNamerTypes.actions())
        uni.MainWindow.Menu.insertMenu(uni.MainWindow.Menu.mTools.menuAction(), uni.MainWindow.Menu.mTableTools)
        #uni.MainWindow.Menu.mView.addActions(actgActionGroupTableTypes.actions())
        
