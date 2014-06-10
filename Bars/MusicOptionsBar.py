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
from Taggers import getTaggerTypesName, getSelectedTaggerTypeForReadName, setSelectedTaggerTypeForReadName, getSelectedTaggerTypeForWriteName, setSelectedTaggerTypeForWriteName

class MusicOptionsBar(MToolBar):

    def __init__(self, _parent):
        MToolBar.__init__(self, _parent)
        self.isActiveChanging = True
        self.cbMusicTagTypeForReadForMenu = None
        self.cbMusicTagTypeForWriteForMenu = None
        self.setWindowTitle(translate("MusicOptionsBar", "Music options"))
        self.setObjectName(translate("MusicOptionsBar", "Music options"))
        lblMusicTagTypeForRead = MLabel(translate("MusicOptionsBar", "Read From : "))
        lblMusicTagTypeForWrite = MLabel(translate("MusicOptionsBar", "Write To : "))
        self.MusicTagTypes = getTaggerTypesName()
        self.cbMusicTagTypeForRead = MComboBox(self)
        self.cbMusicTagTypeForRead.addItems(self.MusicTagTypes)
        self.cbMusicTagTypeForWrite = MComboBox(self)
        self.cbMusicTagTypeForWrite.addItems(self.MusicTagTypes)
        self.isActiveChanging = False
        self.cbMusicTagTypeForRead.setCurrentIndex(self.cbMusicTagTypeForRead.findText(getSelectedTaggerTypeForReadName()))
        self.cbMusicTagTypeForWrite.setCurrentIndex(self.cbMusicTagTypeForWrite.findText(getSelectedTaggerTypeForWriteName()))
        self.isActiveChanging = True
        self.cbMusicTagTypeForRead.setToolTip(translate("MusicOptionsBar", "You can select the ID3 tag source you want to read.<br><font color=blue>ID3 V2 is recommended.</font>"))
        self.cbMusicTagTypeForWrite.setToolTip(translate("MusicOptionsBar", "You can select the ID3 tag target you want to write.<br><font color=blue>ID3 V2 is recommended.</font>"))
        self.addWidget(lblMusicTagTypeForRead)
        self.addWidget(self.cbMusicTagTypeForRead)
        self.addWidget(lblMusicTagTypeForWrite)
        self.addWidget(self.cbMusicTagTypeForWrite)
        MObject.connect(self.cbMusicTagTypeForRead, SIGNAL("currentIndexChanged(int)"), self.musicTagTypeForReadChanged)
        MObject.connect(self.cbMusicTagTypeForWrite, SIGNAL("currentIndexChanged(int)"), self.musicTagTypeForWriteChanged)
        self.setIconSize(MSize(32,32))
    
    def musicTagTypeForReadChanged(self, _action=None):
        try:
            selectedType = str(self.MusicTagTypes[_action])
            if self.isActiveChanging:
                if Universals.MainWindow.Table.checkUnSavedValues()==True:
                    setSelectedTaggerTypeForReadName(selectedType)
                    Universals.MainWindow.Table.refreshForColumns()
                    Universals.MainWindow.SpecialTools.refreshForColumns()
                    Universals.MainWindow.Table.refresh(Universals.MainWindow.FileManager.getCurrentDirectoryPath())
                self.isActiveChanging = False
                self.cbMusicTagTypeForRead.setCurrentIndex(self.cbMusicTagTypeForRead.findText(getSelectedTaggerTypeForReadName()))
                if self.cbMusicTagTypeForReadForMenu != None:
                    self.cbMusicTagTypeForReadForMenu.setCurrentIndex(self.cbMusicTagTypeForReadForMenu.findText(getSelectedTaggerTypeForReadName()))
                self.isActiveChanging = True
        except:
            ReportBug.ReportBug()
    
    def musicTagTypeForWriteChanged(self, _action=None):
        try:
            selectedType = str(self.MusicTagTypes[_action])
            if self.isActiveChanging:
                if Universals.MainWindow.Table.checkUnSavedValues()==True:
                    setSelectedTaggerTypeForWriteName(selectedType)
                self.isActiveChanging = False
                self.cbMusicTagTypeForWrite.setCurrentIndex(self.cbMusicTagTypeForWrite.findText(getSelectedTaggerTypeForWriteName()))
                if self.cbMusicTagTypeForWriteForMenu != None:
                    self.cbMusicTagTypeForWriteForMenu.setCurrentIndex(self.cbMusicTagTypeForWriteForMenu.findText(getSelectedTaggerTypeForWriteName()))
                self.isActiveChanging = True
        except:
            ReportBug.ReportBug()
        
    def getSpecialOptions(self, _menu):
        self.cbMusicTagTypeForReadForMenu = MComboBox(self)
        self.cbMusicTagTypeForWriteForMenu = MComboBox(self)
        self.cbMusicTagTypeForReadForMenu.setToolTip(translate("MusicOptionsBar", "You can select the ID3 tag source you want to read.<br><font color=blue>ID3 V2 is recommended.</font>"))
        self.cbMusicTagTypeForWriteForMenu.setToolTip(translate("MusicOptionsBar", "You can select the ID3 tag target you want to write.<br><font color=blue>ID3 V2 is recommended.</font>"))
        self.cbMusicTagTypeForReadForMenu.addItems(self.MusicTagTypes)
        self.cbMusicTagTypeForWriteForMenu.addItems(self.MusicTagTypes)
        self.isActiveChanging = False
        self.cbMusicTagTypeForReadForMenu.setCurrentIndex(self.cbMusicTagTypeForReadForMenu.findText(getSelectedTaggerTypeForReadName()))
        self.cbMusicTagTypeForWriteForMenu.setCurrentIndex(self.cbMusicTagTypeForWriteForMenu.findText(getSelectedTaggerTypeForWriteName()))
        self.isActiveChanging = True
        MObject.connect(self.cbMusicTagTypeForReadForMenu, SIGNAL("currentIndexChanged(int)"), self.musicTagTypeForReadChanged)
        MObject.connect(self.cbMusicTagTypeForWriteForMenu, SIGNAL("currentIndexChanged(int)"), self.musicTagTypeForWriteChanged)
        wactLabelForRead = MWidgetAction(_menu)
        wactLabelForRead.setDefaultWidget(MLabel(trForUI(translate("MusicOptionsBar", "Read From : "))))
        wactLabelForWrite = MWidgetAction(_menu)
        wactLabelForWrite.setDefaultWidget(MLabel(trForUI(translate("MusicOptionsBar", "Write To : "))))
        wactForRead = MWidgetAction(_menu)
        wactForWrite = MWidgetAction(_menu)
        wactForRead.setDefaultWidget(self.cbMusicTagTypeForReadForMenu)
        wactForWrite.setDefaultWidget(self.cbMusicTagTypeForWriteForMenu)
        _menu.addAction(wactLabelForRead)
        _menu.addAction(wactForRead)
        _menu.addAction(wactLabelForWrite)
        _menu.addAction(wactForWrite)
        
