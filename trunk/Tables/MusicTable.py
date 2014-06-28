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
        allItemNumber = len(self.values)
        Dialogs.showState(translate("FileUtils/Musics", "Writing Music Tags"), 0, allItemNumber, True)
        for rowNo in range(self.rowCount()):
            isContinueThreadAction = uni.isContinueThreadAction()
            if isContinueThreadAction:
                try:
                    changingTag = {"path": self.values[rowNo]["path"]}
                    if fu.isWritableFileOrDir(self.values[rowNo]["path"], False, True):
                        if self.isRowHidden(rowNo):
                            fu.removeFileOrDir(self.values[rowNo]["path"])
                            self.changedValueNumber += 1
                        else:
                            baseNameOfDirectory = str(
                                self.values[rowNo]["baseNameOfDirectory"])
                            baseName = str(self.values[rowNo]["baseName"])
                            tagger = Taggers.getTagger()
                            tagger.loadFileForWrite(self.values[rowNo]["path"])
                            isCheckLike = Taggers.getSelectedTaggerTypeForRead() == Taggers.getSelectedTaggerTypeForWrite()
                            if self.isChangeableItem(rowNo, 2,
                                                     self.values[rowNo]["artist"], True,
                                                           isCheckLike):
                                value = str(self.item(rowNo, 2).text())
                                tagger.setArtist(value)
                                changingTag["artist"] = value
                                Records.add(str(translate("MusicTable", "Artist")),
                                            str(self.values[rowNo]["artist"]), value)
                                self.changedValueNumber += 1
                            if self.isChangeableItem(rowNo, 3,
                                                     self.values[rowNo]["title"], True,
                                                           isCheckLike):
                                value = str(self.item(rowNo, 3).text())
                                tagger.setTitle(value)
                                changingTag["title"] = value
                                Records.add(str(translate("MusicTable", "Title")),
                                            str(self.values[rowNo]["title"]), value)
                                self.changedValueNumber += 1
                            if self.isChangeableItem(rowNo, 4,
                                                     self.values[rowNo]["album"], True,
                                                           isCheckLike):
                                value = str(self.item(rowNo, 4).text())
                                tagger.setAlbum(value)
                                changingTag["album"] = value
                                Records.add(str(translate("MusicTable", "Album")),
                                            str(self.values[rowNo]["album"]), value)
                                self.changedValueNumber += 1
                            if self.isChangeableItem(rowNo, 5,
                                                     self.values[rowNo]["trackNum"],
                                                           True, isCheckLike):
                                value = str(self.item(rowNo, 5).text())
                                tagger.setTrackNum(value)
                                changingTag["trackNum"] = value
                                Records.add(str(translate("MusicTable", "Track No")),
                                            str(self.values[rowNo]["trackNum"]), value)
                                self.changedValueNumber += 1
                            if self.isChangeableItem(rowNo, 6,
                                                     self.values[rowNo]["year"], True,
                                                           isCheckLike):
                                value = str(self.item(rowNo, 6).text())
                                tagger.setDate(value)
                                changingTag["year"] = value
                                Records.add(str(translate("MusicTable", "Year")),
                                            str(self.values[rowNo]["year"]), value)
                                self.changedValueNumber += 1
                            if self.isChangeableItem(rowNo, 7,
                                                     self.values[rowNo]["genre"], True,
                                                           isCheckLike):
                                value = str(self.item(rowNo, 7).text())
                                tagger.setGenre(value)
                                changingTag["genre"] = value
                                Records.add(str(translate("MusicTable", "Genre")),
                                            str(self.values[rowNo]["genre"]), value)
                                self.changedValueNumber += 1
                            if self.isChangeableItem(rowNo, 8,
                                                     self.values[rowNo]["firstComment"],
                                                           True, isCheckLike):
                                value = str(self.item(rowNo, 8).text())
                                tagger.setFirstComment(value)
                                changingTag["firstComment"] = value
                                Records.add(str(translate("MusicTable", "Comment")),
                                            str(self.values[rowNo]["firstComment"]), value)
                                self.changedValueNumber += 1
                            if len(self.tableColumns) > 9 and self.isChangeableItem(rowNo, 9,
                                                                                    self.values[
                                                                                                    rowNo][
                                                                                                    "firstLyrics"],
                                                                                                True, isCheckLike):
                                value = str(self.item(rowNo, 9).text())
                                tagger.setFirstLyrics(value)
                                changingTag["firstLyrics"] = value
                                Records.add(str(translate("MusicTable", "Lyrics")),
                                            str(self.values[rowNo]["firstLyrics"]), value)
                                self.changedValueNumber += 1
                            if len(changingTag) > 1:
                                changingTags.append(changingTag)
                            tagger.update()
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
        MusicDetails.MusicDetails(self.values[_fileNo]["path"],
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
                              ) % Organizer.getLink(self.values[_row]["path"]))

    def refreshColumns(self):
        self.tableColumns = Taggers.getAvailableLabelsForTable()
        self.tableColumnsKey = Taggers.getAvailableKeysForTable()

    def saveTable(self):
        self.checkFileExtensions(1, "baseName")
        MusicDetails.MusicDetails.closeAllMusicDialogs()
        return self.writeContents()

    def refreshTable(self, _path):
        self.values = []
        self.setColumnWidth(5, 70)
        self.setColumnWidth(6, 40)
        musicFileNames = fu.readDirectory(_path, "music", uni.getBoolValue("isShowHiddensInMusicTable"))
        isCanNoncompatible = False
        allItemNumber = len(musicFileNames)
        uni.startThreadAction()
        baseNameOfDirectory = fu.getBaseName(_path)
        rowNo = 0
        self.setRowCount(allItemNumber)
        for musicName in musicFileNames:
            isContinueThreadAction = uni.isContinueThreadAction()
            if isContinueThreadAction:
                try:
                    if fu.isReadableFileOrDir(fu.joinPath(_path, musicName), False, True):
                        tagger = Taggers.getTagger()
                        try:
                            tagger.loadFile(fu.joinPath(_path, musicName))
                        except:
                            Dialogs.showError(translate("FileUtils/Musics", "Incorrect Tag"),
                                              str(translate("FileUtils/Musics",
                                                            "\"%s\" : this file has the incorrect tag so can't read tags.")
                                              ) % Organizer.getLink(fu.joinPath(_path, musicName)))
                        if tagger.isAvailableFile() == False:
                            isCanNoncompatible = True
                        content = {}
                        content["path"] = fu.joinPath(_path, musicName)
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
                        self.values.append(content)

                        newBaseNameOfDirectory = Organizer.emend(
                            self.values[rowNo]["baseNameOfDirectory"], "directory")
                        itemBaseNameOfDirectory = self.createTableWidgetItem(newBaseNameOfDirectory,
                                                                             self.values[rowNo][
                                                                                 "baseNameOfDirectory"])
                        self.setItem(rowNo, 0, itemBaseNameOfDirectory)

                        newBaseName = Organizer.emend(self.values[rowNo]["baseName"], "file")
                        itemBaseName = self.createTableWidgetItem(newBaseName,
                                                                  self.values[rowNo]["baseName"])
                        self.setItem(rowNo, 1, itemBaseName)

                        newArtist = Organizer.emend(self.values[rowNo]["artist"])
                        itemArtist = self.createTableWidgetItem(newArtist, self.values[rowNo]["artist"])
                        self.setItem(rowNo, 2, itemArtist)

                        newTitle = Organizer.emend(self.values[rowNo]["title"])
                        itemTitle = self.createTableWidgetItem(newTitle, self.values[rowNo]["title"])
                        self.setItem(rowNo, 3, itemTitle)

                        newAlbum = Organizer.emend(self.values[rowNo]["album"])
                        itemAlbum = self.createTableWidgetItem(newAlbum, self.values[rowNo]["album"])
                        self.setItem(rowNo, 4, itemAlbum)

                        newTrackNum = str(self.values[rowNo]["trackNum"])
                        itemTrackNum = self.createTableWidgetItem(newTrackNum,
                                                                  self.values[rowNo]["trackNum"])
                        self.setItem(rowNo, 5, itemTrackNum)

                        newYear = Organizer.emend(self.values[rowNo]["year"])
                        itemYear = self.createTableWidgetItem(newYear, self.values[rowNo]["year"])
                        self.setItem(rowNo, 6, itemYear)

                        newGenre = Organizer.emend(self.values[rowNo]["genre"])
                        itemGenre = self.createTableWidgetItem(newGenre, self.values[rowNo]["genre"])
                        self.setItem(rowNo, 7, itemGenre)

                        newFirstComment = Organizer.emend(self.values[rowNo]["firstComment"])
                        itemFirstComment = self.createTableWidgetItem(newFirstComment,
                                                                      self.values[rowNo][
                                                                          "firstComment"])
                        self.setItem(rowNo, 8, itemFirstComment)

                        newFirstLyrics = Organizer.emend(self.values[rowNo]["firstLyrics"])
                        itemFirstLyrics = self.createTableWidgetItem(newFirstLyrics,
                                                                     self.values[rowNo]["firstLyrics"])
                        self.setItem(rowNo, 9, itemFirstLyrics)
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
        if isCanNoncompatible:
            Dialogs.show(translate("FileUtils/Musics", "Possible ID3 Mismatch"),
                         translate("FileUtils/Musics",
                                   "Some of the files presented in the table may not support ID3 technology.<br>Please check the files and make sure they support ID3 information before proceeding."))

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
            return self.values[_rowNo]["baseNameOfDirectory"]
        elif _columnNo == 1:
            return self.values[_rowNo]["baseName"]
        elif _columnNo == 2:
            return self.values[_rowNo]["artist"]
        elif _columnNo == 3:
            return self.values[_rowNo]["title"]
        elif _columnNo == 4:
            return self.values[_rowNo]["album"]
        elif _columnNo == 5:
            return self.values[_rowNo]["trackNum"]
        elif _columnNo == 6:
            return self.values[_rowNo]["year"]
        elif _columnNo == 7:
            return self.values[_rowNo]["genre"]
        elif _columnNo == 8:
            return self.values[_rowNo]["firstComment"]
        elif _columnNo == 9:
            return self.values[_rowNo]["firstLyrics"]
        return ""
