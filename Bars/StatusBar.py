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

class StatusBar(MStatusBar):
    
    def __init__(self, _parent):
        MStatusBar.__init__(self, _parent)
        if var.isRunningAsRoot():
            lblInfo = MLabel(str("<span style=\"color: #FF0000\">" + translate("StatusBar", "Hamsi Manager running as root")+"</span>"))
            self.addWidget(lblInfo)
        self.connectionToCancel = None
        self.lblInfo = MLabel("")
        self.hideInfo()
        self.addWidget(self.lblInfo)
        self.prgbState = MProgressBar()
        self.prgbState.setMinimumWidth(200)
        self.pbtnCancel = MPushButton(translate("StatusBar", "Cancel"))
        self.prgbState.setVisible(False)
        self.pbtnCancel.setVisible(False)
        self.addWidget(self.prgbState)
        self.addWidget(self.pbtnCancel)
        self.addWidget(MLabel(""), 100)
        self.lblTableInfo = MLabel("")
        self.lblImportantInfo = MLabel("")
        self.lblSelectionInfo = MLabel("")
        self.addWidget(self.lblTableInfo)
        self.addWidget(self.lblImportantInfo)
        self.addWidget(self.lblSelectionInfo)
        self.fillSelectionInfo()
    
    def showInfo(self, _info):
        self.lblInfo.setText(_info)
    
    def hideInfo(self):
        self.lblInfo.setText("")
    
    def clearTableInfo(self):
        self.lblTableInfo.setText("")
    
    def clearImportantInfo(self):
        self.lblImportantInfo.setText("")
    
    def clearSelectionInfo(self):
        self.lblSelectionInfo.setText("")
    
    def setTableInfo(self, _info):
        self.lblTableInfo.setText(str(_info))
        uni.MainWindow.setWindowTitle("Hamsi Manager " + var.version + " - " + str(_info))
    
    def setImportantInfo(self, _info):
        self.lblImportantInfo.setText(str("<span style=\"color: #FF0000\">" + _info + "</span>"))
    
    def setSelectionInfo(self, _info):
        self.lblSelectionInfo.setText(str("<span style=\"color: #FF0000\">" + _info + "</span>"))
            
    def fillSelectionInfo(self):
        if uni.getBoolValue("isChangeAll"):
            self.setSelectionInfo(translate("Tables", "All informations will be changed"))
        else:
            if uni.getBoolValue("isChangeSelected"):
                self.setSelectionInfo(translate("Tables", "Just selected informations will be changed"))
            else:
                self.setSelectionInfo(translate("Tables", "Just unselected informations will be changed"))
        
    def showState(self, _title, _value=0, _maxValue=100, _isShowCancel=False, _connectToCancel=None):
        MApplication.processEvents()
        if uni.MainWindow.isLockedMainForm==False:
            uni.MainWindow.lockForm()
        self.prgbState.setVisible(True)
        if _isShowCancel:
            if self.connectionToCancel!=None:
                MObject.disconnect(self.pbtnCancel, SIGNAL("clicked()"), self.connectionToCancel)
            if _connectToCancel==None:
                MObject.connect(self.pbtnCancel, SIGNAL("clicked()"), uni.cancelThreadAction)
                self.connectionToCancel = uni.cancelThreadAction
            else:
                MObject.connect(self.pbtnCancel, SIGNAL("clicked()"), _connectToCancel)
                self.connectionToCancel = _connectToCancel
            self.pbtnCancel.setVisible(True)
        else:
            self.pbtnCancel.setVisible(False)
        self.prgbState.setRange(0, _maxValue)
        self.prgbState.setValue(_value)
        self.showInfo(_title+" ( "+str(_value)+" / "+str(_maxValue)+" )")
        if _value==_maxValue:
            self.hideInfo()
            self.prgbState.setVisible(False)
            self.pbtnCancel.setVisible(False)
            self.prgbState.setRange(0, 100)
            if uni.MainWindow.isLockedMainForm:
                uni.MainWindow.unlockForm()
        
