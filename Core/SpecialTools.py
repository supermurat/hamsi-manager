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

class SpecialTools(MWidget):
    def __init__(self,_parent):
        MWidget.__init__(self, _parent)
        self.tbAddToBefore = MToolButton(self)
        self.btChange = MToolButton(self)
        self.tbAddToAfter = MToolButton(self)
        self.isShowAdvancedSelections = Universals.getBoolValue("isShowAdvancedSelections")
        self.tabwTabs = MTabWidget(self)
        self.specialActions = SpecialActions(self.tabwTabs)
        self.searchAndReplace = SearchAndReplace(self.tabwTabs)
        self.fill = Fill(self.tabwTabs)
        self.clear = Clear(self.tabwTabs)
        self.characterState = CharacterState(self.tabwTabs)
        self.characterEncoding = CharacterEncoding(self.tabwTabs)
        self.quickFill = QuickFill(self.tabwTabs)
        self.pbtnAdvancedSelections = MPushButton("Simple")
        self.pbtnApply = MPushButton(translate("SpecialTools", "Apply"))
        self.pbtnApply.setIcon(MIcon("Images:apply.png"))
        self.pbtnApply.setObjectName("pbtnApply")
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
        VBox1.addStretch(3)
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
        _parent.dckSpecialTools.setObjectName(translate("SpecialTools", "Special Tools"))
        _parent.dckSpecialTools.setWidget(self)
        _parent.dckSpecialTools.setAllowedAreas(Mt.AllDockWidgetAreas)
        _parent.dckSpecialTools.setFeatures(MDockWidget.AllDockWidgetFeatures)
        _parent.addDockWidget(Mt.BottomDockWidgetArea,_parent.dckSpecialTools)
        self.cbInformationSectionX.setEnabled(False)
        self.cbInformationSectionY.setEnabled(False)
        self.cbInformationSection.setFixedWidth(175)
        self.tabwTabs.setCurrentIndex(int(Universals.MySettings["activeTabNoOfSpecialTools"]))
        self.tabChanged(int(Universals.MySettings["activeTabNoOfSpecialTools"]))
        MObject.connect(self.pbtnApply, SIGNAL("clicked()"), self.apply)
        MObject.connect(self.pbtnAdvancedSelections, SIGNAL("clicked()"), self.showOrHideAdvancedSelections)
        MObject.connect(self.tabwTabs, SIGNAL("currentChanged(int)"), self.tabChanged)
        MObject.connect(self.cbInformationSection, SIGNAL("currentIndexChanged(int)"), self.InformationSectionChanged)
        self.refreshForColumns()
        self.reFillCompleters()
        
    def InformationSectionChanged(self):
        if self.cbInformationSection.currentIndex()==0:
            self.cbInformationSectionX.setEnabled(False)
        else:
            self.cbInformationSectionX.setEnabled(True)
        if self.cbInformationSection.currentIndex()>4:
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
        except:pass
        try:
            for lbl in self.quickFill.lblColumns:
                lbl.setVisible(False)
                lbl.deleteLater()
            for le in self.quickFill.leColumns:
                le.setVisible(False)
                le.deleteLater()
        except:pass
        self.specialActions.pbtnAddObjects=[]
        self.quickFill.lblColumns=[]
        self.quickFill.leColumns=[]
        self.searchAndReplace.columns.addItem(translate("SpecialTools", "All"))
        self.clear.columns.addItem(translate("SpecialTools", "All"))
        self.characterState.columns.addItem(translate("SpecialTools", "All"))
        self.characterEncoding.columns.addItem(translate("SpecialTools", "All"))
        for columnName in Universals.MainWindow.Table.tableColumns:
            self.searchAndReplace.columns.addItem(columnName)
            self.fill.columns.addItem(columnName)
            self.clear.columns.addItem(columnName)
            self.characterState.columns.addItem(columnName)
            self.characterEncoding.columns.addItem(columnName)
            tb = SpecialActionsCommandButton(self, Universals.MainWindow.Table.getColumnKeyFromName(columnName))
            self.specialActions.pbtnAddObjects.append(tb)
            lbl = MLabel(columnName + ":")
            self.quickFill.lblColumns.append(lbl)
            le = MLineEdit("")
            le.setObjectName(columnName)
            self.quickFill.leColumns.append(le)
            MObject.connect(self.quickFill.leColumns[-1], SIGNAL("textChanged(const QString&)"), self.quickFill.fillAfter)
        for x in range(0, len(self.specialActions.pbtnAddObjects)):
            self.specialActions.specialActionsCommandContainerAvailable.HBox.addWidget(self.specialActions.pbtnAddObjects[x])
            self.quickFill.HBoxs[0].addWidget(self.quickFill.lblColumns[x])
            self.quickFill.HBoxs[0].addWidget(self.quickFill.leColumns[x])
        self.specialActions.refreshBookmarks()
        if self.isShowAdvancedSelections==False:
            self.hideAdvancedSelections()
        else:
            self.showAdvancedSelections()
        
    def changeTypeChanged(self):
        self.clearChangeTypes()
        if self.sender().toolTip()==translate("SpecialTools", "Add In Front"):
            self.tbAddToBefore.setChecked(True)
        elif self.sender().toolTip()==translate("SpecialTools", "Change"):
            self.btChange.setChecked(True)
        elif self.sender().toolTip()==translate("SpecialTools", "Append"):
            self.tbAddToAfter.setChecked(True)
    
    def clearChangeTypes(self):
        self.tbAddToBefore.setChecked(False)
        self.btChange.setChecked(False)
        self.tbAddToAfter.setChecked(False)
    
    def tabChanged(self, _index):
        Universals.setMySetting("activeTabNoOfSpecialTools", str(_index))
        self.pbtnApply.setEnabled(True)
        self.tbAddToBefore.setEnabled(True)
        self.tbAddToAfter.setEnabled(True)
        if _index==0:
            self.cbInformationSection.setCurrentIndex(0)
            self.cbInformationSection.setEnabled(False)
        elif _index==1:
            self.cbInformationSection.setEnabled(True)
            self.clearChangeTypes()
            self.btChange.setChecked(True)
        elif _index==2:
            self.cbInformationSection.setCurrentIndex(0)
            self.cbInformationSection.setEnabled(False)
        elif _index==3:
            self.cbInformationSection.setEnabled(True)
            self.clearChangeTypes()
            self.btChange.setChecked(True)
            self.tbAddToBefore.setEnabled(False)
            self.tbAddToAfter.setEnabled(False)
        elif _index==4:
            self.cbInformationSection.setEnabled(True)
            self.clearChangeTypes()
            self.btChange.setChecked(True)
            self.tbAddToBefore.setEnabled(False)
            self.tbAddToAfter.setEnabled(False)
        elif _index==5:
            self.cbInformationSection.setCurrentIndex(0)
            self.cbInformationSection.setEnabled(False)
            self.clearChangeTypes()
            self.btChange.setChecked(True)
            self.tbAddToBefore.setEnabled(False)
            self.tbAddToAfter.setEnabled(False)
        elif _index==6:
            self.cbInformationSection.setCurrentIndex(0)
            self.cbInformationSection.setEnabled(False)
            self.pbtnApply.setEnabled(False)
        
    def showOrHideAdvancedSelections(self):
        try:
            if self.isShowAdvancedSelections == False:
                self.showAdvancedSelections()
            else:
                self.hideAdvancedSelections()
        except:
            ReportBug.ReportBug()
    
    def showAdvancedSelections(self):
        self.pbtnAdvancedSelections.setText(translate("SpecialTools", "Simple"))
        self.pnlAdvancedSelections.setVisible(True)
        self.isShowAdvancedSelections = True
        self.tabwTabs.setMaximumHeight(155)
        self.setMaximumHeight(155)
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
            self.checkCompleters()
            self.reFillCompleters()
            Universals.MainWindow.Table.createHistoryPoint()
            if self.tabwTabs.currentIndex()==0:
                if Organizer.whatDoesSpecialCommandDo(self.specialActions.getActionCommand())==True:
                    Organizer.applySpecialCommand(self.specialActions.getActionCommand(), self)
            elif self.tabwTabs.currentIndex()==1:
                Organizer.searchAndReplaceTable(str(self.searchAndReplace.leSearch.text()),str(self.searchAndReplace.leReplace.text()), self)
            elif self.tabwTabs.currentIndex()==2:
                Organizer.fillTable(self.fill.columns.currentText(), self, str(self.fill.leFill.text()))
            elif self.tabwTabs.currentIndex()==3:
                Organizer.clearTable(self)
            elif self.tabwTabs.currentIndex()==4:
                Organizer.correctCaseSensitiveTable(self)
            elif self.tabwTabs.currentIndex()==5:
                Organizer.correctCharacterEncodingTable(self)
            elif self.tabwTabs.currentIndex()==6:
                pass
        except:
            ReportBug.ReportBug()
    
    def checkCompleters(self):
        if Universals.getBoolValue("isActiveCompleter"):
            self.specialActions.checkCompleters()
            self.searchAndReplace.checkCompleters()
            self.fill.checkCompleters()
            self.clear.checkCompleters()
            self.characterState.checkCompleters()
            self.characterEncoding.checkCompleters()
            self.quickFill.checkCompleters()
    
    def reFillCompleters(self):
        if Universals.getBoolValue("isActiveCompleter"):
            self.specialActions.reFillCompleters()
            self.searchAndReplace.reFillCompleters()
            self.fill.reFillCompleters()
            self.clear.reFillCompleters()
            self.characterState.reFillCompleters()
            self.characterEncoding.reFillCompleters()
            self.quickFill.reFillCompleters()
    
class SpecialActions(MWidget):
    def __init__(self, _parent):
        MWidget.__init__(self, _parent)
        self.pbtnAddObjects = []
        lblSplit = MLabel(">>>", self)
        self.cbBookmarks = MComboBox()
        self.tbClear = MToolButton(self)
        self.tbAddBookmark = MToolButton(self)
        self.tbDeleteBookmark = MToolButton(self)
        self.tbWhatDoesThisCommandDo = MToolButton(self)
        self.tbClear.setToolTip(translate("SpecialTools", "Clear"))
        self.tbAddBookmark.setToolTip(translate("SpecialTools", "Add To Bookmarks"))
        self.tbDeleteBookmark.setToolTip(translate("SpecialTools", "Remove From Bookmarks"))
        self.tbWhatDoesThisCommandDo.setToolTip(translate("SpecialTools", "What Does This Command Do?"))
        self.tbClear.setIcon(MIcon("Images:actionClear.png"))
        self.tbAddBookmark.setIcon(MIcon("Images:addBookmark.png"))
        self.tbDeleteBookmark.setIcon(MIcon("Images:actionDelete.png"))
        self.tbWhatDoesThisCommandDo.setIcon(MIcon("Images:whatDoesThisCommandDo.png"))
        self.tbClear.setAutoRaise(True)
        self.tbAddBookmark.setAutoRaise(True)
        self.tbDeleteBookmark.setAutoRaise(True)
        self.tbWhatDoesThisCommandDo.setAutoRaise(True)
        self.tbDeleteBookmark.setEnabled(False)
        MObject.connect(self.cbBookmarks, SIGNAL("currentIndexChanged(int)"), self.cbBookmarksChanged)
        MObject.connect(self.tbClear, SIGNAL("clicked()"), self.makeClear)
        MObject.connect(self.tbWhatDoesThisCommandDo, SIGNAL("clicked()"), self.whatDoesThisCommandDo)
        MObject.connect(self.tbAddBookmark, SIGNAL("clicked()"), self.addBookmark)
        MObject.connect(self.tbDeleteBookmark, SIGNAL("clicked()"), self.deleteBookmark)
        
        self.specialActionsCommandContainerAvailable = SpecialActionsCommandContainer(self, True)
        
        self.specialActionsCommandContainerLeft = SpecialActionsCommandContainer(self)
        self.specialActionsCommandContainerRight = SpecialActionsCommandContainer(self)
        
        self.HBoxs = []
        self.HBoxs.append(MHBoxLayout())
        self.HBoxs[0].addWidget(self.cbBookmarks)
        self.HBoxs[0].addWidget(self.tbDeleteBookmark)
        self.HBoxs.append(MHBoxLayout())
        self.HBoxs[1].addWidget(self.specialActionsCommandContainerAvailable)
        self.HBoxs.append(MHBoxLayout())
        self.HBoxs[2].addWidget(self.specialActionsCommandContainerLeft, 10)
        self.HBoxs[2].addWidget(lblSplit, 1)
        self.HBoxs[2].addWidget(self.specialActionsCommandContainerRight, 10)
        self.HBoxs[2].addWidget(self.tbClear, 1)
        self.HBoxs[2].addWidget(self.tbAddBookmark, 1)
        self.HBoxs[2].addWidget(self.tbWhatDoesThisCommandDo, 1)
        self.HBoxs.append(MHBoxLayout())
        vblSpecialActions = MVBoxLayout()
        vblSpecialActions.addLayout(self.HBoxs[0])
        vblSpecialActions.addLayout(self.HBoxs[1])
        vblSpecialActions.addLayout(self.HBoxs[2])
        self.setLayout(vblSpecialActions)
        self.cbBookmarks.setSizeAdjustPolicy(MComboBox.AdjustToMinimumContentsLength)
        self.refreshBookmarks()
            
    def showAdvancedSelections(self):
        for btn in self.pbtnAddObjects:
            btn.show()
        self.tbClear.show()
        self.tbWhatDoesThisCommandDo.show()
        self.tbAddBookmark.show()
        self.tbDeleteBookmark.show()
    
    def hideAdvancedSelections(self):
        for btn in self.pbtnAddObjects:
            btn.hide()
        self.tbClear.hide()
        self.tbWhatDoesThisCommandDo.hide()
        self.tbAddBookmark.hide()
        self.tbDeleteBookmark.hide()
        
    def getActionCommand(self):
        leftKeys = []
        for child in Universals.getAllChildren(self.specialActionsCommandContainerLeft):
            objectName = str(child.objectName())
            if objectName not in ["", "MoveHere"]:
                leftKeys.append(objectName)
        rightKeys = []
        for child in Universals.getAllChildren(self.specialActionsCommandContainerRight):
            objectName = str(child.objectName())
            if objectName not in ["", "MoveHere"]:
                rightKeys.append(objectName)
        return leftKeys + ["~||~"] + rightKeys
        
    def setActionCommand(self, _actionCommand):
        spliterIndex = _actionCommand.index("~||~")
        leftKeys = _actionCommand[:spliterIndex]
        rightKeys = _actionCommand[spliterIndex+1:]
        for objectName in leftKeys:
            child = Universals.getChild(self.specialActionsCommandContainerAvailable, objectName)
            self.specialActionsCommandContainerLeft.HBox.addWidget(child)
        for objectName in rightKeys:
            child = Universals.getChild(self.specialActionsCommandContainerAvailable, objectName)
            self.specialActionsCommandContainerRight.HBox.addWidget(child)
            
    def makeClear(self):
        try:
            for child in Universals.getAllChildren(self.specialActionsCommandContainerLeft):
                objectName = str(child.objectName())
                if objectName not in ["", "MoveHere"]:
                    self.specialActionsCommandContainerAvailable.HBox.addWidget(child)
            for child in Universals.getAllChildren(self.specialActionsCommandContainerRight):
                objectName = str(child.objectName())
                if objectName not in ["", "MoveHere"]:
                    self.specialActionsCommandContainerAvailable.HBox.addWidget(child)
        except:
            ReportBug.ReportBug()
    
    def whatDoesThisCommandDo(self):
        try:
            Organizer.whatDoesSpecialCommandDo(self.getActionCommand(), True)
        except:
            ReportBug.ReportBug()
            
    def cbBookmarksChanged(self,_index):
        try:
            self.makeClear()
            if _index>0:
                self.setActionCommand(eval(str(Databases.BookmarksOfSpecialTools.fetchAllByType()[_index-1][2])))
                self.tbDeleteBookmark.setEnabled(True)
            else:
                self.tbDeleteBookmark.setEnabled(False)
        except:
            ReportBug.ReportBug()
        
    def addBookmark(self):
        try:
            if Organizer.whatDoesSpecialCommandDo(self.getActionCommand())==True:
                Databases.BookmarksOfSpecialTools.insert(str(self.getActionCommand()))
                self.refreshBookmarks()
                self.cbBookmarks.setCurrentIndex(self.cbBookmarks.count()-1)
        except:
            ReportBug.ReportBug()
           
    def deleteBookmark(self):
        try:
            if self.cbBookmarks.currentIndex()!=-1 and self.cbBookmarks.currentIndex()!=0:
                Databases.BookmarksOfSpecialTools.delete(Databases.BookmarksOfSpecialTools.fetchAllByType()[self.cbBookmarks.currentIndex()-1][0])
                self.refreshBookmarks()
        except:
            ReportBug.ReportBug()
            
    def refreshBookmarks(self):
        try:
            self.makeClear()
            self.cbBookmarks.clear()
            self.cbBookmarks.addItem(translate("SpecialTools", "Please Select An Action!"))
            for fav in Databases.BookmarksOfSpecialTools.fetchAllByType():
                self.cbBookmarks.addItem(trForUI(fav[1]))
        except:
            ReportBug.ReportBug()
    
    def checkCompleters(self):
        pass
        
    def reFillCompleters(self):
        pass
    
    
class SearchAndReplace(MWidget):
    def __init__(self, _parent):
        MWidget.__init__(self, _parent)
        self.lblSearch=MLabel(translate("SpecialTools", "Search: "))
        self.lblReplace=MLabel(translate("SpecialTools", "Replace: "))
        self.leSearch = MLineEdit("")
        self.leReplace = MLineEdit("")
        lblColumns = MLabel(translate("SpecialTools", "Column: "))
        srExamples = translate("SpecialTools", "<table><tr><td><nobr>Before</nobr></td><td>>></td><td><nobr>Search</nobr></td><td>-</td><td><nobr>Replace</nobr></td><td>>></td><td><nobr>After</nobr></td></tr>" +
                                 "<tr><td><nobr>HamsiManager</nobr></td><td>>></td><td><nobr>ager</nobr></td><td>-</td><td><nobr></nobr></td><td>>></td><td><nobr>HamsiMan</nobr></td></tr>" +
                                 "</table><table>")
        sExample=translate("SpecialTools", "<tr><td><nobr>Example: \"search 1<b>;</b>search 2<b>;</b>search 3<b>;</b>...<b>;</b>search n<b>;</b>\"</nobr></td></tr>")
        rExample=translate("SpecialTools", "<tr><td><nobr>Example: \"Change/replace 1<b>;</b>Change/replace 2<b>;</b>Change/replace 3<b>;</b>...<b>;</b>Change/replace n<b>;</b>\"</nobr></td></tr>")
        self.cckbCaseInsensitive = MCheckBox(translate("SpecialTools", "Case Insensitive"))
        self.cckbCaseInsensitive.setChecked(True)
        self.cckbRegExp = MCheckBox(translate("SpecialTools", "Regular Expression (RegExp)"))
        self.leSearch.setToolTip(trForUI(srExamples+sExample+"</table>"))
        self.leReplace.setToolTip(trForUI(srExamples+rExample+"</table>"))
        self.columns = MComboBox()
        self.columns.addItem(translate("SpecialTools", "All"))
        self.pbtnEditValueForSearch = MPushButton(translate("Options", "*"))
        self.pbtnEditValueForSearch.setObjectName(trForUI(translate("Options", "Edit Values With Advanced Value Editor") + "For Search"))
        self.pbtnEditValueForSearch.setToolTip(translate("Options", "Edit values with Advanced Value Editor"))
        self.pbtnEditValueForSearch.setFixedWidth(25)
        MObject.connect(self.pbtnEditValueForSearch, SIGNAL("clicked()"), self.pbtnEditValueClicked)
        self.pbtnEditValueForReplace = MPushButton(translate("Options", "*"))
        self.pbtnEditValueForReplace.setObjectName(trForUI(translate("Options", "Edit Values With Advanced Value Editor") + "For Replace"))
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
        

class Fill(MWidget):
    def __init__(self, _parent):
        MWidget.__init__(self, _parent)
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
       
class Clear(MWidget):
    def __init__(self, _parent):
        MWidget.__init__(self, _parent)
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
        if self.cbClearType.currentIndex()!=4:
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
            
class CharacterState(MWidget):
    def __init__(self, _parent):
        MWidget.__init__(self, _parent)
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
        
        
class CharacterEncoding(MWidget):
    def __init__(self, _parent):
        MWidget.__init__(self, _parent)
        self.cckbCorrectText = MCheckBox(translate("SpecialTools", "Character Encoding"))
        lblColumns = MLabel(translate("SpecialTools", "Column: "))
        lblSourceValues = MLabel(translate("SpecialTools", "Source Values : "))
        lblSourceEncoding = MLabel(translate("SpecialTools", "Source Encoding : "))
        lblDestinationEncoding = MLabel(translate("SpecialTools", "Destination Encoding : "))
        self.columns = MComboBox()
        self.cbSourceEncoding = MComboBox()
        self.cbSourceEncoding.addItems(Variables.getCharSets())
        self.cbDestinationEncoding = MComboBox()
        self.cbDestinationEncoding.addItems(Variables.getCharSets())
        self.cbSourceEncoding.setCurrentIndex(self.cbSourceEncoding.findText(Universals.MySettings["fileSystemEncoding"]))
        self.cbDestinationEncoding.setCurrentIndex(self.cbDestinationEncoding.findText(Universals.MySettings["fileSystemEncoding"]))
        self.cbSourceValues = MComboBox()
        self.cbSourceValues.addItems([translate("Options", "Real Values"), 
                            translate("Options", "Table Contents")])
        HBoxs = []
        HBoxs.append(MHBoxLayout())
        HBoxs[0].addWidget(lblColumns)
        HBoxs[0].addWidget(self.columns)
        HBoxs[0].addWidget(lblSourceValues)
        HBoxs[0].addWidget(self.cbSourceValues)
        HBoxs.append(MHBoxLayout())
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
            
class QuickFill(MWidget):
    def __init__(self, _parent):
        MWidget.__init__(self, _parent)
        self.lblColumns = []
        self.leColumns = []
        self.tmrFillAfter = None
        self.HBoxs = []
        self.HBoxs.append(MHBoxLayout())
        self.HBoxs.append(MHBoxLayout())
        self.HBoxs.append(MHBoxLayout())
        self.HBoxs.append(MHBoxLayout())
        vblFill = MVBoxLayout()
        vblFill.addLayout(self.HBoxs[0])
        vblFill.addLayout(self.HBoxs[1])
        vblFill.addLayout(self.HBoxs[2])
        vblFill.addLayout(self.HBoxs[3])
        self.setLayout(vblFill)
        
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
            Universals.MainWindow.Table.createHistoryPoint()
            Organizer.quickFillTable(str(self.fillFrom.objectName()), self.parent().parent().parent(), str(self.fillFrom.text()))
        except:
            from Core import ReportBug
            ReportBug.ReportBug()
            
            
class SearchAndReplaceListEditDialog(MDialog):
    def __init__(self, _parent):
        MDialog.__init__(self, _parent)
        if Universals.isActivePyKDE4==True:
            self.setButtons(MDialog.NoDefault)
        self.setWindowTitle(translate("SearchAndReplaceListEditDialog", "Advanced Value Editor"))
        currentValueForSearch = str(self.parent().leSearch.text())
        currentValueForReplace = str(self.parent().leReplace.text())
        if Universals.isActivePyKDE4==True:
            self.EditorWidgetForSearch = MEditListBox(self)
            self.EditorWidgetForSearch.setItems([trForUI(x) for x in currentValueForSearch.split(";")])
            self.EditorWidgetForReplace = MEditListBox(self)
            self.EditorWidgetForReplace.setItems([trForUI(x) for x in currentValueForReplace.split(";")])
        else:
            self.EditorWidgetForSearch = MTextEdit(self)
            self.EditorWidgetForSearch.setText(trForUI(currentValueForSearch.replace(";", "\n")))
            self.EditorWidgetForReplace = MTextEdit(self)
            self.EditorWidgetForReplace.setText(trForUI(currentValueForReplace.replace(";", "\n")))
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
        if Universals.isActivePyKDE4==True:
            self.setMainWidget(pnlMain)
        else:
            self.setLayout(vblMain)
        self.setMinimumSize(550, 400)
        self.show()
        
    def apply(self):
        valueForSearch = ""
        valueForReplace = ""
        if Universals.isActivePyKDE4==True:
            for y, info in enumerate(self.EditorWidgetForSearch.items()):
                if y!=0:
                    valueForSearch += ";"
                valueForSearch += str(info)
            for y, info in enumerate(self.EditorWidgetForReplace.items()):
                if y!=0:
                    valueForReplace += ";"
                valueForReplace += str(info)
        else:
            valueForSearch = str(self.EditorWidgetForSearch.toPlainText()).replace("\n", ";")
            valueForReplace = str(self.EditorWidgetForReplace.toPlainText()).replace("\n", ";")
        self.parent().leSearch.setText(trForUI(valueForSearch))
        self.parent().leReplace.setText(trForUI(valueForReplace))
        self.close()
        
class SpecialActionsCommandContainer(MWidget):
    def __init__(self, _parent, _isForAvailable=False):
        MWidget.__init__(self, _parent)
        self.isForAvailable = _isForAvailable
        self.setAcceptDrops(True)
        self.HBox = MHBoxLayout()
        self.lblMoveHere = MLabel(translate("SpecialActionsCommandContainer", "Move Here"), self)
        self.lblMoveHere.setObjectName("MoveHere")
        self.HBox.addWidget(self.lblMoveHere)
        self.setLayout(self.HBox)
        self.checkLabelMoveHere()
        self.setMinimumWidth(200)
    
    def dragEnterEvent(self, _e):
        if _e.mimeData().hasFormat("SpecialActionsCommandButton"):
            _e.accept()
        
    def dropEvent(self, _e):
        #baData = _e.mimeData().data("SpecialActionsCommandButton")
        #objectNameOfButton = str(baData)
        btn = _e.source()
        self.HBox.addWidget(btn)
        self.checkLabelMoveHere()
        _e.accept()
        
    def checkLabelMoveHere(self):
        if self.isForAvailable == False and self.HBox.count()==1:
            self.lblMoveHere.show()
        else:
            self.lblMoveHere.hide()
        
class SpecialActionsCommandButton(MPushButton):
    def __init__(self, _parent, _columnName):
        MPushButton.__init__(self, _parent)
        self.setText(Universals.MainWindow.Table.getColumnNameFromKey(_columnName))
        self.setObjectName(_columnName)

    def mouseMoveEvent(self, _e):
        if _e.buttons() != QtCore.Qt.LeftButton:
            return
        mimeData = QtCore.QMimeData()
        baData = MByteArray()
        baData.append(self.objectName())
        mimeData.setData("SpecialActionsCommandButton", baData)
        drag = QtGui.QDrag(self)
        drag.setMimeData(mimeData)
        dropAction = drag.start(QtCore.Qt.MoveAction)
        
    def mousePressEvent(self, _e):
        MPushButton.mousePressEvent(self, _e)

            
    
    
