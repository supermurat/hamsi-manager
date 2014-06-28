# # This file is part of HamsiManager.
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
from Details import Details
from Core import Dialogs
import Options
from time import gmtime
from Core import Universals as uni
from Core import ReportBug


class SubFolderTable():
    def __init__(self, _table):
        self.Table = _table
        self.keyName = "subfolder"
        self.hiddenTableColumnsSettingKey = "hiddenSubFolderTableColumns"
        self.refreshColumns()

    def readContents(self, _directoryPath):
        currentTableContentValues = []
        allFilesAndDirectories = fu.readDirectoryWithSubDirectoriesThread(_directoryPath,
                                                                          int(uni.MySettings["subDirectoryDeep"]),
                                                                          "file", uni.getBoolValue(
                "isShowHiddensInSubFolderTable"))
        allItemNumber = len(allFilesAndDirectories)
        uni.startThreadAction()
        for fileNo, fileName in enumerate(allFilesAndDirectories):
            isContinueThreadAction = uni.isContinueThreadAction()
            if isContinueThreadAction:
                try:
                    if fu.isReadableFileOrDir(fileName, False, True):
                        content = {}
                        content["path"] = fileName
                        content["baseNameOfDirectory"] = str(
                            str(fu.getBaseName(_directoryPath)) + str(fu.getDirName(fileName)).replace(_directoryPath,
                                                                                                       ""))
                        content["baseName"] = fu.getBaseName(fileName)
                        currentTableContentValues.append(content)
                except:
                    ReportBug.ReportBug()
            else:
                allItemNumber = fileNo + 1
            Dialogs.showState(translate("FileUtils/SubFolders", "Reading File Informations"),
                              fileNo + 1, allItemNumber, True)
            if isContinueThreadAction == False:
                break
        uni.finishThreadAction()
        return currentTableContentValues

    def writeContents(self):
        self.Table.changedValueNumber = 0
        changingFileDirectories = []
        if uni.isActiveAmarok and uni.getBoolValue("isSubFolderTableValuesChangeInAmarokDB"):
            import Amarok

            if Amarok.checkAmarok(True, False) == False:
                return False
        uni.startThreadAction()
        allItemNumber = len(self.Table.currentTableContentValues)
        Dialogs.showState(translate("FileUtils/SubFolders", "Writing File Informations"), 0, allItemNumber, True)
        for rowNo in range(self.Table.rowCount()):
            isContinueThreadAction = uni.isContinueThreadAction()
            if isContinueThreadAction:
                try:
                    if fu.isWritableFileOrDir(self.Table.currentTableContentValues[rowNo]["path"], False, True):
                        if self.Table.isRowHidden(rowNo):
                            fu.removeFileOrDir(self.Table.currentTableContentValues[rowNo]["path"])
                            self.Table.changedValueNumber += 1
                        else:
                            baseNameOfDirectory = str(
                                self.Table.currentTableContentValues[rowNo]["baseNameOfDirectory"])
                            baseName = str(self.Table.currentTableContentValues[rowNo]["baseName"])
                            if self.Table.isChangeableItem(rowNo, 0, baseNameOfDirectory):
                                baseNameOfDirectory = str(self.Table.item(rowNo, 0).text())
                                self.Table.changedValueNumber += 1
                                newDirectoryPath = fu.joinPath(
                                    fu.getDirName(fu.getDirName(self.Table.currentTableContentValues[rowNo]["path"])),
                                    baseNameOfDirectory)
                                self.Table.setNewDirectory(newDirectoryPath)
                            if self.Table.isChangeableItem(rowNo, 1, baseName, False):
                                baseName = str(self.Table.item(rowNo, 1).text())
                                self.Table.changedValueNumber += 1
                            newFilePath = fu.joinPath(str(self.Table.currentTableContentValues[rowNo]["path"]).replace(
                                fu.joinPath(str(self.Table.currentTableContentValues[rowNo]["baseNameOfDirectory"]),
                                            str(self.Table.currentTableContentValues[rowNo]["baseName"])), ""),
                                                      baseNameOfDirectory, baseName)
                            if fu.getRealPath(self.Table.currentTableContentValues[rowNo]["path"]) != fu.getRealPath(
                                newFilePath):
                                changingFileDirectories.append([self.Table.currentTableContentValues[rowNo]["path"],
                                                                fu.getRealPath(newFilePath)])
                except:
                    ReportBug.ReportBug()
            else:
                allItemNumber = rowNo + 1
            Dialogs.showState(translate("FileUtils/SubFolders", "Writing File Informations"), rowNo + 1, allItemNumber,
                              True)
            if isContinueThreadAction == False:
                break
        uni.finishThreadAction()
        pathValues = fu.changeDirectories(changingFileDirectories)
        if uni.isActiveAmarok and uni.getBoolValue("isSubFolderTableValuesChangeInAmarokDB"):
            import Amarok
            from Amarok import Operations

            Operations.changePaths(pathValues, "file")
        return True

    def showDetails(self, _fileNo, _infoNo):
        Details(self.Table.currentTableContentValues[_fileNo]["path"], uni.getBoolValue("isOpenDetailsInNewWindow"))

    def cellClicked(self, _row, _column):
        currentItem = self.Table.currentItem()
        if currentItem is not None:
            cellLenght = len(currentItem.text()) * 8
            if cellLenght > self.Table.columnWidth(_column):
                self.Table.setColumnWidth(_column, cellLenght)

    def cellDoubleClicked(self, _row, _column):
        try:
            if uni.getBoolValue("isRunOnDoubleClick"):
                self.showDetails(_row, _column)
        except:
            Dialogs.showError(translate("SubFolderTable", "Cannot Open File"),
                              str(translate("SubFolderTable",
                                            "\"%s\" : cannot be opened. Please make sure that you selected a text file.")
                              ) % Organizer.getLink(self.Table.currentTableContentValues[_row]["path"]))

    def refreshColumns(self):
        self.Table.tableColumns = [translate("SubFolderTable", "Directory"),
                                   translate("SubFolderTable", "File Name")]
        self.Table.tableColumnsKey = ["Directory", "File Name"]

    def save(self):
        self.Table.checkFileExtensions(1, "baseName")
        return self.writeContents()

    def refresh(self, _path):
        self.Table.currentTableContentValues = self.readContents(_path)
        self.Table.setRowCount(len(self.Table.currentTableContentValues))
        allItemNumber = self.Table.rowCount()
        for rowNo in range(allItemNumber):
            for itemNo in range(2):
                item = None
                if itemNo == 0:
                    newString = Organizer.emend(self.Table.currentTableContentValues[rowNo]["baseNameOfDirectory"],
                                                "directory")
                    item = self.Table.createTableWidgetItem(newString, self.Table.currentTableContentValues[rowNo][
                        "baseNameOfDirectory"])
                elif itemNo == 1:
                    newString = Organizer.emend(self.Table.currentTableContentValues[rowNo]["baseName"], "file")
                    item = self.Table.createTableWidgetItem(newString,
                                                            self.Table.currentTableContentValues[rowNo]["baseName"])
                if item != None:
                    self.Table.setItem(rowNo, itemNo, item)
            Dialogs.showState(translate("Tables", "Generating Table..."), rowNo + 1, allItemNumber)

    def correctTable(self):
        for rowNo in range(self.Table.rowCount()):
            for itemNo in range(self.Table.columnCount()):
                if self.Table.isChangeableItem(rowNo, itemNo):
                    if itemNo == 0:
                        newString = Organizer.emend(str(self.Table.item(rowNo, itemNo).text()), "directory")
                    else:
                        newString = Organizer.emend(str(self.Table.item(rowNo, itemNo).text()), "file")
                    self.Table.item(rowNo, itemNo).setText(str(newString))

    def getValueByRowAndColumn(self, _rowNo, _columnNo):
        if _columnNo == 0:
            return self.Table.currentTableContentValues[_rowNo]["baseNameOfDirectory"]
        elif _columnNo == 1:
            return self.Table.currentTableContentValues[_rowNo]["baseName"]
        return ""
          
