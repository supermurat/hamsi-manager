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


from Core import Variables
import InputOutputs
from Core.MyObjects import *
from Core import Dialogs
from Core import Organizer
from Core import Universals
from Core import ReportBug
import Options
from Options import OptionsForm

MyDialog, MyDialogType, MyParent = getMyDialog()

class TextCorrector(MyDialog):
    
    def __init__(self,_filePath):
        MyDialog.__init__(self, MyParent)
        if MyDialogType=="MDialog":
            if Universals.isActivePyKDE4==True:
                self.setButtons(MyDialog.NoDefault)
        elif MyDialogType=="MMainWindow":
            self.setObjectName("Cleaner")
            Universals.setMainWindow(self)
        newOrChangedKeys = Universals.newSettingsKeys + Universals.changedDefaultValuesKeys
        wOptionsPanel = OptionsForm.OptionsForm(None, "textCorrector", None, newOrChangedKeys)
        self.setWindowTitle(translate("TextCorrector", "Text Corrector")) 
        self.fileValues = None
        self.isChangeSourceCharSetChanged = False
        self.charSet = MComboBox()
        self.charSet.addItems(Variables.getCharSets())
        self.charSet.setCurrentIndex(self.charSet.findText(Universals.MySettings["fileSystemEncoding"]))
        self.sourceCharSet = MComboBox()
        self.sourceCharSet.addItems(Variables.getCharSets())
        self.sourceCharSet.setCurrentIndex(self.sourceCharSet.findText(Universals.MySettings["fileSystemEncoding"]))
        self.pbtnSelectFilePath = MPushButton(translate("TextCorrector", "Browse"))
        self.connect(self.pbtnSelectFilePath,SIGNAL("clicked()"), self.selectFilePath)
        pbtnClose = MPushButton(translate("TextCorrector", "Close"))
        self.pbtnSave = MPushButton(translate("TextCorrector", "Save Changes"))
        self.pbtnSave.setIcon(MIcon("Images:save.png"))
        MObject.connect(pbtnClose, SIGNAL("clicked()"), self.close)
        MObject.connect(self.pbtnSave, SIGNAL("clicked()"), self.save)
        self.labels = [translate("TextCorrector", "File Path : "), 
                            translate("TextCorrector", "Content : ")]
        pnlMain = MWidget(self)
        tabwTabs = MTabWidget()
        pnlMain2 = MWidget(tabwTabs)
        vblMain2 = MVBoxLayout(pnlMain2)
        vblMain = MVBoxLayout(pnlMain)
        self.lblFilePath = MLabel(self.labels[0]) 
        self.lblFileContent = MLabel(self.labels[1])
        self.leFilePath = MLineEdit(trForUI(_filePath))
        self.pteFileContent = MPlainTextEdit(trForUI(""))
        self.pteFileContent.setLineWrapMode(MPlainTextEdit.NoWrap)
        self.fillValues()
        MObject.connect(self.sourceCharSet, SIGNAL("currentIndexChanged(int)"), self.sourceCharSetChanged)
        self.isChangeSourceCharSetChanged = True
        hbFilePath = MHBoxLayout()
        hbFilePath.addWidget(self.lblFilePath)
        hbFilePath.addWidget(self.leFilePath)
        hbFilePath.addWidget(self.pbtnSelectFilePath)
        hbFilePath.addWidget(self.sourceCharSet)
        vblMain2.addLayout(hbFilePath)
        vblMain2.addWidget(self.lblFileContent)
        vblMain2.addWidget(self.pteFileContent)
        hbControls = MHBoxLayout()
        hbControls.addWidget(self.charSet, 1)
        hbControls.addWidget(self.pbtnSave, 4)
        hbControls.addWidget(pbtnClose, 1)
        vblMain2.addLayout(hbControls, 1)
        self.leFilePath.setEnabled(False)
        tabwTabs.addTab(pnlMain2, translate("Searcher", "Search"))
        tabwTabs.addTab(wOptionsPanel, translate("Searcher", "Quick Options"))
        vblMain.addWidget(tabwTabs)
        if MyDialogType=="MDialog":
            if Universals.isActivePyKDE4==True:
                self.setMainWidget(pnlMain)
            else:
                self.setLayout(vblMain)
        elif MyDialogType=="MMainWindow":
            self.setCentralWidget(pnlMain)
            moveToCenter(self)
        self.show()
        self.setMinimumWidth(700)
        self.setMinimumHeight(500)
                        
    def closeEvent(self, _event):
        MApplication.setQuitOnLastWindowClosed(True)
        
    def fillValues(self):
        filePath = str(self.leFilePath.text())
        if InputOutputs.isFile(filePath) and InputOutputs.isReadableFileOrDir(filePath):
            
            self.fileValues = InputOutputs.readTextFile(filePath, str(self.sourceCharSet.currentText()))
            self.pteFileContent.setPlainText(trForUI(Organizer.emend(self.fileValues["content"], "text", False, True)))
            self.isChangeSourceCharSetChanged = True
            self.pbtnSave.setEnabled(True)
        else:
            self.isChangeSourceCharSetChanged = False
            self.pbtnSave.setEnabled(False)
            
    def sourceCharSetChanged(self):
        try:
            if self.isChangeSourceCharSetChanged:
                self.fillValues()
        except:
            self.pbtnSave.setEnabled(False)
            Dialogs.showError(translate("TextCorrector", "Incorrect File Encoding"), 
                        str(translate("TextCorrector", "File can not decode by \"%s\" codec.<br>Please select another file encoding type.")
                            )% trForUI(self.sourceCharSet.currentText()))

    def selectFilePath(self):
        try:
            filePath = QFileDialog.getOpenFileName(self,
                        translate("TextCorrector", "Please Select A Text File To Correct"), self.leFilePath.text(),
                        translate("TextCorrector", "All Files (*)"))
            if filePath!="":
                self.leFilePath.setText(filePath)
                self.isChangeSourceCharSetChanged = False
                self.sourceCharSet.setCurrentIndex(self.sourceCharSet.findText(Universals.MySettings["fileSystemEncoding"]))
                self.fillValues()
        except:
            error = ReportBug.ReportBug()
            error.show() 
        
    def save(self):
        try:
            filePath = str(self.leFilePath.text())
            if self.fileValues!=None:
                from Core import Records
                Records.setTitle(translate("TextCorrector", "Text File"))
                newFileValues = {}
                newFileValues["path"] = filePath
                newFileValues["content"] = str(self.pteFileContent.toPlainText())
                newPath = InputOutputs.writeTextFile(self.fileValues, newFileValues, str(self.charSet.currentText()))
                if newPath!=self.fileValues["path"]:
                    self.changeFile(newPath)
                if hasattr(Universals.MainWindow, "FileManager") and Universals.MainWindow.FileManager is not None: Universals.MainWindow.FileManager.makeRefresh()
                Records.saveAllRecords()
            else:
                Dialogs.showError(translate("TextCorrector", "File Does Not Exist"), 
                        str(translate("TextDetails", "\"%s\" does not exist.<br>Please select an exist file and try again.")
                            )% Organizer.getLink(trForUI(filePath)))
        except:
            error = ReportBug.ReportBug()
            error.show()  
    