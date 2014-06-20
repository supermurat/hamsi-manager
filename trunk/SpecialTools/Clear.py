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


from Core import Organizer
from Core import Universals as uni
from Core.MyObjects import *
import Tables
from Core import Dialogs
import sys
from Core import ReportBug
import Databases


class Clear(MWidget):
    def __init__(self, _parent):
        MWidget.__init__(self, _parent)
        self.specialTools = _parent
        self.leClear = MLineEdit("")
        self.lblClear = MLabel(translate("SpecialTools", "Text: "))
        lblColumns = MLabel(translate("SpecialTools", "Column: "))
        lblClearType = MLabel(translate("SpecialTools", "Content Type: "))
        self.cbClearType = MComboBox()
        self.cbClearType.addItems([translate("SpecialTools", "All"),
                                   translate("SpecialTools", "Letters"),
                                   translate("SpecialTools", "Numbers"),
                                   translate("SpecialTools", "Other Characters"),
                                   translate("SpecialTools", "Selected Text")])
        self.columns = MComboBox()
        self.columns.addItem(translate("SpecialTools", "All"))
        self.cckbCaseInsensitive = MCheckBox(translate("SpecialTools", "Case Insensitive"))
        self.cckbRegExp = MCheckBox(translate("SpecialTools", "Regular Expression (RegExp)"))
        self.cckbCaseInsensitive.setChecked(True)
        HBoxs = []
        HBoxs.append(MHBoxLayout())
        HBoxs[0].addWidget(lblColumns)
        HBoxs[0].addWidget(self.columns)
        HBoxs[0].addWidget(lblClearType)
        HBoxs[0].addWidget(self.cbClearType)
        HBoxs.append(MHBoxLayout())
        HBoxs[1].addWidget(self.lblClear)
        HBoxs[1].addWidget(self.leClear)
        HBoxs[1].addWidget(self.cckbCaseInsensitive)
        HBoxs.append(MHBoxLayout())
        HBoxs[2].addStretch(3)
        HBoxs[2].addWidget(self.cckbRegExp)
        vblClear = MVBoxLayout()
        vblClear.addLayout(HBoxs[0])
        vblClear.addLayout(HBoxs[1])
        vblClear.addLayout(HBoxs[2])
        self.setLayout(vblClear)
        self.cckbCaseInsensitive.setEnabled(False)
        self.cckbRegExp.setEnabled(False)
        self.lblClear.setEnabled(False)
        self.leClear.setEnabled(False)
        lblColumns.setFixedWidth(60)
        self.lblClear.setFixedWidth(60)
        MObject.connect(self.cbClearType, SIGNAL("currentIndexChanged(int)"), self.clearTypeChanged)

    def clearTypeChanged(self):
        if self.cbClearType.currentIndex() != 4:
            self.cckbCaseInsensitive.setEnabled(False)
            self.lblClear.setEnabled(False)
            self.leClear.setEnabled(False)
            self.cckbRegExp.setEnabled(False)
        else:
            self.cckbCaseInsensitive.setEnabled(True)
            self.lblClear.setEnabled(True)
            self.leClear.setEnabled(True)
            self.cckbRegExp.setEnabled(True)

    def showAdvancedSelections(self):
        self.cckbRegExp.show()

    def hideAdvancedSelections(self):
        self.cckbRegExp.hide()
        self.cckbRegExp.setChecked(False)

    def checkCompleters(self):
        Databases.CompleterTable.insert(self.lblClear.text(), self.leClear.text())

    def reFillCompleters(self):
        setCompleter(self.leClear, self.lblClear.text())

    def apply(self):
        getMainWindow().Table.isAskShowHiddenColumn = True
        if self.columns.currentIndex() == 0:
            columns = list(range(0, getMainWindow().Table.columnCount()))
        else:
            columns = [self.columns.currentIndex() - 1]
        for columnNo in columns:
            if getMainWindow().Table.checkHiddenColumn(columnNo, False) == False:
                continue
            for rowNo in range(getMainWindow().Table.rowCount()):
                if getMainWindow().Table.isChangeableItem(rowNo, columnNo):
                    newString = str(getMainWindow().Table.item(rowNo, columnNo).text())
                    newString = uni.trDecode(newString, "utf-8")
                    informationSectionX = self.specialTools.cbInformationSectionX.value()
                    informationSectionY = self.specialTools.cbInformationSectionY.value()
                    isCaseInsensitive = self.cckbCaseInsensitive.isChecked()
                    oldString = str(self.leClear.text())
                    cbClearType = self.cbClearType.currentText()
                    isRegExp = self.cckbRegExp.isChecked()
                    if self.specialTools.cbInformationSection.currentIndex() == 0:
                        myString = Organizer.clear(cbClearType, newString,
                                                   oldString, isCaseInsensitive, isRegExp)
                    elif self.specialTools.cbInformationSection.currentIndex() == 1:
                        myString = Organizer.clear(cbClearType, newString[:informationSectionX],
                                                   oldString, isCaseInsensitive, isRegExp)
                        myString += newString[informationSectionX:]
                    elif self.specialTools.cbInformationSection.currentIndex() == 2:
                        myString = newString[:informationSectionX]
                        myString += Organizer.clear(cbClearType, newString[informationSectionX:],
                                                    oldString, isCaseInsensitive, isRegExp)
                    elif self.specialTools.cbInformationSection.currentIndex() == 3:
                        myString = Organizer.clear(cbClearType, newString[:-informationSectionX],
                                                   oldString, isCaseInsensitive, isRegExp)
                        myString += newString[-informationSectionX:]
                    elif self.specialTools.cbInformationSection.currentIndex() == 4:
                        myString = newString[:-informationSectionX]
                        myString += Organizer.clear(cbClearType, newString[-informationSectionX:],
                                                    oldString, isCaseInsensitive, isRegExp)
                    elif self.specialTools.cbInformationSection.currentIndex() == 5:
                        myString = newString[:informationSectionX]
                        myString += Organizer.clear(cbClearType, newString[informationSectionX:informationSectionY],
                                                    oldString, isCaseInsensitive, isRegExp)
                        myString += newString[informationSectionY:]
                    elif self.specialTools.cbInformationSection.currentIndex() == 6:
                        myString = Organizer.clear(cbClearType, newString[:informationSectionX],
                                                   oldString, isCaseInsensitive, isRegExp)
                        myString += newString[informationSectionX:informationSectionY]
                        myString += Organizer.clear(cbClearType, newString[informationSectionY:],
                                                    oldString, isCaseInsensitive, isRegExp)
                    getMainWindow().Table.item(rowNo, columnNo).setText(str(myString))
    
    
