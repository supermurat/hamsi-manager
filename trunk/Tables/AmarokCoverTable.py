# # This file is part of HamsiManager.
# #
# # Copyright (c) 2010 - 2013 Murat Demir <mopened@gmail.com>
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
from Core import Universals as uni
from Core import ReportBug
from Tables import CoreTable


class AmarokCoverTable(CoreTable):
    def __init__(self, *args, **kwargs):
        CoreTable.__init__(self, *args, **kwargs)
        from Amarok import Filter

        self.keyName = "cover"
        self.amarokFilterKeyName = "AmarokFilterAmarokCoverTable"
        self.hiddenTableColumnsSettingKey = "hiddenAmarokCoverTableColumns"
        self.refreshColumns()
        self.wFilter = Filter.FilterWidget(self, self.amarokFilterKeyName)
        getMainWindow().MainLayout.addWidget(self.wFilter)

    def readContents(self, _directoryPath):
        currentTableContentValues = []
        uni.startThreadAction()
        import Amarok

        Dialogs.showState(translate("AmarokCoverTable", "Checking For Amarok..."), 0, 2)
        if Amarok.checkAmarok():
            Dialogs.showState(translate("AmarokCoverTable", "Getting Values From Amarok"), 1, 2)
            isContinueThreadAction = uni.isContinueThreadAction()
            if isContinueThreadAction:
                from Amarok import Operations

                directoriesAndValues = Operations.getDirectoriesAndValues(uni.MySettings[self.amarokFilterKeyName])
                Dialogs.showState(translate("AmarokCoverTable", "Values Are Being Processed"), 2, 2)
                isContinueThreadAction = uni.isContinueThreadAction()
                if isContinueThreadAction:
                    if directoriesAndValues != None:
                        allItemNumber = len(directoriesAndValues)
                        dirNo = 0
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
                                        if currentCover == None:
                                            currentCover = ""
                                        content["currentCover"] = (currentCover)
                                        content["sourceCover"] = (dirRow["coverPath"][0].replace(dirPath, "."))
                                        content["destinationCover"] = ("./" + Organizer.getIconName(
                                            dirRow["artist"][0],
                                            dirRow["album"][0],
                                            dirRow["genre"][0],
                                            dirRow["year"][0]))
                                        content["flagColor"] = {}
                                        if isCorrectedFileContent == False:
                                            content["flagColor"]["currentCover"] = 255, 163, 163
                                        if fu.isFile(content["sourceCover"]) == False:
                                            content["flagColor"]["sourceCover"] = 255, 163, 163
                                        currentTableContentValues.append(content)
                                except:
                                    ReportBug.ReportBug()
                            else:
                                allItemNumber = dirNo + 1
                            Dialogs.showState(translate("FileUtils/Covers", "Reading Cover Informations"),
                                              dirNo + 1, allItemNumber, True)
                            dirNo += 1
                            if isContinueThreadAction == False:
                                break
        uni.finishThreadAction()
        return currentTableContentValues

    def writeContents(self):
        self.changedValueNumber = 0
        changingFileDirectories = []
        startRowNo, rowStep = 0, 1
        uni.startThreadAction()
        allItemNumber = len(self.currentTableContentValues)
        Dialogs.showState(translate("FileUtils/Covers", "Writing Cover Informations"), 0, allItemNumber, True)
        for rowNo in range(startRowNo, self.rowCount(), rowStep):
            isContinueThreadAction = uni.isContinueThreadAction()
            if isContinueThreadAction:
                try:
                    if fu.isWritableFileOrDir(self.currentTableContentValues[rowNo]["path"], False, True):
                        if self.isRowHidden(rowNo):
                            fu.removeFileOrDir(self.currentTableContentValues[rowNo]["path"])
                            self.changedValueNumber += 1
                        else:
                            pathOfParentDirectory = str(
                                self.currentTableContentValues[rowNo]["pathOfParentDirectory"])
                            baseName = str(self.currentTableContentValues[rowNo]["baseName"])
                            if self.isChangeableItem(rowNo, 3) or self.isChangeableItem(rowNo, 4):
                                sourcePath = self.currentTableContentValues[rowNo]["sourceCover"]
                                destinationPath = self.currentTableContentValues[rowNo]["destinationCover"]
                                if self.isChangeableItem(rowNo, 3):
                                    sourcePath = str(self.item(rowNo, 3).text()).strip()
                                if self.isChangeableItem(rowNo, 4):
                                    destinationPath = str(self.item(rowNo, 4).text()).strip()
                                if (str(self.item(rowNo,
                                                        2).text()) != sourcePath or sourcePath != destinationPath or str(
                                    self.item(rowNo, 2).text()) != destinationPath) or (
                                            str(self.item(rowNo, 2).text()) !=
                                            self.currentTableContentValues[rowNo]["currentCover"] and (
                                                str(self.item(rowNo, 2).text()) != sourcePath and str(
                                            self.item(rowNo, 2).text()) != destinationPath)):
                                    if str(self.item(rowNo, 3).text()).strip() != "":
                                        sourcePath = fu.getRealPath(sourcePath,
                                                                    self.currentTableContentValues[rowNo]["path"])
                                        sourcePath = fu.checkSource(sourcePath, "file")
                                        if sourcePath is not None:
                                            if destinationPath != "":
                                                destinationPath = fu.getRealPath(destinationPath,
                                                                                 self.currentTableContentValues[
                                                                                     rowNo]["path"])
                                                if sourcePath != destinationPath:
                                                    destinationPath = fu.moveOrChange(sourcePath, destinationPath)
                                            else:
                                                destinationPath = sourcePath
                                            fu.setIconToDirectory(self.currentTableContentValues[rowNo]["path"],
                                                                  destinationPath)
                                            self.changedValueNumber += 1
                                    else:
                                        fu.setIconToDirectory(self.currentTableContentValues[rowNo]["path"], "")
                                        self.changedValueNumber += 1
                            if self.isChangeableItem(rowNo, 0, pathOfParentDirectory):
                                pathOfParentDirectory = str(self.item(rowNo, 0).text())
                                self.changedValueNumber += 1
                            if self.isChangeableItem(rowNo, 1, baseName, False):
                                baseName = str(self.item(rowNo, 1).text())
                                self.changedValueNumber += 1
                            newFilePath = fu.joinPath(pathOfParentDirectory, baseName)
                            if fu.getRealPath(self.currentTableContentValues[rowNo]["path"]) != fu.getRealPath(
                                newFilePath):
                                changingFileDirectories.append([self.currentTableContentValues[rowNo]["path"],
                                                                newFilePath])
                except:
                    ReportBug.ReportBug()
            else:
                allItemNumber = rowNo + 1
            Dialogs.showState(translate("FileUtils/Covers", "Writing Cover Informations"), rowNo + 1, allItemNumber,
                              True)
            if isContinueThreadAction == False:
                break
        uni.finishThreadAction()
        pathValues = fu.changeDirectories(changingFileDirectories)
        from Amarok import Operations

        Operations.changePaths(pathValues)
        return True

    def showTableDetails(self, _fileNo, _infoNo):
        directoryPathOfCover = self.currentTableContentValues[_fileNo]["path"]
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
                              ) % Organizer.getLink(self.currentTableContentValues[_row]["path"]))

    def refreshColumns(self):
        self.tableColumns = [translate("AmarokCoverTable", "Directory"),
                                   translate("AmarokCoverTable", "Directory Name"),
                                   translate("AmarokCoverTable", "Current Cover"),
                                   translate("AmarokCoverTable", "Source Cover"),
                                   translate("AmarokCoverTable", "Destination Cover")]
        self.tableColumnsKey = ["Directory", "Directory Name", "Current Cover", "Source Cover",
                                      "Destination Cover"]

    def saveTable(self):
        self.checkFileExtensions(4, 3)
        return self.writeContents()

    def refreshTable(self, _path):
        self.currentTableContentValues = self.readContents(_path)
        self.setRowCount(len(self.currentTableContentValues))
        allItemNumber = self.rowCount()
        for rowNo in range(allItemNumber):
            for itemNo in range(5):
                item = None
                if itemNo == 0:
                    newString = Organizer.emend(self.currentTableContentValues[rowNo]["pathOfParentDirectory"],
                                                "directory")
                    item = self.createTableWidgetItem(newString, self.currentTableContentValues[rowNo][
                        "pathOfParentDirectory"])
                elif itemNo == 1:
                    newString = Organizer.emend(self.currentTableContentValues[rowNo]["baseName"], "directory")
                    item = self.createTableWidgetItem(newString,
                                                      self.currentTableContentValues[rowNo]["baseName"])
                elif itemNo == 2:
                    newString = fu.getShortPath(self.currentTableContentValues[rowNo]["currentCover"],
                                                self.currentTableContentValues[rowNo]["path"])
                    item = self.createTableWidgetItem(newString, newString, True)
                    self.setItemColor(item, rowNo, itemNo, "currentCover")
                elif itemNo == 3:
                    newString = fu.getShortPath(self.currentTableContentValues[rowNo]["sourceCover"],
                                                self.currentTableContentValues[rowNo]["path"])
                    item = self.createTableWidgetItem(newString, fu.getShortPath(
                        self.currentTableContentValues[rowNo]["currentCover"],
                        self.currentTableContentValues[rowNo]["path"]))
                    self.setItemColor(item, rowNo, itemNo, "sourceCover")
                elif itemNo == 4:
                    newString = Organizer.emend(
                        fu.getShortPath(self.currentTableContentValues[rowNo]["destinationCover"],
                                        self.currentTableContentValues[rowNo]["path"]), "file")
                    item = self.createTableWidgetItem(newString, fu.getShortPath(
                        self.currentTableContentValues[rowNo]["currentCover"],
                        self.currentTableContentValues[rowNo]["path"]))
                    self.setItemColor(item, rowNo, itemNo, "destinationCover")
                if item != None:
                    self.setItem(rowNo, itemNo, item)
            Dialogs.showState(translate("Tables", "Generating .."), rowNo + 1, allItemNumber)

    def setItemColor(self, _item, _rowNo, _itemNo, _name):
        if _item != None:
            if _name in self.currentTableContentValues[_rowNo]["flagColor"]:
                r, g, b = self.currentTableContentValues[_rowNo]["flagColor"][_name]
                _item.setBackground(MBrush(MColor(r, g, b)))

    def correctTable(self):
        for rowNo in range(self.rowCount()):
            for itemNo in range(self.columnCount()):
                if self.isChangeableItem(rowNo, itemNo):
                    if itemNo == 0 or itemNo == 1:
                        newString = Organizer.emend(str(self.item(rowNo, itemNo).text()), "directory")
                    elif itemNo == 2 or itemNo == 3:
                        newString = str(str(self.item(rowNo, itemNo).text()))
                    else:
                        newString = Organizer.emend(str(self.item(rowNo, itemNo).text()), "file")
                    self.item(rowNo, itemNo).setText(str(newString))

    def getValueByRowAndColumn(self, _rowNo, _columnNo):
        if _columnNo == 0:
            return self.currentTableContentValues[_rowNo]["baseNameOfDirectory"]
        elif _columnNo == 1:
            return self.currentTableContentValues[_rowNo]["baseName"]
        elif _columnNo == 2:
            return fu.getShortPath(self.currentTableContentValues[_rowNo]["currentCover"],
                                   self.currentTableContentValues[_rowNo]["path"])
        elif _columnNo == 3:
            return fu.getShortPath(self.currentTableContentValues[_rowNo]["sourceCover"],
                                   self.currentTableContentValues[_rowNo]["path"])
        elif _columnNo == 4:
            return fu.getShortPath(self.currentTableContentValues[_rowNo]["destinationCover"],
                                   self.currentTableContentValues[_rowNo]["path"])
        return ""



