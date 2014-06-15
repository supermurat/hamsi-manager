## This file is part of HamsiManager.
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


from Core import Variables
from Core.MyObjects import *
from Core import Universals
from Core import Dialogs
import FileUtils as fu
import Options
from Options import OptionsForm
from Core import Organizer
from Core import ReportBug

MyDialog, MyDialogType, MyParent = getMyDialog()

class Packager(MyDialog):
    def __init__(self, _directory):
        MyDialog.__init__(self, MyParent)
        if MyDialogType=="MDialog":
            if isActivePyKDE4:
                self.setButtons(MyDialog.NoDefault)
        elif MyDialogType=="MMainWindow":
            self.setObjectName("Packager")
            Universals.setMainWindow(self)
        newOrChangedKeys = Universals.newSettingsKeys + Universals.changedDefaultValuesKeys
        wOptionsPanel = OptionsForm.OptionsForm(None, "pack", None, newOrChangedKeys)
        lblPleaseSelect = MLabel(translate("Packager", "Path Of The Directory"))
        lblPathOfPackage = MLabel(translate("Packager", "Path Of The Pack"))
        lblPackageType = MLabel(translate("Packager", "Package Compression Type : "))
        lblHash = MLabel(translate("Packager", "Hash : "))
        lblHashOutput = MLabel(translate("Packager", "Hash Output : "))
        lblHashDigestFile = MLabel(translate("Packager", "Hash Digest File : "))
        self.cbPackageType = Options.MyComboBox(self, 
                                    [translate("Packager", "Archive Without Compression"), ".tar.gz", ".tar.bz2", ".amarokscript.tar.gz"], 
                                    1, "PackagerPackageType", self.packageTypeChanged)
        self.cbHash = Options.MyComboBox(self, [translate("Packager", "No Hash")] + Variables.getHashTypes(), 0, "PackagerHash", self.hashChanged)
        self.cbHashOutput = Options.MyComboBox(self, [translate("Packager", "File"), translate("Packager", "Clipboard")], 0, "PackagerHashOutput", self.hashOutputChanged)
        self.leHashDigestFile = MLineEdit(trForUI(_directory))
        self.pbtnClearAndPack = MPushButton(translate("Packager", "Clear And Pack"))
        self.pbtnClear = MPushButton(translate("Packager", "Clear"))
        self.pbtnPack = MPushButton(translate("Packager", "Pack"))
        self.pbtnClose = MPushButton(translate("Packager", "Close"))
        self.lePathOfProject = MLineEdit(trForUI(_directory))
        self.lePathOfPackage = MLineEdit(trForUI(_directory))
        self.pbtnClearAndPack.setToolTip(translate("Packager", "Do not will cleared directory you selected but unnecessary files and directories package will not."))
        self.pbtnClear.setToolTip(translate("Packager", "Directory you selected will is cleared"))
        self.pbtnPack.setToolTip(translate("Packager", "Directory you selected will is packed. (Do not will Cleared)"))
        self.packageTypeChanged()
        self.pbtnSelectProjectPath = MPushButton(translate("Packager", "Browse"))
        self.pbtnSelectPackagePath = MPushButton(translate("Packager", "Browse"))
        self.connect(self.pbtnSelectProjectPath,SIGNAL("clicked()"),self.selectProjectPath)
        self.connect(self.pbtnSelectPackagePath,SIGNAL("clicked()"),self.selectPackagePath)
        self.connect(self.pbtnClearAndPack,SIGNAL("clicked()"),self.ClearAndPack)
        self.connect(self.pbtnClear,SIGNAL("clicked()"),self.Clear)
        self.connect(self.pbtnPack,SIGNAL("clicked()"),self.Pack)
        self.connect(self.pbtnClose,SIGNAL("clicked()"),self.close)
        self.connect(self.lePathOfProject,SIGNAL("textChanged(const QString&)"),self.pathOfProjectChanged)
        self.connect(self.lePathOfPackage,SIGNAL("textChanged(const QString&)"),self.pathOfPackageChanged)
        pnlMain = MWidget(self)
        tabwTabs = MTabWidget()
        vblMain = MVBoxLayout(pnlMain)
        pnlMain2 = MWidget(tabwTabs)
        vblMain2 = MVBoxLayout(pnlMain2)
        HBox = MHBoxLayout()
        HBox.addWidget(self.lePathOfProject)
        HBox.addWidget(self.pbtnSelectProjectPath)
        HBox1 = MHBoxLayout()
        HBox1.addWidget(self.pbtnClear)
        HBox1.addWidget(self.pbtnPack)
        HBox1.addWidget(self.pbtnClearAndPack)
        HBox1.addWidget(self.pbtnClose)
        HBox2 = MHBoxLayout()
        HBox2.addWidget(self.lePathOfPackage)
        HBox2.addWidget(self.pbtnSelectPackagePath)
        HBox3 = MHBoxLayout()
        HBox3.addWidget(lblPackageType)
        HBox3.addWidget(self.cbPackageType)
        HBox4 = MHBoxLayout()
        HBox4.addWidget(lblHash)
        HBox4.addWidget(self.cbHash)
        HBox5 = MHBoxLayout()
        HBox5.addWidget(lblHashOutput)
        HBox5.addWidget(self.cbHashOutput)
        HBox6 = MHBoxLayout()
        HBox6.addWidget(lblHashDigestFile)
        HBox6.addWidget(self.leHashDigestFile)
        vblMain2.addWidget(lblPleaseSelect)
        vblMain2.addLayout(HBox)
        vblMain2.addWidget(lblPathOfPackage)
        vblMain2.addLayout(HBox2)
        vblMain2.addLayout(HBox3)
        vblMain2.addLayout(HBox4)
        vblMain2.addLayout(HBox5)
        vblMain2.addLayout(HBox6)
        vblMain2.addStretch(1)
        vblMain2.addLayout(HBox1)
        tabwTabs.addTab(pnlMain2, translate("Packager", "Pack"))
        tabwTabs.addTab(wOptionsPanel, translate("Packager", "Quick Options"))
        vblMain.addWidget(tabwTabs)
        self.hashChanged(self.cbHash.currentIndex())
        if MyDialogType=="MDialog":
            if isActivePyKDE4:
                self.setMainWidget(pnlMain)
            else:
                self.setLayout(vblMain)
        elif MyDialogType=="MMainWindow":
            self.setCentralWidget(pnlMain)
            moveToCenter(self)
        self.setWindowTitle(translate("Packager", "Packager"))
        self.setWindowIcon(MIcon("Images:pack.png"))
        self.show()
                        
    def closeEvent(self, _event):
        MApplication.setQuitOnLastWindowClosed(True)
    
    def pathOfProjectChanged(self, _value):
        try:
            if self.cbPackageType.currentIndex()!=0:
                packageExtension = self.cbPackageType.currentText()
            else:
                packageExtension = ".tar"   
            self.lePathOfPackage.setText(self.lePathOfProject.text()+packageExtension)  
        except:
            ReportBug.ReportBug()
    
    def pathOfPackageChanged(self, _value):
        try:
            if self.cbHash.currentIndex()==0:
                packageExtension = "~"
            else:
                packageExtension =  "." + str(self.cbHash.currentText()).lower()
            self.leHashDigestFile.setText(self.lePathOfPackage.text()+packageExtension)  
        except:
            ReportBug.ReportBug()
    
    def hashChanged(self, _value):
        if _value==0:
            self.cbHashOutput.setEnabled(False)
            self.leHashDigestFile.setEnabled(False)
        else:
            self.cbHashOutput.setEnabled(True)
            self.hashOutputChanged(self.cbHashOutput.currentIndex())
        self.pathOfPackageChanged("")
    
    def hashOutputChanged(self, _value):
        if _value==0:
            self.leHashDigestFile.setEnabled(True)
        else:
            self.leHashDigestFile.setEnabled(False)
    
    def createHashDigest(self):
        if self.cbHash.currentIndex()==0:
            hashType = None
        else:
            hashType =  str(self.cbHash.currentText())
        if hashType!=None:
            if self.cbHashOutput.currentIndex()==0:
                if fu.createHashDigestFile(str(self.lePathOfPackage.text()), str(self.leHashDigestFile.text()), hashType, False):
                    Dialogs.show(translate("Packager", "Hash Digest File Created"),
                                str(translate("Packager", "Hash digest writed into %s")) % str(self.leHashDigestFile.text()))
                else:
                    Dialogs.showError(translate("Packager", "Hash Digest File Is Not Created"),
                                translate("Packager", "Hash digest file not cteated."))
            else:
                hashDigestContent = fu.getHashDigest(str(self.lePathOfPackage.text()), hashType)
                if hashDigestContent!=False:
                    MApplication.clipboard().setText(trForUI(hashDigestContent))
                    Dialogs.show(translate("Packager", "Hash Digest Copied To Clipboard"),
                                str(translate("Packager", "Hash digest copied to clipboard.Hash digest is : <br>%s")) % hashDigestContent)
                else:
                    Dialogs.showError(translate("Packager", "Hash Digest Is Not Created"),
                                translate("Packager", "Hash digest not cteated."))
                    
    
    def ClearAndPack(self):
        try:
            Universals.isCanBeShowOnMainWindow = False
            import random
            tempDir = fu.joinPath(fu.getTempDir(), "HamsiManager-" + str(random.randrange(0, 1000000)))
            pathOfProject = str(self.lePathOfProject.text())
            pathOfTempSource = fu.joinPath(tempDir, fu.getBaseName(pathOfProject))
            fu.copyFileOrDir(pathOfProject, pathOfTempSource)
            fu.clearPackagingDirectory(tempDir, True, True)
            if fu.makePack(str(self.lePathOfPackage.text()), self.getPackageType(), pathOfTempSource, fu.getBaseName(pathOfProject)):
                fu.removeFileOrDir(tempDir)
                self.createHashDigest()
                Dialogs.show(translate("Packager", "Project Is Packed"),
                            translate("Packager", "You can now start sharing it."))
            if Universals.getBoolValue("isCloseOnCleanAndPackage"):
                self.close()
            Universals.isCanBeShowOnMainWindow = True
        except:
            ReportBug.ReportBug()
    
    def Clear(self):
        try:
            Universals.isCanBeShowOnMainWindow = False
            answer = Dialogs.ask(translate("Packager", "Your Files Will Be Removed"),
                    str(translate("Packager", "The files in the \"%s\" folder will be cleared according to the criteria you set.<br>"+
                    "This action will delete the files completely, without any chance to recover.<br>"+
                    "Are you sure you want to perform the action?")) % Organizer.getLink(str(self.lePathOfProject.text())))
            if answer==Dialogs.Yes:
                if fu.isWritableFileOrDir(str(self.lePathOfProject.text())):
                    if fu.clearPackagingDirectory(str(self.lePathOfProject.text()), True, True):
                        Dialogs.show(translate("Packager", "Project Is Cleared"),
                                    translate("Packager", "You can now pack your project."))
            Universals.isCanBeShowOnMainWindow = True
        except:
            ReportBug.ReportBug()
    
    def Pack(self):
        try:
            Universals.isCanBeShowOnMainWindow = False
            if fu.makePack(str(self.lePathOfPackage.text()),
                                self.getPackageType(), str(self.lePathOfProject.text()), fu.getBaseName(self.lePathOfProject.text())):
                self.createHashDigest()
                Dialogs.show(translate("Packager", "Project Is Packed"),
                            translate("Packager", "You can now share your project."))
            Universals.isCanBeShowOnMainWindow = True
        except:
            ReportBug.ReportBug()
    
    def getPackageType(self):
        if self.cbPackageType.currentIndex()!=0:
            return str(self.cbPackageType.currentText()).split(".")[-1]
        else:
            return ""
    
    def selectProjectPath(self):
        try:
            self.cbPackageType.setEnabled(True)
            ProjectPath = Dialogs.getExistingDirectory(translate("Packager", "Please Select Project Folder"),self.lePathOfProject.text())
            if ProjectPath is not None:
                self.lePathOfProject.setText(trForUI(ProjectPath))  
            self.packageTypeChanged()
        except:
            ReportBug.ReportBug()
        
    def packageTypeChanged(self):
        try:
            packageName = self.lePathOfPackage.text()
            if packageName[-4:]==".tar":
                packageName = packageName[:-4]
            elif packageName[-20:]==".amarokscript.tar.gz":
                packageName = packageName[:-20]
            elif packageName[-7:]==".tar.gz":
                packageName = packageName[:-7]
            elif packageName[-8:]==".tar.bz2":
                packageName = packageName[:-8]
            if self.cbPackageType.currentIndex()!=0:
                packageExtension = self.cbPackageType.currentText()
            else:
                packageExtension = ".tar"   
            self.lePathOfPackage.setText(packageName+packageExtension)  
        except:
            ReportBug.ReportBug()
        
    def selectPackagePath(self):
        try:
            if self.cbPackageType.currentIndex()!=0:
                packageExtension = self.cbPackageType.currentText()
            else:
                packageExtension = ".tar"   
            PathOfPackage = Dialogs.getSaveFileName(translate("Packager", "Please Select The Pack To Be Created"),self.lePathOfPackage.text(),
                        str(translate("Packager", "Archive Files (*%s)")) % (packageExtension), 2)
            if PathOfPackage is not None:
                self.lePathOfPackage.setText(trForUI(PathOfPackage))    
        except:
            ReportBug.ReportBug()
    
    
                
