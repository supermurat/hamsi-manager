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
from Details.ImageDetails import ImageDetails, closeAllImageDialogs
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
                                translate("MusicDetails", "Track: "),
                                translate("MusicDetails", "Year: "),
                                translate("MusicDetails", "Genre: ")]
                self.pnlMain = MWidget()
                self.vblMain = MVBoxLayout(self.pnlMain)
                self.pnlClearable = None
                self.changeFile(_filePath, True)
                
                
                buttonHBOXs=MHBoxLayout()
                buttonHBOXs.addWidget(self.pbtnSave)
                buttonHBOXs.addWidget(self.pbtnClose)
                self.vblMain.addLayout(buttonHBOXs)
                if Universals.isActivePyKDE4==True:
                    self.setMainWidget(self.pnlMain)
                else:
                    self.setLayout(self.vblMain)
                self.show()
                self.player.play(_filePath, _isPlayNow)
        else:
            Dialogs.showError(translate("MusicDetails", "File Does Not Exist"), 
                    str(translate("MusicDetails", "\"%s\" does not exist.<br>Table will be refreshed automatically!<br>Please retry.")
                        ) % Organizer.getLink(trForUI(_filePath)))
            if hasattr(Universals.MainWindow, "FileManager"): Universals.MainWindow.FileManager.makeRefresh()
    
    def changeFile(self, _filePath, _isNew=False):
        self.musicFile = _filePath
        self.musicValues = Musics.readMusicFile(self.musicFile)
        self.setWindowTitle(trForUI(InputOutputs.getBaseName(self.musicFile)))  
        if self.pnlClearable != None:
            Universals.clearAllChilds(self.pnlClearable, True)
        self.pnlClearable = MWidget()
        self.vblMain.insertWidget(0, self.pnlClearable, 20)
        vblClearable = MVBoxLayout(self.pnlClearable)
        self.player = MusicPlayer.MusicPlayer(self, "dialog", _filePath)     
        self.infoLabels["baseNameOfDirectory"] = MLabel(self.labels[0]) 
        self.infoLabels["baseName"] = MLabel(self.labels[1]) 
        self.infoLabels["artist"] = MLabel(self.labels[2]) 
        self.infoLabels["title"] = MLabel(self.labels[3]) 
        self.infoLabels["album"] = MLabel(self.labels[4]) 
        self.infoLabels["trackNum"] = MLabel(self.labels[5]) 
        self.infoLabels["year"] = MLabel(self.labels[6]) 
        self.infoLabels["genre"] = MLabel(self.labels[7]) 
        self.infoValues["baseNameOfDirectory"] = MLineEdit(trForUI(Organizer.emend(self.musicValues["baseNameOfDirectory"], "directory", False)))
        self.infoValues["baseName"] = MLineEdit(trForUI(Organizer.emend(self.musicValues["baseName"], "file")))
        self.infoValues["artist"] = MLineEdit(trForUI(Organizer.emend(self.musicValues["artist"])))
        self.infoValues["title"] = MLineEdit(trForUI(Organizer.emend(self.musicValues["title"])))
        self.infoValues["album"] = MLineEdit(trForUI(Organizer.emend(self.musicValues["album"])))
        self.infoValues["trackNum"] = MLineEdit(trForUI(Organizer.emend(self.musicValues["trackNum"])))
        self.infoValues["year"] = MLineEdit(trForUI(Organizer.emend(self.musicValues["year"])))
        self.infoValues["genre"] = MLineEdit(trForUI(Organizer.emend(self.musicValues["genre"])))
        self.infoValues["firstComment"] = MPlainTextEdit(trForUI(Organizer.emend(self.musicValues["firstComment"])))
        self.infoValues["firstLyrics"] = MPlainTextEdit(trForUI(Organizer.emend(self.musicValues["firstLyrics"])))
        self.infoValues["firstComment"].setLineWrapMode(MPlainTextEdit.NoWrap)
        self.infoValues["firstLyrics"].setLineWrapMode(MPlainTextEdit.NoWrap)

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
        self.cbImageType.addItems(EyeD3Tagger.getImageTypes())
        self.lblImageType = MLabel(translate("MusicDetails", "Image Type: "))
        
        self.lstwImages = MListWidget()
        self.lstwImages.setGridSize(MSize(250,100))
        self.lstwImages.setIconSize(MSize(98,98))
        MObject.connect(self.lstwImages, SIGNAL("doubleClicked(QModelIndex)"),self.openImageDetails)
        self.lstwImages.clear()
        for image in self.musicValues["images"]:
            pixmImage = MPixmap()
            pixmImage.loadFromData(image[3])
            icnImage = QIcon(pixmImage)
            icnImage.actualSize(MSize(98,98))
            item = MListWidgetItem(icnImage,image[1]+"\n("+image[2]+")")
            item.setSizeHint(MSize(1,100))
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
        HBOXs[5].addWidget(self.infoLabels["trackNum"])
        HBOXs[5].addWidget(self.infoValues["trackNum"])
        HBOXs[5].addWidget(self.infoLabels["year"])
        HBOXs[5].addWidget(self.infoValues["year"])
        HBOXs[5].addWidget(self.infoLabels["genre"])
        HBOXs[5].addWidget(self.infoValues["genre"])
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
        vblComments.addWidget(self.infoValues["firstComment"])
        vblLyrics = MVBoxLayout()
        vblLyrics.addWidget(self.infoValues["firstLyrics"])
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
        vblClearable.addWidget(self.player)
        vblClearable.addLayout(vblInfos)
        vblClearable.addWidget(self.tabwTabs)
        self.pbtnSelectImage.hide()
        self.leImagePath.hide()
        self.lblImagePath.hide()
        self.lblImageType.hide()
        self.cbImageType.hide()
        self.pbtnCancelAddImage.hide()
        
    
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
            newMusicValues["artist"] = str(self.infoValues["artist"].text())
            newMusicValues["title"] = str(self.infoValues["title"].text())
            newMusicValues["album"] = str(self.infoValues["album"].text())
            newMusicValues["trackNum"] = str(self.infoValues["trackNum"].text())
            newMusicValues["year"] = str(self.infoValues["year"].text())
            newMusicValues["genre"] = str(self.infoValues["genre"].text())
            newMusicValues["firstComment"] = str(self.infoValues["firstComment"].toPlainText())
            newMusicValues["firstLyrics"] = str(self.infoValues["firstLyrics"].toPlainText())
            newPath = Musics.writeMusicFile(self.musicValues, newMusicValues)
            if newPath!=self.musicValues["path"]:
                self.changeFile(newPath)
            if hasattr(Universals.MainWindow, "FileManager"): Universals.MainWindow.FileManager.makeRefresh()
            Records.saveAllRecords()
        except:
            error = ReportBug.ReportBug()
            error.show()  
        
    def openImageDetails(self, _index):
        try:
            ImageDetails(self.musicValues["images"][_index.row()][3], "data", self.isOpenImageDetailsOnNewWindow.isChecked())
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
                Musics.writeMusicFile(self.musicValues,False,True,self.cbImageType.currentIndex(),str(str(self.leImagePath.text())))
                self.changeFile(self.musicFile)
                self.cancelAddImage()
            else:
                Dialogs.showError(translate("MusicDetails", "Image Does Not Exist"),
                    str(translate("MusicDetails", "\"%s\" does not exist.")
                        ) % Organizer.getLink(trForUI(self.leImagePath.text())))
    
    def deleteImage(self):
        if self.lstwImages.currentRow()!=-1:
            closeAllImageDialogs()
            Musics.writeMusicFile(self.musicValues,False,True,self.musicValues["images"][self.lstwImages.currentRow()][0],False)
            self.changeFile(self.musicFile)
    
    def saveAsImage(self):
        try:
            if self.lstwImages.currentRow()!=-1:
                imagePath = MFileDialog.getSaveFileName(self,translate("MusicDetails", "Save As"),
                                    InputOutputs.getDirName(self.musicValues["path"]), trForUI(str(translate("MusicDetails", "Images (*.%s)")) %(str(self.musicValues["images"][self.lstwImages.currentRow()][2]).split("/")[1])))
                if imagePath!="":
                    sourceFile = os.getenv("TMP")+"/HamsiManager-image-file."+self.musicValues["images"][self.lstwImages.currentRow()][2].split("/")[1]
                    InputOutputs.IA.writeToBinaryFile(sourceFile, self.musicValues["images"][self.lstwImages.currentRow()][3])
                    InputOutputs.IA.moveOrChange(sourceFile, str(imagePath))
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
                InputOutputs.getDirName(self.musicValues["path"]),trForUI(str(translate("MusicDetails", "Images")) + " " + Variables.imageExtStringOnlyPNGAndJPG))
            if imagePath!="":
                self.leImagePath.setText(imagePath)
        except:
            error = ReportBug.ReportBug()
            error.show()  
            
