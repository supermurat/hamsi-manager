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


from Core import Organizer
import InputOutputs
from Core.MyObjects import *
from Details import TextDetails
from Core import Dialogs
import Options
from time import gmtime
from Core import Universals

class FolderTable():
    def __init__(self, _table):
        self.Table = _table
        self.keyName = "directory"
        self.hiddenTableColumnsSettingKey = "hiddenFolderTableColumns"
        self.refreshColumns()
        self.cckbChangeInAmarokDB = Options.MyCheckBox(_table, translate("FolderTable", "Change In Amarok"), None, "isFolderTableValuesChangeInAmarokDB")
        self.cckbChangeInAmarokDB.setToolTip(translate("FolderTable", "Are you want to change file and directory paths in Amarok database?"))
        self.Table.hblBox.insertWidget(self.Table.hblBox.count()-2, self.cckbChangeInAmarokDB)
        
    def readContents(self, _directoryPath):
        currentTableContentValues = []
        fileAndDirectoryNames = InputOutputs.IA.readDirectory(_directoryPath, "fileAndDirectory", Universals.getBoolValue("isShowHiddensInFolderTable"))
        allItemNumber = len(fileAndDirectoryNames)
        Universals.startThreadAction()
        baseNameOfDirectory = InputOutputs.getBaseName(_directoryPath)
        for dirNo,dirName in enumerate(fileAndDirectoryNames):
            isContinueThreadAction = Universals.isContinueThreadAction()
            if isContinueThreadAction:
                if InputOutputs.IA.isReadableFileOrDir(_directoryPath + "/" + dirName, False, True):
                    content = {}
                    content["path"] = _directoryPath + "/" + dirName
                    content["baseNameOfDirectory"] = baseNameOfDirectory
                    content["baseName"] = dirName
                    currentTableContentValues.append(content)
            else:
                allItemNumber = dirNo+1
            Dialogs.showState(translate("InputOutputs/Folders", "Reading Directory Informations"),dirNo+1,allItemNumber, True) 
            if isContinueThreadAction==False:
                break
        Universals.finishThreadAction()
        return currentTableContentValues
    
    def writeContents(self):
        self.Table.changedValueNumber = 0
        changingFileDirectories=[]
        Universals.startThreadAction()
        if Universals.getBoolValue("isFolderTableValuesChangeInAmarokDB"):
            import Amarok
            if Amarok.checkAmarok(True, False) == False:
                return False
        allItemNumber = len(self.Table.currentTableContentValues)
        Dialogs.showState(translate("InputOutputs/Folders", "Writing Directory Informations"),0,allItemNumber, True)
        for rowNo in range(self.Table.rowCount()):
            isContinueThreadAction = Universals.isContinueThreadAction()
            if isContinueThreadAction:
                if InputOutputs.IA.isWritableFileOrDir(self.Table.currentTableContentValues[rowNo]["path"], False, True):
                    if self.Table.isRowHidden(rowNo):
                        InputOutputs.IA.removeFileOrDir(self.Table.currentTableContentValues[rowNo]["path"], True)
                        self.Table.changedValueNumber += 1
                        continue
                    baseNameOfDirectory = str(self.Table.currentTableContentValues[rowNo]["baseNameOfDirectory"])
                    baseName = str(self.Table.currentTableContentValues[rowNo]["baseName"])
                    if self.Table.isChangableItem(rowNo, 0, baseNameOfDirectory):
                        baseNameOfDirectory = str(self.Table.item(rowNo,0).text())
                        self.Table.changedValueNumber += 1
                    if self.Table.isChangableItem(rowNo, 1, baseName, False):
                        baseName = str(self.Table.item(rowNo,1).text())
                        self.Table.changedValueNumber += 1
                    newFilePath = InputOutputs.getDirName(InputOutputs.getDirName(self.Table.currentTableContentValues[rowNo]["path"])) + "/" + baseNameOfDirectory + "/" + baseName
                    if InputOutputs.getRealPath(self.Table.currentTableContentValues[rowNo]["path"]) != InputOutputs.getRealPath(newFilePath):
                        changingFileDirectories.append([self.Table.currentTableContentValues[rowNo]["path"], 
                                                        newFilePath])
            else:
                allItemNumber = rowNo+1
            Dialogs.showState(translate("InputOutputs/Folders", "Writing Directory Informations"),rowNo+1,allItemNumber, True)
            if isContinueThreadAction==False:
                break
        Universals.finishThreadAction()
        pathValues = InputOutputs.IA.changeDirectories(changingFileDirectories)
        if Universals.getBoolValue("isFolderTableValuesChangeInAmarokDB"):
            import Amarok
            from Amarok import Operations
            Operations.changePaths(pathValues)
        return True
        
    def showDetails(self, _fileNo, _infoNo):
        TextDetails.TextDetails(self.Table.currentTableContentValues[_fileNo]["path"],self.Table.isOpenDetailsOnNewWindow.isChecked())
    
    def cellClicked(self,_row,_column):
        cellLenght = len(self.Table.currentItem().text())*8
        if cellLenght>self.Table.columnWidth(_column):
            self.Table.setColumnWidth(_column,cellLenght)
        
    def cellDoubleClicked(self,_row,_column):
        try:
            if self.Table.tbIsRunOnDoubleClick.isChecked()==True:
                self.showDetails(_row, _column)
        except:
            Dialogs.showError(translate("FolderTable", "Cannot Open File"), 
                        str(translate("FolderTable", "\"%s\" : cannot be opened. Please make sure that you selected a text file.")
                        ) % Organizer.getLink(self.Table.currentTableContentValues[_row]["path"]))
       
    def refreshColumns(self):
        self.Table.tableColumns=[translate("FolderTable", "Directory"), 
                            translate("FolderTable", "File/Directory Name")]
        self.Table.tableColumnsKey=["Directory", "File/Directory Name"]
        
    def save(self):
        self.Table.checkFileExtensions(1, "baseName", True)
        return self.writeContents()
    
    def refresh(self, _path):
        self.Table.currentTableContentValues = self.readContents(_path)
        self.Table.setRowCount(len(self.Table.currentTableContentValues))
        for rowNo in range(self.Table.rowCount()):
            for itemNo in range(2):
                item = None
                if itemNo==0:
                    newString = Organizer.emend(self.Table.currentTableContentValues[rowNo]["baseNameOfDirectory"], "directory")
                    item = self.Table.createTableWidgetItem(newString, self.Table.currentTableContentValues[rowNo]["baseNameOfDirectory"])
                elif itemNo==1:
                    newString = Organizer.emend(self.Table.currentTableContentValues[rowNo]["baseName"], InputOutputs.getObjectType(self.Table.currentTableContentValues[rowNo]["path"]))
                    item = self.Table.createTableWidgetItem(newString, self.Table.currentTableContentValues[rowNo]["baseName"])
                if item!=None:
                    self.Table.setItem(rowNo, itemNo, item)
                    
    def correctTable(self):
        for rowNo in range(self.Table.rowCount()):
            for itemNo in range(self.Table.columnCount()):
                if itemNo==0:
                    newString = Organizer.emend(str(self.Table.item(rowNo,itemNo).text()), "directory")
                else:
                    newString = Organizer.emend(str(self.Table.item(rowNo,itemNo).text()), InputOutputs.IA.getObjectType(self.Table.currentTableContentValues[rowNo]["path"]))
                self.Table.item(rowNo,itemNo).setText(trForUI(newString))
          
