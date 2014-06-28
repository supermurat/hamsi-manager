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


class CoverTable(CoreTable):
    def __init__(self, *args, **kwargs):
        CoreTable.__init__(self, *args, **kwargs)
        self.keyName = "cover"
        self.hiddenTableColumnsSettingKey = "hiddenCoverTableColumns"
        self.refreshColumns()
        if uni.isActiveAmarok:
            pbtnGetFromAmarok = MPushButton(translate("CoverTable", "Get From Amarok"))
            MObject.connect(pbtnGetFromAmarok, SIGNAL("clicked()"), self.getFromAmarok)
            self.hblBox.insertWidget(self.hblBox.count() - 1, pbtnGetFromAmarok)

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
        self.changedValueNumber = 0
        changingFileDirectories = []
        isNewDirectoriesSame = True
        isMovedToNewDirectory = False
        currentDirectoryPath = ""
        newDirectoryPath = ""
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
                            baseNameOfDirectory = str(
                                self.currentTableContentValues[rowNo]["baseNameOfDirectory"])
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
                            if self.isChangeableItem(rowNo, 0, baseNameOfDirectory):
                                baseNameOfDirectory = str(self.item(rowNo, 0).text())
                                self.changedValueNumber += 1
                                isMovedToNewDirectory = True
                                currentDirectoryPath = fu.getDirName(
                                    self.currentTableContentValues[rowNo]["path"])
                                newDirectoryPath = fu.joinPath(
                                    fu.getDirName(fu.getDirName(self.currentTableContentValues[rowNo]["path"])),
                                    baseNameOfDirectory)
                                self.setNewDirectory(newDirectoryPath)
                                if rowNo > 0:
                                    if str(self.item(rowNo - 1, 0).text()) != baseNameOfDirectory:
                                        isNewDirectoriesSame = False
                            if self.isChangeableItem(rowNo, 1, baseName, False):
                                baseName = str(self.item(rowNo, 1).text())
                                self.changedValueNumber += 1
                            newFilePath = fu.joinPath(
                                fu.getDirName(fu.getDirName(self.currentTableContentValues[rowNo]["path"])),
                                baseNameOfDirectory, baseName)
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
        fu.changeDirectories(changingFileDirectories)
        if self.rowCount() == len(changingFileDirectories) and isMovedToNewDirectory and isNewDirectoriesSame:
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
            Dialogs.showError(translate("CoverTable", "Cannot Open File"),
                              str(translate("CoverTable",
                                            "\"%s\" : cannot be opened. Please make sure that you selected a text file.")
                              ) % Organizer.getLink(self.currentTableContentValues[_row]["path"]))

    def refreshColumns(self):
        self.tableColumns = [translate("CoverTable", "Directory"),
                                   translate("CoverTable", "Directory Name"),
                                   translate("CoverTable", "Current Cover"),
                                   translate("CoverTable", "Source Cover"),
                                   translate("CoverTable", "Destination Cover")]
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
                    newString = Organizer.emend(self.currentTableContentValues[rowNo]["baseNameOfDirectory"],
                                                "directory")
                    item = self.createTableWidgetItem(newString, self.currentTableContentValues[rowNo][
                        "baseNameOfDirectory"])
                elif itemNo == 1:
                    newString = Organizer.emend(self.currentTableContentValues[rowNo]["baseName"], "directory")
                    item = self.createTableWidgetItem(newString,
                                                      self.currentTableContentValues[rowNo]["baseName"])
                elif itemNo == 2:
                    newString = str(self.currentTableContentValues[rowNo]["currentCover"])
                    newString = newString.replace(self.currentTableContentValues[rowNo]["path"], ".")
                    item = self.createTableWidgetItem(newString, newString, True)
                elif itemNo == 3:
                    newString = str(self.currentTableContentValues[rowNo]["sourceCover"])
                    newString = newString.replace(self.currentTableContentValues[rowNo]["path"], ".")
                    oldString = self.currentTableContentValues[rowNo]["currentCover"]
                    oldString = oldString.replace(self.currentTableContentValues[rowNo]["path"], ".")
                    item = self.createTableWidgetItem(newString, oldString)
                elif itemNo == 4:
                    newString = self.currentTableContentValues[rowNo]["destinationCover"]
                    newString = newString.replace(self.currentTableContentValues[rowNo]["path"], ".")
                    newString = Organizer.emend(newString, "file")
                    oldString = self.currentTableContentValues[rowNo]["currentCover"]
                    oldString = oldString.replace(self.currentTableContentValues[rowNo]["path"], ".")
                    item = self.createTableWidgetItem(newString, oldString)
                if item != None:
                    self.setItem(rowNo, itemNo, item)
            if self.currentTableContentValues[rowNo]["isCorrectedFileContent"] == False:
                item = self.item(rowNo, 2)
                if item != None:
                    item.setBackground(MBrush(MColor(255, 163, 163)))
            Dialogs.showState(translate("Tables", "Generating .."), rowNo + 1, allItemNumber)

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
                    for rowNo in range(self.rowCount()):
                        if getMainWindow().checkHiddenColumn(3) and getMainWindow().checkHiddenColumn(4):
                            if self.isChangeableItem(rowNo, 3):
                                directoryPath = fu.joinPath(
                                    fu.getDirName(fu.getDirName(self.currentTableContentValues[rowNo]["path"])),
                                    str(self.item(rowNo, 0).text()), str(self.item(rowNo, 1).text()))
                                if directoryPath in directoriesAndValues:
                                    directoryAndValues = directoriesAndValues[directoryPath]
                                    self.item(rowNo, 3).setText(
                                        directoryAndValues["coverPath"][0].replace(directoryPath, "."))
                                    self.item(rowNo, 4).setText("./" + Organizer.getIconName(
                                        directoryAndValues["artist"][0],
                                        directoryAndValues["album"][0],
                                        directoryAndValues["genre"][0],
                                        directoryAndValues["year"][0]))
        except:
            ReportBug.ReportBug()

    def getValueByRowAndColumn(self, _rowNo, _columnNo):
        if _columnNo == 0:
            return self.currentTableContentValues[_rowNo]["baseNameOfDirectory"]
        elif _columnNo == 1:
            return self.currentTableContentValues[_rowNo]["baseName"]
        elif _columnNo == 2:
            return self.currentTableContentValues[_rowNo]["currentCover"].replace(
                self.currentTableContentValues[_rowNo]["path"], ".")
        elif _columnNo == 3:
            return self.currentTableContentValues[_rowNo]["sourceCover"].replace(
                self.currentTableContentValues[_rowNo]["path"], ".")
        elif _columnNo == 4:
            return self.currentTableContentValues[_rowNo]["destinationCover"].replace(
                self.currentTableContentValues[_rowNo]["path"], ".")
        return ""
