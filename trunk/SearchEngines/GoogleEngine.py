# This file is part of HamsiManager.
#
# Copyright (c) 2010 - 2014 Murat Demir <mopened@gmail.com>
#
# Hamsi Manager is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Hamsi Manager is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with HamsiManager; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA


isAvailable = True
contentType = "value"

from Core.MyObjects import *
from Core import Dialogs
import json
import urllib
from Core import Universals as uni
from Core import ReportBug

pluginName = "Google"


class Search(MDialog):
    def __init__(self, _parent, _isCheckSingleFile=False):
        MDialog.__init__(self, _parent)
        if isActivePyKDE4:
            self.setButtons(MDialog.NoDefault)
        self.isCheckSingleFile = _isCheckSingleFile
        self.nullFiles = []
        self.falseFiles = []
        self.trueFiles = []
        self.incorrectFiles = []
        self.setModal(True)
        self.prgbState = MProgressBar()
        self.prgbStateLabel = MLabel(translate("SearchEngines", "Progress State"))
        self.pbtnApply = MPushButton(translate("SearchEngines", "Apply"))
        self.pbtnApply.setMaximumWidth(120)
        self.pbtnApply.setVisible(False)
        self.pbtnCancel = MPushButton(translate("SearchEngines", "Cancel"))
        self.pbtnCancel.setMaximumWidth(120)
        self.pbtnClose = MPushButton(translate("SearchEngines", "Close"))
        self.pbtnClose.setMaximumWidth(120)
        self.pbtnClose.setVisible(False)
        MObject.connect(self.pbtnApply, SIGNAL("clicked()"), self.apply)
        MObject.connect(self.pbtnClose, SIGNAL("clicked()"), self.close)
        MObject.connect(self.pbtnCancel, SIGNAL("clicked()"), uni.cancelThreadAction)
        pnlMain = MWidget(self)
        self.saPanel = MScrollArea(pnlMain)
        self.vblPanel = MVBoxLayout()
        self.vblPanel.setAlignment(Mt.AlignHCenter)
        self.vblPanel.setAlignment(Mt.AlignTop)
        self.vblPanel.addWidget(self.prgbStateLabel)
        self.vblPanel.addWidget(self.prgbState)
        self.pnlPanel = MWidget(pnlMain)
        self.pnlPanel.setLayout(self.vblPanel)
        self.pnlPanel.setFixedSize(595, 100)
        self.saPanel.setWidget(self.pnlPanel)
        self.saPanel.setFrameShape(MFrame.StyledPanel)
        self.saPanel.setAlignment(Mt.AlignHCenter)
        self.saPanel.setFixedSize(645, 110)
        vblBox = MVBoxLayout(pnlMain)
        vblBox.addWidget(self.saPanel)
        hblBox = MHBoxLayout()
        hblBox.addStretch(2)
        hblBox.addWidget(self.pbtnCancel)
        hblBox.addWidget(self.pbtnClose)
        hblBox.addWidget(self.pbtnApply)
        vblBox.addLayout(hblBox)
        if isActivePyKDE4:
            self.setMainWidget(pnlMain)
        else:
            self.setLayout(vblBox)
        self.setWindowTitle(translate("SearchEngines", "Searching Information On The Internet!.."))
        self.setFixedSize(670, 160)
        self.setAttribute(Mt.WA_DeleteOnClose)
        self.show()
        self.connect(self, SIGNAL("changedProgressBarValue"), self.changeProgressBarValue)
        from Core import MyThread

        myProcs = MyThread.MyThread(self.startSearch, self.finishSearch)
        myProcs.start()

    def closeEvent(self, _event):
        if uni.isContinueThreadAction():
            uni.cancelThreadAction()
            _event.ignore()

    def changeProgressBarValue(self, _value):
        self.prgbState.setValue(_value)
        self.prgbState.repaint()

    def startSearch(self):
        try:
            if self.isCheckSingleFile:
                self.prgbState.setRange(0, 1)
                self.rows = list(range(getMainTable().currentRow(), getMainTable().currentRow() + 1))
                self.heightValue = 150
            else:
                self.prgbState.setRange(0, getMainTable().rowCount())
                self.rows = list(range(getMainTable().rowCount()))
                if getMainTable().rowCount() < 7:
                    self.heightValue = 300
                else:
                    self.heightValue = 500
            valuesOfFiles = []
            for rowNo in self.rows:
                valuesOfFiles.append([str(getMainTable().item(rowNo, 1).text()), rowNo])
            uni.startThreadAction()
            self.emit(SIGNAL("changedProgressBarValue"), 0)
            for valuesOfFile in valuesOfFiles:
                isContinueThreadAction = uni.isContinueThreadAction()
                if isContinueThreadAction:
                    try:
                        from ThirdPartyModules import google

                        searchResults = google.search(valuesOfFile[0], lang='tr', stop=5, only_standard=True)
                        isOK = False
                        if len(searchResults) != 0:
                            for result in searchResults:
                                if str(result.title).lower() == str(valuesOfFile[0]).lower():
                                    self.trueFiles.append(valuesOfFile)
                                    isOK = True
                                    break
                            if not isOK:
                                self.falseFiles.append([searchResults, valuesOfFile])
                        else:
                            self.nullFiles.append(valuesOfFile)
                    except Exception as err:
                        # Dialogs.showError(translate("SearchEngines", "An Error Occured"),
                        #                   str(translate("SearchEngines",
                        #                                 "Fetching information for the music file that caused the error is canceled.<br>If you receive the same error, please try the other search engines.<br><b>Error details:</b><br>%s")) % (
                        #                       str(err)))
                        print(err)
                        self.incorrectFiles.append(valuesOfFile)
                    self.emit(SIGNAL("changedProgressBarValue"), valuesOfFile[1] + 1)
                if isContinueThreadAction is False:
                    break
            uni.finishThreadAction()
            return True
        except:
            ReportBug.ReportBug()
            return False

    def finishSearch(self, _isContinue):
        try:
            if _isContinue:
                self.prgbState.setVisible(False)
                self.prgbStateLabel.setVisible(False)
                self.showInList()
                self.pbtnCancel.setVisible(False)
                self.pbtnClose.setVisible(True)
                self.pbtnApply.setVisible(True)
                self.setMinimumSize(670, self.heightValue + 50)
                self.saPanel.setFixedSize(645, self.heightValue)
        except:
            ReportBug.ReportBug()

    def showInList(self):
        try:
            HBoxs = []
            if len(self.trueFiles) > 0 or len(self.falseFiles) > 0:
                if len(self.trueFiles) > 0:
                    HBoxs.append(MHBoxLayout())
                    HBoxs[-1].addWidget(MLabel(translate("SearchEngines", "Files identified correctly:")))
                    for song in self.trueFiles:
                        HBoxs.append(MHBoxLayout())
                        lblSearchedFor = MTextEdit(str(song[0]))
                        lblSearchedFor.setFixedWidth(200)
                        HBoxs[-1].addWidget(lblSearchedFor)
                        cbValue = MComboBox()
                        cbValue.setObjectName("Value" + str(song[1]))
                        cbValue.setEditable(True)
                        cbValue.addItem(str(song[0]))
                        HBoxs[-1].addWidget(cbValue)
                if len(self.falseFiles) > 0:
                    HBoxs.append(MHBoxLayout())
                    HBoxs[-1].addWidget(MLabel(translate("SearchEngines", "Files identified correctly but with errors:")))
                    for song in self.falseFiles:
                        HBoxs.append(MHBoxLayout())
                        lblSearchedFor = MTextEdit(str(self.parent().item(song[1][1], 1).text()))
                        lblSearchedFor.setFixedWidth(200)
                        HBoxs[-1].addWidget(lblSearchedFor)
                        cbValue = MComboBox()
                        cbValue.setObjectName("Value" + str(song[1][1]))
                        cbValue.setEditable(True)
                        for result in song[0]:
                            cbValue.addItem(str(result.title))
                        HBoxs[-1].addWidget(cbValue)
            if len(self.nullFiles) > 0:
                HBoxs.append(MHBoxLayout())
                HBoxs[-1].addWidget(MLabel(translate("SearchEngines", "Files identified incorrectly:")))
                for song in self.nullFiles:
                    HBoxs.append(MHBoxLayout())
                    lblSearchedFor = MTextEdit(str(song[0]))
                    lblSearchedFor.setFixedWidth(200)
                    HBoxs[-1].addWidget(lblSearchedFor)
                    cbValue = MComboBox()
                    cbValue.setObjectName("Value" + str(song[1]))
                    cbValue.setEditable(True)
                    cbValue.addItem(str(song[0]))
                    HBoxs[-1].addWidget(cbValue)
            if len(self.incorrectFiles) > 0:
                HBoxs.append(MHBoxLayout())
                HBoxs[-1].addWidget(MLabel(translate("SearchEngines", "Files that caused errors:")))
                for song in self.incorrectFiles:
                    HBoxs.append(MHBoxLayout())
                    lblSearchedFor = MTextEdit(str(self.parent().item(song[1], 1).text()))
                    lblSearchedFor.setFixedWidth(200)
                    HBoxs[-1].addWidget(lblSearchedFor)
                    cbValue = MComboBox()
                    cbValue.setObjectName("Value" + str(song[1]))
                    cbValue.setEditable(True)
                    cbValue.addItem(str(song[0]))
                    HBoxs[-1].addWidget(cbValue)
            for box in HBoxs:
                self.vblPanel.addLayout(box)
            self.pnlPanel.setFixedSize(620, len(HBoxs) * 30)
        except:
            ReportBug.ReportBug()

    def apply(self):
        try:
            self.parent().createHistoryPoint()
            songs = []
            for tag in self.trueFiles:
                title = str(self.findChild(MComboBox, str("Value" + str(tag[1]))).currentText())
                songs.append([title, tag[1]])
            for tag in self.falseFiles:
                title = str(self.findChild(MComboBox, str("Value" + str(tag[1][1]))).currentText())
                songs.append([title, tag[1][1]])
            for tag in self.nullFiles:
                title = str(self.findChild(MComboBox, str("Value" + str(tag[1]))).currentText())
                songs.append([title, tag[1]])
            for tag in self.incorrectFiles:
                title = str(self.findChild(MComboBox, str("Value" + str(tag[1]))).currentText())
                songs.append([title, tag[1]])
            for song in songs:
                item = self.parent().item(song[1], 1)
                if str(item.text()) != song[0]:
                    item.setText(song[0])
            self.close()
        except:
            ReportBug.ReportBug()
