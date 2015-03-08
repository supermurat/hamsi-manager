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


from Core import Universals as uni
from Core.MyObjects import *


class CharacterEncoding(MWidget):
    def __init__(self, _parent):
        MWidget.__init__(self, _parent)
        self.specialTools = _parent
        self.cckbCorrectText = MCheckBox(translate("SpecialTools", "Character Encoding"))
        lblColumns = MLabel(translate("SpecialTools", "Column: "))
        lblSourceValues = MLabel(translate("SpecialTools", "Source Values : "))
        lblSourceEncoding = MLabel(translate("SpecialTools", "Source Encoding : "))
        lblDestinationEncoding = MLabel(translate("SpecialTools", "Destination Encoding : "))
        self.columns = MyComboBox()
        self.cbSourceEncoding = MComboBox()
        self.cbSourceEncoding.addItems(uni.getCharSets())
        self.cbDestinationEncoding = MComboBox()
        self.cbDestinationEncoding.addItems(uni.getCharSets())
        self.cbSourceEncoding.setCurrentIndex(self.cbSourceEncoding.findText(uni.MySettings["fileSystemEncoding"]))
        self.cbDestinationEncoding.setCurrentIndex(
            self.cbDestinationEncoding.findText(uni.MySettings["fileSystemEncoding"]))
        self.cbSourceValues = MComboBox()
        self.cbSourceValues.addItems([translate("Options", "Real Values"),
                                      translate("Options", "Table Contents")])
        HBoxs = [MHBoxLayout(), MHBoxLayout()]
        HBoxs[0].addWidget(lblColumns)
        HBoxs[0].addWidget(self.columns)
        HBoxs[0].addWidget(lblSourceValues)
        HBoxs[0].addWidget(self.cbSourceValues)
        HBoxs[1].addWidget(lblSourceEncoding)
        HBoxs[1].addWidget(self.cbSourceEncoding)
        HBoxs[1].addWidget(lblDestinationEncoding)
        HBoxs[1].addWidget(self.cbDestinationEncoding)
        vblCharacterEncoding = MVBoxLayout()
        vblCharacterEncoding.addLayout(HBoxs[0])
        vblCharacterEncoding.addLayout(HBoxs[1])
        self.setLayout(vblCharacterEncoding)
        lblColumns.setFixedWidth(60)

    def showAdvancedSelections(self):
        pass

    def hideAdvancedSelections(self):
        pass

    def checkCompleters(self):
        pass

    def reFillCompleters(self):
        pass

    def apply(self):
        self.checkCompleters()
        self.reFillCompleters()
        getMainTable().createHistoryPoint()
        getMainTable().isAskShowHiddenColumn = True
        sourceEncoding = str(self.cbSourceEncoding.currentText())
        destinationEncoding = str(self.cbDestinationEncoding.currentText())
        sourceValues = str(self.cbSourceValues.currentText())
        isUseRealValues = (sourceValues == translate("Options", "Real Values"))
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
                    if isUseRealValues:
                        newString = str(getMainTable().values[rowNo][columnKey])
                    else:
                        newString = str(getMainTable().item(rowNo, columnNo).text())
                    myString = ""
                    try:
                        myString = uni.trDecode(newString, sourceEncoding, "ignore")
                    except:
                        pass
                    try:
                        myString = str(uni.trEncode(myString, destinationEncoding, "ignore"))
                    except:
                        pass
                    getMainTable().item(rowNo, columnNo).setText(str(myString))
