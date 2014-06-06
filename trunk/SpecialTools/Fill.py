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
from Core import Organizer
from Core import Universals
from Core.MyObjects import *
import Tables
from Core import Dialogs
import sys
from Core import ReportBug
import Databases

class Fill(MWidget):
    def __init__(self, _parent):
        MWidget.__init__(self, _parent)
        self.specialTools = _parent
        lblFillType = MLabel(translate("SpecialTools", "Content Type: "))
        self.cbFillType = MComboBox()
        self.cbFillType.addItems([translate("SpecialTools", "Text"),
                                translate("SpecialTools", "Number")])
        lblspCharNumberOfDigit = MLabel(translate("SpecialTools", "Number Of Characters: "))
        self.spCharNumberOfDigit = MSpinBox()
        self.spCharNumberOfDigit.setRange(1, 20)
        self.spCharNumberOfDigit.setValue(2) 
        self.columns = MComboBox()
        lblColumns = MLabel(translate("SpecialTools", "Column: "))
        lblColumns.setFixedWidth(60)
        self.lblFill = MLabel(translate("SpecialTools", "Text: "))
        self.lblFill.setFixedWidth(60)
        self.leFill = MLineEdit("")
        self.lblSort = MLabel(translate("SpecialTools", "Sort: "))
        self.lblSort.setFixedWidth(80)
        self.cbSort = MComboBox()
        self.cbSort.addItems([translate("SpecialTools", "Ascending"),
                            translate("SpecialTools", "Descending")])
        self.lblStartDigit = MLabel(translate("SpecialTools", "Begins With: "))
        self.lblStartDigit.setFixedWidth(120)
        self.spStartDigit = MSpinBox()
        self.spStartDigit.setRange(-999999, 999999)
        self.spStartDigit.setValue(0)
        self.spCharNumberOfDigit.setEnabled(False)
        self.cbSort.setEnabled(False)
        self.spStartDigit.setEnabled(False)
        HBoxs = []
        HBoxs.append(MHBoxLayout())
        HBoxs[0].addWidget(lblColumns)
        HBoxs[0].addWidget(self.columns)
        HBoxs[0].addWidget(lblFillType)
        HBoxs[0].addWidget(self.cbFillType)
        HBoxs.append(MHBoxLayout())
        HBoxs[1].addWidget(self.lblFill)
        HBoxs[1].addWidget(self.leFill)
        HBoxs[1].addWidget(lblspCharNumberOfDigit)
        HBoxs[1].addWidget(self.spCharNumberOfDigit)
        HBoxs.append(MHBoxLayout())
        HBoxs[2].addWidget(self.lblSort)
        HBoxs[2].addWidget(self.cbSort)
        HBoxs[2].addWidget(self.lblStartDigit)
        HBoxs[2].addWidget(self.spStartDigit)
        vblFill = MVBoxLayout()
        vblFill.addLayout(HBoxs[0])
        vblFill.addLayout(HBoxs[1])
        vblFill.addLayout(HBoxs[2])
        self.setLayout(vblFill)
        MObject.connect(self.columns, SIGNAL("currentIndexChanged(int)"), self.columnsChanged)
        MObject.connect(self.cbFillType, SIGNAL("currentIndexChanged(int)"), self.fillTypeChanged)
        
    def showAdvancedSelections(self):
        self.lblSort.show()
        self.cbSort.show()
        self.lblStartDigit.show()
        self.spStartDigit.show()
    
    def hideAdvancedSelections(self):
        self.cbSort.setCurrentIndex(0)
        self.spStartDigit.setValue(0)
        self.lblSort.hide()
        self.cbSort.hide()
        self.lblStartDigit.hide()
        self.spStartDigit.hide()
        
    def columnsChanged(self,_index):
        try:
            if str(self.columns.currentText())=="Track No":
                self.cbFillType.setCurrentIndex(1)
                self.cbFillType.setEnabled(False)
                self.leFill.setEnabled(False)
                self.spCharNumberOfDigit.setEnabled(True)
            else:
                self.cbFillType.setCurrentIndex(0)
                self.cbFillType.setEnabled(True)
                self.leFill.setEnabled(True)
                self.spCharNumberOfDigit.setEnabled(False)
        except:
            ReportBug.ReportBug()
            
    def fillTypeChanged(self):
        if self.cbFillType.currentIndex()==1:
            self.leFill.setEnabled(False)
            self.spCharNumberOfDigit.setEnabled(True)
            self.cbSort.setEnabled(True)
            self.spStartDigit.setEnabled(True)
        else:
            self.leFill.setEnabled(True)
            self.spCharNumberOfDigit.setEnabled(False)
            self.cbSort.setEnabled(False)
            self.spStartDigit.setEnabled(False)
    
    def checkCompleters(self):
        Databases.CompleterTable.insert(self.lblFill.text(), self.leFill.text())
    
    def reFillCompleters(self):
        setCompleter(self.leFill, self.lblFill.text())
       
    def apply(self):
        newString = str(self.leFill.text())
        Tables.isAskShowHiddenColumn=True
        for No, columnName in enumerate(Universals.MainWindow.Table.tableColumns):
            if str(self.columns.currentText()) == str(columnName):
                columnNo=No
                break
        if Tables.checkHiddenColumn(columnNo,False)==False:
            return False
        if self.cbFillType.currentIndex()==1:
            newString = int(self.spStartDigit.value())-1
        for rowNo in range(Universals.MainWindow.Table.rowCount()):
            if Universals.MainWindow.Table.isChangableItem(rowNo, columnNo):
                if self.cbFillType.currentIndex()==1:
                    if self.cbSort.currentIndex()==0:
                        newString+=1
                    else:
                        newString-=1
                    myString = str(newString)
                    inNegative = False
                    if myString.find("-")!=-1:
                        myString = myString.replace("-", "")
                        inNegative = True
                    karakterSayisi = len(myString)
                    while karakterSayisi < int(self.spCharNumberOfDigit.value()):
                        myString="0"+myString
                        karakterSayisi = len(myString)
                    if inNegative:
                        myString="-"+myString
                else:
                    myString = str(newString)
                if self.specialTools.btChange.isChecked()==True:
                    pass
                elif self.specialTools.tbAddToBefore.isChecked()==True:
                    myString += str(Universals.MainWindow.Table.item(rowNo,columnNo).text())
                elif self.specialTools.tbAddToAfter.isChecked()==True:
                    myString = str(Universals.MainWindow.Table.item(rowNo,columnNo).text()) + myString
                Universals.MainWindow.Table.item(rowNo,columnNo).setText(trForUI(Universals.trUnicode(myString)))
                    
    