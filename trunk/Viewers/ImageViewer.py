# -*- coding: utf-8 -*-

import InputOutputs
import os,sys
from MyObjects import *
import Dialogs
import Organizer
import Universals

class ImageViewer(MWidget):
    def __init__(self, _imagePath, _defaultMaxSize=[150, 150]):
        MWidget.__init__(self, MApplication.activeWindow())
        self.defaultMaxSize = _defaultMaxSize
        self.lblImage = MLabel()
        self.lblImage.setAlignment(Mt.AlignHCenter)
        self.lblImage.setScaledContents(True)
        self.pmapImage = MPixmap()
        self.changeCoverValues(_imagePath)
        scraMain = MScrollArea()
        scraMain.setWidget(self.lblImage)
        scraMain.setFrameShape(MFrame.NoFrame)
        scraMain.setAlignment(Mt.AlignHCenter)
        self.pbtnGoOriginalImageZoom = MPushButton(translate("ImageDetails", "1:1"))
        self.pbtnGoOriginalImageZoom.setMaximumWidth(100)
        MObject.connect(self.pbtnGoOriginalImageZoom, SIGNAL("clicked()"), self.goOriginalImageZoom)
        self.pbtnZoomOut = MPushButton(translate("ImageDetails", "-"))
        self.pbtnZoomOut.setMaximumWidth(30)
        MObject.connect(self.pbtnZoomOut, SIGNAL("clicked()"), self.zoomOut)
        self.pbtnZoomIn = MPushButton(translate("ImageDetails", "+"))
        self.pbtnZoomIn.setMaximumWidth(30)
        MObject.connect(self.pbtnZoomIn, SIGNAL("clicked()"), self.zoomIn)
        HBOXs = []
        HBOXs.append(MHBoxLayout())
        HBOXs[0].addWidget(self.pbtnGoOriginalImageZoom)
        HBOXs[0].addWidget(self.pbtnZoomOut)
        HBOXs[0].addWidget(self.pbtnZoomIn)
        self.pnlMain = MWidget()
        vblMain = MVBoxLayout(self.pnlMain)
        vblMain.addWidget(scraMain)
        vblMain.addLayout(HBOXs[0])
        self.setLayout(vblMain)
        self.show()
                  
    def changeCoverValues(self, _imagePath):
        self.zoomValue = 1.0
        self.pmapImage.load(_imagePath.decode("utf-8"))
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
    
    
     
     
