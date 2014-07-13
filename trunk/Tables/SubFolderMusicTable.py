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
import SearchEngines
from Core.MyObjects import *
from Details import MusicDetails
from Core import Universals as uni
from Core import Dialogs
import Taggers
from Core import Records
from Core import ReportBug
from Tables import CoreTable
from Taggers import getTaggerTypesName, getSelectedTaggerTypeForReadName, setSelectedTaggerTypeForReadName
from Taggers import getSelectedTaggerTypeForWriteName, setSelectedTaggerTypeForWriteName


class SubFolderMusicTable(CoreTable):
    def __init__(self, *args, **kwargs):
        CoreTable.__init__(self, *args, **kwargs)
        self.keyName = "music"
        self.hiddenTableColumnsSettingKey = "hiddenSubFolderMusicTableColumns"
        self.refreshColumns()
        pbtnVerifyTableValues = MPushButton(translate("SubFolderMusicTable", "Verify Table"))
        pbtnVerifyTableValues.setMenu(SearchEngines.SearchEngines(self))
        self.mContextMenu.addMenu(SearchEngines.SearchEngines(self, True))
        lblSourceDetails = MLabel(translate("MusicOptionsBar", "Read From:"))
        lblTargetDetails = MLabel(translate("MusicOptionsBar", "Write To:"))
        self.MusicTagTypes = getTaggerTypesName()
        self.cbTagSourceType = MComboBox(self)
        self.cbTagSourceType.addItems(self.MusicTagTypes)
        self.cbTagTargetType = MComboBox(self)
        self.cbTagTargetType.addItems(self.MusicTagTypes)
        self.isActiveChanging = False
        self.cbTagSourceType.setCurrentIndex(
            self.cbTagSourceType.findText(getSelectedTaggerTypeForReadName()))
        self.cbTagTargetType.setCurrentIndex(
            self.cbTagTargetType.findText(getSelectedTaggerTypeForWriteName()))
        self.isActiveChanging = True
        self.cbTagSourceType.setToolTip(translate("MusicOptionsBar",
                                                  "You can select the ID3 tag source you want to read.<br><font color=blue>ID3 V2 is recommended.</font>"))
        self.cbTagTargetType.setToolTip(translate("MusicOptionsBar",
                                                  "You can select the ID3 tag target you want to write.<br><font color=blue>ID3 V2 is recommended.</font>"))
        lblDetails = translate("SubDirectoryOptionsBar",
                               "You can select sub directory deep.<br><font color=blue>You can select \"-1\" for all sub directories.</font>")
        lblSubDirectoryDeep = MLabel(str(translate("SubDirectoryOptionsBar", "Deep") + " : "))
        self.SubDirectoryDeeps = [str(x) for x in range(-1, 10)]
        self.cbSubDirectoryDeep = MComboBox(self)
        self.cbSubDirectoryDeep.addItems(self.SubDirectoryDeeps)
        self.cbSubDirectoryDeep.setCurrentIndex(self.cbSubDirectoryDeep.findText(uni.MySettings["subDirectoryDeep"]))
        self.cbSubDirectoryDeep.setToolTip(lblDetails)
        hblTagSourceType = MHBoxLayout()
        hblTagSourceType.addWidget(lblSourceDetails)
        hblTagSourceType.addWidget(self.cbTagSourceType)
        hblTagTargetType = MHBoxLayout()
        hblTagTargetType.addWidget(lblTargetDetails)
        hblTagTargetType.addWidget(self.cbTagTargetType)
        self.vblBoxSourceAndTarget.addLayout(hblTagSourceType)
        self.vblBoxSourceAndTarget.addLayout(hblTagTargetType)
        self.hblBoxOptions.addWidget(pbtnVerifyTableValues)
        hblSubDirectory = MHBoxLayout()
        hblSubDirectory.addWidget(lblSubDirectoryDeep)
        hblSubDirectory.addWidget(self.cbSubDirectoryDeep)
        self.hblBoxOptions.addLayout(hblSubDirectory)
        MObject.connect(self.cbTagSourceType, SIGNAL("currentIndexChanged(int)"), self.musicTagSourceTypeChanged)
        MObject.connect(self.cbTagTargetType, SIGNAL("currentIndexChanged(int)"),
                        self.musicTagTargetTypeChanged)

        MObject.connect(self.cbSubDirectoryDeep, SIGNAL("currentIndexChanged(int)"), self.subDirectoryDeepChanged)

    def writeContents(self):
        self.changedValueNumber = 0
        oldAndNewPathValues = []
        changingTags = []
        if uni.isActiveAmarok and uni.getBoolValue("isSubFolderMusicTableValuesChangeInAmarokDB"):
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
                            isCheckLike = (
                                Taggers.getSelectedTaggerTypeForRead() == Taggers.getSelectedTaggerTypeForWrite() or
                                (uni.isActiveAmarok and
                                 uni.getBoolValue("isSubFolderMusicTableValuesChangeInAmarokDB")))
                            if self.isChangeableItem(rowNo, 2,
                                                     self.values[rowNo]["artist"], True,
                                                     isCheckLike):
                                value = str(self.item(rowNo, 2).text())
                                tagger.setArtist(value)
                                changingTag["artist"] = value
                                Records.add(str(translate("SubFolderMusicTable", "Artist")),
                                            str(self.values[rowNo]["artist"]), value)
                                self.changedValueNumber += 1
                            if self.isChangeableItem(rowNo, 3,
                                                     self.values[rowNo]["title"], True,
                                                     isCheckLike):
                                value = str(self.item(rowNo, 3).text())
                                tagger.setTitle(value)
                                changingTag["title"] = value
                                Records.add(str(translate("SubFolderMusicTable", "Title")),
                                            str(self.values[rowNo]["title"]), value)
                                self.changedValueNumber += 1
                            if self.isChangeableItem(rowNo, 4,
                                                     self.values[rowNo]["album"], True,
                                                     isCheckLike):
                                value = str(self.item(rowNo, 4).text())
                                tagger.setAlbum(value)
                                changingTag["album"] = value
                                Records.add(str(translate("SubFolderMusicTable", "Album")),
                                            str(self.values[rowNo]["album"]), value)
                                self.changedValueNumber += 1
                            if self.isChangeableItem(rowNo, 5,
                                                     self.values[rowNo]["albumArtist"], True,
                                                     isCheckLike):
                                value = str(self.item(rowNo, 5).text())
                                tagger.setAlbumArtist(value)
                                changingTag["albumArtist"] = value
                                Records.add(str(translate("SubFolderMusicTable", "Album Artist")),
                                            str(self.values[rowNo]["albumArtist"]), value)
                                self.changedValueNumber += 1
                            if self.isChangeableItem(rowNo, 6,
                                                     self.values[rowNo]["trackNum"],
                                                     True, isCheckLike):
                                value = str(self.item(rowNo, 6).text())
                                tagger.setTrackNum(value)
                                changingTag["trackNum"] = value
                                Records.add(str(translate("SubFolderMusicTable", "Track No")),
                                            str(self.values[rowNo]["trackNum"]), value)
                                self.changedValueNumber += 1
                            if self.isChangeableItem(rowNo, 7,
                                                     self.values[rowNo]["year"], True,
                                                     isCheckLike):
                                value = str(self.item(rowNo, 7).text())
                                tagger.setDate(value)
                                changingTag["year"] = value
                                Records.add(str(translate("SubFolderMusicTable", "Year")),
                                            str(self.values[rowNo]["year"]), value)
                                self.changedValueNumber += 1
                            if self.isChangeableItem(rowNo, 8,
                                                     self.values[rowNo]["genre"], True,
                                                     isCheckLike):
                                value = str(self.item(rowNo, 8).text())
                                tagger.setGenre(value)
                                changingTag["genre"] = value
                                Records.add(str(translate("SubFolderMusicTable", "Genre")),
                                            str(self.values[rowNo]["genre"]), value)
                                self.changedValueNumber += 1
                            if self.isChangeableItem(rowNo, 9,
                                                     self.values[rowNo]["firstComment"],
                                                     True, isCheckLike):
                                value = str(self.item(rowNo, 9).text())
                                tagger.setFirstComment(value)
                                changingTag["firstComment"] = value
                                Records.add(str(translate("SubFolderMusicTable", "Comment")),
                                            str(self.values[rowNo]["firstComment"]), value)
                                self.changedValueNumber += 1
                            if (self.tableColumnsKey.count("Lyrics") > 0 and
                                    self.isChangeableItem(rowNo, 10,
                                                          self.values[rowNo]["firstLyrics"], True, isCheckLike)):
                                value = str(self.item(rowNo, 10).text())
                                tagger.setFirstLyrics(value)
                                changingTag["firstLyrics"] = value
                                Records.add(str(translate("SubFolderMusicTable", "Lyrics")),
                                            str(self.values[rowNo]["firstLyrics"]), value)
                                self.changedValueNumber += 1
                            if len(changingTag) > 1:
                                changingTags.append(changingTag)
                            tagger.update()
                            if self.isChangeableItem(rowNo, 0, baseNameOfDirectory):
                                baseNameOfDirectory = str(self.item(rowNo, 0).text())
                                self.changedValueNumber += 1
                                newDirectoryPath = fu.joinPath(
                                    fu.getDirName(fu.getDirName(self.values[rowNo]["path"])),
                                    baseNameOfDirectory)
                                self.setNewDirectory(newDirectoryPath)
                            if self.isChangeableItem(rowNo, 1, baseName, False):
                                baseName = str(self.item(rowNo, 1).text())
                                self.changedValueNumber += 1
                            newFilePath = fu.joinPath(str(self.values[rowNo]["path"]).replace(
                                fu.joinPath(str(self.values[rowNo]["baseNameOfDirectory"]),
                                            str(self.values[rowNo]["baseName"])), ""),
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
            Dialogs.showState(translate("FileUtils/Musics", "Writing Music Tags And Informations"),
                              rowNo + 1, allItemNumber, True)
            if isContinueThreadAction == False:
                break
        uni.finishThreadAction()
        if uni.isActiveAmarok and uni.getBoolValue("isSubFolderMusicTableValuesChangeInAmarokDB"):
            import Amarok
            from Amarok import Operations

            Operations.changeTags(changingTags)
            if len(oldAndNewPathValues) > 0:
                Operations.changePaths(oldAndNewPathValues, "file")
        return True

    def showTableDetails(self, _fileNo, _infoNo):
        MusicDetails.MusicDetails(self.values[_fileNo]["path"], uni.getBoolValue("isOpenDetailsInNewWindow"))

    def cellClickedTable(self, _row, _column):
        currentItem = self.currentItem()
        if currentItem is not None:
            cellLenght = len(currentItem.text()) * 8
            if cellLenght > self.columnWidth(_column):
                self.setColumnWidth(_column, cellLenght)
            if _column == 9 or _column == 10:
                if self.rowHeight(_row) < 150:
                    self.setRowHeight(_row, 150)
                if self.columnWidth(_column) < 250:
                    self.setColumnWidth(_column, 250)

    def cellDoubleClickedTable(self, _row, _column):
        try:
            if _column == 9 or _column == 10:
                self.showTableDetails(_row, _column)
            else:
                if uni.getBoolValue("isRunOnDoubleClick"):
                    self.showTableDetails(_row, _column)
        except:
            Dialogs.showError(translate("SubFolderMusicTable", "Cannot Open Music File"),
                              str(translate("SubFolderMusicTable",
                                            "\"%s\" : cannot be opened. Please make sure that you selected a music file.")
                              ) % Organizer.getLink(self.values[_row]["path"]))

    def refreshColumns(self):
        self.tableColumns = Taggers.getAvailableLabelsForTable()
        self.tableColumnsKey = Taggers.getAvailableKeysForTable()
        self.valueKeys = ["baseNameOfDirectory", "baseName", "artist", "title", "album",
                          "trackNum", "year", "genre", "firstComment", "firstLyrics"]

    def saveTable(self):
        self.checkFileExtensions(1, "baseName")
        MusicDetails.MusicDetails.closeAllMusicDialogs()
        return self.writeContents()

    def refreshTable(self, _path):
        self.values = []
        self.setColumnWidth(6, 70)
        self.setColumnWidth(7, 40)
        musicFileNames = fu.readDirectoryWithSubDirectoriesThread(_path,
                                                                  int(uni.MySettings["subDirectoryDeep"]), "music",
                                                                  uni.getBoolValue(
                                                                      "isShowHiddensInSubFolderMusicTable"))
        isCanNoncompatible = False
        allItemNumber = len(musicFileNames)
        uni.startThreadAction()
        rowNo = 0
        self.setRowCount(allItemNumber)
        for musicName in musicFileNames:
            isContinueThreadAction = uni.isContinueThreadAction()
            if isContinueThreadAction:
                try:
                    if fu.isReadableFileOrDir(musicName, False, True):
                        tagger = Taggers.getTagger()
                        try:
                            tagger.loadFile(musicName)
                        except:
                            Dialogs.showError(translate("FileUtils/Musics", "Incorrect Tag"),
                                              str(translate("FileUtils/Musics",
                                                            "\"%s\" : this file has the incorrect tag so can't read tags.")
                                              ) % Organizer.getLink(musicName))
                        if tagger.isAvailableFile() == False:
                            isCanNoncompatible = True
                        content = {}
                        content["path"] = musicName
                        content["baseNameOfDirectory"] = str(
                            str(fu.getBaseName(_path)) + str(fu.getDirName(musicName)).replace(_path, ""))
                        content["baseName"] = fu.getBaseName(musicName)
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
                        itemBaseNameOfDirectory = self.createItem(newBaseNameOfDirectory,
                                                                             self.values[rowNo][
                                                                                 "baseNameOfDirectory"])
                        self.setItem(rowNo, 0, itemBaseNameOfDirectory)

                        newBaseName = Organizer.emend(self.values[rowNo]["baseName"], "file")
                        itemBaseName = self.createItem(newBaseName,
                                                                  self.values[rowNo]["baseName"])
                        self.setItem(rowNo, 1, itemBaseName)

                        newArtist = Organizer.emend(self.values[rowNo]["artist"])
                        itemArtist = self.createItem(newArtist, self.values[rowNo]["artist"])
                        self.setItem(rowNo, 2, itemArtist)

                        newTitle = Organizer.emend(self.values[rowNo]["title"])
                        itemTitle = self.createItem(newTitle, self.values[rowNo]["title"])
                        self.setItem(rowNo, 3, itemTitle)

                        newAlbum = Organizer.emend(self.values[rowNo]["album"])
                        itemAlbum = self.createItem(newAlbum, self.values[rowNo]["album"])
                        self.setItem(rowNo, 4, itemAlbum)

                        newAlbumArtist = Organizer.emend(self.values[rowNo]["albumArtist"])
                        itemAlbumArtist = self.createItem(newAlbumArtist,
                                                                     self.values[rowNo]["albumArtist"])
                        self.setItem(rowNo, 5, itemAlbumArtist)

                        newTrackNum = str(self.values[rowNo]["trackNum"])
                        itemTrackNum = self.createItem(newTrackNum,
                                                                  self.values[rowNo]["trackNum"])
                        self.setItem(rowNo, 6, itemTrackNum)

                        newYear = Organizer.emend(self.values[rowNo]["year"])
                        itemYear = self.createItem(newYear, self.values[rowNo]["year"])
                        self.setItem(rowNo, 7, itemYear)

                        newGenre = Organizer.emend(self.values[rowNo]["genre"])
                        itemGenre = self.createItem(newGenre, self.values[rowNo]["genre"])
                        self.setItem(rowNo, 8, itemGenre)

                        newFirstComment = Organizer.emend(self.values[rowNo]["firstComment"])
                        itemFirstComment = self.createItem(newFirstComment,
                                                                      self.values[rowNo][
                                                                          "firstComment"])
                        self.setItem(rowNo, 9, itemFirstComment)

                        newFirstLyrics = Organizer.emend(self.values[rowNo]["firstLyrics"])
                        itemFirstLyrics = self.createItem(newFirstLyrics,
                                                                     self.values[rowNo]["firstLyrics"])
                        self.setItem(rowNo, 10, itemFirstLyrics)
                        rowNo += 1
                    else:
                        allItemNumber -= 1
                except:
                    ReportBug.ReportBug()
                    allItemNumber -= 1
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

    def musicTagSourceTypeChanged(self, _action=None):
        try:
            selectedType = str(self.MusicTagTypes[_action])
            if self.checkUnSavedValues():
                setSelectedTaggerTypeForReadName(selectedType)
                self.refreshForColumns()
                getMainWindow().SpecialTools.refreshForColumns()
                self.refresh(getMainWindow().FileManager.getCurrentDirectoryPath())
            self.cbTagSourceType.setCurrentIndex(
                self.cbTagSourceType.findText(getSelectedTaggerTypeForReadName()))
        except:
            ReportBug.ReportBug()

    def musicTagTargetTypeChanged(self, _action=None):
        try:
            selectedType = str(self.MusicTagTypes[_action])
            setSelectedTaggerTypeForWriteName(selectedType)
            self.cbTagTargetType.setCurrentIndex(
                self.cbTagTargetType.findText(getSelectedTaggerTypeForWriteName()))
        except:
            ReportBug.ReportBug()

    def subDirectoryDeepChanged(self, _action=None):
        try:
            selectedDeep = str(self.SubDirectoryDeeps[_action])
            if self.checkUnSavedValues():
                uni.setMySetting("subDirectoryDeep", int(selectedDeep))
                self.refreshForColumns()
                getMainWindow().SpecialTools.refreshForColumns()
                self.refresh(getMainWindow().FileManager.getCurrentDirectoryPath())
            self.cbSubDirectoryDeep.setCurrentIndex(
                self.cbSubDirectoryDeep.findText(str(uni.MySettings["subDirectoryDeep"])))
        except:
            ReportBug.ReportBug()


