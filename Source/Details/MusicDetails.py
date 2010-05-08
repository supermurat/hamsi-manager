# -*- coding: utf-8 -*-

from InputOutputs import Musics
import InputOutputs
import os,sys
from MyObjects import *
from PyQt4.Qt import QIcon
import Dialogs
import Organizer
import Player
from ImageDetails import ImageDetails, closeAllImageDialogs
import Universals
import ReportBug

class MusicDetails(MDialog):
    global musicDialogs, closeAllMusicDialogs
    musicDialogs =[]
    def __init__(self,_filePath,_isOpenDetailsOnNewWindow,_isPlayNow=True,_FocusedInfoNo=None):
        global musicDialogs, musicTagType
        musicTagType = Universals.MySettings["musicTagType"]
        if InputOutputs.isFile(_filePath):
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
                        if _FocusedInfoNo!=None:
                            self.infoValues[_FocusedInfoNo].setFocus()
                        break
                if isHasOpenedDialog==False:
                    _isOpenDetailsOnNewWindow=True
            if _isOpenDetailsOnNewWindow==True:
                musicDialogs.append(self)
                MDialog.__init__(self, MApplication.activeWindow())
                if Universals.isActivePyKDE4==True:
                    self.setButtons(MDialog.None)
                self.isActiveAddImage = False
                self.infoLabels = []
                self.infoValues = []
                self.musicValues = []
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
                self.leImagePath = MLineEdit(u"")
                self.lblImagePath = MLabel(translate("MusicDetails", "Image Path: "))
                self.cbImageType = MComboBox()
                self.cbImageType.addItems(Musics.types)
                self.lblImageType = MLabel(translate("MusicDetails", "Image Type: "))
                self.labels = [translate("MusicDetails", "Directory: "),
                                translate("MusicDetails", "File Name: "),
                                translate("MusicDetails", "Artist: "),
                                translate("MusicDetails", "Title: "),
                                translate("MusicDetails", "Album: "),
                                translate("MusicDetails", "Track: "),
                                translate("MusicDetails", "Year: "),
                                translate("MusicDetails", "Genre: "),
                                translate("MusicDetails", "Comments: "),
                                translate("MusicDetails", "Lyrics: ")]
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
                for infoNo in range(5):
                    HBOXs.append(MHBoxLayout())
                    HBOXs[infoNo].addWidget(self.infoLabels[infoNo])
                    HBOXs[infoNo].addWidget(self.infoValues[infoNo])
                HBOXs.append(MHBoxLayout())
                HBOXs[5].addWidget(self.infoLabels[5])
                HBOXs[5].addWidget(self.infoValues[5])
                HBOXs[5].addWidget(self.infoLabels[6])
                HBOXs[5].addWidget(self.infoValues[6])
                HBOXs[5].addWidget(self.infoLabels[7])
                HBOXs[5].addWidget(self.infoValues[7])
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
                vblComments.addWidget(self.infoValues[8])
                vblLyrics = MVBoxLayout()
                vblLyrics.addWidget(self.infoValues[9])
                self.pnlMain = MWidget()
                self.tabwTabs = MTabWidget(self.pnlMain)
                self.pnlComments = MWidget(self.tabwTabs)
                self.pnlLyrics = MWidget(self.tabwTabs)
                self.pnlImages = MWidget(self.tabwTabs)
                self.pnlImages.setLayout(vblImages)
                self.pnlComments.setLayout(vblComments)
                self.pnlLyrics.setLayout(vblLyrics)
                self.tabwTabs.addTab(self.pnlComments, self.labels[8][:-2])
                self.tabwTabs.addTab(self.pnlLyrics, self.labels[9][:-2])
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
                if _FocusedInfoNo!=None:
                    self.infoValues[_FocusedInfoNo].setFocus()
        else:
            Dialogs.showError(translate("MusicDetails", "File Does Not Exist"), 
                    str(translate("MusicDetails", "\"%s\" does not exist.<br>Table will be refreshed automatically!<br>Please retry.")
                        ) % Organizer.getLink(Organizer.showWithIncorrectChars(_filePath)))
            from Universals import MainWindow
            MainWindow.FileManager.makeRefresh()
    
    def checkMusicTagType(self):
        if musicTagType=="ID3 V2":
            self.tabwTabs.setTabEnabled(1, True)
            self.tabwTabs.setTabEnabled(2, True)
        else:
            self.tabwTabs.setTabEnabled(1, False)
            self.tabwTabs.setTabEnabled(2, False)
    
    def changeFile(self, _filePath, _isNew=False):
        self.musicFile = _filePath
        self.musicValues = Musics.readMusics(None,self.musicFile)
        self.setWindowTitle(Organizer.showWithIncorrectChars(InputOutputs.getBaseName(self.musicFile)).decode("utf-8"))  
        self.player = Player.Player(self, "dialog", _filePath)              
        for infoNo, label in enumerate(self.labels):
            if self.musicValues[infoNo]=="None" or self.musicValues[infoNo]=="None/None":
                self.musicValues[infoNo] = ""
            if _isNew==True and infoNo!=8 and infoNo!=9:
                self.infoLabels.append(MLabel(label))
                if infoNo==5 or infoNo==6 or infoNo==7:
                    self.infoLabels[infoNo].setMaximumWidth(len(label)*6)
                    self.infoLabels[infoNo].setMinimumWidth(len(label)*6)
                else:
                    self.infoLabels[infoNo].setMaximumWidth(105)
                    self.infoLabels[infoNo].setMinimumWidth(105)
            if infoNo==8 or infoNo==9:
                if _isNew==True:
                    self.infoValues.append(MPlainTextEdit(Organizer.emend(self.musicValues[infoNo]).decode("utf-8")))
                    self.infoValues[infoNo].setLineWrapMode(MPlainTextEdit.NoWrap)
                else:
                    self.infoValues[infoNo].setPlainText(Organizer.emend(self.musicValues[infoNo]).decode("utf-8"))
            elif infoNo==0:
                if _isNew==True:
                    self.infoValues.append(MLineEdit(Organizer.emend(self.musicValues[infoNo], True, False).decode("utf-8")))
                else:
                    self.infoValues[infoNo].setText(Organizer.emend(self.musicValues[infoNo], True, False).decode("utf-8"))
            elif infoNo==1:
                newInfo = Organizer.emend(self.musicValues[infoNo], True)
                if newInfo.find(".")!=-1:
                    tempInfo=""
                    newInfos = newInfo.split(".")
                    for key,i in enumerate(newInfos):
                        if key!=len(newInfos)-1:
                            tempInfo+=i+"."
                        else:
                            tempInfo+=self.musicValues[infoNo].split(".")[-1].decode("utf-8").lower()
                            newInfo = tempInfo
                if _isNew==True:
                    self.infoValues.append(MLineEdit(newInfo.decode("utf-8")))
                else:
                    self.infoValues[infoNo].setText(newInfo.decode("utf-8"))
            else:
                if _isNew==True:
                    self.infoValues.append(MLineEdit(Organizer.emend(self.musicValues[infoNo]).decode("utf-8")))
                else:
                    self.infoValues[infoNo].setText(Organizer.emend(self.musicValues[infoNo]).decode("utf-8"))
            if infoNo<5:
                self.infoValues[infoNo].setMinimumWidth(290)
                self.infoValues[infoNo].setMaximumWidth(290)
            elif infoNo==5 or infoNo==6:
                self.infoValues[infoNo].setMaximumWidth(60)
                self.infoValues[infoNo].setMinimumWidth(60)
            elif infoNo==7:
                self.infoValues[infoNo].setMaximumWidth(100)
                self.infoValues[infoNo].setMinimumWidth(100)
        self.lstwImages.clear()
        for image in self.musicValues[-1]:
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
            except AttributeError:
                continue
        
    def save(self):
        try:
            import Records
            Records.setTitle(translate("MusicDetails", "Music File"))
            closeAllImageDialogs()
            newMusicValues=[]
            for infoNo,info in enumerate(self.infoValues):
                if infoNo==0:
                    if str(unicode(info.text()).encode("utf-8")).find(InputOutputs.getDirName(self.musicValues[0]))!=-1:
                        newMusicValues.append(unicode(info.text()).encode("utf-8"))
                    else:
                        newMusicValues.append(InputOutputs.getDirName(self.musicValues[0])+unicode(info.text()).encode("utf-8"))
                elif infoNo==8 or infoNo==9:
                    newMusicValues.append(unicode(info.toPlainText()).encode("utf-8"))
                elif infoNo>9:
                    pass
                else:
                    newMusicValues.append(unicode(info.text()).encode("utf-8"))
            newPath = Musics.writeMusicFile(self.musicValues,newMusicValues)
            if newPath!=self.musicValues[0]+"/"+self.musicValues[1]:
                self.changeFile(newPath)
            from Universals import MainWindow
            MainWindow.FileManager.makeRefresh()
            Records.saveAllRecords()
        except:
            error = ReportBug.ReportBug()
            error.show()  
        
    def openImageDetails(self, _index):
        try:
            ImageDetails(self.musicValues[-1][_index.row()][3], "data", self.isOpenImageDetailsOnNewWindow.isChecked())
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
            if InputOutputs.isFile(self.leImagePath.text())==True:
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
            Musics.writeMusicFile(self.musicValues,False,True,self.musicValues[-1][self.lstwImages.currentRow()][0],False)
            self.changeFile(self.musicFile)
    
    def saveAsImage(self):
        try:
            if self.lstwImages.currentRow()!=-1:
                imagePath = MFileDialog.getSaveFileName(self,translate("MusicDetails", "Save As"),
                                    self.musicValues[0],str(translate("MusicDetails", "Images (*.%s)")
                                        ) %(str(self.musicValues[-1][self.lstwImages.currentRow()][2]).split("/")[1].decode("utf-8")))
                if imagePath!="":
                    sourceFile = os.getenv("TMP")+"/HamsiManager-image-file."+self.musicValues[-1][self.lstwImages.currentRow()][2].split("/")[1]
                    InputOutputs.writeToBinaryFile(sourceFile, self.musicValues[-1][self.lstwImages.currentRow()][3])
                    InputOutputs.moveOrChange(sourceFile,unicode(imagePath, "utf-8"))
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
                                    self.musicValues[0],(str(translate("MusicDetails", "Images")) + " " +Universals.imageExtStringOnlyPNGAndJPG).decode("utf-8"))
            if imagePath!="":
                self.leImagePath.setText(imagePath)
        except:
            error = ReportBug.ReportBug()
            error.show()  
            