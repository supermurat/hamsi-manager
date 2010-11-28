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
from Details import CoverDetails
import Dialogs
from time import gmtime
import Universals

class Content():
    global readContents, writeContents
    
    def readContents(_directoryPath):
        currentTableContentValues = []
        allFilesAndDirectories = InputOutputs.IA.readDirectoryWithSubDirectories(_directoryPath, 
                    int(Universals.MySettings["CoversSubDirectoryDeep"]), True, True)
        allItemNumber = len(allFilesAndDirectories)
        Universals.startThreadAction()
        for dirNo,dirName in enumerate(allFilesAndDirectories):
            isContinueThreadAction = Universals.isContinueThreadAction()
            if isContinueThreadAction:
                if InputOutputs.IA.isReadableFileOrDir(dirName):
                    content = {}
                    content["path"] = dirName
                    content["baseNameOfDirectory"] = str(str(InputOutputs.IA.getBaseName(_directoryPath)) + 
                                    str(InputOutputs.IA.getDirName(dirName)).replace(_directoryPath,""))
                    content["baseName"] = InputOutputs.IA.getBaseName(dirName)

                    currentCover, isCorrectedFileContent = InputOutputs.IA.getIconFromDirectory(dirName)
                    selectedName = None
                    if isCorrectedFileContent and currentCover!=None:
                        selectedName = InputOutputs.IA.getBaseName(currentCover)
                    sourceCover = InputOutputs.IA.getFirstImageInDirectory(dirName, selectedName, False, False)
                    if currentCover==None:
                        currentCover = ""
                    if sourceCover==None:
                        sourceCover = ""
                    else:
                        sourceCover = dirName + "/" + sourceCover
                    content["currentCover"] = (currentCover)
                    content["sourceCover"] = (sourceCover)
                    content["destinationCover"] = (sourceCover)
                    content["isCorrectedFileContent"] = (isCorrectedFileContent)
                    currentTableContentValues.append(content)
            else:
                allItemNumber = dirNo+1
            Dialogs.showState(translate("InputOutputs/Covers", "Reading Cover Informations"),
                              dirNo+1,allItemNumber, True) 
            if isContinueThreadAction==False:
                break
        Universals.finishThreadAction()
        return currentTableContentValues
    
    def writeContents(_table):
        _table.changedValueNumber = 0
        changingFileDirectories=[]
        startRowNo,rowStep=0,1
        Universals.startThreadAction()
        allItemNumber = len(_table.currentTableContentValues)
        Dialogs.showState(translate("InputOutputs/Covers", "Writing Cover Informations"),0,allItemNumber, True)
        for rowNo in range(startRowNo,_table.rowCount(),rowStep):
            isContinueThreadAction = Universals.isContinueThreadAction()
            if isContinueThreadAction:
                if InputOutputs.IA.isWritableFileOrDir(_table.currentTableContentValues[rowNo]["path"]):
                    if _table.isRowHidden(rowNo):
                        InputOutputs.IA.removeFileOrDir(_table.currentTableContentValues[rowNo]["path"])
                        continue
                    newFileName=str(_table.currentTableContentValues[rowNo]["baseName"])
                    if _table.isChangableItem(rowNo, 1, _table.currentTableContentValues[rowNo]["baseName"], False):
                        _table.setItem(rowNo,1,MTableWidgetItem(str(unicode(_table.item(rowNo,1).text()).encode("utf-8")).decode("utf-8")))
                        newFileName = InputOutputs.IA.moveOrChange(_table.currentTableContentValues[rowNo]["path"], str(InputOutputs.IA.getDirName(InputOutputs.currentDirectoryPath))+"/"+str(_table.currentTableContentValues[rowNo]["baseNameOfDirectory"])+"/"+unicode(_table.item(rowNo,1).text()).encode("utf-8"), InputOutputs.IA.getObjectType(_table.currentTableContentValues[rowNo]["path"]))
                        _table.changedValueNumber += 1
                    if newFileName==False:
                        continue
                    #Cover Proccess
                    if _table.isChangableItem(rowNo, 3) or _table.isChangableItem(rowNo, 4):
                        sourcePath = _table.currentTableContentValues[rowNo]["sourceCover"]
                        destinationPath = _table.currentTableContentValues[rowNo]["destinationCover"]
                        if _table.isChangableItem(rowNo, 3):
                            sourcePath = unicode(_table.item(rowNo,3).text()).encode("utf-8").strip()
                        if _table.isChangableItem(rowNo, 4):
                            destinationPath = unicode(_table.item(rowNo,4).text()).encode("utf-8").strip()
                        if (unicode(_table.item(rowNo,2).text()).encode("utf-8")!=sourcePath or sourcePath!=destinationPath or unicode(_table.item(rowNo,2).text()).encode("utf-8")!=destinationPath) or (unicode(_table.item(rowNo,2).text()).encode("utf-8")!=_table.currentTableContentValues[rowNo]["currentCover"] and(unicode(_table.item(rowNo,2).text()).encode("utf-8")!=sourcePath and unicode(_table.item(rowNo,2).text()).encode("utf-8")!=destinationPath)):
                            if unicode(_table.item(rowNo,3).text()).encode("utf-8").strip()!="":
                                sourcePath = InputOutputs.IA.getRealPath(sourcePath, str(InputOutputs.IA.getDirName(InputOutputs.currentDirectoryPath))+"/"+str(_table.currentTableContentValues[rowNo]["baseNameOfDirectory"])+"/"+newFileName)
                                if InputOutputs.IA.checkSource(sourcePath, "file"):
                                    if destinationPath!="":
                                        destinationPath = InputOutputs.IA.getRealPath(destinationPath, str(InputOutputs.IA.getDirName(InputOutputs.currentDirectoryPath))+"/"+str(_table.currentTableContentValues[rowNo]["baseNameOfDirectory"])+"/"+newFileName)
                                        if sourcePath!=destinationPath:
                                            destinationPath = InputOutputs.IA.moveOrChange(sourcePath, destinationPath)
                                    else:
                                        destinationPath = sourcePath
                                    if destinationPath!=False:
                                        InputOutputs.IA.setIconToDirectory(str(InputOutputs.IA.getDirName(InputOutputs.currentDirectoryPath))+"/"+str(_table.currentTableContentValues[rowNo]["baseNameOfDirectory"]) + "/" + newFileName, destinationPath)
                                        _table.changedValueNumber += 1
                            else:
                                InputOutputs.IA.setIconToDirectory(str(InputOutputs.IA.getDirName(InputOutputs.currentDirectoryPath))+"/"+str(_table.currentTableContentValues[rowNo]["baseNameOfDirectory"])+"/"+newFileName, "")
                                _table.changedValueNumber += 1
                    if _table.isChangableItem(rowNo, 0):
                        newDirectoryName=unicode(_table.item(rowNo,0).text()).encode("utf-8")
                        try:
                            newDirectoryName=int(newDirectoryName)
                            newDirectoryName=str(newDirectoryName)
                        except:
                            if newDirectoryName.decode("utf-8").lower()==newDirectoryName.upper():
                                newDirectoryName=str(_table.currentTableContentValues[rowNo]["baseNameOfDirectory"])
                        if str(_table.currentTableContentValues[rowNo]["baseNameOfDirectory"])!=newDirectoryName:
                            newPath=InputOutputs.IA.getDirName(InputOutputs.currentDirectoryPath)
                            changingFileDirectories.append([])
                            changingFileDirectories[-1].append(str(newPath)+"/"+str(_table.currentTableContentValues[rowNo]["baseNameOfDirectory"])+"/"+str(newFileName))
                            changingFileDirectories[-1].append(str(newPath)+"/"+str(newDirectoryName)+"/"+str(newFileName))
                            _table.changedValueNumber += 1
            else:
                allItemNumber = rowNo+1
            Dialogs.showState(translate("InputOutputs/Covers", "Writing Cover Informations"),rowNo+1,allItemNumber, True)
            if isContinueThreadAction==False:
                break
        Universals.finishThreadAction()
        return InputOutputs.IA.changeDirectories(changingFileDirectories)



class CoverTable():
    def __init__(self, _table):
        self.Table = _table
        self.specialTollsBookmarkPointer = "cover"
        self.hiddenTableColumnsSettingKey = "hiddenCoverTableColumns"
        self.refreshColumns()
        pbtnGetFromAmarok = MPushButton(translate("CoverTable", "Get From Amarok"))
        MObject.connect(pbtnGetFromAmarok, SIGNAL("clicked()"), self.getFromAmarok)
        self.Table.hblBox.insertWidget(self.Table.hblBox.count()-1, pbtnGetFromAmarok)
        
    def showDetails(self, _fileNo, _infoNo):
        directoryPathOfCover = self.Table.currentTableContentValues[_fileNo]["path"]
        coverValues = [directoryPathOfCover, 
                       InputOutputs.IA.getRealPath(str(self.Table.item(_fileNo, 2).text()), directoryPathOfCover), 
                       InputOutputs.IA.getRealPath(str(self.Table.item(_fileNo, 3).text()), directoryPathOfCover), 
                       InputOutputs.IA.getRealPath(str(self.Table.item(_fileNo, 4).text()), directoryPathOfCover)]
        CoverDetails.CoverDetails(coverValues, self.Table.isOpenDetailsOnNewWindow.isChecked(), _infoNo)
        
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
            Dialogs.showError(translate("CoverTable", "Cannot Open File"), 
                        str(translate("CoverTable", "\"%s\" : cannot be opened. Please make sure that you selected a text file.")
                        ) % Organizer.getLink(self.Table.currentTableContentValues[_row]["path"]))
       
    def refreshColumns(self):
        self.Table.tableColumns=[translate("CoverTable", "Directory"), 
                            translate("CoverTable", "Directory Name"), 
                            translate("CoverTable", "Current Cover"), 
                            translate("CoverTable", "Source Cover"), 
                            translate("CoverTable", "Destination Cover")]
        self.Table.tableColumnsKey=["Directory", "Directory Name", "Current Cover", "Source Cover", "Destination Cover"]
        
    def save(self):
        returnValue = writeContents(self.Table)
        return returnValue
        
    def refresh(self, _path):
        self.Table.currentTableContentValues = readContents(_path)
        self.Table.setRowCount(len(self.Table.currentTableContentValues))
        for rowNo in range(self.Table.rowCount()):
            for itemNo in range(5):
                item = None
                if itemNo==0:
                    newString = Organizer.emend(self.Table.currentTableContentValues[rowNo]["baseNameOfDirectory"], "directory")
                    item = self.Table.createTableWidgetItem(newString, self.Table.currentTableContentValues[rowNo]["baseNameOfDirectory"])
                elif itemNo==1:
                    newString = Organizer.emend(self.Table.currentTableContentValues[rowNo]["baseName"], "directory")
                    item = self.Table.createTableWidgetItem(newString, self.Table.currentTableContentValues[rowNo]["baseName"])
                elif itemNo==2:
                    newString = Organizer.showWithIncorrectChars(self.Table.currentTableContentValues[rowNo]["currentCover"])
                    newString = newString.replace(self.Table.currentTableContentValues[rowNo]["path"], ".")
                    item = self.Table.createTableWidgetItem(newString, self.Table.currentTableContentValues[rowNo]["currentCover"])
                elif itemNo==3:
                    newString = Organizer.showWithIncorrectChars(self.Table.currentTableContentValues[rowNo]["sourceCover"])
                    newString = newString.replace(self.Table.currentTableContentValues[rowNo]["path"], ".")
                    item = self.Table.createTableWidgetItem(newString, self.Table.currentTableContentValues[rowNo]["sourceCover"])
                elif itemNo==4:
                    newString = Organizer.emend(self.Table.currentTableContentValues[rowNo]["destinationCover"], "file")
                    newString = newString.replace(self.Table.currentTableContentValues[rowNo]["path"], ".")
                    item = self.Table.createTableWidgetItem(newString, self.Table.currentTableContentValues[rowNo]["destinationCover"])
                if item!=None:
                    self.Table.setItem(rowNo, itemNo, item)
            if self.Table.currentTableContentValues[rowNo]["isCorrectedFileContent"]==False:
                item = self.Table.item(rowNo, 2)
                if item!=None:
                    item.setBackground(MBrush(MColor(255,163,163)))
                    
    def correctTable(self):
        for rowNo in range(self.Table.rowCount()):
            for itemNo in range(self.Table.columnCount()):
                if itemNo==0 or itemNo==1:
                    newString = Organizer.emend(unicode(self.Table.item(rowNo,itemNo).text(),"utf-8"), "directory")
                elif itemNo==2 or itemNo==3:
                    newString = Organizer.showWithIncorrectChars(unicode(self.Table.item(rowNo,itemNo).text(),"utf-8"))
                else:
                    newString = Organizer.emend(unicode(self.Table.item(rowNo,itemNo).text(),"utf-8"), "file")
                self.Table.item(rowNo,itemNo).setText(str(newString).decode("utf-8"))
        
    def getFromAmarok(self):
        try:
            import Amarok
            Dialogs.showState(translate("CoverTable", "Checking For Amarok..."), 0, 2)
            if Amarok.checkAmarok():
                Dialogs.showState(translate("CoverTable", "Getting Values From Amarok"), 1, 2)
                from Amarok import Commands
                directoriesAndValues = Commands.getDirectoriesAndValues()
                Dialogs.showState(translate("CoverTable", "Values Are Being Processed"), 2, 2)
                if directoriesAndValues!=None:
                    for rowNo in range(self.Table.rowCount()):
                        if self.Table.checkHiddenColumn(3) and self.Table.checkHiddenColumn(4):
                            if _table.isChangableItem(rowNo, 3):
                                directoryPath = str(InputOutputs.IA.getDirName(InputOutputs.currentDirectoryPath))+"/"+unicode(self.Table.item(rowNo,0).text()).encode("utf-8")+"/"+unicode(self.Table.item(rowNo,1).text()).encode("utf-8")
                                if directoryPath in directoriesAndValues:
                                    directoryAndValues = directoriesAndValues[directoryPath]
                                    self.Table.item(rowNo,3).setText(directoryAndValues["coverPath"][0].replace(directoryPath, "."))
                                    self.Table.item(rowNo,4).setText("./" + Organizer.getIconName(
                                                            directoryAndValues["Artist"][0], 
                                                            directoryAndValues["Album"][0], 
                                                            directoryAndValues["Genre"][0], 
                                                            directoryAndValues["Year"][0]))
        except:
            import ReportBug
            error = ReportBug.ReportBug()
            error.show()
        
