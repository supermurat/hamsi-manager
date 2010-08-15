# -*- coding: utf-8 -*-

import InputOutputs
import os,sys
from MyObjects import *
import Dialogs
import Organizer
import Universals

class ImageDetails(MDialog):
    global imageDialogs,closeAllImageDialogs
    imageDialogs = []
    def __init__(self,_file, _valueType="file", _isOpenDetailsOnNewWindow=True, _defaultMaxSize=[500, 400]):
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
            self.lblImage = MLabel()
            self.lblImage.setAlignment(Mt.AlignHCenter)
            self.lblImage.setScaledContents(True)
            self.pmapImage = MPixmap()
            self.changeFile(_file, _valueType)
            scraMain = MScrollArea()
            scraMain.setWidget(self.lblImage)
            scraMain.setFrameShape(MFrame.NoFrame)
            scraMain.setAlignment(Mt.AlignHCenter)
            pbtnClose = MPushButton(translate("ImageDetails", "OK"))
            pbtnClose.setFocus()
            pbtnClose.setMaximumWidth(100)
            MObject.connect(pbtnClose, SIGNAL("clicked()"), self.close)
            self.pbtnGoOriginalImageZoom = MPushButton(translate("ImageDetails", "Original"))
            self.pbtnGoOriginalImageZoom.setMaximumWidth(100)
            MObject.connect(self.pbtnGoOriginalImageZoom, SIGNAL("clicked()"), self.goOriginalImageZoom)
            self.pbtnZoomOut = MPushButton(translate("ImageDetails", "Smaller"))
            self.pbtnZoomOut.setMaximumWidth(100)
            MObject.connect(self.pbtnZoomOut, SIGNAL("clicked()"), self.zoomOut)
            self.pbtnZoomIn = MPushButton(translate("ImageDetails", "Larger"))
            self.pbtnZoomIn.setMaximumWidth(100)
            MObject.connect(self.pbtnZoomIn, SIGNAL("clicked()"), self.zoomIn)
            imageDialogs[-1].setWindowTitle(translate("ImageDetails", "Image"))
            HBOXs = []
            HBOXs.append(MHBoxLayout())
            HBOXs[0].addWidget(self.pbtnGoOriginalImageZoom)
            HBOXs[0].addWidget(self.pbtnZoomOut)
            HBOXs[0].addWidget(self.pbtnZoomIn)
            HBOXs[0].addWidget(pbtnClose)
            self.pnlMain = MWidget()
            vblMain = MVBoxLayout(self.pnlMain)
            vblMain.addWidget(scraMain)
            vblMain.addLayout(HBOXs[0])
            if Universals.isActivePyKDE4==True:
                self.setMainWidget(self.pnlMain)
            else:
                self.setLayout(vblMain)
            scraMain.setMinimumWidth(520)
            scraMain.setMinimumHeight(420)
            self.show()
                  
    def changeFile(self, _file, _valueType):
        self.zoomValue = 1.0
        if _valueType=="data":
            self.pmapImage.loadFromData(_file)
        else:
            self.pmapImage.load(_file)
        self.lblImage.setPixmap(self.pmapImage)
        self.width = self.pmapImage.width()
        self.height = self.pmapImage.height()
        while 1==1:
            if self.width>self.defaultMaxSize[0] or self.height>self.defaultMaxSize[1]:
                self.width*=0.9
                self.height*=0.9
            else:
                break
        self.lblImage.resize(int(self.width),int(self.height))
                  
    def closeAllImageDialogs():
        for dialog in imageDialogs:
            try:
                if dialog.isVisible()==True:
                    dialog.close()
            except AttributeError:
                continue

    def goOriginalImageZoom(self):
        self.makeZoom(1)
    
    def zoomOut(self):
        self.makeZoom(-0.1)
    
    def zoomIn(self):
        self.makeZoom(0.1)
        
    def makeZoom(self, _value):
        if _value==1:
            self.zoomValue = 1.0
            self.width = self.pmapImage.width()
            self.height = self.pmapImage.height()
            self.lblImage.resize(self.width, self.height)
        else:
            self.zoomValue += _value
            self.lblImage.resize(self.width*self.zoomValue, self.height*self.zoomValue)
    
    
     
     
