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
                self.setButtons(MDialog.NoDefault)
            self.vblCurrent = MVBoxLayout()
            self.vblSource = MVBoxLayout()
            self.vblDestination = MVBoxLayout()
            self.lePathOfCurrent = MLineEdit(self)
            self.lePathOfSource = MLineEdit(self)
            self.lePathOfDestination = MLineEdit(self)
            self.wCurrent = ImageViewer.ImageViewer(self)
            self.wSource = ImageViewer.ImageViewer(self)
            self.wDestination = ImageViewer.ImageViewer(self, None, _isCorrectedWhenNotExist=True)
            self.wCurrent.setMinimumWidth(170)
            self.wSource.setMinimumWidth(170)
            self.wDestination.setMinimumWidth(170)
            self.wCurrent.setMinimumHeight(190)
            self.wSource.setMinimumHeight(190)
            self.wDestination.setMinimumHeight(190)
            self.vblCurrent.insertWidget(0, self.wCurrent, 1)
            self.vblSource.insertWidget(0, self.wSource, 1)
            self.vblDestination.insertWidget(0, self.wDestination, 1)
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
            MObject.connect(self.lePathOfSource, SIGNAL("textChanged(const QString&)"), self.sourceChanged)
            MObject.connect(self.lePathOfDestination, SIGNAL("textChanged(const QString&)"), self.destinationChanged)
            self.lePathOfCurrent.setEnabled(False)
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
        if _coverValues[1].strip()=="/": _coverValues[1] = _coverValues[0] + "/"
        if _coverValues[2].strip()=="/": _coverValues[2] = _coverValues[0] + "/"
        if _coverValues[3].strip()=="/": _coverValues[3] = _coverValues[0] + "/"
        self.setWindowTitle(trForUI(str(translate("ImageDetails", "Cover Details ( %s )")) % (_coverValues[0])))
        self.lePathOfCurrent.setText(trForUI(_coverValues[1]))
        self.lePathOfSource.setText(trForUI(_coverValues[2]))
        self.lePathOfDestination.setText(trForUI(_coverValues[3]))
        self.wCurrent.changeCoverValues(_coverValues[1])
        self.wSource.changeCoverValues(_coverValues[2])
        self.wDestination.changeCoverValues(_coverValues[3])
        
    def sourceChanged(self):
        self.wSource.changeCoverValues(str(self.lePathOfSource.text()))
        
    def destinationChanged(self):
        self.wDestination.changeCoverValues(str(self.lePathOfDestination.text()))
        
    def sourceClicked(self):
        imagePath = MFileDialog.getOpenFileName(self,translate("ImageDetails", "Choose Image"),
                                    self.lePathOfSource.text(),trForUI(str(translate("ImageDetails", "Images (*.%s)")) % Universals.getStrintFromList(Universals.getListFromStrint(Universals.MySettings["imageExtensions"])).replace(";", " *.")))
        if imagePath!="":
            self.lePathOfSource.setText(imagePath)
        
    def destinationClicked(self):
        imagePath = MFileDialog.getSaveFileName(self,translate("ImageDetails", "Save As"),
                                    self.lePathOfDestination.text(),trForUI(str(translate("ImageDetails", "Images (*.%s)")) % Universals.getStrintFromList(Universals.getListFromStrint(Universals.MySettings["imageExtensions"])).replace(";", " *.")))
        if imagePath!="":
            self.lePathOfDestination.setText(imagePath)
        
    def closeAllCoverDialogs():
        for dialog in coverDialogs:
            try:
                if dialog.isVisible()==True:
                    dialog.close()
            except:
                continue
    
    
     
     
