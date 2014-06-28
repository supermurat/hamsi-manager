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
import SearchEngines
from Core.MyObjects import *
from Details import AmarokArtistDetails
from Core import Universals as uni
from Core import Dialogs
import Taggers
from Core import Records
from Core import ReportBug
from Tables import CoreTable


class AmarokArtistTable(CoreTable):
    def __init__(self, *args, **kwargs):
        CoreTable.__init__(self, *args, **kwargs)
        from Amarok import Filter

        self.keyName = "ADCArtist"
        self.amarokFilterKeyName = "AmarokFilterArtistTable"
        self.hiddenTableColumnsSettingKey = "hiddenAmarokArtistTableColumns"
        self.refreshColumns()
        self.wFilter = Filter.FilterWidget(self, self.amarokFilterKeyName)
        getMainWindow().MainLayout.addWidget(self.wFilter)

    def readContents(self, _directoryPath):
        currentTableContentValues = []
        uni.startThreadAction()
        import Amarok

        Dialogs.showState(translate("AmarokArtistTable", "Checking For Amarok..."), 0, 2)
        if Amarok.checkAmarok():
            Dialogs.showState(translate("AmarokArtistTable", "Getting Values From Amarok"), 1, 2)
            isContinueThreadAction = uni.isContinueThreadAction()
            if isContinueThreadAction:
                from Amarok import Operations

                artistValues = Operations.getAllArtistsValues(uni.MySettings[self.amarokFilterKeyName])
                Dialogs.showState(translate("AmarokArtistTable", "Values Are Being Processed"), 2, 2)
                isContinueThreadAction = uni.isContinueThreadAction()
                if isContinueThreadAction:
                    if artistValues != None:
                        allItemNumber = len(artistValues)
                        musicFileNo = 0
                        for musicFileRow in artistValues:
                            isContinueThreadAction = uni.isContinueThreadAction()
                            if isContinueThreadAction:
                                try:
                                    content = {}
                                    content["id"] = musicFileRow["id"]
                                    content["name"] = musicFileRow["name"]
                                    currentTableContentValues.append(content)
                                except:
                                    ReportBug.ReportBug()
                            else:
                                allItemNumber = musicFileNo + 1
                            Dialogs.showState(translate("FileUtils/Covers", "Reading Music File Informations"),
                                              musicFileNo + 1, allItemNumber, True)
                            musicFileNo += 1
                            if isContinueThreadAction == False:
                                break
        uni.finishThreadAction()
        return currentTableContentValues

    def writeContents(self):
        self.changedValueNumber = 0
        changedArtistValues = []
        uni.startThreadAction()
        import Amarok

        allItemNumber = len(self.currentTableContentValues)
        Dialogs.showState(translate("FileUtils/Musics", "Writing Music Tags"), 0, allItemNumber, True)
        for rowNo in range(self.rowCount()):
            isContinueThreadAction = uni.isContinueThreadAction()
            if isContinueThreadAction:
                try:
                    if self.isRowHidden(rowNo) == False:
                        if self.isChangeableItem(rowNo, 1,
                                                 str(self.currentTableContentValues[rowNo]["name"])):
                            changedArtistValues.append({})
                            changedArtistValues[-1]["id"] = str(self.currentTableContentValues[rowNo]["id"])
                            value = str(self.item(rowNo, 1).text())
                            changedArtistValues[-1]["name"] = value
                            Records.add(str(translate("AmarokArtistTable", "Artist")),
                                        str(self.currentTableContentValues[rowNo]["name"]), value)
                            self.changedValueNumber += 1
                except:
                    ReportBug.ReportBug()
            else:
                allItemNumber = rowNo + 1
            Dialogs.showState(translate("FileUtils/Musics", "Writing Music Tags"), rowNo + 1, allItemNumber, True)
            if isContinueThreadAction == False:
                break
        uni.finishThreadAction()
        from Amarok import Operations

        Operations.changeArtistValues(changedArtistValues)
        return True

    def showTableDetails(self, _fileNo, _infoNo):
        AmarokArtistDetails.AmarokArtistDetails(self.currentTableContentValues[_fileNo]["id"],
                                                uni.getBoolValue("isOpenDetailsInNewWindow"))

    def cellClickedTable(self, _row, _column):
        currentItem = self.currentItem()
        if currentItem is not None:
            cellLenght = len(currentItem.text()) * 8
            if cellLenght > self.columnWidth(_column):
                self.setColumnWidth(_column, cellLenght)

    def cellDoubleClickedTable(self, _row, _column):
        if uni.getBoolValue("isRunOnDoubleClick"):
            self.showTableDetails(_row, _column)

    def refreshColumns(self):
        self.tableColumns = [translate("AmarokArtistTable", "Current Artist"),
                                   translate("AmarokArtistTable", "Corrected Artist")]
        self.tableColumnsKey = ["currentArtist", "correctedArtist"]

    def saveTable(self):
        AmarokArtistDetails.AmarokArtistDetails.closeAllAmarokArtistDialogs()
        return self.writeContents()

    def refreshTable(self, _path):
        self.currentTableContentValues = self.readContents(_path)
        self.setRowCount(len(self.currentTableContentValues))
        allItemNumber = self.rowCount()
        for rowNo in range(allItemNumber):
            newString = self.currentTableContentValues[rowNo]["name"]
            item = self.createTableWidgetItem(newString, newString, True)
            self.setItem(rowNo, 0, item)
            newString = Organizer.emend(self.currentTableContentValues[rowNo]["name"])
            isReadOnly = self.currentTableContentValues[rowNo]["name"].strip() == ""
            item = self.createTableWidgetItem(newString, self.currentTableContentValues[rowNo]["name"],
                                                    isReadOnly)
            self.setItem(rowNo, 1, item)
            Dialogs.showState(translate("Tables", "Generating .."), rowNo + 1, allItemNumber)

    def correctTable(self):
        for rowNo in range(self.rowCount()):
            for itemNo in range(self.columnCount()):
                if self.isChangeableItem(rowNo, itemNo):
                    if itemNo == 0:
                        continue
                    elif itemNo == 1:
                        newString = Organizer.emend(str(self.item(rowNo, itemNo).text()))
                    self.item(rowNo, itemNo).setText(str(newString))

    def getValueByRowAndColumn(self, _rowNo, _columnNo):
        if _columnNo == 0:
            return self.currentTableContentValues[_rowNo]["name"]
        elif _columnNo == 1:
            return self.currentTableContentValues[_rowNo]["name"]
        return ""
