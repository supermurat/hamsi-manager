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
                    fileValues=[]
                    fileValues.append(str(str(InputOutputs.IA.getBaseName(_directoryPath)) + 
                                    str(InputOutputs.IA.getDirName(dirName)).replace(_directoryPath,"")))
                    fileValues.append(InputOutputs.IA.getBaseName(dirName))
                    iconPath, isCorrectedFileContent = InputOutputs.IA.getIconFromDirectory(dirName)
                    selectedName = None
                    if isCorrectedFileContent and iconPath!=None:
                        selectedName = InputOutputs.IA.getBaseName(iconPath)
                    sourceCover = InputOutputs.IA.getFirstImageInDirectory(dirName, selectedName, False, False)
                    if iconPath==None:
                        iconPath = ""
                    if sourceCover==None:
                        sourceCover = ""
                    else:
                        sourceCover = dirName + "/" + sourceCover
                    fileValues.append(iconPath)
                    fileValues.append(sourceCover)
                    fileValues.append(sourceCover)
                    fileValues.append(isCorrectedFileContent)
                    currentTableContentValues.append(fileValues)
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
            realRowNo=rowNo
            isContinueThreadAction = Universals.isContinueThreadAction()
            if isContinueThreadAction:
                if InputOutputs.IA.isWritableFileOrDir(str(InputOutputs.IA.getDirName(InputOutputs.currentDirectoryPath))+"/"+str(_table.currentTableContentValues[realRowNo][0])+"/"+str(_table.currentTableContentValues[realRowNo][1])):
                    if _table.isRowHidden(rowNo):
                        InputOutputs.IA.removeFileOrDir(str(InputOutputs.IA.getDirName(InputOutputs.currentDirectoryPath))+"/"+str(_table.currentTableContentValues[realRowNo][0])+"/"+str(_table.currentTableContentValues[realRowNo][1]))
                        continue
                    newFileName=str(_table.currentTableContentValues[realRowNo][1])
                    if _table.isChangableItem(rowNo, 1, True, False):
                        _table.setItem(rowNo,1,MTableWidgetItem(str(unicode(_table.item(rowNo,1).text()).encode("utf-8")).decode("utf-8")))
                        newFileName = InputOutputs.IA.moveOrChange(str(InputOutputs.IA.getDirName(InputOutputs.currentDirectoryPath))+"/"+str(_table.currentTableContentValues[realRowNo][0])+"/"+str(_table.currentTableContentValues[realRowNo][1]), str(InputOutputs.IA.getDirName(InputOutputs.currentDirectoryPath))+"/"+str(_table.currentTableContentValues[realRowNo][0])+"/"+unicode(_table.item(rowNo,1).text()).encode("utf-8"), InputOutputs.IA.getObjectType(str(InputOutputs.IA.getDirName(InputOutputs.currentDirectoryPath))+"/"+str(_table.currentTableContentValues[realRowNo][0])+"/"+str(_table.currentTableContentValues[realRowNo][1])))
                        _table.changedValueNumber += 1
                    if newFileName==False:
                        continue
                    #Cover Proccess
                    if _table.isChangableItem(rowNo, 3, False) or _table.isChangableItem(rowNo, 4, False):
                        sourcePath = _table.currentTableContentValues[realRowNo][3]
                        destinationPath = _table.currentTableContentValues[realRowNo][4]
                        if _table.isChangableItem(rowNo, 3, False):
                            sourcePath = unicode(_table.item(rowNo,3).text()).encode("utf-8").strip()
                        if _table.isChangableItem(rowNo, 4, False):
                            destinationPath = unicode(_table.item(rowNo,4).text()).encode("utf-8").strip()
                        if (unicode(_table.item(rowNo,2).text()).encode("utf-8")!=sourcePath or sourcePath!=destinationPath or unicode(_table.item(rowNo,2).text()).encode("utf-8")!=destinationPath) or (unicode(_table.item(rowNo,2).text()).encode("utf-8")!=_table.currentTableContentValues[realRowNo][2] and(unicode(_table.item(rowNo,2).text()).encode("utf-8")!=sourcePath and unicode(_table.item(rowNo,2).text()).encode("utf-8")!=destinationPath)):
                            if unicode(_table.item(rowNo,3).text()).encode("utf-8").strip()!="":
                                sourcePath = InputOutputs.IA.getRealPath(sourcePath, str(InputOutputs.IA.getDirName(InputOutputs.currentDirectoryPath))+"/"+str(_table.currentTableContentValues[realRowNo][0])+"/"+newFileName)
                                if InputOutputs.IA.checkSource(sourcePath, "file"):
                                    if destinationPath!="":
                                        destinationPath = InputOutputs.IA.getRealPath(destinationPath, str(InputOutputs.IA.getDirName(InputOutputs.currentDirectoryPath))+"/"+str(_table.currentTableContentValues[realRowNo][0])+"/"+newFileName)
                                        if sourcePath!=destinationPath:
                                            destinationPath = InputOutputs.IA.moveOrChange(sourcePath, destinationPath)
                                    else:
                                        destinationPath = sourcePath
                                    if destinationPath!=False:
                                        InputOutputs.IA.setIconToDirectory(str(InputOutputs.IA.getDirName(InputOutputs.currentDirectoryPath))+"/"+str(_table.currentTableContentValues[realRowNo][0]) + "/" + newFileName, destinationPath)
                                        _table.changedValueNumber += 1
                            else:
                                InputOutputs.IA.setIconToDirectory(str(InputOutputs.IA.getDirName(InputOutputs.currentDirectoryPath))+"/"+str(_table.currentTableContentValues[realRowNo][0])+"/"+newFileName, "")
                                _table.changedValueNumber += 1
                    if _table.isChangableItem(rowNo, 0, False):
                        newDirectoryName=unicode(_table.item(rowNo,0).text()).encode("utf-8")
                        try:
                            newDirectoryName=int(newDirectoryName)
                            newDirectoryName=str(newDirectoryName)
                        except:
                            if newDirectoryName.decode("utf-8").lower()==newDirectoryName.upper():
                                newDirectoryName=str(_table.currentTableContentValues[realRowNo][0])
                        if str(_table.currentTableContentValues[realRowNo][0])!=newDirectoryName:
                            newPath=InputOutputs.IA.getDirName(InputOutputs.currentDirectoryPath)
                            changingFileDirectories.append([])
                            changingFileDirectories[-1].append(str(newPath)+"/"+str(_table.currentTableContentValues[realRowNo][0])+"/"+str(newFileName))
                            changingFileDirectories[-1].append(str(newPath)+"/"+str(newDirectoryName)+"/"+str(newFileName))
                            _table.changedValueNumber += 1
            else:
                allItemNumber = realRowNo+1
            Dialogs.showState(translate("InputOutputs/Covers", "Writing Cover Informations"),realRowNo+1,allItemNumber, True)
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
        directoryPathOfCover = InputOutputs.currentDirectoryPath + "/" + self.Table.currentTableContentValues[_fileNo][1]
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
                        ) % Organizer.getLink(InputOutputs.currentDirectoryPath + "/" + self.Table.currentTableContentValues[_row][1]))
       
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
        startRowNo, rowStep = 0, 1
        for dirNo in range(startRowNo, self.Table.rowCount(), rowStep):
            for itemNo in range(0,5):
                if itemNo==0 or itemNo==1:
                    newString = Organizer.emend(self.Table.currentTableContentValues[dirNo][itemNo], "directory")
                elif itemNo==2 or itemNo==3:
                    newString = Organizer.showWithIncorrectChars(self.Table.currentTableContentValues[dirNo][itemNo])
                else:
                    newString = Organizer.emend(self.Table.currentTableContentValues[dirNo][itemNo], "file")
                if 1<itemNo and itemNo<5:
                    newString = newString.replace(_path + "/" + self.Table.currentTableContentValues[dirNo][1], ".")
                item = MTableWidgetItem(newString.decode("utf-8"))
                item.setStatusTip(item.text())
                self.Table.setItem(dirNo,itemNo,item)
                if itemNo!=2 and itemNo!=3 and str(self.Table.currentTableContentValues[dirNo][itemNo])!=str(newString) and str(self.Table.currentTableContentValues[dirNo][itemNo])!=str(_path + "/" + self.Table.currentTableContentValues[dirNo][1] + newString[1:]) and str(self.Table.currentTableContentValues[dirNo][itemNo])!="None":
                    self.Table.item(dirNo,itemNo).setBackground(MBrush(MColor(142,199,255)))
                    self.Table.item(dirNo,itemNo).setToolTip(Organizer.showWithIncorrectChars(self.Table.currentTableContentValues[dirNo][itemNo]).decode("utf-8"))
            if self.Table.currentTableContentValues[dirNo][5]==False:
                self.Table.item(dirNo,2).setBackground(MBrush(MColor(255,163,163)))
                    
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
                            if _table.isChangableItem(rowNo, 3, False):
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
        
