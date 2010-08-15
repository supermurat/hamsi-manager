# -*- coding: utf-8 -*-

import InputOutputs
import os,sys
from MyObjects import *
from Viewers import ImageViewer
import Dialogs
import Organizer
import Universals

class CoverDetails(MDialog):
    global coverDialogs,closeAllCoverDialogs
    coverDialogs = []
    def __init__(self, _coverValues, _isOpenDetailsOnNewWindow=True, _FocusedInfoNo=None):
        """_coverValues[0] = Directory Path
        _coverValues[1] = Current Cover Path
        _coverValues[2] = Source Cover Path
        _coverValues[3] = Destination Cover Path
        """
        global coverDialogs
        if _isOpenDetailsOnNewWindow==False:
            isHasOpenedDialog=False
            for dialog in coverDialogs:
                if dialog.isVisible()==True:
                    isHasOpenedDialog=True
                    self = dialog
                    self.changeCoverValues(_coverValues)
                    dialog.activateWindow()
                    dialog.raise_()
                    break
            if isHasOpenedDialog==False:
                _isOpenDetailsOnNewWindow=True
        if _isOpenDetailsOnNewWindow==True:
            coverDialogs.append(self)
            MDialog.__init__(self, MApplication.activeWindow())
            if Universals.isActivePyKDE4==True:
                self.setButtons(MDialog.None)
            self.vblCurrent = MVBoxLayout()
            self.vblSource = MVBoxLayout()
            self.vblDestination = MVBoxLayout()
            self.lePathOfCurrent = MLineEdit(self)
            self.lePathOfSource = MLineEdit(self)
            self.lePathOfDestination = MLineEdit(self)
            self.changeCoverValues(_coverValues)
            pbtnClose = MPushButton(translate("ImageDetails", "OK"))
            pbtnClose.setFocus()
            pbtnClose.setMaximumWidth(150)
            MObject.connect(pbtnClose, SIGNAL("clicked()"), self.close)
            self.pbtnSource = MPushButton(translate("ImageDetails", "..."))
            self.pbtnSource.setMaximumWidth(30)
            MObject.connect(self.pbtnSource, SIGNAL("clicked()"), self.sourceClicked)
            self.pbtnDestination = MPushButton(translate("ImageDetails", "..."))
            self.pbtnDestination.setMaximumWidth(30)
            MObject.connect(self.pbtnDestination, SIGNAL("clicked()"), self.destinationClicked)
            self.hblImages = MHBoxLayout()
            self.hblImages.addLayout(self.vblCurrent)
            self.hblImages.addLayout(self.vblSource)
            self.hblImages.addLayout(self.vblDestination)
            hblPathOfSource = MHBoxLayout()
            hblPathOfDestination = MHBoxLayout()
            HBOXs = []
            HBOXs.append(MHBoxLayout())
            self.vblCurrent.addWidget(self.lePathOfCurrent)
            hblPathOfSource.addWidget(self.lePathOfSource)
            hblPathOfDestination.addWidget(self.lePathOfDestination)
            hblPathOfSource.addWidget(self.pbtnSource)
            hblPathOfDestination.addWidget(self.pbtnDestination)
            self.vblSource.addLayout(hblPathOfSource)
            self.vblDestination.addLayout(hblPathOfDestination)
            HBOXs[0].addStretch(1)
            HBOXs[0].addWidget(pbtnClose)
            self.pnlMain = MWidget()
            vblMain = MVBoxLayout(self.pnlMain)
            vblMain.addLayout(self.hblImages)
            vblMain.addLayout(HBOXs[0])
            if Universals.isActivePyKDE4==True:
                self.setMainWidget(self.pnlMain)
            else:
                self.setLayout(vblMain)
            self.show()
                  
    def changeCoverValues(self, _coverValues):
        try:
            self.wCurrent.setVisible(False)
            self.wSource.setVisible(False)
            self.wDestination.setVisible(False)
            self.wCurrent.deleteLater()
            self.wSource.deleteLater()
            self.wDestination.deleteLater()
        except:pass
        self.setWindowTitle((str(translate("ImageDetails", "Cover Details ( %s )")) % Organizer.showWithIncorrectChars(_coverValues[0])).decode("utf-8"))
        self.lePathOfCurrent.setText(Organizer.showWithIncorrectChars(_coverValues[1]).decode("utf-8"))
        self.lePathOfSource.setText(Organizer.showWithIncorrectChars(_coverValues[2]).decode("utf-8"))
        self.lePathOfDestination.setText(Organizer.showWithIncorrectChars(_coverValues[3]).decode("utf-8"))
        self.wCurrent = ImageViewer.ImageViewer(_coverValues[1])
        self.wSource = ImageViewer.ImageViewer(_coverValues[2])
        self.wDestination = ImageViewer.ImageViewer(_coverValues[3])
        self.wCurrent.setMinimumWidth(170)
        self.wSource.setMinimumWidth(170)
        self.wDestination.setMinimumWidth(170)
        self.wCurrent.setMinimumHeight(190)
        self.wSource.setMinimumHeight(190)
        self.wDestination.setMinimumHeight(190)
        self.vblCurrent.insertWidget(0, self.wCurrent, 1)
        self.vblSource.insertWidget(0, self.wSource, 1)
        self.vblDestination.insertWidget(0, self.wDestination, 1)
        
    def sourceClicked(self):
        imagePath = MFileDialog.getOpenFileName(self,translate("ImageDetails", "Choose Image"),
                                    self.lePathOfSource.text(),(str(translate("ImageDetails", "Images (*.%s)")) % Universals.getStrintFromList(Universals.getListFromStrint(Universals.MySettings["imageExtensions"])).replace(";", " *.")).decode("utf-8"))
        if imagePath!="":
            self.lePathOfSource.setText(imagePath)
        
    def destinationClicked(self):
        imagePath = MFileDialog.getSaveFileName(self,translate("ImageDetails", "Save As"),
                                    self.lePathOfDestination.text(),(str(translate("ImageDetails", "Images (*.%s)")) % Universals.getStrintFromList(Universals.getListFromStrint(Universals.MySettings["imageExtensions"])).replace(";", " *.")).decode("utf-8"))
        if imagePath!="":
            self.lePathOfDestination.setText(imagePath)
        
    def closeAllCoverDialogs():
        for dialog in coverDialogs:
            try:
                if dialog.isVisible()==True:
                    dialog.close()
            except AttributeError:
                continue
    
    
     
     
