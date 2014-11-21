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
import Details
from Core import Universals as uni
from Core import Dialogs
import Taggers
from Core import Records
from Core import ReportBug
from Tables import CoreTable
from Taggers import getTaggerTypesName, getSelectedTaggerTypeForReadName, setSelectedTaggerTypeForReadName
from Taggers import getSelectedTaggerTypeForWriteName, setSelectedTaggerTypeForWriteName


class MusicTable(CoreTable):
    def __init__(self, *args, **kwargs):
        CoreTable.__init__(self, *args, **kwargs)
        self.keyName = "music"
        self.hiddenTableColumnsSettingKey = "hiddenMusicTableColumns"
        self.refreshColumns()
        pbtnVerifyTableValues = MPushButton(translate("MusicTable", "Verify Table"))
        pbtnVerifyTableValues.setMenu(SearchEngines.SearchEngines(self, "music"))
        self.mContextMenu.addMenu(SearchEngines.SearchEngines(self, "music", True))
        lblSourceDetails = MLabel(translate("MusicTable", "Read From:"))
        lblTargetDetails = MLabel(translate("MusicTable", "Write To:"))
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
        self.cbTagSourceType.setToolTip(translate("MusicTable",
                                                        "You can select the ID3 tag source you want to read.<br><font color=blue>ID3 V2 is recommended.</font>"))
        self.cbTagTargetType.setToolTip(translate("MusicTable",
                                                         "You can select the ID3 tag target you want to write.<br><font color=blue>ID3 V2 is recommended.</font>"))
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

    def writeContents(self):
        self.changedValueNumber = 0
        oldAndNewPathValues = []
        changingTags = []
        isNewDirectoriesSame = True
        isMovedToNewDirectory = False
        currentDirectoryPath = ""
        newDirectoryPath = ""
        if uni.isActiveAmarok and uni.getBoolValue("isMusicTableValuesChangeInAmarokDB"):
            import Amarok

            if Amarok.checkAmarok(True, False) is False:
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
                                (uni.isActiveAmarok and uni.getBoolValue("isMusicTableValuesChangeInAmarokDB"))
                            )
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
                                                     self.values[rowNo]["albumArtist"], True,
                                                     isCheckLike):
                                value = str(self.item(rowNo, 5).text())
                                tagger.setAlbumArtist(value)
                                changingTag["albumArtist"] = value
                                Records.add(str(translate("MusicTable", "Album Artist")),
                                            str(self.values[rowNo]["albumArtist"]), value)
                                self.changedValueNumber += 1
                            if self.isChangeableItem(rowNo, 6,
                                                     self.values[rowNo]["trackNum"],
                                                     True, isCheckLike):
                                value = str(self.item(rowNo, 6).text())
                                tagger.setTrackNum(value)
                                changingTag["trackNum"] = value
                                Records.add(str(translate("MusicTable", "Track No")),
                                            str(self.values[rowNo]["trackNum"]), value)
                                self.changedValueNumber += 1
                            if self.isChangeableItem(rowNo, 7,
                                                     self.values[rowNo]["year"], True,
                                                     isCheckLike):
                                value = str(self.item(rowNo, 7).text())
                                tagger.setDate(value)
                                changingTag["year"] = value
                                Records.add(str(translate("MusicTable", "Year")),
                                            str(self.values[rowNo]["year"]), value)
                                self.changedValueNumber += 1
                            if self.isChangeableItem(rowNo, 8,
                                                     self.values[rowNo]["genre"], True,
                                                     isCheckLike):
                                value = str(self.item(rowNo, 8).text())
                                tagger.setGenre(value)
                                changingTag["genre"] = value
                                Records.add(str(translate("MusicTable", "Genre")),
                                            str(self.values[rowNo]["genre"]), value)
                                self.changedValueNumber += 1
                            if self.isChangeableItem(rowNo, 9,
                                                     self.values[rowNo]["firstComment"],
                                                     True, isCheckLike):
                                value = str(self.item(rowNo, 9).text())
                                tagger.setFirstComment(value)
                                changingTag["firstComment"] = value
                                Records.add(str(translate("MusicTable", "Comment")),
                                            str(self.values[rowNo]["firstComment"]), value)
                                self.changedValueNumber += 1
                            if self.isChangeableItem(rowNo, 10, self.values[rowNo]["firstLyrics"], True, isCheckLike):
                                value = str(self.item(rowNo, 10).text())
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
        if uni.isActiveAmarok and uni.getBoolValue("isMusicTableValuesChangeInAmarokDB"):
            import Amarok
            from Amarok import Operations

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
        self.checkFileExtensions(1, "baseName")
        return self.writeContents()

    def refreshTable(self, _path):
        self.values = []
        self.setColumnWidth(6, 70)
        self.setColumnWidth(7, 40)
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
                        if tagger.isAvailableFile() is False:
                            isCanNoncompatible = True
                        content = {}
                        content["path"] = fu.joinPath(_path, musicName)
                        content["baseNameOfDirectory"] = baseNameOfDirectory
                        content["baseName"] = musicName
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
                        newBaseNameOfDirectory = Organizer.emend(self.values[rowNo]["baseNameOfDirectory"], "directory")
                        self.createItem(rowNo, 0, "baseNameOfDirectory", newBaseNameOfDirectory,
                                        self.values[rowNo]["baseNameOfDirectory"])

                        newBaseName = Organizer.emend(self.values[rowNo]["baseName"], "file")
                        self.createItem(rowNo, 1, "baseName", newBaseName, self.values[rowNo]["baseName"])

                        newArtist = Organizer.emend(self.values[rowNo]["artist"])
                        self.createItem(rowNo, 2, "artist", newArtist, self.values[rowNo]["artist"])

                        newTitle = Organizer.emend(self.values[rowNo]["title"])
                        self.createItem(rowNo, 3, "title", newTitle, self.values[rowNo]["title"])

                        newAlbum = Organizer.emend(self.values[rowNo]["album"])
                        self.createItem(rowNo, 4, "album", newAlbum, self.values[rowNo]["album"])

                        newAlbumArtist = Organizer.emend(self.values[rowNo]["albumArtist"])
                        self.createItem(rowNo, 5, "albumArtist", newAlbumArtist, self.values[rowNo]["albumArtist"])

                        newTrackNum = str(self.values[rowNo]["trackNum"])
                        self.createItem(rowNo, 6, "trackNum", newTrackNum, self.values[rowNo]["trackNum"])

                        newYear = Organizer.emend(self.values[rowNo]["year"])
                        self.createItem(rowNo, 7, "year", newYear, self.values[rowNo]["year"])

                        newGenre = Organizer.emend(self.values[rowNo]["genre"])
                        self.createItem(rowNo, 8, "genre", newGenre, self.values[rowNo]["genre"])

                        newFirstComment = Organizer.emend(self.values[rowNo]["firstComment"])
                        self.createItem(rowNo, 9, "firstComment", newFirstComment, self.values[rowNo]["firstComment"])

                        newFirstLyrics = Organizer.emend(self.values[rowNo]["firstLyrics"])
                        self.createItem(rowNo, 10, "firstLyrics", newFirstLyrics, self.values[rowNo]["firstLyrics"])
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
            self.cbTagSourceType.setCurrentIndex(self.cbTagSourceType.findText(getSelectedTaggerTypeForReadName()))
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