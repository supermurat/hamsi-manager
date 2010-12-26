# -*- coding: utf-8 -*-
## This file is part of HamsiManager.
## 
## Copyright (c) 2010 Murat Demir <mopened@gmail.com>      
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


import Variables
from InputOutputs import Musics
import InputOutputs
import os,sys
from MyObjects import *
import Dialogs
import Organizer
from Viewers import MusicPlayer
from ImageDetails import ImageDetails, closeAllImageDialogs
import Universals
import ReportBug
import Taggers
from Taggers import EyeD3Tagger

class MusicDetails(MDialog):
    global musicDialogs, closeAllMusicDialogs
    musicDialogs =[]
    def __init__(self, _filePath, _isOpenDetailsOnNewWindow=True, _isPlayNow=False):
        global musicDialogs
        if InputOutputs.IA.isFile(_filePath):
            if _isOpenDetailsOnNewWindow==False:
                isHasOpenedDialog=False
                for dialog in musicDialogs:
                    if dialog.isVisible()==True:
                        isHasOpenedDialog=True
                        self = dialog
                        self.changeFile(_filePath)
                        self.checkMusicTagType()
                        self.activateWindow()
                        self.raise_()
                        self.player.play(_filePath, _isPlayNow)
                        break
                if isHasOpenedDialog==False:
                    _isOpenDetailsOnNewWindow=True
            if _isOpenDetailsOnNewWindow==True:
                musicDialogs.append(self)
                MDialog.__init__(self, MApplication.activeWindow())
                if Universals.isActivePyKDE4==True:
                    self.setButtons(MDialog.None)
                self.isActiveAddImage = False
                self.infoLabels = {}
                self.infoValues = {}
                self.musicValues = {}
                self.isOpenImageDetailsOnNewWindow = MCheckBox(translate("MusicDetails", "Show Images In New Window"))
                self.pbtnClose = MPushButton(translate("MusicDetails", "Close"))
                self.pbtnSave = MPushButton(translate("MusicDetails", "Save Changes"))
                self.pbtnSave.setIcon(MIcon("Images:save.png"))
                self.pbtnAddImage = MPushButton(translate("MusicDetails", "Append"))
                self.pbtnDeleteImage = MPushButton(translate("MusicDetails", "Delete"))
                self.pbtnSaveAsImage = MPushButton(translate("MusicDetails", "Save As ..."))
                self.pbtnCancelAddImage = MPushButton(translate("MusicDetails", "Cancel"))
                self.pbtnSelectImage = MPushButton(translate("MusicDetails", "Choose Image"))
                MObject.connect(self.pbtnClose, SIGNAL("clicked()"), self.close)
                MObject.connect(self.pbtnSave, SIGNAL("clicked()"), self.save)
                MObject.connect(self.pbtnAddImage, SIGNAL("clicked()"), self.addImage)
                MObject.connect(self.pbtnDeleteImage, SIGNAL("clicked()"), self.deleteImage)
                MObject.connect(self.pbtnSaveAsImage, SIGNAL("clicked()"), self.saveAsImage)
                MObject.connect(self.pbtnCancelAddImage, SIGNAL("clicked()"), self.cancelAddImage)
                MObject.connect(self.pbtnSelectImage, SIGNAL("clicked()"), self.selectImage)
                self.leImagePath = MLineEdit("")
                self.lblImagePath = MLabel(translate("MusicDetails", "Image Path: "))
                self.cbImageType = MComboBox()
                self.cbImageType.addItems(EyeD3Tagger.getImageTypes())
                self.lblImageType = MLabel(translate("MusicDetails", "Image Type: "))
                self.labels = [translate("MusicDetails", "Directory: "),
                                translate("MusicDetails", "File Name: "),
                                translate("MusicDetails", "Artist: "),
                                translate("MusicDetails", "Title: "),
                                translate("MusicDetails", "Album: "),
                                translate("MusicDetails", "Track: "),
                                translate("MusicDetails", "Year: "),
                                translate("MusicDetails", "Genre: ")]
                self.lstwImages = MListWidget()
                self.lstwImages.setGridSize(MSize(250,100))
                self.lstwImages.setIconSize(MSize(98,98))
                MObject.connect(self.lstwImages, SIGNAL("doubleClicked(QModelIndex)"),self.openImageDetails)
                self.changeFile(_filePath, True)
                self.pbtnSelectImage.hide()
                self.leImagePath.hide()
                self.lblImagePath.hide()
                self.lblImageType.hide()
                self.cbImageType.hide()
                self.pbtnCancelAddImage.hide()
                HBOXs = []
                HBOXs.append(MHBoxLayout())
                HBOXs[-1].addWidget(self.infoLabels["baseNameOfDirectory"])
                HBOXs[-1].addWidget(self.infoValues["baseNameOfDirectory"])
                HBOXs.append(MHBoxLayout())
                HBOXs[-1].addWidget(self.infoLabels["baseName"])
                HBOXs[-1].addWidget(self.infoValues["baseName"])
                HBOXs.append(MHBoxLayout())
                HBOXs[-1].addWidget(self.infoLabels["Artist"])
                HBOXs[-1].addWidget(self.infoValues["Artist"])
                HBOXs.append(MHBoxLayout())
                HBOXs[-1].addWidget(self.infoLabels["Title"])
                HBOXs[-1].addWidget(self.infoValues["Title"])
                HBOXs.append(MHBoxLayout())
                HBOXs[-1].addWidget(self.infoLabels["Album"])
                HBOXs[-1].addWidget(self.infoValues["Album"])
                HBOXs.append(MHBoxLayout())
                HBOXs[5].addWidget(self.infoLabels["TrackNum"])
                HBOXs[5].addWidget(self.infoValues["TrackNum"])
                HBOXs[5].addWidget(self.infoLabels["Year"])
                HBOXs[5].addWidget(self.infoValues["Year"])
                HBOXs[5].addWidget(self.infoLabels["Genre"])
                HBOXs[5].addWidget(self.infoValues["Genre"])
                vblInfos = MVBoxLayout()
                for hbox in HBOXs:
                    vblInfos.addLayout(hbox)
                imageBoxs=[]
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
                vblComments.addWidget(self.infoValues["FirstComment"])
                vblLyrics = MVBoxLayout()
                vblLyrics.addWidget(self.infoValues["FirstLyrics"])
                self.pnlMain = MWidget()
                self.tabwTabs = MTabWidget(self.pnlMain)
                self.pnlComments = MWidget(self.tabwTabs)
                self.pnlLyrics = MWidget(self.tabwTabs)
                self.pnlImages = MWidget(self.tabwTabs)
                self.pnlImages.setLayout(vblImages)
                self.pnlComments.setLayout(vblComments)
                self.pnlLyrics.setLayout(vblLyrics)
                self.tabwTabs.addTab(self.pnlComments, translate("MusicDetails", "Comments"))
                self.tabwTabs.addTab(self.pnlLyrics, translate("MusicDetails", "Lyrics"))
                self.tabwTabs.addTab(self.pnlImages, translate("MusicDetails", "Images"))
                vblMain = MVBoxLayout(self.pnlMain)
                buttonHBOXs=MHBoxLayout()
                buttonHBOXs.addWidget(self.pbtnSave)
                buttonHBOXs.addWidget(self.pbtnClose)
                vblMain.addWidget(self.player)
                vblMain.addLayout(vblInfos)
                vblMain.addWidget(self.tabwTabs)
                vblMain.addLayout(buttonHBOXs)
                if Universals.isActivePyKDE4==True:
                    self.setMainWidget(self.pnlMain)
                else:
                    self.setLayout(vblMain)
                self.checkMusicTagType()
                self.show()
                self.player.play(_filePath, _isPlayNow)
        else:
            Dialogs.showError(translate("MusicDetails", "File Does Not Exist"), 
                    str(translate("MusicDetails", "\"%s\" does not exist.<br>Table will be refreshed automatically!<br>Please retry.")
                        ) % Organizer.getLink(Organizer.showWithIncorrectChars(_filePath)))
            from Universals import MainWindow
            MainWindow.FileManager.makeRefresh()
    
    def checkMusicTagType(self):
        if Taggers.getSelectedTaggerTypeName()=="ID3 V2":
            self.tabwTabs.setTabEnabled(1, True)
            self.tabwTabs.setTabEnabled(2, True)
        else:
            self.tabwTabs.setTabEnabled(1, False)
            self.tabwTabs.setTabEnabled(2, False)
    
    def changeFile(self, _filePath, _isNew=False):
        self.musicFile = _filePath
        self.musicValues = Musics.readMusicFile(self.musicFile)
        self.setWindowTitle(Organizer.showWithIncorrectChars(InputOutputs.getBaseName(self.musicFile)).decode("utf-8"))  
        self.player = MusicPlayer.MusicPlayer(self, "dialog", _filePath)     
        self.infoLabels["baseNameOfDirectory"] = MLabel(self.labels[0]) 
        self.infoLabels["baseName"] = MLabel(self.labels[1]) 
        self.infoLabels["Artist"] = MLabel(self.labels[2]) 
        self.infoLabels["Title"] = MLabel(self.labels[3]) 
        self.infoLabels["Album"] = MLabel(self.labels[4]) 
        self.infoLabels["TrackNum"] = MLabel(self.labels[5]) 
        self.infoLabels["Year"] = MLabel(self.labels[6]) 
        self.infoLabels["Genre"] = MLabel(self.labels[7]) 
        self.infoValues["baseNameOfDirectory"] = MLineEdit(Organizer.emend(self.musicValues["baseNameOfDirectory"], "directory", False).decode("utf-8"))
        self.infoValues["baseName"] = MLineEdit(Organizer.emend(self.musicValues["baseName"], "file").decode("utf-8"))
        self.infoValues["Artist"] = MLineEdit(Organizer.emend(self.musicValues["Artist"]).decode("utf-8"))
        self.infoValues["Title"] = MLineEdit(Organizer.emend(self.musicValues["Title"]).decode("utf-8"))
        self.infoValues["Album"] = MLineEdit(Organizer.emend(self.musicValues["Album"]).decode("utf-8"))
        self.infoValues["TrackNum"] = MLineEdit(Organizer.emend(self.musicValues["TrackNum"]).decode("utf-8"))
        self.infoValues["Year"] = MLineEdit(Organizer.emend(self.musicValues["Year"]).decode("utf-8"))
        self.infoValues["Genre"] = MLineEdit(Organizer.emend(self.musicValues["Genre"]).decode("utf-8"))
        self.infoValues["FirstComment"] = MPlainTextEdit(Organizer.emend(self.musicValues["FirstComment"]).decode("utf-8"))
        self.infoValues["FirstLyrics"] = MPlainTextEdit(Organizer.emend(self.musicValues["FirstLyrics"]).decode("utf-8"))
        self.infoValues["FirstComment"].setLineWrapMode(MPlainTextEdit.NoWrap)
        self.infoValues["FirstLyrics"].setLineWrapMode(MPlainTextEdit.NoWrap)
        self.lstwImages.clear()
        for image in self.musicValues["Images"]:
            pixmImage = MPixmap()
            pixmImage.loadFromData(image[3])
            icnImage = QIcon(pixmImage)
            icnImage.actualSize(MSize(98,98))
            item = MListWidgetItem(icnImage,image[1]+"\n("+image[2]+")")
            item.setSizeHint(MSize(1,100))
            self.lstwImages.addItem(item)
    
    def closeEvent(self, _event):
        try:
            self.player.stop()
        except:
            pass
        closeAllImageDialogs()
    
    def closeAllMusicDialogs():
        for dialog in musicDialogs:
            try:
                if dialog.isVisible()==True:
                    dialog.player.stop()
                    dialog.close()
            except:
                continue
        
    def save(self):
        try:
            import Records
            Records.setTitle(translate("MusicDetails", "Music File"))
            closeAllImageDialogs()
            newMusicValues={}
            newMusicValues["baseNameOfDirectory"] = str(self.infoValues["baseNameOfDirectory"].text())
            newMusicValues["baseName"] = str(self.infoValues["baseName"].text())
            newMusicValues["Artist"] = str(self.infoValues["Artist"].text())
            newMusicValues["Title"] = str(self.infoValues["Title"].text())
            newMusicValues["Album"] = str(self.infoValues["Album"].text())
            newMusicValues["TrackNum"] = str(self.infoValues["TrackNum"].text())
            newMusicValues["Year"] = str(self.infoValues["Year"].text())
            newMusicValues["Genre"] = str(self.infoValues["Genre"].text())
            newMusicValues["FirstComment"] = str(self.infoValues["FirstComment"].toPlainText())
            newMusicValues["FirstLyrics"] = str(self.infoValues["FirstLyrics"].toPlainText())
            newPath = Musics.writeMusicFile(self.musicValues, newMusicValues)
            if newPath!=self.musicValues["path"]:
                self.changeFile(newPath)
            from Universals import MainWindow
            MainWindow.FileManager.makeRefresh()
            Records.saveAllRecords()
        except:
            error = ReportBug.ReportBug()
            error.show()  
        
    def openImageDetails(self, _index):
        try:
            ImageDetails(self.musicValues["Images"][_index.row()][3], "data", self.isOpenImageDetailsOnNewWindow.isChecked())
        except:
            error = ReportBug.ReportBug()
            error.show()  
        
    def addImage(self):
        if self.isActiveAddImage==False:
            self.isActiveAddImage=True
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
            if InputOutputs.IA.isFile(self.leImagePath.text())==True:
                closeAllImageDialogs()
                Musics.writeMusicFile(self.musicValues,False,True,self.cbImageType.currentIndex(),str(unicode(self.leImagePath.text()).encode("utf-8")))
                self.changeFile(self.musicFile)
                self.cancelAddImage()
            else:
                Dialogs.showError(translate("MusicDetails", "Image Does Not Exist"),
                    str(translate("MusicDetails", "\"%s\" does not exist.")
                        ) % Organizer.getLink(Organizer.showWithIncorrectChars(str(unicode(self.leImagePath.text()).encode("utf-8")))))
    
    def deleteImage(self):
        if self.lstwImages.currentRow()!=-1:
            closeAllImageDialogs()
            Musics.writeMusicFile(self.musicValues,False,True,self.musicValues["Images"][self.lstwImages.currentRow()][0],False)
            self.changeFile(self.musicFile)
    
    def saveAsImage(self):
        try:
            if self.lstwImages.currentRow()!=-1:
                imagePath = MFileDialog.getSaveFileName(self,translate("MusicDetails", "Save As"),
                                    InputOutputs.getDirName(self.musicValues["path"]), str(translate("MusicDetails", "Images (*.%s)")
                                        ) %(str(self.musicValues["Images"][self.lstwImages.currentRow()][2]).split("/")[1].decode("utf-8")))
                if imagePath!="":
                    sourceFile = os.getenv("TMP")+"/HamsiManager-image-file."+self.musicValues["Images"][self.lstwImages.currentRow()][2].split("/")[1]
                    InputOutputs.IA.writeToBinaryFile(sourceFile, self.musicValues["Images"][self.lstwImages.currentRow()][3])
                    InputOutputs.IA.moveOrChange(sourceFile,unicode(imagePath, "utf-8"))
        except:
            error = ReportBug.ReportBug()
            error.show()  
            
    def cancelAddImage(self):
        self.isActiveAddImage=False
        self.pbtnAddImage.setText(translate("MusicDetails", "Append"))
        self.pbtnSelectImage.hide()
        self.leImagePath.hide()
        self.lblImagePath.hide()
        self.lblImageType.hide()
        self.cbImageType.hide()
        self.pbtnCancelAddImage.hide()
        self.pbtnDeleteImage.show()
        self.pbtnSaveAsImage.show()
        
    def selectImage(self):
        try:
            imagePath = MFileDialog.getOpenFileName(self,translate("MusicDetails", "Choose Image"),
                InputOutputs.getDirName(self.musicValues["path"]),(str(translate("MusicDetails", "Images")) + " " + Variables.imageExtStringOnlyPNGAndJPG).decode("utf-8"))
            if imagePath!="":
                self.leImagePath.setText(imagePath)
        except:
            error = ReportBug.ReportBug()
            error.show()  
            
