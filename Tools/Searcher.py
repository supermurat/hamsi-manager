## This file is part of HamsiManager.
## 
## Copyright (c) 2010 Murat Demir <mopened@gmail.com>      
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


from MyObjects import *
import Universals
import Dialogs
import InputOutputs
from Options import OptionsForm
import Organizer
import unicodedata

MyDialog, MyDialogType, MyParent = getMyDialog()

class Searcher(MyDialog):
    def __init__(self, _directory):
        MyDialog.__init__(self, MyParent)
        if MyDialogType=="MDialog":
            if Universals.isActivePyKDE4==True:
                self.setButtons(MyDialog.NoDefault)
        elif MyDialogType=="MMainWindow":
            self.setObjectName("Searcher")
            Universals.MainWindow = self
        newOrChangedKeys = Universals.newSettingsKeys + Universals.changedDefaultValuesKeys
        wOptionsPanel = OptionsForm.OptionsForm(None, "search", None, newOrChangedKeys)
        self.sourceToSearch = None
        lblPleaseSelect = MLabel(translate("Searcher", "Directory"))
        self.pbtnClose = MPushButton(translate("Searcher", "Close"))
        self.lePathToSeach = MLineEdit(trForM(_directory))
        self.pbtnSelectSeachDirectoryPath = MPushButton(translate("Searcher", "Select Directory"))
        self.pbtnSelectSeachFilePath = MPushButton(translate("Searcher", "Select File"))
        self.connect(self.pbtnSelectSeachDirectoryPath,SIGNAL("clicked()"),self.selectSearchDirectoryPath)
        self.connect(self.pbtnSelectSeachFilePath,SIGNAL("clicked()"),self.selectSearchFilePath)
        self.connect(self.pbtnClose,SIGNAL("clicked()"),self.close)
        self.pbtnReloadSourceToSearch = MPushButton(translate("Searcher", "(Re)Load"))
        self.connect(self.pbtnReloadSourceToSearch,SIGNAL("clicked()"),self.reloadSourceToSearch)
        lblSearch = MLabel(translate("Searcher", "Search"))
        self.leSeach = MLineEdit(trForM(""))
        self.teSeachResult = MTextEdit()
        self.teSeachResult.setText(trForUI(""))
        self.connect(self.leSeach,SIGNAL("textChanged(const QString&)"),self.search)
        pnlMain = MWidget(self)
        tabwTabs = MTabWidget()
        vblMain = MVBoxLayout(pnlMain)
        pnlMain2 = MWidget(tabwTabs)
        vblMain2 = MVBoxLayout(pnlMain2)
        HBox = MHBoxLayout()
        HBox.addWidget(self.lePathToSeach)
        HBox1 = MHBoxLayout()
        HBox1.addWidget(self.pbtnReloadSourceToSearch)
        HBox1.addWidget(self.pbtnSelectSeachDirectoryPath)
        HBox1.addWidget(self.pbtnSelectSeachFilePath)
        HBox3 = MHBoxLayout()
        HBox3.addWidget(lblSearch)
        HBox3.addWidget(self.leSeach)
        HBox2 = MHBoxLayout()
        HBox2.addWidget(self.pbtnClose)
        vblMain2.addWidget(lblPleaseSelect)
        vblMain2.addLayout(HBox)
        vblMain2.addLayout(HBox1)
        vblMain2.addLayout(HBox3)
        vblMain2.addWidget(self.teSeachResult, 20)
        vblMain2.addStretch(1)
        vblMain2.addLayout(HBox2)
        tabwTabs.addTab(pnlMain2, translate("Searcher", "Search"))
        tabwTabs.addTab(wOptionsPanel, translate("Searcher", "Quick Options"))
        vblMain.addWidget(tabwTabs)
        if MyDialogType=="MDialog":
            if Universals.isActivePyKDE4==True:
                self.setMainWidget(pnlMain)
            else:
                self.setLayout(vblMain)
        elif MyDialogType=="MMainWindow":
            self.setCentralWidget(pnlMain)
            moveToCenter(self)
        self.setWindowTitle(translate("Searcher", "Searcher"))
        self.setWindowIcon(MIcon("Images:search.png"))
        self.show()
                        
    def closeEvent(self, _event):
        MApplication.setQuitOnLastWindowClosed(True)
    
    def reloadSourceToSearch(self):
        if self.setSourceToSearch():
            self.search()
    
    def setSourceToSearch(self, _isReload=True):
        try:
            if self.sourceToSearch == None or _isReload==True:
                pathToSearch = str(self.lePathToSeach.text())
                if InputOutputs.IA.checkSource(pathToSearch):
                    if InputOutputs.IA.isReadableFileOrDir(pathToSearch):
                        if InputOutputs.isFile(pathToSearch):
                            self.sourceToSearch = InputOutputs.readFromFile(pathToSearch)
                            self.sourceToSearchType = "file"
                            return True
                        elif InputOutputs.isDir(pathToSearch):
                            self.sourceToSearch = InputOutputs.getFileTree(pathToSearch, -1, "plainText", "fileList")
                            self.sourceToSearchType = "dir"
                            return True
                return False
            else:
                return True
        except:
            import ReportBug
            error = ReportBug.ReportBug()
            error.show() 
    
    def search(self, _searchValue=""):
        try:
            import re
            #Universals.isCanBeShowOnMainWindow = False
            if self.setSourceToSearch(False):
                searchValue = str(self.leSeach.text())
                if searchValue!="":
                    searchValueList = [searchValue]
                    
                    _isCaseInsensitive = True
                    
                    clearedSearchValue = ''.join(c for c in unicodedata.normalize('NFKD', Universals.trUnicode(searchValue)) if unicodedata.category(c) != 'Mn')
                    clearedSearchValue = str(Universals.trEncode(clearedSearchValue, "utf-8", "ignore")).replace(Universals.getUtf8Data("little+I"), "i")
                    searchValueList.append(clearedSearchValue)
                    
                    clearedSearchValue1 = ""
                    for char in searchValue:
                        if char.isdigit()==False:
                            clearedSearchValue1+=char
                    searchValueList.append(clearedSearchValue1)
                    
                    clearedSearchValue2 = ""
                    for char in searchValue:
                        if char.isdigit()==True or char.isalpha()==True:
                            clearedSearchValue2+=char
                    searchValueList.append(clearedSearchValue2)
                    
                    vowels=["a", "e", "i", "o", "u", "A", "E", "I", "O", "U"]
                    clearedSearchValue3 = ""
                    for char in Universals.trUnicode(searchValue):
                        clearedChar = ''.join(c for c in unicodedata.normalize('NFKD', Universals.trUnicode(char)) if unicodedata.category(c) != 'Mn')
                        clearedChar = str(Universals.trEncode(clearedChar, "utf-8", "ignore")).replace(Universals.getUtf8Data("little+I"), "i")
                        if clearedChar not in vowels:
                            clearedSearchValue3+=char
                    searchValueList.append(clearedSearchValue3)
                    
                    clearedSearchValue4 = ""
                    for char in clearedSearchValue:
                        if clearedChar not in vowels:
                            clearedSearchValue4+=char
                    searchValueList.append(clearedSearchValue4)
                    
                    resultOfSearch = ""
                    arrayOfSource = str(self.sourceToSearch).split("\n\r")
                    if len(arrayOfSource)==1: arrayOfSource = str(self.sourceToSearch).split("\n")
                    if len(arrayOfSource)==1: arrayOfSource = str(self.sourceToSearch).split("<br>")
                    if len(arrayOfSource)==1: arrayOfSource = str(self.sourceToSearch).split("<br/>")
                    if len(arrayOfSource)==1: arrayOfSource = str(self.sourceToSearch).split("<br >")
                    if len(arrayOfSource)==1: arrayOfSource = str(self.sourceToSearch).split("<br />")
                    for row in arrayOfSource:
                        for searchVal in searchValueList:
                            if row.find(searchVal) != -1:
                                resultOfSearch += row + "\n"
                                break
                            if _isCaseInsensitive == True:
                                pattern = re.compile(Universals.trUnicode(searchVal), re.I | re.U)
                                if re.search(pattern, Universals.trUnicode(row)) is not None:
                                    resultOfSearch += row + "\n"
                                    break
                            else:
                                pattern = re.compile(Universals.trUnicode(searchVal))
                                if re.search(pattern, Universals.trUnicode(row)) is not None:
                                    resultOfSearch += row + "\n"
                                    break
                else:
                    resultOfSearch = str(self.sourceToSearch)
                self.teSeachResult.setText(trForUI(resultOfSearch))
            #Universals.isCanBeShowOnMainWindow = True
        except:
            import ReportBug
            error = ReportBug.ReportBug()
            error.show() 

    def selectSearchDirectoryPath(self):
        try:
            SearchPath = MFileDialog.getExistingDirectory(self,
                            translate("Searcher", "Please Select Directory"),self.lePathToSeach.text())
            if SearchPath!="":
                self.lePathToSeach.setText(SearchPath)
                if self.setSourceToSearch(True):
                    self.search()
        except:
            import ReportBug
            error = ReportBug.ReportBug()
            error.show() 

    def selectSearchFilePath(self):
        try:
            SearchPath = MFileDialog.getOpenFileName(self,
                        translate("Searcher", "Please Select A Text File To Search"), self.lePathToSeach.text(),
                        translate("Searcher", "All Files (*.*)"))
            if SearchPath!="":
                self.lePathToSeach.setText(SearchPath)
                if self.setSourceToSearch(True):
                    self.search()
        except:
            import ReportBug
            error = ReportBug.ReportBug()
            error.show() 
    
    
    
                
