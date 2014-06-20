# # This file is part of HamsiManager.
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


from Core import Universals as uni
from Core.MyObjects import *
from Core import ReportBug
from Taggers import getSelectedTaggerTypeForReadName
import Amarok


class AmarokCopyOptionsBar(MToolBar):
    def __init__(self, _parent):
        MToolBar.__init__(self, _parent)
        self.isActiveChanging = True
        self.cbTagSourceTypeForMenu = None
        self.cbTagTargetTypeForMenu = None
        self.setWindowTitle(translate("AmarokCopyOptionsBar", "Music options"))
        self.setObjectName(translate("AmarokCopyOptionsBar", "Music options"))
        lblSourceDetails = MLabel(translate("AmarokCopyOptionsBar", "Read From : "))
        lblTargetDetails = MLabel(translate("AmarokCopyOptionsBar", "Write To : "))
        self.MusicTagSourceTypes = Amarok.getTagSourceTypes()
        self.cbTagSourceType = MComboBox(self)
        self.cbTagSourceType.addItems(self.MusicTagSourceTypes)
        musicTagTargetTypes = Amarok.getTagTargetTypes()
        self.MusicTagTargetTypes = []
        for mttt in musicTagTargetTypes:
            if mttt.find("Amarok") == -1:
                self.MusicTagTargetTypes.append(mttt)
        if Amarok.getSelectedTagTargetType("AmarokCopyTable") not in self.MusicTagTargetTypes:
            Amarok.setSelectedTagTargetType(self.MusicTagTargetTypes[0], "AmarokCopyTable")
        self.cbTagTargetType = MComboBox(self)
        self.cbTagTargetType.addItems(self.MusicTagTargetTypes)
        self.isActiveChanging = False
        self.cbTagSourceType.setCurrentIndex(
            self.cbTagSourceType.findText(Amarok.getSelectedTagSourseType("AmarokCopyTable")))
        self.cbTagTargetType.setCurrentIndex(
            self.cbTagTargetType.findText(Amarok.getSelectedTagTargetType("AmarokCopyTable")))
        self.isActiveChanging = True
        self.cbTagSourceType.setToolTip(translate("AmarokCopyOptionsBar", "You can select the ID3 tag source to read."))
        self.cbTagTargetType.setToolTip(
            translate("AmarokCopyOptionsBar", "You can select the ID3 tag target to write."))
        self.addWidget(lblSourceDetails)
        self.addWidget(self.cbTagSourceType)
        self.addWidget(lblTargetDetails)
        self.addWidget(self.cbTagTargetType)
        MObject.connect(self.cbTagSourceType, SIGNAL("currentIndexChanged(int)"), self.musicTagSourceTypeChanged)
        MObject.connect(self.cbTagTargetType, SIGNAL("currentIndexChanged(int)"), self.musicTagTargetTypeChanged)
        self.setIconSize(MSize(32, 32))

    def musicTagSourceTypeChanged(self, _action=None):
        try:
            selectedType = str(self.MusicTagSourceTypes[_action])
            if self.isActiveChanging:
                if getMainWindow().Table.checkUnSavedValues():
                    Amarok.setSelectedTagSourseType(selectedType, "AmarokCopyTable")
                    getMainWindow().Table.refreshForColumns()
                    getMainWindow().SpecialTools.refreshForColumns()
                    getMainWindow().Table.refresh(getMainWindow().FileManager.getCurrentDirectoryPath())
                self.isActiveChanging = False
                self.cbTagSourceType.setCurrentIndex(
                    self.cbTagSourceType.findText(Amarok.getSelectedTagSourseType("AmarokCopyTable")))
                if self.cbTagSourceTypeForMenu != None:
                    self.cbTagSourceTypeForMenu.setCurrentIndex(
                        self.cbTagSourceTypeForMenu.findText(Amarok.getSelectedTagSourseType("AmarokCopyTable")))
                self.isActiveChanging = True
        except:
            ReportBug.ReportBug()

    def musicTagTargetTypeChanged(self, _action=None):
        try:
            selectedType = str(self.MusicTagTargetTypes[_action])
            if self.isActiveChanging:
                Amarok.setSelectedTagTargetType(selectedType, "AmarokCopyTable")
                self.isActiveChanging = False
                self.cbTagTargetType.setCurrentIndex(
                    self.cbTagTargetType.findText(Amarok.getSelectedTagTargetType("AmarokCopyTable")))
                if self.cbTagTargetTypeForMenu != None:
                    self.cbTagTargetTypeForMenu.setCurrentIndex(
                        self.cbTagTargetTypeForMenu.findText(Amarok.getSelectedTagTargetType("AmarokCopyTable")))
                self.isActiveChanging = True
        except:
            ReportBug.ReportBug()

    def getSpecialOptions(self, _menu):
        self.cbTagSourceTypeForMenu = MComboBox(self)
        self.cbTagSourceTypeForMenu.addItems(self.MusicTagSourceTypes)
        self.cbTagTargetTypeForMenu = MComboBox(self)
        self.cbTagTargetTypeForMenu.addItems(self.MusicTagTargetTypes)
        self.isActiveChanging = False
        self.cbTagSourceTypeForMenu.setCurrentIndex(
            self.cbTagSourceTypeForMenu.findText(getSelectedTaggerTypeForReadName()))
        self.cbTagTargetTypeForMenu.setCurrentIndex(
            self.cbTagTargetTypeForMenu.findText(getSelectedTaggerTypeForReadName()))
        self.isActiveChanging = True
        MObject.connect(self.cbTagSourceTypeForMenu, SIGNAL("currentIndexChanged(int)"), self.musicTagSourceTypeChanged)
        MObject.connect(self.cbTagTargetTypeForMenu, SIGNAL("currentIndexChanged(int)"), self.musicTagTargetTypeChanged)
        wactSourceLabel = MWidgetAction(_menu)
        wactSourceLabel.setDefaultWidget(MLabel(str(translate("AmarokCopyOptionsBar", "Read From : "))))
        wactTargetLabel = MWidgetAction(_menu)
        wactTargetLabel.setDefaultWidget(MLabel(str(translate("AmarokCopyOptionsBar", "Write To : "))))
        wactSource = MWidgetAction(_menu)
        wactSource.setDefaultWidget(self.cbTagSourceTypeForMenu)
        wactTarget = MWidgetAction(_menu)
        wactTarget.setDefaultWidget(self.cbTagTargetTypeForMenu)
        _menu.addAction(wactSourceLabel)
        _menu.addAction(wactSource)
        _menu.addAction(wactTargetLabel)
        _menu.addAction(wactTarget)
        
