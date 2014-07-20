## This file is part of HamsiManager.
##
## Copyright (c) 2010 - 2014 Murat Demir <mopened@gmail.com>
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


import sys, os
from Core.MyObjects import *
from Core import Dialogs
from Core import Universals as uni
from Core import Records
import FileUtils as fu
import Databases
from Core import ReportBug


class TableQuickOptions(MMenu):
    def __init__(self, _parent=None):
        MDialog.__init__(self, _parent)
        self.setTitle(translate("MenuBar", "Table Quick Options"))
        self.setObjectName(translate("MenuBar", "Table Quick Options"))
        self.values, self.hiddenKeys = [], []
        self.keysOfSettings = ["isChangeAll", "isChangeSelected",
                               "isRunOnDoubleClick", "isOpenDetailsInNewWindow",
                               "isOpenWithDefaultApplication",
                               "isForceOpenWithDefaultApplication",
                               "isFileTableValuesChangeInAmarokDB",
                               "isFolderTableValuesChangeInAmarokDB",
                               "isMusicTableValuesChangeInAmarokDB",
                               "isSubFolderTableValuesChangeInAmarokDB",
                               "isSubFolderMusicTableValuesChangeInAmarokDB"]
        self.labels = [translate("TableQuickOptions", "Ignore Selection"),
                       translate("TableQuickOptions", "Change Just Selected Cells"),
                       translate("TableQuickOptions", "Show Details On Double Click"),
                       translate("TableQuickOptions", "Show Details In New Window"),
                       translate("TableQuickOptions", "Open With Default Application"),
                       translate("TableQuickOptions", "Force To Open With Default Application"),
                       translate("TableQuickOptions", "Change In Amarok"),
                       translate("TableQuickOptions", "Change In Amarok"),
                       translate("TableQuickOptions", "Change In Amarok"),
                       translate("TableQuickOptions", "Change In Amarok"),
                       translate("TableQuickOptions", "Change In Amarok")]
        self.toolTips = [translate("TableQuickOptions", "Are you want to change all cells?"),
                         translate("TableQuickOptions", "Are you want to change just selected cells?"),
                         translate("TableQuickOptions", "Are you want to open details on double click?"),
                         translate("TableQuickOptions", "Are you want to open details in new window?"),
                         translate("TableQuickOptions",
                                   "Are you want to open selected files and directories (Which are not supported by Hamsi Manager) with default application?"),
                         translate("TableQuickOptions",
                                   "Are you want to force to open selected files and directories with default application instead of Hamsi Manager`s Details Window?"),
                         translate("TableQuickOptions", "Are you want to change file paths in Amarok database?"),
                         translate("TableQuickOptions",
                                   "Are you want to change file and directory paths in Amarok database?"),
                         translate("TableQuickOptions",
                                   "Are you want to change file paths and tags in Amarok database?"),
                         translate("TableQuickOptions", "Are you want to change file paths in Amarok database?"),
                         translate("TableQuickOptions",
                                   "Are you want to change file paths and tags in Amarok database?")]
        self.typesOfValues = ["Yes/No", "Yes/No", "Yes/No", "Yes/No", "Yes/No", "Yes/No", "Yes/No", "Yes/No", "Yes/No",
                              "Yes/No", "Yes/No"]
        self.valuesOfOptions = []
        self.valuesOfOptionsKeys = []
        if uni.isActiveAmarok is False:
            self.hiddenKeys += ["isFileTableValuesChangeInAmarokDB",
                                "isFolderTableValuesChangeInAmarokDB",
                                "isMusicTableValuesChangeInAmarokDB",
                                "isSubFolderTableValuesChangeInAmarokDB"]
        else:
            if uni.tableType == "0":
                self.hiddenKeys = ["isFileTableValuesChangeInAmarokDB",
                                   "isMusicTableValuesChangeInAmarokDB",
                                   "isSubFolderTableValuesChangeInAmarokDB",
                                   "isSubFolderMusicTableValuesChangeInAmarokDB"]
            elif uni.tableType == "1":
                self.hiddenKeys = ["isFolderTableValuesChangeInAmarokDB",
                                   "isMusicTableValuesChangeInAmarokDB",
                                   "isSubFolderTableValuesChangeInAmarokDB",
                                   "isSubFolderMusicTableValuesChangeInAmarokDB"]
            elif uni.tableType == "2":
                self.hiddenKeys = ["isFileTableValuesChangeInAmarokDB",
                                   "isFolderTableValuesChangeInAmarokDB",
                                   "isSubFolderTableValuesChangeInAmarokDB",
                                   "isSubFolderMusicTableValuesChangeInAmarokDB"]
            elif uni.tableType == "3":
                self.hiddenKeys = ["isFileTableValuesChangeInAmarokDB",
                                   "isFolderTableValuesChangeInAmarokDB",
                                   "isMusicTableValuesChangeInAmarokDB",
                                   "isSubFolderMusicTableValuesChangeInAmarokDB"]
            elif uni.tableType == "9":
                self.hiddenKeys = ["isFileTableValuesChangeInAmarokDB",
                                   "isFolderTableValuesChangeInAmarokDB",
                                   "isMusicTableValuesChangeInAmarokDB",
                                   "isSubFolderTableValuesChangeInAmarokDB"]
            else:
                self.hiddenKeys = ["isFileTableValuesChangeInAmarokDB",
                                   "isFolderTableValuesChangeInAmarokDB",
                                   "isMusicTableValuesChangeInAmarokDB",
                                   "isSubFolderTableValuesChangeInAmarokDB",
                                   "isSubFolderMusicTableValuesChangeInAmarokDB"]
        self.createActions()
        self.checkEnableStates()

    def checkEnableStates(self):
        if uni.getBoolValue("isForceOpenWithDefaultApplication"):
            actED = self.getActionByKey("isOpenDetailsInNewWindow")
            if actED is not None:
                actED.setEnabled(False)
            actED = self.getActionByKey("isOpenWithDefaultApplication")
            if actED is not None:
                actED.setEnabled(False)
        else:
            actED = self.getActionByKey("isOpenDetailsInNewWindow")
            if actED is not None:
                actED.setEnabled(True)
            actED = self.getActionByKey("isOpenWithDefaultApplication")
            if actED is not None:
                actED.setEnabled(True)
        if uni.getBoolValue("isChangeAll"):
            actED = self.getActionByKey("isChangeSelected")
            if actED is not None:
                actED.setEnabled(False)
        else:
            actED = self.getActionByKey("isChangeSelected")
            if actED is not None:
                actED.setEnabled(True)

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
            getMainWindow().StatusBar.fillSelectionInfo()
            if getMainWindow().Table is not None:
                getMainWindow().Table.fillSelectionInfo()
        except:
            ReportBug.ReportBug()
        
    
