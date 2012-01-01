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


import Variables
from MyObjects import *
import Universals
import Dialogs
import InputOutputs
import Options
import Organizer

MyDialog, MyDialogType, MyParent = getMyDialog()

class Hasher(MyDialog):
    def __init__(self, _file=None):
        MyDialog.__init__(self, MyParent)
        if MyDialogType=="MDialog":
            if Universals.isActivePyKDE4==True:
                self.setButtons(MyDialog.NoDefault)
        elif MyDialogType=="MMainWindow":
            self.setObjectName("Hasher")
            Universals.MainWindow = self
        newOrChangedKeys = Universals.newSettingsKeys + Universals.changedDefaultValuesKeys
        wOptionsPanel = Options.Options(None, "hash", None, newOrChangedKeys)
        lblPathOfPackage = MLabel(translate("Hasher", "Path Of The File : "))
        lblHash = MLabel(translate("Hasher", "Hash Type : "))
        lblHashOutput = MLabel(translate("Hasher", "Hash Output : "))
        lblHashDigestFile = MLabel(translate("Hasher", "Hash Digest File : "))
        lblHashDigest = MLabel(translate("Hasher", "Hash Digest : "))
        self.teHashDigest = MTextEdit("")
        self.cbHash = MComboBox()
        self.cbHash.addItems(Variables.getHashTypes())
        self.cbHashOutput = MComboBox()
        self.cbHashOutput.addItems([translate("Hasher", "Only Show"), translate("Hasher", "File"), translate("Hasher", "Clipboard")])
        self.leHashDigestFile = MLineEdit(trForM(_file))
        self.pbtnHash = MPushButton(translate("Hasher", "Hash"))
        self.pbtnClose = MPushButton(translate("Hasher", "Close"))
        self.lePathOfPackage = MLineEdit(trForM(_file))
        self.pbtnHash.setToolTip(translate("Hasher", "Hash the selected file"))
        self.pbtnSelectProjectPath = MPushButton(translate("Hasher", "Browse"))
        self.pbtnSelectPackagePath = MPushButton(translate("Hasher", "Browse"))
        self.connect(self.pbtnSelectPackagePath,SIGNAL("clicked()"),self.selectPackagePath)
        self.connect(self.pbtnHash,SIGNAL("clicked()"),self.hash)
        self.connect(self.pbtnClose,SIGNAL("clicked()"),self.close)
        self.connect(self.cbHash,SIGNAL("currentIndexChanged(int)"),self.pathOfPackageChanged)
        self.connect(self.cbHashOutput,SIGNAL("currentIndexChanged(int)"),self.hashOutputChanged)
        self.connect(self.lePathOfPackage,SIGNAL("textChanged(const QString&)"),self.pathOfPackageChanged)
        self.teHashDigest.setMaximumHeight(80)
        pnlMain = MWidget(self)
        tabwTabs = MTabWidget()
        vblMain = MVBoxLayout(pnlMain)
        pnlMain2 = MWidget(tabwTabs)
        vblMain2 = MVBoxLayout(pnlMain2)
        HBox1 = MHBoxLayout()
        HBox1.addWidget(self.pbtnHash)
        HBox1.addWidget(self.pbtnClose)
        HBox2 = MHBoxLayout()
        HBox2.addWidget(self.lePathOfPackage)
        HBox2.addWidget(self.pbtnSelectPackagePath)
        HBox3 = MHBoxLayout()
        HBox3.addWidget(lblHashDigest)
        HBox3.addWidget(self.teHashDigest)
        HBox4 = MHBoxLayout()
        HBox4.addWidget(lblHash)
        HBox4.addWidget(self.cbHash)
        HBox5 = MHBoxLayout()
        HBox5.addWidget(lblHashOutput)
        HBox5.addWidget(self.cbHashOutput)
        HBox6 = MHBoxLayout()
        HBox6.addWidget(lblHashDigestFile)
        HBox6.addWidget(self.leHashDigestFile)
        vblMain2.addWidget(lblPathOfPackage)
        vblMain2.addLayout(HBox2)
        vblMain2.addLayout(HBox4)
        vblMain2.addLayout(HBox3)
        vblMain2.addLayout(HBox5)
        vblMain2.addLayout(HBox6)
        vblMain2.addStretch(1)
        vblMain2.addLayout(HBox1)
        tabwTabs.addTab(pnlMain2, translate("Hasher", "Hash"))
        tabwTabs.addTab(wOptionsPanel, translate("Hasher", "Quick Options"))
        vblMain.addWidget(tabwTabs)
        self.pathOfPackageChanged("")
        self.hashOutputChanged(self.cbHashOutput.currentIndex())
        if MyDialogType=="MDialog":
            if Universals.isActivePyKDE4==True:
                self.setMainWidget(pnlMain)
            else:
                self.setLayout(vblMain)
        elif MyDialogType=="MMainWindow":
            self.setCentralWidget(pnlMain)
            moveToCenter(self)
        self.setWindowTitle(translate("Hasher", "Hasher"))
        self.setWindowIcon(MIcon("Images:hash.png"))
        self.show()
                        
    def closeEvent(self, _event):
        MApplication.setQuitOnLastWindowClosed(True)
    
    def pathOfPackageChanged(self, _value):
        try:
            self.teHashDigest.setText("")
            packageExtension =  "." + str(self.cbHash.currentText()).lower()
            self.leHashDigestFile.setText(self.lePathOfPackage.text() + packageExtension)  
        except:
            import ReportBug
            error = ReportBug.ReportBug()
            error.show()  
    
    def hashOutputChanged(self, _value):
        if _value==1:
            self.leHashDigestFile.setEnabled(True)
        else:
            self.leHashDigestFile.setEnabled(False)
    
    def hash(self):
        sourceFile = str(self.lePathOfPackage.text())
        if InputOutputs.IA.checkSource(sourceFile, "file"):
            hashType = str(self.cbHash.currentText())
            if hashType!=None:
                hashDigestContent = InputOutputs.IA.getHashDigest(sourceFile, hashType)
                if hashDigestContent!=False:
                    self.teHashDigest.setText(trForM(hashDigestContent))
                    if self.cbHashOutput.currentIndex()==1:
                        if InputOutputs.IA.createHashDigestFile(sourceFile, str(self.leHashDigestFile.text()), hashType, False, hashDigestContent):
                            Dialogs.show(translate("Hasher", "Hash Digest File Created"),
                                        str(translate("Hasher", "Hash digest writed into %s")) % str(self.leHashDigestFile.text()))
                        else:
                            Dialogs.showError(translate("Hasher", "Hash Digest File Is Not Created"),
                                        translate("Hasher", "Hash digest file not cteated."))
                    elif self.cbHashOutput.currentIndex()==2:
                            MApplication.clipboard().setText(trForM(hashDigestContent))
                            Dialogs.show(translate("Hasher", "Hash Digest Copied To Clipboard"),
                                        str(translate("Hasher", "Hash digest copied to clipboard.Hash digest is : <br>%s")) % hashDigestContent)
                else:
                    Dialogs.showError(translate("Hasher", "Hash Digest Is Not Created"),
                                    translate("Hasher", "Hash digest not cteated."))
        
    def selectPackagePath(self):
        try:
            self.teHashDigest.setText("")
            PathOfPackage = MFileDialog.getOpenFileName(self,
                        translate("Hasher", "Please Select The Pack To Be Created"), self.lePathOfPackage.text(),
                        translate("Hasher", "All Files (*.*)"))
            if PathOfPackage!="":
                self.lePathOfPackage.setText(PathOfPackage)    
        except:
            import ReportBug
            error = ReportBug.ReportBug()
            error.show() 
    
    
                