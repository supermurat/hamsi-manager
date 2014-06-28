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
import SearchEngines
from Core.MyObjects import *
from Details import MusicDetails
from Core import Universals as uni
from Core import Dialogs
import Taggers
from Core import Records
from Core import ReportBug
from Tables import CoreTable


class MusicTable(CoreTable):
    def __init__(self, *args, **kwargs):
        CoreTable.__init__(self, *args, **kwargs)
        self.keyName = "music"
        self.hiddenTableColumnsSettingKey = "hiddenMusicTableColumns"
        self.refreshColumns()
        pbtnVerifyTableValues = MPushButton(translate("MusicTable", "Verify Table"))
        pbtnVerifyTableValues.setMenu(SearchEngines.SearchEngines(self))
        self.mContextMenu.addMenu(SearchEngines.SearchEngines(self, True))
        self.isPlayNow = MToolButton()
        self.isPlayNow.setToolTip(translate("MusicTable", "Play Now"))
        self.isPlayNow.setIcon(MIcon("Images:playNow.png"))
        self.isPlayNow.setCheckable(True)
        self.isPlayNow.setAutoRaise(True)
        self.isPlayNow.setChecked(uni.getBoolValue("isPlayNow"))
        self.hblBox.insertWidget(self.hblBox.count() - 3, self.isPlayNow)
        self.hblBox.insertWidget(self.hblBox.count() - 1, pbtnVerifyTableValues)

    def readContents(self, _directoryPath):
        currentTableContentValues = []
        musicFileNames = fu.readDirectory(_directoryPath, "music", uni.getBoolValue("isShowHiddensInMusicTable"))
        isCanNoncompatible = False
        allItemNumber = len(musicFileNames)
        uni.startThreadAction()
        baseNameOfDirectory = fu.getBaseName(_directoryPath)
        for musicNo, musicName in enumerate(musicFileNames):
            isContinueThreadAction = uni.isContinueThreadAction()
            if isContinueThreadAction:
                try:
                    if fu.isReadableFileOrDir(fu.joinPath(_directoryPath, musicName), False, True):
                        tagger = Taggers.getTagger()
                        try:
                            tagger.loadFile(fu.joinPath(_directoryPath, musicName))
                        except:
                            Dialogs.showError(translate("FileUtils/Musics", "Incorrect Tag"),
                                              str(translate("FileUtils/Musics",
                                                            "\"%s\" : this file has the incorrect tag so can't read tags.")
                                              ) % Organizer.getLink(fu.joinPath(_directoryPath, musicName)))
                        if tagger.isAvailableFile() == False:
                            isCanNoncompatible = True
                        content = {}
                        content["path"] = fu.joinPath(_directoryPath, musicName)
                        content["baseNameOfDirectory"] = baseNameOfDirectory
                        content["baseName"] = musicName
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
                allItemNumber = musicNo + 1
            Dialogs.showState(translate("FileUtils/Musics", "Reading Music Tags"), musicNo + 1, allItemNumber, True)
            if isContinueThreadAction == False:
                break
        uni.finishThreadAction()
        if isCanNoncompatible:
            Dialogs.show(translate("FileUtils/Musics", "Possible ID3 Mismatch"),
                         translate("FileUtils/Musics",
                                   "Some of the files presented in the table may not support ID3 technology.<br>Please check the files and make sure they support ID3 information before proceeding."))
        return currentTableContentValues

    def writeContents(self):
        self.changedValueNumber = 0
        changingFileDirectories = []
        changingTags = []
        isNewDirectoriesSame = True
        isMovedToNewDirectory = False
        currentDirectoryPath = ""
        newDirectoryPath = ""
        if uni.isActiveAmarok and uni.getBoolValue("isMusicTableValuesChangeInAmarokDB"):
            import Amarok

            if Amarok.checkAmarok(True, False) == False:
                return False
        uni.startThreadAction()
        allItemNumber = len(self.currentTableContentValues)
        Dialogs.showState(translate("FileUtils/Musics", "Writing Music Tags"), 0, allItemNumber, True)
        for rowNo in range(self.rowCount()):
            isContinueThreadAction = uni.isContinueThreadAction()
            if isContinueThreadAction:
                try:
                    changingTag = {"path": self.currentTableContentValues[rowNo]["path"]}
                    if fu.isWritableFileOrDir(self.currentTableContentValues[rowNo]["path"], False, True):
                        if self.isRowHidden(rowNo):
                            fu.removeFileOrDir(self.currentTableContentValues[rowNo]["path"])
                            self.changedValueNumber += 1
                        else:
                            baseNameOfDirectory = str(
                                self.currentTableContentValues[rowNo]["baseNameOfDirectory"])
                            baseName = str(self.currentTableContentValues[rowNo]["baseName"])
                            tagger = Taggers.getTagger()
                            tagger.loadFileForWrite(self.currentTableContentValues[rowNo]["path"])
                            isCheckLike = Taggers.getSelectedTaggerTypeForRead() == Taggers.getSelectedTaggerTypeForWrite()
                            if self.isChangeableItem(rowNo, 2,
                                                     self.currentTableContentValues[rowNo]["artist"], True,
                                                           isCheckLike):
                                value = str(self.item(rowNo, 2).text())
                                tagger.setArtist(value)
                                changingTag["artist"] = value
                                Records.add(str(translate("MusicTable", "Artist")),
                                            str(self.currentTableContentValues[rowNo]["artist"]), value)
                                self.changedValueNumber += 1
                            if self.isChangeableItem(rowNo, 3,
                                                     self.currentTableContentValues[rowNo]["title"], True,
                                                           isCheckLike):
                                value = str(self.item(rowNo, 3).text())
                                tagger.setTitle(value)
                                changingTag["title"] = value
                                Records.add(str(translate("MusicTable", "Title")),
                                            str(self.currentTableContentValues[rowNo]["title"]), value)
                                self.changedValueNumber += 1
                            if self.isChangeableItem(rowNo, 4,
                                                     self.currentTableContentValues[rowNo]["album"], True,
                                                           isCheckLike):
                                value = str(self.item(rowNo, 4).text())
                                tagger.setAlbum(value)
                                changingTag["album"] = value
                                Records.add(str(translate("MusicTable", "Album")),
                                            str(self.currentTableContentValues[rowNo]["album"]), value)
                                self.changedValueNumber += 1
                            if self.isChangeableItem(rowNo, 5,
                                                     self.currentTableContentValues[rowNo]["trackNum"],
                                                           True, isCheckLike):
                                value = str(self.item(rowNo, 5).text())
                                tagger.setTrackNum(value)
                                changingTag["trackNum"] = value
                                Records.add(str(translate("MusicTable", "Track No")),
                                            str(self.currentTableContentValues[rowNo]["trackNum"]), value)
                                self.changedValueNumber += 1
                            if self.isChangeableItem(rowNo, 6,
                                                     self.currentTableContentValues[rowNo]["year"], True,
                                                           isCheckLike):
                                value = str(self.item(rowNo, 6).text())
                                tagger.setDate(value)
                                changingTag["year"] = value
                                Records.add(str(translate("MusicTable", "Year")),
                                            str(self.currentTableContentValues[rowNo]["year"]), value)
                                self.changedValueNumber += 1
                            if self.isChangeableItem(rowNo, 7,
                                                     self.currentTableContentValues[rowNo]["genre"], True,
                                                           isCheckLike):
                                value = str(self.item(rowNo, 7).text())
                                tagger.setGenre(value)
                                changingTag["genre"] = value
                                Records.add(str(translate("MusicTable", "Genre")),
                                            str(self.currentTableContentValues[rowNo]["genre"]), value)
                                self.changedValueNumber += 1
                            if self.isChangeableItem(rowNo, 8,
                                                     self.currentTableContentValues[rowNo]["firstComment"],
                                                           True, isCheckLike):
                                value = str(self.item(rowNo, 8).text())
                                tagger.setFirstComment(value)
                                changingTag["firstComment"] = value
                                Records.add(str(translate("MusicTable", "Comment")),
                                            str(self.currentTableContentValues[rowNo]["firstComment"]), value)
                                self.changedValueNumber += 1
                            if len(self.tableColumns) > 9 and self.isChangeableItem(rowNo, 9,
                                                                                    self.currentTableContentValues[
                                                                                                    rowNo][
                                                                                                    "firstLyrics"],
                                                                                                True, isCheckLike):
                                value = str(self.item(rowNo, 9).text())
                                tagger.setFirstLyrics(value)
                                changingTag["firstLyrics"] = value
                                Records.add(str(translate("MusicTable", "Lyrics")),
                                            str(self.currentTableContentValues[rowNo]["firstLyrics"]), value)
                                self.changedValueNumber += 1
                            if len(changingTag) > 1:
                                changingTags.append(changingTag)
                            tagger.update()
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
            Dialogs.showState(translate("FileUtils/Musics", "Writing Music Tags"), rowNo + 1, allItemNumber, True)
            if isContinueThreadAction == False:
                break
        uni.finishThreadAction()
        pathValues = fu.changeDirectories(changingFileDirectories)
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
                    pathValues += fu.changeDirectories(changingOtherFileDirectories)
        if uni.isActiveAmarok and uni.getBoolValue("isMusicTableValuesChangeInAmarokDB"):
            import Amarok
            from Amarok import Operations

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
            Dialogs.showError(translate("MusicTable", "Cannot Open Music File"),
                              str(translate("MusicTable",
                                            "\"%s\" : cannot be opened. Please make sure that you selected a music file.")
                              ) % Organizer.getLink(self.currentTableContentValues[_row]["path"]))

    def refreshColumns(self):
        self.tableColumns = Taggers.getAvailableLabelsForTable()
        self.tableColumnsKey = Taggers.getAvailableKeysForTable()

    def saveTable(self):
        self.checkFileExtensions(1, "baseName")
        MusicDetails.MusicDetails.closeAllMusicDialogs()
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
