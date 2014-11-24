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


class SubFolderMusicTable(CoreTable):
    def __init__(self, *args, **kwargs):
        CoreTable.__init__(self, *args, **kwargs)
        self.keyName = "music"
        self.hiddenTableColumnsSettingKey = "hiddenSubFolderMusicTableColumns"
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
        lblDetails = translate("SubFolderTable",
                               "You can select sub directory deep.<br><font color=blue>You can select \"-1\" for all sub directories.</font>")
        lblSubDirectoryDeep = MLabel(str(translate("SubFolderTable", "Deep") + " : "))
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
                                (uni.isActiveAmarok and
                                 uni.getBoolValue("isSubFolderMusicTableValuesChangeInAmarokDB")))
                            if self.isChangeableItem(rowNo, "artist", self.values[rowNo]["artist"], True,
                                                     isCheckLike):
                                value = str(self.item(rowNo, 2).text())
                                tagger.setArtist(value)
                                changingTag["artist"] = value
                                Records.add(str(translate("MusicTable", "Artist")),
                                            str(self.values[rowNo]["artist"]), value)
                                self.changedValueNumber += 1
                            if self.isChangeableItem(rowNo, "title", self.values[rowNo]["title"], True,
                                                     isCheckLike):
                                value = str(self.item(rowNo, 3).text())
                                tagger.setTitle(value)
                                changingTag["title"] = value
                                Records.add(str(translate("MusicTable", "Title")),
                                            str(self.values[rowNo]["title"]), value)
                                self.changedValueNumber += 1
                            if self.isChangeableItem(rowNo, "album", self.values[rowNo]["album"], True,
                                                     isCheckLike):
                                value = str(self.item(rowNo, 4).text())
                                tagger.setAlbum(value)
                                changingTag["album"] = value
                                Records.add(str(translate("MusicTable", "Album")),
                                            str(self.values[rowNo]["album"]), value)
                                self.changedValueNumber += 1
                            if self.isChangeableItem(rowNo, "albumArtist", self.values[rowNo]["albumArtist"], True,
                                                     isCheckLike):
                                value = str(self.item(rowNo, 5).text())
                                tagger.setAlbumArtist(value)
                                changingTag["albumArtist"] = value
                                Records.add(str(translate("MusicTable", "Album Artist")),
                                            str(self.values[rowNo]["albumArtist"]), value)
                                self.changedValueNumber += 1
                            if self.isChangeableItem(rowNo, "trackNum", self.values[rowNo]["trackNum"],
                                                     True, isCheckLike):
                                value = str(self.item(rowNo, 6).text())
                                tagger.setTrackNum(value)
                                changingTag["trackNum"] = value
                                Records.add(str(translate("MusicTable", "Track No")),
                                            str(self.values[rowNo]["trackNum"]), value)
                                self.changedValueNumber += 1
                            if self.isChangeableItem(rowNo, "year", self.values[rowNo]["year"], True, isCheckLike):
                                value = str(self.item(rowNo, 7).text())
                                tagger.setDate(value)
                                changingTag["year"] = value
                                Records.add(str(translate("MusicTable", "Year")),
                                            str(self.values[rowNo]["year"]), value)
                                self.changedValueNumber += 1
                            if self.isChangeableItem(rowNo, "genre", self.values[rowNo]["genre"], True, isCheckLike):
                                value = str(self.item(rowNo, 8).text())
                                tagger.setGenre(value)
                                changingTag["genre"] = value
                                Records.add(str(translate("MusicTable", "Genre")),
                                            str(self.values[rowNo]["genre"]), value)
                                self.changedValueNumber += 1
                            if self.isChangeableItem(rowNo, "firstComment", self.values[rowNo]["firstComment"],
                                                     True, isCheckLike):
                                value = str(self.item(rowNo, 9).text())
                                tagger.setFirstComment(value)
                                changingTag["firstComment"] = value
                                Records.add(str(translate("MusicTable", "Comment")),
                                            str(self.values[rowNo]["firstComment"]), value)
                                self.changedValueNumber += 1
                            if self.isChangeableItem(rowNo, "firstLyrics", self.values[rowNo]["firstLyrics"], True, isCheckLike):
                                value = str(self.item(rowNo, 10).text())
                                tagger.setFirstLyrics(value)
                                changingTag["firstLyrics"] = value
                                Records.add(str(translate("MusicTable", "Lyrics")),
                                            str(self.values[rowNo]["firstLyrics"]), value)
                                self.changedValueNumber += 1
                            if len(changingTag) > 1:
                                changingTags.append(changingTag)
                            tagger.update()
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
            if isContinueThreadAction is False:
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
                        if tagger.isAvailableFile() is False:
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

                        newBaseNameOfDirectory = Organizer.emend(self.values[rowNo]["baseNameOfDirectory"], "directory")
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
                        self.createItem(rowNo, "albumArtist", newAlbumArtist, self.values[rowNo]["albumArtist"])

                        newTrackNum = str(self.values[rowNo]["trackNum"])
                        self.createItem(rowNo, "trackNum", newTrackNum, self.values[rowNo]["trackNum"])

                        newYear = Organizer.emend(self.values[rowNo]["year"])
                        self.createItem(rowNo, "year", newYear, self.values[rowNo]["year"])

                        newGenre = Organizer.emend(self.values[rowNo]["genre"])
                        self.createItem(rowNo, "genre", newGenre, self.values[rowNo]["genre"])

                        newFirstComment = Organizer.emend(self.values[rowNo]["firstComment"])
                        self.createItem(rowNo, "firstComment", newFirstComment, self.values[rowNo]["firstComment"])

                        newFirstLyrics = Organizer.emend(self.values[rowNo]["firstLyrics"])
                        self.createItem(rowNo, "firstLyrics", newFirstLyrics, self.values[rowNo]["firstLyrics"])
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
                coloumKey = self.getColumnKeyFromNo(itemNo)
                if self.isChangeableItem(rowNo, coloumKey):
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


