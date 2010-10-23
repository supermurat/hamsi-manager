# -*- coding: utf-8 -*-

import os,sys
from MyObjects import *
from Viewers import ImageViewer
import Dialogs
import Organizer
import Universals

class ImageDetails(MDialog):
    global imageDialogs,closeAllImageDialogs
    imageDialogs = []
    def __init__(self, _file, _valueType="file", _isOpenDetailsOnNewWindow=True, _defaultMaxSize=[500, 400]):
        global imageDialogs
        self.defaultMaxSize = _defaultMaxSize
        if _isOpenDetailsOnNewWindow==False:
            isHasOpenedDialog=False
            for dialog in imageDialogs:
                if dialog.isVisible()==True:
                    isHasOpenedDialog=True
                    self = dialog
                    self.changeFile(_file, _valueType)
                    dialog.activateWindow()
                    dialog.raise_()
                    break
            if isHasOpenedDialog==False:
                _isOpenDetailsOnNewWindow=True
        if _isOpenDetailsOnNewWindow==True:
            imageDialogs.append(self)
            MDialog.__init__(self, MApplication.activeWindow())
            if Universals.isActivePyKDE4==True:
                self.setButtons(MDialog.None)
            self.wImage = ImageViewer.ImageViewer(self, _defaultMaxSize=_defaultMaxSize)
            self.wImage.setMinimumWidth(520)
            self.wImage.setMinimumHeight(420)
            self.changeFile(_file, _valueType)
            pbtnClose = MPushButton(translate("ImageDetails", "OK"))
            pbtnClose.setFocus()
            pbtnClose.setMaximumWidth(100)
            MObject.connect(pbtnClose, SIGNAL("clicked()"), self.close)
            HBOXs = []
            HBOXs.append(MHBoxLayout())
            HBOXs[0].addStretch(1)
            HBOXs[0].addWidget(pbtnClose)
            self.pnlMain = MWidget()
            vblMain = MVBoxLayout(self.pnlMain)
            vblMain.addWidget(self.wImage)
            vblMain.addLayout(HBOXs[0])
            if Universals.isActivePyKDE4==True:
                self.setMainWidget(self.pnlMain)
            else:
                self.setLayout(vblMain)
            self.show()
                  
    def changeFile(self, _file, _valueType):
        if _valueType=="data":
            self.setWindowTitle(translate("ImageDetails", "Image Details"))
        else:
            self.setWindowTitle((str(translate("ImageDetails", "Image Details ( %s )")) % Organizer.showWithIncorrectChars(_file)).decode("utf-8"))
        self.wImage.changeCoverValues(_file, _valueType)
                  
    def closeAllImageDialogs():
        for dialog in imageDialogs:
            try:
                if dialog.isVisible()==True:
                    dialog.close()
            except AttributeError:
                continue
