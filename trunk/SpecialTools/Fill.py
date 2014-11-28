# This file is part of HamsiManager.
#
# Copyright (c) 2010 - 2014 Murat Demir <mopened@gmail.com>
#
# Hamsi Manager is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Hamsi Manager is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with HamsiManager; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA


from Core import Universals as uni
from Core.MyObjects import *
from Core import ReportBug
from Databases import CompleterTable


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
        self.columns = MyComboBox()
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

    def columnsChanged(self, _index):
        try:
            if str(self.columns.currentText()) == "Track No":
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
        if self.cbFillType.currentIndex() == 1:
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
        if uni.getBoolValue("isActiveCompleter"):
            CompleterTable.insert(self.lblFill.text(), self.leFill.text())

    def reFillCompleters(self):
        if uni.getBoolValue("isActiveCompleter"):
            setCompleter(self.leFill, self.lblFill.text())

    def apply(self):
        self.checkCompleters()
        self.reFillCompleters()
        getMainTable().createHistoryPoint()
        newString = str(self.leFill.text())
        getMainTable().isAskShowHiddenColumn = True
        columnKey = self.columns.currentData()
        columnNo = getMainTable().getColumnNoFromKey(columnKey)
        if getMainTable().checkReadOnlyColumn(columnKey) is False:
            return False
        if getMainTable().checkHiddenColumn(columnKey, False) is False:
            return False
        if self.cbFillType.currentIndex() == 1:
            newString = int(self.spStartDigit.value()) - 1
        for rowNo in range(getMainTable().rowCount()):
            if getMainTable().isChangeableItem(rowNo, columnKey):
                if self.cbFillType.currentIndex() == 1:
                    if self.cbSort.currentIndex() == 0:
                        newString += 1
                    else:
                        newString -= 1
                    myString = str(newString)
                    inNegative = False
                    if myString.find("-") != -1:
                        myString = myString.replace("-", "")
                        inNegative = True
                    karakterSayisi = len(myString)
                    while karakterSayisi < int(self.spCharNumberOfDigit.value()):
                        myString = "0" + myString
                        karakterSayisi = len(myString)
                    if inNegative:
                        myString = "-" + myString
                else:
                    myString = str(newString)
                if self.specialTools.btChange.isChecked():
                    pass
                elif self.specialTools.tbAddToBefore.isChecked():
                    myString += str(getMainTable().item(rowNo, columnNo).text())
                elif self.specialTools.tbAddToAfter.isChecked():
                    myString = str(getMainTable().item(rowNo, columnNo).text()) + myString
                getMainTable().item(rowNo, columnNo).setText(str(uni.trUnicode(myString)))
                    
    
