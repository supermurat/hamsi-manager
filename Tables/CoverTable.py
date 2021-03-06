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


class CoverTable(CoreTable):
    def __init__(self, *args, **kwargs):
        CoreTable.__init__(self, *args, **kwargs)
        self.keyName = "cover"
        self.hiddenTableColumnsSettingKey = "hiddenCoverTableColumns"
        self.refreshColumns()
        lblDetails = translate("CoverOptionsBar",
                               "You can select sub directory deep.<br><font color=blue>You can select \"-1\" for all sub directories.</font>")
        lblSubDirectoryDeep = MLabel(str(translate("CoverOptionsBar", "Deep") + " : "))
        self.SubDirectoryDeeps = [str(x) for x in range(-1, 10) if x != 0]
        self.cbSubDirectoryDeep = MComboBox(self)
        self.cbSubDirectoryDeep.addItems(self.SubDirectoryDeeps)
        self.cbSubDirectoryDeep.setCurrentIndex(
            self.cbSubDirectoryDeep.findText(uni.MySettings["CoversSubDirectoryDeep"]))
        self.cbSubDirectoryDeep.setToolTip(lblDetails)
        hblSubDirectory = MHBoxLayout()
        hblSubDirectory.addWidget(lblSubDirectoryDeep)
        hblSubDirectory.addWidget(self.cbSubDirectoryDeep)
        MObject.connect(self.cbSubDirectoryDeep, SIGNAL("currentIndexChanged(int)"), self.coverDeepChanged)
        if uni.isActiveAmarok:
            pbtnGetFromAmarok = MPushButton(translate("CoverTable", "Get From Amarok"))
            MObject.connect(pbtnGetFromAmarok, SIGNAL("clicked()"), self.getFromAmarok)
            self.hblBoxOptions.addWidget(pbtnGetFromAmarok)
        self.hblBoxOptions.addLayout(hblSubDirectory)
        pbtnVerifyTableValues = MPushButton(translate("FileTable", "Verify Table"))
        pbtnVerifyTableValues.setMenu(SearchEngines.SearchEngines(self, "value"))
        self.mContextMenu.addMenu(SearchEngines.SearchEngines(self, "value", True))
        self.hblBoxTools.addWidget(pbtnVerifyTableValues)

    def refreshColumns(self):
        self.tableColumns = [translate("CoverTable", "Directory"),
                             translate("CoverTable", "Directory Name"),
                             translate("CoverTable", "Current Cover"),
                             translate("CoverTable", "Source Cover"),
                             translate("CoverTable", "Destination Cover")]
        self.tableColumnsKey = ["baseNameOfDirectory", "baseName", "currentCover", "sourceCover", "destinationCover"]
        self.tableReadOnlyColumnsKey = []

    def saveTable(self):
        self.checkFileExtensions("destinationCover", "sourceCover")
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
                        if isCorrectedFileContent and currentCover is not None:
                            selectedName = fu.getBaseName(currentCover)
                        sourceCover = fu.getFirstImageInDirectory(dirName, selectedName, False, False)
                        if currentCover is None:
                            currentCover = ""
                        if sourceCover is None:
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
                        self.createItem(rowNo, "baseNameOfDirectory", newBaseNameOfDirectory,
                                        self.values[rowNo]["baseNameOfDirectory"])

                        newBaseName = Organizer.emend(self.values[rowNo]["baseName"], "directory")
                        self.createItem(rowNo, "baseName", newBaseName, self.values[rowNo]["baseName"])

                        newCurrentCover = str(self.values[rowNo]["currentCover"])
                        newCurrentCover = newCurrentCover.replace(self.values[rowNo]["path"], ".")
                        itemCurrentCover = self.createItem(rowNo, "currentCover", newCurrentCover, newCurrentCover,
                                                           True)
                        if self.values[rowNo]["isCorrectedFileContent"] is False:
                            itemCurrentCover.setBackground(MBrush(MColor(255, 163, 163)))

                        newSourceCover = str(self.values[rowNo]["sourceCover"])
                        newSourceCover = newSourceCover.replace(self.values[rowNo]["path"], ".")
                        oldSourceCover = self.values[rowNo]["currentCover"]
                        oldSourceCover = oldSourceCover.replace(self.values[rowNo]["path"], ".")
                        self.createItem(rowNo, "sourceCover", newSourceCover, oldSourceCover)

                        newDestinationCover = self.values[rowNo]["destinationCover"]
                        newDestinationCover = newDestinationCover.replace(self.values[rowNo]["path"], ".")
                        newDestinationCover = Organizer.emend(newDestinationCover, "file")
                        oldDestinationCover = self.values[rowNo]["currentCover"]
                        oldDestinationCover = oldDestinationCover.replace(self.values[rowNo]["path"], ".")
                        self.createItem(rowNo, "destinationCover", newDestinationCover, oldDestinationCover)
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
                            if (self.isChangeableItem(rowNo, "sourceCover") or
                                    self.isChangeableItem(rowNo, "destinationCover")):
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
                            if self.isChangeableItem(rowNo, "baseNameOfDirectory", baseNameOfDirectory):
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
                            if self.isChangeableItem(rowNo, "baseName", baseName, False):
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
        if self.rowCount() == len(oldAndNewPathValues) and isMovedToNewDirectory and isNewDirectoriesSame:
            otherFileNames = fu.readDirectory(currentDirectoryPath, "fileAndDirectory", True)
            if len(otherFileNames) > 0:
                answer = Dialogs.ask(translate("FileUtils/Musics", "There Are More Files"),
                                     str(translate("FileUtils/Musics",
                                                   "\"%s\" : there are more files in this directory.<br>Are you want to move all found files into new directory?<br>New Directory : \"%s\"")) % (
                                         Organizer.getLink(currentDirectoryPath), Organizer.getLink(newDirectoryPath)))
                if answer == Dialogs.Yes:
                    uni.startThreadAction()
                    allItemNumber = len(otherFileNames)
                    for rowNo, fileName in enumerate(otherFileNames):
                        isContinueThreadAction = uni.isContinueThreadAction()
                        if isContinueThreadAction:
                            try:
                                oldFilePath = fu.getRealPath(fu.joinPath(currentDirectoryPath, fileName))
                                newFilePath = fu.getRealPath(fu.joinPath(newDirectoryPath, fileName))
                                if oldFilePath != newFilePath:
                                    oldAndNewPaths = {}
                                    oldAndNewPaths["oldPath"] = oldFilePath
                                    oldAndNewPaths["newPath"] = fu.moveOrChange(oldFilePath, newFilePath,
                                                                                fu.getObjectType(oldFilePath))
                                    if oldFilePath != oldAndNewPaths["newPath"]:
                                        oldAndNewPathValues.append(oldAndNewPaths)
                            except:
                                ReportBug.ReportBug()
                        else:
                            allItemNumber = rowNo + 1
                        Dialogs.showState(translate("FileUtils/Covers", "Writing Directory And File Informations"),
                                          rowNo + 1, allItemNumber, True)
                        if isContinueThreadAction is False:
                            break
                    uni.finishThreadAction()
                    if uni.getBoolValue("isClearEmptyDirectoriesWhenFileMove"):
                        fu.checkEmptyDirectories(currentDirectoryPath, True, True,
                                                 uni.getBoolValue("isAutoCleanSubFolderWhenFileMove"))
                    if (uni.isActiveDirectoryCover and uni.getBoolValue("isActiveAutoMakeIconToDirectory") and
                            uni.getBoolValue("isAutoMakeIconToDirectoryWhenFileMove")):
                        fu.checkIcon(newDirectoryPath)
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
            Dialogs.showError(translate("CoverTable", "Cannot Open File"),
                              str(translate("CoverTable",
                                            "\"%s\" : cannot be opened. Please make sure that you selected a text file.")
                              ) % Organizer.getLink(self.values[_row]["path"]))

    def getFromAmarok(self):
        try:
            import Amarok

            Dialogs.showState(translate("CoverTable", "Checking For Amarok..."), 0, 1)
            if Amarok.checkAmarok():
                from Amarok import Operations

                directoriesAndValues = Operations.getDirectoriesAndValues()
                Dialogs.showState(translate("CoverTable", "Values Are Being Processed"), 1, 1)
                if directoriesAndValues is not None:
                    for rowNo in range(self.rowCount()):
                        if (getMainWindow().checkHiddenColumn("sourceCover") and
                                getMainWindow().checkHiddenColumn("destinationCover")):
                            if self.isChangeableItem(rowNo, "sourceCover"):
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

    def coverDeepChanged(self, _action=None):
        try:
            selectedDeep = str(self.SubDirectoryDeeps[_action])
            if self.checkUnSavedValues():
                uni.setMySetting("CoversSubDirectoryDeep", int(selectedDeep))
                self.refreshForColumns()
                getMainWindow().SpecialTools.refreshForColumns()
                self.refresh(getMainWindow().FileManager.getCurrentDirectoryPath())
            self.cbSubDirectoryDeep.setCurrentIndex(
                self.cbSubDirectoryDeep.findText(str(uni.MySettings["CoversSubDirectoryDeep"])))
        except:
            ReportBug.ReportBug()