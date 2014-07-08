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


class FolderTable(CoreTable):
    def __init__(self, *args, **kwargs):
        CoreTable.__init__(self, *args, **kwargs)
        self.keyName = "directory"
        self.hiddenTableColumnsSettingKey = "hiddenFolderTableColumns"
        self.refreshColumns()

    def writeContents(self):
        self.changedValueNumber = 0
        oldAndNewPathValues = []
        uni.startThreadAction()
        if uni.isActiveAmarok and uni.getBoolValue("isFolderTableValuesChangeInAmarokDB"):
            import Amarok

            if Amarok.checkAmarok(True, False) == False:
                return False
        allItemNumber = len(self.values)
        Dialogs.showState(translate("FileUtils/Folders", "Writing Directory Informations"), 0, allItemNumber, True)
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
                            newFilePath = fu.joinPath(
                                fu.getDirName(fu.getDirName(self.values[rowNo]["path"])),
                                baseNameOfDirectory, baseName)

                            oldFilePath = fu.getRealPath(self.values[rowNo]["path"])
                            newFilePath = fu.getRealPath(newFilePath)
                            if oldFilePath != newFilePath:
                                oldAndNewPaths = {}
                                oldAndNewPaths["oldPath"] = oldFilePath
                                oldAndNewPaths["newPath"] = fu.moveOrChange(oldFilePath, newFilePath,
                                                                            fu.getObjectType(oldFilePath))
                                if oldFilePath != oldAndNewPaths["newPath"]:
                                    oldAndNewPathValues.append(oldAndNewPaths)
                                    oldDirName = fu.getDirName(oldFilePath)
                                    if uni.getBoolValue("isClearEmptyDirectoriesWhenFileMove"):
                                        fu.checkEmptyDirectories(oldDirName, True, True,
                                                                 uni.getBoolValue("isAutoCleanSubFolderWhenFileMove"))
                                    if (uni.isActiveDirectoryCover and
                                            uni.getBoolValue("isActiveAutoMakeIconToDirectory") and
                                            uni.getBoolValue("isAutoMakeIconToDirectoryWhenFileMove") and
                                            fu.getObjectType(oldFilePath) == "file"):
                                        fu.checkIcon(oldDirName)
                                        fu.checkIcon(fu.getDirName(oldAndNewPaths["newPath"]))
                except:
                    ReportBug.ReportBug()
            else:
                allItemNumber = rowNo + 1
            Dialogs.showState(translate("FileUtils/Folders", "Writing Directory And File Informations"), rowNo + 1,
                              allItemNumber, True)
            if isContinueThreadAction == False:
                break
        uni.finishThreadAction()
        if (uni.isActiveAmarok and uni.getBoolValue("isFolderTableValuesChangeInAmarokDB") and
                    len(oldAndNewPathValues) > 0):
            import Amarok
            from Amarok import Operations

            Operations.changePaths(oldAndNewPathValues)
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
            Dialogs.showError(translate("FolderTable", "Cannot Open File"),
                              str(translate("FolderTable",
                                            "\"%s\" : cannot be opened. Please make sure that you selected a text file.")
                              ) % Organizer.getLink(self.values[_row]["path"]))

    def refreshColumns(self):
        self.tableColumns = [translate("FolderTable", "Directory"),
                             translate("FolderTable", "File/Directory Name")]
        self.tableColumnsKey = ["Directory", "File/Directory Name"]
        self.valueKeys = ["baseNameOfDirectory", "baseName"]

    def saveTable(self):
        self.checkFileExtensions(1, "baseName", True)
        return self.writeContents()

    def refreshTable(self, _path):
        self.values = []
        fileAndDirectoryNames = fu.readDirectory(_path, "fileAndDirectory",
                                                 uni.getBoolValue("isShowHiddensInFolderTable"))
        allItemNumber = len(fileAndDirectoryNames)
        uni.startThreadAction()
        baseNameOfDirectory = fu.getBaseName(_path)
        rowNo = 0
        self.setRowCount(allItemNumber)
        for dirName in fileAndDirectoryNames:
            isContinueThreadAction = uni.isContinueThreadAction()
            if isContinueThreadAction:
                try:
                    if fu.isReadableFileOrDir(fu.joinPath(_path, dirName), False, True):
                        content = {}
                        content["path"] = fu.joinPath(_path, dirName)
                        content["baseNameOfDirectory"] = baseNameOfDirectory
                        content["baseName"] = dirName
                        self.values.append(content)

                        newBaseNameOfDirectory = Organizer.emend(content["baseNameOfDirectory"], "directory")
                        itemBaseNameOfDirectory = self.createItem(newBaseNameOfDirectory,
                                                                             content["baseNameOfDirectory"])
                        self.setItem(rowNo, 0, itemBaseNameOfDirectory)

                        newBaseName = Organizer.emend(content["baseName"], fu.getObjectType(self.values[rowNo]["path"]))
                        itemBaseName = self.createItem(newBaseName, content["baseName"])
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
                        newString = Organizer.emend(str(self.item(rowNo, itemNo).text()), fu.getObjectType(
                            self.values[rowNo]["path"]))
                    self.item(rowNo, itemNo).setText(str(newString))
