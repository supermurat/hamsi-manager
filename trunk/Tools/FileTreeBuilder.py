# -*- coding: utf-8 -*-
## This file is part of HamsiManager.
## 
## Copyright (c) 2010 Murat Demir <mopened@gmail.com>      
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


from MyObjects import *
import Universals
import Dialogs
import InputOutputs
import Options

MyDialog, MyDialogType, MyParent = getMyDialog()

class FileTreeBuilder(MyDialog):
    def __init__(self, _directory):
        MyDialog.__init__(self, MyParent)
        if MyDialogType=="MDialog":
            if Universals.isActivePyKDE4==True:
                self.setButtons(MyDialog.None)
        elif MyDialogType=="MMainWindow":
            self.setObjectName("Packager")
            Universals.MainWindow = self
        newOrChangedKeys = Universals.newSettingsKeys + Universals.changedDefaultValuesKeys
        wOptionsPanel = Options.Options(None, "fileTree", None, newOrChangedKeys)
        lblDirectory = MLabel(translate("FileTreeBuilder", "Directory : "))
        lblOutputType = MLabel(translate("FileTreeBuilder", "Output Type : "))
        lblContentType = MLabel(translate("FileTreeBuilder", "Content Type : "))
        lblSubDirectoryDeepDetails = translate("FileTreeBuilder", "You can select sub directory deep.<br><font color=blue>You can select \"-1\" for all sub directories.</font>")
        lblSubDirectoryDeep = MLabel(translate("FileTreeBuilder", "Deep : "))
        self.cbSubDirectoryDeep = MComboBox(self)
        for x in range(-1, 10):
            self.cbSubDirectoryDeep.addItem(str(x))
        self.cbSubDirectoryDeep.setCurrentIndex(self.cbSubDirectoryDeep.findText(Universals.MySettings["subDirectoryDeep"]))
        self.cbSubDirectoryDeep.setToolTip(lblSubDirectoryDeepDetails)
        self.cbContentType = MComboBox()
        self.cbContentType.addItems([translate("FileTreeBuilder", "HTML"),
                                    translate("FileTreeBuilder", "Plain Text")])
        self.cbOutputType = MComboBox()
        self.cbOutputType.addItems([translate("FileTreeBuilder", "File"),
                                    translate("FileTreeBuilder", "Dialog"),
                                    translate("FileTreeBuilder", "Clipboard")])
        self.cbOutputType.setCurrentIndex(1)
        pbtnBuild = MPushButton(translate("FileTreeBuilder", "Build"))
        pbtnClose = MPushButton(translate("FileTreeBuilder", "Close"))
        self.lePath = MLineEdit(_directory.decode("utf-8"))
        pbtnSelectPath = MPushButton(translate("FileTreeBuilder", "Browse"))
        self.connect(pbtnSelectPath,SIGNAL("clicked()"),self.selectPath)
        self.connect(pbtnBuild,SIGNAL("clicked()"), self.build)
        self.connect(pbtnClose,SIGNAL("clicked()"),self.close)
        pnlMain = MWidget(self)
        tabwTabs = MTabWidget()
        vblMain = MVBoxLayout(pnlMain)
        pnlMain2 = MWidget(tabwTabs)
        vblMain2 = MVBoxLayout(pnlMain2)
        HBox = MHBoxLayout()
        HBox.addWidget(self.lePath)
        HBox.addWidget(pbtnSelectPath)
        HBox1 = MHBoxLayout()
        HBox1.addWidget(pbtnBuild)
        HBox1.addWidget(pbtnClose)
        HBox2 = MHBoxLayout()
        HBox2.addWidget(lblOutputType)
        HBox2.addWidget(self.cbOutputType)
        HBox3 = MHBoxLayout()
        HBox3.addWidget(lblContentType)
        HBox3.addWidget(self.cbContentType)
        HBox4 = MHBoxLayout()
        HBox4.addWidget(lblSubDirectoryDeep)
        HBox4.addWidget(self.cbSubDirectoryDeep)
        vblMain2.addWidget(lblDirectory)
        vblMain2.addLayout(HBox)
        vblMain2.addLayout(HBox2)
        vblMain2.addLayout(HBox3)
        vblMain2.addLayout(HBox4)
        vblMain2.addStretch(1)
        vblMain2.addLayout(HBox1)
        tabwTabs.addTab(pnlMain2, translate("FileTreeBuilder", "File Tree"))
        tabwTabs.addTab(wOptionsPanel, translate("FileTreeBuilder", "Quick Options"))
        vblMain.addWidget(tabwTabs)
        if MyDialogType=="MDialog":
            if Universals.isActivePyKDE4==True:
                self.setMainWidget(pnlMain)
            else:
                self.setLayout(vblMain)
        elif MyDialogType=="MMainWindow":
            self.setCentralWidget(pnlMain)
            moveToCenter(self)
        self.setWindowTitle(translate("FileTreeBuilder", "File Tree Builder"))
        self.setWindowIcon(MIcon("Images:fileTree.png"))
        self.setMinimumWidth(450)
        self.show()
                        
    def closeEvent(self, _event):
        MApplication.setQuitOnLastWindowClosed(True)
    
    def build(self):
        try:
            Universals.isCanBeShowOnMainWindow = False
            outputType = "file"
            contentType = "html"
            if self.cbOutputType.currentIndex()==1:
                outputType = "dialog"
            elif self.cbOutputType.currentIndex()==2:
                outputType = "clipboard"
            if self.cbContentType.currentIndex()==1:
                contentType = "plainText"
            InputOutputs.IA.getFileTree(unicode(self.lePath.text(), "utf-8"), 
                                self.cbSubDirectoryDeep.currentText(), 
                                outputType, contentType, "title")
            if self.cbOutputType.currentIndex()==2:
                Dialogs.show(translate("FileTreeBuilder", "Builded File Tree"),
                            translate("FileTreeBuilder", "File tree copied to clipboard."))
            Universals.isCanBeShowOnMainWindow = True
        except:
            import ReportBug
            error = ReportBug.ReportBug()
            error.show()   
    
    def selectPath(self):
        try:
            dirPath = MFileDialog.getExistingDirectory(self,
                            translate("FileTreeBuilder", "Please Select"),self.lePath.text())
            if dirPath!="":
                self.lePath.setText(dirPath)
        except:
            import ReportBug
            error = ReportBug.ReportBug()
            error.show() 
    
    
                