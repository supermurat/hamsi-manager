## This file is part of HamsiManager.
## 
## Copyright (c) 2010 Murat Demir <mopened@gmail.com>      
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


import Variables
from MyObjects import *
import Universals
import Dialogs
import InputOutputs
import Options
import Organizer
import Amarok
from Amarok import Commands

class FilterWidget(MWidget):
    def __init__(self, _parent, _filterKeyName):
        MWidget.__init__(self, _parent)
        vblMain = MVBoxLayout(self)
        self.filterKeyName = _filterKeyName
        lblFilter = MLabel(translate("Amarok/FilterWidget", "Filter"))
        self.leFilter = MLineEdit(Universals.MySettings[self.filterKeyName])
        self.pbtnEditFilter = MPushButton(translate("Amarok/FilterDialog", "Edit"))
        self.pbtnApply = MPushButton(translate("Amarok/FilterDialog", "Apply"))
        _parent.connect(self.pbtnEditFilter,SIGNAL("clicked()"),self.editFilter)
        _parent.connect(self.pbtnApply,SIGNAL("clicked()"),self.apply)
        self.hblBox = MHBoxLayout()
        self.hblBox.addWidget(lblFilter)
        self.hblBox.addWidget(self.leFilter)
        self.hblBox.addWidget(self.pbtnEditFilter)
        self.hblBox.addWidget(self.pbtnApply)
        vblMain.addLayout(self.hblBox)
        self.setLayout(vblMain)
        
    def editFilter(self):
        try:
            self.dFilterEditor = FilterEditor(self, self.filterKeyName)
            self.dFilterEditor.show()
        except:
            import ReportBug
            error = ReportBug.ReportBug()
            error.show() 
        
    def apply(self):
        try:
            Universals.setMySetting(self.filterKeyName, str(self.leFilter.text()))
            Universals.MainWindow.Table.refresh(Universals.MainWindow.FileManager.getCurrentDirectoryPath())
        except:
            import ReportBug
            error = ReportBug.ReportBug()
            error.show() 

class FilterEditor(MDialog):
    def __init__(self, _parent, _filterKeyName):
        MDialog.__init__(self, _parent)
        self.fWidget = _parent
        if Universals.isActivePyKDE4==True:
            self.setButtons(MDialog.NoDefault)
        pnlMain = MWidget(self)
        vblMain = MVBoxLayout(pnlMain)
        self.filterKeyName = _filterKeyName
        lblFilter = MLabel(translate("Amarok/FilterEditor", "Filter"))
        self.leFilter = MLineEdit(Universals.MySettings[self.filterKeyName])
        self.pbtnApply = MPushButton(translate("Amarok/FilterEditor", "Apply"))
        _parent.connect(self.pbtnApply,SIGNAL("clicked()"),self.apply)
        self.hblBox = MHBoxLayout()
        self.hblBox.addWidget(lblFilter)
        self.hblBox.addWidget(self.leFilter)
        self.hblBox.addWidget(self.pbtnApply)
        vblMain.addLayout(self.hblBox)
        self.setLayout(vblMain)
        if Universals.isActivePyKDE4==True:
            self.setMainWidget(pnlMain)
        else:
            self.setLayout(vblMain)
        self.setWindowTitle(translate("Amarok/FilterEditor", "Edit Filter"))
        self.show()
        self.setWindowIcon(MIcon("Images:amarokFilter.png"))
        
    def apply(self):
        try:
            self.fWidget.leFilter.setText(self.leFilter.text())
            self.fWidget.apply()
        except:
            import ReportBug
            error = ReportBug.ReportBug()
            error.show() 
        
        
            
    
            
            
            
            
            
            

