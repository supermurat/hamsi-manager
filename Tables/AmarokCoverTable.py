# This file is part of HamsiManager.
#
# Copyright (c) 2010 - 2015 Murat Demir <mopened@gmail.com>
#
# Hamsi Manager is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Hamsi Manager is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with HamsiManager; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA


from Core import Organizer
import FileUtils as fu
from Core.MyObjects import *
from Details import CoverDetails
from Core import Dialogs
from Core import Universals as uni
from Core import ReportBug
from Tables import CoreTable
import SearchEngines


class AmarokCoverTable(CoreTable):
    def __init__(self, *args, **kwargs):
        CoreTable.__init__(self, *args, **kwargs)
        from Amarok import Filter

        self.keyName = "cover"
        self.amarokFilterKeyName = "AmarokFilterAmarokCoverTable"
        self.hiddenTableColumnsSettingKey = "hiddenAmarokCoverTableColumns"
        self.refreshColumns()
        self.wFilter = Filter.FilterWidget(self, self.amarokFilterKeyName)
        self.hblBoxOptions.addWidget(self.wFilter)
        pbtnVerifyTableValues = MPushButton(translate("FileTable", "Verify Table"))
        pbtnVerifyTableValues.setMenu(SearchEngines.SearchEngines(self, "value"))
        self.mContextMenu.addMenu(SearchEngines.SearchEngines(self, "value", True))
        self.hblBoxTools.addWidget(pbtnVerifyTableValues)

    def refreshColumns(self):
        self.tableColumns = [translate("AmarokCoverTable", "Directory"),
                             translate("AmarokCoverTable", "Directory Name"),
                             translate("AmarokCoverTable", "Current Cover"),
                             translate("AmarokCoverTable", "Source Cover"),
                             translate("AmarokCoverTable", "Destination Cover")]
        self.tableColumnsKey = ["baseNameOfDirectory", "baseName", "currentCover", "sourceCover", "destinationCover"]
        self.tableReadOnlyColumnsKey = []

    def saveTable(self):
        self.checkFileExtensions("destinationCover", "sourceCover")
        return self.writeContents()

    def refreshTable(self, _path):
        self.values = []
        uni.startThreadAction()
        import Amarok

        Dialogs.showState(translate("AmarokMusicTable", "Getting Values From Amarok"), 0, 1)
        if Amarok.checkAmarok():
            isContinueThreadAction = uni.isContinueThreadAction()
            if isContinueThreadAction:
                from Amarok import Operations

                directoriesAndValues = Operations.getDirectoriesAndValues(uni.MySettings[self.amarokFilterKeyName])
                Dialogs.showState(translate("AmarokMusicTable", "Values Are Being Processed"), 1, 1)
                isContinueThreadAction = uni.isContinueThreadAction()
                if isContinueThreadAction:
                    if directoriesAndValues is not None:
                        allItemNumber = len(directoriesAndValues)
                        self.setRowCount(allItemNumber)
                        rowNo = 0
                        for dirPath, dirRow in directoriesAndValues.items():
                            isContinueThreadAction = uni.isContinueThreadAction()
                            if isContinueThreadAction:
                                try:
                                    if fu.isReadableFileOrDir(dirPath, False, True) and fu.isReadableFileOrDir(
                                        fu.joinPath(dirPath, ".directory"), False, True):
                                        content = {}
                                        content["path"] = dirPath
                                        content["pathOfParentDirectory"] = fu.getDirName(dirPath)
                                        content["baseName"] = fu.getBaseName(dirPath)
                                        currentCover, isCorrectedFileContent = fu.getIconFromDirectory(dirPath)
                                        if currentCover is None:
                                            currentCover = ""
                                        content["currentCover"] = (currentCover)
                                        content["sourceCover"] = (dirRow["coverPath"][0].replace(dirPath, "."))
                                        content["destinationCover"] = ("./" + Organizer.getIconName(
                                            dirRow["artist"][0],
                                            dirRow["album"][0],
                                            dirRow["genre"][0],
                                            dirRow["year"][0]))
                                        content["flagColor"] = {}
                                        if isCorrectedFileContent is False:
                                            content["flagColor"]["currentCover"] = 255, 163, 163
                                        if fu.isFile(content["sourceCover"]) is False:
                                            content["flagColor"]["sourceCover"] = 255, 163, 163
                                        self.values.append(content)

                                        newPathOfParentDirectory = Organizer.emend(
                                            self.values[rowNo]["pathOfParentDirectory"], "directory")
                                        self.createItem(rowNo, "pathOfParentDirectory", newPathOfParentDirectory,
                                                        self.values[rowNo]["pathOfParentDirectory"])

                                        newBaseName = Organizer.emend(self.values[rowNo]["baseName"], "directory")
                                        self.createItem(rowNo, "pathOfParentDirectory", newBaseName,
                                                        self.values[rowNo]["baseName"])

                                        newCurrentCover = fu.getShortPath(self.values[rowNo]["currentCover"],
                                                                          self.values[rowNo]["path"])
                                        itemCurrentCover = self.createItem(rowNo, "currentCover", newCurrentCover,
                                                                           newCurrentCover, True)
                                        self.setItemColor(itemCurrentCover, rowNo, 2, "currentCover")

                                        newSourceCover = fu.getShortPath(self.values[rowNo]["sourceCover"],
                                                                         self.values[rowNo]["path"])
                                        itemSourceCover = self.createItem(rowNo, "sourceCover", newSourceCover,
                                                                          fu.getShortPath(
                                                                              self.values[rowNo]["currentCover"],
                                                                              self.values[rowNo]["path"]))
                                        self.setItemColor(itemSourceCover, rowNo, 3, "sourceCover")

                                        newDestinationCover = Organizer.emend(
                                            fu.getShortPath(self.values[rowNo]["destinationCover"],
                                                            self.values[rowNo]["path"]), "file")
                                        itemDestinationCover = self.createItem(rowNo, "destinationCover",
                                                                               newDestinationCover,
                                                                               fu.getShortPath(
                                                                                   self.values[rowNo]["currentCover"],
                                                                                   self.values[rowNo]["path"]))
                                        self.setItemColor(itemDestinationCover, rowNo, 4, "destinationCover")
                                        rowNo += 1
                                    else:
                                        allItemNumber -= 1
                                except:
                                    ReportBug.ReportBug()
                                    allItemNumber -= 1
                            else:
                                allItemNumber = rowNo
                            Dialogs.showState(translate("Tables", "Generating Table..."), rowNo, allItemNumber, True)
                            if isContinueThreadAction is False:
                                break
        uni.finishThreadAction()
        self.setRowCount(len(self.values))  # In case of Non Readable Files and Canceled process

    def writeContents(self):
        self.changedValueNumber = 0
        oldAndNewPathValues = []
        startRowNo, rowStep = 0, 1
        uni.startThreadAction()
        allItemNumber = len(self.values)
        Dialogs.showState(translate("FileUtils/Covers", "Writing Cover Informations"), 0, allItemNumber, True)
        for rowNo in range(startRowNo, self.rowCount(), rowStep):
            isContinueThreadAction = uni.isContinueThreadAction()
            if isContinueThreadAction:
                try:
                    if fu.isWritableFileOrDir(self.values[rowNo]["path"], False, True):
                        if self.isRowHidden(rowNo):
                            fu.removeFileOrDir(self.values[rowNo]["path"])
                            self.changedValueNumber += 1
                        else:
                            pathOfParentDirectory = str(
                                self.values[rowNo]["pathOfParentDirectory"])
                            baseName = str(self.values[rowNo]["baseName"])
                            if self.isChangeableItem(rowNo, "sourceCover") or self.isChangeableItem(rowNo, "destinationCover"):
                                sourcePath = self.values[rowNo]["sourceCover"]
                                destinationPath = self.values[rowNo]["destinationCover"]
                                if self.isChangeableItem(rowNo, "sourceCover"):
                                    sourcePath = str(self.item(rowNo, 3).text()).strip()
                                if self.isChangeableItem(rowNo, "destinationCover"):
                                    destinationPath = str(self.item(rowNo, 4).text()).strip()
                                if (str(self.item(rowNo,
                                                  2).text()) != sourcePath or sourcePath != destinationPath or str(
                                    self.item(rowNo, 2).text()) != destinationPath) or (
                                            str(self.item(rowNo, 2).text()) !=
                                            self.values[rowNo]["currentCover"] and (
                                                str(self.item(rowNo, 2).text()) != sourcePath and str(
                                            self.item(rowNo, 2).text()) != destinationPath)):
                                    if str(self.item(rowNo, 3).text()).strip() != "":
                                        sourcePath = fu.getRealPath(sourcePath,
                                                                    self.values[rowNo]["path"])
                                        sourcePath = fu.checkSource(sourcePath, "file")
                                        if sourcePath is not None:
                                            if destinationPath != "":
                                                destinationPath = fu.getRealPath(destinationPath,
                                                                                 self.values[
                                                                                     rowNo]["path"])
                                                if sourcePath != destinationPath:
                                                    destinationPath = fu.moveOrChange(sourcePath, destinationPath)
                                            else:
                                                destinationPath = sourcePath
                                            fu.setIconToDirectory(self.values[rowNo]["path"],
                                                                  destinationPath)
                                            self.changedValueNumber += 1
                                    else:
                                        fu.setIconToDirectory(self.values[rowNo]["path"], "")
                                        self.changedValueNumber += 1
                            if self.isChangeableItem(rowNo, "baseNameOfDirectory", pathOfParentDirectory):
                                pathOfParentDirectory = str(self.item(rowNo, 0).text())
                                self.changedValueNumber += 1
                            if self.isChangeableItem(rowNo, "baseName", baseName, False):
                                baseName = str(self.item(rowNo, 1).text())
                                self.changedValueNumber += 1
                            newFilePath = fu.joinPath(pathOfParentDirectory, baseName)
                            oldFilePath = fu.getRealPath(self.values[rowNo]["path"])
                            newFilePath = fu.getRealPath(newFilePath)
                            if oldFilePath != newFilePath:
                                oldAndNewPaths = {}
                                oldAndNewPaths["oldPath"] = oldFilePath
                                oldAndNewPaths["newPath"] = fu.moveOrChange(oldFilePath, newFilePath, "directory")
                                if oldFilePath != oldAndNewPaths["newPath"]:
                                    oldAndNewPathValues.append(oldAndNewPaths)
                                    oldDirName = fu.getDirName(oldFilePath)
                                    if uni.getBoolValue("isClearEmptyDirectoriesWhenFileMove"):
                                        fu.checkEmptyDirectories(oldDirName, True, True,
                                                                 uni.getBoolValue("isAutoCleanSubFolderWhenFileMove"))
                except:
                    ReportBug.ReportBug()
            else:
                allItemNumber = rowNo + 1
            Dialogs.showState(translate("FileUtils/Covers", "Writing Cover Informations"), rowNo + 1, allItemNumber,
                              True)
            if isContinueThreadAction is False:
                break
        uni.finishThreadAction()
        if len(oldAndNewPathValues) > 0:
            from Amarok import Operations

            Operations.changePaths(oldAndNewPathValues)
        return True

    def correctTable(self):
        for rowNo in range(self.rowCount()):
            for coloumKey in self.getWritableColumnKeys():
                coloumNo = self.getColumnNoFromKey(coloumKey)
                if self.isChangeableItem(rowNo, coloumKey):
                    if coloumKey == "baseNameOfDirectory" or coloumKey == "baseName":
                        newString = Organizer.emend(str(self.item(rowNo, coloumNo).text()), "directory")
                    elif coloumKey == "currentCover" or coloumKey == "sourceCover":
                        newString = str(str(self.item(rowNo, coloumNo).text()))
                    else:
                        newString = Organizer.emend(str(self.item(rowNo, coloumNo).text()), "file")
                    self.item(rowNo, coloumNo).setText(str(newString))

    def showTableDetails(self, _fileNo, _infoNo):
        directoryPathOfCover = self.values[_fileNo]["path"]
        coverValues = [directoryPathOfCover,
                       fu.getRealPath(str(self.item(_fileNo, 2).text()), directoryPathOfCover),
                       fu.getRealPath(str(self.item(_fileNo, 3).text()), directoryPathOfCover),
                       fu.getRealPath(str(self.item(_fileNo, 4).text()), directoryPathOfCover)]
        CoverDetails.CoverDetails(coverValues, uni.getBoolValue("isOpenDetailsInNewWindow"), _infoNo)

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
            Dialogs.showError(translate("AmarokCoverTable", "Cannot Open File"),
                              str(translate("AmarokCoverTable",
                                            "\"%s\" : cannot be opened. Please make sure that you selected a text file.")
                              ) % Organizer.getLink(self.values[_row]["path"]))

    def setItemColor(self, _item, _rowNo, _itemNo, _name):
        if _item is not None:
            if _name in self.values[_rowNo]["flagColor"]:
                r, g, b = self.values[_rowNo]["flagColor"][_name]
                _item.setBackground(MBrush(MColor(r, g, b)))

