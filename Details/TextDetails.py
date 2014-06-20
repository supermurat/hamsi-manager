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


import FileUtils as fu
from Core.MyObjects import *
from Core import Dialogs
from Core import Organizer
from Core import Universals as uni
from Core import ReportBug


class TextDetails(MDialog):
    global textDialogs
    textDialogs = []

    def __init__(self, _filePath, _isOpenDetailsOnNewWindow):
        global textDialogs
        _filePath = fu.checkSource(_filePath, "file")
        if _filePath is not None:
            if _isOpenDetailsOnNewWindow == False:
                isHasOpenedDialog = False
                for dialog in textDialogs:
                    if dialog.isVisible():
                        isHasOpenedDialog = True
                        self = dialog
                        self.changeFile(_filePath)
                        self.activateWindow()
                        self.raise_()
                        break
                if isHasOpenedDialog == False:
                    _isOpenDetailsOnNewWindow = True
            if _isOpenDetailsOnNewWindow:
                textDialogs.append(self)
                MDialog.__init__(self, MApplication.activeWindow())
                if isActivePyKDE4:
                    self.setButtons(MDialog.NoDefault)
                self.charSet = MComboBox()
                self.charSet.addItems(uni.getCharSets())
                self.charSet.setCurrentIndex(self.charSet.findText(uni.MySettings["fileSystemEncoding"]))
                self.infoLabels = {}
                self.infoValues = {}
                self.fileValues = {}
                pbtnClose = MPushButton(translate("TextDetails", "Close"))
                pbtnSave = MPushButton(translate("TextDetails", "Save Changes"))
                pbtnSave.setIcon(MIcon("Images:save.png"))
                MObject.connect(pbtnClose, SIGNAL("clicked()"), self.close)
                MObject.connect(pbtnSave, SIGNAL("clicked()"), self.save)
                self.labels = [translate("TextDetails", "File Path : "),
                               translate("TextDetails", "Content : ")]
                self.pnlMain = MWidget()
                self.vblMain = MVBoxLayout(self.pnlMain)
                self.pnlClearable = None
                self.changeFile(_filePath, True)
                HBOXs, VBOXs = [], []
                VBOXs.append(MVBoxLayout())
                HBOXs.append(MHBoxLayout())
                HBOXs[-1].addWidget(self.charSet, 1)
                HBOXs[-1].addWidget(pbtnSave, 4)
                VBOXs[0].addLayout(HBOXs[-1])
                VBOXs[0].addWidget(pbtnClose)
                self.vblMain.addLayout(VBOXs[0], 1)
                if isActivePyKDE4:
                    self.setMainWidget(self.pnlMain)
                else:
                    self.setLayout(self.vblMain)
                self.show()
                self.setMinimumWidth(700)
                self.setMinimumHeight(500)
        else:
            Dialogs.showError(translate("TextDetails", "File Does Not Exist"),
                              str(translate("TextDetails",
                                            "\"%s\" does not exist.<br>Table will be refreshed automatically!<br>Please retry.")
                              ) % Organizer.getLink(str(_filePath)))
            if hasattr(getMainWindow(),
                       "FileManager") and getMainWindow().FileManager is not None: getMainWindow().FileManager.makeRefresh()

    def changeFile(self, _filePath, _isNew=False):
        self.fileValues = fu.readTextFile(_filePath, uni.MySettings["fileSystemEncoding"])
        self.setWindowTitle(str(fu.getBaseName(self.fileValues["path"])))
        if self.pnlClearable != None:
            clearAllChildren(self.pnlClearable, True)
        self.pnlClearable = MWidget()
        self.vblMain.insertWidget(0, self.pnlClearable, 20)
        vblClearable = MVBoxLayout(self.pnlClearable)
        self.infoLabels["path"] = MLabel(self.labels[0])
        self.infoLabels["content"] = MLabel(self.labels[1])
        dirPath = fu.getDirName(self.fileValues["path"])
        baseName = fu.getBaseName(self.fileValues["path"])
        self.infoValues["path"] = MLineEdit(str(fu.joinPath(dirPath, Organizer.emend(baseName, "file"))))
        self.infoValues["content"] = MPlainTextEdit(
            str(Organizer.emend(self.fileValues["content"], "text", False, True)))
        self.infoValues["content"].setLineWrapMode(MPlainTextEdit.NoWrap)
        self.sourceCharSet = MComboBox()
        self.sourceCharSet.addItems(uni.getCharSets())
        self.sourceCharSet.setCurrentIndex(self.sourceCharSet.findText(uni.MySettings["fileSystemEncoding"]))
        MObject.connect(self.sourceCharSet, SIGNAL("currentIndexChanged(int)"), self.sourceCharSetChanged)
        HBOXs = []
        HBOXs.append(MHBoxLayout())
        HBOXs[-1].addWidget(self.infoLabels["path"])
        HBOXs[-1].addWidget(self.infoValues["path"])
        HBOXs[-1].addWidget(self.sourceCharSet)
        for hbox in HBOXs:
            vblClearable.addLayout(hbox)
        vblClearable.addWidget(self.infoLabels["content"])
        vblClearable.addWidget(self.infoValues["content"])

    def sourceCharSetChanged(self):
        try:
            self.fileValues = fu.readTextFile(self.fileValues["path"], str(self.sourceCharSet.currentText()))
            self.infoValues["content"].setPlainText(
                str(Organizer.emend(self.fileValues["content"], "text", False, True)))
        except:
            Dialogs.showError(translate("TextDetails", "Incorrect File Encoding"),
                              str(translate("TextDetails",
                                            "File can not decode by \"%s\" codec.<br>Please select another file encoding type.")
                              ) % str(self.sourceCharSet.currentText()))

    @staticmethod
    def closeAllTextDialogs():
        for dialog in textDialogs:
            try:
                if dialog.isVisible():
                    dialog.close()
            except:
                continue

    def save(self):
        try:
            from Core import Records

            Records.setTitle(translate("TextDetails", "Text File"))
            newFileValues = {}
            newFileValues["path"] = str(self.infoValues["path"].text())
            newFileValues["content"] = str(self.infoValues["content"].toPlainText())
            newPath = fu.writeTextFile(self.fileValues, newFileValues, str(self.charSet.currentText()))
            if newPath != self.fileValues["path"]:
                self.changeFile(newPath)
            if hasattr(getMainWindow(),
                       "FileManager") and getMainWindow().FileManager is not None: getMainWindow().FileManager.makeRefresh()
            Records.saveAllRecords()
        except:
            ReportBug.ReportBug()
    
