# -*- coding: utf-8 -*-
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
from Details import TextDetails
import Dialogs
from time import gmtime
import Universals

class Content():
    global readContents, writeContents
    
    def readContents(_directoryPath):
        currentTableContentValues = []
        allFilesAndDirectories = InputOutputs.IA.readDirectoryWithSubDirectories(_directoryPath, 
                    int(Universals.MySettings["subDirectoryDeep"]))
        allItemNumber = len(allFilesAndDirectories)
        Universals.startThreadAction()
        for fileNo,fileName in enumerate(allFilesAndDirectories):
            isContinueThreadAction = Universals.isContinueThreadAction()
            if isContinueThreadAction:
                if InputOutputs.IA.isReadableFileOrDir(fileName):
                    fileValues=[]
                    fileValues.append(str(str(InputOutputs.IA.getBaseName(_directoryPath)) + 
                                    str(InputOutputs.IA.getDirName(fileName)).replace(_directoryPath,"")))
                    fileValues.append(InputOutputs.IA.getBaseName(fileName))
                    currentTableContentValues.append(fileValues)
            else:
                allItemNumber = fileNo+1
            Dialogs.showState(translate("InputOutputs/SubFolders", "Reading File Informations"),
                              fileNo+1,allItemNumber, True) 
            if isContinueThreadAction==False:
                break
        Universals.finishThreadAction()
        return currentTableContentValues
    
    def writeContents(_table):
        _table.changedValueNumber = 0
        changingFileDirectories=[]
        Universals.startThreadAction()
        allItemNumber = len(_table.currentTableContentValues)
        Dialogs.showState(translate("InputOutputs/SubFolders", "Writing File Informations"),0,allItemNumber, True)
        for rowNo in range(_table.rowCount()):
            isContinueThreadAction = Universals.isContinueThreadAction()
            if isContinueThreadAction:
                if InputOutputs.IA.isWritableFileOrDir(str(InputOutputs.IA.getDirName(InputOutputs.currentDirectoryPath))+"/"+str(_table.currentTableContentValues[rowNo][0])+"/"+str(_table.currentTableContentValues[rowNo][1])):
                    if _table.isRowHidden(rowNo):
                        InputOutputs.IA.removeFileOrDir(str(InputOutputs.IA.getDirName(InputOutputs.currentDirectoryPath))+"/"+str(_table.currentTableContentValues[rowNo][0])+"/"+str(_table.currentTableContentValues[rowNo][1]))
                        continue
                    newFileName=str(_table.currentTableContentValues[rowNo][1])
                    if _table.isChangableItem(rowNo, 1, True, False):
                        _table.setItem(rowNo,1,MTableWidgetItem(str(unicode(_table.item(rowNo,1).text()).encode("utf-8")).decode("utf-8")))
                        newFileName = InputOutputs.IA.moveOrChange(str(InputOutputs.IA.getDirName(InputOutputs.currentDirectoryPath))+"/"+str(_table.currentTableContentValues[rowNo][0])+"/"+str(_table.currentTableContentValues[rowNo][1]),str(InputOutputs.IA.getDirName(InputOutputs.currentDirectoryPath))+"/"+str(_table.currentTableContentValues[rowNo][0])+"/"+unicode(_table.item(rowNo,1).text()).encode("utf-8"))
                        _table.changedValueNumber += 1
                    if newFileName==False:
                        continue
                    if _table.isChangableItem(rowNo, 0, False):
                        newDirectoryName=unicode(_table.item(rowNo,0).text()).encode("utf-8")
                        try:
                            newDirectoryName=int(newDirectoryName)
                            newDirectoryName=str(newDirectoryName)
                        except:
                            if newDirectoryName.decode("utf-8").lower()==newDirectoryName.upper():
                                newDirectoryName=str(_table.currentTableContentValues[rowNo][0])
                        if str(_table.currentTableContentValues[rowNo][0])!=newDirectoryName:
                            newPath=InputOutputs.IA.getDirName(InputOutputs.currentDirectoryPath)
                            changingFileDirectories.append([])
                            changingFileDirectories[-1].append(str(newPath)+"/"+str(_table.currentTableContentValues[rowNo][0])+"/"+str(newFileName))
                            changingFileDirectories[-1].append(str(newPath)+"/"+str(newDirectoryName)+"/"+str(newFileName))
                            _table.changedValueNumber += 1
            else:
                allItemNumber = rowNo+1
            Dialogs.showState(translate("InputOutputs/SubFolders", "Writing File Informations"),rowNo+1,allItemNumber, True)
            if isContinueThreadAction==False:
                break
        Universals.finishThreadAction()
        return InputOutputs.IA.changeDirectories(changingFileDirectories)



class SubFolderTable():
    def __init__(self, _table):
        self.Table = _table
        self.specialTollsBookmarkPointer = "subfolder"
        self.hiddenTableColumnsSettingKey = "hiddenSubFolderTableColumns"
        self.refreshColumns()
        
    def showDetails(self, _fileNo, _infoNo):
        TextDetails.TextDetails(InputOutputs.currentDirectoryPath+"/"+self.Table.currentTableContentValues[_fileNo][1],self.Table.isOpenDetailsOnNewWindow.isChecked())
        
    def cellClicked(self,_row,_column):
        for row_no in range(self.Table.rowCount()):
            self.Table.setRowHeight(row_no,30)
        if len(self.Table.currentItem().text())*8>self.Table.columnWidth(_column):
            self.Table.setColumnWidth(_column,len(self.Table.currentItem().text())*8)
    
    def cellDoubleClicked(self,_row,_column):
        try:
            if self.Table.tbIsRunOnDoubleClick.isChecked()==True:
                self.showDetails(_row, _column)
        except:
            Dialogs.showError(translate("SubFolderTable", "Cannot Open File"), 
                        str(translate("SubFolderTable", "\"%s\" : cannot be opened. Please make sure that you selected a text file.")
                        ) % Organizer.getLink(InputOutputs.currentDirectoryPath+"/"+self.Table.currentTableContentValues[_row][1]))
       
    def refreshColumns(self):
        self.Table.tableColumns=[translate("SubFolderTable", "Directory"), 
                            translate("SubFolderTable", "File Name")]
        self.Table.tableColumnsKey=["Directory", "File Name"]
        
    def save(self):
        returnValue = writeContents(self.Table)
        return returnValue
        
    def refresh(self, _path):
        self.Table.currentTableContentValues = readContents(_path)
        self.Table.setRowCount(len(self.Table.currentTableContentValues))
        for fileNo in range(self.Table.rowCount()):
            for itemNo in range(0,2):
                if itemNo==0:
                    newString = Organizer.emend(self.Table.currentTableContentValues[rowNo][itemNo], "directory")
                else:
                    newString = Organizer.emend(self.Table.currentTableContentValues[rowNo][itemNo], "file")
                item = MTableWidgetItem(newString.decode("utf-8"))
                item.setStatusTip(item.text())
                self.Table.setItem(fileNo,itemNo,item)
                if str(self.Table.currentTableContentValues[rowNo][itemNo])!=str(newString) and str(self.Table.currentTableContentValues[rowNo][itemNo])!="None":
                    self.Table.item(fileNo,itemNo).setBackground(MBrush(MColor(142,199,255)))
                    self.Table.item(fileNo,itemNo).setToolTip(Organizer.showWithIncorrectChars(self.Table.currentTableContentValues[rowNo][itemNo]).decode("utf-8"))
                    
    def correctTable(self):
        for rowNo in range(self.Table.rowCount()):
            for itemNo in range(self.Table.columnCount()):
                if itemNo==0:
                    newString = Organizer.emend(unicode(self.Table.item(rowNo,itemNo).text(),"utf-8"), "directory")
                else:
                    newString = Organizer.emend(unicode(self.Table.item(rowNo,itemNo).text(),"utf-8"), "file")
                self.Table.item(rowNo,itemNo).setText(str(newString).decode("utf-8"))

          
