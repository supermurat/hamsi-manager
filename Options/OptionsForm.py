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


import sys,os
from Core import Variables
from Core.MyObjects import *
from Core import Settings, Dialogs, Universals, Records
import InputOutputs
import Databases
from Options import OptionsFormContent
from Core import ReportBug

class OptionsForm(MDialog):
    
    def __init__(self, _parent=None, _showType="Normal", _focusTo = None, _markedKeys = []):
        MDialog.__init__(self, _parent)
        if isActivePyKDE4==True:
            self.setButtons(MDialog.NoDefault)
        self.showType = _showType
        self.focusTo = _focusTo
        self.focusToCategory = None
        self.markedKeys = _markedKeys
        self.defaultValues = Variables.getDefaultValues()
        self.checkVisibility(self.showType)
        if self.showType=="Normal":
            self.tboxCategories = MToolBox()
            pnlCategories = MHBoxLayout()
            pnlCategories.addWidget(self.tboxCategories, 1)
            self.setMinimumWidth(700)
            self.setMinimumHeight(520)
            self.show()
        elif len(self.categories)>1:
            pnlCategories = MTabWidget()
        else:
            pnlCategories = MVBoxLayout()
        for x, category in enumerate(self.categories):
            category.categoryNo = x
            if self.showType=="Normal":
                wCategory = MWidget()
                self.tboxCategories.addItem(wCategory, category.titleOfCategory)
                lblLabelOfCategory = MLabel(category.labelOfCategory, wCategory)
                lblLabelOfCategory.setWordWrap(True)
                lblLabelOfCategory.setFixedWidth(195)
                pnlCategories.addWidget(category, 20)
                if x!=0:
                    category.setVisible(False)
            elif len(self.categories)>1:
                pnlCategories.addTab(category, category.titleOfCategory)
            else:
                wCategory = MGroupBox(self)
                wCategory.setTitle(category.titleOfCategory)
                category.setParent(wCategory)
                hblTemp = MHBoxLayout(wCategory)
                hblTemp.addWidget(category)
                wCategory.setLayout(hblTemp)
                pnlCategories.addWidget(wCategory, 20)
        pnlMain = MWidget(self)
        vblMain = MVBoxLayout(pnlMain)
        if len(self.categories)==0:
            lblNotice = MLabel(translate("Options", "You have not any option."))
            vblMain.addWidget(lblNotice, 1)
        else:
            pbtnApply = MPushButton(translate("Options", "Apply"))
            MObject.connect(pbtnApply, SIGNAL("clicked()"), self.apply)
            hblButtons = MHBoxLayout()
            hblButtons.addStretch(20)
            hblButtons.addWidget(pbtnApply, 1)
            if self.showType=="Normal":
                pbtnSave = MPushButton(translate("Options", "Save"))
                pbtnCancel = MPushButton(translate("Options", "Cancel"))
                MObject.connect(self.tboxCategories, SIGNAL("currentChanged(int)"), self.tabChanged)
                MObject.connect(pbtnSave, SIGNAL("clicked()"), self.save)
                MObject.connect(pbtnCancel, SIGNAL("clicked()"), self.close)
                hblButtons.addWidget(pbtnSave, 1)
                hblButtons.addWidget(pbtnCancel, 1)
                self.tboxCategories.setFixedWidth(200)
                vblMain.addLayout(pnlCategories)
            elif len(self.categories)>1:
                self.setMinimumWidth(470)
                pbtnApply.setMinimumWidth(150)
                vblMain.addWidget(pnlCategories)
            else:
                self.setMinimumWidth(470)
                pbtnApply.setMinimumWidth(150)
                vblMain.addLayout(pnlCategories)
            vblMain.addLayout(hblButtons)
        if isActivePyKDE4==True:
            self.setMainWidget(pnlMain)
        else:
            self.setLayout(vblMain)
        self.setWindowTitle(translate("Options", "Options"))
        if self.showType=="Normal":
            if self.focusToCategory!=None:
                for x, category in enumerate(self.categories):
                    if self.focusToCategory==category:
                        self.tboxCategories.setCurrentIndex(x)
            self.show()
            self.setWindowIcon(MIcon("Images:options.png"))
            
    def checkVisibility(self, _showType):
        if _showType=="Normal":
            self.categories = [OptionsFormContent.General(self, _showType), 
                            OptionsFormContent.Appearance(self, _showType), 
                            OptionsFormContent.Correct(self, _showType), 
                            OptionsFormContent.SearchAndReplace(self, _showType), 
                            OptionsFormContent.ClearGeneral(self, _showType),
                            OptionsFormContent.Advanced(self, _showType), 
                            OptionsFormContent.Player(self, _showType), 
                            OptionsFormContent.Packager(self, _showType), 
                            OptionsFormContent.Cleaner(self, _showType), 
                            OptionsFormContent.HiddenObjects(self, _showType), 
                            OptionsFormContent.MySettings(self, _showType, [])]
            if Variables.isActiveAmarok:
                self.categories.insert(len(self.categories)-2, OptionsFormContent.Amarok(self, _showType))
            if Variables.isActiveDirectoryCover:
                self.categories.insert(5, OptionsFormContent.Cover(self, _showType))
        elif _showType=="pack":
            self.categories = [OptionsFormContent.General(self, _showType, ["isSaveActions"]), 
                            OptionsFormContent.ClearGeneral(self, _showType, ["isActiveClearGeneral", "isDeleteEmptyDirectories", 
                                "unneededDirectoriesIfIsEmpty", "unneededDirectories", 
                                "unneededFiles", "unneededFileExtensions", 
                                "ignoredDirectories", 
                                "ignoredFiles", "ignoredFileExtensions"]),
                            OptionsFormContent.Packager(self, _showType), 
                            OptionsFormContent.Advanced(self, _showType, ["isDontDeleteFileAndDirectory", "pathOfDeletedFilesAndDirectories"])]
        elif _showType=="checkIcon":
            self.categories = [OptionsFormContent.General(self, _showType, ["isSaveActions"]), 
                            OptionsFormContent.Correct(self, _showType), 
                            OptionsFormContent.SearchAndReplace(self, _showType)]
            if Variables.isActiveDirectoryCover:
                self.categories.insert(1, OptionsFormContent.Cover(self, _showType, ["priorityIconNames", "isChangeExistIcon"]))
        elif _showType=="clearEmptyDirectories":
            self.categories = [OptionsFormContent.General(self, _showType, ["isSaveActions"]), 
                            OptionsFormContent.ClearGeneral(self, _showType, ["isActiveClearGeneral", "isDeleteEmptyDirectories",
                                "unneededDirectoriesIfIsEmpty", "unneededDirectories", 
                                "unneededFiles", "unneededFileExtensions", 
                                "ignoredDirectories", 
                                "ignoredFiles", "ignoredFileExtensions"]), 
                            OptionsFormContent.Advanced(self, _showType, ["isDontDeleteFileAndDirectory", "pathOfDeletedFilesAndDirectories"])]
        elif _showType=="clearUnneededs":
            self.categories = [OptionsFormContent.General(self, _showType, ["isSaveActions"]), 
                            OptionsFormContent.ClearGeneral(self, _showType, ["isActiveClearGeneral", "isDeleteEmptyDirectories",
                                "unneededDirectoriesIfIsEmpty", "unneededDirectories", 
                                "unneededFiles", "unneededFileExtensions"]), 
                            OptionsFormContent.Advanced(self, _showType, ["isDontDeleteFileAndDirectory", "pathOfDeletedFilesAndDirectories"])]
        elif _showType=="clearIgnoreds":
            self.categories = [OptionsFormContent.General(self, _showType, ["isSaveActions"]), 
                            OptionsFormContent.ClearGeneral(self, _showType, ["isActiveClearGeneral", "isDeleteEmptyDirectories",
                                "ignoredDirectories", 
                                "ignoredFiles", "ignoredFileExtensions"]), 
                            OptionsFormContent.Advanced(self, _showType, ["isDontDeleteFileAndDirectory", "pathOfDeletedFilesAndDirectories"])]
        elif _showType=="emendFile":
            self.categories = [OptionsFormContent.General(self, _showType, ["isSaveActions"]), 
                            OptionsFormContent.Correct(self, _showType), 
                            OptionsFormContent.SearchAndReplace(self, _showType)]
            if Variables.isActiveDirectoryCover:
                self.categories.insert(1, OptionsFormContent.Cover(self, _showType, ["priorityIconNames", "isChangeExistIcon", 
                                "isAutoMakeIconToDirectoryWhenFileMove"]))
        elif _showType=="emendDirectory":
            self.categories = [OptionsFormContent.General(self, _showType, ["isSaveActions"]), 
                            OptionsFormContent.Correct(self, _showType),  
                            OptionsFormContent.ClearGeneral(self, _showType, ["isActiveClearGeneral", "isDeleteEmptyDirectories",
                                "unneededDirectoriesIfIsEmpty", "unneededDirectories", 
                                "unneededFiles", "unneededFileExtensions", 
                                "ignoredDirectories", 
                                "ignoredFiles", "ignoredFileExtensions", 
                                "isClearEmptyDirectoriesWhenMoveOrChange", "isAutoCleanSubFolderWhenMoveOrChange"]), 
                            OptionsFormContent.Advanced(self, _showType, ["isDontDeleteFileAndDirectory", "pathOfDeletedFilesAndDirectories"]), 
                            OptionsFormContent.SearchAndReplace(self, _showType)]
            if Variables.isActiveDirectoryCover:
                self.categories.insert(2, OptionsFormContent.Cover(self, _showType, ["priorityIconNames", "isChangeExistIcon", 
                                "isAutoMakeIconToDirectoryWhenMoveOrChange"]))
        elif _showType=="emendDirectoryWithContents":
            self.categories = [OptionsFormContent.General(self, _showType, ["isSaveActions"]), 
                            OptionsFormContent.Correct(self, _showType),  
                            OptionsFormContent.ClearGeneral(self, _showType, ["isActiveClearGeneral", "isDeleteEmptyDirectories",
                                "unneededDirectoriesIfIsEmpty", "unneededDirectories", 
                                "unneededFiles", "unneededFileExtensions", 
                                "ignoredDirectories", 
                                "ignoredFiles", "ignoredFileExtensions", 
                                "isClearEmptyDirectoriesWhenMoveOrChange", "isAutoCleanSubFolderWhenMoveOrChange"]), 
                            OptionsFormContent.Advanced(self, _showType, ["isDontDeleteFileAndDirectory", "pathOfDeletedFilesAndDirectories"]), 
                            OptionsFormContent.SearchAndReplace(self, _showType)]
            if Variables.isActiveDirectoryCover:
                self.categories.insert(2, OptionsFormContent.Cover(self, _showType, ["priorityIconNames", "isChangeExistIcon", 
                                "isAutoMakeIconToDirectoryWhenMoveOrChange", 
                                "isAutoMakeIconToDirectoryWhenFileMove"]))
        elif _showType=="fileTree":
            self.categories = [OptionsFormContent.General(self, _showType, ["isSaveActions"])]
        elif _showType=="removeOnlySubFiles":
            self.categories = [OptionsFormContent.General(self, _showType, ["isSaveActions"]), 
                            OptionsFormContent.Advanced(self, _showType, ["isDontDeleteFileAndDirectory", "pathOfDeletedFilesAndDirectories"])]
        elif _showType=="clear":
            self.categories = [OptionsFormContent.General(self, _showType, ["isSaveActions"]), 
                            OptionsFormContent.ClearGeneral(self, _showType, ["isActiveClearGeneral", "isDeleteEmptyDirectories",
                                "unneededDirectoriesIfIsEmpty", "unneededDirectories", 
                                "unneededFiles", "unneededFileExtensions", 
                                "ignoredDirectories", 
                                "ignoredFiles", "ignoredFileExtensions"]),
                            OptionsFormContent.Cleaner(self, _showType)]
        elif _showType=="hash":
            self.categories = [OptionsFormContent.General(self, _showType, ["isSaveActions"])]
        elif _showType=="textCorrector":
            self.categories = [OptionsFormContent.General(self, _showType, ["isSaveActions"]), 
                            OptionsFormContent.Correct(self, _showType, ["isEmendIncorrectChars", "isCorrectFileNameWithSearchAndReplaceTable", "isCorrectValueWithSearchAndReplaceTable", "isClearFirstAndLastSpaceChars"]), 
                            OptionsFormContent.SearchAndReplace(self, _showType)]
        else:
            self.categories = []
    
    def closeEvent(self, _event):
        MApplication.setStyle(Universals.MySettings["applicationStyle"])
    
    def save(self):
        if self.apply():
            self.close()
    
    def tabChanged(self, _tabNo):
        try:
            for category in self.categories:
                category.setVisible(False)
            self.categories[_tabNo].setVisible(True)
        except:
            ReportBug.ReportBug()

    def reStart(self):
        answer = Dialogs.ask(translate("Options", "Please Restart"), 
                    translate("Options", "In order to apply the changes you have to restart Hamsi Manager.<br>Do you want to restart now?"))
        if answer==Dialogs.Yes:
            self.close()
            if Universals.MainWindow.close():
                from Core.Execute import execute
                execute([], "HamsiManager")
    
    def setVisibleFormItems(self, _category, _keyOfSetting, _visible):
        if _category.visibleKeys.count(_keyOfSetting)>0 and _category.keysOfSettings.count(_keyOfSetting)>0:
            if _category.tabsOfSettings[_category.keysOfSettings.index(_keyOfSetting)]==None:
                flForm = _category.flForm
            else:
                flForm = _category.flForms[_category.tabsOfSettings[_category.keysOfSettings.index(_keyOfSetting)]]
            itemIndex = flForm.keysOfSettings.index(_keyOfSetting)*2
            flForm.itemAt(itemIndex).widget().setVisible(_visible)
            flForm.itemAt(itemIndex+1).layout().itemAt(0).widget().setVisible(_visible)
            try:
                flForm.itemAt(itemIndex+1).layout().itemAt(1).widget().setVisible(_visible)
                flForm.itemAt(itemIndex+1).layout().itemAt(2).widget().setVisible(_visible)
                flForm.itemAt(itemIndex+1).layout().itemAt(3).widget().setVisible(_visible)
            except:pass
    
    def isVisibleFormItems(self, _category, _keyOfSetting):
        if _category.visibleKeys.count(_keyOfSetting)>0 and _category.keysOfSettings.count(_keyOfSetting)>0:
            if _category.tabsOfSettings[_category.keysOfSettings.index(_keyOfSetting)]==None:
                flForm = _category.flForm
            else:
                flForm = _category.flForms[_category.tabsOfSettings[_category.keysOfSettings.index(_keyOfSetting)]]
            itemIndex = flForm.keysOfSettings.index(_keyOfSetting)*2
            return flForm.itemAt(itemIndex).widget().isVisible()
        return False
        
    def setEnabledFormItems(self, _category, _keyOfSetting, _visible):
        if _category.visibleKeys.count(_keyOfSetting)>0 and _category.keysOfSettings.count(_keyOfSetting)>0:
            if _category.tabsOfSettings[_category.keysOfSettings.index(_keyOfSetting)]==None:
                flForm = _category.flForm
            else:
                flForm = _category.flForms[_category.tabsOfSettings[_category.keysOfSettings.index(_keyOfSetting)]]
            itemIndex = flForm.keysOfSettings.index(_keyOfSetting)*2
            flForm.itemAt(itemIndex).widget().setEnabled(_visible)
            flForm.itemAt(itemIndex+1).layout().itemAt(0).widget().setEnabled(_visible)
            try:
                flForm.itemAt(itemIndex+1).layout().itemAt(1).widget().setEnabled(_visible)
                flForm.itemAt(itemIndex+1).layout().itemAt(2).widget().setEnabled(_visible)
                flForm.itemAt(itemIndex+1).layout().itemAt(3).widget().setEnabled(_visible)
            except:pass
    
    def isEnabledFormItems(self, _category, _keyOfSetting):
        if _category.visibleKeys.count(_keyOfSetting)>0 and _category.keysOfSettings.count(_keyOfSetting)>0:
            if _category.tabsOfSettings[_category.keysOfSettings.index(_keyOfSetting)]==None:
                flForm = _category.flForm
            else:
                flForm = _category.flForms[_category.tabsOfSettings[_category.keysOfSettings.index(_keyOfSetting)]]
            itemIndex = flForm.keysOfSettings.index(_keyOfSetting)*2
            return flForm.itemAt(itemIndex).widget().isEnabled()
        return False
        
    def pbtnFileClicked(self):
        requestInfos = str(self.sender().objectName()).split("_")
        leValue = self.categories[self.tboxCategories.currentIndex()].values[int(requestInfos[2])]
        if requestInfos[0]=="file":
            if requestInfos[1]=="image":
                directory = InputOutputs.getRealDirName(leValue.text())
                filePath = Dialogs.getOpenFileName(translate("Options", "Choose Image"),
                                            directory, str(translate("Options", "Images")) + " " + Variables.imageExtStringOnlyPNGAndJPG, 0)
                if filePath is not None:
                    leValue.setText(trForUI(filePath))   
            if requestInfos[1]=="executable":
                directory = InputOutputs.getRealDirName(leValue.text())
                filePath = Dialogs.getOpenFileName(translate("Options", "Choose Executable File"),
                                            directory, translate("Options", "Executable Files") + " (*)", 0)
                if filePath is not None:
                    leValue.setText(trForUI(filePath))  
                    
    def pbtnDirectoryClicked(self):
        requestInfos = str(self.sender().objectName()).split("_")
        leValue = self.categories[self.tboxCategories.currentIndex()].values[int(requestInfos[2])]
        if requestInfos[0]=="directory":  
            if requestInfos[1]=="exist":
                directory = InputOutputs.getRealPath(leValue.text())
                dirPath = Dialogs.getExistingDirectory(self,translate("Options", "Choose Image"),
                                                directory, 0)
                if dirPath is not None:
                    leValue.setText(trForUI(dirPath))
                
    def pbtnDefaultValueClicked(self):
        requestInfos = str(self.sender().objectName()).split("_")
        categoryNo = self.tboxCategories.currentIndex()
        typeOfValue = requestInfos[0]
        keyValue = requestInfos[1]
        keyNo = int(requestInfos[2])
        leValue = self.categories[categoryNo].values[keyNo]
        if typeOfValue=="string":
            self.categories[categoryNo].values[keyNo].setText(trForUI(self.defaultValues[keyValue]))
        elif typeOfValue=="richtext":
            self.categories[categoryNo].values[keyNo].setPlainText(trForUI(self.defaultValues[keyValue]))
        elif typeOfValue=="list":
            value = ""
            for y, info in enumerate(Universals.getListFromListString(self.defaultValues[keyValue])):
                if y!=0:
                    value += ";"
                value += str(info)
            self.categories[categoryNo].values[keyNo].setText(trForUI(value))
        elif typeOfValue=="trString":
            value = self.defaultValues[keyValue]
            for y, info in enumerate(self.categories[categoryNo].stringSearchList[self.categories[categoryNo].typesOfValues[keyNo][1]]):
                value = value.replace(str(info), str(self.categories[categoryNo].stringReplaceList[self.categories[categoryNo].typesOfValues[keyNo][1]][y]))
            self.categories[categoryNo].values[keyNo].setText(trForUI(value))
        elif typeOfValue=="options":
            self.categories[categoryNo].values[keyNo].setCurrentIndex(self.categories[categoryNo].valuesOfOptionsKeys[self.categories[categoryNo].typesOfValues[keyNo][1]].index(self.defaultValues[keyValue]))
        elif typeOfValue=="number":
            self.categories[categoryNo].values[keyNo].setValue(int(self.defaultValues[keyValue])) 
        elif typeOfValue=="Yes/No":
            if eval(self.defaultValues[keyValue].title())==True:
                self.categories[categoryNo].values[keyNo].setCurrentIndex(1)
            else:
                self.categories[categoryNo].values[keyNo].setCurrentIndex(0)
        elif typeOfValue=="file":
            self.categories[categoryNo].values[keyNo].setText(self.defaultValues[keyValue])
        elif typeOfValue=="directory":
            self.categories[categoryNo].values[keyNo].setText(self.defaultValues[keyValue])
    
    def createDefaultValueButton(self, _category, _typeOfValue, _keyValue, x):
        pbtnDefaultValue = MPushButton(translate("Options", "?"))
        pbtnDefaultValue.setObjectName(_typeOfValue + "_"+_keyValue+"_"+str(x))
        toolTips = str(translate("Options", "Default Value : "))
        if _typeOfValue=="string":
            toolTips += self.defaultValues[_keyValue]
        elif _typeOfValue=="richtext":
            toolTips += self.defaultValues[_keyValue]
        elif _typeOfValue=="list":
            for y, info in enumerate(Universals.getListFromListString(self.defaultValues[_keyValue])):
                if y!=0:
                    toolTips += ";"
                toolTips += str(info)
        elif _typeOfValue=="trString":
            value = self.defaultValues[_keyValue]
            for y, info in enumerate(_category.stringSearchList[_category.typesOfValues[x][1]]):
                value = value.replace(str(info), str(_category.stringReplaceList[_category.typesOfValues[x][1]][y]))
            toolTips += value
        elif _typeOfValue=="options":
            toolTips += str(_category.valuesOfOptions[_category.typesOfValues[x][1]][_category.valuesOfOptionsKeys[_category.typesOfValues[x][1]].index(self.defaultValues[_keyValue])])
        elif _typeOfValue=="number":
            toolTips += self.defaultValues[_keyValue]
        elif _typeOfValue=="Yes/No":
            if eval(self.defaultValues[_keyValue].title())==True:
                toolTips += str(translate("Dialogs", "Yes"))
            else:
                toolTips += str(translate("Dialogs", "No"))
        elif _typeOfValue=="file":
            toolTips += self.defaultValues[_keyValue]
        elif _typeOfValue=="directory":
            toolTips += self.defaultValues[_keyValue]
        pbtnDefaultValue.setToolTip(trForUI(toolTips))
        pbtnDefaultValue.setFixedWidth(25)
        MObject.connect(pbtnDefaultValue, SIGNAL("clicked()"), _category.parent().pbtnDefaultValueClicked)
        return pbtnDefaultValue
    
    def pbtnEditValueClicked(self):
        ed = EditDialog(self, self.sender())
    
    def createEditValueButton(self, _category, _typeOfValue, _keyValue, x):
        pbtnEditValue = MPushButton(translate("Options", "*"))
        pbtnEditValue.setObjectName(_typeOfValue + "_"+_keyValue+"_"+str(x))
        pbtnEditValue.setToolTip(translate("Options", "Edit values with Advanced Value Editor"))
        pbtnEditValue.setFixedWidth(25)
        MObject.connect(pbtnEditValue, SIGNAL("clicked()"), _category.parent().pbtnEditValueClicked)
        return pbtnEditValue
    
    def apply(self):
        try:
            isNeededRestart = False
            isDontClose = False
            isSaveSearchAndReplaceTable, searchAndReplaceCategoryNo = False, 0
            defaultValues = Variables.getDefaultValues()
            valueTypesAndValues = Variables.getValueTypesAndValues(True)
            for categoryNo, category in enumerate(self.categories):
                for x, keyValue in enumerate(category.keysOfSettings):
                    if category.visibleKeys.count(keyValue)>0:
                        if category.typesOfValues[x]=="string":
                            value = str(category.values[x].text())
                        elif category.typesOfValues[x]=="richtext":
                            value = str(category.values[x].toPlainText())
                        elif category.typesOfValues[x]=="list":
                            value = "['"
                            for y, bilgi in enumerate(str(category.values[x].text()).split(";")):
                                if y!=0:
                                    value += "','"
                                value += bilgi
                            value+="']"
                        elif category.typesOfValues[x][0]=="trString":
                            value = str(category.values[x].text())
                            for y, info in enumerate(category.stringReplaceList[category.typesOfValues[x][1]]):
                                value = value.replace(str(info), str(category.stringSearchList[category.typesOfValues[x][1]][y]))
                        elif category.typesOfValues[x][0]=="options":
                            value = category.valuesOfOptionsKeys[category.typesOfValues[x][1]][category.values[x].currentIndex()]
                        elif category.typesOfValues[x][0]=="number":
                            value = str(category.values[x].value())
                        elif category.typesOfValues[x]=="Yes/No":
                            if category.values[x].currentIndex()==0:
                                value = "False"
                            else:
                                value = "True"
                        elif category.typesOfValues[x][0]=="file":
                            value = str(category.values[x].text())
                        elif category.typesOfValues[x][0]=="directory":
                            value = str(category.values[x].text())
                        elif category.typesOfValues[x]=="password":
                            value = str(category.values[x].text())
                        category.values[x].setStyleSheet("")
                        if Universals.MySettings[keyValue]!=value:
                            emendedValue = Settings.emendValue(keyValue, value, defaultValues[keyValue], valueTypesAndValues[keyValue])
                            if emendedValue != value:
                                answer = Dialogs.ask(translate("Options", "Incorrect Value"), 
                                                     str(translate("Options", "\"%s\" been set incorrectly.Are you want to set it automatically emend?")) % (str(category.labels[x])))
                                if answer==Dialogs.Yes:
                                    Universals.setMySetting(keyValue, emendedValue)
                                    if category.typesOfValues[x]=="string":
                                        category.values[x].setText(trForUI(emendedValue))
                                    elif category.typesOfValues[x]=="list":
                                        value = ""
                                        for y, info in enumerate(Universals.getListFromListString(emendedValue)):
                                            if y!=0:
                                                value += ";"
                                            value += str(info)
                                        category.values[x].setText(trForUI(value))
                                else:
                                    if self.showType=="Normal":
                                        self.tboxCategories.setCurrentIndex(categoryNo)
                                        if category.tabsOfSettings[x]!=None:
                                            category.tabwTabs.setCurrentIndex(category.tabsOfSettings[x])
                                    category.values[x].setStyleSheet("background-color: #FF5E5E;")
                                    isDontClose = True
                            else:
                                Universals.setMySetting(keyValue, value) 
                            if category.neededRestartSettingKeys.count(keyValue)>0:
                                isNeededRestart = True
                if str(category).find("SearchAndReplace")!=-1:
                    isSaveSearchAndReplaceTable = True
                    searchAndReplaceCategoryNo = categoryNo
            Universals.saveSettings()
            if isSaveSearchAndReplaceTable:
                self.categories[searchAndReplaceCategoryNo].searchAndReplaceTable.save()
            if Universals.MainWindow.Menu!=None:
                Universals.MainWindow.Menu.refreshQuickOptions()
            Records.checkSize()
            if isDontClose:return False
            if isNeededRestart==True:
                self.reStart()
            else:return True
        except:
            ReportBug.ReportBug()
            
    def applySetting(self, _category, _keyValue):
        try:
            defaultValues = Variables.getDefaultValues()
            valueTypesAndValues = Variables.getValueTypesAndValues(True)
            x = _category.keysOfSettings.index(_keyValue)
            if _category.visibleKeys.count(_keyValue)>0:
                if _category.typesOfValues[x]=="string":
                    value = str(_category.values[x].text())
                elif _category.typesOfValues[x]=="richtext":
                    value = str(_category.values[x].toPlainText())
                elif _category.typesOfValues[x]=="list":
                    value = "['"
                    for y, bilgi in enumerate(str(_category.values[x].text()).split(";")):
                        if y!=0:
                            value += "','"
                        value += bilgi
                    value+="']"
                elif _category.typesOfValues[x][0]=="trString":
                    value = str(_category.values[x].text())
                    for y, info in enumerate(_category.stringReplaceList[_category.typesOfValues[x][1]]):
                        value = value.replace(str(info), str(_category.stringSearchList[_category.typesOfValues[x][1]][y]))
                elif _category.typesOfValues[x][0]=="options":
                    value = _category.valuesOfOptionsKeys[_category.typesOfValues[x][1]][_category.values[x].currentIndex()]
                elif _category.typesOfValues[x][0]=="number":
                    value = str(_category.values[x].value())
                elif _category.typesOfValues[x]=="Yes/No":
                    if _category.values[x].currentIndex()==0:
                        value = "False"
                    else:
                        value = "True"
                elif _category.typesOfValues[x][0]=="file":
                    value = str(_category.values[x].text())
                elif _category.typesOfValues[x][0]=="directory":
                    value = str(_category.values[x].text())
                elif _category.typesOfValues[x]=="password":
                    value = str(_category.values[x].text())
                _category.values[x].setStyleSheet("")
                if Universals.MySettings[_keyValue]!=value:
                    emendedValue = Settings.emendValue(_keyValue, value, defaultValues[_keyValue], valueTypesAndValues[_keyValue])
                    if emendedValue != value:
                        answer = Dialogs.ask(translate("Options", "Incorrect Value"), 
                                             str(translate("Options", "\"%s\" been set incorrectly.Are you want to set it automatically emend?")) % (str(_category.labels[x])))
                        if answer==Dialogs.Yes:
                            Universals.setMySetting(_keyValue, emendedValue)
                            if _category.typesOfValues[x]=="string":
                                _category.values[x].setText(trForUI(emendedValue))
                            elif _category.typesOfValues[x]=="list":
                                value = ""
                                for y, info in enumerate(Universals.getListFromListString(emendedValue)):
                                    if y!=0:
                                        value += ";"
                                    value += str(info)
                                _category.values[x].setText(trForUI(value))
                        else:
                            if self.showType=="Normal":
                                self.tboxCategories.setCurrentIndex(_category.categoryNo)
                                _category.tabwTabs.setCurrentIndex(_category.tabsOfSettings[x])
                            _category.values[x].setStyleSheet("background-color: #FF5E5E;")
                            isDontClose = True
                    else:
                        Universals.setMySetting(_keyValue, value) 
        except:
            ReportBug.ReportBug()
            
    def createOptions(self, _category):
        self.correctSettingKeys(_category)
        isNeededRestart = False
        _category.flForm = MyFormLayout()
        _category.flForms = []
        if len(_category.tabNames)>0:
            _category.tabwTabs = MTabWidget()
        for x, name in enumerate(_category.tabNames):
            wCategory = MWidget()
            _category.flForms.append(MyFormLayout())
            wCategory.setLayout(_category.flForms[x])
            _category.tabwTabs.addTab(wCategory, _category.tabNames[x])
        for x, keyValue in enumerate(_category.keysOfSettings):
            if _category.visibleKeys.count(keyValue)>0:
                valueLayout = MHBoxLayout()
                typeOfValue = "string"
                if _category.neededRestartSettingKeys.count(keyValue)>0:
                    _category.labels[x] = _category.labels[x]+" <font color=red>*</font> "
                    isNeededRestart = True
                if _category.typesOfValues[x]=="string":
                    _category.values.append(MLineEdit())
                    _category.values[x].setText(trForUI(Universals.MySettings[keyValue]))
                elif _category.typesOfValues[x]=="richtext":
                    typeOfValue = "richtext"
                    _category.values.append(MTextEdit())
                    _category.values[x].setPlainText(trForUI(Universals.MySettings[keyValue]))
                elif _category.typesOfValues[x]=="list":
                    typeOfValue = "list"
                    _category.values.append(MLineEdit())
                    value = ""
                    for y, info in enumerate(Universals.getListValue(keyValue)):
                        if y!=0:
                            value += ";"
                        value += str(info)
                    _category.values[x].setText(trForUI(value))
                elif _category.typesOfValues[x][0]=="trString":
                    typeOfValue = "trString"
                    _category.values.append(MLineEdit())
                    value = Universals.MySettings[keyValue]
                    for y, info in enumerate(_category.stringSearchList[_category.typesOfValues[x][1]]):
                        value = value.replace(str(info), str(_category.stringReplaceList[_category.typesOfValues[x][1]][y]))
                    _category.values[x].setText(trForUI(value))
                elif _category.typesOfValues[x][0]=="options":
                    typeOfValue = "options"
                    _category.values.append(MComboBox())
                    for info in _category.valuesOfOptions[_category.typesOfValues[x][1]]:
                        _category.values[x].addItem(info)
                    try:_category.values[x].setCurrentIndex(_category.valuesOfOptionsKeys[_category.typesOfValues[x][1]].index(Universals.MySettings[keyValue]))
                    except:pass#pass for unknown values
                elif _category.typesOfValues[x][0]=="number":
                    typeOfValue = "number"
                    _category.values.append(MSpinBox())
                    _category.values[x].setRange(int(_category.valuesOfOptions[_category.typesOfValues[x][1]][0]), int(_category.valuesOfOptions[_category.typesOfValues[x][1]][1]))
                    try:_category.values[x].setValue(int(Universals.MySettings[keyValue])) 
                    except:pass#pass for unknown values
                elif _category.typesOfValues[x]=="Yes/No":
                    typeOfValue = "Yes/No"
                    _category.values.append(MComboBox())
                    _category.values[x].addItems([translate("Dialogs", "No"),translate("Dialogs", "Yes")])
                    if Universals.getBoolValue(keyValue):
                        _category.values[x].setCurrentIndex(1)
                elif _category.typesOfValues[x][0]=="file":
                    typeOfValue = "file"
                    _category.values.append(MLineEdit())
                    _category.values[x].setText(Universals.MySettings[keyValue])
                    pbtnFile = MPushButton(translate("Options", "...."))
                    pbtnFile.setObjectName("file_"+_category.typesOfValues[x][1]+"_"+str(x))
                    pbtnFile.setToolTip(_category.toolTips[x])
                    MObject.connect(pbtnFile, SIGNAL("clicked()"), _category.parent().pbtnFileClicked)
                    valueLayout.addWidget(pbtnFile)
                elif _category.typesOfValues[x][0]=="directory":
                    typeOfValue = "directory"
                    _category.values.append(MLineEdit())
                    _category.values[x].setText(Universals.MySettings[keyValue])
                    pbtnDirectory = MPushButton(translate("Options", "...."))
                    pbtnDirectory.setObjectName("directory_"+_category.typesOfValues[x][1]+"_"+str(x))
                    pbtnDirectory.setToolTip(_category.toolTips[x])
                    MObject.connect(pbtnDirectory, SIGNAL("clicked()"), _category.parent().pbtnDirectoryClicked)
                    valueLayout.addWidget(pbtnDirectory)
                if _category.typesOfValues[x]=="password":
                    _category.values.append(MLineEdit())
                    _category.values[x].setText(trForUI(Universals.MySettings[keyValue]))
                    _category.values[x].setEchoMode(MLineEdit.Password)
                if typeOfValue=="list":
                    pbtnEditValue = _category.parent().createEditValueButton(_category, typeOfValue, keyValue, x)
                    valueLayout.addWidget(pbtnEditValue)
                pbtnDefaultValue = _category.parent().createDefaultValueButton(_category, typeOfValue, keyValue, x)
                valueLayout.addWidget(pbtnDefaultValue)
                valueLayout.insertWidget(0, _category.values[x])
                _category.values[x].setToolTip(_category.toolTips[x])
                lblLabel = MLabel(trForUI(_category.labels[x]+" : "))
                lblLabel.setToolTip(_category.toolTips[x])
                _category.lblLabels.append(lblLabel)
                if _category.tabsOfSettings[x]==None:
                    _category.flForm.addRow(_category.lblLabels[x], valueLayout)
                    _category.flForm.keysOfSettings.append(keyValue)
                else:
                    _category.flForms[_category.tabsOfSettings[x]].addRow(_category.lblLabels[x], valueLayout)
                    _category.flForms[_category.tabsOfSettings[x]].keysOfSettings.append(keyValue)
                if keyValue == _category.parent().focusTo:
                    _category.parent().focusToCategory = _category
                    _category.values[x].setStyleSheet("background-color: #4D9AFF;")
                if _category.parent().markedKeys.count(keyValue)>0:
                    if _category.parent().focusToCategory==None:
                        _category.parent().focusToCategory = _category
                    _category.values[x].setStyleSheet("background-color: #81DEFF;")
            else:
                _category.values.append(None)
                _category.lblLabels.append(None)
        _category.Panel.addStretch(1)
        for x, flForm in enumerate([_category.flForm] + _category.flForms):
            flForm.setRowWrapPolicy(MFormLayout.DontWrapRows)
            flForm.setFieldGrowthPolicy(MFormLayout.AllNonFixedFieldsGrow)
            flForm.setFormAlignment(Mt.AlignHCenter | Mt.AlignTop)
            flForm.setLabelAlignment(Mt.AlignLeft)
            if len(flForm.keysOfSettings)==0:
                _category.tabwTabs.removeTab(x-1)
        _category.Panel.insertLayout(1, _category.flForm) 
        _category.Panel.addStretch(1)
        if len(_category.tabNames)>0:
            _category.Panel.insertWidget(3, _category.tabwTabs) 
        _category.Panel.addStretch(1)
        if isNeededRestart==True:
            _category.Panel.addWidget(MLabel(translate("Options", "<font color=red>* :Requires a restart of Hamsi Manager.</font>"))) 
            
    def correctSettingKeys(self, _category):
        if len(_category.visibleKeys)!=len(_category.keysOfSettings):
            keysOfSettings, labels, toolTips, typesOfValues = [], [], [], []
            for x, keyName in enumerate(_category.keysOfSettings):
                if _category.visibleKeys.count(keyName)>0:
                    keysOfSettings.append(_category.keysOfSettings[x])
                    labels.append(_category.labels[x])
                    toolTips.append(_category.toolTips[x])
                    typesOfValues.append(_category.typesOfValues[x])
            _category.keysOfSettings = keysOfSettings
            _category.labels = labels
            _category.toolTips = toolTips
            _category.typesOfValues = typesOfValues
       
class EditDialog(MDialog):
    
    def __init__(self, _parent, _sender):
        MDialog.__init__(self, _parent)
        if isActivePyKDE4==True:
            self.setButtons(MDialog.NoDefault)
        self.setWindowTitle(translate("EditDialog", "Advanced Value Editor"))
        self.requestInfos = str(_sender.objectName()).split("_")
        self.categoryNo = self.parent().tboxCategories.currentIndex()
        self.typeOfValue = self.requestInfos[0]
        self.keyValue = self.requestInfos[1]
        self.keyNo = int(self.requestInfos[2])
        if self.typeOfValue=="string":
            #This Is Not Used (For only future)
            currentValue = str(self.parent().categories[self.categoryNo].values[self.keyNo].text())
            self.EditorWidget = MTextEdit(self)
            self.EditorWidget.setText(trForUI(currentValue))
        elif self.typeOfValue=="richtext":
            #This Is Not Used (For only future)
            currentValue = str(self.parent().categories[self.categoryNo].values[self.keyNo].plainText())
            self.EditorWidget = MTextEdit(self)
            self.EditorWidget.setAcceptRichText(True)
            self.EditorWidget.setPlainText(trForUI(currentValue))
        elif self.typeOfValue=="list":
            currentValue = str(self.parent().categories[self.categoryNo].values[self.keyNo].text())
            if isActivePyKDE4==True:
                self.EditorWidget = MEditListBox(self)
                self.EditorWidget.setItems([trForUI(x) for x in currentValue.split(";")])
            else:
                self.EditorWidget = MTextEdit(self)
                self.EditorWidget.setText(trForUI(currentValue.replace(";", "\n")))
        elif self.typeOfValue=="options":
            #This Is Not Used (For only future)
            currentValue = str(self.parent().categories[self.categoryNo].values[self.keyNo].currentIndex())
        elif self.typeOfValue=="number":
            #This Is Not Used (For only future)
            currentValue = str(self.parent().categories[self.categoryNo].values[self.keyNo].value())
        elif self.typeOfValue=="Yes/No":
            #This Is Not Used (For only future)
            if self.parent().categories[self.categoryNo].values[self.keyNo].currentIndex()==1:
                currentValue = True
            else:
                currentValue = False
        elif self.typeOfValue=="file":
            #This Is Not Used (For only future)
            currentValue = str(self.parent().categories[self.categoryNo].values[self.keyNo].text())
        pnlMain = MWidget(self)
        vblMain = MVBoxLayout(pnlMain)
        pbtnCancel = MPushButton(translate("EditDialog", "Cancel"))
        pbtnApply = MPushButton(translate("EditDialog", "Apply"))
        MObject.connect(pbtnCancel, SIGNAL("clicked()"), self.close)
        MObject.connect(pbtnApply, SIGNAL("clicked()"), self.apply)
        vblMain.addWidget(self.EditorWidget)
        hblBox = MHBoxLayout()
        hblBox.addWidget(pbtnApply)
        hblBox.addWidget(pbtnCancel)
        vblMain.addLayout(hblBox)
        if isActivePyKDE4==True:
            self.setMainWidget(pnlMain)
        else:
            self.setLayout(vblMain)
        self.setMinimumSize(550, 400)
        self.show()
        
    def apply(self):
        if self.typeOfValue=="string":
            #This Is Not Used (For only future)
            newValue = "" #NotUsed
            self.parent().categories[self.categoryNo].values[self.keyNo].setText(trForUI(newValue))
        elif self.typeOfValue=="richtext":
            #This Is Not Used (For only future)
            newValue = "" #NotUsed
            self.parent().categories[self.categoryNo].values[self.keyNo].setPlainText(trForUI(newValue))
        elif self.typeOfValue=="list":
            value = ""
            if isActivePyKDE4==True:
                for y, info in enumerate(self.EditorWidget.items()):
                    if y!=0:
                        value += ";"
                    value += str(info)
            else:
                value = str(self.EditorWidget.toPlainText()).replace("\n", ";")
            self.parent().categories[self.categoryNo].values[self.keyNo].setText(trForUI(value))
        elif self.typeOfValue=="options":
            #This Is Not Used (For only future)
            newValue = "" #NotUsed
            self.parent().categories[self.categoryNo].values[self.keyNo].setCurrentIndex(self.parent().categories[self.categoryNo].valuesOfOptionsKeys[self.parent().categories[self.categoryNo].typesOfValues[self.keyNo][1]].index(newValue))
        elif self.typeOfValue=="number":
            #This Is Not Used (For only future)
            newValue = "" #NotUsed
            self.parent().categories[self.categoryNo].values[self.keyNo].setValue(int(newValue)) 
        elif self.typeOfValue=="Yes/No":
            #This Is Not Used (For only future)
            newValue = "" #NotUsed
            if eval(newValue.title())==True:
                self.parent().categories[self.categoryNo].values[self.keyNo].setCurrentIndex(1)
            else:
                self.parent().categories[self.categoryNo].values[self.keyNo].setCurrentIndex(0)
        elif self.typeOfValue=="file":
            #This Is Not Used (For only future)
            newValue = "" #NotUsed
            self.parent().categories[self.categoryNo].values[self.keyNo].setText(newValue)
        self.close()
        
class MyFormLayout(MFormLayout):
    
    def __init__(self):
        MFormLayout.__init__(self, None)
        self.keysOfSettings = []
      
