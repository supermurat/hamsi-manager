## This file is part of HamsiManager.
## 
## Copyright (c) 2010 - 2012 Murat Demir <mopened@gmail.com>      
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


import InputOutputs
import os,sys
from Core.MyObjects import *
from Core import Dialogs
from Core import Organizer
from Core import Universals

class ImageViewer(MWidget):
    def __init__(self, _parent, _image = None, _valueType="file", _isCorrectedWhenNotExist=False, _defaultMaxSize=[150, 150]):
        MWidget.__init__(self, _parent)
        self.defaultMaxSize = _defaultMaxSize
        self.isCorrectedWhenNotExist = _isCorrectedWhenNotExist
        self.lblImage = MLabel()
        self.lblImage.setAlignment(Mt.AlignHCenter)
        self.lblImage.setScaledContents(True)
        self.pmapImage = MPixmap()
        self.changeCoverValues(_image, _valueType)
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
                  
    def changeCoverValues(self, _image=None, _valueType="file"):
        self.zoomValue = 1.0
        if _image!=None and _valueType=="file":
            if InputOutputs.isFile(_image)==False:
                if self.isCorrectedWhenNotExist==True:
                    _image = InputOutputs.joinPath(Universals.themePath, "Images", "ok.png")
                else:
                    _image = InputOutputs.joinPath(Universals.themePath, "Images", "notExist.png")
        elif _valueType=="file":
            _image = InputOutputs.joinPath(Universals.themePath, "Images", "notExist.png")
        self.pmapImage.detach()
        if _valueType=="data":
            self.pmapImage.loadFromData(_image)
        else:
            self.pmapImage.load(trForM(_image))
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
    
    
     
     
