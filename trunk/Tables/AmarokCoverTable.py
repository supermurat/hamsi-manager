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


import Organizer
import InputOutputs
from MyObjects import *
from Details import CoverDetails
import Dialogs
from time import gmtime
import Universals

class AmarokCoverTable():
    def __init__(self, _table):
        self.Table = _table
        self.keyName = "cover"
        self.hiddenTableColumnsSettingKey = "hiddenAmarokCoverTableColumns"
        self.refreshColumns()
        
    def readContents(self, _directoryPath):
        currentTableContentValues = []
        Universals.startThreadAction()
        import Amarok
        Dialogs.showState(translate("AmarokCoverTable", "Checking For Amarok..."), 0, 2)
        if Amarok.checkAmarok():
            Dialogs.showState(translate("AmarokCoverTable", "Getting Values From Amarok"), 1, 2)
            isContinueThreadAction = Universals.isContinueThreadAction()
            if isContinueThreadAction:
                from Amarok import Operations
                directoriesAndValues = Operations.getDirectoriesAndValues()
                Dialogs.showState(translate("AmarokCoverTable", "Values Are Being Processed"), 2, 2)
                isContinueThreadAction = Universals.isContinueThreadAction()
                if isContinueThreadAction:
                    if directoriesAndValues!=None:
                        allItemNumber = len(directoriesAndValues)
                        dirNo = 0
                        for dirPath,dirRow in directoriesAndValues.items():
                            isContinueThreadAction = Universals.isContinueThreadAction()
                            if isContinueThreadAction:
                                if InputOutputs.IA.isReadableFileOrDir(dirPath):
                                    content = {}
                                    content["path"] = dirPath
                                    content["pathOfParentDirectory"] = InputOutputs.IA.getDirName(dirPath)
                                    content["baseName"] = InputOutputs.IA.getBaseName(dirPath)
                                    currentCover, isCorrectedFileContent = InputOutputs.IA.getIconFromDirectory(dirPath)
                                    if currentCover==None:
                                        currentCover = ""
                                    content["currentCover"] = (currentCover)
                                    content["sourceCover"] = (dirRow["coverPath"][0].replace(dirPath, "."))
                                    content["destinationCover"] = ("./" + Organizer.getIconName(
                                                            dirRow["artist"][0], 
                                                            dirRow["album"][0], 
                                                            dirRow["genre"][0], 
                                                            dirRow["year"][0]))
                                    content["flagColor"] = {}
                                    if isCorrectedFileContent==False:
                                        content["flagColor"]["currentCover"] = 255,163,163
                                    if InputOutputs.isFile(content["sourceCover"])==False:
                                        content["flagColor"]["sourceCover"] = 255,163,163
                                    currentTableContentValues.append(content)
                            else:
                                allItemNumber = dirNo+1
                            Dialogs.showState(translate("InputOutputs/Covers", "Reading Cover Informations"),
                                              dirNo+1,allItemNumber, True) 
                            dirNo += 1
                            if isContinueThreadAction==False:
                                break
        Universals.finishThreadAction()
        return currentTableContentValues
    
    def writeContents(self):
        self.Table.changedValueNumber = 0
        changingFileDirectories=[]
        startRowNo,rowStep=0,1
        Universals.startThreadAction()
        allItemNumber = len(self.Table.currentTableContentValues)
        Dialogs.showState(translate("InputOutputs/Covers", "Writing Cover Informations"),0,allItemNumber, True)
        for rowNo in range(startRowNo,self.Table.rowCount(),rowStep):
            isContinueThreadAction = Universals.isContinueThreadAction()
            if isContinueThreadAction:
                if InputOutputs.IA.isWritableFileOrDir(self.Table.currentTableContentValues[rowNo]["path"]):
                    if self.Table.isRowHidden(rowNo):
                        InputOutputs.IA.removeFileOrDir(self.Table.currentTableContentValues[rowNo]["path"])
                        self.Table.changedValueNumber += 1
                        continue
                    pathOfParentDirectory = str(self.Table.currentTableContentValues[rowNo]["pathOfParentDirectory"])
                    baseName = str(self.Table.currentTableContentValues[rowNo]["baseName"])
                    if self.Table.isChangableItem(rowNo, 3) or self.Table.isChangableItem(rowNo, 4):
                        sourcePath = self.Table.currentTableContentValues[rowNo]["sourceCover"]
                        destinationPath = self.Table.currentTableContentValues[rowNo]["destinationCover"]
                        if self.Table.isChangableItem(rowNo, 3):
                            sourcePath = str(self.Table.item(rowNo,3).text()).strip()
                        if self.Table.isChangableItem(rowNo, 4):
                            destinationPath = str(self.Table.item(rowNo,4).text()).strip()
                        if (str(self.Table.item(rowNo,2).text())!=sourcePath or sourcePath!=destinationPath or str(self.Table.item(rowNo,2).text())!=destinationPath) or (str(self.Table.item(rowNo,2).text())!=self.Table.currentTableContentValues[rowNo]["currentCover"] and (str(self.Table.item(rowNo,2).text())!=sourcePath and str(self.Table.item(rowNo,2).text())!=destinationPath)):
                            if str(self.Table.item(rowNo,3).text()).strip()!="":
                                sourcePath = InputOutputs.IA.getRealPath(sourcePath, self.Table.currentTableContentValues[rowNo]["path"])
                                if InputOutputs.IA.checkSource(sourcePath, "file"):
                                    if destinationPath!="":
                                        destinationPath = InputOutputs.IA.getRealPath(destinationPath, self.Table.currentTableContentValues[rowNo]["path"])
                                        if sourcePath!=destinationPath:
                                            destinationPath = InputOutputs.IA.moveOrChange(sourcePath, destinationPath)
                                    else:
                                        destinationPath = sourcePath
                                    InputOutputs.IA.setIconToDirectory(self.Table.currentTableContentValues[rowNo]["path"], destinationPath)
                                    self.Table.changedValueNumber += 1
                            else:
                                InputOutputs.IA.setIconToDirectory(self.Table.currentTableContentValues[rowNo]["path"], "")
                                self.Table.changedValueNumber += 1
                    if self.Table.isChangableItem(rowNo, 0, pathOfParentDirectory):
                        pathOfParentDirectory = str(self.Table.item(rowNo,0).text())
                        self.Table.changedValueNumber += 1
                    if self.Table.isChangableItem(rowNo, 1, baseName, False):
                        baseName = str(self.Table.item(rowNo,1).text())
                        self.Table.changedValueNumber += 1
                    newFilePath = pathOfParentDirectory + "/" + baseName
                    if InputOutputs.getRealPath(self.Table.currentTableContentValues[rowNo]["path"]) != InputOutputs.getRealPath(newFilePath):
                        changingFileDirectories.append([self.Table.currentTableContentValues[rowNo]["path"], 
                                                        newFilePath])
            else:
                allItemNumber = rowNo+1
            Dialogs.showState(translate("InputOutputs/Covers", "Writing Cover Informations"),rowNo+1,allItemNumber, True)
            if isContinueThreadAction==False:
                break
        Universals.finishThreadAction()
        pathValues = InputOutputs.IA.changeDirectories(changingFileDirectories)
        from Amarok import Operations
        Operations.changePaths(pathValues)
        return True
        
    def showDetails(self, _fileNo, _infoNo):
        directoryPathOfCover = self.Table.currentTableContentValues[_fileNo]["path"]
        coverValues = [directoryPathOfCover, 
                       InputOutputs.IA.getRealPath(str(self.Table.item(_fileNo, 2).text()), directoryPathOfCover), 
                       InputOutputs.IA.getRealPath(str(self.Table.item(_fileNo, 3).text()), directoryPathOfCover), 
                       InputOutputs.IA.getRealPath(str(self.Table.item(_fileNo, 4).text()), directoryPathOfCover)]
        CoverDetails.CoverDetails(coverValues, self.Table.isOpenDetailsOnNewWindow.isChecked(), _infoNo)
        
    def cellClicked(self,_row,_column):
        cellLenght = len(self.Table.currentItem().text())*8
        if cellLenght>self.Table.columnWidth(_column):
            self.Table.setColumnWidth(_column,cellLenght)
    
    def cellDoubleClicked(self,_row,_column):
        try:
            if self.Table.tbIsRunOnDoubleClick.isChecked()==True:
                self.showDetails(_row, _column)
        except:
            Dialogs.showError(translate("AmarokCoverTable", "Cannot Open File"), 
                        str(translate("AmarokCoverTable", "\"%s\" : cannot be opened. Please make sure that you selected a text file.")
                        ) % Organizer.getLink(self.Table.currentTableContentValues[_row]["path"]))
       
    def refreshColumns(self):
        self.Table.tableColumns=[translate("AmarokCoverTable", "Directory"), 
                            translate("AmarokCoverTable", "Directory Name"), 
                            translate("AmarokCoverTable", "Current Cover"), 
                            translate("AmarokCoverTable", "Source Cover"), 
                            translate("AmarokCoverTable", "Destination Cover")]
        self.Table.tableColumnsKey=["Directory", "Directory Name", "Current Cover", "Source Cover", "Destination Cover"]
        
    def save(self):
        self.Table.checkFileExtensions(4, 3)
        return self.writeContents()
        
    def refresh(self, _path):
        self.Table.currentTableContentValues = self.readContents(_path)
        self.Table.setRowCount(len(self.Table.currentTableContentValues))
        for rowNo in range(self.Table.rowCount()):
            for itemNo in range(5):
                item = None
                if itemNo==0:
                    newString = Organizer.emend(self.Table.currentTableContentValues[rowNo]["pathOfParentDirectory"], "directory")
                    item = self.Table.createTableWidgetItem(newString, self.Table.currentTableContentValues[rowNo]["pathOfParentDirectory"])
                elif itemNo==1:
                    newString = Organizer.emend(self.Table.currentTableContentValues[rowNo]["baseName"], "directory")
                    item = self.Table.createTableWidgetItem(newString, self.Table.currentTableContentValues[rowNo]["baseName"])
                elif itemNo==2:
                    newString = InputOutputs.getShortPath(self.Table.currentTableContentValues[rowNo]["currentCover"], self.Table.currentTableContentValues[rowNo]["path"])
                    item = self.Table.createTableWidgetItem(newString)
                    self.setItemColor(item, rowNo, itemNo, "currentCover")
                elif itemNo==3:
                    newString = InputOutputs.getShortPath(self.Table.currentTableContentValues[rowNo]["sourceCover"], self.Table.currentTableContentValues[rowNo]["path"])
                    item = self.Table.createTableWidgetItem(newString, InputOutputs.getShortPath(self.Table.currentTableContentValues[rowNo]["currentCover"], self.Table.currentTableContentValues[rowNo]["path"]))
                    self.setItemColor(item, rowNo, itemNo, "sourceCover")
                elif itemNo==4:
                    newString = Organizer.emend(InputOutputs.getShortPath(self.Table.currentTableContentValues[rowNo]["destinationCover"], self.Table.currentTableContentValues[rowNo]["path"]), "file")
                    item = self.Table.createTableWidgetItem(newString, InputOutputs.getShortPath(self.Table.currentTableContentValues[rowNo]["currentCover"], self.Table.currentTableContentValues[rowNo]["path"]))
                    self.setItemColor(item, rowNo, itemNo, "destinationCover")
                if item!=None:
                    self.Table.setItem(rowNo, itemNo, item)
                    
    def setItemColor(self, _item, _rowNo, _itemNo, _name):
        if _item!=None:
            if _name in self.Table.currentTableContentValues[_rowNo]["flagColor"]:
                r, g, b = self.Table.currentTableContentValues[_rowNo]["flagColor"][_name]
                _item.setBackground(MBrush(MColor(r, g, b)))
                    
    def correctTable(self):
        for rowNo in range(self.Table.rowCount()):
            for itemNo in range(self.Table.columnCount()):
                if itemNo==0 or itemNo==1:
                    newString = Organizer.emend(str(self.Table.item(rowNo,itemNo).text()), "directory")
                elif itemNo==2 or itemNo==3:
                    newString = trForUI(str(self.Table.item(rowNo,itemNo).text()))
                else:
                    newString = Organizer.emend(str(self.Table.item(rowNo,itemNo).text()), "file")
                self.Table.item(rowNo,itemNo).setText(trForUI(newString))



