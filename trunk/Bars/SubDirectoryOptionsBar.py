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


from Core import Universals as uni
from Core.MyObjects import *
from Core import ReportBug


class SubDirectoryOptionsBar(MToolBar):
    def __init__(self, _parent):
        MToolBar.__init__(self, _parent)
        self.isActiveChanging = True
        self.cbSubDirectoryDeepForMenu = None
        self.setWindowTitle(translate("SubDirectoryOptionsBar", "Sub Directory Options"))
        self.setObjectName(translate("SubDirectoryOptionsBar", "Sub Directory Options"))
        lblDetails = translate("SubDirectoryOptionsBar",
                               "You can select sub directory deep.<br><font color=blue>You can select \"-1\" for all sub directories.</font>")
        lblSubDirectoryDeep = MLabel(str(translate("SubDirectoryOptionsBar", "Deep") + " : "))
        self.SubDirectoryDeeps = [str(x) for x in range(-1, 10)]
        self.cbSubDirectoryDeep = MComboBox(self)
        self.cbSubDirectoryDeep.addItems(self.SubDirectoryDeeps)
        self.isActiveChanging = False
        self.cbSubDirectoryDeep.setCurrentIndex(self.cbSubDirectoryDeep.findText(uni.MySettings["subDirectoryDeep"]))
        self.isActiveChanging = True
        self.cbSubDirectoryDeep.setToolTip(lblDetails)
        pnlSubDirectoryDeep = MWidget()
        hblSubDirectoryDeep = MHBoxLayout(pnlSubDirectoryDeep)
        hblSubDirectoryDeep.addWidget(lblSubDirectoryDeep)
        hblSubDirectoryDeep.addWidget(self.cbSubDirectoryDeep)
        pnlSubDirectoryDeep.setLayout(hblSubDirectoryDeep)
        self.addWidget(pnlSubDirectoryDeep)
        MObject.connect(self.cbSubDirectoryDeep, SIGNAL("currentIndexChanged(int)"), self.subDirectoryDeepChanged)
        self.setIconSize(MSize(32, 32))

    def subDirectoryDeepChanged(self, _action=None):
        try:
            selectedDeep = str(self.SubDirectoryDeeps[_action])
            if self.isActiveChanging:
                if getMainWindow().Table.checkUnSavedValues():
                    uni.setMySetting("subDirectoryDeep", int(selectedDeep))
                    getMainWindow().Table.refreshForColumns()
                    getMainWindow().SpecialTools.refreshForColumns()
                    getMainWindow().Table.refresh(getMainWindow().FileManager.getCurrentDirectoryPath())
                self.isActiveChanging = False
                self.cbSubDirectoryDeep.setCurrentIndex(
                    self.cbSubDirectoryDeep.findText(str(uni.MySettings["subDirectoryDeep"])))
                if self.cbSubDirectoryDeepForMenu != None:
                    self.cbSubDirectoryDeepForMenu.setCurrentIndex(
                        self.cbSubDirectoryDeepForMenu.findText(str(uni.MySettings["subDirectoryDeep"])))
                self.isActiveChanging = True
        except:
            ReportBug.ReportBug()

    def getSpecialOptions(self, _menu):
        self.cbSubDirectoryDeepForMenu = MComboBox(self)
        self.cbSubDirectoryDeepForMenu.addItems(self.SubDirectoryDeeps)
        self.isActiveChanging = False
        self.cbSubDirectoryDeepForMenu.setCurrentIndex(
            self.cbSubDirectoryDeepForMenu.findText(str(uni.MySettings["subDirectoryDeep"])))
        self.isActiveChanging = True
        MObject.connect(self.cbSubDirectoryDeepForMenu, SIGNAL("currentIndexChanged(int)"),
                        self.subDirectoryDeepChanged)
        wactLabel = MWidgetAction(_menu)
        wactLabel.setObjectName(str(translate("SubDirectoryOptionsBar", "Label Deep") + " : "))
        wactLabel.setDefaultWidget(MLabel(str(translate("SubDirectoryOptionsBar", "Deep") + " : ")))
        wact = MWidgetAction(_menu)
        wact.setObjectName(str(translate("SubDirectoryOptionsBar", "Deep") + " : "))
        wact.setDefaultWidget(self.cbSubDirectoryDeepForMenu)
        _menu.addAction(wactLabel)
        _menu.addAction(wact)
        
