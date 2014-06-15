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


from Core import Organizer
import FileUtils as fu
from Core.MyObjects import *
from Details import CoverDetails
from Core import Dialogs
from time import gmtime
from Core import Universals
from Core import ReportBug

class AmarokCoverTable():
    def __init__(self, _table):
        from Amarok import Filter
        self.Table = _table
        self.keyName = "cover"
        self.amarokFilterKeyName = "AmarokFilterAmarokCoverTable"
        self.hiddenTableColumnsSettingKey = "hiddenAmarokCoverTableColumns"
        self.refreshColumns()
        self.wFilter = Filter.FilterWidget(self.Table, self.amarokFilterKeyName)
        Universals.MainWindow.MainLayout.addWidget(self.wFilter)
        
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
                directoriesAndValues = Operations.getDirectoriesAndValues(Universals.MySettings[self.amarokFilterKeyName])
                Dialogs.showState(translate("AmarokCoverTable", "Values Are Being Processed"), 2, 2)
                isContinueThreadAction = Universals.isContinueThreadAction()
                if isContinueThreadAction:
                    if directoriesAndValues!=None:
                        allItemNumber = len(directoriesAndValues)
                        dirNo = 0
                        for dirPath,dirRow in directoriesAndValues.items():
                            isContinueThreadAction = Universals.isContinueThreadAction()
                            if isContinueThreadAction:
                                try:
                                    if fu.isReadableFileOrDir(dirPath, False, True) and fu.isReadableFileOrDir(fu.joinPath(dirPath, ".directory"), False, True):
                                        content = {}
                                        content["path"] = dirPath
                                        content["pathOfParentDirectory"] = fu.getDirName(dirPath)
                                        content["baseName"] = fu.getBaseName(dirPath)
                                        currentCover, isCorrectedFileContent = fu.getIconFromDirectory(dirPath)
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
                                        if fu.isFile(content["sourceCover"])==False:
                                            content["flagColor"]["sourceCover"] = 255,163,163
                                        currentTableContentValues.append(content)
                                except:
                                    ReportBug.ReportBug()
                            else:
                                allItemNumber = dirNo+1
                            Dialogs.showState(translate("FileUtils/Covers", "Reading Cover Informations"),
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
        Dialogs.showState(translate("FileUtils/Covers", "Writing Cover Informations"),0,allItemNumber, True)
        for rowNo in range(startRowNo,self.Table.rowCount(),rowStep):
            isContinueThreadAction = Universals.isContinueThreadAction()
            if isContinueThreadAction:
                try:
                    if fu.isWritableFileOrDir(self.Table.currentTableContentValues[rowNo]["path"], False, True):
                        if self.Table.isRowHidden(rowNo):
                            fu.removeFileOrDir(self.Table.currentTableContentValues[rowNo]["path"])
                            self.Table.changedValueNumber += 1
                        else:
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
                                        sourcePath = fu.getRealPath(sourcePath, self.Table.currentTableContentValues[rowNo]["path"])
                                        sourcePath = fu.checkSource(sourcePath, "file")
                                        if sourcePath is not None:
                                            if destinationPath!="":
                                                destinationPath = fu.getRealPath(destinationPath, self.Table.currentTableContentValues[rowNo]["path"])
                                                if sourcePath!=destinationPath:
                                                    destinationPath = fu.moveOrChange(sourcePath, destinationPath)
                                            else:
                                                destinationPath = sourcePath
                                            fu.setIconToDirectory(self.Table.currentTableContentValues[rowNo]["path"], destinationPath)
                                            self.Table.changedValueNumber += 1
                                    else:
                                        fu.setIconToDirectory(self.Table.currentTableContentValues[rowNo]["path"], "")
                                        self.Table.changedValueNumber += 1
                            if self.Table.isChangableItem(rowNo, 0, pathOfParentDirectory):
                                pathOfParentDirectory = str(self.Table.item(rowNo,0).text())
                                self.Table.changedValueNumber += 1
                            if self.Table.isChangableItem(rowNo, 1, baseName, False):
                                baseName = str(self.Table.item(rowNo,1).text())
                                self.Table.changedValueNumber += 1
                            newFilePath = fu.joinPath(pathOfParentDirectory, baseName)
                            if fu.getRealPath(self.Table.currentTableContentValues[rowNo]["path"]) != fu.getRealPath(newFilePath):
                                changingFileDirectories.append([self.Table.currentTableContentValues[rowNo]["path"], 
                                                                newFilePath])
                except:
                    ReportBug.ReportBug()
            else:
                allItemNumber = rowNo+1
            Dialogs.showState(translate("FileUtils/Covers", "Writing Cover Informations"),rowNo+1,allItemNumber, True)
            if isContinueThreadAction==False:
                break
        Universals.finishThreadAction()
        pathValues = fu.changeDirectories(changingFileDirectories)
        from Amarok import Operations
        Operations.changePaths(pathValues)
        return True
        
    def showDetails(self, _fileNo, _infoNo):
        directoryPathOfCover = self.Table.currentTableContentValues[_fileNo]["path"]
        coverValues = [directoryPathOfCover, 
                       fu.getRealPath(str(self.Table.item(_fileNo, 2).text()), directoryPathOfCover),
                       fu.getRealPath(str(self.Table.item(_fileNo, 3).text()), directoryPathOfCover),
                       fu.getRealPath(str(self.Table.item(_fileNo, 4).text()), directoryPathOfCover)]
        CoverDetails.CoverDetails(coverValues, Universals.getBoolValue("isOpenDetailsInNewWindow"), _infoNo)
        
    def cellClicked(self,_row,_column):
        currentItem = self.Table.currentItem()
        if currentItem is not None:
            cellLenght = len(currentItem.text())*8
            if cellLenght>self.Table.columnWidth(_column):
                self.Table.setColumnWidth(_column,cellLenght)
    
    def cellDoubleClicked(self,_row,_column):
        try:
            if Universals.getBoolValue("isRunOnDoubleClick"):
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
        allItemNumber = self.Table.rowCount()
        for rowNo in range(allItemNumber):
            for itemNo in range(5):
                item = None
                if itemNo==0:
                    newString = Organizer.emend(self.Table.currentTableContentValues[rowNo]["pathOfParentDirectory"], "directory")
                    item = self.Table.createTableWidgetItem(newString, self.Table.currentTableContentValues[rowNo]["pathOfParentDirectory"])
                elif itemNo==1:
                    newString = Organizer.emend(self.Table.currentTableContentValues[rowNo]["baseName"], "directory")
                    item = self.Table.createTableWidgetItem(newString, self.Table.currentTableContentValues[rowNo]["baseName"])
                elif itemNo==2:
                    newString = fu.getShortPath(self.Table.currentTableContentValues[rowNo]["currentCover"], self.Table.currentTableContentValues[rowNo]["path"])
                    item = self.Table.createTableWidgetItem(newString, newString, True)
                    self.setItemColor(item, rowNo, itemNo, "currentCover")
                elif itemNo==3:
                    newString = fu.getShortPath(self.Table.currentTableContentValues[rowNo]["sourceCover"], self.Table.currentTableContentValues[rowNo]["path"])
                    item = self.Table.createTableWidgetItem(newString, fu.getShortPath(self.Table.currentTableContentValues[rowNo]["currentCover"], self.Table.currentTableContentValues[rowNo]["path"]))
                    self.setItemColor(item, rowNo, itemNo, "sourceCover")
                elif itemNo==4:
                    newString = Organizer.emend(fu.getShortPath(self.Table.currentTableContentValues[rowNo]["destinationCover"], self.Table.currentTableContentValues[rowNo]["path"]), "file")
                    item = self.Table.createTableWidgetItem(newString, fu.getShortPath(self.Table.currentTableContentValues[rowNo]["currentCover"], self.Table.currentTableContentValues[rowNo]["path"]))
                    self.setItemColor(item, rowNo, itemNo, "destinationCover")
                if item!=None:
                    self.Table.setItem(rowNo, itemNo, item)
            Dialogs.showState(translate("FileUtils/Tables", "Generating Table..."), rowNo+1, allItemNumber)
                    
    def setItemColor(self, _item, _rowNo, _itemNo, _name):
        if _item!=None:
            if _name in self.Table.currentTableContentValues[_rowNo]["flagColor"]:
                r, g, b = self.Table.currentTableContentValues[_rowNo]["flagColor"][_name]
                _item.setBackground(MBrush(MColor(r, g, b)))
                    
    def correctTable(self):
        for rowNo in range(self.Table.rowCount()):
            for itemNo in range(self.Table.columnCount()):
                if self.Table.isChangableItem(rowNo, itemNo):
                    if itemNo==0 or itemNo==1:
                        newString = Organizer.emend(str(self.Table.item(rowNo,itemNo).text()), "directory")
                    elif itemNo==2 or itemNo==3:
                        newString = trForUI(str(self.Table.item(rowNo,itemNo).text()))
                    else:
                        newString = Organizer.emend(str(self.Table.item(rowNo,itemNo).text()), "file")
                    self.Table.item(rowNo,itemNo).setText(trForUI(newString))
          
    def getValueByRowAndColumn(self, _rowNo, _columnNo):
        if _columnNo==0:
            return self.Table.currentTableContentValues[_rowNo]["baseNameOfDirectory"]
        elif _columnNo==1:
            return self.Table.currentTableContentValues[_rowNo]["baseName"]
        elif _columnNo==2:
            return fu.getShortPath(self.Table.currentTableContentValues[_rowNo]["currentCover"], self.Table.currentTableContentValues[_rowNo]["path"])
        elif _columnNo==3:
            return fu.getShortPath(self.Table.currentTableContentValues[_rowNo]["sourceCover"], self.Table.currentTableContentValues[_rowNo]["path"])
        elif _columnNo==4:
            return fu.getShortPath(self.Table.currentTableContentValues[_rowNo]["destinationCover"], self.Table.currentTableContentValues[_rowNo]["path"])
        return ""



