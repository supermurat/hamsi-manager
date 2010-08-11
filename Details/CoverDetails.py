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
            self.changeCoverValues(_coverValues)
            pbtnClose = MPushButton(translate("ImageDetails", "OK"))
            pbtnClose.setFocus()
            pbtnClose.setMaximumWidth(100)
            MObject.connect(pbtnClose, SIGNAL("clicked()"), self.close)
            self.pbtnSource = MPushButton(translate("ImageDetails", "Source"))
            self.pbtnSource.setMaximumWidth(100)
            MObject.connect(self.pbtnSource, SIGNAL("clicked()"), self.sourceClicked)
            self.pbtnDestination = MPushButton(translate("ImageDetails", "Destination"))
            self.pbtnDestination.setMaximumWidth(100)
            MObject.connect(self.pbtnDestination, SIGNAL("clicked()"), self.destinationClicked)
            self.setWindowTitle(translate("ImageDetails", "Cover Details"))
            self.hblImages = MHBoxLayout()
            self.hblImages.addLayout(self.vblCurrent)
            self.hblImages.addLayout(self.vblSource)
            self.hblImages.addLayout(self.vblDestination)
            HBOXs = []
            HBOXs.append(MHBoxLayout())
            self.vblSource.addWidget(self.pbtnSource, 1)
            self.vblDestination.addWidget(self.pbtnDestination, 1)
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
        self.wCurrent = ImageViewer.ImageViewer(_coverValues[1])
        self.wSource = ImageViewer.ImageViewer(_coverValues[2])
        self.wDestination = ImageViewer.ImageViewer(_coverValues[3])
        self.vblCurrent.insertWidget(0, self.wCurrent)
        self.vblSource.insertWidget(0, self.wSource)
        self.vblDestination.insertWidget(0, self.wDestination)
        
    def sourceClicked(self):
        pass
        
    def destinationClicked(self):
        pass
        
    def closeAllCoverDialogs():
        for dialog in coverDialogs:
            try:
                if dialog.isVisible()==True:
                    dialog.close()
            except AttributeError:
                continue
    
    
     
     
