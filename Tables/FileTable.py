# This file is part of HamsiManager.
#
# Copyright (c) 2010 - 2014 Murat Demir <mopened@gmail.com>
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

import stat
from Core import Organizer
import FileUtils as fu
from Core.MyObjects import *
from Details import Details
from Core import Dialogs
from Core import Universals as uni
from Core import ReportBug
from Tables import CoreTable
import SearchEngines


class FileTable(CoreTable):
    def __init__(self, *args, **kwargs):
        CoreTable.__init__(self, *args, **kwargs)
        self.keyName = "file"
        self.hiddenTableColumnsSettingKey = "hiddenFileTableColumns"
        self.refreshColumns()
        pbtnVerifyTableValues = MPushButton(translate("FileTable", "Verify Table"))
        pbtnVerifyTableValues.setMenu(SearchEngines.SearchEngines(self, "value"))
        self.mContextMenu.addMenu(SearchEngines.SearchEngines(self, "value", True))
        self.hblBoxTools.addWidget(pbtnVerifyTableValues)

    def writeContents(self):
        self.changedValueNumber = 0
        oldAndNewPathValues = []
        if uni.isActiveAmarok and uni.getBoolValue("isFileTableValuesChangeInAmarokDB"):
            import Amarok

            if Amarok.checkAmarok(True, False) is False:
                return False
        uni.startThreadAction()
        allItemNumber = len(self.values)
        Dialogs.showState(translate("FileUtils/Files", "Writing File Informations"), 0, allItemNumber, True)
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
                            if self.isChangeableItem(rowNo, "baseNameOfDirectory", baseNameOfDirectory):
                                baseNameOfDirectory = str(self.item(rowNo, 0).text())
                                self.changedValueNumber += 1
                                newDirectoryPath = fu.joinPath(
                                    fu.getDirName(fu.getDirName(self.values[rowNo]["path"])),
                                    baseNameOfDirectory)
                                self.setNewDirectory(newDirectoryPath)
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
                                oldAndNewPaths["newPath"] = fu.moveOrChange(oldFilePath, newFilePath, "file")
                                if oldFilePath != oldAndNewPaths["newPath"]:
                                    oldAndNewPathValues.append(oldAndNewPaths)
                                    oldDirName = fu.getDirName(oldFilePath)
                                    if uni.getBoolValue("isClearEmptyDirectoriesWhenFileMove"):
                                        fu.checkEmptyDirectories(oldDirName, True, True,
                                                              uni.getBoolValue("isAutoCleanSubFolderWhenFileMove"))
                                    if (uni.isActiveDirectoryCover and
                                            uni.getBoolValue("isActiveAutoMakeIconToDirectory") and
                                            uni.getBoolValue("isAutoMakeIconToDirectoryWhenFileMove")):
                                        fu.checkIcon(oldDirName)
                                        fu.checkIcon(fu.getDirName(oldAndNewPaths["newPath"]))
                except:
                    ReportBug.ReportBug()
            else:
                allItemNumber = rowNo + 1
            Dialogs.showState(translate("FileUtils/Files", "Writing File Informations"), rowNo + 1, allItemNumber, True)
            if isContinueThreadAction is False:
                break
        uni.finishThreadAction()
        if (uni.isActiveAmarok and uni.getBoolValue("isFileTableValuesChangeInAmarokDB") and
                len(oldAndNewPathValues) > 0):
            import Amarok
            from Amarok import Operations

            Operations.changePaths(oldAndNewPathValues, "file")
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
            Dialogs.showError(translate("FileTable", "Cannot Open File"),
                              str(translate("FileTable",
                                            "\"%s\" : cannot be opened. Please make sure that you selected a text file.")
                              ) % Organizer.getLink(self.values[_row]["path"]))

    def refreshColumns(self):
        self.tableColumns = [translate("FileTable", "Directory"),
                             translate("FileTable", "File Name"),
                             translate("FileTable", "Size"),
                             translate("FileTable", "Last Accessed"),
                             translate("FileTable", "Last Modified"),
                             translate("FileTable", "Last Metadata Changed"),
                             translate("FileTable", "Access Rights"),
                             translate("FileTable", "User ID Of Owner"),
                             translate("FileTable", "Group ID Of Owner"),
                             translate("FileTable", "Number Of Hard Links")
        ]
        self.tableColumnsKey = ["baseNameOfDirectory", "baseName", "size", "lastAccessed", "lastModified",
                                "lastMetadataChanged", "accessRights", "userIDOfOwner", "groupIDOfOwner",
                                "numberOfHardLinks"]
        self.tableReadOnlyColumnsKey = ["size", "lastAccessed", "lastModified", "lastMetadataChanged",
                                        "accessRights", "userIDOfOwner", "groupIDOfOwner", "numberOfHardLinks"]

    def saveTable(self):
        self.checkFileExtensions("baseName", "baseName")
        return self.writeContents()

    def refreshTable(self, _path):
        self.values = []
        fileNames = fu.readDirectory(_path, "file", uni.getBoolValue("isShowHiddensInFileTable"))
        allItemNumber = len(fileNames)
        uni.startThreadAction()
        baseNameOfDirectory = fu.getBaseName(_path)
        rowNo = 0
        self.setRowCount(allItemNumber)
        for baseName in fileNames:
            isContinueThreadAction = uni.isContinueThreadAction()
            if isContinueThreadAction:
                try:
                    if fu.isReadableFileOrDir(fu.joinPath(_path, baseName), False, True):
                        details = fu.getDetails(fu.joinPath(_path, baseName))
                        content = {}
                        content["path"] = fu.joinPath(_path, baseName)
                        content["baseNameOfDirectory"] = baseNameOfDirectory
                        content["baseName"] = baseName
                        content["accessRights"] = oct(stat.S_IMODE(details[stat.ST_MODE]))
                        content["numberOfHardLinks"] = details[stat.ST_NLINK]
                        content["userIDOfOwner"] = details[stat.ST_UID]
                        content["groupIDOfOwner"] = details[stat.ST_GID]
                        content["size"] = details[stat.ST_SIZE]
                        content["lastAccessed"] = details[stat.ST_ATIME]
                        content["lastModified"] = details[stat.ST_MTIME]
                        content["lastMetadataChanged"] = details[stat.ST_CTIME] #time of creation on Windows
                        self.values.append(content)

                        newBaseNameOfDirectory = Organizer.emend(content["baseNameOfDirectory"], "directory")
                        self.createItem(rowNo, "baseNameOfDirectory", newBaseNameOfDirectory,
                                        content["baseNameOfDirectory"])

                        newBaseName = Organizer.emend(content["baseName"], "file")
                        self.createItem(rowNo, "baseName", newBaseName, content["baseName"])

                        self.createItem(rowNo, "size", Organizer.getCorrectedFileSize(content["size"]))

                        self.createItem(rowNo, "lastAccessed", Organizer.getCorrectedTime(content["lastAccessed"]))

                        self.createItem(rowNo, "lastModified", Organizer.getCorrectedTime(content["lastModified"]))

                        self.createItem(rowNo, "lastMetadataChanged",
                                        Organizer.getCorrectedTime(content["lastMetadataChanged"]))

                        self.createItem(rowNo, "accessRights", content["accessRights"])

                        self.createItem(rowNo, "userIDOfOwner", content["userIDOfOwner"])

                        self.createItem(rowNo, "groupIDOfOwner", content["groupIDOfOwner"])

                        self.createItem(rowNo, "numberOfHardLinks", content["numberOfHardLinks"])

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

    def correctTable(self):
        for rowNo in range(self.rowCount()):
            for coloumKey in self.getWritableColumnKeys():
                coloumNo = self.getColumnNoFromKey(coloumKey)
                if self.isChangeableItem(rowNo, coloumKey):
                    if coloumKey == "baseNameOfDirectory":
                        newString = Organizer.emend(str(self.item(rowNo, coloumNo).text()), "directory")
                    else:
                        newString = Organizer.emend(str(self.item(rowNo, coloumNo).text()), "file")
                    self.item(rowNo, coloumNo).setText(str(newString))
    
    
