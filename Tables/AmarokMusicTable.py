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
from Details import MusicDetails
from Core import Universals as uni
from Core import Dialogs
import Taggers
from Core import Records
from Core import ReportBug
from Tables import CoreTable


class AmarokMusicTable(CoreTable):
    def __init__(self, *args, **kwargs):
        CoreTable.__init__(self, *args, **kwargs)
        from Amarok import Filter

        self.keyName = "music"
        self.amarokFilterKeyName = "AmarokFilterAmarokMusicTable"
        self.hiddenTableColumnsSettingKey = "hiddenAmarokMusicTableColumns"
        self.refreshColumns()
        pbtnVerifyTableValues = MPushButton(translate("AmarokMusicTable", "Verify Table"))
        pbtnVerifyTableValues.setMenu(SearchEngines.SearchEngines(self))
        self.mContextMenu.addMenu(SearchEngines.SearchEngines(self, True))
        self.isPlayNow = MToolButton()
        self.isPlayNow.setToolTip(translate("AmarokMusicTable", "Play Now"))
        self.isPlayNow.setIcon(MIcon("Images:playNow.png"))
        self.isPlayNow.setCheckable(True)
        self.isPlayNow.setAutoRaise(True)
        self.isPlayNow.setChecked(uni.getBoolValue("isPlayNow"))
        self.hblBox.insertWidget(self.hblBox.count() - 3, self.isPlayNow)
        self.hblBox.insertWidget(self.hblBox.count() - 1, pbtnVerifyTableValues)
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

                musicFileValuesWithNames = Operations.getAllMusicFileValuesWithNames(
                    uni.MySettings[self.amarokFilterKeyName])
                Dialogs.showState(translate("AmarokCoverTable", "Values Are Being Processed"), 2, 2)
                isContinueThreadAction = uni.isContinueThreadAction()
                if isContinueThreadAction:
                    if musicFileValuesWithNames != None:
                        allItemNumber = len(musicFileValuesWithNames)
                        musicFileNo = 0
                        for musicFileRow in musicFileValuesWithNames:
                            isContinueThreadAction = uni.isContinueThreadAction()
                            if isContinueThreadAction:
                                try:
                                    if Amarok.getSelectedTagSourseType("AmarokMusicTable") == "Amarok":
                                        content = {}
                                        content["path"] = musicFileRow["filePath"]
                                        content["baseNameOfDirectory"] = fu.getBaseName(
                                            fu.getDirName(musicFileRow["filePath"]))
                                        content["baseName"] = fu.getBaseName(musicFileRow["filePath"])
                                        content["artist"] = musicFileRow["artist"]
                                        content["title"] = musicFileRow["title"]
                                        content["album"] = musicFileRow["album"]
                                        content["trackNum"] = musicFileRow["tracknumber"]
                                        content["year"] = musicFileRow["year"]
                                        content["genre"] = musicFileRow["genre"]
                                        content["firstComment"] = musicFileRow["comment"]
                                        content["firstLyrics"] = musicFileRow["lyrics"]
                                        currentTableContentValues.append(content)
                                    else:
                                        if fu.isFile(musicFileRow["filePath"]) and fu.isReadableFileOrDir(
                                            musicFileRow["filePath"], False, True):
                                            tagger = Taggers.getTagger()
                                            try:
                                                tagger.loadFile(musicFileRow["filePath"])
                                            except:
                                                Dialogs.showError(translate("FileUtils/Musics", "Incorrect Tag"),
                                                                  str(translate("FileUtils/Musics",
                                                                                "\"%s\" : this file has the incorrect tag so can't read tags.")
                                                                  ) % Organizer.getLink(musicFileRow["filePath"]))
                                            content = {}
                                            content["path"] = musicFileRow["filePath"]
                                            content["baseNameOfDirectory"] = fu.getBaseName(
                                                fu.getDirName(musicFileRow["filePath"]))
                                            content["baseName"] = fu.getBaseName(musicFileRow["filePath"])
                                            content["artist"] = tagger.getArtist()
                                            content["title"] = tagger.getTitle()
                                            content["album"] = tagger.getAlbum()
                                            content["trackNum"] = tagger.getTrackNum()
                                            content["year"] = tagger.getYear()
                                            content["genre"] = tagger.getGenre()
                                            content["firstComment"] = tagger.getFirstComment()
                                            content["firstLyrics"] = tagger.getFirstLyrics()
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
        changingFileDirectories = []
        changingTags = []
        uni.startThreadAction()
        import Amarok

        allItemNumber = len(self.currentTableContentValues)
        Dialogs.showState(translate("FileUtils/Musics", "Writing Music Tags"), 0, allItemNumber, True)
        for rowNo in range(self.rowCount()):
            isContinueThreadAction = uni.isContinueThreadAction()
            if isContinueThreadAction:
                try:
                    if self.isRowHidden(rowNo):
                        isWritableFileOrDir = fu.isFile(
                            self.currentTableContentValues[rowNo]["path"]) and fu.isWritableFileOrDir(
                            self.currentTableContentValues[rowNo]["path"], False, True)
                        if isWritableFileOrDir:
                            fu.removeFileOrDir(self.currentTableContentValues[rowNo]["path"])
                            self.changedValueNumber += 1
                    else:
                        changingTag = {"path": self.currentTableContentValues[rowNo]["path"]}
                        isWritableFileOrDir = fu.isFile(
                            self.currentTableContentValues[rowNo]["path"]) and fu.isWritableFileOrDir(
                            self.currentTableContentValues[rowNo]["path"], False, True)
                        if isWritableFileOrDir:
                            baseNameOfDirectory = str(
                                self.currentTableContentValues[rowNo]["baseNameOfDirectory"])
                            baseName = str(self.currentTableContentValues[rowNo]["baseName"])
                            if Amarok.getSelectedTagTargetType("AmarokMusicTable").find("ID3") > -1:
                                typeTemp = Amarok.getSelectedTagTargetType("AmarokMusicTable").split(" + ")
                                if len(typeTemp) > 1:
                                    taggerType = typeTemp[1]
                                else:
                                    taggerType = typeTemp[0]
                                Taggers.setSelectedTaggerTypeForWriteName(taggerType)
                            tagger = Taggers.getTagger()
                            tagger.loadFileForWrite(self.currentTableContentValues[rowNo]["path"])
                        if self.isChangeableItem(rowNo, 2):
                            value = str(self.item(rowNo, 2).text())
                            if isWritableFileOrDir: tagger.setArtist(value)
                            changingTag["artist"] = value
                            Records.add(str(translate("AmarokMusicTable", "Artist")),
                                        str(self.currentTableContentValues[rowNo]["artist"]), value)
                            self.changedValueNumber += 1
                        if self.isChangeableItem(rowNo, 3):
                            value = str(self.item(rowNo, 3).text())
                            if isWritableFileOrDir: tagger.setTitle(value)
                            changingTag["title"] = value
                            Records.add(str(translate("AmarokMusicTable", "Title")),
                                        str(self.currentTableContentValues[rowNo]["title"]), value)
                            self.changedValueNumber += 1
                        if self.isChangeableItem(rowNo, 4):
                            value = str(self.item(rowNo, 4).text())
                            if isWritableFileOrDir: tagger.setAlbum(value)
                            changingTag["album"] = value
                            Records.add(str(translate("AmarokMusicTable", "Album")),
                                        str(self.currentTableContentValues[rowNo]["album"]), value)
                            self.changedValueNumber += 1
                        if self.isChangeableItem(rowNo, 5):
                            value = str(self.item(rowNo, 5).text())
                            if isWritableFileOrDir: tagger.setTrackNum(value)
                            changingTag["trackNum"] = value
                            Records.add(str(translate("AmarokMusicTable", "Track No")),
                                        str(self.currentTableContentValues[rowNo]["trackNum"]), value)
                            self.changedValueNumber += 1
                        if self.isChangeableItem(rowNo, 6):
                            value = str(self.item(rowNo, 6).text())
                            if isWritableFileOrDir: tagger.setDate(value)
                            changingTag["year"] = value
                            Records.add(str(translate("AmarokMusicTable", "Year")),
                                        str(self.currentTableContentValues[rowNo]["year"]), value)
                            self.changedValueNumber += 1
                        if self.isChangeableItem(rowNo, 7):
                            value = str(self.item(rowNo, 7).text())
                            if isWritableFileOrDir: tagger.setGenre(value)
                            changingTag["genre"] = value
                            Records.add(str(translate("AmarokMusicTable", "Genre")),
                                        str(self.currentTableContentValues[rowNo]["genre"]), value)
                            self.changedValueNumber += 1
                        if self.isChangeableItem(rowNo, 8):
                            value = str(self.item(rowNo, 8).text())
                            if isWritableFileOrDir: tagger.setFirstComment(value)
                            changingTag["firstComment"] = value
                            Records.add(str(translate("AmarokMusicTable", "Comment")),
                                        str(self.currentTableContentValues[rowNo]["firstComment"]), value)
                            self.changedValueNumber += 1
                        if len(self.tableColumns) > 9 and self.isChangeableItem(rowNo, 9):
                            value = str(self.item(rowNo, 9).text())
                            if isWritableFileOrDir: tagger.setFirstLyrics(value)
                            changingTag["firstLyrics"] = value
                            Records.add(str(translate("AmarokMusicTable", "Lyrics")),
                                        str(self.currentTableContentValues[rowNo]["firstLyrics"]), value)
                            self.changedValueNumber += 1
                        if len(changingTag) > 1:
                            changingTags.append(changingTag)
                        if isWritableFileOrDir:
                            if Amarok.getSelectedTagTargetType("AmarokMusicTable").find("ID3") > -1:
                                tagger.update()
                            if self.isChangeableItem(rowNo, 0, baseNameOfDirectory):
                                baseNameOfDirectory = str(self.item(rowNo, 0).text())
                                self.changedValueNumber += 1
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
            Dialogs.showState(translate("FileUtils/Musics", "Writing Music Tags"), rowNo + 1, allItemNumber, True)
            if isContinueThreadAction == False:
                break
        uni.finishThreadAction()
        pathValues = fu.changeDirectories(changingFileDirectories)
        from Amarok import Operations

        if Amarok.getSelectedTagTargetType("AmarokMusicTable").find("Amarok") > -1:
            Operations.changeTags(changingTags)
        Operations.changePaths(pathValues, "file")
        return True

    def showTableDetails(self, _fileNo, _infoNo):
        MusicDetails.MusicDetails(self.currentTableContentValues[_fileNo]["path"],
                                  uni.getBoolValue("isOpenDetailsInNewWindow"), self.isPlayNow.isChecked())

    def cellClickedTable(self, _row, _column):
        currentItem = self.currentItem()
        if currentItem is not None:
            cellLenght = len(currentItem.text()) * 8
            if cellLenght > self.columnWidth(_column):
                self.setColumnWidth(_column, cellLenght)
            if _column == 8 or _column == 9:
                if self.rowHeight(_row) < 150:
                    self.setRowHeight(_row, 150)
                if self.columnWidth(_column) < 250:
                    self.setColumnWidth(_column, 250)

    def cellDoubleClickedTable(self, _row, _column):
        try:
            if _column == 8 or _column == 9:
                self.showTableDetails(_row, _column)
            else:
                if uni.getBoolValue("isRunOnDoubleClick"):
                    self.showTableDetails(_row, _column)
        except:
            Dialogs.showError(translate("AmarokMusicTable", "Cannot Open Music File"),
                              str(translate("AmarokMusicTable",
                                            "\"%s\" : cannot be opened. Please make sure that you selected a music file.")
                              ) % Organizer.getLink(self.currentTableContentValues[_row]["path"]))

    def refreshColumns(self):
        self.tableColumns = Taggers.getAvailableLabelsForTable()
        self.tableColumnsKey = Taggers.getAvailableKeysForTable()

    def saveTable(self):
        MusicDetails.MusicDetails.closeAllMusicDialogs()
        self.checkFileExtensions(1, "baseName")
        return self.writeContents()

    def refreshTable(self, _path):
        self.setColumnWidth(5, 70)
        self.setColumnWidth(6, 40)
        self.currentTableContentValues = self.readContents(_path)
        self.setRowCount(len(self.currentTableContentValues))
        allItemNumber = self.rowCount()
        for rowNo in range(allItemNumber):
            for itemNo in range(len(self.tableColumns)):
                item = None
                if itemNo == 0:
                    newString = Organizer.emend(self.currentTableContentValues[rowNo]["baseNameOfDirectory"],
                                                "directory")
                    item = self.createTableWidgetItem(newString, self.currentTableContentValues[rowNo][
                        "baseNameOfDirectory"])
                elif itemNo == 1:
                    newString = Organizer.emend(self.currentTableContentValues[rowNo]["baseName"], "file")
                    item = self.createTableWidgetItem(newString,
                                                      self.currentTableContentValues[rowNo]["baseName"])
                elif itemNo == 2:
                    newString = Organizer.emend(self.currentTableContentValues[rowNo]["artist"])
                    item = self.createTableWidgetItem(newString,
                                                      self.currentTableContentValues[rowNo]["artist"])
                elif itemNo == 3:
                    newString = Organizer.emend(self.currentTableContentValues[rowNo]["title"])
                    item = self.createTableWidgetItem(newString,
                                                      self.currentTableContentValues[rowNo]["title"])
                elif itemNo == 4:
                    newString = Organizer.emend(self.currentTableContentValues[rowNo]["album"])
                    item = self.createTableWidgetItem(newString,
                                                      self.currentTableContentValues[rowNo]["album"])
                elif itemNo == 5:
                    newString = str(self.currentTableContentValues[rowNo]["trackNum"])
                    item = self.createTableWidgetItem(newString,
                                                      self.currentTableContentValues[rowNo]["trackNum"])
                elif itemNo == 6:
                    newString = Organizer.emend(self.currentTableContentValues[rowNo]["year"])
                    item = self.createTableWidgetItem(newString,
                                                      self.currentTableContentValues[rowNo]["year"])
                elif itemNo == 7:
                    newString = Organizer.emend(self.currentTableContentValues[rowNo]["genre"])
                    item = self.createTableWidgetItem(newString,
                                                      self.currentTableContentValues[rowNo]["genre"])
                elif itemNo == 8:
                    newString = Organizer.emend(self.currentTableContentValues[rowNo]["firstComment"])
                    item = self.createTableWidgetItem(newString,
                                                      self.currentTableContentValues[rowNo]["firstComment"])
                elif itemNo == 9:
                    newString = Organizer.emend(self.currentTableContentValues[rowNo]["firstLyrics"])
                    item = self.createTableWidgetItem(newString,
                                                      self.currentTableContentValues[rowNo]["firstLyrics"])
                if item != None:
                    self.setItem(rowNo, itemNo, item)
            Dialogs.showState(translate("Tables", "Generating .."), rowNo + 1, allItemNumber)

    def correctTable(self):
        for rowNo in range(self.rowCount()):
            for itemNo in range(self.columnCount()):
                if self.isChangeableItem(rowNo, itemNo):
                    if itemNo == 0:
                        newString = Organizer.emend(str(self.item(rowNo, itemNo).text()), "directory")
                    elif itemNo == 1:
                        newString = Organizer.emend(str(self.item(rowNo, itemNo).text()), "file")
                    else:
                        newString = Organizer.emend(str(self.item(rowNo, itemNo).text()))
                    self.item(rowNo, itemNo).setText(str(newString))

    def getValueByRowAndColumn(self, _rowNo, _columnNo):
        if _columnNo == 0:
            return self.currentTableContentValues[_rowNo]["baseNameOfDirectory"]
        elif _columnNo == 1:
            return self.currentTableContentValues[_rowNo]["baseName"]
        elif _columnNo == 2:
            return self.currentTableContentValues[_rowNo]["artist"]
        elif _columnNo == 3:
            return self.currentTableContentValues[_rowNo]["title"]
        elif _columnNo == 4:
            return self.currentTableContentValues[_rowNo]["album"]
        elif _columnNo == 5:
            return self.currentTableContentValues[_rowNo]["trackNum"]
        elif _columnNo == 6:
            return self.currentTableContentValues[_rowNo]["year"]
        elif _columnNo == 7:
            return self.currentTableContentValues[_rowNo]["genre"]
        elif _columnNo == 8:
            return self.currentTableContentValues[_rowNo]["firstComment"]
        elif _columnNo == 9:
            return self.currentTableContentValues[_rowNo]["firstLyrics"]
        return ""
