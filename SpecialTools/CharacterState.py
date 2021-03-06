# This file is part of HamsiManager.
#
# Copyright (c) 2010 - 2015 Murat Demir <mopened@gmail.com>
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


from Core import Organizer
from Core import Universals as uni
from Core.MyObjects import *
from Databases import CompleterTable


class CharacterState(MWidget):
    def __init__(self, _parent):
        MWidget.__init__(self, _parent)
        self.specialTools = _parent
        self.leSearch = MLineEdit("")
        self.cckbCorrectText = MCheckBox(translate("SpecialTools", "Correct Text"))
        lblColumns = MLabel(translate("SpecialTools", "Column: "))
        lblCharacterType = MLabel(translate("SpecialTools", "Character Format: "))
        self.columns = MyComboBox()
        self.cbCharacterType = MComboBox()
        self.cbCharacterType.addItems([translate("Options", "Title"),
                                       translate("Options", "All Small"),
                                       translate("Options", "All Caps"),
                                       translate("Options", "Sentence"),
                                       translate("Options", "Don`t Change")])
        self.cckbCaseInsensitive = MCheckBox(translate("SpecialTools", "Case Insensitive"))
        self.cckbRegExp = MCheckBox(translate("SpecialTools", "Regular Expression (RegExp)"))
        HBoxs = []
        HBoxs.append(MHBoxLayout())
        HBoxs[0].addWidget(lblColumns)
        HBoxs[0].addWidget(self.columns)
        HBoxs[0].addWidget(lblCharacterType)
        HBoxs[0].addWidget(self.cbCharacterType)
        HBoxs.append(MHBoxLayout())
        HBoxs[1].addWidget(self.cckbCorrectText)
        HBoxs[1].addWidget(self.leSearch)
        HBoxs[1].addWidget(self.cckbCaseInsensitive)
        HBoxs.append(MHBoxLayout())
        HBoxs[2].addStretch(3)
        HBoxs[2].addWidget(self.cckbRegExp)
        self.cckbCaseInsensitive.setEnabled(False)
        self.cckbRegExp.setEnabled(False)
        self.leSearch.setEnabled(False)
        vblCharacterState = MVBoxLayout()
        vblCharacterState.addLayout(HBoxs[0])
        vblCharacterState.addLayout(HBoxs[1])
        vblCharacterState.addLayout(HBoxs[2])
        self.setLayout(vblCharacterState)
        lblColumns.setFixedWidth(60)
        MObject.connect(self.cckbCorrectText, SIGNAL("stateChanged(int)"), self.cckbCorrectTextChanged)

    def showAdvancedSelections(self):
        self.cckbRegExp.show()

    def hideAdvancedSelections(self):
        self.cckbRegExp.hide()
        self.cckbRegExp.setChecked(False)

    def cckbCorrectTextChanged(self, _value):
        if _value == 2:
            self.cckbCaseInsensitive.setEnabled(True)
            self.cckbRegExp.setEnabled(True)
            self.leSearch.setEnabled(True)
        else:
            self.cckbCaseInsensitive.setEnabled(False)
            self.cckbRegExp.setEnabled(False)
            self.leSearch.setEnabled(False)

    def checkCompleters(self):
        if uni.getBoolValue("isActiveCompleter"):
            CompleterTable.insert(self.cckbCorrectText.text(), self.leSearch.text())

    def reFillCompleters(self):
        if uni.getBoolValue("isActiveCompleter"):
            setCompleter(self.leSearch, self.cckbCorrectText.text())

    def apply(self):
        self.checkCompleters()
        self.reFillCompleters()
        getMainTable().createHistoryPoint()
        getMainTable().isAskShowHiddenColumn = True
        searchStrings = str(self.leSearch.text()).split(";")
        selectedColumnKey = self.columns.currentData()
        if selectedColumnKey == "all":
            columnKeys = getMainTable().getWritableColumnKeys()
        else:
            columnKeys = [selectedColumnKey]
        for columnKey in columnKeys:
            columnNo = getMainTable().getColumnNoFromKey(columnKey)
            if getMainTable().checkReadOnlyColumn(columnKey) is False:
                continue
            if getMainTable().checkHiddenColumn(columnKey, False) is False:
                continue
            for rowNo in range(getMainTable().rowCount()):
                if getMainTable().isChangeableItem(rowNo, columnKey):
                    newString = uni.trUnicode(getMainTable().item(rowNo, columnNo).text())
                    myString = ""
                    informationSectionX = self.specialTools.cbInformationSectionX.value()
                    informationSectionY = self.specialTools.cbInformationSectionY.value()
                    cbCharacterType = uni.validSentenceStructureKeys[self.cbCharacterType.currentIndex()]
                    isCaseInsensitive = self.cckbCaseInsensitive.isChecked()
                    isRegExp = self.cckbRegExp.isChecked()
                    isCorrectText = self.cckbCorrectText.isChecked()
                    if self.specialTools.cbInformationSection.currentIndex() == 0:
                        myString = Organizer.correctCaseSensitive(newString, cbCharacterType, isCorrectText,
                                                                  searchStrings, isCaseInsensitive, isRegExp)
                    elif self.specialTools.cbInformationSection.currentIndex() == 1:
                        myString = Organizer.correctCaseSensitive(newString[:informationSectionX], cbCharacterType,
                                                                  isCorrectText, searchStrings, isCaseInsensitive,
                                                                  isRegExp)
                        myString += newString[informationSectionX:]
                    elif self.specialTools.cbInformationSection.currentIndex() == 2:
                        myString = newString[:informationSectionX]
                        myString += Organizer.correctCaseSensitive(newString[informationSectionX:], cbCharacterType,
                                                                   isCorrectText, searchStrings, isCaseInsensitive,
                                                                   isRegExp)
                    elif self.specialTools.cbInformationSection.currentIndex() == 3:
                        myString = Organizer.correctCaseSensitive(newString[:-informationSectionX], cbCharacterType,
                                                                  isCorrectText, searchStrings, isCaseInsensitive,
                                                                  isRegExp)
                        myString += newString[-informationSectionX:]
                    elif self.specialTools.cbInformationSection.currentIndex() == 4:
                        myString = newString[:-informationSectionX]
                        myString += Organizer.correctCaseSensitive(newString[-informationSectionX:], cbCharacterType,
                                                                   isCorrectText, searchStrings, isCaseInsensitive,
                                                                   isRegExp)
                    elif self.specialTools.cbInformationSection.currentIndex() == 5:
                        myString = newString[:informationSectionX]
                        myString += Organizer.correctCaseSensitive(newString[informationSectionX:informationSectionY],
                                                                   cbCharacterType, isCorrectText, searchStrings,
                                                                   isCaseInsensitive, isRegExp)
                        myString += newString[informationSectionY:]
                    elif self.specialTools.cbInformationSection.currentIndex() == 6:
                        myString = Organizer.correctCaseSensitive(newString[:informationSectionX], cbCharacterType,
                                                                  isCorrectText, searchStrings, isCaseInsensitive,
                                                                  isRegExp)
                        myString += newString[informationSectionX:informationSectionY]
                        myString += Organizer.correctCaseSensitive(newString[informationSectionY:], cbCharacterType,
                                                                   isCorrectText, searchStrings, isCaseInsensitive,
                                                                   isRegExp)
                    getMainTable().item(rowNo, columnNo).setText(str(myString))
            
    
