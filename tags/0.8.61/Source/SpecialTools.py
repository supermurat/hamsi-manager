# -*- coding: utf-8 -*-

import Organizer
import Settings
import Universals
from MyObjects import *
import Tables
import Dialogs
import sys
import ReportBug

class SpecialTools(MWidget):
    def __init__(self,_parent):
        MWidget.__init__(self, _parent)
        self.tbAddToBefore = MToolButton(self)
        self.btChange = MToolButton(self)
        self.tbAddToAfter = MToolButton(self)
        if Universals.windowMode==Universals.windowModeKeys[1]:
            self.isShowAdvancedSelections = False
        else:
            self.isShowAdvancedSelections = Universals.getBoolValue("isShowAdvancedSelections")
        self.tabwTabs = MTabWidget(self)
        self.specialActions = SpecialActions(self.tabwTabs)
        self.searchAndReplace = SearchAndReplace(self.tabwTabs)
        self.fill = Fill(self.tabwTabs)
        self.clear = Clear(self.tabwTabs)
        self.characterState = CharacterState(self.tabwTabs)
        self.pbtnAdvancedSelections = MPushButton(u"Simple")
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
        self.tabwTabs.setCurrentIndex(int(Universals.MySettings["activeTabNoOfSpecialTools"]))
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
        MObject.connect(self.pbtnApply, SIGNAL("clicked()"), self.apply)
        MObject.connect(self.pbtnAdvancedSelections, SIGNAL("clicked()"), self.showOrHideAdvancedSelections)
        MObject.connect(self.tabwTabs, SIGNAL("currentChanged(int)"), self.tabChanged)
        self.cbInformationSectionX.setEnabled(False)
        self.cbInformationSectionY.setEnabled(False)
        self.cbInformationSection.setFixedWidth(175)
        MObject.connect(self.cbInformationSection, SIGNAL("currentIndexChanged(int)"), self.InformationSectionChanged)
        self.refreshForTableColumns()
        
    def InformationSectionChanged(self):
        if self.cbInformationSection.currentIndex()==0:
            self.cbInformationSectionX.setEnabled(False)
        else:
            self.cbInformationSectionX.setEnabled(True)
        if self.cbInformationSection.currentIndex()>4:
            self.cbInformationSectionY.setEnabled(True)
        else:
            self.cbInformationSectionY.setEnabled(False)
        
    def refreshForTableColumns(self):
        self.searchAndReplace.columns.clear()
        self.fill.columns.clear()
        self.clear.columns.clear()
        self.characterState.columns.clear()
        try:
            for btn in self.specialActions.pbtnAddObjects:
                btn.setVisible(False)
                btn.deleteLater()
        except:pass
        self.specialActions.pbtnAddObjects=[]
        self.searchAndReplace.columns.addItem(translate("SpecialTools", "All"))
        self.clear.columns.addItem(translate("SpecialTools", "All"))
        self.characterState.columns.addItem(translate("SpecialTools", "All"))
        for columnName in Universals.MainWindow.Table.tableColumns:
            self.searchAndReplace.columns.addItem(columnName)
            self.fill.columns.addItem(columnName)
            self.clear.columns.addItem(columnName)
            self.characterState.columns.addItem(columnName)
            tb = MToolButton()
            tb.setText(columnName)
            tb.setObjectName(columnName)
            tb.setAutoRaise(True)
            self.specialActions.pbtnAddObjects.append(tb)
            MObject.connect(self.specialActions.pbtnAddObjects[-1], SIGNAL("clicked()"), self.specialActions.AddObjects)
        try:
            if Universals.tableType==2:
                for x in range(0, 5):
                    self.specialActions.HBoxs[0].addWidget(self.specialActions.pbtnAddObjects[x])
                for x in range(len(self.specialActions.pbtnAddObjects)-1, 4, -1):
                    self.specialActions.HBoxs[1].insertWidget(0, self.specialActions.pbtnAddObjects[x])
            else:
                for btn in self.specialActions.pbtnAddObjects:
                    self.specialActions.HBoxs[0].addWidget(btn)
        except:pass
        self.specialActions.refreshBookmarks()
        if self.isShowAdvancedSelections==False:
            self.hideAdvancedSelections()
        else:
            self.showAdvancedSelections()
        
    def changeTypeChanged(self):
        self.tbAddToBefore.setChecked(False)
        self.btChange.setChecked(False)
        self.tbAddToAfter.setChecked(False)
        if self.sender().toolTip()==translate("SpecialTools", "Add In Front"):
            self.tbAddToBefore.setChecked(True)
        elif self.sender().toolTip()==translate("SpecialTools", "Change"):
            self.btChange.setChecked(True)
        elif self.sender().toolTip()==translate("SpecialTools", "Append"):
            self.tbAddToAfter.setChecked(True)
    
    def tabChanged(self, _index):
        Universals.setMySetting("activeTabNoOfSpecialTools", str(_index))
        self.tbAddToBefore.setEnabled(True)
        self.tbAddToAfter.setEnabled(True)
        if _index==0:
            self.cbInformationSection.setCurrentIndex(0)
            self.cbInformationSection.setEnabled(False)
        elif _index==1:
            self.cbInformationSection.setEnabled(True)
            self.changeTypeChanged()
            self.btChange.setChecked(True)
        elif _index==2:
            self.cbInformationSection.setCurrentIndex(0)
            self.cbInformationSection.setEnabled(False)
        elif _index==3:
            self.cbInformationSection.setEnabled(True)
            self.changeTypeChanged()
            self.btChange.setChecked(True)
            self.tbAddToBefore.setEnabled(False)
            self.tbAddToAfter.setEnabled(False)
        elif _index==4:
            self.cbInformationSection.setEnabled(True)
            self.changeTypeChanged()
            self.btChange.setChecked(True)
            self.tbAddToBefore.setEnabled(False)
            self.tbAddToAfter.setEnabled(False)
        
    def showOrHideAdvancedSelections(self):
        try:
            if self.isShowAdvancedSelections == False:
                self.showAdvancedSelections()
            else:
                self.hideAdvancedSelections()
        except:
            error = ReportBug.ReportBug()
            error.show()
    
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
        
    def apply(self):
        try:
            Universals.MainWindow.Table.createHistoryPoint()
            if self.tabwTabs.currentIndex()==0:
                if Organizer.whatDoesSpecialCommandDo(unicode(self.specialActions.leSplitPointer.text()).encode("utf-8"),
                                            self.specialActions.whereIsSplitPointer,
                                            self.specialActions.actionCommand, 
                                            True)==True:
                    Organizer.applySpecialCommand(unicode(self.specialActions.leSplitPointer.text()).encode("utf-8"),
                                self.specialActions.whereIsSplitPointer,
                                self.specialActions.actionCommand, self)
            elif self.tabwTabs.currentIndex()==1:
                Organizer.searchAndReplaceTable(unicode(self.searchAndReplace.leSearch.text()).encode("utf-8"),unicode(self.searchAndReplace.leReplace.text()).encode("utf-8"), self)
            elif self.tabwTabs.currentIndex()==2:
                Organizer.fillTable(self.fill.columns.currentText(), self, unicode(self.fill.leFill.text()).encode("utf-8"))
            elif self.tabwTabs.currentIndex()==3:
                Organizer.clearTable(self)
            elif self.tabwTabs.currentIndex()==4:
                Organizer.correctCaseSensitiveTable(self)
        except:
            error = ReportBug.ReportBug()
            error.show()
    
class SpecialActions(MWidget):
    def __init__(self, _parent):
        MWidget.__init__(self, _parent)
        self.history, self.future, self.isPressedAddObjects=[], [], False
        self.pbtnAddObjects = []
        self.details = MLabel(translate("SpecialTools", "Please Select An Action!.."))
        self.details.setWordWrap(True)
        self.whereIsSplitPointer, self.numberOfActionCommand, self.commaAndSplitControl="right",0,0
        self.actionCommand = ""
        self.leActionString = MLineEdit("")
        self.leSplitPointer = MLineEdit("-")
        fntFont = MFont()
        fntFont.setPointSize(16)
        fntFont.setBold(True)
        self.leSplitPointer.setFont(fntFont)
        self.cbBookmarks = MComboBox()
        self.refreshBookmarks()
        self.tbAddComma = MToolButton()
        self.tbAddComma.setText(translate("SpecialTools", ","))
        self.tbAddComma.setAutoRaise(True)
        self.tbAddSplit = MToolButton()
        self.tbAddSplit.setText(translate("SpecialTools", "Hyphen(-)"))
        self.tbAddSplit.setAutoRaise(True)
        self.tbClear = MToolButton(self)
        self.tbAddBookmark = MToolButton(self)
        self.tbDeleteBookmark = MToolButton(self)
        self.tbGoBack = MToolButton(self)
        self.tbGoForward = MToolButton(self)
        self.tbWhatDoesThisCommandDo = MToolButton(self)
        self.tbClear.setToolTip(translate("SpecialTools", "Clear"))
        self.tbAddBookmark.setToolTip(translate("SpecialTools", "Add To Bookmarks"))
        self.tbDeleteBookmark.setToolTip(translate("SpecialTools", "Remove From Bookmarks"))
        self.tbGoBack.setToolTip(translate("SpecialTools", "Back"))
        self.tbGoForward.setToolTip(translate("SpecialTools", "Forward"))
        self.tbWhatDoesThisCommandDo.setToolTip(translate("SpecialTools", "What Does This Command Do?"))
        self.tbClear.setIcon(MIcon("Images:actionClear.png"))
        self.tbAddBookmark.setIcon(MIcon("Images:addBookmark.png"))
        self.tbDeleteBookmark.setIcon(MIcon("Images:actionDelete.png"))
        self.tbGoBack.setIcon(MIcon("Images:actionBack.png"))
        self.tbGoForward.setIcon(MIcon("Images:actionForward.png"))
        self.tbWhatDoesThisCommandDo.setIcon(MIcon("Images:whatDoesThisCommandDo.png"))
        self.tbClear.setAutoRaise(True)
        self.tbAddBookmark.setAutoRaise(True)
        self.tbDeleteBookmark.setAutoRaise(True)
        self.tbGoBack.setAutoRaise(True)
        self.tbGoForward.setAutoRaise(True)
        self.tbWhatDoesThisCommandDo.setAutoRaise(True)
        self.leActionString.setEnabled(False)
        self.tbDeleteBookmark.setEnabled(False)
        MObject.connect(self.cbBookmarks, SIGNAL("currentIndexChanged(int)"), self.cbBookmarksChanged)
        MObject.connect(self.tbAddComma, SIGNAL("clicked()"), self.addComma)
        MObject.connect(self.tbAddSplit, SIGNAL("clicked()"), self.addSplit)
        MObject.connect(self.tbClear, SIGNAL("clicked()"), self.makeClear)
        MObject.connect(self.tbGoBack, SIGNAL("clicked()"), self.goBack)
        MObject.connect(self.tbGoForward, SIGNAL("clicked()"), self.goForward)
        MObject.connect(self.tbWhatDoesThisCommandDo, SIGNAL("clicked()"), self.whatDoesThisCommandDo)
        MObject.connect(self.tbAddBookmark, SIGNAL("clicked()"), self.addBookmark)
        MObject.connect(self.tbDeleteBookmark, SIGNAL("clicked()"), self.deleteBookmark)
        self.HBoxs = []
        self.HBoxs.append(MHBoxLayout())
        self.HBoxs.append(MHBoxLayout())
        self.HBoxs[1].addWidget(self.tbAddComma)
        self.HBoxs[1].addWidget(self.tbAddSplit)
        self.HBoxs[1].addWidget(self.leSplitPointer)
        self.HBoxs.append(MHBoxLayout())
        self.HBoxs[2].addWidget(self.cbBookmarks)
        self.HBoxs[2].addWidget(self.tbDeleteBookmark)
        self.HBoxs.append(MHBoxLayout())
        self.HBoxs[3].addWidget(self.tbGoBack)
        self.HBoxs[3].addWidget(self.tbGoForward)
        self.HBoxs[3].addWidget(self.tbClear)
        self.HBoxs[3].addWidget(self.leActionString)
        self.HBoxs[3].addWidget(self.tbAddBookmark)
        self.HBoxs[3].addWidget(self.tbWhatDoesThisCommandDo)
        self.HBoxs[3].addWidget(self.details)
        vblSpecialActions = MVBoxLayout()
        vblSpecialActions.addLayout(self.HBoxs[0])
        vblSpecialActions.addLayout(self.HBoxs[1])
        vblSpecialActions.addLayout(self.HBoxs[2])
        vblSpecialActions.addLayout(self.HBoxs[3])
        self.setLayout(vblSpecialActions)
        self.cbBookmarks.setSizeAdjustPolicy(MComboBox.AdjustToMinimumContentsLength)
        self.leSplitPointer.setMaximumWidth(40)
        self.tbAddComma.setMaximumWidth(40)
        self.tbAddComma.setMaximumWidth(40)
        self.leSplitPointer.setMaximumHeight(30)   
        if self.parent().parent().isShowAdvancedSelections==True:
            self.details.hide()
            
    def showAdvancedSelections(self):
        self.leActionString.show()
        self.leSplitPointer.show()
        for btn in self.pbtnAddObjects:
            btn.show()
        self.tbAddComma.show()
        self.tbAddSplit.show()
        self.tbClear.show()
        self.tbGoBack.show()
        self.tbGoForward.show()
        self.tbWhatDoesThisCommandDo.show()
        self.tbAddBookmark.show()
        self.tbDeleteBookmark.show()
        self.details.hide()
    
    def hideAdvancedSelections(self):
        self.leActionString.hide()
        self.leSplitPointer.hide()
        for btn in self.pbtnAddObjects:
            btn.hide()
        self.tbAddComma.hide()
        self.tbAddSplit.hide()
        self.tbClear.hide()
        self.tbGoBack.hide()
        self.tbGoForward.hide()
        self.tbWhatDoesThisCommandDo.hide()
        self.tbAddBookmark.hide()
        self.tbDeleteBookmark.hide()
        self.details.show()
        
    def AddObjects(self):
        try:
            if self.isPressedAddObjects==False:
                self.history.append(self.leActionString.text())
                self.future=[]
                self.tbGoForward.setEnabled(False)
                self.numberOfActionCommand+=1
                self.isPressedAddObjects=True
                self.leActionString.setText(str(self.leActionString.text()) + 
                            str(self.sender().objectName())+u" ")
                self.actionCommand += Universals.MainWindow.Table.getColumnKeyFromName(self.sender().text())
        except:
            error = ReportBug.ReportBug()
            error.show()
            
    def addComma(self):
        try:
            if self.numberOfActionCommand>0 and (self.commaAndSplitControl==0 or self.commaAndSplitControl<self.numberOfActionCommand) and self.numberOfActionCommand<100:
                self.history.append(self.leActionString.text())
                self.future=[]
                self.tbGoForward.setEnabled(False)
                self.leActionString.setText(self.leActionString.text() + u", ")
                self.actionCommand += ", "
                self.tbAddComma.setEnabled(False)
                self.numberOfActionCommand+=100
                self.commaAndSplitControl = self.numberOfActionCommand
                self.isPressedAddObjects=False
        except:
            error = ReportBug.ReportBug()
            error.show()
            
    def addSplit(self):
        try:
            if self.numberOfActionCommand>0 and (self.commaAndSplitControl==0 or self.commaAndSplitControl<self.numberOfActionCommand) and (self.whereIsSplitPointer=="right" or self.numberOfActionCommand<100) :
                if self.numberOfActionCommand<100:
                    self.whereIsSplitPointer="left"
                if unicode(self.leSplitPointer.text()).encode("utf-8").upper()!=unicode(self.leSplitPointer.text()).encode("utf-8").decode("utf-8").lower() or unicode(self.leSplitPointer.text()).encode("utf-8").strip()=="":
                    self.leSplitPointer.setText("-")
                self.history.append(self.leActionString.text())
                self.future=[]
                self.tbGoForward.setEnabled(False)
                self.leActionString.setText(self.leActionString.text() + (unicode(self.leSplitPointer.text(), "utf-8").strip()).decode("utf-8") + u" ")
                self.actionCommand += unicode(self.leSplitPointer.text(), "utf-8").strip() + u" "
                self.numberOfActionCommand+=10
                self.commaAndSplitControl = self.numberOfActionCommand
                self.isPressedAddObjects=False
        except:
            error = ReportBug.ReportBug()
            error.show()
            
    def makeClear(self):
        try:
            self.history.append(self.leActionString.text())
            self.future=[]
            self.tbGoForward.setEnabled(False)
            self.leActionString.setText("")
            self.actionCommand = ""
            self.tbAddComma.setEnabled(True)
            self.numberOfActionCommand=0
            self.commaAndSplitControl=0
            self.whereIsSplitPointer="right"
            self.isPressedAddObjects=False
        except:
            error = ReportBug.ReportBug()
            error.show()
    
    def whatDoesThisCommandDo(self):
        try:
            Organizer.whatDoesSpecialCommandDo(unicode(self.leSplitPointer.text()).encode("utf-8"),self.whereIsSplitPointer,self.actionCommand)
        except:
            error = ReportBug.ReportBug()
            error.show()
    
    def goBack(self):
        try:
            if len(self.history)>0:
                if str(self.leActionString.text())[-2:].strip()==str(self.leSplitPointer.text()).strip():
                    self.numberOfActionCommand-=10
                    self.commaAndSplitControl = self.numberOfActionCommand-1
                    self.isPressedAddObjects=True
                elif str(self.leActionString.text())[-2:].strip()==",":
                    self.tbAddComma.setEnabled(True)
                    self.numberOfActionCommand-=100
                    self.commaAndSplitControl = self.numberOfActionCommand-1
                    self.isPressedAddObjects=True
                else:
                    self.numberOfActionCommand-=1
                    self.isPressedAddObjects=False
                self.future.append(self.leActionString.text())
                h = self.history.pop()
                self.leActionString.setText(h)
                self.actionCommand = unicode(h, "utf-8")
                self.tbGoForward.setEnabled(True)
            else:
                self.tbGoBack.setEnabled(False)
        except:
            error = ReportBug.ReportBug()
            error.show()
            
    def goForward(self):
        try:
            if len(self.future)>0:
                future_temp=self.future.pop()
                if str(future_temp)[-2:].strip()==str(self.leSplitPointer.text()).strip():
                    self.numberOfActionCommand+=10
                    self.commaAndSplitControl = self.numberOfActionCommand
                    self.isPressedAddObjects=False
                elif str(future_temp)[-2:].strip()==",":
                    self.tbAddComma.setEnabled(False)
                    self.numberOfActionCommand+=100
                    self.commaAndSplitControl = self.numberOfActionCommand
                    self.isPressedAddObjects=False
                else: 
                    self.numberOfActionCommand+=1
                    self.isPressedAddObjects=True
                self.history.append(self.leActionString.text())
                self.leActionString.setText(future_temp)
                self.actionCommand = unicode(future_temp, "utf-8")
                self.tbGoBack.setEnabled(True)
            else:
                self.tbGoForward.setEnabled(False)
        except:
            error = ReportBug.ReportBug()
            error.show()
           
    def cbBookmarksChanged(self,_index):
        try:
            if _index>0:
                tempT = Settings.bookmarksOfSpecialTools()[_index-1][2]
                tempString = tempT.split(";")
                tempT = ""
                tempA = ""
                for t in tempString[:-2]:
                    tempT += t
                    tempA += t
                    for colNo, colName in enumerate(Universals.MainWindow.Table.tableColumnsKey):
                        tempT = tempT.replace(colName, str(Universals.MainWindow.Table.tableColumns[colNo]))
                self.history.append(self.leActionString.text())
                self.future=[]
                self.leActionString.setText(tempT.decode("utf-8"))
                self.actionCommand = tempA
                self.whereIsSplitPointer = tempString[-2]
                self.numberOfActionCommand = int(tempString[-1])
                self.commaAndSplitControl = self.numberOfActionCommand-1
                self.tbDeleteBookmark.setEnabled(True)
                self.isPressedAddObjects=True
                self.tbGoBack.setEnabled(True)
                self.tbGoForward.setEnabled(False)
                self.tbAddComma.setEnabled(False)
                self.details.setText(str(Organizer.whatDoesSpecialCommandDo(unicode(self.leSplitPointer.text()).encode("utf-8"),
                                    self.whereIsSplitPointer,
                                    self.actionCommand, 
                                    _isReturnDetails=True)).decode("utf-8"))
            else:
                self.whereIsSplitPointer, self.numberOfActionCommand, self.commaAndSplitControl, self.isPressedAddObjects="right",0,0, False
                self.leActionString.setText(u"")
                self.actionCommand = ""
                self.tbDeleteBookmark.setEnabled(False)
                self.tbAddComma.setEnabled(True)
                self.details.setText(translate("SpecialTools", "Please Select An Action!"))
        except:
            error = ReportBug.ReportBug()
            error.show()
        
    def addBookmark(self):
        try:
            tempString = self.actionCommand
            if Organizer.whatDoesSpecialCommandDo(unicode(self.leSplitPointer.text()).encode("utf-8"),self.whereIsSplitPointer,unicode(self.leActionString.text()).encode("utf-8"),True)==True:
                addition = " ;"+self.whereIsSplitPointer +";"+ str(self.numberOfActionCommand)
                Settings.bookmarksOfSpecialTools("add","",tempString+addition)
                self.refreshBookmarks()
                self.cbBookmarks.setCurrentIndex(self.cbBookmarks.count()-1)
        except:
            error = ReportBug.ReportBug()
            error.show()
           
    def deleteBookmark(self):
        try:
            if self.cbBookmarks.currentIndex()!=-1 and self.cbBookmarks.currentIndex()!=0:
                Settings.bookmarksOfSpecialTools("delete",Settings.bookmarksOfSpecialTools()[self.cbBookmarks.currentIndex()-1][2])
                self.refreshBookmarks()
        except:
            error = ReportBug.ReportBug()
            error.show()
            
    def refreshBookmarks(self):
        try:
            self.cbBookmarks.clear()
            self.cbBookmarks.addItem(translate("SpecialTools", "Please Select An Action!"))
            for fav in Settings.bookmarksOfSpecialTools():
                if Universals.MySettings["musicTagType"]=="ID3 V2":
                    self.cbBookmarks.addItem(fav[1].decode("utf-8"))
                else:
                    if fav[1].find("Lyrics")==-1:
                        self.cbBookmarks.addItem(fav[1].decode("utf-8"))
        except:
            error = ReportBug.ReportBug()
            error.show()
            
        
                
class SearchAndReplace(MWidget):
    def __init__(self, _parent):
        MWidget.__init__(self, _parent)
        lblSearch=MLabel(translate("SpecialTools", "Search: "))
        lblReplace=MLabel(translate("SpecialTools", "Replace: "))
        self.leSearch = MLineEdit("")
        self.leReplace = MLineEdit("")
        lblColumns = MLabel(translate("SpecialTools", "Column: "))
        srExamples = translate("SpecialTools", "<table><tr><td><nobr>Before</nobr></td><td>>></td><td><nobr>Search</nobr></td><td>-</td><td><nobr>Replace</nobr></td><td>>></td><td><nobr>After</nobr></td></tr>" +
                                 "<tr><td><nobr>HamsiManager</nobr></td><td>>></td><td><nobr>ager</nobr></td><td>-</td><td><nobr></nobr></td><td>>></td><td><nobr>HamsiMan</nobr></td></tr>" +
                                 "</table><table>")
        sExample=translate("SpecialTools", "<tr><td><nobr>Example: \"search 1<b>;</b>search 2<b>;</b>search 3<b>;</b>...<b>;</b>search n<b>;</b>\"</nobr></td></tr>")
        rExample=translate("SpecialTools", "<tr><td><nobr>Example: \"Change/replace 1<b>;</b>Change/replace 2<b>;</b>Change/replace 3<b>;</b>...<b>;</b>Change/replace n<b>;</b>\"</nobr></td></tr>")
        self.cckbCaseSensitive = MCheckBox(translate("SpecialTools", "Case Insensitive"))
        self.cckbCaseSensitive.setChecked(True)
        self.cckbRegExp = MCheckBox(translate("SpecialTools", "Regular Expression (RegExp)"))
        self.leSearch.setToolTip(srExamples+sExample+u"</table>")
        self.leReplace.setToolTip(srExamples+rExample+"</table>")
        self.columns = MComboBox()
        self.columns.addItem(translate("SpecialTools", "All"))
        lblSearch.setFixedWidth(60)
        lblReplace.setFixedWidth(100)
        lblColumns.setFixedWidth(60)
        HBoxs = []
        HBoxs.append(MHBoxLayout())
        HBoxs[0].addWidget(lblSearch)
        HBoxs[0].addWidget(self.leSearch)
        HBoxs[0].addWidget(lblReplace)
        HBoxs[0].addWidget(self.leReplace)
        HBoxs.append(MHBoxLayout())
        HBoxs[1].addWidget(lblColumns)
        HBoxs[1].addWidget(self.columns)
        HBoxs[1].addStretch(2)
        HBoxs[1].addWidget(self.cckbCaseSensitive)
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
    
    def hideAdvancedSelections(self):
        self.cckbRegExp.hide()
        self.cckbRegExp.setChecked(False)
             
class Fill(MWidget):
    def __init__(self, _parent):
        MWidget.__init__(self, _parent)
        self.leFill = MLineEdit("")
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
        lblFill = MLabel(translate("SpecialTools", "Text: "))
        lblFill.setFixedWidth(60)
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
        HBoxs[1].addWidget(lblFill)
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
            if unicode(self.columns.currentText()).encode("utf-8")=="Track No":
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
            error = ReportBug.ReportBug()
            error.show()
            
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
        self.cckbCaseSensitive = MCheckBox(translate("SpecialTools", "Case Insensitive"))
        self.cckbRegExp = MCheckBox(translate("SpecialTools", "Regular Expression (RegExp)"))
        self.cckbCaseSensitive.setChecked(True)
        HBoxs = []
        HBoxs.append(MHBoxLayout())
        HBoxs[0].addWidget(lblColumns)
        HBoxs[0].addWidget(self.columns)
        HBoxs[0].addWidget(lblClearType)
        HBoxs[0].addWidget(self.cbClearType)
        HBoxs.append(MHBoxLayout())
        HBoxs[1].addWidget(self.lblClear)
        HBoxs[1].addWidget(self.leClear)
        HBoxs[1].addWidget(self.cckbCaseSensitive)
        HBoxs.append(MHBoxLayout())
        HBoxs[2].addStretch(3)
        HBoxs[2].addWidget(self.cckbRegExp)
        vblClear = MVBoxLayout()
        vblClear.addLayout(HBoxs[0])
        vblClear.addLayout(HBoxs[1])
        vblClear.addLayout(HBoxs[2])
        self.setLayout(vblClear)
        self.cckbCaseSensitive.setEnabled(False)
        self.cckbRegExp.setEnabled(False)
        self.lblClear.setEnabled(False)
        self.leClear.setEnabled(False)
        lblColumns.setFixedWidth(60)
        self.lblClear.setFixedWidth(60)
        MObject.connect(self.cbClearType, SIGNAL("currentIndexChanged(int)"), self.clearTypeChanged)
        
    def clearTypeChanged(self):
        if self.cbClearType.currentIndex()!=4:
            self.cckbCaseSensitive.setEnabled(False)
            self.lblClear.setEnabled(False)
            self.leClear.setEnabled(False)
            self.cckbRegExp.setEnabled(False)
        else:
            self.cckbCaseSensitive.setEnabled(True)
            self.lblClear.setEnabled(True)
            self.leClear.setEnabled(True)
            self.cckbRegExp.setEnabled(True)
        
    def showAdvancedSelections(self):
        self.cckbRegExp.show()
    
    def hideAdvancedSelections(self):
        self.cckbRegExp.hide()
        self.cckbRegExp.setChecked(False)
            
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
        self.cckbCaseSensitive = MCheckBox(translate("SpecialTools", "Case Insensitive"))
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
        HBoxs[1].addWidget(self.cckbCaseSensitive)
        HBoxs.append(MHBoxLayout())
        HBoxs[2].addStretch(3)
        HBoxs[2].addWidget(self.cckbRegExp)
        self.cckbCaseSensitive.setEnabled(False)
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
            self.cckbCaseSensitive.setEnabled(True)
            self.cckbRegExp.setEnabled(True)
            self.leSearch.setEnabled(True)
        else:
            self.cckbCaseSensitive.setEnabled(False)
            self.cckbRegExp.setEnabled(False)
            self.leSearch.setEnabled(False)
            
        
        
        
        
        
