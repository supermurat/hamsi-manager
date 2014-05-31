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

class CharacterState(MWidget):
    def __init__(self, _parent):
        MWidget.__init__(self, _parent)
        self.specialTools = _parent
        self.leSearch = MLineEdit("")
        self.cckbCorrectText = MCheckBox(translate("SpecialTools", "Correct Text"))
        lblColumns = MLabel(translate("SpecialTools", "Column: "))
        lblCharacterType = MLabel(translate("SpecialTools", "Character Format: "))
        self.columns = MComboBox()
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
        if _value==2:
            self.cckbCaseInsensitive.setEnabled(True)
            self.cckbRegExp.setEnabled(True)
            self.leSearch.setEnabled(True)
        else:
            self.cckbCaseInsensitive.setEnabled(False)
            self.cckbRegExp.setEnabled(False)
            self.leSearch.setEnabled(False)
    
    def checkCompleters(self):
        Databases.CompleterTable.insert(self.cckbCorrectText.text(), self.leSearch.text())
    
    def reFillCompleters(self):
        setCompleter(self.leSearch, self.cckbCorrectText.text())
        
    def apply(self):
        Tables.isAskShowHiddenColumn=True
        searchStrings = str(self.leSearch.text()).split(";")
        if self.columns.currentIndex()==0:
            columns = list(range(0,Universals.MainWindow.Table.columnCount()))
        else:
            columns = [self.columns.currentIndex()-1]
        for columnNo in columns:
            if Tables.checkHiddenColumn(columnNo,False)==False:
                continue
            for rowNo in range(Universals.MainWindow.Table.rowCount()):
                if Universals.MainWindow.Table.isChangableItem(rowNo, columnNo):
                    newString = str(Universals.MainWindow.Table.item(rowNo,columnNo).text())
                    myString = ""
                    informationSectionX = self.specialTools.cbInformationSectionX.value()
                    informationSectionY = self.specialTools.cbInformationSectionY.value()
                    cbCharacterType = Variables.validSentenceStructureKeys[self.cbCharacterType.currentIndex()]
                    isCaseInsensitive = self.cckbCaseInsensitive.isChecked()
                    isRegExp = self.cckbRegExp.isChecked()
                    isCorrectText = self.cckbCorrectText.isChecked()
                    if self.specialTools.cbInformationSection.currentIndex()==0:
                        myString = Organizer.correctCaseSensitive(newString, cbCharacterType, isCorrectText, searchStrings, isCaseInsensitive, isRegExp)
                    elif self.specialTools.cbInformationSection.currentIndex()==1:
                        myString = Organizer.correctCaseSensitive(newString[:informationSectionX], cbCharacterType, isCorrectText, searchStrings, isCaseInsensitive, isRegExp)
                        myString += newString[informationSectionX:]
                    elif self.specialTools.cbInformationSection.currentIndex()==2:
                        myString = newString[:informationSectionX]
                        myString += Organizer.correctCaseSensitive(newString[informationSectionX:], cbCharacterType, isCorrectText, searchStrings, isCaseInsensitive, isRegExp)
                    elif self.specialTools.cbInformationSection.currentIndex()==3:
                        myString = Organizer.correctCaseSensitive(newString[:-informationSectionX], cbCharacterType, isCorrectText, searchStrings, isCaseInsensitive, isRegExp)
                        myString += newString[-informationSectionX:]
                    elif self.specialTools.cbInformationSection.currentIndex()==4:
                        myString = newString[:-informationSectionX]
                        myString += Organizer.correctCaseSensitive(newString[-informationSectionX:], cbCharacterType, isCorrectText, searchStrings, isCaseInsensitive, isRegExp)
                    elif self.specialTools.cbInformationSection.currentIndex()==5:
                        myString = newString[:informationSectionX]
                        myString += Organizer.correctCaseSensitive(newString[informationSectionX:informationSectionY], cbCharacterType, isCorrectText, searchStrings, isCaseInsensitive, isRegExp)
                        myString += newString[informationSectionY:]
                    elif self.specialTools.cbInformationSection.currentIndex()==6:
                        myString = Organizer.correctCaseSensitive(newString[:informationSectionX], cbCharacterType, isCorrectText, searchStrings, isCaseInsensitive, isRegExp)
                        myString += newString[informationSectionX:informationSectionY]
                        myString += Organizer.correctCaseSensitive(newString[informationSectionY:], cbCharacterType, isCorrectText, searchStrings, isCaseInsensitive, isRegExp)
                    Universals.MainWindow.Table.item(rowNo,columnNo).setText(trForUI(myString))
            
    
