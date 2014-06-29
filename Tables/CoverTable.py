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

    def writeContents(self):
        self.changedValueNumber = 0
        changingFileDirectories = []
        isNewDirectoriesSame = True
        isMovedToNewDirectory = False
        currentDirectoryPath = ""
        newDirectoryPath = ""
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
                            baseNameOfDirectory = str(
                                self.values[rowNo]["baseNameOfDirectory"])
                            baseName = str(self.values[rowNo]["baseName"])
                            if self.isChangeableItem(rowNo, 3) or self.isChangeableItem(rowNo, 4):
                                sourcePath = self.values[rowNo]["sourceCover"]
                                destinationPath = self.values[rowNo]["destinationCover"]
                                if self.isChangeableItem(rowNo, 3):
                                    sourcePath = str(self.item(rowNo, 3).text()).strip()
                                if self.isChangeableItem(rowNo, 4):
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
                            if self.isChangeableItem(rowNo, 0, baseNameOfDirectory):
                                baseNameOfDirectory = str(self.item(rowNo, 0).text())
                                self.changedValueNumber += 1
                                isMovedToNewDirectory = True
                                currentDirectoryPath = fu.getDirName(
                                    self.values[rowNo]["path"])
                                newDirectoryPath = fu.joinPath(
                                    fu.getDirName(fu.getDirName(self.values[rowNo]["path"])),
                                    baseNameOfDirectory)
                                self.setNewDirectory(newDirectoryPath)
                                if rowNo > 0:
                                    if str(self.item(rowNo - 1, 0).text()) != baseNameOfDirectory:
                                        isNewDirectoriesSame = False
                            if self.isChangeableItem(rowNo, 1, baseName, False):
                                baseName = str(self.item(rowNo, 1).text())
                                self.changedValueNumber += 1
                            newFilePath = fu.joinPath(
                                fu.getDirName(fu.getDirName(self.values[rowNo]["path"])),
                                baseNameOfDirectory, baseName)
                            if fu.getRealPath(self.values[rowNo]["path"]) != fu.getRealPath(
                                newFilePath):
                                changingFileDirectories.append([self.values[rowNo]["path"],
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
            Dialogs.showError(translate("CoverTable", "Cannot Open File"),
                              str(translate("CoverTable",
                                            "\"%s\" : cannot be opened. Please make sure that you selected a text file.")
                              ) % Organizer.getLink(self.values[_row]["path"]))

    def refreshColumns(self):
        self.tableColumns = [translate("CoverTable", "Directory"),
                             translate("CoverTable", "Directory Name"),
                             translate("CoverTable", "Current Cover"),
                             translate("CoverTable", "Source Cover"),
                             translate("CoverTable", "Destination Cover")]
        self.tableColumnsKey = ["Directory", "Directory Name", "Current Cover", "Source Cover",
                                "Destination Cover"]
        self.valueKeys = ["baseNameOfDirectory", "baseName", "currentCover", "sourceCover", "destinationCover"]

    def saveTable(self):
        self.checkFileExtensions(4, 3)
        return self.writeContents()

    def refreshTable(self, _path):
        self.values = []
        allFilesAndDirectories = fu.readDirectoryWithSubDirectoriesThread(_path,
                                                                          int(uni.MySettings["CoversSubDirectoryDeep"]),
                                                                          "directory",
                                                                          uni.getBoolValue("isShowHiddensInCoverTable"))
        allItemNumber = len(allFilesAndDirectories)
        uni.startThreadAction()
        rowNo = 0
        self.setRowCount(allItemNumber)
        for dirName in allFilesAndDirectories:
            isContinueThreadAction = uni.isContinueThreadAction()
            if isContinueThreadAction:
                try:
                    if fu.isReadableFileOrDir(dirName, False, True) and fu.isReadableFileOrDir(
                        fu.joinPath(dirName, ".directory"), False, True):
                        content = {}
                        content["path"] = dirName
                        content["baseNameOfDirectory"] = str(str(fu.getBaseName(_path)) +
                                                             str(fu.getDirName(dirName)).replace(_path, ""))
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
                        self.values.append(content)

                        newBaseNameOfDirectory = Organizer.emend(self.values[rowNo]["baseNameOfDirectory"],
                                                                 "directory")
                        itemBaseNameOfDirectory = self.createTableWidgetItem(newBaseNameOfDirectory,
                                                                             self.values[rowNo]["baseNameOfDirectory"])
                        self.setItem(rowNo, 0, itemBaseNameOfDirectory)

                        newBaseName = Organizer.emend(self.values[rowNo]["baseName"], "directory")
                        itemBaseName = self.createTableWidgetItem(newBaseName,
                                                                  self.values[rowNo]["baseName"])
                        self.setItem(rowNo, 1, itemBaseName)

                        newCurrentCover = str(self.values[rowNo]["currentCover"])
                        newCurrentCover = newCurrentCover.replace(self.values[rowNo]["path"], ".")
                        itemCurrentCover = self.createTableWidgetItem(newCurrentCover, newCurrentCover, True)
                        self.setItem(rowNo, 2, itemCurrentCover)
                        if self.values[rowNo]["isCorrectedFileContent"] == False:
                            itemCurrentCover.setBackground(MBrush(MColor(255, 163, 163)))

                        newSourceCover = str(self.values[rowNo]["sourceCover"])
                        newSourceCover = newSourceCover.replace(self.values[rowNo]["path"], ".")
                        oldSourceCover = self.values[rowNo]["currentCover"]
                        oldSourceCover = oldSourceCover.replace(self.values[rowNo]["path"], ".")
                        itemSourceCover = self.createTableWidgetItem(newSourceCover, oldSourceCover)
                        self.setItem(rowNo, 3, itemSourceCover)

                        newDestinationCover = self.values[rowNo]["destinationCover"]
                        newDestinationCover = newDestinationCover.replace(self.values[rowNo]["path"], ".")
                        newDestinationCover = Organizer.emend(newDestinationCover, "file")
                        oldDestinationCover = self.values[rowNo]["currentCover"]
                        oldDestinationCover = oldDestinationCover.replace(self.values[rowNo]["path"], ".")
                        itemDestinationCover = self.createTableWidgetItem(newDestinationCover, oldDestinationCover)
                        self.setItem(rowNo, 4, itemDestinationCover)
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
                                    fu.getDirName(fu.getDirName(self.values[rowNo]["path"])),
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
