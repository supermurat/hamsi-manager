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


from Core import Universals as uni
from Core.MyObjects import *
from Core import ReportBug
import Tables


class TableToolsBar(MToolBar):
    def __init__(self, _parent):
        MToolBar.__init__(self, _parent)
        _parent.addToolBar(Mt.TopToolBarArea, self)
        self.setWindowTitle(translate("TableToolsBar", "Table Tools"))
        self.setObjectName(translate("TableToolsBar", "Table Tools"))
        actgActionGroupTableTypes = MActionGroup(self)
        actgActionGroupTableTypes.setObjectName(translate("ToolsBar", "Table Types"))
        for x in uni.tableTypeOrder:
            if x in uni.tableTypesNames.keys():
                name = uni.tableTypesNames[x]
                a = actgActionGroupTableTypes.addAction(MIcon("Images:" + uni.tableTypeIcons[x]), name)
                a.setCheckable(True)
                a.setObjectName(name)
                if uni.tableType == Tables.Tables.getThisTableType(name):
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
            self.actsFileReNamerTypes.append(
                MAction(MIcon("Images:" + buttonIcons[x]), str(name), actgActionGroupReNamerTypes))
            self.actsFileReNamerTypes[-1].setObjectName(str(name))
            self.actsFileReNamerTypes[x].setToolTip(
                str(str(translate("ToolsBar", "Renames files and folders in \"%s\" format.")) % (name)))
            self.actsFileReNamerTypes[x].setCheckable(True)
            actgActionGroupReNamerTypes.addAction(self.actsFileReNamerTypes[x])
            if uni.MySettings["fileReNamerType"] == uni.fileReNamerTypeNamesKeys[x]:
                self.actsFileReNamerTypes[x].setChecked(True)
        if uni.fileReNamerTypeNamesKeys.count(str(uni.MySettings["fileReNamerType"])) == 0:
            self.actsFileReNamerTypes[0].setChecked(True)
        self.addActions(actgActionGroupReNamerTypes.actions())
        self.setIconSize(MSize(16, 16))
        getMainWindow().Menu.mTableTools = MMenu(translate("MenuBar", "Table Tools"), self)
        getMainWindow().Menu.mTableTools.setObjectName(translate("MenuBar", "Table Tools"))
        getMainWindow().Menu.mTableTools.addActions(actgActionGroupTableTypes.actions())
        getMainWindow().Menu.mTableTools.addSeparator()
        getMainWindow().Menu.mTableTools.addActions(actgActionGroupReNamerTypes.actions())
        getMainWindow().Menu.insertMenu(getMainWindow().Menu.mTools.menuAction(), getMainWindow().Menu.mTableTools)
        #getMainWindow().Menu.mView.addActions(actgActionGroupTableTypes.actions())
        
