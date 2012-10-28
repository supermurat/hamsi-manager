## This file is part of HamsiManager.
## 
## Copyright (c) 2010 - 2012 Murat Demir <mopened@gmail.com>      
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

import sys,os
from Core import Variables
from Core.MyObjects import *
from Core import Settings, Dialogs, Universals, Records
import InputOutputs
import Databases
from Core import ReportBug

  
  
class General(MWidget):
    def __init__(self, _parent=None, _showType = None, _visibleKeys = None):
        MWidget.__init__(self, _parent)
        self._parent = _parent
        self.titleOfCategory = translate("Options/General", "General")
        self.labelOfCategory = translate("Options/General", "You can change the general settings in this section.")
        self.categoryNo = None
        self.Panel = MVBoxLayout(self)
        self.values, self.lblLabels = [], []
        self.keysOfSettings = ["isCheckUnSavedValues", "isSaveActions", "maxRecordFileSize", 
                                "updateInterval", "language"]
        self.tabsOfSettings = [None, None, None, None, None]
        self.tabNames = []
        if _visibleKeys==None:
            self.visibleKeys = self.keysOfSettings
        else:
            self.visibleKeys = _visibleKeys
        self.neededRestartSettingKeys = ["language"]
        self.valuesOfOptionsKeys = []
        self.labels = [translate("Options/General", "Check Unsaved Values"), 
                    translate("Options/General", "Save Actions"), 
                    translate("Options/General", "Record File Size"), 
                    translate("Options/General", "Update Interval (in days)"), 
                    translate("Options/General", "Application Language")]
        self.toolTips = [translate("Options/General", "Are you want to check unsaved values in tables while Hamsi Manager was closing?"), 
                    translate("Options/General", "If you want to save the actions you performed select \"Yes\"."), 
                    translate("Options/General", "You can select record file size.(Kilobytes)"), 
                    translate("Options/General", "Which interval (in days) do you want to set to check the updates?"), 
                    translate("Options/General", "You can select Hamsi Manager`s language.")]
        self.typesOfValues = ["Yes/No", "Yes/No", ["number", 2], 
                                ["number", 1], ["options", 0]]
        self.valuesOfOptions = [Variables.getInstalledLanguagesNames(), 
                                ["1", "30"], ["10", "100000"]]
        self.valuesOfOptionsKeys = [Variables.getInstalledLanguagesCodes(), 
                                ["1", "30"], ["10", "100000"]]
        _parent.createOptions(self)
        if Universals.isActivePyKDE4==True:
            _parent.setVisibleFormItems(self, "language", False)
        if self.visibleKeys.count("isSaveActions")>0:
            MObject.connect(self.values[self.keysOfSettings.index("isSaveActions")], SIGNAL("currentIndexChanged(int)"), self.saveActionsChanged)
            self.saveActionsChanged()
    
    def saveActionsChanged(self):
        if self.values[self.keysOfSettings.index("isSaveActions")].currentIndex()==1:
            self._parent.setEnabledFormItems(self, "maxRecordFileSize", True)
        else:
            self._parent.setEnabledFormItems(self, "maxRecordFileSize", False)
            

class Appearance(MWidget):
    def __init__(self, _parent=None, _showType = None, _visibleKeys = None):
        MWidget.__init__(self, _parent)
        self._parent = _parent
        self.titleOfCategory = translate("Options/Appearance", "Appearance")
        self.labelOfCategory = translate("Options/Appearance", "You can change the appearance settings in this section.")
        self.categoryNo = None
        self.Panel = MVBoxLayout(self)
        self.values, self.lblLabels = [], []
        self.keysOfSettings = ["applicationStyle", "themeName", "colorSchemes", 
                                "isMinimumWindowMode", "isShowQuickMakeWindow", 
                                "isShowTransactionDetails", "windowMode", "isResizeTableColumnsToContents"]
        self.tabsOfSettings = [None, None, None, 
                                None, None, None, 
                                None, None]
        self.tabNames = []
        if _visibleKeys==None:
            self.visibleKeys = self.keysOfSettings
        else:
            self.visibleKeys = _visibleKeys
        self.neededRestartSettingKeys = ["themeName", "windowMode"]
        self.valuesOfOptionsKeys = []
        self.labels = [translate("Options/Appearance", "Application Style"),
                    translate("Options/Appearance", "Application Theme"), 
                    translate("Options/Appearance", "Color Schemes"), 
                    translate("Options/Appearance", "Activate Minimal Window Mode"), 
                    translate("Options/Appearance", "Show Quick Make Dialog"),  
                    translate("Options/Appearance", "Show Transaction Details"), 
                    translate("Options/Appearance", "Window Mode"), 
                    translate("Options/Appearance", "Resize Table Columns")]
        self.toolTips = [translate("Options/Appearance", "You can select style for Hamsi Manager."),
                    translate("Options/Appearance", "You can select theme for Hamsi Manager."),
                    translate("Options/Appearance", "You can select color schemes for Hamsi Manager."),
                    translate("Options/Appearance", "You have to activate this if you want to work as little number of windows as possible."), 
                    translate("Options/Appearance", "Are you want to show quick make dialog in runed with command line or my plugins?"),
                    translate("Options/Appearance", "Are you want to show transaction details after save table?"), 
                    translate("Options/Appearance", "You can select window mode.You can select \"Mini\" section for netbook or small screen."),
                    translate("Options/Appearance", "Are you want to resize table columns to contents?")]
        self.typesOfValues = [["options", 0], ["options", 1], ["options", 3], 
                                "Yes/No", "Yes/No", "Yes/No", ["options", 2], "Yes/No"]
        styles = Variables.getStyles()
        themes = Variables.getInstalledThemes()
        schemes, schemePaths  = Variables.getColorSchemesAndPath()
        if Universals.isActivePyKDE4==False:
            keyNo = self.keysOfSettings.index("colorSchemes")
            del self.keysOfSettings[keyNo]
            del self.labels[keyNo]
            del self.toolTips[keyNo]
            del self.typesOfValues[keyNo]
        self.valuesOfOptions = [styles, themes, 
                                [translate("Options/Appearance", "Normal"), 
                                    translate("Options/Appearance", "Mini")], schemes]
        self.valuesOfOptionsKeys = [styles, themes, 
                                Variables.windowModeKeys, schemePaths]
        _parent.createOptions(self)
        if self.visibleKeys.count("applicationStyle")>0:
            MObject.connect(self.values[self.keysOfSettings.index("applicationStyle")], SIGNAL("currentIndexChanged(int)"), self.styleChanged)
        if self.visibleKeys.count("colorSchemes")>0:
            MObject.connect(self.values[self.keysOfSettings.index("colorSchemes")], SIGNAL("currentIndexChanged(int)"), self.schemeChanged)
        if self.visibleKeys.count("windowMode")>0:
            MObject.connect(self.values[self.keysOfSettings.index("windowMode")], SIGNAL("currentIndexChanged(int)"), self.windowModeChanged)
    
    def styleChanged(self, _value):
        MApplication.setStyle(self.values[self.keysOfSettings.index("applicationStyle")].currentText())
    
    def schemeChanged(self, _value):
        x = self.keysOfSettings.index("colorSchemes")
        schemePath = self.valuesOfOptionsKeys[self.typesOfValues[x][1]][self.values[x].currentIndex()]
        if InputOutputs.isFile(schemePath):
            config = MSharedConfig.openConfig(schemePath)
            plt = MGlobalSettings.createApplicationPalette(config)
        else:
            plt = MApplication.desktop().palette()
        MApplication.setPalette(plt)
        
    def windowModeChanged(self, _value):
        Universals.setMySetting("isShowWindowModeSuggestion", True)
        
        
class Correct(MWidget):
    def __init__(self, _parent=None, _showType = None, _visibleKeys = None):
        MWidget.__init__(self, _parent)
        self._parent = _parent
        self.titleOfCategory = translate("Options/Correct", "Correct")
        self.labelOfCategory = translate("Options/Correct", "You can change the correct and emend settings in this section.")
        self.categoryNo = None
        self.Panel = MVBoxLayout(self)
        self.values, self.lblLabels = [], []
        self.keysOfSettings = ["isActiveCompleter", "isShowAllForCompleter",
            "validSentenceStructure", "validSentenceStructureForFile", "validSentenceStructureForDirectory", 
            "validSentenceStructureForFileExtension", "fileExtesionIs", "isEmendIncorrectChars", 
            "isCorrectFileNameWithSearchAndReplaceTable", "isCorrectValueWithSearchAndReplaceTable", "isClearFirstAndLastSpaceChars", "isCorrectDoubleSpaceChars", "isDecodeURLStrings"]
        self.tabsOfSettings = [None, None, None, None, 
                                None, None, None, 
                                None, None, None, None, None, None]
        self.tabNames = []
        if _visibleKeys==None:
            self.visibleKeys = self.keysOfSettings
        else:
            self.visibleKeys = _visibleKeys
        self.neededRestartSettingKeys = []
        self.valuesOfOptionsKeys = []
        self.labels = [translate("Options/Correct", "Use Completer"), 
                    translate("Options/Correct", "Show All"), 
                    translate("Options/Correct", "Valid Sentence Structure"), 
                    translate("Options/Correct", "Valid Sentence Structure For Files"),
                    translate("Options/Correct", "Valid Sentence Structure For Directories"),
                    translate("Options/Correct", "Valid Sentence Structure For File Extensions"), 
                    translate("Options/Correct", "Which Part Is The File Extension"), 
                    translate("Options/Correct", "Emend Incorrect Chars"),  
                    translate("Options/Correct", "Correct File Name By Search Table"), 
                    translate("Options/Correct", "Correct Value By Search Table"), 
                    translate("Options/Correct", "Clear First And Last Space Chars"), 
                    translate("Options/Correct", "Correct Double Space Chars"), 
                    translate("Options/Correct", "Decode URL Strings")]
        self.toolTips = [translate("Options/Correct", "Are you want to activate completer for auto complete some input controls?"), 
                    translate("Options/Correct", "Are you want to show all words in all input controls?"), 
                    translate("Options/Correct", "All information (Artist name,title etc.) will be changed automatically to the format you selected."), 
                    translate("Options/Correct", "File names will be changed automatically to the format you selected."),
                    translate("Options/Correct", "Directory names will be changed automatically to the format you selected."),
                    translate("Options/Correct", "File extensions will be changed automatically to the format you selected."), 
                    translate("Options/Correct", "Which part of the filename is the file extension?"), 
                    translate("Options/Correct", "Are you want to emend incorrect chars?"), 
                    translate("Options/Correct", "Are you want to correct file and directory names by search and replace table?"), 
                    translate("Options/Correct", "Are you want to correct values by search and replace table?"), 
                    translate("Options/Correct", "Are you want to clear first and last space chars?"), 
                    translate("Options/Correct", "Are you want to correct double space chars?"), 
                    translate("Options/Correct", "Are you want to decode URL strings? ( For Example : '%20' >>> ' ', '%26' >>> '&' ) ")]
        self.typesOfValues = ["Yes/No", "Yes/No", ["options", 0], ["options", 0], ["options", 0], ["options", 0], 
                            ["options", 1], "Yes/No", "Yes/No", "Yes/No", 
                            "Yes/No", "Yes/No", "Yes/No"]
        self.valuesOfOptions = [[translate("Options/Correct", "Title"), 
                                    translate("Options/Correct", "All Small"), 
                                    translate("Options/Correct", "All Caps"), 
                                    translate("Options/Correct", "Sentence"), 
                                    translate("Options/Correct", "Don`t Change")], 
                                [translate("Options/Correct", "After The First Point"), 
                                    translate("Options/Correct", "After The Last Point")]]
        self.valuesOfOptionsKeys = [Variables.validSentenceStructureKeys, 
                        Variables.fileExtesionIsKeys]
        _parent.createOptions(self)
        if self.visibleKeys.count("isActiveCompleter")>0:
            MObject.connect(self.values[self.keysOfSettings.index("isActiveCompleter")], SIGNAL("currentIndexChanged(int)"), self.activeCompleterChanged)
            self.activeCompleterChanged()
    
    def activeCompleterChanged(self):
        if self.values[self.keysOfSettings.index("isActiveCompleter")].currentIndex()==1:
            self._parent.setEnabledFormItems(self, "isShowAllForCompleter", True)
        else:
            self._parent.setEnabledFormItems(self, "isShowAllForCompleter", False)
    
                
class SearchAndReplace(MWidget):
    def __init__(self, _parent=None, _showType = None, _visibleKeys = None):
        MWidget.__init__(self, _parent)
        self._parent = _parent
        self.titleOfCategory = translate("Options/SearchAndReplace", "Search - Replace")
        self.labelOfCategory = translate("Options/SearchAndReplace", "You can set the text you want to search and replace in this section.")
        self.categoryNo = None
        self.values, self.lblLabels = [], []
        self.keysOfSettings = []
        self.tabsOfSettings = []
        self.tabNames = []
        if _visibleKeys==None:
            self.visibleKeys = self.keysOfSettings
        else:
            self.visibleKeys = _visibleKeys
        self.neededRestartSettingKeys = []
        self.valuesOfOptionsKeys = []
        self.typesOfValues = []
        self.searchAndReplaceTable = self.SearchAndReplaceTable(self)
        self.Panel = MVBoxLayout(self)
        self.Panel.addWidget(self.searchAndReplaceTable)
        lblDeleteInfo= MLabel(translate("Options/SearchAndReplace", "*Right-click on the criterion you want to delete and click the \"Delete Row\" button."))
        self.Panel.addWidget(lblDeleteInfo)
        
    class SearchAndReplaceTable(MTableWidget):
        def __init__(self,_parent):
            MTableWidget.__init__(self, _parent)
            self.setAlternatingRowColors(True)
            self.setWordWrap(False)
            self.setVerticalScrollMode(self.ScrollPerPixel)
            self.setHorizontalScrollMode(self.ScrollPerPixel)
            MObject.connect(self,SIGNAL("cellClicked(int,int)"),self.clicked)
            MObject.connect(self,SIGNAL("itemChanged(QTableWidgetItem *)"),self.itemChanged)
            self.clear()
            self.setColumnCount(7)
            self.setHorizontalHeaderLabels(["id", 
                            translate("Options/SearchAndReplace", "Label"), 
                            translate("Options/SearchAndReplace", "Search"), 
                            translate("Options/SearchAndReplace", "Replace"), 
                            translate("Options/SearchAndReplace", "Active"), 
                            translate("Options/SearchAndReplace", "C.Sens."), 
                            translate("Options/SearchAndReplace", "RegExp")])
            self.hideColumn(0)
            self.setColumnWidth(1,90)
            self.setColumnWidth(2,100)
            self.setColumnWidth(3,100)
            self.setColumnWidth(4,50)
            self.setColumnWidth(5,50)
            self.setColumnWidth(6,50)
            self.searchAndReplaceTableValues = Databases.SearchAndReplaceTable.fetchAll()
            self.setRowCount(len(self.searchAndReplaceTableValues)+1)
            self.isShowChanges=False
            for rowNo, info in enumerate(self.searchAndReplaceTableValues):
                for columnNo in range(self.columnCount()):
                    if columnNo>3:
                        if info[columnNo] == 1:
                            checkState = Mt.Checked
                        else:
                            checkState = Mt.Unchecked
                        twiItem = MTableWidgetItem(" ")
                        twiItem.setCheckState(checkState)
                        self.setItem(rowNo, columnNo, twiItem)
                    else:
                        self.setItem(rowNo, columnNo, MTableWidgetItem(trForUI(info[columnNo])))
            self.setItem(len(self.searchAndReplaceTableValues), 1, MTableWidgetItem(""))
            self.setItem(len(self.searchAndReplaceTableValues), 2, MTableWidgetItem(""))
            self.setItem(len(self.searchAndReplaceTableValues), 3, MTableWidgetItem(""))
            twiItem = MTableWidgetItem(" ")
            twiItem.setCheckState(Mt.Checked)
            self.setItem(len(self.searchAndReplaceTableValues), 4, twiItem)
            twiItem1 = MTableWidgetItem(" ")
            twiItem1.setCheckState(Mt.Checked)
            self.setItem(len(self.searchAndReplaceTableValues), 5, twiItem1)
            twiItem2 = MTableWidgetItem(" ")
            twiItem2.setCheckState(Mt.Unchecked)
            self.setItem(len(self.searchAndReplaceTableValues), 6, twiItem2)
            self.isShowChanges=True
            self.mMenu = MMenu()
            self.namesOfButtons = [translate("Options/SearchAndReplace", "Cut"),
                                    translate("Options/SearchAndReplace", "Copy"),
                                    translate("Options/SearchAndReplace", "Paste"),
                                    translate("Options/SearchAndReplace", "Delete"),
                                    translate("Options/SearchAndReplace", "Change"), 
                                    translate("Options/SearchAndReplace", "Delete Row")]
            for btnName in self.namesOfButtons:
                self.mMenu.addAction(btnName).setObjectName(btnName)
        
        def contextMenuEvent(self,_action):
            try:
                self.mMenu.setGeometry(_action.globalX(),_action.globalY(),1,1)
                selected = self.mMenu.exec_()
                if selected!=None:
                    if selected.objectName()==self.namesOfButtons[0]:
                        MApplication.clipboard().setText(self.currentItem().text())
                        self.currentItem().setText("")
                    elif selected.objectName()==self.namesOfButtons[1]:
                        MApplication.clipboard().setText(self.currentItem().text())
                    elif selected.objectName()==self.namesOfButtons[2]:
                        self.currentItem().setText(MApplication.clipboard().text())
                    elif selected.objectName()==self.namesOfButtons[3]:
                        self.currentItem().setText("")
                        self.editItem(self.currentItem())
                    elif selected.objectName()==self.namesOfButtons[4]:
                        self.editItem(self.currentItem())
                    elif selected.objectName()==self.namesOfButtons[5]:
                        self.hideRow(self.currentItem().row())
            except:
                error = ReportBug.ReportBug()
                error.show()
        
        def clicked(self, _row, _column):
            try:
                if len(self.currentItem().text())*8>self.columnWidth(_column):
                    self.setColumnWidth(_column,len(self.currentItem().text())*8)
            except:pass
        
        def itemChanged(self, _item):
            if self.isShowChanges==True:
                try:
                    lastRowNo = -1
                    for rowNo in range(self.rowCount(), 0, -1):
                        if self.isRowHidden(rowNo -1)==False:
                            lastRowNo = rowNo -1
                            break
                    if _item.row()==lastRowNo and self.item(lastRowNo, 1).text()!="" :
                        self.setRowCount(self.rowCount()+1)
                        self.isShowChanges = False
                        self.setItem(self.rowCount()-1, 1, MTableWidgetItem(""))
                        self.setItem(self.rowCount()-1, 2, MTableWidgetItem(""))
                        self.setItem(self.rowCount()-1, 3, MTableWidgetItem(""))
                        twiItem = MTableWidgetItem(" ")
                        twiItem.setCheckState(Mt.Checked)
                        self.setItem(self.rowCount()-1, 4, twiItem)
                        twiItem1 = MTableWidgetItem(" ")
                        twiItem1.setCheckState(Mt.Checked)
                        self.setItem(self.rowCount()-1, 5, twiItem1)
                        twiItem2 = MTableWidgetItem(" ")
                        twiItem2.setCheckState(Mt.Unchecked)
                        self.setItem(self.rowCount()-1, 6, twiItem2)
                        self.isShowChanges = True
                except:pass
        
        def save(self):
            for rowNo in range(self.rowCount()):
                checkStateActive, checkStateCaseSensitive, checkStateRegExp = 0, 0, 0
                if self.item(rowNo, 4).checkState() == Mt.Checked:
                    checkStateActive = 1
                if self.item(rowNo, 5).checkState() == Mt.Checked:
                    checkStateCaseSensitive = 1
                if self.item(rowNo, 6).checkState() == Mt.Checked:
                    checkStateRegExp = 1
                try:
                    temp = self.item(rowNo, 0).text()
                    if self.isRowHidden(rowNo):
                        Databases.SearchAndReplaceTable.delete(str(self.item(rowNo, 0).text()))
                    else:
                        if str(self.item(rowNo, 1).text()).strip()!="":
                            Databases.SearchAndReplaceTable.update(str(self.item(rowNo, 0).text()), str(self.item(rowNo, 1).text()), str(self.item(rowNo, 2).text()), str(self.item(rowNo, 3).text()), checkStateActive, checkStateCaseSensitive, checkStateRegExp)
                except:
                    if str(self.item(rowNo, 1).text()).strip()!="":
                        insertedId = Databases.SearchAndReplaceTable.insert(str(self.item(rowNo, 1).text()), str(self.item(rowNo, 2).text()), str(self.item(rowNo, 3).text()), checkStateActive, checkStateCaseSensitive, checkStateRegExp)
                        self.setItem(rowNo, 0, MTableWidgetItem(str(insertedId)))
        
class ClearGeneral(MWidget):
    def __init__(self, _parent=None, _showType = None, _visibleKeys = None):
        MWidget.__init__(self, _parent)
        self._parent = _parent
        self.titleOfCategory = translate("Options/ClearGeneral", "General Cleaning")
        self.labelOfCategory = translate("Options/ClearGeneral", "You can change the settings to clean your system in this section.")
        self.categoryNo = None
        self.Panel = MVBoxLayout(self)
        self.values, self.lblLabels = [], []
        self.keysOfSettings = ["isActiveClearGeneral", "isDeleteEmptyDirectories", "unneededDirectoriesIfIsEmpty", "unneededDirectories", 
                            "unneededFiles", "unneededFileExtensions", 
                            "ignoredDirectories", "ignoredFiles", "ignoredFileExtensions", 
                            "isClearEmptyDirectoriesWhenSave", "isClearEmptyDirectoriesWhenMoveOrChange", 
                            "isClearEmptyDirectoriesWhenCopyOrChange", "isClearEmptyDirectoriesWhenFileMove", 
                            "isAutoCleanSubFolderWhenSave", "isAutoCleanSubFolderWhenMoveOrChange", 
                            "isAutoCleanSubFolderWhenCopyOrChange", "isAutoCleanSubFolderWhenFileMove"]
        self.tabsOfSettings = [None, 0, 0, 0, 
                                0, 0, 
                                0, 0, 0, 
                                1, 1, 
                                1, 1, 
                                1, 1, 
                                1, 1]
        self.tabNames = [translate("Options/ClearGeneral", "General"), 
                         translate("Options/ClearGeneral", "Make On ..")]
        if _visibleKeys==None:
            self.visibleKeys = self.keysOfSettings
        else:
            self.visibleKeys = _visibleKeys
        self.neededRestartSettingKeys = []
        self.valuesOfOptionsKeys = []
        self.labels = [translate("Options/ClearGeneral", "Activate General Cleaner"), 
                    translate("Options/ClearGeneral", "Delete Empty Directories"), 
                    translate("Options/ClearGeneral", "Unnecessary Directories (If Is Empty)"), 
                    translate("Options/ClearGeneral", "Unnecessary Directories"), 
                    translate("Options/ClearGeneral", "Unnecessary Files"), 
                    translate("Options/ClearGeneral", "Unnecessary File Extensions"), 
                    translate("Options/ClearGeneral", "Directories To Be Ignored"), 
                    translate("Options/ClearGeneral", "Files To Be Ignored"), 
                    translate("Options/ClearGeneral", "File Extensions To Be Ignored"), 
                    translate("Options/ClearGeneral", "General Cleaning (Table Saved)"), 
                    translate("Options/ClearGeneral", "General Cleaning (Moved Or Changed)"), 
                    translate("Options/ClearGeneral", "General Cleaning (Copied Or Changed)"), 
                    translate("Options/ClearGeneral", "General Cleaning (Moved File)"), 
                    translate("Options/ClearGeneral", "Clean Subfolders (Table Saved)"), 
                    translate("Options/ClearGeneral", "Clean Subfolders (Moved Or Changed)"), 
                    translate("Options/ClearGeneral", "Clean Subfolders (Copied Or Changed)"), 
                    translate("Options/ClearGeneral", "Clean Subfolders (Moved File)")]
        self.toolTips = [translate("Options/ClearGeneral", "Are you want to activate General Cleaner?"), 
                    translate("Options/ClearGeneral", "Are you want to delete empty directories?"), 
                    translate("Options/ClearGeneral", "<font color=red>The directories (empty) you selected will be deleted permanently from your system!</font><br><font color=blue>Example: directory1;directory2;...</font>"), 
                    translate("Options/ClearGeneral", "<font color=red>The directories you selected will be deleted permanently from your system!</font><br><font color=blue>Example: directory1;directory2;...</font>"), 
                    translate("Options/ClearGeneral", "<font color=red>The files you selected will be deleted permanently from your system!</font><br><font color=blue>Example: file1.abc; file2.def;...</font>"), 
                    translate("Options/ClearGeneral", "<font color=red>The file extensions you selected will be deleted permanently from your system!</font><br><font color=blue>Example: mood; db;...</font>"), 
                    translate("Options/ClearGeneral", "If the folders contain only the directories that match the criteria you selected here, they will be recognized as empty and will be deleted.<br><font color=blue>Example: directory1;directory2;...</font>"), 
                    translate("Options/ClearGeneral", "If the folders contain only the files that match the criteria you selected here, they will be recognized as empty and will be deleted.<br><font color=blue>Example: file1.abc; file2.def;...</font>"), 
                    translate("Options/ClearGeneral", "If the folders contain only the files that have the extensions which match the criteria you selected here, they will be recognized as empty and will be deleted.<br><font color=blue>Example: m3u; pls;...</font>"), 
                    translate("Options/ClearGeneral", "Do you want to general cleaning when table saved?"), 
                    translate("Options/ClearGeneral", "Do you want to general cleaning when directory moved or changed?"), 
                    translate("Options/ClearGeneral", "Do you want to general cleaning when directory copied or changed?"), 
                    translate("Options/ClearGeneral", "Do you want to general cleaning when file moved?"), 
                    translate("Options/ClearGeneral", "Do you want to clear the subfolders when table saved?"), 
                    translate("Options/ClearGeneral", "Do you want to clear the subfolders when directory moved or changed?"), 
                    translate("Options/ClearGeneral", "Do you want to clear the subfolders when directory copied or changed?"), 
                    translate("Options/ClearGeneral", "Do you want to clear the subfolders when file moved?")]
        self.typesOfValues = ["Yes/No", "Yes/No", "list", "list", "list", "list", "list", "list", "list", 
                              "Yes/No", "Yes/No", "Yes/No", "Yes/No", "Yes/No", "Yes/No", "Yes/No", "Yes/No"]
        self.valuesOfOptions = []
        _parent.createOptions(self) 
        if self.visibleKeys.count("isActiveClearGeneral")>0:
            MObject.connect(self.values[self.keysOfSettings.index("isActiveClearGeneral")], SIGNAL("currentIndexChanged(int)"), self.activeClearGeneralChanged)
            self.activeClearGeneralChanged()
        if self.visibleKeys.count("isDeleteEmptyDirectories")>0:
            MObject.connect(self.values[self.keysOfSettings.index("isDeleteEmptyDirectories")], SIGNAL("currentIndexChanged(int)"), self.deleteEmptyDirectoriesChanged)
            self.deleteEmptyDirectoriesChanged()
            
    def activeClearGeneralChanged(self):
        if self.values[self.keysOfSettings.index("isActiveClearGeneral")].currentIndex()==1:
            self.tabwTabs.setEnabled(True)
        else:
            self.tabwTabs.setEnabled(False)
            
    def deleteEmptyDirectoriesChanged(self):
        if self.values[self.keysOfSettings.index("isDeleteEmptyDirectories")].currentIndex()==1:
            self._parent.setEnabledFormItems(self, "unneededDirectoriesIfIsEmpty", False)
            self._parent.setEnabledFormItems(self, "ignoredDirectories", True)
            self._parent.setEnabledFormItems(self, "ignoredFiles", True)
            self._parent.setEnabledFormItems(self, "ignoredFileExtensions", True)
        else:
            self._parent.setEnabledFormItems(self, "unneededDirectoriesIfIsEmpty", True)
            self._parent.setEnabledFormItems(self, "ignoredDirectories", False)
            self._parent.setEnabledFormItems(self, "ignoredFiles", False)
            self._parent.setEnabledFormItems(self, "ignoredFileExtensions", False)
        
class Cover(MWidget):
    def __init__(self, _parent=None, _showType = None, _visibleKeys = None):
        MWidget.__init__(self, _parent)
        self._parent = _parent
        self.titleOfCategory = translate("Options/Cover", "Cover")
        self.labelOfCategory = translate("Options/Cover", "You can change the cover settings in this section.")
        self.categoryNo = None
        self.Panel = MVBoxLayout(self)
        self.values, self.lblLabels = [], []
        self.keysOfSettings = ["priorityIconNames", "isChangeExistIcon", "isAskIfHasManyImagesInAlbumDirectory", 
                            "isActiveAutoMakeIconToDirectory", 
                            "isAutoMakeIconToDirectoryWhenSave", "isAutoMakeIconToDirectoryWhenMoveOrChange", 
                            "isAutoMakeIconToDirectoryWhenCopyOrChange", "isAutoMakeIconToDirectoryWhenFileMove", 
                            "iconNameFormat", "iconFileType"]
        self.tabsOfSettings = [0, 0, 0, 0, 0, 0, 0, 0, 
                               1, 1]
        self.tabNames = [translate("Options/Cover", "General"), 
                         translate("Options/Cover", "For Amarok")]
        if _visibleKeys==None:
            self.visibleKeys = self.keysOfSettings
        else:
            self.visibleKeys = _visibleKeys
        self.neededRestartSettingKeys = []
        self.labels = [translate("Options/Cover", "Priority Icon Names"), 
                    translate("Options/Cover", "Change Directory Icon If Is Already Exist"), 
                    translate("Options/Cover", "Ask Me If Has Many Images"), 
                    translate("Options/Cover", "Auto Change Directory Icon"), 
                    translate("Options/Cover", "Change Directory Icon (Table Saved)"), 
                    translate("Options/Cover", "Change Directory Icon (Moved Or Changed)"), 
                    translate("Options/Cover", "Change Directory Icon (Copied Or Changed)"), 
                    translate("Options/Cover", "Change Directory Icon (Moved File)"), 
                    translate("Options/Cover", "Icon Name Format"), 
                    translate("Options/Cover", "Icon Type")]
        self.toolTips = [translate("Options/Cover", "The file names you selected will be folder icons first.<br>If the file name you selected does not exist, the first graphics file in the folder will be set as the folder icon.<br><font color=blue>Example: cover; icon...</font>"), 
                    translate("Options/Cover", "Are you want to change directory icon if is already exist?"), 
                    translate("Options/Cover", "Ask me if has many images in the directory.<br>Note: If you select \"No\" the first image will be chosen."), 
                    translate("Options/Cover", "Are you want to change directory icon automatically?"), 
                    translate("Options/Cover", "Do you want to change directory icon when table saved?"), 
                    translate("Options/Cover", "Do you want to change directory icon when directory moved or changed?"), 
                    translate("Options/Cover", "Do you want to change directory icon when directory copied or changed?"), 
                    translate("Options/Cover", "Do you want to change directory icon when file moved?"), 
                    translate("Options/Cover", "You can set icon name format."), 
                    translate("Options/Cover", "You can select file type of icon.")]
        self.typesOfValues = ["list", "Yes/No", "Yes/No", 
                    "Yes/No", "Yes/No", "Yes/No", "Yes/No", "Yes/No", 
                    ["trString", 0], ["options", 0]]
        self.valuesOfOptions = [["png", "jpg"]]
        self.valuesOfOptionsKeys = [["png", "jpg"]]
        self.stringSearchList = [Variables.iconNameFormatKeys]
        self.stringReplaceList = [Universals.iconNameFormatLabels]
        _parent.createOptions(self) 
        if self.visibleKeys.count("isActiveAutoMakeIconToDirectory")>0:
            MObject.connect(self.values[self.keysOfSettings.index("isActiveAutoMakeIconToDirectory")], SIGNAL("currentIndexChanged(int)"), self.activeAutoMakeIconToDirectory)
            self.activeAutoMakeIconToDirectory()
        if Universals.isActiveAmarok==False:
            self.tabwTabs.setTabEnabled(1, False)
            
    def activeAutoMakeIconToDirectory(self):
        if self.values[self.keysOfSettings.index("isActiveAutoMakeIconToDirectory")].currentIndex()==1:
            self._parent.setEnabledFormItems(self, "isAutoMakeIconToDirectoryWhenSave", True)
            self._parent.setEnabledFormItems(self, "isAutoMakeIconToDirectoryWhenMoveOrChange", True)
            self._parent.setEnabledFormItems(self, "isAutoMakeIconToDirectoryWhenCopyOrChange", True)
            self._parent.setEnabledFormItems(self, "isAutoMakeIconToDirectoryWhenFileMove", True)
        else:
            self._parent.setEnabledFormItems(self, "isAutoMakeIconToDirectoryWhenSave", False)
            self._parent.setEnabledFormItems(self, "isAutoMakeIconToDirectoryWhenMoveOrChange", False)
            self._parent.setEnabledFormItems(self, "isAutoMakeIconToDirectoryWhenCopyOrChange", False)
            self._parent.setEnabledFormItems(self, "isAutoMakeIconToDirectoryWhenFileMove", False)
 

class Advanced(MWidget):
    def __init__(self, _parent=None, _showType = None, _visibleKeys = None):
        MWidget.__init__(self, _parent)
        self._parent = _parent
        self.titleOfCategory = translate("Options/Advanced", "Advanced")
        self.labelOfCategory = translate("Options/Advanced", "You can change the advanced settings in this section.<br><font color=red>Only proceed when you make sure that everything here is correct.</font>")
        self.categoryNo = None
        self.Panel = MVBoxLayout(self)
        self.values, self.lblLabels = [], []
        self.keysOfSettings = ["fileSystemEncoding", "imageExtensions", "musicExtensions", "NeededObjectsName", "isActivePyKDE4", "isDontDeleteFileAndDirectory", "pathOfDeletedFilesAndDirectories"]
        self.tabsOfSettings = [None, None, None, None, None, None, None]
        self.tabNames = []
        if _visibleKeys==None:
            self.visibleKeys = self.keysOfSettings
        else:
            self.visibleKeys = _visibleKeys
        self.neededRestartSettingKeys = ["fileSystemEncoding", "NeededObjectsName", "isActivePyKDE4"]
        self.valuesOfOptionsKeys = []
        self.labels = [translate("Options/Advanced", "File System Character Set"), 
                    translate("Options/Advanced", "Graphics Files` Extensions"), 
                    translate("Options/Advanced", "Music Files` Extensions"), 
                    translate("Options/Advanced", "Please Select The Object Set You Want To Use"), 
                    translate("Options/Advanced", "Do You Want To Use PyKDE4?"), 
                    translate("Options/Advanced", "Never Delete Files And Directories"), 
                    translate("Options/Advanced", "Path Of Deleted Files And Directories")]
        self.toolTips = [trForUI(str(translate("Options/Advanced", "You can choose the character set of your operating system and/or file system. The records will be saved according to the character set of your choice.<br><font color=red><b>If you think the character set is wrong, you can change it. However we do not recommend to make any changes if you are not definitely sure. Else, proceed at your own responsibility!<br>Default is \"%s\".</b></font>")) % (Variables.defaultFileSystemEncoding)), 
                    translate("Options/Advanced", "The files with the extension you have selected will be recognized as graphics files.<br><font color=red><b>We do not recommend to make any changes if you are not definitely sure. Proceed at your own responsibility!</b></font><br><font color=blue>Example: png;jpg;gif;...</font>"), 
                    translate("Options/Advanced", "The files with the extension you have selected will be recognized as music files.<br><font color=red><b>We do not recommend to make any changes if you are not definitely sure. Proceed at your own responsibility!</b></font><br><font color=blue>Example: mp3;...</font>"), 
                    translate("Options/Advanced", "KPlease select the object set you want to use (the object types installed on your system will be presented in the Options dialog.)"), 
                    translate("Options/Advanced", "<font color=blue>You can use PyKDE4 for better desktop integration.</font>"), 
                    translate("Options/Advanced", "Would you like to move files to specific directory to be deleted?<br><font color=red><b>This process can cause slow!</b></font>"), 
                    translate("Options/Advanced", "")]
        self.typesOfValues = [["options", 0], "list", "list", ["options", 1], "Yes/No", "Yes/No", ["directory", "exist"]]
        charSets = Variables.getCharSets()
        objectsNames = Variables.getMyObjectsNames()
        if Variables.isAvailablePyKDE4()==False:
            keyNo = self.keysOfSettings.index("isActivePyKDE4")
            del self.keysOfSettings[keyNo]
            del self.labels[keyNo]
            del self.toolTips[keyNo]
            del self.typesOfValues[keyNo]
        self.valuesOfOptions = [charSets, objectsNames]
        self.valuesOfOptionsKeys = [charSets, objectsNames]
        _parent.createOptions(self) 
        if self.visibleKeys.count("isDontDeleteFileAndDirectory")>0:
            MObject.connect(self.values[self.keysOfSettings.index("isDontDeleteFileAndDirectory")], SIGNAL("currentIndexChanged(int)"), self.dontDeleteFileAndDirectoryChanged)
            self.dontDeleteFileAndDirectoryChanged()
    
    def dontDeleteFileAndDirectoryChanged(self):
        if self.values[self.keysOfSettings.index("isDontDeleteFileAndDirectory")].currentIndex()==1:
            self._parent.setVisibleFormItems(self, "pathOfDeletedFilesAndDirectories", True)
        else:
            self._parent.setVisibleFormItems(self, "pathOfDeletedFilesAndDirectories", False)
        
class Player(MWidget):
    def __init__(self, _parent=None, _showType = None, _visibleKeys = None):
        MWidget.__init__(self, _parent)
        self._parent = _parent
        self.titleOfCategory = translate("Options/Player", "Player")
        self.labelOfCategory = translate("Options/Player", "You can change the player settings in this section.")
        self.categoryNo = None
        self.Panel = MVBoxLayout(self)
        self.values, self.lblLabels = [], []
        self.keysOfSettings = ["playerName","mplayerPath", "mplayerArgs", "mplayerAudioDevicePointer", "mplayerAudioDevice"]
        self.tabsOfSettings = [None, None, None, None, None]
        self.tabNames = []
        if _visibleKeys==None:
            self.visibleKeys = self.keysOfSettings
        else:
            self.visibleKeys = _visibleKeys
        self.neededRestartSettingKeys = []
        self.valuesOfOptionsKeys = []
        self.labels = [translate("Options/Player", "Player Name"), 
                    translate("Options/Player", "Player Path (Name)"), 
                    translate("Options/Player", "Player Arguments"), 
                    translate("Options/Player", "Player Sound Playback Device Pointer"), 
                    translate("Options/Player", "Player Sound Playback Device")]
        self.toolTips = [translate("Options/Player", "Please select the player you want to use.<br>"+
                    "If installed, the following players will be presented in the Options dialog and you will be able to select the one you want to use.<br>"+
                    "Mplayer<br>Phonon (Recommended)<br>Phonon (PySide) (Recommended)<br>tkSnack"), 
                    translate("Options/Player", "Please enter the path of the player program you want to use.<br><font color=red>Default value: mplayer</font>"), 
                    translate("Options/Player", "Please enter the player arguments.<br><font color=red>Default value(s): -slave -quiet</font>"), 
                    translate("Options/Player", "The argument used to point to the sound device you want to use.<br><font color=red>Default value: -ao</font>"),
                    translate("Options/Player", "The sound device you want to use.<br><font color=red>Default value: alsa</font>")]
        self.typesOfValues = [["options", 0], ["file", "executable"], "string", "string", ["options", 1]]
        self.valuesOfOptions = [Variables.getAvailablePlayers(), Variables.mplayerSoundDevices]
        self.valuesOfOptionsKeys = [Variables.getAvailablePlayers(), Variables.mplayerSoundDevices]
        _parent.createOptions(self)
        if self.visibleKeys.count("playerName")>0:
            MObject.connect(self.values[self.keysOfSettings.index("playerName")], SIGNAL("currentIndexChanged(int)"), self.playerChanged)
            self.playerChanged()
    
    def playerChanged(self):
        if self.values[self.keysOfSettings.index("playerName")].currentIndex()==0:
            self._parent.setVisibleFormItems(self, "mplayerPath", True)
            self._parent.setVisibleFormItems(self, "mplayerArgs", True)
            self._parent.setVisibleFormItems(self, "mplayerAudioDevicePointer", True)
            self._parent.setVisibleFormItems(self, "mplayerAudioDevice", True)
        else:
            self._parent.setVisibleFormItems(self, "mplayerPath", False)
            self._parent.setVisibleFormItems(self, "mplayerArgs", False)
            self._parent.setVisibleFormItems(self, "mplayerAudioDevicePointer", False)
            self._parent.setVisibleFormItems(self, "mplayerAudioDevice", False)

class Packager(MWidget):
    def __init__(self, _parent=None, _showType = None, _visibleKeys = None):
        MWidget.__init__(self, _parent)
        self._parent = _parent
        self.titleOfCategory = translate("Options/Packager", "Packager")
        self.labelOfCategory = translate("Options/Packager", "You can change the packager-specific settings in this section.")
        self.categoryNo = None
        self.Panel = MVBoxLayout(self)
        self.values, self.lblLabels = [], []
        self.keysOfSettings = ["isPackagerDeleteEmptyDirectories", "packagerUnneededFiles", "packagerUnneededFileExtensions", 
                                "packagerUnneededDirectories", "isClearEmptyDirectoriesWhenPath",
                                "isAutoCleanSubFolderWhenPath", "isCloseOnCleanAndPackage"]
        self.tabsOfSettings = [None, None, None, 
                               None, None, 
                               None, None]
        self.tabNames = []
        if _visibleKeys==None:
            self.visibleKeys = self.keysOfSettings
        else:
            self.visibleKeys = _visibleKeys
        self.neededRestartSettingKeys = []
        self.valuesOfOptionsKeys = []
        self.labels = [translate("Options/Packager", "Delete Empty Directories"), 
                    translate("Options/Packager", "Unnecessary Files"),
                    translate("Options/Packager", "Unnecessary File Extensions"), 
                    translate("Options/Packager", "Unnecessary Folders"), 
                    translate("Options/Packager", "General Cleaning"), 
                    translate("Options/Packager", "Auto Clean Subfolders"), 
                    translate("Options/Packager", "Close When Cleaned And Packed?")]
        self.toolTips = [translate("Options/Packager", "Are you want to delete empty directories?"), 
                    translate("Options/Packager", "Please select the files that you DO NOT want to be included in the package"), 
                    translate("Options/Packager", "Please select the file extensions that you DO NOT want to be included in the package"), 
                    translate("Options/Packager", "Please select the files that you DO NOT want to be included in the package"), 
                    translate("Options/Packager", "Do you want to general cleaning?"), 
                    translate("Options/Packager", "You have to select to clear the subfolders automatically."), 
                    translate("Options/Packager", "Close the package manager when the folder is cleaned and packed?")]
        self.typesOfValues = ["Yes/No", "list", "list", "list", "Yes/No", "Yes/No", "Yes/No"]
        self.valuesOfOptions = []
        _parent.createOptions(self) 
    
class Cleaner(MWidget):
    def __init__(self, _parent=None, _showType = None, _visibleKeys = None):
        MWidget.__init__(self, _parent)
        self._parent = _parent
        self.titleOfCategory = translate("Options/Cleaner", "Cleaner")
        self.labelOfCategory = translate("Options/Cleaner", "You can change the cleaner-specific settings in this section.")
        self.categoryNo = None
        self.Panel = MVBoxLayout(self)
        self.values, self.lblLabels = [], []
        self.keysOfSettings = ["isCleanerDeleteEmptyDirectories", "cleanerUnneededFiles", "cleanerUnneededFileExtensions", 
                                "cleanerUnneededDirectories", "isClearEmptyDirectoriesWhenClear",
                                "isAutoCleanSubFolderWhenClear"]
        self.tabsOfSettings = [None, None, None, 
                                None, None, 
                                None]
        self.tabNames = []
        if _visibleKeys==None:
            self.visibleKeys = self.keysOfSettings
        else:
            self.visibleKeys = _visibleKeys
        self.neededRestartSettingKeys = []
        self.valuesOfOptionsKeys = []
        self.labels = [translate("Options/Cleaner", "Delete Empty Directories"), 
                    translate("Options/Cleaner", "Unnecessary Files"),
                    translate("Options/Cleaner", "Unnecessary File Extensions"), 
                    translate("Options/Cleaner", "Unnecessary Folders"), 
                    translate("Options/Cleaner", "General Cleaning"), 
                    translate("Options/Cleaner", "Auto Clean Subfolders")]
        self.toolTips = [translate("Options/Cleaner", "Are you want to delete empty directories?"), 
                    translate("Options/Cleaner", "Please select the files that you want to be deleted"), 
                    translate("Options/Cleaner", "Please select the file extensions that you want to be deleted"), 
                    translate("Options/Cleaner", "Please select the files that you want to be deleted"), 
                    translate("Options/Cleaner", "Do you want to general cleaning?"), 
                    translate("Options/Cleaner", "You have to select to clear the subfolders automatically.")]
        self.typesOfValues = ["Yes/No", "list", "list", "list", "Yes/No", "Yes/No"]
        self.valuesOfOptions = []
        _parent.createOptions(self) 
        
class Amarok(MWidget):
    def __init__(self, _parent=None, _showType = None, _visibleKeys = None):
        MWidget.__init__(self, _parent)
        self._parent = _parent
        self.titleOfCategory = translate("Options/Amarok", "Amarok")
        self.labelOfCategory = translate("Options/Amarok", "You can change the Amarok settings in this section.")
        self.categoryNo = None
        self.Panel = MVBoxLayout(self)
        self.values, self.lblLabels = [], []
        self.keysOfSettings = ["amarokIsUseHost", "amarokDBHost", "amarokDBPort", "amarokDBUser", "amarokDBPass", "amarokDBDB", "isReadOnlyAmarokDB", "isReadOnlyAmarokDBHost", "pathOfMysqldSafe"]
        self.tabsOfSettings = [None, None, None, None, None, None, None, None, None]
        self.tabNames = []
        if _visibleKeys==None:
            self.visibleKeys = self.keysOfSettings
        else:
            self.visibleKeys = _visibleKeys
        self.neededRestartSettingKeys = ["amarokIsUseHost", "isReadOnlyAmarokDB", "isReadOnlyAmarokDBHost"]
        self.valuesOfOptionsKeys = []
        self.labels = [translate("Options/Amarok", "Using MySQL Server"), 
                    translate("Options/Amarok", "Host"), 
                    translate("Options/Amarok", "Port"), 
                    translate("Options/Amarok", "User Name"), 
                    translate("Options/Amarok", "Password"), 
                    translate("Options/Amarok", "Database"), 
                    translate("Options/Amarok", "Read Only Connection"), 
                    translate("Options/Amarok", "Read Only Connection"), 
                    translate("Options/Amarok", "Path Of Executable \"mysqld_safe\"")]
        self.toolTips = [translate("Options/Amarok", "Are you use MySQL server in the Amarok?"), 
                    translate("Options/Amarok", "Please enter host name of Amarok database."), 
                    translate("Options/Amarok", "Please enter port number of Amarok database."), 
                    translate("Options/Amarok", "Please enter user name of Amarok database."), 
                    translate("Options/Amarok", "Please enter user password of Amarok database."), 
                    translate("Options/Amarok", "Please enter database name of Amarok database."), 
                    translate("Options/Amarok", "Are you want to read only connection to database?<br>If you select \"Yes\" : Amarok database files will be copied to %s. Any changes will not be written to the database so some things will not be run.<br>If you select \"No\" : Some Hamsi Manager default database files will be copied to %s. All existing files will be backup and after will be replaced. Some changes will be written to the database."), 
                    translate("Options/Amarok", "Are you want to read only connection to database?<br>If you select \"No\" : Some changes will be written to the database. <br>If you select \"Yes\" : Any changes will not be written to the database so some things will not be run."), 
                    translate("Options/Amarok", "Where is executable \"mysqld_safe\" file?")]
        self.typesOfValues = ["Yes/No", "string", "string", "string", "password", "string", "Yes/No", "Yes/No", ["file", "executable"]]
        self.valuesOfOptions = []
        self.valuesOfOptionsKeys = []
        _parent.createOptions(self)
        pbtnTestAmarokMysql = MPushButton(translate("Options/Amarok", "Test"))
        hblBottom = MHBoxLayout()
        self.Panel.addLayout(hblBottom)
        hblBottom.addWidget(pbtnTestAmarokMysql)
        MObject.connect(pbtnTestAmarokMysql, SIGNAL("clicked()"), self.testAmarokMysql)
        if self.visibleKeys.count("amarokIsUseHost")>0:
            MObject.connect(self.values[self.keysOfSettings.index("amarokIsUseHost")], SIGNAL("currentIndexChanged(int)"), self.useMySQLServerChanged)
            self.useMySQLServerChanged()
    
    def useMySQLServerChanged(self):
        if self.values[self.keysOfSettings.index("amarokIsUseHost")].currentIndex()==0:
            self._parent.setVisibleFormItems(self, "amarokDBHost", False)
            self._parent.setVisibleFormItems(self, "amarokDBPort", False)
            self._parent.setVisibleFormItems(self, "amarokDBUser", False)
            self._parent.setVisibleFormItems(self, "amarokDBPass", False)
            self._parent.setVisibleFormItems(self, "amarokDBDB", False)
            self._parent.setVisibleFormItems(self, "pathOfMysqldSafe", True)
            self._parent.setVisibleFormItems(self, "isReadOnlyAmarokDB", True)
            self._parent.setVisibleFormItems(self, "isReadOnlyAmarokDBHost", False)
        else:
            self._parent.setVisibleFormItems(self, "amarokDBHost", True)
            self._parent.setVisibleFormItems(self, "amarokDBPort", True)
            self._parent.setVisibleFormItems(self, "amarokDBUser", True)
            self._parent.setVisibleFormItems(self, "amarokDBPass", True)
            self._parent.setVisibleFormItems(self, "amarokDBDB", True)
            self._parent.setVisibleFormItems(self, "pathOfMysqldSafe", False)
            self._parent.setVisibleFormItems(self, "isReadOnlyAmarokDB", False)
            self._parent.setVisibleFormItems(self, "isReadOnlyAmarokDBHost", True)
    
    def saveSettingsForTest(self):
        self._parent.applySetting(self, "amarokIsUseHost")
        self._parent.applySetting(self, "amarokDBHost")
        self._parent.applySetting(self, "amarokDBPort")
        self._parent.applySetting(self, "amarokDBUser")
        self._parent.applySetting(self, "amarokDBPass")
        self._parent.applySetting(self, "amarokDBDB")
    
    def testAmarokMysql(self):
        try:
            import Amarok
            self.saveSettingsForTest()
            amarokDb = Amarok.checkAndGetDB(False, True)
            if amarokDb!=None:
                answer = Dialogs.ask(translate("Options/Amarok", "Are You Want To Save"), 
                                             translate("Options/Amarok", "Are you want to save this Amarok settings?"))
                if answer==Dialogs.Yes:
                    Universals.saveSettings()
            amarokDb = None
        except:
            error = ReportBug.ReportBug()
            error.show()

class HiddenObjects(MWidget):
    def __init__(self, _parent=None, _showType = None, _visibleKeys = None):
        MWidget.__init__(self, _parent)
        self._parent = _parent
        self.titleOfCategory = translate("Options/HiddenObjects", "Hidden Objects")
        self.labelOfCategory = translate("Options/HiddenObjects", "You can change the hidden files / directories visibility in this section.")
        self.categoryNo = None
        self.Panel = MVBoxLayout(self)
        self.values, self.lblLabels = [], []
        self.keysOfSettings = ["isShowHiddensInSubFolderTable", "isShowHiddensInFolderTable", "isShowHiddensInFileTable", 
                                "isShowHiddensInMusicTable", "isShowHiddensInCoverTable"]
        self.tabsOfSettings = [0, 0, 0, 0, 0]
        self.tabNames = [translate("Options/ClearGeneral", "Show Hidden Files / Directories ...")]
        if _visibleKeys==None:
            self.visibleKeys = self.keysOfSettings
        else:
            self.visibleKeys = _visibleKeys
        self.neededRestartSettingKeys = []
        self.valuesOfOptionsKeys = []
        self.labels = [translate("Options/HiddenObjects", "In SubFolder Table"), 
                    translate("Options/HiddenObjects", "In Folder Table"), 
                    translate("Options/HiddenObjects", "In File Table"), 
                    translate("Options/HiddenObjects", "In Music Table"), 
                    translate("Options/HiddenObjects", "In Cover Table")]
        self.toolTips = [translate("Options/HiddenObjects", "Are you want to show hidden files and directories in subfolder table?"), 
                    translate("Options/HiddenObjects", "Are you want to show hidden files and directories in folder table?"), 
                    translate("Options/HiddenObjects", "Are you want to show hidden files in file table?"), 
                    translate("Options/HiddenObjects", "Are you want to show hidden files in music table?"),
                    translate("Options/HiddenObjects", "Are you want to show hidden directories in cover table?")]
        self.typesOfValues = ["Yes/No", "Yes/No", "Yes/No", "Yes/No", "Yes/No"]
        self.valuesOfOptions = []
        self.valuesOfOptionsKeys = []
        if Universals.isActiveDirectoryCover==False:
            self.visibleKeys.remove("isShowHiddensInCoverTable")
        _parent.createOptions(self)

class MySettings(MWidget):
    def __init__(self, _parent=None, _showType = None, _visibleKeys = None):
        MWidget.__init__(self, _parent)
        self._parent = _parent
        self.titleOfCategory = translate("Options/MySettings", "Settings")
        self.labelOfCategory = translate("Options/MySettings", "You can reset you settings or back them up in this section.")
        self.categoryNo = None
        self.Panel = MVBoxLayout(self)
        Panel0 = MHBoxLayout()
        Panel1 = MHBoxLayout()
        Panel2 = MHBoxLayout()
        left0 = MVBoxLayout()
        right0 = MVBoxLayout()
        left1 = MVBoxLayout()
        right1 = MVBoxLayout()
        left2 = MVBoxLayout()
        right2 = MVBoxLayout()
        bottom1 = MHBoxLayout()
        self.values, self.lblLabels = [], []
        self.keysOfSettings = []
        self.tabsOfSettings = []
        self.tabNames = []
        if _visibleKeys==None:
            self.visibleKeys = self.keysOfSettings
        else:
            self.visibleKeys = _visibleKeys
        self.neededRestartSettingKeys = []
        self.valuesOfOptionsKeys = []
        self.labels = []
        self.toolTips = []
        self.typesOfValues = []
        self.valuesOfOptions = []
        lblBackUp = MLabel(trForUI("<b>" + translate("Options/MySettings", "Backup Settings") + "</b>"))
        lblRestore = MLabel(trForUI("<b>" + translate("Options/MySettings", "Restore Settings") + "</b>"))
        reFillSettings = MLabel(trForUI("<b>" + translate("Options/MySettings", "Reset Settings") + "</b>"))
        lblBackUp.setAlignment(Mt.AlignHCenter)
        lblRestore.setAlignment(Mt.AlignHCenter)
        reFillSettings.setAlignment(Mt.AlignHCenter)
        pbtnRestoreBookmarks = MPushButton(translate("Options/MySettings", "Bookmarks"))
        pbtnRestoreSearchAndReplaceTable = MPushButton(translate("Options/MySettings", "Search-Replace Parameters"))
        pbtnRestoreSettings = MPushButton(translate("Options/MySettings", "Program Settings"))
        pbtnRestoreAll = MPushButton(translate("Options/MySettings", "All"))
        pbtnBackUpBookmarks = MPushButton(translate("Options/MySettings", "Bookmarks"))
        pbtnBackUpSearchAndReplaceTable = MPushButton(translate("Options/MySettings", "Search-Replace Parameters"))
        pbtnBackUpSettings = MPushButton(translate("Options/MySettings", "Program Settings"))
        pbtnBackUpAll = MPushButton(translate("Options/MySettings", "All"))
        pbtnReFillBookmarks = MPushButton(translate("Options/MySettings", "Bookmarks"))
        pbtnReFillSearchAndReplaceTable = MPushButton(translate("Options/MySettings", "Search-Replace Parameters"))
        pbtnReFillSettings = MPushButton(translate("Options/MySettings", "Program Settings"))
        pbtnReFillAll = MPushButton(translate("Options/MySettings", "All"))
        pbtnClearErrorFiles = MPushButton(translate("Options/MySettings", "Delete Error Logs"))
        MObject.connect(pbtnRestoreBookmarks, SIGNAL("clicked()"), self.restoreBookmarks)
        MObject.connect(pbtnRestoreSearchAndReplaceTable, SIGNAL("clicked()"), self.restoreSearchAndReplaceTable)
        MObject.connect(pbtnRestoreSettings, SIGNAL("clicked()"), self.restoreSettings)
        MObject.connect(pbtnRestoreAll, SIGNAL("clicked()"), self.restoreAll)
        MObject.connect(pbtnBackUpBookmarks, SIGNAL("clicked()"), self.backUpBookmarks)
        MObject.connect(pbtnBackUpSearchAndReplaceTable, SIGNAL("clicked()"), self.backUpSearchAndReplaceTable)
        MObject.connect(pbtnBackUpSettings, SIGNAL("clicked()"), self.backUpSettings)
        MObject.connect(pbtnBackUpAll, SIGNAL("clicked()"), self.backUpAll)
        MObject.connect(pbtnReFillBookmarks, SIGNAL("clicked()"), self.reFillBookmarks)
        MObject.connect(pbtnReFillSearchAndReplaceTable, SIGNAL("clicked()"), self.reFillSearchAndReplaceTable)
        MObject.connect(pbtnReFillSettings, SIGNAL("clicked()"), self.reFillSettings)
        MObject.connect(pbtnReFillAll, SIGNAL("clicked()"), self.reFillAll)
        MObject.connect(pbtnClearErrorFiles, SIGNAL("clicked()"), self.clearErrorFiles)
        left0.addWidget(pbtnBackUpBookmarks) 
        left0.addWidget(pbtnBackUpSearchAndReplaceTable) 
        right0.addWidget(pbtnBackUpSettings) 
        right0.addWidget(pbtnBackUpAll) 
        left1.addWidget(pbtnRestoreBookmarks) 
        left1.addWidget(pbtnRestoreSearchAndReplaceTable) 
        right1.addWidget(pbtnRestoreSettings) 
        right1.addWidget(pbtnRestoreAll) 
        left2.addWidget(pbtnReFillBookmarks) 
        left2.addWidget(pbtnReFillSearchAndReplaceTable) 
        right2.addWidget(pbtnReFillSettings) 
        right2.addWidget(pbtnReFillAll) 
        Panel0.addLayout(left0) 
        Panel0.addLayout(right0) 
        Panel1.addLayout(left1) 
        Panel1.addLayout(right1) 
        Panel2.addLayout(left2) 
        Panel2.addLayout(right2) 
        self.Panel.addWidget(lblBackUp)  
        self.Panel.addLayout(Panel0) 
        self.Panel.addWidget(lblRestore)  
        self.Panel.addLayout(Panel1)  
        self.Panel.addWidget(reFillSettings)  
        self.Panel.addLayout(Panel2)  
        self.Panel.addStretch(1)
        self.Panel.addLayout(bottom1)
        hbox1 = MHBoxLayout()
        hbox1.addWidget(pbtnClearErrorFiles)
        gboxErrors = MGroupBox(translate("Options/MySettings", "Error Logs"))
        gboxErrors.setLayout(hbox1)
        self.Panel.addWidget(gboxErrors)
        if Universals.isActivePyKDE4==True:
            pbtnClearMyAnswers = MPushButton(translate("Options/MySettings", "Clear My Answers"))
            pbtnClearMyAnswers.setToolTip(translate("Options/MySettings", "Clear my answers to the notification messages"))
            MObject.connect(pbtnClearMyAnswers, SIGNAL("clicked()"), self.clearMyAnswers)
            bottom1.addWidget(pbtnClearMyAnswers)
            pbtnReInstallKDE4Language = MPushButton(translate("Options/MySettings", "Reinstall Language"))
            MObject.connect(pbtnReInstallKDE4Language, SIGNAL("clicked()"), self.reInstallKDE4Language)
            bottom1.addWidget(pbtnReInstallKDE4Language)
        
    def clearErrorFiles(self):
        try:
            InputOutputs.clearTempFiles()
            Records.saveAllRecords()
            Dialogs.show(translate("Options/General", "Error Logs Deleted"), translate("Options/General", "All created by Hamsi Manager error logs and temp files is deleted."))
        except:
            error = ReportBug.ReportBug()
            error.show()
    
    def clearMyAnswers(self):
        try:
            answer = Dialogs.ask(translate("Options/MySettings", "Your Answers Will Be Cleared"),
                        translate("Options/MySettings", "Are you sure you want to clear your answers to the notification messages?"))
            if answer==Dialogs.Yes:
                MMessageBox.enableAllMessages()
                Dialogs.show(translate("Options/MySettings", "Your Answers Cleared"), 
                        translate("Options/MySettings", "Cleared your answers to the notification messages.All notification messages will be asked again."))
        except:
            error = ReportBug.ReportBug()
            error.show()
                    
    def reInstallKDE4Language(self):
        try:
            from Core import MyConfigure
            answer = Dialogs.ask(translate("Options/MySettings", "KDE4 Language Will Be Reinstalled Into Hamsi Manager"),
                        translate("Options/MySettings", "Are you sure you want to reinstall kde4 language into Hamsi Manager?"))
            if answer==Dialogs.Yes:
                MyConfigure.installKDE4Languages()
                Dialogs.show(translate("Options/MySettings", "Language Reinstallation Completed"), 
                        translate("Options/MySettings", "Language has successfully been reinstalled."))
                self.parent().parent().reStart()
        except:
            error = ReportBug.ReportBug()
            error.show()
    
    def backUpBookmarks(self):
        try:
            Settings.makeBackUp("bookmarks")
            Dialogs.show(translate("Options/MySettings", "Backup Succesfully"), 
                    translate("Options/MySettings", "Backup operation was performed successfully."))
        except:
            error = ReportBug.ReportBug()
            error.show()
    
    def backUpSearchAndReplaceTable(self):
        try:
            Settings.makeBackUp("searchAndReplaceTable")
            Dialogs.show(translate("Options/MySettings", "Backup Succesfully"), 
                    translate("Options/MySettings", "Backup operation was performed successfully."))
        except:
            error = ReportBug.ReportBug()
            error.show()
        
    def backUpSettings(self):
        try:
            Settings.makeBackUp("Settings")
            Dialogs.show(translate("Options/MySettings", "Backup Succesfully"), 
                    translate("Options/MySettings", "Backup operation was performed successfully."))
        except:
            error = ReportBug.ReportBug()
            error.show()
    
    def backUpAll(self):
        try:
            Settings.makeBackUp("All")
            Dialogs.show(translate("Options/MySettings", "Backup Succesfully"), 
                    translate("Options/MySettings", "Backup operation was performed successfully."))
        except:
            error = ReportBug.ReportBug()
            error.show()
    
    def restoreBookmarks(self):
        try:
            if Settings.restoreBackUp("bookmarks")==True:
                self.parent().parent().reStart()
            else:
                Dialogs.showError("Failed To Restore", "An error occurred during restore. Maybe not found any backup file.")
        except:
            error = ReportBug.ReportBug()
            error.show()
    
    def restoreSearchAndReplaceTable(self):
        try:
            if Settings.restoreBackUp("searchAndReplaceTable")==True:
                self.parent().parent().close()
            else:
                Dialogs.showError("Failed To Restore", "An error occurred during restore. Maybe not found any backup file.")
        except:
            error = ReportBug.ReportBug()
            error.show()
        
    def restoreSettings(self):
        try:
            if Settings.restoreBackUp("Settings")==True:
                self.parent().parent().reStart()
            else:
                Dialogs.showError("Failed To Restore", "An error occurred during restore. Maybe not found any backup file.")
        except:
            error = ReportBug.ReportBug()
            error.show()
    
    def restoreAll(self):
        try:
            if Settings.restoreBackUp("All")==True:
                self.parent().parent().reStart()
            else:
                Dialogs.showError("Failed To Restore", "An error occurred during restore. Maybe not found any backup file.")
        except:
            error = ReportBug.ReportBug()
            error.show()

    def reFillBookmarks(self):
        try:
            answer = Dialogs.askSpecial(translate("Options/MySettings", "Are You Sure You Want To Reset?"),
                        translate("Options/MySettings", "Are you sure you want to reset your bookmarks?"), 
                        translate("Options/MySettings", "Yes"), 
                        translate("Options/MySettings", "No (Cancel)"), 
                        translate("Options/MySettings", "Back Up And Reset"))
            if answer==translate("Options/MySettings", "Yes"):
                Databases.reFillDatabases("bookmarks")
            elif answer==translate("Options/MySettings", "Back Up And Reset"):
                Databases.reFillDatabases("bookmarks", _makeBackUp=True)
            self.parent().parent().reStart()
        except:
            error = ReportBug.ReportBug()
            error.show()
        
    def reFillSearchAndReplaceTable(self):
        try:
            answer = Dialogs.askSpecial(translate("Options/MySettings", "Are You Sure You Want To Reset?"),
                        translate("Options/MySettings", "Do you want to reset your find-replace (automatic) settings?"), 
                        translate("Options/MySettings", "Yes"), 
                        translate("Options/MySettings", "No (Cancel)"), 
                        translate("Options/MySettings", "Back Up And Reset"))
            if answer==translate("Options/MySettings", "Yes"):
                Databases.reFillDatabases("searchAndReplaceTable")
            elif answer==translate("Options/MySettings", "Back Up And Reset"):
                Databases.reFillDatabases("searchAndReplaceTable", _makeBackUp=True)
            self.parent().parent().close()
        except:
            error = ReportBug.ReportBug()
            error.show()

    def reFillSettings(self):
        try:
            answer = Dialogs.askSpecial(translate("Options/MySettings", "Are You Sure You Want To Reset?"),
                        translate("Options/MySettings", "Do you want to reset program settings?"), 
                        translate("Options/MySettings", "Yes"), 
                        translate("Options/MySettings", "No (Cancel)"), 
                        translate("Options/MySettings", "Back Up And Reset"))
            if answer==translate("Options/MySettings", "Yes"):
                Settings.reFillSettings()
            elif answer==translate("Options/MySettings", "Back Up And Reset"):
                Settings.reFillSettings(True)
            self.parent().parent().reStart()
        except:
            error = ReportBug.ReportBug()
            error.show()
        
    def reFillAll(self):
        try:
            answer = Dialogs.askSpecial(translate("Options/MySettings", "Are You Sure You Want To Reset?"),
                        translate("Options/MySettings", "Are you sure you want to reset all settings?"), 
                        translate("Options/MySettings", "Yes"), 
                        translate("Options/MySettings", "No (Cancel)"), 
                        translate("Options/MySettings", "Back Up And Reset"))
            if answer==translate("Options/MySettings", "Yes"):
                Settings.reFillAll()
            elif answer==translate("Options/MySettings", "Back Up And Reset"):
                Settings.reFillAll(True)
            self.parent().parent().reStart()
        except:
            error = ReportBug.ReportBug()
            error.show()
        
        
        
   
