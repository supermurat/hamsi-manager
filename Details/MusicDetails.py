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


from FileUtils import Musics
import FileUtils as fu
from Core.MyObjects import *
from Core import Dialogs
from Core import Organizer
from Viewers import MusicPlayer
from Details import ImageDetails
from Core import Universals as uni
from Core import ReportBug
import Taggers

currentDialogs = []

class MusicDetails(MDialog):
    global currentDialogs
    def __init__(self, _filePath, _isOpenDetailsOnNewWindow=True):
        global currentDialogs
        MDialog.__init__(self, MApplication.activeWindow())
        self.currenctImageDialogs = []
        _filePath = fu.checkSource(_filePath, "file")
        if _filePath is not None:
            if _isOpenDetailsOnNewWindow is False:
                isHasOpenedDialog = False
                for dialog in currentDialogs:
                    if dialog.isVisible():
                        isHasOpenedDialog = True
                        dialog.closeCurrenctImageDialogs()
                        dialog.changeFile(_filePath)
                        dialog.activateWindow()
                        dialog.raise_()
                        dialog.player.play(_filePath, dialog.isPlayNow.isChecked())
                        break
                if isHasOpenedDialog is False:
                    _isOpenDetailsOnNewWindow = True
            if _isOpenDetailsOnNewWindow:
                currentDialogs.append(self)
                if isActivePyKDE4:
                    self.setButtons(MDialog.NoDefault)
                self.isActiveAddImage = False
                self.infoLabels = {}
                self.infoValues = {}
                self.musicValues = {}
                self.pbtnClose = MPushButton(translate("MusicDetails", "Close"))
                self.pbtnSave = MPushButton(translate("MusicDetails", "Save Changes"))
                self.pbtnSave.setIcon(MIcon("Images:save.png"))
                MObject.connect(self.pbtnClose, SIGNAL("clicked()"), self.close)
                MObject.connect(self.pbtnSave, SIGNAL("clicked()"), self.save)
                self.labels = [translate("MusicDetails", "Directory: "),
                               translate("MusicDetails", "File Name: "),
                               translate("MusicDetails", "Artist: "),
                               translate("MusicDetails", "Title: "),
                               translate("MusicDetails", "Album: "),
                               translate("MusicDetails", "Album Artist: "),
                               translate("MusicDetails", "Track: "),
                               translate("MusicDetails", "Year: "),
                               translate("MusicDetails", "Genre: ")]
                self.pnlMain = MWidget()
                self.vblMain = MVBoxLayout(self.pnlMain)
                self.pnlClearable = None
                self.changeFile(_filePath)

                buttonHBOXs = MHBoxLayout()
                buttonHBOXs.addWidget(self.pbtnSave)
                buttonHBOXs.addWidget(self.pbtnClose)
                self.vblMain.addLayout(buttonHBOXs)
                if isActivePyKDE4:
                    self.setMainWidget(self.pnlMain)
                else:
                    self.setLayout(self.vblMain)
                self.show()
                self.player.play(_filePath, self.isPlayNow.isChecked())
        else:
            Dialogs.showError(translate("MusicDetails", "File Does Not Exist"),
                              str(translate("MusicDetails",
                                            "\"%s\" does not exist.<br>Table will be refreshed automatically!<br>Please retry.")
                              ) % Organizer.getLink(str(_filePath)))
            if hasattr(getMainWindow(),
                       "FileManager") and getMainWindow().FileManager is not None: getMainWindow().FileManager.makeRefresh()

    def changeFile(self, _filePath, _readFrom="tag"):
        self.musicFile = _filePath
        self.musicValues = None
        self.isPlayNow = MToolButton()
        self.isPlayNow.setToolTip(translate("MusicDetails", "Play Suddenly Music When Open"))
        self.isPlayNow.setText(translate("MusicDetails", "Play When Open"))
        self.isPlayNow.setCheckable(True)
        self.isPlayNow.setChecked(uni.getBoolValue("isPlayNow"))
        self.isGetFromAmarok = MToolButton()
        self.isGetFromAmarok.setToolTip(translate("MusicDetails", "Get Values From Amarok"))
        self.isGetFromAmarok.setText(translate("MusicDetails", "Get From Amarok"))
        self.isGetFromAmarok.setCheckable(True)
        if _readFrom.count("Amarok") > 0:
            import Amarok

            uni.startThreadAction()
            Dialogs.showState(translate("MusicDetails", "Getting Values From Amarok"), 0, 1)
            if Amarok.checkAmarok():
                isContinueThreadAction = uni.isContinueThreadAction()
                if isContinueThreadAction:
                    from Amarok import Operations

                    musicFileRows = Operations.getAllMusicFileValuesWithNames("filename:\"" + _filePath + "\"")
                    Dialogs.showState(translate("MusicDetails", "Values Are Being Processed"), 1, 1)
                    if len(musicFileRows)>0:
                        musicFileRow = musicFileRows[0]
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
                        content["images"] = []
                        if _readFrom == "Amarok (Smart)":
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
                                content["images"] = tagger.getImages()
                        self.isGetFromAmarok.setChecked(True)
                        self.musicValues = content
                    else:
                        Dialogs.show(translate("MusicDetails", "Not Exist In Amarok"),
                                     translate("MusicDetails", "This music file not exist in Amarok DB."))
            uni.finishThreadAction()
        if self.musicValues is None:
            self.isGetFromAmarok.setChecked(False)
            self.musicValues = Musics.readMusicFile(self.musicFile)
        self.setWindowTitle(str(fu.getBaseName(self.musicFile)))
        if self.pnlClearable is not None:
            clearAllChildren(self.pnlClearable, True)
        self.pnlClearable = MWidget()
        self.vblMain.insertWidget(0, self.pnlClearable, 20)
        vblClearable = MVBoxLayout(self.pnlClearable)
        self.player = MusicPlayer.MusicPlayer(self, "dialog", _filePath)
        self.infoLabels["baseNameOfDirectory"] = MLabel(self.labels[0])
        self.infoLabels["baseName"] = MLabel(self.labels[1])
        self.infoLabels["artist"] = MLabel(self.labels[2])
        self.infoLabels["title"] = MLabel(self.labels[3])
        self.infoLabels["album"] = MLabel(self.labels[4])
        self.infoLabels["albumArtist"] = MLabel(self.labels[5])
        self.infoLabels["trackNum"] = MLabel(self.labels[6])
        self.infoLabels["year"] = MLabel(self.labels[7])
        self.infoLabels["genre"] = MLabel(self.labels[8])
        self.infoValues["baseNameOfDirectory"] = MLineEdit(
            str(Organizer.emend(self.musicValues["baseNameOfDirectory"], "directory", False)))
        self.infoValues["baseName"] = MLineEdit(str(Organizer.emend(self.musicValues["baseName"], "file")))
        self.infoValues["artist"] = MLineEdit(str(Organizer.emend(self.musicValues["artist"])))
        self.infoValues["title"] = MLineEdit(str(Organizer.emend(self.musicValues["title"])))
        self.infoValues["album"] = MLineEdit(str(Organizer.emend(self.musicValues["album"])))
        self.infoValues["albumArtist"] = MLineEdit(str(Organizer.emend(self.musicValues["albumArtist"])))
        self.infoValues["trackNum"] = MLineEdit(str(Organizer.emend(self.musicValues["trackNum"])))
        self.infoValues["year"] = MLineEdit(str(Organizer.emend(self.musicValues["year"])))
        self.infoValues["genre"] = MLineEdit(str(Organizer.emend(self.musicValues["genre"])))
        self.infoValues["firstComment"] = MPlainTextEdit(str(Organizer.emend(self.musicValues["firstComment"])))
        self.infoValues["firstLyrics"] = MPlainTextEdit(str(Organizer.emend(self.musicValues["firstLyrics"])))
        self.infoValues["firstComment"].setLineWrapMode(MPlainTextEdit.NoWrap)
        self.infoValues["firstLyrics"].setLineWrapMode(MPlainTextEdit.NoWrap)

        if Taggers.getTagger().isSupportImages:
            self.isOpenImageDetailsOnNewWindow = MCheckBox(translate("MusicDetails", "Show Images In New Window"))
            self.pbtnAddImage = MPushButton(translate("MusicDetails", "Append"))
            self.pbtnDeleteImage = MPushButton(translate("MusicDetails", "Delete"))
            self.pbtnSaveAsImage = MPushButton(translate("MusicDetails", "Save As ..."))
            self.pbtnCancelAddImage = MPushButton(translate("MusicDetails", "Cancel"))
            self.pbtnSelectImage = MPushButton(translate("MusicDetails", "Choose Image"))
            MObject.connect(self.pbtnAddImage, SIGNAL("clicked()"), self.addImage)
            MObject.connect(self.pbtnDeleteImage, SIGNAL("clicked()"), self.deleteImage)
            MObject.connect(self.pbtnSaveAsImage, SIGNAL("clicked()"), self.saveAsImage)
            MObject.connect(self.pbtnCancelAddImage, SIGNAL("clicked()"), self.cancelAddImage)
            MObject.connect(self.pbtnSelectImage, SIGNAL("clicked()"), self.selectImage)
            self.leImagePath = MLineEdit("")
            self.lblImagePath = MLabel(translate("MusicDetails", "Image Path: "))
            self.cbImageType = MComboBox()
            self.cbImageType.addItems(Taggers.getTagger().getImageTypes())
            self.lblImageType = MLabel(translate("MusicDetails", "Image Type: "))

            self.lstwImages = MListWidget()
            self.lstwImages.setGridSize(MSize(350, 100))
            self.lstwImages.setIconSize(MSize(98, 98))
            MObject.connect(self.lstwImages, SIGNAL("doubleClicked(QModelIndex)"), self.openImageDetails)
            MObject.connect(self.isGetFromAmarok, SIGNAL("toggled(bool)"), self.isGetFromAmarokTiggered)
            self.lstwImages.clear()
            for image in self.musicValues["images"]:
                if len(image) == 5:
                    pixmImage = MPixmap()
                    pixmImage.loadFromData(image[3])
                    icnImage = QIcon(pixmImage)
                    icnImage.actualSize(MSize(98, 98))
                    item = MListWidgetItem(icnImage, image[1] + "\n(" + image[2] + ")")
                    item.setSizeHint(MSize(1, 100))
                    self.lstwImages.addItem(item)
        HBOXs = []
        HBOXs.append(MHBoxLayout())
        HBOXs[-1].addWidget(self.infoLabels["baseNameOfDirectory"])
        HBOXs[-1].addWidget(self.infoValues["baseNameOfDirectory"])
        HBOXs.append(MHBoxLayout())
        HBOXs[-1].addWidget(self.infoLabels["baseName"])
        HBOXs[-1].addWidget(self.infoValues["baseName"])
        HBOXs.append(MHBoxLayout())
        HBOXs[-1].addWidget(self.infoLabels["artist"])
        HBOXs[-1].addWidget(self.infoValues["artist"])
        HBOXs.append(MHBoxLayout())
        HBOXs[-1].addWidget(self.infoLabels["title"])
        HBOXs[-1].addWidget(self.infoValues["title"])
        HBOXs.append(MHBoxLayout())
        HBOXs[-1].addWidget(self.infoLabels["album"])
        HBOXs[-1].addWidget(self.infoValues["album"])
        HBOXs.append(MHBoxLayout())
        HBOXs[-1].addWidget(self.infoLabels["albumArtist"])
        HBOXs[-1].addWidget(self.infoValues["albumArtist"])
        HBOXs.append(MHBoxLayout())
        HBOXs[-1].addWidget(self.infoLabels["trackNum"])
        HBOXs[-1].addWidget(self.infoValues["trackNum"])
        HBOXs[-1].addWidget(self.infoLabels["year"])
        HBOXs[-1].addWidget(self.infoValues["year"])
        HBOXs[-1].addWidget(self.infoLabels["genre"])
        HBOXs[-1].addWidget(self.infoValues["genre"])
        vblInfos = MVBoxLayout()
        for hbox in HBOXs:
            vblInfos.addLayout(hbox)
        if Taggers.getTagger().isSupportImages:
            imageBoxs = []
            imageBoxs.append(MHBoxLayout())
            imageBoxs[0].addWidget(self.leImagePath)
            imageBoxs[0].addWidget(self.pbtnSelectImage)
            imageBoxs.append(MHBoxLayout())
            imageBoxs[1].addWidget(self.lblImageType)
            imageBoxs[1].addWidget(self.cbImageType)
            imageBoxs.append(MHBoxLayout())
            imageBoxs[2].addWidget(self.pbtnAddImage)
            imageBoxs[2].addWidget(self.pbtnDeleteImage)
            imageBoxs[2].addWidget(self.pbtnSaveAsImage)
            imageBoxs[2].addWidget(self.pbtnCancelAddImage)
            vblImages = MVBoxLayout()
            vblImages.addWidget(self.lstwImages)
            vblImages.addWidget(self.isOpenImageDetailsOnNewWindow)
            vblImages.addWidget(self.lblImagePath)
            vblImages.addLayout(imageBoxs[0])
            vblImages.addLayout(imageBoxs[1])
            vblImages.addLayout(imageBoxs[2])
        vblComments = MVBoxLayout()
        vblComments.addWidget(self.infoValues["firstComment"])
        vblLyrics = MVBoxLayout()
        vblLyrics.addWidget(self.infoValues["firstLyrics"])
        self.tabwTabs = MTabWidget(self.pnlMain)
        self.pnlComments = MWidget(self.tabwTabs)
        self.pnlComments.setLayout(vblComments)
        self.tabwTabs.addTab(self.pnlComments, translate("MusicDetails", "Comments"))
        self.pnlLyrics = MWidget(self.tabwTabs)
        self.pnlLyrics.setLayout(vblLyrics)
        self.tabwTabs.addTab(self.pnlLyrics, translate("MusicDetails", "Lyrics"))
        if Taggers.getTagger().isSupportImages:
            self.pnlImages = MWidget(self.tabwTabs)
            self.pnlImages.setLayout(vblImages)
            self.tabwTabs.addTab(self.pnlImages, translate("MusicDetails", "Images"))
            self.pbtnSelectImage.hide()
            self.leImagePath.hide()
            self.lblImagePath.hide()
            self.lblImageType.hide()
            self.cbImageType.hide()
            self.pbtnCancelAddImage.hide()
        hblPlayer = MHBoxLayout()
        vblExtraButtons = MVBoxLayout()
        hblPlayer.addWidget(self.player)
        vblExtraButtons.addWidget(self.isPlayNow)
        vblExtraButtons.addWidget(self.isGetFromAmarok)
        hblPlayer.addLayout(vblExtraButtons)
        vblClearable.addLayout(hblPlayer)
        vblClearable.addLayout(vblInfos)
        vblClearable.addWidget(self.tabwTabs)

    def closeEvent(self, _event):
        try:
            self.player.stop()
            uni.setMySetting("isPlayNow", self.isPlayNow.isChecked())
        except:
            pass
        self.closeCurrenctImageDialogs()

    def closeCurrenctImageDialogs(self):
        for dialog in self.currenctImageDialogs:
            try:
                if dialog.isVisible():
                    dialog.close()
                    self.currenctImageDialogs.remove(dialog)
            except:
                continue

    def save(self):
        try:
            from Core import Records

            Records.setTitle(translate("MusicDetails", "Music File"))
            newMusicValues = {}
            newMusicValues["baseNameOfDirectory"] = str(self.infoValues["baseNameOfDirectory"].text())
            newMusicValues["baseName"] = str(self.infoValues["baseName"].text())
            newMusicValues["artist"] = str(self.infoValues["artist"].text())
            newMusicValues["title"] = str(self.infoValues["title"].text())
            newMusicValues["album"] = str(self.infoValues["album"].text())
            newMusicValues["albumArtist"] = str(self.infoValues["albumArtist"].text())
            newMusicValues["trackNum"] = str(self.infoValues["trackNum"].text())
            newMusicValues["year"] = str(self.infoValues["year"].text())
            newMusicValues["genre"] = str(self.infoValues["genre"].text())
            newMusicValues["firstComment"] = str(self.infoValues["firstComment"].toPlainText())
            newMusicValues["firstLyrics"] = str(self.infoValues["firstLyrics"].toPlainText())
            newPath = Musics.writeMusicFile(self.musicValues, newMusicValues)
            if newPath != self.musicValues["path"]:
                self.changeFile(newPath)
            if hasattr(getMainWindow(),
                       "FileManager") and getMainWindow().FileManager is not None: getMainWindow().FileManager.makeRefresh()
            Records.saveAllRecords()
        except:
            ReportBug.ReportBug()

    def openImageDetails(self, _index):
        try:
            self.currenctImageDialogs.append(ImageDetails.ImageDetails(self.musicValues["images"][_index.row()][3],
                                                                       "data",
                                                                       self.isOpenImageDetailsOnNewWindow.isChecked()))
        except:
            ReportBug.ReportBug()

    def addImage(self):
        try:
            if self.isActiveAddImage is False:
                self.isActiveAddImage = True
                self.pbtnAddImage.setText(translate("MusicDetails", "OK"))
                self.pbtnSelectImage.show()
                self.leImagePath.show()
                self.lblImagePath.show()
                self.lblImageType.show()
                self.cbImageType.show()
                self.pbtnCancelAddImage.show()
                self.pbtnDeleteImage.hide()
                self.pbtnSaveAsImage.hide()
            else:
                if fu.isFile(self.leImagePath.text()):
                    imageType = Taggers.getTagger().getImageTypesNo()[self.cbImageType.currentIndex()]
                    description = str(imageType)
                    Musics.writeMusicFile(self.musicValues, None, True, imageType, str(self.leImagePath.text()),
                                          description)
                    self.changeFile(self.musicFile)
                    self.cancelAddImage()
                else:
                    Dialogs.showError(translate("MusicDetails", "Image Does Not Exist"),
                                      str(translate("MusicDetails", "\"%s\" does not exist.")
                                      ) % Organizer.getLink(str(self.leImagePath.text())))
        except:
            ReportBug.ReportBug()

    def deleteImage(self):
        try:
            if self.lstwImages.currentRow() != -1:
                description = self.musicValues["images"][self.lstwImages.currentRow()][4]
                Musics.writeMusicFile(self.musicValues, None, True,
                                      self.musicValues["images"][self.lstwImages.currentRow()][0], False, description)
                self.changeFile(self.musicFile)
        except:
            ReportBug.ReportBug()

    def saveAsImage(self):
        try:
            if self.lstwImages.currentRow() != -1:
                imagePath = Dialogs.getSaveFileName(translate("MusicDetails", "Save As"),
                                                    fu.getDirName(self.musicValues["path"]),
                                                    str(translate("MusicDetails", "Images (*.%s)")) % (str(
                                                        self.musicValues["images"][self.lstwImages.currentRow()][
                                                            2]).split("/")[1]), 0)
                if imagePath is not None:
                    sourceFile = fu.joinPath(fu.getTempDir(), "HamsiManager-image-file." +
                                             self.musicValues["images"][self.lstwImages.currentRow()][2].split("/")[1])
                    fu.writeToBinaryFile(sourceFile, self.musicValues["images"][self.lstwImages.currentRow()][3])
                    fu.moveOrChange(sourceFile, imagePath)
        except:
            ReportBug.ReportBug()

    def cancelAddImage(self):
        try:
            self.isActiveAddImage = False
            self.pbtnAddImage.setText(translate("MusicDetails", "Append"))
            self.pbtnSelectImage.hide()
            self.leImagePath.hide()
            self.lblImagePath.hide()
            self.lblImageType.hide()
            self.cbImageType.hide()
            self.pbtnCancelAddImage.hide()
            self.pbtnDeleteImage.show()
            self.pbtnSaveAsImage.show()
        except:
            ReportBug.ReportBug()

    def selectImage(self):
        try:
            imagePath = Dialogs.getOpenFileName(translate("MusicDetails", "Choose Image"),
                                                fu.getDirName(self.musicValues["path"]), str(
                    translate("MusicDetails", "Images")) + " " + uni.imageExtStringOnlyPNGAndJPG, 0)
            if imagePath is not None:
                self.leImagePath.setText(imagePath)
        except:
            ReportBug.ReportBug()

    def isGetFromAmarokTiggered(self, _action):
        readFrom = "tag"
        if self.isGetFromAmarok.isChecked():
            readFrom = "Amarok (Smart)"
        self.changeFile(self.musicFile, readFrom)
