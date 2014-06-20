# # This file is part of HamsiManager.
##
## Copyright (c) 2010 - 2013 Murat Demir <mopened@gmail.com>
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


import os, sys
from Core.MyObjects import *
from Viewers import ImageViewer
from Core import Dialogs
from Core import Organizer
from Core import Universals as uni


class HtmlDetails(MDialog):
    global htmlDialogs
    htmlDialogs = []

    def __init__(self, _file, _valueType="file", _isOpenDetailsOnNewWindow=True):
        global htmlDialogs
        if _isOpenDetailsOnNewWindow == False:
            isHasOpenedDialog = False
            for dialog in htmlDialogs:
                if dialog.isVisible():
                    isHasOpenedDialog = True
                    self = dialog
                    self.changeFile(_file, _valueType)
                    dialog.activateWindow()
                    dialog.raise_()
                    break
            if isHasOpenedDialog == False:
                _isOpenDetailsOnNewWindow = True
        if _isOpenDetailsOnNewWindow:
            QtWebKit = getMyObject("QtWebKit")
            htmlDialogs.append(self)
            MDialog.__init__(self, MApplication.activeWindow())
            if isActivePyKDE4:
                self.setButtons(MDialog.NoDefault)
            self.wvWeb = QtWebKit.QWebView()
            self.wvWeb.setMinimumWidth(520)
            self.wvWeb.setMinimumHeight(420)
            self.changeFile(_file, _valueType)
            pbtnClose = MPushButton(translate("HtmlDetails", "OK"))
            pbtnClose.setFocus()
            pbtnClose.setMaximumWidth(100)
            MObject.connect(pbtnClose, SIGNAL("clicked()"), self.close)
            HBOXs = []
            HBOXs.append(MHBoxLayout())
            HBOXs[0].addStretch(1)
            HBOXs[0].addWidget(pbtnClose)
            self.pnlMain = MWidget()
            vblMain = MVBoxLayout(self.pnlMain)
            vblMain.addWidget(self.wvWeb)
            vblMain.addLayout(HBOXs[0])
            if isActivePyKDE4:
                self.setMainWidget(self.pnlMain)
            else:
                self.setLayout(vblMain)
            self.show()

    def changeFile(self, _file, _valueType):
        if _valueType == "data":
            self.setWindowTitle(translate("HtmlDetails", "Html Details"))
            self.wvWeb.setHtml(str(_file))
        else:
            self.setWindowTitle(str(str(translate("HtmlDetails", "Html Details ( %s )")) % (_file)))
            self.wvWeb.setUrl(MUrl(str(_file)))

    @staticmethod
    def closeAllHtmlDialogs():
        for dialog in htmlDialogs:
            try:
                if dialog.isVisible():
                    dialog.close()
            except:
                continue
