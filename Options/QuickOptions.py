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


import sys, os
from Core.MyObjects import *
from Core import Dialogs
from Core import Universals as uni
from Core import Records
import FileUtils as fu
import Databases
from Core import ReportBug


class QuickOptions(MMenu):
    def __init__(self, _parent=None):
        MDialog.__init__(self, _parent)
        self.setTitle(translate("MenuBar", "Quick Options"))
        self.setObjectName(translate("MenuBar", "Quick Options"))
        self.values, self.hiddenKeys = [], []
        self.keysOfSettings = ["isActiveCompleter", "isActiveClearGeneral", "isClearEmptyDirectoriesWhenSave",
                               "isAutoCleanSubFolderWhenSave",
                               "isActiveAutoMakeIconToDirectory",
                               "validSentenceStructure", "validSentenceStructureForFile",
                               "validSentenceStructureForDirectory",
                               "validSentenceStructureForFileExtension", "fileExtensionIs",
                               "isEmendIncorrectChars", "isCorrectFileNameWithSearchAndReplaceTable",
                               "isCorrectValueWithSearchAndReplaceTable", "isDecodeURLStrings",
                               "isClearFirstAndLastSpaceChars", "isCorrectDoubleSpaceChars",
                               "isShowHiddensInSubFolderTable", "isShowHiddensInFolderTable",
                               "isShowHiddensInFileTable",
                               "isShowHiddensInMusicTable", "isShowHiddensInCoverTable",
                               "isShowHiddensInSubFolderMusicTable"]
        self.labels = [translate("Options/Correct", "Use Completer"),
                       translate("QuickOptions", "Activate General Cleaner"),
                       translate("Options/ClearGeneral", "General Cleaning (Table Saved)"),
                       translate("Options/ClearGeneral", "Clean Subfolders (Table Saved)"),
                       translate("QuickOptions", "Auto Change Directory Icon"),
                       translate("QuickOptions", "Valid Sentence Structure"),
                       translate("QuickOptions", "Valid Sentence Structure For Files"),
                       translate("QuickOptions", "Valid Sentence Structure For Directories"),
                       translate("QuickOptions", "Valid Sentence Structure For File Extensions"),
                       translate("QuickOptions", "Which Part Is The File Extension"),
                       translate("QuickOptions", "Emend Incorrect Chars"),
                       translate("QuickOptions", "Correct File Name By Search Table"),
                       translate("QuickOptions", "Correct Values By Search Table"),
                       translate("QuickOptions", "Decode URL Strings"),
                       translate("QuickOptions", "Clear First And Last Space Chars"),
                       translate("QuickOptions", "Correct Double Space Chars"),
                       translate("Options/HiddenObjects", "Show Hidden Files And Directories"),
                       translate("Options/HiddenObjects", "Show Hidden Files And Directories"),
                       translate("Options/HiddenObjects", "Show Hidden Files"),
                       translate("Options/HiddenObjects", "Show Hidden Files"),
                       translate("Options/HiddenObjects", "Show Hidden Directories"),
                       translate("Options/HiddenObjects", "Show Hidden Files")]
        self.toolTips = [
            translate("Options/Correct", "Are you want to activate completer for auto complete some input controls?"),
            translate("QuickOptions", "Are you want to activate General Cleaner?"),
            translate("Options/ClearGeneral", "Do you want to general cleaning when table saved?"),
            translate("Options/ClearGeneral", "Do you want to clear the subfolders when table saved?"),
            translate("QuickOptions", "Are you want to change directory icon automatically?"),
            translate("QuickOptions",
                      "All information (Artist name,title etc.) will be changed automatically to the format you selected."),
            translate("QuickOptions", "File names will be changed automatically to the format you selected."),
            translate("QuickOptions", "Directory names will be changed automatically to the format you selected."),
            translate("QuickOptions", "File extensions will be changed automatically to the format you selected."),
            translate("QuickOptions", "Which part of the filename is the file extension?"),
            translate("QuickOptions", "Are you want to emend incorrect chars?"),
            translate("QuickOptions", "Are you want to correct file and directory names by search and replace table?"),
            translate("QuickOptions", "Are you want to correct values by search and replace table?"),
            translate("QuickOptions",
                      "Are you want to decode URL strings? ( For Example : '%20' >>> ' ', '%26' >>> '&' ) "),
            translate("QuickOptions", "Are you want to clear first and last space chars?"),
            translate("QuickOptions", "Are you want to correct double space chars?"),
            translate("Options/HiddenObjects", "Are you want to show hidden files and directories in subfolder table?"),
            translate("Options/HiddenObjects",  "Are you want to show hidden files and directories in folder table?"),
            translate("Options/HiddenObjects", "Are you want to show hidden files in file table?"),
            translate("Options/HiddenObjects", "Are you want to show hidden files in music table?"),
            translate("Options/HiddenObjects", "Are you want to show hidden directories in cover table?"),
            translate("Options/HiddenObjects", "Are you want to show hidden files in subfolder music table?")]
        self.typesOfValues = ["Yes/No", "Yes/No", "Yes/No", "Yes/No", "Yes/No",
                              ["options", 0], ["options", 0], ["options", 0], ["options", 0],
                              ["options", 1], "Yes/No", "Yes/No", "Yes/No", "Yes/No", "Yes/No", "Yes/No",
                              "Yes/No", "Yes/No", "Yes/No", "Yes/No", "Yes/No", "Yes/No"]
        self.valuesOfOptions = [[translate("QuickOptions", "Title"),
                                 translate("QuickOptions", "All Small"),
                                 translate("QuickOptions", "All Caps"),
                                 translate("QuickOptions", "Sentence"),
                                 translate("QuickOptions", "Don`t Change")],
                                [translate("QuickOptions", "After The First Point"),
                                 translate("QuickOptions", "After The Last Point"),
                                 translate("Options/Correct", "Be Smart")]]
        self.valuesOfOptionsKeys = [uni.validSentenceStructureKeys,
                                    uni.fileExtensionIsKeys]
        if uni.tableType == "0":
            self.hiddenKeys = ["isShowHiddensInSubFolderTable", "isShowHiddensInFileTable",
                               "isShowHiddensInMusicTable", "isShowHiddensInCoverTable",
                               "isCorrectValueWithSearchAndReplaceTable", "isShowHiddensInSubFolderMusicTable"]
        elif uni.tableType == "1":
            self.hiddenKeys = ["isShowHiddensInSubFolderTable", "isShowHiddensInFolderTable",
                               "isShowHiddensInMusicTable", "isShowHiddensInCoverTable",
                               "isCorrectValueWithSearchAndReplaceTable", "isShowHiddensInSubFolderMusicTable"]
        elif uni.tableType == "2":
            self.hiddenKeys = ["isShowHiddensInSubFolderTable", "isShowHiddensInFolderTable",
                               "isShowHiddensInFileTable", "isShowHiddensInCoverTable",
                               "isShowHiddensInSubFolderMusicTable"]
        elif uni.tableType == "3":
            self.hiddenKeys = ["isShowHiddensInFolderTable", "isShowHiddensInFileTable",
                               "isShowHiddensInMusicTable", "isShowHiddensInCoverTable",
                               "isCorrectValueWithSearchAndReplaceTable", "isShowHiddensInSubFolderMusicTable"]
        elif uni.tableType == "4":
            self.hiddenKeys = ["isShowHiddensInSubFolderTable", "isShowHiddensInFolderTable",
                               "isShowHiddensInFileTable", "isShowHiddensInMusicTable",
                               "isActiveAutoMakeIconToDirectory",
                               "isCorrectValueWithSearchAndReplaceTable", "isShowHiddensInSubFolderMusicTable"]
        elif uni.tableType == "9":
            self.hiddenKeys = ["isShowHiddensInSubFolderTable", "isShowHiddensInMusicTable",
                               "isShowHiddensInFolderTable",
                               "isShowHiddensInFileTable", "isShowHiddensInCoverTable"]
        else:
            self.hiddenKeys = ["isShowHiddensInSubFolderTable", "isShowHiddensInFolderTable",
                               "isShowHiddensInFileTable",
                               "isShowHiddensInMusicTable", "isShowHiddensInCoverTable",
                               "isShowHiddensInSubFolderMusicTable",
                               "isActiveClearGeneral", "isClearEmptyDirectoriesWhenSave",
                               "isAutoCleanSubFolderWhenSave",
                               "isActiveAutoMakeIconToDirectory"]
        if uni.isActiveDirectoryCover is False:
            self.hiddenKeys += ["isActiveAutoMakeIconToDirectory"]
        self.createActions()
        self.checkEnableStates()

    def checkEnableStates(self):
        if uni.getBoolValue("isActiveClearGeneral"):
            actED = self.getActionByKey("isClearEmptyDirectoriesWhenSave")
            if actED is not None:
                actED.setEnabled(True)
            if uni.getBoolValue("isClearEmptyDirectoriesWhenSave"):
                actSF = self.getActionByKey("isAutoCleanSubFolderWhenSave")
                if actSF is not None:
                    actSF.setEnabled(True)
            else:
                actSF = self.getActionByKey("isAutoCleanSubFolderWhenSave")
                if actSF is not None:
                    actSF.setEnabled(False)
        else:
            actED = self.getActionByKey("isClearEmptyDirectoriesWhenSave")
            if actED is not None:
                actED.setEnabled(False)
            actSF = self.getActionByKey("isAutoCleanSubFolderWhenSave")
            if actSF is not None:
                actSF.setEnabled(False)

    def getActionByKey(self, _key):
        for act in self.values:
            try:
                if str(act.objectName()) == str(_key):
                    return act
            except: pass
        return None

    def createActions(self):
        for x, keyValue in enumerate(self.keysOfSettings):
            if keyValue not in self.hiddenKeys:
                if self.typesOfValues[x][0] == "options":
                    actionLabelList = self.valuesOfOptions[self.typesOfValues[x][1]]
                    selectedIndex = self.valuesOfOptionsKeys[self.typesOfValues[x][1]].index(uni.MySettings[keyValue])
                    self.values.append(MMenu(self.labels[x], self))
                    actgActionGroupTableTypes = MActionGroup(self.values[-1])
                    for y, actionLabel in enumerate(actionLabelList):
                        actAction = actgActionGroupTableTypes.addAction(actionLabel)
                        actAction.setCheckable(True)
                        actAction.setObjectName(str(self.keysOfSettings[x] + ";" + str(y)))
                        if selectedIndex == y:
                            actAction.setChecked(True)
                    self.values[-1].addActions(actgActionGroupTableTypes.actions())
                    self.addAction(self.values[-1].menuAction())
                    MObject.connect(actgActionGroupTableTypes, SIGNAL("selected(QAction *)"), self.valueChanged)
                elif self.typesOfValues[x] == "Yes/No":
                    self.values.append(MAction(self.labels[x], self))
                    self.values[-1].setCheckable(True)
                    self.values[-1].setChecked(uni.getBoolValue(keyValue))
                    self.addAction(self.values[-1])
                    MObject.connect(self.values[-1], SIGNAL("changed()"), self.valueChanged)
                self.values[-1].setObjectName(self.keysOfSettings[x])
                self.values[-1].setToolTip(self.toolTips[x])
                self.values[-1].setStatusTip(self.toolTips[x])
        else:
                self.values.append(None)

    def valueChanged(self, _action=None):
        try:
            senderAction = self.sender()
            if senderAction.parent().objectName() in self.keysOfSettings:
                indexNo = self.keysOfSettings.index(senderAction.parent().objectName())
            else:
                indexNo = self.keysOfSettings.index(senderAction.objectName())
            selectedValue = None
            if self.typesOfValues[indexNo] == "Yes/No":
                if senderAction.isChecked():
                    selectedValue = True
                else:
                    selectedValue = False
            elif self.typesOfValues[indexNo][0] == "options":
                valueIndex = int(_action.objectName().split(";")[1])
                selectedValue = self.valuesOfOptionsKeys[self.typesOfValues[indexNo][1]][valueIndex]
            uni.setMySetting(self.keysOfSettings[indexNo], selectedValue)
            self.checkEnableStates()
        except:
            ReportBug.ReportBug()
        
    
