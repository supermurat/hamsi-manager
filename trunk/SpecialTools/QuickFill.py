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
            if self.tmrFillAfter != None:
                self.tmrFillAfter.stop()
                self.tmrFillAfter.deleteLater()
            self.tmrFillAfter = MTimer(self)
            self.tmrFillAfter.setSingleShot(True)
            self.connect(self.tmrFillAfter, SIGNAL("timeout()"), self.fill)
            self.tmrFillAfter.start(1000)
        except:
            from Core import ReportBug

            ReportBug.ReportBug()

    def fill(self, _searchValue=""):
        try:
            self.checkCompleters()
            self.reFillCompleters()
            getMainWindow().Table.createHistoryPoint()
            self.apply()
        except:
            from Core import ReportBug

            ReportBug.ReportBug()

    def apply(self):
        _newString = str(self.fillFrom.text())
        getMainWindow().Table.isAskShowHiddenColumn = True
        for No, columnName in enumerate(getMainWindow().Table.tableColumns):
            if str(self.fillFrom.objectName()) == str(columnName):
                columnNo = No
                break
        if getMainWindow().Table.checkHiddenColumn(columnNo, False) == False:
            return False
        for rowNo in range(getMainWindow().Table.rowCount()):
            if getMainWindow().Table.isChangeableItem(rowNo, columnNo):
                myString = str(_newString)
                if self.specialTools.btChange.isChecked():
                    pass
                elif self.specialTools.tbAddToBefore.isChecked():
                    myString += str(getMainWindow().Table.item(rowNo, columnNo).text())
                elif self.specialTools.tbAddToAfter.isChecked():
                    myString = str(getMainWindow().Table.item(rowNo, columnNo).text()) + myString
                getMainWindow().Table.item(rowNo, columnNo).setText(str(uni.trUnicode(myString)))
                    
    
