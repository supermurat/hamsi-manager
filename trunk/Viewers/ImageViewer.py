# -*- coding: utf-8 -*-

import InputOutputs
import os,sys
from MyObjects import *
import Dialogs
import Organizer
import Universals

class ImageViewer(MWidget):
    def __init__(self, _imagePath):
        MWidget.__init__(self, MApplication.activeWindow())
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
        self.pbtnZoomOut.setMaximumWidth(100)
        MObject.connect(self.pbtnZoomOut, SIGNAL("clicked()"), self.zoomOut)
        self.pbtnZoomIn = MPushButton(translate("ImageDetails", "+"))
        self.pbtnZoomIn.setMaximumWidth(100)
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
        self.lastValue = 1
        self.pmapImage.load(_imagePath.decode("utf-8"))
        self.lblImage.setPixmap(self.pmapImage)
        width = self.pmapImage.width()
        height = self.pmapImage.height()
        isLittle=False
        while isLittle==False:
            if width>150:
                width*=0.9
                height*=0.9
            if height>150:
                width*=0.9
                height*=0.9
            if width<=150 and height<=150:
                isLittle=True
        self.lblImage.resize(int(width),int(height))

    def goOriginalImageZoom(self):
        self.makeZoom(0)
    
    def zoomOut(self):
        self.makeZoom(0.9)
    
    def zoomIn(self):
        self.makeZoom(1.1)
        
    def makeZoom(self, _value):
        if _value!=0:
            self.lblImage.resize(self.lblImage.width()*_value,self.lblImage.height()*_value)
            self.lastValue*=_value
        else:
            self.lblImage.resize(self.pmapImage.width(),self.pmapImage.height())
            self.lastValue=1.0
        self.pbtnZoomOut.setEnabled(self.lastValue > 0.01)
        self.pbtnZoomIn.setEnabled(self.lastValue < 10.0)
    
    
     
     
