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
from SpecialTools import SpecialActions
from SpecialTools import SearchAndReplace
from SpecialTools import Fill
from SpecialTools import Clear
from SpecialTools import CharacterState
from SpecialTools import CharacterEncoding
from SpecialTools import QuickFill


class SpecialTools(MWidget):
    def __init__(self, _parent):
        MWidget.__init__(self, _parent)
        self.tbAddToBefore = MToolButton(self)
        self.btChange = MToolButton(self)
        self.tbAddToAfter = MToolButton(self)
        self.isShowAdvancedSelections = uni.getBoolValue("isShowAdvancedSelections")
        self.tabwTabs = MTabWidget(self)
        self.specialActions = SpecialActions.SpecialActions(self)
        self.searchAndReplace = SearchAndReplace.SearchAndReplace(self)
        self.fill = Fill.Fill(self)
        self.clear = Clear.Clear(self)
        self.characterState = CharacterState.CharacterState(self)
        self.characterEncoding = CharacterEncoding.CharacterEncoding(self)
        self.quickFill = QuickFill.QuickFill(self)
        self.pbtnAdvancedSelections = MPushButton("Simple")
        self.pbtnApply = MPushButton(translate("SpecialTools", "Apply"))
        self.pbtnApply.setIcon(MIcon("Images:apply.png"))
        self.pbtnApply.setObjectName("pbtnApply")
        self.pbtnApply.setMinimumHeight(35)
        self.tbAddToBefore.setToolTip(translate("SpecialTools", "Add In Front"))
        self.btChange.setToolTip(translate("SpecialTools", "Change"))
        self.tbAddToAfter.setToolTip(translate("SpecialTools", "Append"))
        self.tbAddToBefore.setIcon(MIcon("Images:addToBefore.png"))
        self.btChange.setIcon(MIcon("Images:change.png"))
        self.tbAddToAfter.setIcon(MIcon("Images:addToAfter.png"))
        self.tbAddToBefore.setAutoRaise(True)
        self.btChange.setAutoRaise(True)
        self.tbAddToAfter.setAutoRaise(True)
        self.tbAddToBefore.setCheckable(True)
        self.btChange.setCheckable(True)
        self.tbAddToAfter.setCheckable(True)
        self.btChange.setChecked(True)
        MObject.connect(self.tbAddToBefore, SIGNAL("clicked()"), self.changeTypeChanged)
        MObject.connect(self.btChange, SIGNAL("clicked()"), self.changeTypeChanged)
        MObject.connect(self.tbAddToAfter, SIGNAL("clicked()"), self.changeTypeChanged)
        self.tabwTabs.addTab(self.specialActions, translate("SpecialTools", "Special Actions"))
        self.tabwTabs.addTab(self.searchAndReplace, translate("SpecialTools", "Search - Replace"))
        self.tabwTabs.addTab(self.fill, translate("SpecialTools", "Fill"))
        self.tabwTabs.addTab(self.clear, translate("SpecialTools", "Clear"))
        self.tabwTabs.addTab(self.characterState, translate("SpecialTools", "Character State"))
        self.tabwTabs.addTab(self.characterEncoding, translate("SpecialTools", "Character Encoding"))
        self.tabwTabs.addTab(self.quickFill, translate("SpecialTools", "Quick Fill"))
        HBox0 = MHBoxLayout()
        HBox0.addWidget(self.tbAddToBefore)
        HBox0.addWidget(self.btChange)
        HBox0.addWidget(self.tbAddToAfter)
        lblX = MLabel(translate("SpecialTools", "X : "))
        lblY = MLabel(translate("SpecialTools", "Y : "))
        self.cbInformationSection = MComboBox()
        self.cbInformationSection.addItems([translate("SpecialTools", "All"),
                                            translate("SpecialTools", "Before X"),
                                            translate("SpecialTools", "After X"),
                                            translate("SpecialTools", "From Last, Before X"),
                                            translate("SpecialTools", "From Last After X"),
                                            translate("SpecialTools", "Between X And Y"),
                                            translate("SpecialTools", "Not Between X And Y")])
        self.cbInformationSectionX = MSpinBox()
        self.cbInformationSectionX.setRange(1, 100)
        self.cbInformationSectionX.setValue(3)
        self.cbInformationSectionY = MSpinBox()
        self.cbInformationSectionY.setRange(1, 100)
        self.cbInformationSectionY.setValue(5)
        self.pnlAdvancedSelections = MWidget()
        VBox = MVBoxLayout()
        self.pnlAdvancedSelections.setLayout(VBox)
        VBox1 = MVBoxLayout()
        VBox1.addWidget(self.pbtnAdvancedSelections)
        VBox.addWidget(self.cbInformationSection)
        HBoxs1 = MHBoxLayout()
        HBoxs1.addWidget(lblX)
        HBoxs1.addWidget(self.cbInformationSectionX)
        HBoxs1.addWidget(lblY)
        HBoxs1.addWidget(self.cbInformationSectionY)
        VBox.addLayout(HBoxs1)
        VBox.addLayout(HBox0)
        VBox1.addWidget(self.pnlAdvancedSelections)
        VBox1.addWidget(self.pbtnApply)
        HBox = MHBoxLayout()
        HBox.addWidget(self.tabwTabs)
        HBox.addLayout(VBox1)
        self.setLayout(HBox)
        _parent.dckSpecialTools = MDockWidget(translate("SpecialTools", "Special Tools"))
        _parent.dckSpecialTools.setObjectName("Special Tools")
        _parent.dckSpecialTools.setWidget(self)
        _parent.dckSpecialTools.setAllowedAreas(Mt.AllDockWidgetAreas)
        _parent.dckSpecialTools.setFeatures(MDockWidget.AllDockWidgetFeatures)
        _parent.addDockWidget(Mt.BottomDockWidgetArea, _parent.dckSpecialTools)
        self.cbInformationSectionX.setEnabled(False)
        self.cbInformationSectionY.setEnabled(False)
        self.cbInformationSection.setFixedWidth(175)
        self.tabwTabs.setCurrentIndex(int(uni.MySettings["activeTabNoOfSpecialTools"]))
        self.tabChanged(int(uni.MySettings["activeTabNoOfSpecialTools"]))
        MObject.connect(self.pbtnApply, SIGNAL("clicked()"), self.apply)
        MObject.connect(self.pbtnAdvancedSelections, SIGNAL("clicked()"), self.showOrHideAdvancedSelections)
        MObject.connect(self.tabwTabs, SIGNAL("currentChanged(int)"), self.tabChanged)
        MObject.connect(self.cbInformationSection, SIGNAL("currentIndexChanged(int)"), self.InformationSectionChanged)
        self.refreshForColumns()
        self.reFillCompleters()

    def InformationSectionChanged(self):
        if self.cbInformationSection.currentIndex() == 0:
            self.cbInformationSectionX.setEnabled(False)
        else:
            self.cbInformationSectionX.setEnabled(True)
        if self.cbInformationSection.currentIndex() > 4:
            self.cbInformationSectionY.setEnabled(True)
        else:
            self.cbInformationSectionY.setEnabled(False)

    def refreshForColumns(self):
        self.searchAndReplace.columns.clear()
        self.fill.columns.clear()
        self.clear.columns.clear()
        self.characterState.columns.clear()
        self.characterEncoding.columns.clear()
        try:
            for btn in self.specialActions.pbtnAddObjects:
                btn.setVisible(False)
                btn.deleteLater()
        except: pass
        try:
            for lbl in self.quickFill.lblColumns:
                lbl.setVisible(False)
                lbl.deleteLater()
            for le in self.quickFill.leColumns:
                le.setVisible(False)
                le.deleteLater()
        except: pass
        self.specialActions.pbtnAddObjects = []
        self.quickFill.lblColumns = []
        self.quickFill.leColumns = []
        self.searchAndReplace.columns.addItem(translate("SpecialTools", "All"), trQVariant("all"))
        self.clear.columns.addItem(translate("SpecialTools", "All"), trQVariant("all"))
        self.characterState.columns.addItem(translate("SpecialTools", "All"), trQVariant("all"))
        self.characterEncoding.columns.addItem(translate("SpecialTools", "All"), trQVariant("all"))
        for columnKey in getMainTable().tableColumnsKey:
            columnName = getMainTable().getColumnNameFromKey(columnKey)
            if columnKey not in getMainTable().tableReadOnlyColumnsKey:
                self.searchAndReplace.columns.addItem(columnName, trQVariant(columnKey))
                self.fill.columns.addItem(columnName, trQVariant(columnKey))
                self.clear.columns.addItem(columnName, trQVariant(columnKey))
                self.characterState.columns.addItem(columnName, trQVariant(columnKey))
                self.characterEncoding.columns.addItem(columnName, trQVariant(columnKey))
                lbl = MLabel(columnName + ":")
                self.quickFill.lblColumns.append(lbl)
                le = MLineEdit("")
                le.setObjectName(columnKey)
                self.quickFill.leColumns.append(le)
                MObject.connect(self.quickFill.leColumns[-1], SIGNAL("textChanged(const QString&)"),
                                self.quickFill.fillAfter)
            tb = SpecialActions.SpecialActionsCommandButton(self.specialActions, columnKey)
            self.specialActions.pbtnAddObjects.append(tb)
        for btn in self.specialActions.pbtnAddObjects:
            self.specialActions.saccAvailable.addToWidgetList(btn)
        for x in range(0, len(self.quickFill.leColumns)):
            if len(self.quickFill.leColumns) < 7:
                columnNo = (x * 2) - (int(x / 2) * (2 * 2))
                self.quickFill.gridLayout.addWidget(self.quickFill.lblColumns[x], int(x / 2), columnNo)
                self.quickFill.gridLayout.addWidget(self.quickFill.leColumns[x], int(x / 2), columnNo + 1)
            else:
                columnNo = (x * 4) - (int(x / 4) * (4 * 4))
                self.quickFill.gridLayout.addWidget(self.quickFill.lblColumns[x], int(x / 4), columnNo)
                self.quickFill.gridLayout.addWidget(self.quickFill.leColumns[x], int(x / 4), columnNo + 1)
        self.specialActions.refreshBookmarks()
        if self.isShowAdvancedSelections is False:
            self.hideAdvancedSelections()
        else:
            self.showAdvancedSelections()

    def changeTypeChanged(self):
        self.clearChangeTypes()
        if self.sender().toolTip() == translate("SpecialTools", "Add In Front"):
            self.tbAddToBefore.setChecked(True)
        elif self.sender().toolTip() == translate("SpecialTools", "Change"):
            self.btChange.setChecked(True)
        elif self.sender().toolTip() == translate("SpecialTools", "Append"):
            self.tbAddToAfter.setChecked(True)

    def clearChangeTypes(self):
        self.tbAddToBefore.setChecked(False)
        self.btChange.setChecked(False)
        self.tbAddToAfter.setChecked(False)

    def tabChanged(self, _index):
        uni.setMySetting("activeTabNoOfSpecialTools", str(_index))
        self.pbtnApply.setEnabled(True)
        self.tbAddToBefore.setEnabled(True)
        self.tbAddToAfter.setEnabled(True)
        if _index == 0:
            self.cbInformationSection.setCurrentIndex(0)
            self.cbInformationSection.setEnabled(False)
        elif _index == 1:
            self.cbInformationSection.setEnabled(True)
            self.clearChangeTypes()
            self.btChange.setChecked(True)
        elif _index == 2:
            self.cbInformationSection.setCurrentIndex(0)
            self.cbInformationSection.setEnabled(False)
        elif _index == 3:
            self.cbInformationSection.setEnabled(True)
            self.clearChangeTypes()
            self.btChange.setChecked(True)
            self.tbAddToBefore.setEnabled(False)
            self.tbAddToAfter.setEnabled(False)
        elif _index == 4:
            self.cbInformationSection.setEnabled(True)
            self.clearChangeTypes()
            self.btChange.setChecked(True)
            self.tbAddToBefore.setEnabled(False)
            self.tbAddToAfter.setEnabled(False)
        elif _index == 5:
            self.cbInformationSection.setCurrentIndex(0)
            self.cbInformationSection.setEnabled(False)
            self.clearChangeTypes()
            self.btChange.setChecked(True)
            self.tbAddToBefore.setEnabled(False)
            self.tbAddToAfter.setEnabled(False)
        elif _index == 6:
            self.cbInformationSection.setCurrentIndex(0)
            self.cbInformationSection.setEnabled(False)
            self.pbtnApply.setEnabled(False)

    def showOrHideAdvancedSelections(self):
        try:
            if self.isShowAdvancedSelections is False:
                self.showAdvancedSelections()
            else:
                self.hideAdvancedSelections()
        except:
            ReportBug.ReportBug()

    def showAdvancedSelections(self):
        self.pbtnAdvancedSelections.setText(translate("SpecialTools", "Simple"))
        self.pnlAdvancedSelections.setVisible(True)
        self.isShowAdvancedSelections = True
        if uni.isWindows:
            self.tabwTabs.setMaximumHeight(235)
            self.setMaximumHeight(235)
        else:
            self.tabwTabs.setMaximumHeight(205)
            self.setMaximumHeight(205)
        self.specialActions.showAdvancedSelections()
        self.fill.showAdvancedSelections()
        self.searchAndReplace.showAdvancedSelections()
        self.clear.showAdvancedSelections()
        self.characterState.showAdvancedSelections()
        self.characterEncoding.showAdvancedSelections()
        self.quickFill.showAdvancedSelections()

    def hideAdvancedSelections(self):
        self.pbtnAdvancedSelections.setText(translate("SpecialTools", "Advance"))
        self.cbInformationSection.setCurrentIndex(0)
        self.pnlAdvancedSelections.setVisible(False)
        self.isShowAdvancedSelections = False
        self.tabwTabs.setMaximumHeight(100)
        self.setMaximumHeight(100)
        self.specialActions.hideAdvancedSelections()
        self.fill.hideAdvancedSelections()
        self.searchAndReplace.hideAdvancedSelections()
        self.clear.hideAdvancedSelections()
        self.characterState.hideAdvancedSelections()
        self.characterEncoding.hideAdvancedSelections()
        self.quickFill.hideAdvancedSelections()

    def apply(self):
        try:
            if self.tabwTabs.currentIndex() == 0:
                if SpecialActions.whatDoesSpecialCommandDo(self.specialActions.getActionCommand()):
                    self.specialActions.apply()
            elif self.tabwTabs.currentIndex() == 1:
                self.searchAndReplace.apply()
            elif self.tabwTabs.currentIndex() == 2:
                self.fill.apply()
            elif self.tabwTabs.currentIndex() == 3:
                self.clear.apply()
            elif self.tabwTabs.currentIndex() == 4:
                self.characterState.apply()
            elif self.tabwTabs.currentIndex() == 5:
                self.characterEncoding.apply()
            elif self.tabwTabs.currentIndex() == 6:
                pass
        except:
            ReportBug.ReportBug()

    def reFillCompleters(self):
        if uni.getBoolValue("isActiveCompleter"):
            self.specialActions.reFillCompleters()
            self.searchAndReplace.reFillCompleters()
            self.fill.reFillCompleters()
            self.clear.reFillCompleters()
            self.characterState.reFillCompleters()
            self.characterEncoding.reFillCompleters()
            self.quickFill.reFillCompleters()
    
