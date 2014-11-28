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
import FileUtils as fu
import SearchEngines
from Core.MyObjects import *
import Details
from Core import Universals as uni
from Core import Dialogs
import Taggers
from Core import Records
from Core import ReportBug
from Tables import CoreTable
import Amarok


class AmarokMusicTable(CoreTable):
    def __init__(self, *args, **kwargs):
        CoreTable.__init__(self, *args, **kwargs)
        from Amarok import Filter

        self.keyName = "music"
        self.amarokFilterKeyName = "AmarokFilterAmarokMusicTable"
        self.hiddenTableColumnsSettingKey = "hiddenAmarokMusicTableColumns"
        self.refreshColumns()
        pbtnVerifyTableValues = MPushButton(translate("MusicTable", "Verify Table"))
        pbtnVerifyTableValues.setMenu(SearchEngines.SearchEngines(self, "music"))
        self.mContextMenu.addMenu(SearchEngines.SearchEngines(self, "music", True))
        lblSourceDetails = MLabel(translate("MusicTable", "Read From:"))
        lblTargetDetails = MLabel(translate("MusicTable", "Write To:"))
        self.MusicTagSourceTypes = Amarok.getTagSourceTypes()
        self.cbTagSourceType = MComboBox(self)
        self.cbTagSourceType.addItems(self.MusicTagSourceTypes)
        self.MusicTagTargetTypes = Amarok.getTagTargetTypes()
        self.cbTagTargetType = MComboBox(self)
        self.cbTagTargetType.addItems(self.MusicTagTargetTypes)
        self.cbTagSourceType.setCurrentIndex(
            self.cbTagSourceType.findText(Amarok.getSelectedTagSourseType("AmarokMusicTable")))
        self.cbTagTargetType.setCurrentIndex(
            self.cbTagTargetType.findText(Amarok.getSelectedTagTargetType("AmarokMusicTable")))
        self.cbTagSourceType.setToolTip(translate("MusicTable",
                                                  "You can select the ID3 tag source you want to read.<br><font color=blue>Amarok (Smart) is recommended.</font>"))
        self.cbTagTargetType.setToolTip(translate("MusicTable",
                                                  "You can select the ID3 tag target you want to write.<br><font color=blue>Amarok + ID3 V2 is recommended.</font>"))
        hblTagSourceType = MHBoxLayout()
        hblTagSourceType.addWidget(lblSourceDetails)
        hblTagSourceType.addWidget(self.cbTagSourceType)
        hblTagTargetType = MHBoxLayout()
        hblTagTargetType.addWidget(lblTargetDetails)
        hblTagTargetType.addWidget(self.cbTagTargetType)
        self.vblBoxSourceAndTarget.addLayout(hblTagSourceType)
        self.vblBoxSourceAndTarget.addLayout(hblTagTargetType)
        MObject.connect(self.cbTagSourceType, SIGNAL("currentIndexChanged(int)"), self.musicTagSourceTypeChanged)
        MObject.connect(self.cbTagTargetType, SIGNAL("currentIndexChanged(int)"), self.musicTagTargetTypeChanged)
        self.hblBoxOptions.addWidget(pbtnVerifyTableValues)
        self.wFilter = Filter.FilterWidget(self, self.amarokFilterKeyName)
        self.hblBoxOptions.addWidget(self.wFilter)

    def writeContents(self):
        self.changedValueNumber = 0
        oldAndNewPathValues = []
        changingTags = []
        uni.startThreadAction()
        import Amarok

        allItemNumber = len(self.values)
        Dialogs.showState(translate("FileUtils/Musics", "Writing Music Tags"), 0, allItemNumber, True)
        for rowNo in range(self.rowCount()):
            isContinueThreadAction = uni.isContinueThreadAction()
            if isContinueThreadAction:
                try:
                    if self.isRowHidden(rowNo):
                        isWritableFileOrDir = fu.isFile(
                            self.values[rowNo]["path"]) and fu.isWritableFileOrDir(
                            self.values[rowNo]["path"], False, True)
                        if isWritableFileOrDir:
                            fu.removeFileOrDir(self.values[rowNo]["path"])
                            self.changedValueNumber += 1
                    else:
                        changingTag = {"path": self.values[rowNo]["path"]}
                        isWritableFileOrDir = fu.isFile(
                            self.values[rowNo]["path"]) and fu.isWritableFileOrDir(
                            self.values[rowNo]["path"], False, True)
                        isSetTagOfFile = False
                        if isWritableFileOrDir:
                            baseNameOfDirectory = str(
                                self.values[rowNo]["baseNameOfDirectory"])
                            baseName = str(self.values[rowNo]["baseName"])
                            if Amarok.getSelectedTagTargetType("AmarokMusicTable").find("ID3") > -1:
                                typeTemp = Amarok.getSelectedTagTargetType("AmarokMusicTable").split(" + ")
                                if len(typeTemp) > 1:
                                    taggerType = typeTemp[1]
                                else:
                                    taggerType = typeTemp[0]
                                Taggers.setSelectedTaggerTypeForWriteName(taggerType)
                                isSetTagOfFile = True
                                tagger = Taggers.getTagger()
                                tagger.loadFileForWrite(self.values[rowNo]["path"])
                        if self.isChangeableItem(rowNo, "artist"):
                            value = str(self.item(rowNo, 2).text())
                            if isSetTagOfFile: tagger.setArtist(value)
                            changingTag["artist"] = value
                            Records.add(str(translate("MusicTable", "Artist")),
                                        str(self.values[rowNo]["artist"]), value)
                            self.changedValueNumber += 1
                        if self.isChangeableItem(rowNo, "title"):
                            value = str(self.item(rowNo, 3).text())
                            if isSetTagOfFile: tagger.setTitle(value)
                            changingTag["title"] = value
                            Records.add(str(translate("MusicTable", "Title")),
                                        str(self.values[rowNo]["title"]), value)
                            self.changedValueNumber += 1
                        if self.isChangeableItem(rowNo, "album"):
                            value = str(self.item(rowNo, 4).text())
                            if isSetTagOfFile: tagger.setAlbum(value)
                            changingTag["album"] = value
                            Records.add(str(translate("MusicTable", "Album")),
                                        str(self.values[rowNo]["album"]), value)
                            self.changedValueNumber += 1
                        if self.isChangeableItem(rowNo, "albumArtist"):
                            value = str(self.item(rowNo, 5).text())
                            if isSetTagOfFile: tagger.setAlbumArtist(value)
                            changingTag["albumArtist"] = value
                            Records.add(str(translate("MusicTable", "Album Artist")),
                                        str(self.values[rowNo]["albumArtist"]), value)
                            self.changedValueNumber += 1
                        if self.isChangeableItem(rowNo, "trackNum"):
                            value = str(self.item(rowNo, 6).text())
                            if isSetTagOfFile: tagger.setTrackNum(value)
                            changingTag["trackNum"] = value
                            Records.add(str(translate("MusicTable", "Track No")),
                                        str(self.values[rowNo]["trackNum"]), value)
                            self.changedValueNumber += 1
                        if self.isChangeableItem(rowNo, "year"):
                            value = str(self.item(rowNo, 7).text())
                            if isSetTagOfFile: tagger.setDate(value)
                            changingTag["year"] = value
                            Records.add(str(translate("MusicTable", "Year")),
                                        str(self.values[rowNo]["year"]), value)
                            self.changedValueNumber += 1
                        if self.isChangeableItem(rowNo, "genre"):
                            value = str(self.item(rowNo, 8).text())
                            if isSetTagOfFile: tagger.setGenre(value)
                            changingTag["genre"] = value
                            Records.add(str(translate("MusicTable", "Genre")),
                                        str(self.values[rowNo]["genre"]), value)
                            self.changedValueNumber += 1
                        if self.isChangeableItem(rowNo, "firstComment"):
                            value = str(self.item(rowNo, 9).text())
                            if isSetTagOfFile: tagger.setFirstComment(value)
                            changingTag["firstComment"] = value
                            Records.add(str(translate("MusicTable", "Comment")),
                                        str(self.values[rowNo]["firstComment"]), value)
                            self.changedValueNumber += 1
                        if self.isChangeableItem(rowNo, "firstLyrics"):
                            value = str(self.item(rowNo, 10).text())
                            if isSetTagOfFile: tagger.setFirstLyrics(value)
                            changingTag["firstLyrics"] = value
                            Records.add(str(translate("MusicTable", "Lyrics")),
                                        str(self.values[rowNo]["firstLyrics"]), value)
                            self.changedValueNumber += 1
                        if len(changingTag) > 1:
                            changingTags.append(changingTag)
                        if isWritableFileOrDir:
                            if isSetTagOfFile:
                                tagger.update()
                            if self.isChangeableItem(rowNo, "baseNameOfDirectory", baseNameOfDirectory):
                                baseNameOfDirectory = str(self.item(rowNo, 0).text())
                                self.changedValueNumber += 1
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
                except:
                    ReportBug.ReportBug()
            else:
                allItemNumber = rowNo + 1
            Dialogs.showState(translate("FileUtils/Musics", "Writing Music Tags And Informations"), rowNo + 1, allItemNumber, True)
            if isContinueThreadAction is False:
                break
        uni.finishThreadAction()
        from Amarok import Operations

        if Amarok.getSelectedTagTargetType("AmarokMusicTable").find("Amarok") > -1:
            Operations.changeTags(changingTags)
        if len(oldAndNewPathValues) > 0:
            Operations.changePaths(oldAndNewPathValues, "file")
        return True

    def showTableDetails(self, _fileNo, _infoNo):
        Details.Details(self.values[_fileNo]["path"], uni.getBoolValue("isOpenDetailsInNewWindow"))

    def cellClickedTable(self, _row, _column):
        currentItem = self.currentItem()
        if currentItem is not None:
            if _column == 9 or _column == 10:
                if self.rowHeight(_row) < 150:
                    self.setRowHeight(_row, 150)
                if self.columnWidth(_column) < 250:
                    self.setColumnWidth(_column, 250)
            else:
                cellLenght = len(currentItem.text()) * 8
                if cellLenght > self.columnWidth(_column):
                    self.setColumnWidth(_column, cellLenght)


    def cellDoubleClickedTable(self, _row, _column):
        try:
            if _column == 9 or _column == 10:
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
        self.tableReadOnlyColumnsKey = Taggers.getReadOnlyKeysForTable()

    def saveTable(self):
        Details.closeAllDialogs()
        self.checkFileExtensions("baseName", "baseName")
        return self.writeContents()

    def refreshTable(self, _path):
        self.values = []
        self.setColumnWidth(6, 70)
        self.setColumnWidth(7, 40)
        uni.startThreadAction()
        import Amarok

        Dialogs.showState(translate("AmarokMusicTable", "Getting Values From Amarok"), 0, 1)
        if Amarok.checkAmarok():
            isContinueThreadAction = uni.isContinueThreadAction()
            if isContinueThreadAction:
                from Amarok import Operations

                musicFileValuesWithNames = Operations.getAllMusicFileValuesWithNames(
                    uni.MySettings[self.amarokFilterKeyName])
                Dialogs.showState(translate("AmarokMusicTable", "Values Are Being Processed"), 1, 1)
                isContinueThreadAction = uni.isContinueThreadAction()
                if isContinueThreadAction:
                    if musicFileValuesWithNames is not None:
                        allItemNumber = len(musicFileValuesWithNames)
                        self.setRowCount(allItemNumber)
                        rowNo = 0
                        for musicFileRow in musicFileValuesWithNames:
                            isContinueThreadAction = uni.isContinueThreadAction()
                            if isContinueThreadAction:
                                try:
                                    if fu.isFile(musicFileRow["filePath"]) and fu.isReadableFileOrDir(
                                        musicFileRow["filePath"], False, True):
                                        if Amarok.getSelectedTagSourseType("AmarokMusicTable") == "Amarok (Smart)":
                                            content = {}
                                            content["path"] = musicFileRow["filePath"]
                                            content["baseNameOfDirectory"] = fu.getBaseName(
                                                fu.getDirName(musicFileRow["filePath"]))
                                            content["baseName"] = fu.getBaseName(musicFileRow["filePath"])
                                            content["artist"] = musicFileRow["artist"]
                                            content["title"] = musicFileRow["title"]
                                            content["album"] = musicFileRow["album"]
                                            content["albumArtist"] = musicFileRow["albumArtist"]
                                            content["trackNum"] = musicFileRow["trackNumber"]
                                            content["year"] = musicFileRow["year"]
                                            content["genre"] = musicFileRow["genre"]
                                            content["firstComment"] = musicFileRow["comment"]
                                            content["firstLyrics"] = musicFileRow["lyrics"]
                                            tagger = Taggers.getTagger()
                                            try:
                                                tagger.loadFile(musicFileRow["filePath"])
                                            except:
                                                pass
                                            else:
                                                if content["artist"].strip() == "":
                                                    content["artist"] = tagger.getArtist()
                                                if content["title"].strip() == "":
                                                    content["title"] = tagger.getTitle()
                                                if content["album"].strip() == "":
                                                    content["album"] = tagger.getAlbum()
                                                if content["albumArtist"].strip() == "":
                                                    content["albumArtist"] = tagger.getAlbumArtist()
                                                if str(content["trackNum"]).strip() == "":
                                                    content["trackNum"] = tagger.getTrackNum()
                                                if str(content["year"]).strip() == "":
                                                    content["year"] = tagger.getYear()
                                                if content["genre"].strip() == "":
                                                    content["genre"] = tagger.getGenre()
                                                if content["firstComment"].strip() == "":
                                                    content["firstComment"] = tagger.getFirstComment()
                                                if content["firstLyrics"].strip() == "":
                                                    content["firstLyrics"] = tagger.getFirstLyrics()
                                            self.values.append(content)
                                        elif Amarok.getSelectedTagSourseType("AmarokMusicTable") == "Only Amarok":
                                            content = {}
                                            content["path"] = musicFileRow["filePath"]
                                            content["baseNameOfDirectory"] = fu.getBaseName(
                                                fu.getDirName(musicFileRow["filePath"]))
                                            content["baseName"] = fu.getBaseName(musicFileRow["filePath"])
                                            content["artist"] = musicFileRow["artist"]
                                            content["title"] = musicFileRow["title"]
                                            content["album"] = musicFileRow["album"]
                                            content["albumArtist"] = musicFileRow["albumArtist"]
                                            content["trackNum"] = musicFileRow["trackNumber"]
                                            content["year"] = musicFileRow["year"]
                                            content["genre"] = musicFileRow["genre"]
                                            content["firstComment"] = musicFileRow["comment"]
                                            content["firstLyrics"] = musicFileRow["lyrics"]
                                            self.values.append(content)
                                        else:
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
                                            content["albumArtist"] = tagger.getAlbumArtist()
                                            content["trackNum"] = tagger.getTrackNum()
                                            content["year"] = tagger.getYear()
                                            content["genre"] = tagger.getGenre()
                                            content["firstComment"] = tagger.getFirstComment()
                                            content["firstLyrics"] = tagger.getFirstLyrics()
                                            self.values.append(content)
                                        newBaseNameOfDirectory = Organizer.emend(
                                            self.values[rowNo]["baseNameOfDirectory"], "directory")
                                        self.createItem(rowNo, "baseNameOfDirectory", newBaseNameOfDirectory,
                                                        self.values[rowNo]["baseNameOfDirectory"])

                                        newBaseName = Organizer.emend(self.values[rowNo]["baseName"], "file")
                                        self.createItem(rowNo, "baseName", newBaseName, self.values[rowNo]["baseName"])

                                        newArtist = Organizer.emend(self.values[rowNo]["artist"])
                                        self.createItem(rowNo, "artist", newArtist, self.values[rowNo]["artist"])

                                        newTitle = Organizer.emend(self.values[rowNo]["title"])
                                        self.createItem(rowNo, "title", newTitle, self.values[rowNo]["title"])

                                        newAlbum = Organizer.emend(self.values[rowNo]["album"])
                                        self.createItem(rowNo, "album", newAlbum, self.values[rowNo]["album"])

                                        newAlbumArtist = Organizer.emend(self.values[rowNo]["albumArtist"])
                                        self.createItem(rowNo, "albumArtist", newAlbumArtist,
                                                        self.values[rowNo]["albumArtist"])

                                        newTrackNum = str(self.values[rowNo]["trackNum"])
                                        self.createItem(rowNo, "trackNum", newTrackNum, self.values[rowNo]["trackNum"])

                                        newYear = Organizer.emend(self.values[rowNo]["year"])
                                        self.createItem(rowNo, "year", newYear, self.values[rowNo]["year"])

                                        newGenre = Organizer.emend(self.values[rowNo]["genre"])
                                        self.createItem(rowNo, "genre", newGenre, self.values[rowNo]["genre"])

                                        newFirstComment = Organizer.emend(self.values[rowNo]["firstComment"])
                                        self.createItem(rowNo, "firstComment", newFirstComment,
                                                        self.values[rowNo]["firstComment"])

                                        newFirstLyrics = Organizer.emend(self.values[rowNo]["firstLyrics"])
                                        self.createItem(rowNo, "firstLyrics", newFirstLyrics,
                                                        self.values[rowNo]["firstLyrics"])
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
                    elif coloumKey == "baseName":
                        newString = Organizer.emend(str(self.item(rowNo, coloumNo).text()), "file")
                    else:
                        newString = Organizer.emend(str(self.item(rowNo, coloumNo).text()))
                    self.item(rowNo, coloumNo).setText(str(newString))


    def musicTagSourceTypeChanged(self, _action=None):
        try:
            selectedType = str(self.MusicTagSourceTypes[_action])
            if self.checkUnSavedValues():
                Amarok.setSelectedTagSourseType(selectedType, "AmarokMusicTable")
                self.refreshForColumns()
                getMainWindow().SpecialTools.refreshForColumns()
                self.refresh(getMainWindow().FileManager.getCurrentDirectoryPath())
            self.cbTagSourceType.setCurrentIndex(
                self.cbTagSourceType.findText(Amarok.getSelectedTagSourseType("AmarokMusicTable")))
        except:
            ReportBug.ReportBug()

    def musicTagTargetTypeChanged(self, _action=None):
        try:
            selectedType = str(self.MusicTagTargetTypes[_action])
            Amarok.setSelectedTagTargetType(selectedType, "AmarokMusicTable")
            self.cbTagTargetType.setCurrentIndex(
                self.cbTagTargetType.findText(Amarok.getSelectedTagTargetType("AmarokMusicTable")))
        except:
            ReportBug.ReportBug()