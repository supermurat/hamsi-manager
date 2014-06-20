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


class SearchAndReplace(MWidget):
    def __init__(self, _parent):
        MWidget.__init__(self, _parent)
        self.specialTools = _parent
        self.lblSearch = MLabel(translate("SpecialTools", "Search: "))
        self.lblReplace = MLabel(translate("SpecialTools", "Replace: "))
        self.leSearch = MLineEdit("")
        self.leReplace = MLineEdit("")
        lblColumns = MLabel(translate("SpecialTools", "Column: "))
        srExamples = translate("SpecialTools",
                               "<table><tr><td><nobr>Before</nobr></td><td>>></td><td><nobr>Search</nobr></td><td>-</td><td><nobr>Replace</nobr></td><td>>></td><td><nobr>After</nobr></td></tr>" +
                               "<tr><td><nobr>HamsiManager</nobr></td><td>>></td><td><nobr>ager</nobr></td><td>-</td><td><nobr></nobr></td><td>>></td><td><nobr>HamsiMan</nobr></td></tr>" +
                               "</table><table>")
        sExample = translate("SpecialTools",
                             "<tr><td><nobr>Example: \"search 1<b>;</b>search 2<b>;</b>search 3<b>;</b>...<b>;</b>search n<b>;</b>\"</nobr></td></tr>")
        rExample = translate("SpecialTools",
                             "<tr><td><nobr>Example: \"Change/replace 1<b>;</b>Change/replace 2<b>;</b>Change/replace 3<b>;</b>...<b>;</b>Change/replace n<b>;</b>\"</nobr></td></tr>")
        self.cckbCaseInsensitive = MCheckBox(translate("SpecialTools", "Case Insensitive"))
        self.cckbCaseInsensitive.setChecked(True)
        self.cckbRegExp = MCheckBox(translate("SpecialTools", "Regular Expression (RegExp)"))
        self.leSearch.setToolTip(str(srExamples + sExample + "</table>"))
        self.leReplace.setToolTip(str(srExamples + rExample + "</table>"))
        self.columns = MComboBox()
        self.columns.addItem(translate("SpecialTools", "All"))
        self.pbtnEditValueForSearch = MPushButton(translate("Options", "*"))
        self.pbtnEditValueForSearch.setObjectName(
            str(translate("Options", "Edit Values With Advanced Value Editor") + "For Search"))
        self.pbtnEditValueForSearch.setToolTip(translate("Options", "Edit values with Advanced Value Editor"))
        self.pbtnEditValueForSearch.setFixedWidth(25)
        MObject.connect(self.pbtnEditValueForSearch, SIGNAL("clicked()"), self.pbtnEditValueClicked)
        self.pbtnEditValueForReplace = MPushButton(translate("Options", "*"))
        self.pbtnEditValueForReplace.setObjectName(
            str(translate("Options", "Edit Values With Advanced Value Editor") + "For Replace"))
        self.pbtnEditValueForReplace.setToolTip(translate("Options", "Edit values with Advanced Value Editor"))
        self.pbtnEditValueForReplace.setFixedWidth(25)
        MObject.connect(self.pbtnEditValueForReplace, SIGNAL("clicked()"), self.pbtnEditValueClicked)
        self.lblSearch.setFixedWidth(60)
        self.lblReplace.setFixedWidth(100)
        lblColumns.setFixedWidth(60)
        HBoxs = []
        HBoxs.append(MHBoxLayout())
        HBoxs[0].addWidget(self.lblSearch)
        HBoxs[0].addWidget(self.leSearch)
        HBoxs[0].addWidget(self.pbtnEditValueForSearch)
        HBoxs[0].addWidget(self.lblReplace)
        HBoxs[0].addWidget(self.leReplace)
        HBoxs[0].addWidget(self.pbtnEditValueForReplace)
        HBoxs.append(MHBoxLayout())
        HBoxs[1].addWidget(lblColumns)
        HBoxs[1].addWidget(self.columns)
        HBoxs[1].addStretch(2)
        HBoxs[1].addWidget(self.cckbCaseInsensitive)
        HBoxs.append(MHBoxLayout())
        HBoxs[2].addStretch(3)
        HBoxs[2].addWidget(self.cckbRegExp)
        vblSearchAndReplace = MVBoxLayout()
        vblSearchAndReplace.addLayout(HBoxs[0])
        vblSearchAndReplace.addLayout(HBoxs[1])
        vblSearchAndReplace.addLayout(HBoxs[2])
        self.setLayout(vblSearchAndReplace)

    def showAdvancedSelections(self):
        self.cckbRegExp.show()
        self.pbtnEditValueForSearch.show()
        self.pbtnEditValueForReplace.show()

    def hideAdvancedSelections(self):
        self.cckbRegExp.hide()
        self.pbtnEditValueForSearch.hide()
        self.pbtnEditValueForReplace.hide()
        self.cckbRegExp.setChecked(False)

    def pbtnEditValueClicked(self):
        sarled = SearchAndReplaceListEditDialog(self)

    def checkCompleters(self):
        Databases.CompleterTable.insert(self.lblSearch.text(), self.leSearch.text())
        Databases.CompleterTable.insert(self.lblReplace.text(), self.leReplace.text())

    def reFillCompleters(self):
        setCompleter(self.leReplace, self.lblReplace.text())
        setCompleter(self.leSearch, self.lblSearch.text())

    def apply(self):
        searchStrings = str(self.leSearch.text()).split(";")
        replaceStrings = str(self.leReplace.text()).split(";")
        for filterNo in range(0, len(searchStrings)):
            if self.specialTools.btChange.isChecked():
                pass
            elif self.specialTools.tbAddToBefore.isChecked():
                replaceStrings[filterNo] += searchStrings[filterNo]
            elif self.specialTools.tbAddToAfter.isChecked():
                replaceStrings[filterNo] = searchStrings[filterNo] + replaceStrings[filterNo]
        while len(replaceStrings) != len(searchStrings):
            replaceStrings.append("")
        if self.columns.currentIndex() == 0:
            columns = list(range(0, getMainWindow().Table.columnCount()))
        else:
            columns = [self.columns.currentIndex() - 1]
        for columnNo in columns:
            if getMainWindow().Table.isColumnHidden(columnNo):
                continue
            for rowNo in range(getMainWindow().Table.rowCount()):
                if getMainWindow().Table.isChangeableItem(rowNo, columnNo, None, True):
                    newString = str(getMainWindow().Table.item(rowNo, columnNo).text())
                    newString = str(newString)
                    myString = ""
                    informationSectionX = self.specialTools.cbInformationSectionX.value()
                    informationSectionY = self.specialTools.cbInformationSectionY.value()
                    isCaseInsensitive = self.cckbCaseInsensitive.isChecked()
                    isRegExp = self.cckbRegExp.isChecked()
                    if self.specialTools.cbInformationSection.currentIndex() == 0:
                        myString = Organizer.searchAndReplace(newString, searchStrings,
                                                              replaceStrings, isCaseInsensitive, isRegExp)
                    elif self.specialTools.cbInformationSection.currentIndex() == 1:
                        myString = Organizer.searchAndReplace(newString[:informationSectionX], searchStrings,
                                                              replaceStrings, isCaseInsensitive, isRegExp)
                        myString += newString[informationSectionX:]
                    elif self.specialTools.cbInformationSection.currentIndex() == 2:
                        myString = newString[:informationSectionX]
                        myString += Organizer.searchAndReplace(newString[informationSectionX:], searchStrings,
                                                               replaceStrings, isCaseInsensitive, isRegExp)
                    elif self.specialTools.cbInformationSection.currentIndex() == 3:
                        myString = Organizer.searchAndReplace(newString[:-informationSectionX], searchStrings,
                                                              replaceStrings, isCaseInsensitive, isRegExp)
                        myString += newString[-informationSectionX:]
                    elif self.specialTools.cbInformationSection.currentIndex() == 4:
                        myString = newString[:-informationSectionX]
                        myString += Organizer.searchAndReplace(newString[-informationSectionX:], searchStrings,
                                                               replaceStrings, isCaseInsensitive, isRegExp)
                    elif self.specialTools.cbInformationSection.currentIndex() == 5:
                        myString = newString[:informationSectionX]
                        myString += Organizer.searchAndReplace(newString[informationSectionX:informationSectionY],
                                                               searchStrings,
                                                               replaceStrings, isCaseInsensitive, isRegExp)
                        myString += newString[informationSectionY:]
                    elif self.specialTools.cbInformationSection.currentIndex() == 6:
                        myString = Organizer.searchAndReplace(newString[:informationSectionX], searchStrings,
                                                              replaceStrings, isCaseInsensitive, isRegExp)
                        myString += newString[informationSectionX:informationSectionY]
                        myString += Organizer.searchAndReplace(newString[informationSectionY:], searchStrings,
                                                               replaceStrings, isCaseInsensitive, isRegExp)
                    getMainWindow().Table.item(rowNo, columnNo).setText(str(myString))


class SearchAndReplaceListEditDialog(MDialog):
    def __init__(self, _parent):
        MDialog.__init__(self, _parent)
        if isActivePyKDE4:
            self.setButtons(MDialog.NoDefault)
        self.setWindowTitle(translate("SearchAndReplaceListEditDialog", "Advanced Value Editor"))
        currentValueForSearch = str(self.parent().leSearch.text())
        currentValueForReplace = str(self.parent().leReplace.text())
        if isActivePyKDE4:
            self.EditorWidgetForSearch = MEditListBox(self)
            self.EditorWidgetForSearch.setItems([str(x) for x in currentValueForSearch.split(";")])
            self.EditorWidgetForReplace = MEditListBox(self)
            self.EditorWidgetForReplace.setItems([str(x) for x in currentValueForReplace.split(";")])
        else:
            self.EditorWidgetForSearch = MTextEdit(self)
            self.EditorWidgetForSearch.setText(str(currentValueForSearch.replace(";", "\n")))
            self.EditorWidgetForReplace = MTextEdit(self)
            self.EditorWidgetForReplace.setText(str(currentValueForReplace.replace(";", "\n")))
        pnlMain = MWidget(self)
        vblMain = MVBoxLayout(pnlMain)
        pbtnCancel = MPushButton(translate("SearchAndReplaceListEditDialog", "Cancel"))
        pbtnApply = MPushButton(translate("SearchAndReplaceListEditDialog", "Apply"))
        MObject.connect(pbtnCancel, SIGNAL("clicked()"), self.close)
        MObject.connect(pbtnApply, SIGNAL("clicked()"), self.apply)
        vblMain.addWidget(MLabel(translate("SearchAndReplaceListEditDialog", "Search List : ")))
        vblMain.addWidget(self.EditorWidgetForSearch)
        vblMain.addWidget(MLabel(translate("SearchAndReplaceListEditDialog", "Replace List : ")))
        vblMain.addWidget(self.EditorWidgetForReplace)
        hblBox = MHBoxLayout()
        hblBox.addWidget(pbtnApply)
        hblBox.addWidget(pbtnCancel)
        vblMain.addLayout(hblBox)
        if isActivePyKDE4:
            self.setMainWidget(pnlMain)
        else:
            self.setLayout(vblMain)
        self.setMinimumSize(550, 400)
        self.show()

    def apply(self):
        valueForSearch = ""
        valueForReplace = ""
        if isActivePyKDE4:
            for y, info in enumerate(self.EditorWidgetForSearch.items()):
                if y != 0:
                    valueForSearch += ";"
                valueForSearch += str(info)
            for y, info in enumerate(self.EditorWidgetForReplace.items()):
                if y != 0:
                    valueForReplace += ";"
                valueForReplace += str(info)
        else:
            valueForSearch = str(self.EditorWidgetForSearch.toPlainText()).replace("\n", ";")
            valueForReplace = str(self.EditorWidgetForReplace.toPlainText()).replace("\n", ";")
        self.parent().leSearch.setText(str(valueForSearch))
        self.parent().leReplace.setText(str(valueForReplace))
        self.close()
        
