# -*- coding: utf-8 -*-

import sys,os
import Variables
from MyObjects import *
import Settings, Dialogs , Universals, InputOutputs, Records, Organizer
import ReportBug

class Options(MDialog):
    global createOptions, setVisibleFormItems, isVisibleFormItems, setEnabledFormItems, isEnabledFormItems, correctSettingKeys, applySetting
    
    def __init__(self, _parent=None, _showType="Normal", _focusTo = None, _markedKeys = []):
        MDialog.__init__(self, _parent)
        if Universals.isActivePyKDE4==True:
            self.setButtons(MDialog.None)
        self.showType = _showType
        self.focusTo = _focusTo
        self.focusToCategory = None
        self.markedKeys = _markedKeys
        self.defaultValues = Settings.getDefaultValues()
        self.checkVisibility(self.showType)
        if self.showType=="Normal":
            self.tboxCategories = MToolBox()
            pnlCategories = MHBoxLayout()
            pnlCategories.addWidget(self.tboxCategories, 1)
            self.setMinimumWidth(700)
            self.setMinimumHeight(450)
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
        if Universals.isActivePyKDE4==True:
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
            self.categories = [General(self, _showType), 
                            Correct(self, _showType), 
                            SearchAndReplace(self, _showType), 
                            ClearGeneral(self, _showType),
                            Cover(self, _showType),
                            Advanced(self, _showType), 
                            Player(self, _showType), 
                            Packager(self, _showType), 
                            Cleaner(self, _showType), 
                            Amarok(self, _showType), 
                            MySettings(self, _showType, [])]
        elif _showType=="pack":
            self.categories = [General(self, _showType, ["isSaveActions"]), 
                            ClearGeneral(self, _showType, ["isDeleteEmptyDirectories", 
                                "unneededDirectoriesIfIsEmpty", "unneededDirectories", 
                                "unneededFiles", "unneededFileExtensions", 
                                "ignoredDirectories", 
                                "ignoredFiles", "ignoredFileExtensions"]),
                            Packager(self, _showType)]
        elif _showType=="checkIcon":
            self.categories = [General(self, _showType, ["isSaveActions"]), 
                            Cover(self, _showType, ["priorityIconNames", "isChangeExistIcon"]), 
                            Correct(self, _showType)]
        elif _showType=="clearEmptyDirectories":
            self.categories = [General(self, _showType, ["isSaveActions"]), 
                            ClearGeneral(self, _showType, ["isDeleteEmptyDirectories",
                                "unneededDirectoriesIfIsEmpty", "unneededDirectories", 
                                "unneededFiles", "unneededFileExtensions", 
                                "ignoredDirectories", 
                                "ignoredFiles", "ignoredFileExtensions"])]
        elif _showType=="clearUnneededs":
            self.categories = [General(self, _showType, ["isSaveActions"]), 
                            ClearGeneral(self, _showType, ["isDeleteEmptyDirectories",
                                "unneededDirectoriesIfIsEmpty", "unneededDirectories", 
                                "unneededFiles", "unneededFileExtensions"])]
        elif _showType=="clearIgnoreds":
            self.categories = [General(self, _showType, ["isSaveActions"]), 
                            ClearGeneral(self, _showType, ["isDeleteEmptyDirectories",
                                "ignoredDirectories", 
                                "ignoredFiles", "ignoredFileExtensions"])]
        elif _showType=="emendFile":
            self.categories = [General(self, _showType, ["isSaveActions"]), 
                            Cover(self, _showType, ["priorityIconNames", "isChangeExistIcon", 
                                "isAutoMakeIconToDirectoryWhenFileMove"]), 
                            Correct(self, _showType)]
        elif _showType=="emendDirectory":
            self.categories = [General(self, _showType, ["priorityIconNames", "isSaveActions"]), 
                            Correct(self, _showType),  
                            Cover(self, _showType, ["priorityIconNames", "isChangeExistIcon", 
                                "isAutoMakeIconToDirectoryWhenMoveOrChange"]), 
                            ClearGeneral(self, _showType, ["isDeleteEmptyDirectories",
                                "unneededDirectoriesIfIsEmpty", "unneededDirectories", 
                                "unneededFiles", "unneededFileExtensions", 
                                "ignoredDirectories", 
                                "ignoredFiles", "ignoredFileExtensions", 
                                "isClearEmptyDirectoriesWhenMoveOrChange", "isAutoCleanSubFolderWhenMoveOrChange"])]
        elif _showType=="emendDirectoryWithContents":
            self.categories = [General(self, _showType, ["priorityIconNames", "isSaveActions"]), 
                            Correct(self, _showType),  
                            Cover(self, _showType, ["priorityIconNames", "isChangeExistIcon", 
                                "isAutoMakeIconToDirectoryWhenMoveOrChange", 
                                "isAutoMakeIconToDirectoryWhenFileMove"]), 
                            ClearGeneral(self, _showType, ["isDeleteEmptyDirectories",
                                "unneededDirectoriesIfIsEmpty", "unneededDirectories", 
                                "unneededFiles", "unneededFileExtensions", 
                                "ignoredDirectories", 
                                "ignoredFiles", "ignoredFileExtensions", 
                                "isClearEmptyDirectoriesWhenMoveOrChange", "isAutoCleanSubFolderWhenMoveOrChange"])]
        elif _showType=="fileTree":
            self.categories = [General(self, _showType, ["isSaveActions"])]
        elif _showType=="removeOnlySubFiles":
            self.categories = [General(self, _showType, ["isSaveActions"])]
        elif _showType=="clear":
            self.categories = [General(self, _showType, ["isSaveActions"]), 
                            ClearGeneral(self, _showType, ["isDeleteEmptyDirectories",
                                "unneededDirectoriesIfIsEmpty", "unneededDirectories", 
                                "unneededFiles", "unneededFileExtensions", 
                                "ignoredDirectories", 
                                "ignoredFiles", "ignoredFileExtensions"]),
                            Cleaner(self, _showType)]
        elif _showType=="hash":
            self.categories = [General(self, _showType, ["isSaveActions"])]
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
            error = ReportBug.ReportBug()
            error.show()

    def reStart(self):
        answer = Dialogs.ask(translate("Options", "Please Restart"), 
                    translate("Options", "In order to apply the changes you have to restart Hamsi Manager.<br>Do you want to restart now?"))
        if answer==Dialogs.Yes:
            self.close()
            if Universals.MainWindow.close():
                from Execute import executeHamsiManager
                executeHamsiManager()
    
    def setVisibleFormItems(_category, _keyOfSetting, _visible):
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
    
    def isVisibleFormItems(_category, _keyOfSetting):
        if _category.visibleKeys.count(_keyOfSetting)>0 and _category.keysOfSettings.count(_keyOfSetting)>0:
            if _category.tabsOfSettings[_category.keysOfSettings.index(_keyOfSetting)]==None:
                flForm = _category.flForm
            else:
                flForm = _category.flForms[_category.tabsOfSettings[_category.keysOfSettings.index(_keyOfSetting)]]
            itemIndex = flForm.keysOfSettings.index(_keyOfSetting)*2
            return flForm.itemAt(itemIndex).widget().isVisible()
        return False
        
    def setEnabledFormItems(_category, _keyOfSetting, _visible):
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
    
    def isEnabledFormItems(_category, _keyOfSetting):
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
                filePath = MFileDialog.getOpenFileName(self,translate("Options", "Choose Image"),
                                            directory,(str(translate("Options", "Images")) + " " + Universals.imageExtStringOnlyPNGAndJPG).decode("utf-8"))
                if filePath!="":
                    leValue.setText(filePath)   
            if requestInfos[1]=="executable":
                directory = InputOutputs.getRealDirName(leValue.text())
                filePath = MFileDialog.getOpenFileName(self,translate("Options", "Choose Executable File"),
                                            directory,translate("Options", "Executable Files") + u" (*)")
                if filePath!="":
                    leValue.setText(filePath)     
            
    def pbtnDefaultValueClicked(self):
        requestInfos = str(self.sender().objectName()).split("_")
        categoryNo = self.tboxCategories.currentIndex()
        typeOfValue = requestInfos[0]
        keyValue = requestInfos[1]
        keyNo = int(requestInfos[2])
        leValue = self.categories[categoryNo].values[keyNo]
        if typeOfValue=="string":
            self.categories[categoryNo].values[keyNo].setText(self.defaultValues[keyValue].decode("utf-8"))
        elif typeOfValue=="richtext":
            self.categories[categoryNo].values[keyNo].setPlainText(self.defaultValues[keyValue].decode("utf-8"))
        elif typeOfValue=="list":
            value = ""
            for y, info in enumerate(Universals.getListFromStrint(self.defaultValues[keyValue])):
                if y!=0:
                    value += ";"
                value += unicode(info, "utf-8")
            self.categories[categoryNo].values[keyNo].setText(value.decode("utf-8"))
        elif typeOfValue=="trString":
            value = self.defaultValues[keyValue]
            for y, info in enumerate(self.categories[categoryNo].stringSearchList[self.categories[categoryNo].typesOfValues[keyNo][1]]):
                value = value.replace(str(info), str(self.categories[categoryNo].stringReplaceList[self.categories[categoryNo].typesOfValues[keyNo][1]][y]))
            self.categories[categoryNo].values[keyNo].setText(value.decode("utf-8"))
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
    
    def createDefaultValueButton(self, _category, _typeOfValue, _keyValue, x):
        pbtnDefaultValue = MPushButton(translate("Options", "?"))
        pbtnDefaultValue.setObjectName(_typeOfValue + "_"+_keyValue+"_"+str(x))
        toolTips = str(translate("Options", "Default Value : "))
        if _typeOfValue=="string":
            toolTips += self.defaultValues[_keyValue]
        elif _typeOfValue=="richtext":
            toolTips += self.defaultValues[_keyValue]
        elif _typeOfValue=="list":
            for y, info in enumerate(Universals.getListFromStrint(self.defaultValues[_keyValue])):
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
                toolTips += str(translate("Options", "Yes"))
            else:
                toolTips += str(translate("Options", "No"))
        elif _typeOfValue=="file":
            toolTips += self.defaultValues[_keyValue]
        pbtnDefaultValue.setToolTip(toolTips.decode("utf-8"))
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
            defaultValues = Settings.getDefaultValues()
            valueTypesAndValues = Settings.getValueTypesAndValues()
            for categoryNo, category in enumerate(self.categories):
                for x, keyValue in enumerate(category.keysOfSettings):
                    if category.visibleKeys.count(keyValue)>0:
                        if category.typesOfValues[x]=="string":
                            value = unicode(category.values[x].text(),"utf-8")
                        elif category.typesOfValues[x]=="richtext":
                            value = unicode(category.values[x].toPlainText(),"utf-8")
                        elif category.typesOfValues[x]=="list":
                            value = "['"
                            for y, bilgi in enumerate(unicode(category.values[x].text(),"utf-8").split(";")):
                                if y!=0:
                                    value += "','"
                                value += bilgi
                            value+="']"
                        elif category.typesOfValues[x][0]=="trString":
                            value = unicode(category.values[x].text(),"utf-8")
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
                            value = unicode(category.values[x].text(),"utf-8")
                        elif category.typesOfValues[x]=="password":
                            value = unicode(category.values[x].text(),"utf-8")
                        category.values[x].setStyleSheet("")
                        if Universals.MySettings[keyValue]!=value:
                            emendedValue = Settings.emendValue(keyValue, value, defaultValues[keyValue], valueTypesAndValues[keyValue])
                            if emendedValue != value:
                                answer = Dialogs.ask(translate("Options", "Incorrect Value"), 
                                                     str(translate("Options", "\"%s\" been set incorrectly.Are you want to set it automatically emend?")) % (str(category.labels[x])))
                                if answer==Dialogs.Yes:
                                    Universals.setMySetting(keyValue, emendedValue)
                                    if category.typesOfValues[x]=="string":
                                        category.values[x].setText(emendedValue.decode("utf-8"))
                                    elif category.typesOfValues[x]=="list":
                                        value = ""
                                        for y, info in enumerate(Universals.getListFromStrint(emendedValue)):
                                            if y!=0:
                                                value += ";"
                                            value += unicode(info, "utf-8")
                                        category.values[x].setText(value.decode("utf-8"))
                                else:
                                    if self.showType=="Normal":
                                        self.tboxCategories.setCurrentIndex(categoryNo)
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
            Records.checkSize()
            if isNeededRestart==True:
                self.reStart()
            if isDontClose:return False
            else:return True
        except:
            self.error = ReportBug.ReportBug()
            self.error.show()
            
    def applySetting(_category, _keyValue):
        try:
            defaultValues = Settings.getDefaultValues()
            valueTypesAndValues = Settings.getValueTypesAndValues()
            x = _category.keysOfSettings.index(_keyValue)
            if _category.visibleKeys.count(_keyValue)>0:
                if _category.typesOfValues[x]=="string":
                    value = unicode(_category.values[x].text(),"utf-8")
                elif _category.typesOfValues[x]=="richtext":
                    value = unicode(_category.values[x].toPlainText(),"utf-8")
                elif _category.typesOfValues[x]=="list":
                    value = "['"
                    for y, bilgi in enumerate(unicode(_category.values[x].text(),"utf-8").split(";")):
                        if y!=0:
                            value += "','"
                        value += bilgi
                    value+="']"
                elif _category.typesOfValues[x][0]=="trString":
                    value = unicode(_category.values[x].text(),"utf-8")
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
                    value = unicode(_category.values[x].text(),"utf-8")
                elif _category.typesOfValues[x]=="password":
                    value = unicode(_category.values[x].text(),"utf-8")
                _category.values[x].setStyleSheet("")
                if Universals.MySettings[_keyValue]!=value:
                    emendedValue = Settings.emendValue(_keyValue, value, defaultValues[_keyValue], valueTypesAndValues[_keyValue])
                    if emendedValue != value:
                        answer = Dialogs.ask(translate("Options", "Incorrect Value"), 
                                             str(translate("Options", "\"%s\" been set incorrectly.Are you want to set it automatically emend?")) % (str(_category.labels[x])))
                        if answer==Dialogs.Yes:
                            Universals.setMySetting(_keyValue, emendedValue)
                            if _category.typesOfValues[x]=="string":
                                _category.values[x].setText(emendedValue.decode("utf-8"))
                            elif _category.typesOfValues[x]=="list":
                                value = ""
                                for y, info in enumerate(Universals.getListFromStrint(emendedValue)):
                                    if y!=0:
                                        value += ";"
                                    value += unicode(info, "utf-8")
                                _category.values[x].setText(value.decode("utf-8"))
                        else:
                            if self.showType=="Normal":
                                self.tboxCategories.setCurrentIndex(_category.categoryNo)
                                _category.tabwTabs.setCurrentIndex(_category.tabsOfSettings[x])
                            _category.values[x].setStyleSheet("background-color: #FF5E5E;")
                            isDontClose = True
                    else:
                        Universals.setMySetting(_keyValue, value) 
        except:
            self.error = ReportBug.ReportBug()
            self.error.show()
            
    def createOptions(_category):
        correctSettingKeys(_category)
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
                    _category.values[x].setText(Universals.MySettings[keyValue].decode("utf-8"))
                elif _category.typesOfValues[x]=="richtext":
                    typeOfValue = "richtext"
                    _category.values.append(MTextEdit())
                    _category.values[x].setPlainText(Universals.MySettings[keyValue].decode("utf-8"))
                elif _category.typesOfValues[x]=="list":
                    typeOfValue = "list"
                    _category.values.append(MLineEdit())
                    value = ""
                    for y, info in enumerate(Universals.getListFromStrint(Universals.MySettings[keyValue])):
                        if y!=0:
                            value += ";"
                        value += unicode(info, "utf-8")
                    _category.values[x].setText(value.decode("utf-8"))
                elif _category.typesOfValues[x][0]=="trString":
                    typeOfValue = "trString"
                    _category.values.append(MLineEdit())
                    value = Universals.MySettings[keyValue]
                    for y, info in enumerate(_category.stringSearchList[_category.typesOfValues[x][1]]):
                        value = value.replace(str(info), str(_category.stringReplaceList[_category.typesOfValues[x][1]][y]))
                    _category.values[x].setText(value.decode("utf-8"))
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
                    _category.values[x].addItems([translate("Options", "No"),translate("Options", "Yes")])
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
                if _category.typesOfValues[x]=="password":
                    _category.values.append(MLineEdit())
                    _category.values[x].setText(Universals.MySettings[keyValue].decode("utf-8"))
                    _category.values[x].setEchoMode(MLineEdit.Password)
                if typeOfValue=="list":
                    pbtnEditValue = _category.parent().createEditValueButton(_category, typeOfValue, keyValue, x)
                    valueLayout.addWidget(pbtnEditValue)
                pbtnDefaultValue = _category.parent().createDefaultValueButton(_category, typeOfValue, keyValue, x)
                valueLayout.addWidget(pbtnDefaultValue)
                valueLayout.insertWidget(0, _category.values[x])
                _category.values[x].setToolTip(_category.toolTips[x])
                lblLabel = MLabel(_category.labels[x]+u" : ")
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
            
    def correctSettingKeys(_category):
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
        if Universals.isActivePyKDE4==True:
            self.setButtons(MDialog.None)
        self.setWindowTitle(translate("EditDialog", "Advanced Value Editor"))
        self.requestInfos = str(_sender.objectName()).split("_")
        self.categoryNo = self.parent().tboxCategories.currentIndex()
        self.typeOfValue = self.requestInfos[0]
        self.keyValue = self.requestInfos[1]
        self.keyNo = int(self.requestInfos[2])
        if self.typeOfValue=="string":
            #This İs Not Used (For only next)
            currentValue = str(self.parent().categories[self.categoryNo].values[self.keyNo].text())
            self.EditorWidget = MTextEdit(self)
            self.EditorWidget.setText(currentValue.decode("utf-8"))
        elif self.typeOfValue=="richtext":
            #This İs Not Used (For only next)
            currentValue = str(self.parent().categories[self.categoryNo].values[self.keyNo].plainText())
            self.EditorWidget = MTextEdit(self)
            self.EditorWidget.setAcceptRichText(True)
            self.EditorWidget.setPlainText(currentValue.decode("utf-8"))
        elif self.typeOfValue=="list":
            currentValue = str(self.parent().categories[self.categoryNo].values[self.keyNo].text())
            if Universals.isActivePyKDE4==True:
                self.EditorWidget = MEditListBox(self)
                self.EditorWidget.setItems([x.decode("utf-8") for x in currentValue.split(";")])
            else:
                self.EditorWidget = MTextEdit(self)
                self.EditorWidget.setText(currentValue.replace(";", "\n").decode("utf-8"))
        elif self.typeOfValue=="options":
            #This İs Not Used (For only next)
            currentValue = str(self.parent().categories[self.categoryNo].values[self.keyNo].currentIndex())
        elif self.typeOfValue=="number":
            #This İs Not Used (For only next)
            currentValue = str(self.parent().categories[self.categoryNo].values[self.keyNo].value())
        elif self.typeOfValue=="Yes/No":
            #This İs Not Used (For only next)
            if self.parent().categories[self.categoryNo].values[self.keyNo].currentIndex()==1:
                currentValue = True
            else:
                currentValue = False
        elif self.typeOfValue=="file":
            #This İs Not Used (For only next)
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
        if Universals.isActivePyKDE4==True:
            self.setMainWidget(pnlMain)
        else:
            self.setLayout(vblMain)
        self.setMinimumSize(550, 400)
        self.show()
        
    def apply(self):
        if self.typeOfValue=="string":
            #This İs Not Used (For only next)
            newValue = "" #NotUsed
            self.parent().categories[self.categoryNo].values[self.keyNo].setText(newValue.decode("utf-8"))
        elif self.typeOfValue=="richtext":
            #This İs Not Used (For only next)
            newValue = "" #NotUsed
            self.parent().categories[self.categoryNo].values[self.keyNo].setPlainText(newValue.decode("utf-8"))
        elif self.typeOfValue=="list":
            value = ""
            if Universals.isActivePyKDE4==True:
                for y, info in enumerate(self.EditorWidget.items()):
                    if y!=0:
                        value += ";"
                    value += unicode(info, "utf-8")
            else:
                value = unicode(self.EditorWidget.toPlainText(), "utf-8").replace("\n", ";")
            self.parent().categories[self.categoryNo].values[self.keyNo].setText(value.decode("utf-8"))
        elif self.typeOfValue=="options":
            #This İs Not Used (For only next)
            newValue = "" #NotUsed
            self.parent().categories[self.categoryNo].values[self.keyNo].setCurrentIndex(self.parent().categories[self.categoryNo].valuesOfOptionsKeys[self.parent().categories[self.categoryNo].typesOfValues[self.keyNo][1]].index(newValue))
        elif self.typeOfValue=="number":
            #This İs Not Used (For only next)
            newValue = "" #NotUsed
            self.parent().categories[self.categoryNo].values[self.keyNo].setValue(int(newValue)) 
        elif self.typeOfValue=="Yes/No":
            #This İs Not Used (For only next)
            newValue = "" #NotUsed
            if eval(newValue.title())==True:
                self.parent().categories[self.categoryNo].values[self.keyNo].setCurrentIndex(1)
            else:
                self.parent().categories[self.categoryNo].values[self.keyNo].setCurrentIndex(0)
        elif self.typeOfValue=="file":
            #This İs Not Used (For only next)
            newValue = "" #NotUsed
            self.parent().categories[self.categoryNo].values[self.keyNo].setText(newValue)
        self.close()
        
class MyFormLayout(MFormLayout):
    def __init__(self):
        MFormLayout.__init__(self, None)
        self.keysOfSettings = []
        
class General(MWidget):
    def __init__(self, _parent=None, _showType = None, _visibleKeys = None):
        MWidget.__init__(self, _parent)
        self.titleOfCategory = translate("Options/General", "General")
        self.labelOfCategory = translate("Options/General", "You can change the general settings in this section.")
        self.categoryNo = None
        self.Panel = MVBoxLayout(self)
        self.values, self.lblLabels = [], []
        self.keysOfSettings = ["applicationStyle", "themeName", "isSaveActions", "maxRecordFileSize", 
                                "isMinimumWindowMode", "updateInterval", "isShowQuickMakeWindow", 
                                "isShowTransactionDetails", "windowMode", "language"]
        self.tabsOfSettings = [None, None, None, None, 
                                None, None, None, 
                                None, None, None]
        self.tabNames = []
        if _visibleKeys==None:
            self.visibleKeys = self.keysOfSettings
        else:
            self.visibleKeys = _visibleKeys
        self.neededRestartSettingKeys = ["language", "themeName", "windowMode"]
        self.valuesOfOptionsKeys = []
        self.labels = [translate("Options/General", "Application Style"),
                    translate("Options/General", "Application Theme"), 
                    translate("Options/General", "Save Actions"), 
                    translate("Options/General", "Record File Size"), 
                    translate("Options/General", "Activate Minimal Window Mode"), 
                    translate("Options/General", "Update Interval (in days)"), 
                    translate("Options/General", "Show Quick Make Dialog"),  
                    translate("Options/General", "Show Transaction Details"), 
                    translate("Options/General", "Window Mode"),  
                    translate("Options/General", "Application Language")]
        self.toolTips = [translate("Options/General", "You can select Hamsi Manager`s style."),
                    translate("Options/General", "You can select Hamsi Manager`s theme."),
                    translate("Options/General", "If you want to save the actions you performed select \"Yes\"."), 
                    translate("Options/General", "You can select record file size.(Kilobytes)"), 
                    translate("Options/General", "You have to activate this if you want to work as little number of windows as possible."), 
                    translate("Options/General", "Which interval (in days) do you want to set to check the updates?"), 
                    translate("Options/General", "Are you want to show quick make dialog in runed with command line or my plugins?"),
                    translate("Options/General", "Are you want to show transaction details after save table?"), 
                    translate("Options/General", "You can select window mode.You can select \"Mini\" section for netbook or small screen."),
                    translate("Options/General", "You can select Hamsi Manager`s language.")]
        self.typesOfValues = [["options", 1], ["options", 4], "Yes/No", ["number", 3], 
                                "Yes/No", ["number", 2], "Yes/No", "Yes/No", ["options", 5], ["options", 0]]
        styles = Variables.getStyles()
        themes = InputOutputs.getInstalledThemes()
        self.valuesOfOptions = [InputOutputs.getInstalledLanguagesNames(), styles, 
                                ["1", "30"], ["10", "100000"], themes, 
                                [translate("Options/General", "Normal"), 
                                    translate("Options/General", "Mini")]]
        self.valuesOfOptionsKeys = [InputOutputs.getInstalledLanguagesCodes(), styles, 
                                ["1", "30"], ["10", "100000"], themes, 
                                Universals.windowModeKeys]
        createOptions(self)
        if Universals.isActivePyKDE4==True:
            setVisibleFormItems(self, "language", False)
        if self.visibleKeys.count("applicationStyle")>0:
            MObject.connect(self.values[self.keysOfSettings.index("applicationStyle")], SIGNAL("currentIndexChanged(int)"), self.styleChanged)
        if self.visibleKeys.count("windowMode")>0:
            MObject.connect(self.values[self.keysOfSettings.index("windowMode")], SIGNAL("currentIndexChanged(int)"), self.windowModeChanged)
        if self.visibleKeys.count("isSaveActions")>0:
            MObject.connect(self.values[self.keysOfSettings.index("isSaveActions")], SIGNAL("currentIndexChanged(int)"), self.saveActionsChanged)
            self.saveActionsChanged()
    
    def saveActionsChanged(self):
        if self.values[self.keysOfSettings.index("isSaveActions")].currentIndex()==1:
            setEnabledFormItems(self, "maxRecordFileSize", True)
        else:
            setEnabledFormItems(self, "maxRecordFileSize", False)
    
    def styleChanged(self, _value):
        MApplication.setStyle(self.values[self.keysOfSettings.index("applicationStyle")].currentText())
        
        
    def windowModeChanged(self, _value):
        Universals.setMySetting("isShowWindowModeSuggestion", True)

class Correct(MWidget):
    def __init__(self, _parent=None, _showType = None, _visibleKeys = None):
        MWidget.__init__(self, _parent)
        self.titleOfCategory = translate("Options/Correct", "Correct")
        self.labelOfCategory = translate("Options/Correct", "You can change the correct and emend settings in this section.")
        self.categoryNo = None
        self.Panel = MVBoxLayout(self)
        self.values, self.lblLabels = [], []
        self.keysOfSettings = ["validSentenceStructure", "validSentenceStructureForFile", 
                                "validSentenceStructureForFileExtension", "fileExtesionIs", "isEmendIncorrectChars", 
                                "isCorrectFileNameWithSearchAndReplaceTable", "isClearFirstAndLastSpaceChars", "isCorrectDoubleSpaceChars"]
        self.tabsOfSettings = [None, None, 
                                None, None, None, 
                                None, None, None]
        self.tabNames = []
        if _visibleKeys==None:
            self.visibleKeys = self.keysOfSettings
        else:
            self.visibleKeys = _visibleKeys
        self.neededRestartSettingKeys = []
        self.valuesOfOptionsKeys = []
        self.labels = [translate("Options/Correct", "Valid Sentence Structure"), 
                    translate("Options/Correct", "Valid Sentence Structure For Files"),
                    translate("Options/Correct", "Valid Sentence Structure For File Extensions"), 
                    translate("Options/Correct", "Which Part Is The File Extension"), 
                    translate("Options/Correct", "Emend Incorrect Chars"),  
                    translate("Options/Correct", "Correct File Name By Search Table"), 
                    translate("Options/Correct", "Clear First And Last Space Chars"), 
                    translate("Options/Correct", "Correct Double Space Chars")]
        self.toolTips = [translate("Options/Correct", "All information (Artist name,title etc.) will be changed automatically to the format you selected."), 
                    translate("Options/Correct", "File and directory names will be changed automatically to the format you selected."),
                    translate("Options/Correct", "File extensions will be changed automatically to the format you selected."), 
                    translate("Options/Correct", "Which part of the filename is the file extension?"), 
                    translate("Options/Correct", "Are you want to emend incorrect chars?"), 
                    translate("Options/Correct", "Are you want to correct file and directory names by search and replace table?"), 
                    translate("Options/Correct", "Are you want to clear first and last space chars?"), 
                    translate("Options/Correct", "Are you want to correct double space chars?")]
        self.typesOfValues = [["options", 0], ["options", 0], ["options", 0], 
                            ["options", 1], "Yes/No", "Yes/No", 
                            "Yes/No", "Yes/No"]
        self.valuesOfOptions = [[translate("Options/Correct", "Title"), 
                                    translate("Options/Correct", "All Small"), 
                                    translate("Options/Correct", "All Caps"), 
                                    translate("Options/Correct", "Sentence"), 
                                    translate("Options/Correct", "Don`t Change")], 
                                [translate("Options/Correct", "After The First Point"), 
                                    translate("Options/Correct", "After The Last Point")]]
        self.valuesOfOptionsKeys = [Universals.validSentenceStructureKeys, 
                        Universals.fileExtesionIsKeys]
        createOptions(self)
                
class SearchAndReplace(MWidget):
    def __init__(self, _parent=None, _showType = None, _visibleKeys = None):
        MWidget.__init__(self, _parent)
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
            self.setColumnCount(6)
            self.setHorizontalHeaderLabels(["id", 
                            translate("Options/SearchAndReplace", "Search"), 
                            translate("Options/SearchAndReplace", "Replace"), 
                            translate("Options/SearchAndReplace", "Active"), 
                            translate("Options/SearchAndReplace", "C.Sens."), 
                            translate("Options/SearchAndReplace", "RegExp")])
            self.hideColumn(0)
            self.setColumnWidth(1,135)
            self.setColumnWidth(2,135)
            self.setColumnWidth(3,50)
            self.setColumnWidth(4,50)
            self.setColumnWidth(5,50)
            self.searchAndReplaceTableValues = Settings.searchAndReplaceTable()
            self.setRowCount(len(self.searchAndReplaceTableValues)+1)
            self.isShowChanges=False
            for rowNo, info in enumerate(self.searchAndReplaceTableValues):
                for columnNo in range(self.columnCount()):
                    if columnNo>2:
                        if info[columnNo] == 1:
                            checkState = Mt.Checked
                        else:
                            checkState = Mt.Unchecked
                        twiItem = MTableWidgetItem(u" ")
                        twiItem.setCheckState(checkState)
                        self.setItem(rowNo, columnNo, twiItem)
                    else:
                        self.setItem(rowNo, columnNo, MTableWidgetItem(str(info[columnNo]).decode("utf-8")))
            self.setItem(len(self.searchAndReplaceTableValues), 1, MTableWidgetItem(u""))
            self.setItem(len(self.searchAndReplaceTableValues), 2, MTableWidgetItem(u""))
            twiItem = MTableWidgetItem(u" ")
            twiItem.setCheckState(Mt.Checked)
            self.setItem(len(self.searchAndReplaceTableValues), 3, twiItem)
            twiItem1 = MTableWidgetItem(u" ")
            twiItem1.setCheckState(Mt.Checked)
            self.setItem(len(self.searchAndReplaceTableValues), 4, twiItem1)
            twiItem2 = MTableWidgetItem(u" ")
            twiItem2.setCheckState(Mt.Unchecked)
            self.setItem(len(self.searchAndReplaceTableValues), 5, twiItem2)
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
                        self.currentItem().setText(u"")
                    elif selected.objectName()==self.namesOfButtons[1]:
                        MApplication.clipboard().setText(self.currentItem().text())
                    elif selected.objectName()==self.namesOfButtons[2]:
                        self.currentItem().setText(MApplication.clipboard().text())
                    elif selected.objectName()==self.namesOfButtons[3]:
                        self.currentItem().setText(u"")
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
                        self.setItem(self.rowCount()-1, 1, MTableWidgetItem(u""))
                        self.setItem(self.rowCount()-1, 2, MTableWidgetItem(u""))
                        twiItem = MTableWidgetItem(u" ")
                        twiItem.setCheckState(Mt.Checked)
                        self.setItem(self.rowCount()-1, 3, twiItem)
                        twiItem1 = MTableWidgetItem(u" ")
                        twiItem1.setCheckState(Mt.Checked)
                        self.setItem(self.rowCount()-1, 4, twiItem1)
                        twiItem2 = MTableWidgetItem(u" ")
                        twiItem2.setCheckState(Mt.Unchecked)
                        self.setItem(self.rowCount()-1, 5, twiItem2)
                        self.isShowChanges = True
                except:pass
        
        def save(self):
            for rowNo in range(self.rowCount()):
                checkStateActive, checkStateCaseSensitive, checkStateRegExp = 0, 0, 0
                if self.item(rowNo, 3).checkState() == Mt.Checked:
                    checkStateActive = 1
                if self.item(rowNo, 4).checkState() == Mt.Checked:
                    checkStateCaseSensitive = 1
                if self.item(rowNo, 5).checkState() == Mt.Checked:
                    checkStateRegExp = 1
                try:
                    temp = self.item(rowNo, 0).text()
                    if self.isRowHidden(rowNo):
                        Settings.searchAndReplaceTable("delete", str(self.item(rowNo, 0).text()))
                    else:
                        if str(self.item(rowNo, 1).text()).strip()!="":
                            Settings.searchAndReplaceTable("update", str(self.item(rowNo, 0).text()), str(self.item(rowNo, 1).text()), str(self.item(rowNo, 2).text()), checkStateActive, checkStateCaseSensitive, checkStateRegExp)
                except:
                    if str(self.item(rowNo, 1).text()).strip()!="":
                        insertedId = Settings.searchAndReplaceTable("add", str(self.item(rowNo, 1).text()), str(self.item(rowNo, 2).text()), checkStateActive, checkStateCaseSensitive, checkStateRegExp)
                        self.setItem(rowNo, 0, MTableWidgetItem(str(insertedId)))
        
class ClearGeneral(MWidget):
    def __init__(self, _parent=None, _showType = None, _visibleKeys = None):
        MWidget.__init__(self, _parent)
        self.titleOfCategory = translate("Options/ClearGeneral", "General Cleaning")
        self.labelOfCategory = translate("Options/ClearGeneral", "You can change the settings to clean your system in this section.")
        self.categoryNo = None
        self.Panel = MVBoxLayout(self)
        self.values, self.lblLabels = [], []
        self.keysOfSettings = ["isDeleteEmptyDirectories", "unneededDirectoriesIfIsEmpty", "unneededDirectories", 
                            "unneededFiles", "unneededFileExtensions", 
                            "ignoredDirectories", "ignoredFiles", "ignoredFileExtensions", 
                            "isClearEmptyDirectoriesWhenSave", "isClearEmptyDirectoriesWhenMoveOrChange", 
                            "isClearEmptyDirectoriesWhenCopyOrChange", "isClearEmptyDirectoriesWhenFileMove", 
                            "isAutoCleanSubFolderWhenSave", "isAutoCleanSubFolderWhenMoveOrChange", 
                            "isAutoCleanSubFolderWhenCopyOrChange", "isAutoCleanSubFolderWhenFileMove"]
        self.tabsOfSettings = [0, 0, 0, 
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
        self.labels = [translate("Options/ClearGeneral", "Delete Empty Directories"), 
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
        self.toolTips = [translate("Options/ClearGeneral", "Are you want to delete empty directories?"), 
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
        self.typesOfValues = ["Yes/No", "list", "list", "list", "list", "list", "list", "list", 
                              "Yes/No", "Yes/No", "Yes/No", "Yes/No", "Yes/No", "Yes/No", "Yes/No", "Yes/No"]
        self.valuesOfOptions = []
        createOptions(self) 
        if self.visibleKeys.count("isDeleteEmptyDirectories")>0:
            MObject.connect(self.values[self.keysOfSettings.index("isDeleteEmptyDirectories")], SIGNAL("currentIndexChanged(int)"), self.deleteEmptyDirectoriesChanged)
            self.deleteEmptyDirectoriesChanged()
            
    def deleteEmptyDirectoriesChanged(self):
        if self.values[self.keysOfSettings.index("isDeleteEmptyDirectories")].currentIndex()==1:
            setEnabledFormItems(self, "unneededDirectoriesIfIsEmpty", False)
            setEnabledFormItems(self, "ignoredDirectories", True)
            setEnabledFormItems(self, "ignoredFiles", True)
            setEnabledFormItems(self, "ignoredFileExtensions", True)
        else:
            setEnabledFormItems(self, "unneededDirectoriesIfIsEmpty", True)
            setEnabledFormItems(self, "ignoredDirectories", False)
            setEnabledFormItems(self, "ignoredFiles", False)
            setEnabledFormItems(self, "ignoredFileExtensions", False)
        
class Cover(MWidget):
    def __init__(self, _parent=None, _showType = None, _visibleKeys = None):
        MWidget.__init__(self, _parent)
        self.titleOfCategory = translate("Options/Cover", "Cover")
        self.labelOfCategory = translate("Options/Cover", "You can change the cover settings in this section.")
        self.categoryNo = None
        self.Panel = MVBoxLayout(self)
        self.values, self.lblLabels = [], []
        self.keysOfSettings = ["priorityIconNames", "isChangeExistIcon", "isAskIfHasManyImagesInAlbumDirectory", 
                            "isAutoMakeIconToDirectoryWhenSave", "isAutoMakeIconToDirectoryWhenMoveOrChange", 
                            "isAutoMakeIconToDirectoryWhenCopyOrChange", "isAutoMakeIconToDirectoryWhenFileMove", 
                            "iconNameFormat", "iconFileType"]
        self.tabsOfSettings = [0, 0, 0, 0, 0, 0, 0, 
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
                    translate("Options/Cover", "Change Directory Icon (Table Saved)"), 
                    translate("Options/Cover", "Change Directory Icon (Moved Or Changed)"), 
                    translate("Options/Cover", "Change Directory Icon (Copied Or Changed)"), 
                    translate("Options/Cover", "Change Directory Icon (Moved File)"), 
                    translate("Options/Cover", "Icon Name Format"), 
                    translate("Options/Cover", "Icon Type")]
        self.toolTips = [translate("Options/Cover", "The file names you selected will be folder icons first.<br>If the file name you selected does not exist, the first graphics file in the folder will be set as the folder icon.<br><font color=blue>Example: cover; icon...</font>"), 
                    translate("Options/Cover", "Are you want to change directory icon if is already exist?"), 
                    translate("Options/Cover", "Ask me if has many images in the directory.<br>Note: If you select \"No\" the first image will be chosen."), 
                    translate("Options/Cover", "Do you want to change directory icon when table saved?"), 
                    translate("Options/Cover", "Do you want to change directory icon when directory moved or changed?"), 
                    translate("Options/Cover", "Do you want to change directory icon when directory copied or changed?"), 
                    translate("Options/Cover", "Do you want to change directory icon when file moved?"), 
                    translate("Options/Cover", "You can set icon name format."), 
                    translate("Options/Cover", "You can select file type of icon.")]
        self.typesOfValues = ["list", "Yes/No", "Yes/No", "Yes/No", "Yes/No", "Yes/No", "Yes/No", 
                            ["trString", 0], ["options", 0]]
        self.valuesOfOptions = [["png", "jpg"]]
        self.valuesOfOptionsKeys = [["png", "jpg"]]
        self.stringSearchList = [Universals.iconNameFormatKeys]
        self.stringReplaceList = [Universals.iconNameFormatLabels]
        createOptions(self) 
 

class Advanced(MWidget):
    def __init__(self, _parent=None, _showType = None, _visibleKeys = None):
        MWidget.__init__(self, _parent)
        self.titleOfCategory = translate("Options/Advanced", "Advanced")
        self.labelOfCategory = translate("Options/Advanced", "You can change the advanced settings in this section.<br><font color=red>Only proceed when you make sure that everything here is correct.</font>")
        self.categoryNo = None
        self.Panel = MVBoxLayout(self)
        self.values, self.lblLabels = [], []
        self.keysOfSettings = ["fileSystemEncoding", "isMoveToTrash", "imageExtensions", "musicExtensions", "NeededObjectsName", "isActivePyKDE4"]
        self.tabsOfSettings = [None, None, None, None, None, None]
        self.tabNames = []
        if _visibleKeys==None:
            self.visibleKeys = self.keysOfSettings
        else:
            self.visibleKeys = _visibleKeys
        self.neededRestartSettingKeys = ["fileSystemEncoding", "NeededObjectsName", "isActivePyKDE4"]
        self.valuesOfOptionsKeys = []
        self.labels = [translate("Options/Advanced", "File System Character Set"), 
                    translate("Options/Advanced", "Move To Trash"),  
                    translate("Options/Advanced", "Graphics Files` Extensions"), 
                    translate("Options/Advanced", "Music Files` Extensions"), 
                    translate("Options/Advanced", "Please Select The Object Set You Want To Use"), 
                    translate("Options/Advanced", "Do You Want To Use PyKDE4?")]
        self.toolTips = [(str(translate("Options/Advanced", "You can choose the character set of your operating system and/or file system. The records will be saved according to the character set of your choice.<br><font color=red><b>If you think the character set is wrong, you can change it. However we do not recommend to make any changes if you are not definitely sure. Else, proceed at your own responsibility!<br>Default is \"%s\".</b></font>")) % (Variables.defaultFileSystemEncoding)).decode("utf-8"), 
                    translate("Options/Advanced", "Would you like to move files to the trash files to be deleted?<br><font color=red><b>This process can cause slow!</b></font>"), 
                    translate("Options/Advanced", "The files with the extension you have selected will be recognized as graphics files.<br><font color=red><b>We do not recommend to make any changes if you are not definitely sure. Proceed at your own responsibility!</b></font><br><font color=blue>Example: png;jpg;gif;...</font>"), 
                    translate("Options/Advanced", "The files with the extension you have selected will be recognized as music files.<br><font color=red><b>We do not recommend to make any changes if you are not definitely sure. Proceed at your own responsibility!</b></font><br><font color=blue>Example: mp3;...</font>"), 
                    translate("Options/Advanced", "KPlease select the object set you want to use (the object types installed on your system will be presented in the Options dialog.)"), 
                    translate("Options/Advanced", "<font color=blue>You can use PyKDE4 for better desktop integration.</font>")]
        self.typesOfValues = [["options", 0], "Yes/No", "list", "list", ["options", 1], "Yes/No"]
        charSets = Variables.getCharSets()
        objectsNames = [] 
        try:
            import PyQt4
            objectsNames.append("PyQt4")
        except:pass
#        try:
#            import PySide
#            objectsNames.append("PySide")
#        except:pass
        try:
            import PyKDE4
        except:
            keyNo = self.keysOfSettings.index("isActivePyKDE4")
            del self.keysOfSettings[keyNo]
            del self.labels[keyNo]
            del self.toolTips[keyNo]
            del self.typesOfValues[keyNo]
            keyNo = self.keysOfSettings.index("isMoveToTrash")
            del self.keysOfSettings[keyNo]
            del self.labels[keyNo]
            del self.toolTips[keyNo]
            del self.typesOfValues[keyNo]
        self.valuesOfOptions = [charSets, objectsNames]
        self.valuesOfOptionsKeys = [charSets, objectsNames]
        createOptions(self) 
        if self.visibleKeys.count("isActivePyKDE4")>0:
            MObject.connect(self.values[self.keysOfSettings.index("isActivePyKDE4")], SIGNAL("currentIndexChanged(int)"), self.activePyKDE4Changed)
            self.activePyKDE4Changed()
    
    def activePyKDE4Changed(self):
        if self.values[self.keysOfSettings.index("isActivePyKDE4")].currentIndex()==1:
            setVisibleFormItems(self, "isMoveToTrash", True)
        else:
            setVisibleFormItems(self, "isMoveToTrash", False)
        
class Player(MWidget):
    def __init__(self, _parent=None, _showType = None, _visibleKeys = None):
        MWidget.__init__(self, _parent)
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
        self.valuesOfOptions = [Variables.getAvailablePlayers(), Universals.mplayerSoundDevices]
        self.valuesOfOptionsKeys = [Variables.getAvailablePlayers(), Universals.mplayerSoundDevices]
        createOptions(self)
        if self.visibleKeys.count("playerName")>0:
            MObject.connect(self.values[self.keysOfSettings.index("playerName")], SIGNAL("currentIndexChanged(int)"), self.playerChanged)
            self.playerChanged()
    
    def playerChanged(self):
        if self.values[self.keysOfSettings.index("playerName")].currentIndex()==0:
            setVisibleFormItems(self, "mplayerPath", True)
            setVisibleFormItems(self, "mplayerArgs", True)
            setVisibleFormItems(self, "mplayerAudioDevicePointer", True)
            setVisibleFormItems(self, "mplayerAudioDevice", True)
        else:
            setVisibleFormItems(self, "mplayerPath", False)
            setVisibleFormItems(self, "mplayerArgs", False)
            setVisibleFormItems(self, "mplayerAudioDevicePointer", False)
            setVisibleFormItems(self, "mplayerAudioDevice", False)

class Packager(MWidget):
    def __init__(self, _parent=None, _showType = None, _visibleKeys = None):
        MWidget.__init__(self, _parent)
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
        createOptions(self) 
    
class Cleaner(MWidget):
    def __init__(self, _parent=None, _showType = None, _visibleKeys = None):
        MWidget.__init__(self, _parent)
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
        createOptions(self) 
        
class Amarok(MWidget):
    def __init__(self, _parent=None, _showType = None, _visibleKeys = None):
        MWidget.__init__(self, _parent)
        self.titleOfCategory = translate("Options/Amarok", "Amarok")
        self.labelOfCategory = translate("Options/Amarok", "You can change the Amarok settings in this section.")
        self.categoryNo = None
        self.Panel = MVBoxLayout(self)
        self.values, self.lblLabels = [], []
        self.keysOfSettings = ["amarokIsUseHost", "amarokDBHost", "amarokDBPort", "amarokDBUser", "amarokDBPass", "amarokDBDB", "pathOfMysqldSafe"]
        self.tabsOfSettings = [None, None, None, None, None, None, None]
        self.tabNames = []
        if _visibleKeys==None:
            self.visibleKeys = self.keysOfSettings
        else:
            self.visibleKeys = _visibleKeys
        self.neededRestartSettingKeys = []
        self.valuesOfOptionsKeys = []
        self.labels = [translate("Options/Amarok", "Using MySQL Server"), 
                    translate("Options/Amarok", "Host"), 
                    translate("Options/Amarok", "Port"), 
                    translate("Options/Amarok", "User Name"), 
                    translate("Options/Amarok", "Password"), 
                    translate("Options/Amarok", "Database"), 
                    translate("Options/Amarok", "Path Of Executable \"mysqld_safe\"")]
        self.toolTips = [translate("Options/Amarok", "Are you use MySQL server in the Amarok?"), 
                    translate("Options/Amarok", "Please enter host name of Amarok database."), 
                    translate("Options/Amarok", "Please enter port number of Amarok database."), 
                    translate("Options/Amarok", "Please enter user name of Amarok database."), 
                    translate("Options/Amarok", "Please enter user password of Amarok database."), 
                    translate("Options/Amarok", "Please enter database name of Amarok database."), 
                    translate("Options/Amarok", "Where is executable \"mysqld_safe\" file?")]
        self.typesOfValues = ["Yes/No", "string", "string", "string", "password", "string", ["file", "executable"]]
        self.valuesOfOptions = []
        self.valuesOfOptionsKeys = []
        createOptions(self)
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
            setVisibleFormItems(self, "amarokDBHost", False)
            setVisibleFormItems(self, "amarokDBPort", False)
            setVisibleFormItems(self, "amarokDBUser", False)
            setVisibleFormItems(self, "amarokDBPass", False)
            setVisibleFormItems(self, "amarokDBDB", False)
            setVisibleFormItems(self, "pathOfMysqldSafe", True)
        else:
            setVisibleFormItems(self, "amarokDBHost", True)
            setVisibleFormItems(self, "amarokDBPort", True)
            setVisibleFormItems(self, "amarokDBUser", True)
            setVisibleFormItems(self, "amarokDBPass", True)
            setVisibleFormItems(self, "amarokDBDB", True)
            setVisibleFormItems(self, "pathOfMysqldSafe", False)
    
    def saveSettingsForTest(self):
        applySetting(self, "amarokIsUseHost")
        applySetting(self, "amarokDBHost")
        applySetting(self, "amarokDBPort")
        applySetting(self, "amarokDBUser")
        applySetting(self, "amarokDBPass")
        applySetting(self, "amarokDBDB")
    
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
        

class MySettings(MWidget):
    def __init__(self, _parent=None, _showType = None, _visibleKeys = None):
        MWidget.__init__(self, _parent)
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
        lblBackUp = MLabel(u"<b>" + translate("Options/MySettings", "Backup Settings") + u"</b>")
        lblRestore = MLabel(u"<b>" + translate("Options/MySettings", "Restore Settings") + u"</b>")
        reFillSettings = MLabel(u"<b>" + translate("Options/MySettings", "Reset Settings") + u"</b>")
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
            import InputOutputs, Records
            InputOutputs.clearTempFiles()
            Records.saveAllRecords()
            Dialogs.show(translate("Options/General", "Error Logs Deleted"), translate("Options/General", "All created by Hamsi Manager error logs and temp files is deleted."))
        except:
            import ReportBug
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
            import MyConfigure
            answer = Dialogs.ask(translate("Options/MySettings", "KDE4 Language Will Be Reinstalled Into Hamsi Manager"),
                        translate("Options/MySettings", "Are you sure you want to reinstall kde4 language into Hamsi Manager?"))
            if answer==Dialogs.Yes:
                from PyQt4.QtCore import QLocale 
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
        except:
            error = ReportBug.ReportBug()
            error.show()
    
    def restoreSearchAndReplaceTable(self):
        try:
            if Settings.restoreBackUp("searchAndReplaceTable")==True:
                self.parent().parent().close()
        except:
            error = ReportBug.ReportBug()
            error.show()
        
    def restoreSettings(self):
        try:
            if Settings.restoreBackUp("Settings")==True:
                self.parent().parent().reStart()
        except:
            error = ReportBug.ReportBug()
            error.show()
    
    def restoreAll(self):
        try:
            if Settings.restoreBackUp("All")==True:
                self.parent().parent().reStart()
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
                Settings.reFillDatabases("bookmarks")
            elif answer==translate("Options/MySettings", "Back Up And Reset"):
                Settings.reFillDatabases("bookmarks", _makeBackUp=True)
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
                Settings.reFillDatabases("searchAndReplaceTable")
            elif answer==translate("Options/MySettings", "Back Up And Reset"):
                Settings.reFillDatabases("searchAndReplaceTable", _makeBackUp=True)
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
                Settings.reFillSettings(False, True)
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
                Settings.reFillAll(False, True)
            self.parent().parent().reStart()
        except:
            error = ReportBug.ReportBug()
            error.show()
        
        
        
        

class QuickOptions(MMenu):
    def __init__(self, _parent=None):
        MDialog.__init__(self, _parent)
        self.setTitle(translate("MenuBar", "Quick Options"))
        self.setObjectName(translate("MenuBar", "Quick Options"))
        self.values = []
        self.keysOfSettings = ["validSentenceStructure", "validSentenceStructureForFile", 
                                "validSentenceStructureForFileExtension", "fileExtesionIs", "isEmendIncorrectChars", 
                                "isCorrectFileNameWithSearchAndReplaceTable", "isClearFirstAndLastSpaceChars", "isCorrectDoubleSpaceChars"]
        self.labels = [translate("QuickOptions", "Valid Sentence Structure"), 
                    translate("QuickOptions", "Valid Sentence Structure For Files"),
                    translate("QuickOptions", "Valid Sentence Structure For File Extensions"), 
                    translate("QuickOptions", "Which Part Is The File Extension"), 
                    translate("QuickOptions", "Emend Incorrect Chars"),  
                    translate("QuickOptions", "Correct File Name By Search Table"), 
                    translate("QuickOptions", "Clear First And Last Space Chars"), 
                    translate("QuickOptions", "Correct Double Space Chars")]
        self.toolTips = [translate("QuickOptions", "All information (Artist name,title etc.) will be changed automatically to the format you selected."), 
                    translate("QuickOptions", "File and directory names will be changed automatically to the format you selected."),
                    translate("QuickOptions", "File extensions will be changed automatically to the format you selected."), 
                    translate("QuickOptions", "Which part of the filename is the file extension?"), 
                    translate("QuickOptions", "Are you want to emend incorrect chars?"), 
                    translate("QuickOptions", "Are you want to correct file and directory names by search and replace table?"), 
                    translate("QuickOptions", "Are you want to clear first and last space chars?"), 
                    translate("QuickOptions", "Are you want to correct double space chars?")]
        self.typesOfValues = [["options", 0], ["options", 0], ["options", 0], 
                            ["options", 1], "Yes/No", "Yes/No", 
                            "Yes/No", "Yes/No"]
        self.valuesOfOptions = [[translate("QuickOptions", "Title"), 
                                    translate("QuickOptions", "All Small"), 
                                    translate("QuickOptions", "All Caps"), 
                                    translate("QuickOptions", "Sentence"), 
                                    translate("QuickOptions", "Don`t Change")], 
                                [translate("QuickOptions", "After The First Point"), 
                                    translate("QuickOptions", "After The Last Point")]]
        self.valuesOfOptionsKeys = [Universals.validSentenceStructureKeys,
                                    Universals.fileExtesionIsKeys]
        self.createActions()
        
    def createActions(self):
        for x, keyValue in enumerate(self.keysOfSettings):
            if self.typesOfValues[x][0]=="options":
                self.values.append(MComboBox())
                for info in self.valuesOfOptions[self.typesOfValues[x][1]]:
                    self.values[x].addItem(info)
                self.values[x].setCurrentIndex(self.valuesOfOptionsKeys[self.typesOfValues[x][1]].index(Universals.MySettings[keyValue]))
                MObject.connect(self.values[x], SIGNAL("currentIndexChanged(int)"), self.valueChanged)
            elif self.typesOfValues[x]=="Yes/No":
                self.values.append(MComboBox())
                self.values[x].addItems([translate("QuickOptions", "No"),translate("QuickOptions", "Yes")])
                if Universals.getBoolValue(keyValue):
                    self.values[x].setCurrentIndex(1)
                MObject.connect(self.values[x], SIGNAL("currentIndexChanged(int)"), self.valueChanged)
            self.values[x].setToolTip(self.toolTips[x])
            lblLabel = MLabel(self.labels[x]+u" : ")
            lblLabel.setToolTip(self.toolTips[x])
            wactLabel = MWidgetAction(self)
            wactLabel.setDefaultWidget(lblLabel)
            wact = MWidgetAction(self)
            wact.setDefaultWidget(self.values[x])
            self.addAction(wactLabel)
            self.addAction(wact)
        
    def valueChanged(self, _value):
        try:
            indexNo = self.values.index(self.sender())
            selectedValue = None
            if self.typesOfValues[indexNo] =="Yes/No":
                if self.values[indexNo].currentIndex()==0:
                    selectedValue = False
                else:
                    selectedValue = True
            elif self.typesOfValues[indexNo][0] =="options":
                selectedValue = self.valuesOfOptionsKeys[self.typesOfValues[indexNo][1]][self.values[indexNo].currentIndex()]
            Universals.setMySetting(self.keysOfSettings[indexNo], selectedValue)
        except:
            error = ReportBug.ReportBug()
            error.show()
        
    