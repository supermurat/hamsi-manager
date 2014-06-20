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
from Details import CoverDetails
from Core import Dialogs
from time import gmtime
from Core import Universals as uni
from Core import ReportBug


class CoverTable():
    def __init__(self, _table):
        self.Table = _table
        self.keyName = "cover"
        self.hiddenTableColumnsSettingKey = "hiddenCoverTableColumns"
        self.refreshColumns()
        if uni.isActiveAmarok:
            pbtnGetFromAmarok = MPushButton(translate("CoverTable", "Get From Amarok"))
            MObject.connect(pbtnGetFromAmarok, SIGNAL("clicked()"), self.getFromAmarok)
            self.Table.hblBox.insertWidget(self.Table.hblBox.count() - 1, pbtnGetFromAmarok)

    def readContents(self, _directoryPath):
        currentTableContentValues = []
        allFilesAndDirectories = fu.readDirectoryWithSubDirectoriesThread(_directoryPath,
                                                                          int(uni.MySettings["CoversSubDirectoryDeep"]),
                                                                          "directory",
                                                                          uni.getBoolValue("isShowHiddensInCoverTable"))
        allItemNumber = len(allFilesAndDirectories)
        uni.startThreadAction()
        for dirNo, dirName in enumerate(allFilesAndDirectories):
            isContinueThreadAction = uni.isContinueThreadAction()
            if isContinueThreadAction:
                try:
                    if fu.isReadableFileOrDir(dirName, False, True) and fu.isReadableFileOrDir(
                        fu.joinPath(dirName, ".directory"), False, True):
                        content = {}
                        content["path"] = dirName
                        content["baseNameOfDirectory"] = str(str(fu.getBaseName(_directoryPath)) +
                                                             str(fu.getDirName(dirName)).replace(_directoryPath, ""))
                        content["baseName"] = fu.getBaseName(dirName)

                        currentCover, isCorrectedFileContent = fu.getIconFromDirectory(dirName)
                        selectedName = None
                        if isCorrectedFileContent and currentCover != None:
                            selectedName = fu.getBaseName(currentCover)
                        sourceCover = fu.getFirstImageInDirectory(dirName, selectedName, False, False)
                        if currentCover == None:
                            currentCover = ""
                        if sourceCover == None:
                            sourceCover = ""
                        else:
                            sourceCover = fu.joinPath(dirName, sourceCover)
                        content["currentCover"] = (currentCover)
                        content["sourceCover"] = (sourceCover)
                        content["destinationCover"] = (sourceCover)
                        content["isCorrectedFileContent"] = (isCorrectedFileContent)
                        currentTableContentValues.append(content)
                except:
                    ReportBug.ReportBug()
            else:
                allItemNumber = dirNo + 1
            Dialogs.showState(translate("FileUtils/Covers", "Reading Cover Informations"),
                              dirNo + 1, allItemNumber, True)
            if isContinueThreadAction == False:
                break
        uni.finishThreadAction()
        return currentTableContentValues

    def writeContents(self):
        self.Table.changedValueNumber = 0
        changingFileDirectories = []
        isNewDirectoriesSame = True
        isMovedToNewDirectory = False
        currentDirectoryPath = ""
        newDirectoryPath = ""
        startRowNo, rowStep = 0, 1
        uni.startThreadAction()
        allItemNumber = len(self.Table.currentTableContentValues)
        Dialogs.showState(translate("FileUtils/Covers", "Writing Cover Informations"), 0, allItemNumber, True)
        for rowNo in range(startRowNo, self.Table.rowCount(), rowStep):
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
                            if self.Table.isChangeableItem(rowNo, 3) or self.Table.isChangeableItem(rowNo, 4):
                                sourcePath = self.Table.currentTableContentValues[rowNo]["sourceCover"]
                                destinationPath = self.Table.currentTableContentValues[rowNo]["destinationCover"]
                                if self.Table.isChangeableItem(rowNo, 3):
                                    sourcePath = str(self.Table.item(rowNo, 3).text()).strip()
                                if self.Table.isChangeableItem(rowNo, 4):
                                    destinationPath = str(self.Table.item(rowNo, 4).text()).strip()
                                if (str(self.Table.item(rowNo,
                                                        2).text()) != sourcePath or sourcePath != destinationPath or str(
                                    self.Table.item(rowNo, 2).text()) != destinationPath) or (
                                            str(self.Table.item(rowNo, 2).text()) !=
                                            self.Table.currentTableContentValues[rowNo]["currentCover"] and (
                                                str(self.Table.item(rowNo, 2).text()) != sourcePath and str(
                                            self.Table.item(rowNo, 2).text()) != destinationPath)):
                                    if str(self.Table.item(rowNo, 3).text()).strip() != "":
                                        sourcePath = fu.getRealPath(sourcePath,
                                                                    self.Table.currentTableContentValues[rowNo]["path"])
                                        sourcePath = fu.checkSource(sourcePath, "file")
                                        if sourcePath is not None:
                                            if destinationPath != "":
                                                destinationPath = fu.getRealPath(destinationPath,
                                                                                 self.Table.currentTableContentValues[
                                                                                     rowNo]["path"])
                                                if sourcePath != destinationPath:
                                                    destinationPath = fu.moveOrChange(sourcePath, destinationPath)
                                            else:
                                                destinationPath = sourcePath
                                            fu.setIconToDirectory(self.Table.currentTableContentValues[rowNo]["path"],
                                                                  destinationPath)
                                            self.Table.changedValueNumber += 1
                                    else:
                                        fu.setIconToDirectory(self.Table.currentTableContentValues[rowNo]["path"], "")
                                        self.Table.changedValueNumber += 1
                            if self.Table.isChangeableItem(rowNo, 0, baseNameOfDirectory):
                                baseNameOfDirectory = str(self.Table.item(rowNo, 0).text())
                                self.Table.changedValueNumber += 1
                                isMovedToNewDirectory = True
                                currentDirectoryPath = fu.getDirName(
                                    self.Table.currentTableContentValues[rowNo]["path"])
                                newDirectoryPath = fu.joinPath(
                                    fu.getDirName(fu.getDirName(self.Table.currentTableContentValues[rowNo]["path"])),
                                    baseNameOfDirectory)
                                self.Table.setNewDirectory(newDirectoryPath)
                                if rowNo > 0:
                                    if str(self.Table.item(rowNo - 1, 0).text()) != baseNameOfDirectory:
                                        isNewDirectoriesSame = False
                            if self.Table.isChangeableItem(rowNo, 1, baseName, False):
                                baseName = str(self.Table.item(rowNo, 1).text())
                                self.Table.changedValueNumber += 1
                            newFilePath = fu.joinPath(
                                fu.getDirName(fu.getDirName(self.Table.currentTableContentValues[rowNo]["path"])),
                                baseNameOfDirectory, baseName)
                            if fu.getRealPath(self.Table.currentTableContentValues[rowNo]["path"]) != fu.getRealPath(
                                newFilePath):
                                changingFileDirectories.append([self.Table.currentTableContentValues[rowNo]["path"],
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
        fu.changeDirectories(changingFileDirectories)
        if self.Table.rowCount() == len(changingFileDirectories) and isMovedToNewDirectory and isNewDirectoriesSame:
            otherFileNames = fu.readDirectory(currentDirectoryPath, "fileAndDirectory", True)
            if len(otherFileNames) > 0:
                answer = Dialogs.ask(translate("FileUtils/Musics", "There Are More Files"),
                                     str(translate("FileUtils/Musics",
                                                   "\"%s\" : there are more files in this directory.<br>Are you want to move all found files into new directory?<br>New Directory : \"%s\"")) % (
                                         Organizer.getLink(currentDirectoryPath), Organizer.getLink(newDirectoryPath)))
                if answer == Dialogs.Yes:
                    changingOtherFileDirectories = []
                    for fileName in otherFileNames:
                        changingOtherFileDirectories.append(
                            [fu.joinPath(currentDirectoryPath, fileName), fu.joinPath(newDirectoryPath, fileName)])
                    fu.changeDirectories(changingOtherFileDirectories)
        return True

    def showDetails(self, _fileNo, _infoNo):
        directoryPathOfCover = self.Table.currentTableContentValues[_fileNo]["path"]
        coverValues = [directoryPathOfCover,
                       fu.getRealPath(str(self.Table.item(_fileNo, 2).text()), directoryPathOfCover),
                       fu.getRealPath(str(self.Table.item(_fileNo, 3).text()), directoryPathOfCover),
                       fu.getRealPath(str(self.Table.item(_fileNo, 4).text()), directoryPathOfCover)]
        CoverDetails.CoverDetails(coverValues, uni.getBoolValue("isOpenDetailsInNewWindow"), _infoNo)

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
            Dialogs.showError(translate("CoverTable", "Cannot Open File"),
                              str(translate("CoverTable",
                                            "\"%s\" : cannot be opened. Please make sure that you selected a text file.")
                              ) % Organizer.getLink(self.Table.currentTableContentValues[_row]["path"]))

    def refreshColumns(self):
        self.Table.tableColumns = [translate("CoverTable", "Directory"),
                                   translate("CoverTable", "Directory Name"),
                                   translate("CoverTable", "Current Cover"),
                                   translate("CoverTable", "Source Cover"),
                                   translate("CoverTable", "Destination Cover")]
        self.Table.tableColumnsKey = ["Directory", "Directory Name", "Current Cover", "Source Cover",
                                      "Destination Cover"]

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
                if itemNo == 0:
                    newString = Organizer.emend(self.Table.currentTableContentValues[rowNo]["baseNameOfDirectory"],
                                                "directory")
                    item = self.Table.createTableWidgetItem(newString, self.Table.currentTableContentValues[rowNo][
                        "baseNameOfDirectory"])
                elif itemNo == 1:
                    newString = Organizer.emend(self.Table.currentTableContentValues[rowNo]["baseName"], "directory")
                    item = self.Table.createTableWidgetItem(newString,
                                                            self.Table.currentTableContentValues[rowNo]["baseName"])
                elif itemNo == 2:
                    newString = str(self.Table.currentTableContentValues[rowNo]["currentCover"])
                    newString = newString.replace(self.Table.currentTableContentValues[rowNo]["path"], ".")
                    item = self.Table.createTableWidgetItem(newString, newString, True)
                elif itemNo == 3:
                    newString = str(self.Table.currentTableContentValues[rowNo]["sourceCover"])
                    newString = newString.replace(self.Table.currentTableContentValues[rowNo]["path"], ".")
                    oldString = self.Table.currentTableContentValues[rowNo]["currentCover"]
                    oldString = oldString.replace(self.Table.currentTableContentValues[rowNo]["path"], ".")
                    item = self.Table.createTableWidgetItem(newString, oldString)
                elif itemNo == 4:
                    newString = self.Table.currentTableContentValues[rowNo]["destinationCover"]
                    newString = newString.replace(self.Table.currentTableContentValues[rowNo]["path"], ".")
                    newString = Organizer.emend(newString, "file")
                    oldString = self.Table.currentTableContentValues[rowNo]["currentCover"]
                    oldString = oldString.replace(self.Table.currentTableContentValues[rowNo]["path"], ".")
                    item = self.Table.createTableWidgetItem(newString, oldString)
                if item != None:
                    self.Table.setItem(rowNo, itemNo, item)
            if self.Table.currentTableContentValues[rowNo]["isCorrectedFileContent"] == False:
                item = self.Table.item(rowNo, 2)
                if item != None:
                    item.setBackground(MBrush(MColor(255, 163, 163)))
            Dialogs.showState(translate("FileUtils/Tables", "Generating Table..."), rowNo + 1, allItemNumber)

    def correctTable(self):
        for rowNo in range(self.Table.rowCount()):
            for itemNo in range(self.Table.columnCount()):
                if self.Table.isChangeableItem(rowNo, itemNo):
                    if itemNo == 0 or itemNo == 1:
                        newString = Organizer.emend(str(self.Table.item(rowNo, itemNo).text()), "directory")
                    elif itemNo == 2 or itemNo == 3:
                        newString = str(str(self.Table.item(rowNo, itemNo).text()))
                    else:
                        newString = Organizer.emend(str(self.Table.item(rowNo, itemNo).text()), "file")
                    self.Table.item(rowNo, itemNo).setText(str(newString))

    def getFromAmarok(self):
        try:
            import Amarok

            Dialogs.showState(translate("CoverTable", "Checking For Amarok..."), 0, 2)
            if Amarok.checkAmarok():
                Dialogs.showState(translate("CoverTable", "Getting Values From Amarok"), 1, 2)
                from Amarok import Operations

                directoriesAndValues = Operations.getDirectoriesAndValues()
                Dialogs.showState(translate("CoverTable", "Values Are Being Processed"), 2, 2)
                if directoriesAndValues != None:
                    for rowNo in range(self.Table.rowCount()):
                        if getMainWindow().Table.checkHiddenColumn(3) and getMainWindow().Table.checkHiddenColumn(4):
                            if self.Table.isChangeableItem(rowNo, 3):
                                directoryPath = fu.joinPath(
                                    fu.getDirName(fu.getDirName(self.Table.currentTableContentValues[rowNo]["path"])),
                                    str(self.Table.item(rowNo, 0).text()), str(self.Table.item(rowNo, 1).text()))
                                if directoryPath in directoriesAndValues:
                                    directoryAndValues = directoriesAndValues[directoryPath]
                                    self.Table.item(rowNo, 3).setText(
                                        directoryAndValues["coverPath"][0].replace(directoryPath, "."))
                                    self.Table.item(rowNo, 4).setText("./" + Organizer.getIconName(
                                        directoryAndValues["artist"][0],
                                        directoryAndValues["album"][0],
                                        directoryAndValues["genre"][0],
                                        directoryAndValues["year"][0]))
        except:
            ReportBug.ReportBug()

    def getValueByRowAndColumn(self, _rowNo, _columnNo):
        if _columnNo == 0:
            return self.Table.currentTableContentValues[_rowNo]["baseNameOfDirectory"]
        elif _columnNo == 1:
            return self.Table.currentTableContentValues[_rowNo]["baseName"]
        elif _columnNo == 2:
            return self.Table.currentTableContentValues[_rowNo]["currentCover"].replace(
                self.Table.currentTableContentValues[_rowNo]["path"], ".")
        elif _columnNo == 3:
            return self.Table.currentTableContentValues[_rowNo]["sourceCover"].replace(
                self.Table.currentTableContentValues[_rowNo]["path"], ".")
        elif _columnNo == 4:
            return self.Table.currentTableContentValues[_rowNo]["destinationCover"].replace(
                self.Table.currentTableContentValues[_rowNo]["path"], ".")
        return ""
