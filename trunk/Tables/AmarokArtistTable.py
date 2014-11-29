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

from Core import Organizer
from Core.MyObjects import *
import Details
from Details import AmarokArtistDetails
from Core import Universals as uni
from Core import Dialogs
from Core import Records
from Core import ReportBug
from Tables import CoreTable
import Amarok
from Amarok import Operations
from Amarok import Filter
import SearchEngines


class AmarokArtistTable(CoreTable):
    def __init__(self, *args, **kwargs):
        CoreTable.__init__(self, *args, **kwargs)
        self.keyName = "ADCArtist"
        self.amarokFilterKeyName = "AmarokFilterArtistTable"
        self.hiddenTableColumnsSettingKey = "hiddenAmarokArtistTableColumns"
        self.refreshColumns()
        self.wFilter = Filter.FilterWidget(self, self.amarokFilterKeyName)
        self.hblBoxOptions.addWidget(self.wFilter)
        pbtnVerifyTableValues = MPushButton(translate("FileTable", "Verify Table"))
        pbtnVerifyTableValues.setMenu(SearchEngines.SearchEngines(self, "value"))
        self.mContextMenu.addMenu(SearchEngines.SearchEngines(self, "value", True))
        self.hblBoxTools.addWidget(pbtnVerifyTableValues)

    def refreshColumns(self):
        self.tableColumns = [translate("AmarokArtistTable", "Current Artist"),
                             translate("AmarokArtistTable", "Corrected Artist")]
        self.tableColumnsKey = ["currentArtist", "correctedArtist"]
        self.tableReadOnlyColumnsKey = []

    def saveTable(self):
        Details.closeAllDialogs()
        return self.writeContents()

    def refreshTable(self, _path):
        self.values = []
        uni.startThreadAction()
        Dialogs.showState(translate("AmarokArtistTable", "Getting Values From Amarok"), 0, 1)
        if Amarok.checkAmarok():
            isContinueThreadAction = uni.isContinueThreadAction()
            if isContinueThreadAction:
                artistValues = Operations.getAllArtistsValues(uni.MySettings[self.amarokFilterKeyName])
                Dialogs.showState(translate("AmarokArtistTable", "Values Are Being Processed"), 1, 1)
                isContinueThreadAction = uni.isContinueThreadAction()
                if isContinueThreadAction:
                    if artistValues is not None:
                        allItemNumber = len(artistValues)
                        self.setRowCount(allItemNumber)
                        rowNo = 0
                        for musicFileRow in artistValues:
                            isContinueThreadAction = uni.isContinueThreadAction()
                            if isContinueThreadAction:
                                try:
                                    content = {}
                                    content["id"] = musicFileRow["id"]
                                    content["currentArtist"] = musicFileRow["name"]
                                    content["correctedArtist"] = musicFileRow["name"]
                                    self.values.append(content)

                                    currentName = content["currentArtist"]
                                    self.createItem(rowNo, "currentArtist", currentName, currentName, True)

                                    newName = Organizer.emend(content["correctedArtist"])
                                    isReadOnlyNewName = (content["correctedArtist"].strip() == "")
                                    self.createItem(rowNo, "correctedArtist", newName, content["currentArtist"],
                                                    isReadOnlyNewName)
                                    rowNo += 1
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
        changedArtistValues = []
        uni.startThreadAction()
        allItemNumber = len(self.values)
        Dialogs.showState(translate("FileUtils/Musics", "Writing Music Tags"), 0, allItemNumber, True)
        for rowNo in range(self.rowCount()):
            isContinueThreadAction = uni.isContinueThreadAction()
            if isContinueThreadAction:
                try:
                    if self.isRowHidden(rowNo) is False:
                        if self.isChangeableItem(rowNo, "correctedArtist", str(self.values[rowNo]["currentArtist"])):
                            changedArtistValues.append({})
                            changedArtistValues[-1]["id"] = str(self.values[rowNo]["id"])
                            value = str(self.item(rowNo, 1).text())
                            changedArtistValues[-1]["name"] = value
                            Records.add(str(translate("AmarokArtistTable", "Artist")),
                                        str(self.values[rowNo]["currentArtist"]), value)
                            self.changedValueNumber += 1
                except:
                    ReportBug.ReportBug()
            else:
                allItemNumber = rowNo + 1
            Dialogs.showState(translate("FileUtils/Musics", "Writing Music Tags"), rowNo + 1, allItemNumber, True)
            if isContinueThreadAction is False:
                break
        uni.finishThreadAction()
        Operations.changeArtistValues(changedArtistValues)
        return True

    def correctTable(self):
        for rowNo in range(self.rowCount()):
            for coloumKey in self.getWritableColumnKeys():
                coloumNo = self.getColumnNoFromKey(coloumKey)
                if self.isChangeableItem(rowNo, coloumKey):
                    newString = None
                    if coloumKey == "correctedArtist":
                        newString = Organizer.emend(str(self.item(rowNo, coloumNo).text()))
                    self.item(rowNo, coloumNo).setText(str(newString))

    def showTableDetails(self, _fileNo, _infoNo):
        AmarokArtistDetails.AmarokArtistDetails(self.values[_fileNo]["id"], uni.getBoolValue("isOpenDetailsInNewWindow"))

    def cellClickedTable(self, _row, _column):
        currentItem = self.currentItem()
        if currentItem is not None:
            cellLenght = len(currentItem.text()) * 8
            if cellLenght > self.columnWidth(_column):
                self.setColumnWidth(_column, cellLenght)

    def cellDoubleClickedTable(self, _row, _column):
        if uni.getBoolValue("isRunOnDoubleClick"):
            self.showTableDetails(_row, _column)
