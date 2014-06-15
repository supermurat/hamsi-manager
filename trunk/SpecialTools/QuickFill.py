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
from Core import Organizer
from Core import Universals as uni
from Core.MyObjects import *
import Tables
from Core import Dialogs
import sys
from Core import ReportBug
import Databases

class QuickFill(MWidget):
    def __init__(self, _parent):
        MWidget.__init__(self, _parent)
        self.specialTools = _parent
        self.lblColumns = []
        self.leColumns = []
        self.tmrFillAfter = None
        self.gridLayout = MGridLayout()
        self.setLayout(self.gridLayout)
        
    def showAdvancedSelections(self):
        for x in range(8, len(self.leColumns)):
            self.lblColumns[x].show()
            self.leColumns[x].show()
    
    def hideAdvancedSelections(self):
        for x in range(8, len(self.leColumns)):
            self.lblColumns[x].hide()
            self.leColumns[x].hide()
    
    def checkCompleters(self):
        for x in range(0, len(self.leColumns)):
            Databases.CompleterTable.insert(self.lblColumns[x].text(), self.leColumns[x].text())
    
    def reFillCompleters(self):
        for x in range(0, len(self.leColumns)):
            setCompleter(self.leColumns[x], self.lblColumns[x].text())
        
    def fillAfter(self, _searchValue=""):
        try:
            self.fillFrom = self.sender()
            if self.tmrFillAfter!= None:
                self.tmrFillAfter.stop()
                self.tmrFillAfter.deleteLater()
            self.tmrFillAfter = MTimer(self)
            self.tmrFillAfter.setSingleShot(True)
            self.connect(self.tmrFillAfter,SIGNAL("timeout()"), self.fill)
            self.tmrFillAfter.start(1000)
        except:
            from Core import ReportBug
            ReportBug.ReportBug()
            
    def fill(self, _searchValue=""):
        try:
            self.checkCompleters()
            self.reFillCompleters()
            uni.MainWindow.Table.createHistoryPoint()
            self.apply()
        except:
            from Core import ReportBug
            ReportBug.ReportBug()
            
    def apply(self):
        _newString = str(self.fillFrom.text())
        uni.MainWindow.Table.isAskShowHiddenColumn = True
        for No, columnName in enumerate(uni.MainWindow.Table.tableColumns):
            if str(self.fillFrom.objectName()) == str(columnName):
                columnNo=No
                break
        if uni.MainWindow.Table.checkHiddenColumn(columnNo,False)==False:
            return False
        for rowNo in range(uni.MainWindow.Table.rowCount()):
            if uni.MainWindow.Table.isChangeableItem(rowNo, columnNo):
                myString = str(_newString)
                if self.specialTools.btChange.isChecked()==True:
                    pass
                elif self.specialTools.tbAddToBefore.isChecked()==True:
                    myString += str(uni.MainWindow.Table.item(rowNo,columnNo).text())
                elif self.specialTools.tbAddToAfter.isChecked()==True:
                    myString = str(uni.MainWindow.Table.item(rowNo,columnNo).text()) + myString
                uni.MainWindow.Table.item(rowNo,columnNo).setText(str(uni.trUnicode(myString)))
                    
    
