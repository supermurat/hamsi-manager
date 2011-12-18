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

class FileTable():
    def __init__(self, _table):
        self.Table = _table
        self.keyName = "file"
        self.hiddenTableColumnsSettingKey = "hiddenFileTableColumns"
        self.refreshColumns()
        if Universals.isActiveAmarok:
            self.cckbChangeInAmarokDB = Options.MyCheckBox(_table, translate("FileTable", "Change In Amarok"), None, "isFileTableValuesChangeInAmarokDB")
            self.cckbChangeInAmarokDB.setToolTip(translate("FileTable", "Are you want to change file paths in Amarok database?"))
            self.Table.hblBox.insertWidget(self.Table.hblBox.count()-2, self.cckbChangeInAmarokDB)
        
    def readContents(self, _directoryPath):
        currentTableContentValues = []
        fileNames = InputOutputs.readDirectory(_directoryPath, "file", Universals.getBoolValue("isShowHiddensInFileTable"))
        allItemNumber = len(fileNames)
        Universals.startThreadAction()
        baseNameOfDirectory = InputOutputs.getBaseName(_directoryPath)
        for fileNo,fileName in enumerate(fileNames):
            isContinueThreadAction = Universals.isContinueThreadAction()
            if isContinueThreadAction:
                if InputOutputs.isReadableFileOrDir(InputOutputs.joinPath(_directoryPath, fileName), False, True):
                    content = {}
                    content["path"] = InputOutputs.joinPath(_directoryPath, fileName)
                    content["baseNameOfDirectory"] = baseNameOfDirectory
                    content["baseName"] = fileName
                    currentTableContentValues.append(content)
            else:
                allItemNumber = fileNo+1
            Dialogs.showState(translate("InputOutputs/Files", "Reading File Informations"),fileNo+1,allItemNumber, True) 
            if isContinueThreadAction==False:
                break
        Universals.finishThreadAction()
        return currentTableContentValues
    
    def writeContents(self):
        self.Table.changedValueNumber = 0
        changingFileDirectories=[]
        if Universals.isActiveAmarok and Universals.getBoolValue("isFileTableValuesChangeInAmarokDB"):
            import Amarok
            if Amarok.checkAmarok(True, False) == False:
                return False
        Universals.startThreadAction()
        allItemNumber = len(self.Table.currentTableContentValues)
        Dialogs.showState(translate("InputOutputs/Files", "Writing File Informations"),0,allItemNumber, True)
        for rowNo in range(self.Table.rowCount()):
            isContinueThreadAction = Universals.isContinueThreadAction()
            if isContinueThreadAction:
                if InputOutputs.isWritableFileOrDir(self.Table.currentTableContentValues[rowNo]["path"], False, True):
                    if self.Table.isRowHidden(rowNo):
                        InputOutputs.removeFileOrDir(self.Table.currentTableContentValues[rowNo]["path"])
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
                    newFilePath = InputOutputs.joinPath(InputOutputs.getDirName(InputOutputs.getDirName(self.Table.currentTableContentValues[rowNo]["path"])), baseNameOfDirectory, baseName)
                    if InputOutputs.getRealPath(self.Table.currentTableContentValues[rowNo]["path"]) != InputOutputs.getRealPath(newFilePath):
                        changingFileDirectories.append([self.Table.currentTableContentValues[rowNo]["path"], 
                                                        newFilePath])
            else:
                allItemNumber = rowNo+1
            Dialogs.showState(translate("InputOutputs/Files", "Writing File Informations"),rowNo+1,allItemNumber, True)
            if isContinueThreadAction==False:
                break
        Universals.finishThreadAction()
        pathValues = InputOutputs.changeDirectories(changingFileDirectories)
        if Universals.isActiveAmarok and Universals.getBoolValue("isFileTableValuesChangeInAmarokDB"):
            import Amarok
            from Amarok import Operations
            Operations.changePaths(pathValues, "file")
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
            Dialogs.showError(translate("FileTable", "Cannot Open File"), 
                        str(translate("FileTable", "\"%s\" : cannot be opened. Please make sure that you selected a text file.")
                        ) % Organizer.getLink(self.Table.currentTableContentValues[_row]["path"]))
       
    def refreshColumns(self):
        self.Table.tableColumns=[translate("FileTable", "Directory"), 
                            translate("FileTable", "File Name")]
        self.Table.tableColumnsKey=["Directory", "File Name"]
        
    def save(self):
        self.Table.checkFileExtensions(1, "baseName")
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
                    newString = Organizer.emend(self.Table.currentTableContentValues[rowNo]["baseName"], "file")
                    item = self.Table.createTableWidgetItem(newString, self.Table.currentTableContentValues[rowNo]["baseName"])
                if item!=None:
                    self.Table.setItem(rowNo, itemNo, item)
                    
    def correctTable(self):
        for rowNo in range(self.Table.rowCount()):
            for itemNo in range(self.Table.columnCount()):
                if itemNo==0:
                    newString = Organizer.emend(str(self.Table.item(rowNo,itemNo).text()), "directory")
                else:
                    newString = Organizer.emend(str(self.Table.item(rowNo,itemNo).text()), "file")
                self.Table.item(rowNo,itemNo).setText(trForUI(newString))
          
