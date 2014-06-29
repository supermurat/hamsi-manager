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


from Core import Organizer
import FileUtils as fu
from Core.MyObjects import *
from Details import Details
from Core import Dialogs
from Core import Universals as uni
from Core import ReportBug
from Tables import CoreTable


class SubFolderTable(CoreTable):
    def __init__(self, *args, **kwargs):
        CoreTable.__init__(self, *args, **kwargs)
        self.keyName = "subfolder"
        self.hiddenTableColumnsSettingKey = "hiddenSubFolderTableColumns"
        self.refreshColumns()

    def writeContents(self):
        self.changedValueNumber = 0
        changingFileDirectories = []
        if uni.isActiveAmarok and uni.getBoolValue("isSubFolderTableValuesChangeInAmarokDB"):
            import Amarok

            if Amarok.checkAmarok(True, False) == False:
                return False
        uni.startThreadAction()
        allItemNumber = len(self.values)
        Dialogs.showState(translate("FileUtils/SubFolders", "Writing File Informations"), 0, allItemNumber, True)
        for rowNo in range(self.rowCount()):
            isContinueThreadAction = uni.isContinueThreadAction()
            if isContinueThreadAction:
                try:
                    if fu.isWritableFileOrDir(self.values[rowNo]["path"], False, True):
                        if self.isRowHidden(rowNo):
                            fu.removeFileOrDir(self.values[rowNo]["path"])
                            self.changedValueNumber += 1
                        else:
                            baseNameOfDirectory = str(
                                self.values[rowNo]["baseNameOfDirectory"])
                            baseName = str(self.values[rowNo]["baseName"])
                            if self.isChangeableItem(rowNo, 0, baseNameOfDirectory):
                                baseNameOfDirectory = str(self.item(rowNo, 0).text())
                                self.changedValueNumber += 1
                                newDirectoryPath = fu.joinPath(
                                    fu.getDirName(fu.getDirName(self.values[rowNo]["path"])),
                                    baseNameOfDirectory)
                                self.setNewDirectory(newDirectoryPath)
                            if self.isChangeableItem(rowNo, 1, baseName, False):
                                baseName = str(self.item(rowNo, 1).text())
                                self.changedValueNumber += 1
                            newFilePath = fu.joinPath(str(self.values[rowNo]["path"]).replace(
                                fu.joinPath(str(self.values[rowNo]["baseNameOfDirectory"]),
                                            str(self.values[rowNo]["baseName"])), ""),
                                                      baseNameOfDirectory, baseName)
                            if fu.getRealPath(self.values[rowNo]["path"]) != fu.getRealPath(
                                newFilePath):
                                changingFileDirectories.append([self.values[rowNo]["path"],
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

    def showTableDetails(self, _fileNo, _infoNo):
        Details(self.values[_fileNo]["path"], uni.getBoolValue("isOpenDetailsInNewWindow"))

    def cellClickedTable(self, _row, _column):
        currentItem = self.currentItem()
        if currentItem is not None:
            cellLenght = len(currentItem.text()) * 8
            if cellLenght > self.columnWidth(_column):
                self.setColumnWidth(_column, cellLenght)

    def cellDoubleClickedTable(self, _row, _column):
        try:
            if uni.getBoolValue("isRunOnDoubleClick"):
                self.showTableDetails(_row, _column)
        except:
            Dialogs.showError(translate("SubFolderTable", "Cannot Open File"),
                              str(translate("SubFolderTable",
                                            "\"%s\" : cannot be opened. Please make sure that you selected a text file.")
                              ) % Organizer.getLink(self.values[_row]["path"]))

    def refreshColumns(self):
        self.tableColumns = [translate("SubFolderTable", "Directory"),
                             translate("SubFolderTable", "File Name")]
        self.tableColumnsKey = ["Directory", "File Name"]
        self.valueKeys = ["baseNameOfDirectory", "baseName", "artist", "title", "album",
                          "trackNum", "year", "genre", "firstComment", "firstLyrics"]

    def saveTable(self):
        self.checkFileExtensions(1, "baseName")
        return self.writeContents()

    def refreshTable(self, _path):
        self.values = []
        allFilesAndDirectories = fu.readDirectoryWithSubDirectoriesThread(_path,
                                                                          int(uni.MySettings["subDirectoryDeep"]),
                                                                          "file", uni.getBoolValue(
                "isShowHiddensInSubFolderTable"))
        allItemNumber = len(allFilesAndDirectories)
        uni.startThreadAction()
        rowNo = 0
        self.setRowCount(allItemNumber)
        for fileName in allFilesAndDirectories:
            isContinueThreadAction = uni.isContinueThreadAction()
            if isContinueThreadAction:
                try:
                    if fu.isReadableFileOrDir(fileName, False, True):
                        content = {}
                        content["path"] = fileName
                        content["baseNameOfDirectory"] = str(
                            str(fu.getBaseName(_path)) + str(fu.getDirName(fileName)).replace(_path, ""))
                        content["baseName"] = fu.getBaseName(fileName)
                        self.values.append(content)

                        newBaseNameOfDirectory = Organizer.emend(content["baseNameOfDirectory"], "directory")
                        itemBaseNameOfDirectory = self.createTableWidgetItem(newBaseNameOfDirectory,
                                                                             content["baseNameOfDirectory"])
                        self.setItem(rowNo, 0, itemBaseNameOfDirectory)

                        newBaseName = Organizer.emend(content["baseName"], "file")
                        itemBaseName = self.createTableWidgetItem(newBaseName, content["baseName"])
                        self.setItem(rowNo, 1, itemBaseName)
                except:
                    ReportBug.ReportBug()
                rowNo += 1
            else:
                allItemNumber = rowNo
            Dialogs.showState(translate("Tables", "Generating Table..."), rowNo, allItemNumber, True)
            if isContinueThreadAction == False:
                break
        uni.finishThreadAction()
        self.setRowCount(len(self.values))  # In case of Non Readable Files and Canceled process

    def correctTable(self):
        for rowNo in range(self.rowCount()):
            for itemNo in range(self.columnCount()):
                if self.isChangeableItem(rowNo, itemNo):
                    if itemNo == 0:
                        newString = Organizer.emend(str(self.item(rowNo, itemNo).text()), "directory")
                    else:
                        newString = Organizer.emend(str(self.item(rowNo, itemNo).text()), "file")
                    self.item(rowNo, itemNo).setText(str(newString))
          
