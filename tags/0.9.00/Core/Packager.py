# -*- coding: utf-8 -*-

from MyObjects import *
import Universals
import Dialogs
import InputOutputs
import Options
import Organizer

MyDialog, MyDialogType, MyParent = getMyDialog()

class Packager(MyDialog):
    def __init__(self, _directory):
        MyDialog.__init__(self, MyParent)
        if MyDialogType=="MDialog":
            if Universals.isActivePyKDE4==True:
                self.setButtons(MyDialog.None)
        elif MyDialogType=="MMainWindow":
            self.setObjectName("Packager")
            Universals.MainWindow = self
        newOrChangedKeys = Universals.newSettingsKeys + Universals.changedDefaultValuesKeys
        wOptionsPanel = Options.Options(None, "pack", None, newOrChangedKeys)
        lblPleaseSelect = MLabel(translate("Packager", "<font color=red><b>Project Folder</b></font>"))
        lblPathOfPackage = MLabel(translate("Packager", "<b>Path Of The Pack</b>"))
        lblPackageType = MLabel(translate("Packager", "<b>Package Compression Type : </b>"))
        lblHash = MLabel(translate("Packager", "<b>Hash : </b>"))
        lblHashOutput = MLabel(translate("Packager", "<b>Hash Output : </b>"))
        lblHashDigestFile = MLabel(translate("Packager", "<b>Hash Digest File : </b>"))
        self.cbPackageType = MComboBox()
        self.cbPackageType.addItems([translate("Packager", "Archive Without Compression"),
                                    u".tar.gz",u".tar.bz2", ".amarokscript.tar.gz"])
        self.cbPackageType.setCurrentIndex(1)
        self.cbHash = MComboBox()
        self.cbHash.addItems([translate("Packager", "No Hash")] + InputOutputs.getHashTypes())
        self.cbHashOutput = MComboBox()
        self.cbHashOutput.addItems([translate("Packager", "File"), translate("Packager", "Clipboard")])
        self.leHashDigestFile = MLineEdit(_directory.decode("utf-8"))
        self.pbtnClearAndPack = MPushButton(translate("Packager", "Clear And Pack"))
        self.pbtnClear = MPushButton(translate("Packager", "Clear"))
        self.pbtnPack = MPushButton(translate("Packager", "Pack"))
        self.pbtnClose = MPushButton(translate("Packager", "Close"))
        self.lePathOfProject = MLineEdit(_directory.decode("utf-8"))
        self.lePathOfPackage = MLineEdit(_directory.decode("utf-8"))
        self.pbtnClearAndPack.setToolTip(translate("Packager", "Do not will cleared directory you selected but unnecessary files and directories package will not."))
        self.pbtnClear.setToolTip(translate("Packager", "Directory you selected will is cleared"))
        self.pbtnPack.setToolTip(translate("Packager", "Directory you selected will is packed. (Do not will Cleared)"))
        self.packageTypeChanged()
        self.pbtnSelectProjectPath = MPushButton(translate("Packager", "Browse"))
        self.pbtnSelectPackagePath = MPushButton(translate("Packager", "Browse"))
        self.connect(self.cbPackageType, SIGNAL("currentIndexChanged(int)"), self.packageTypeChanged)
        self.connect(self.pbtnSelectProjectPath,SIGNAL("clicked()"),self.selectProjectPath)
        self.connect(self.pbtnSelectPackagePath,SIGNAL("clicked()"),self.selectPackagePath)
        self.connect(self.pbtnClearAndPack,SIGNAL("clicked()"),self.ClearAndPack)
        self.connect(self.pbtnClear,SIGNAL("clicked()"),self.Clear)
        self.connect(self.pbtnPack,SIGNAL("clicked()"),self.Pack)
        self.connect(self.pbtnClose,SIGNAL("clicked()"),self.close)
        self.connect(self.cbHash,SIGNAL("currentIndexChanged(int)"),self.hashChanged)
        self.connect(self.cbHashOutput,SIGNAL("currentIndexChanged(int)"),self.hashOutputChanged)
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
            if Universals.isActivePyKDE4==True:
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
            import ReportBug
            error = ReportBug.ReportBug()
            error.show()  
    
    def pathOfPackageChanged(self, _value):
        try:
            if self.cbHash.currentIndex()==0:
                packageExtension = "~"
            else:
                packageExtension =  "." + str(self.cbHash.currentText()).lower()
            self.leHashDigestFile.setText(self.lePathOfPackage.text()+packageExtension)  
        except:
            import ReportBug
            error = ReportBug.ReportBug()
            error.show()  
    
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
            hashType =  "." + str(self.cbHash.currentText())
        hashType = None
        if hashType!=None:
            if self.cbHashOutput.currentIndex()==0:
                if InputOutputs.createHashDigestFile(unicode(self.lePathOfPackage.text(), "utf-8"), unicode(self.leHashDigestFile.text(), "utf-8"), hashType, False):
                    Dialogs.show(translate("Packager", "Hash Digest File Created"),
                                str(translate("Packager", "Hash digest writed into %s")) % unicode(self.leHashDigestFile.text(), "utf-8"))
                else:
                    Dialogs.showError(translate("Packager", "Hash Digest File Is Not Created"),
                                translate("Packager", "Hash digest file not cteated."))
            else:
                hashDigestContent = InputOutputs.getHashDigest(unicode(self.lePathOfPackage.text(), "utf-8"), hashType)
                if hashDigestContent!=False:
                    MApplication.clipboard().setText(hashDigestContent.decode("utf-8"))
                    Dialogs.show(translate("Packager", "Hash Digest Copied To Clipboard"),
                                str(translate("Packager", "Hash digest copied to clipboard.Hash digest is : <br>%s")) % hashDigestContent)
                else:
                    Dialogs.showError(translate("Packager", "Hash Digest Is Not Created"),
                                translate("Packager", "Hash digest not cteated."))
                    
    
    def ClearAndPack(self):
        try:
            Universals.isCanBeShowOnMainWindow = False
            import tempfile, random
            tempDir = tempfile.gettempdir() + "/HamsiManager-" + str(random.randrange(0, 1000000))
            PathOfProject = unicode(self.lePathOfProject.text(), "utf-8")
            InputOutputs.copyFileOrDir(PathOfProject, tempDir+"/"+InputOutputs.getBaseName(PathOfProject))
            InputOutputs.clearPackagingDirectory(tempDir, True, True)
            if InputOutputs.makePack(unicode(self.lePathOfPackage.text(), "utf-8"), self.getPackageType(), tempDir):
                InputOutputs.removeFileOrDir(tempDir, True)
                self.createHashDigest()
                Dialogs.show(translate("Packager", "Project Is Packed"),
                            translate("Packager", "You can now start sharing it."))
            if Universals.getBoolValue("isCloseOnCleanAndPackage"):
                self.close()
            Universals.isCanBeShowOnMainWindow = True
        except:
            import ReportBug
            error = ReportBug.ReportBug()
            error.show()   
    
    def Clear(self):
        try:
            Universals.isCanBeShowOnMainWindow = False
            answer = Dialogs.ask(translate("Packager", "Your Files Will Be Removed"),
                    str(translate("Packager", "The files in the \"%s\" folder will be cleared according to the criteria you set.<br>"+
                    "This action will delete the files completely, without any chance to recover.<br>"+
                    "Are you sure you want to perform the action?")) % Organizer.getLink(unicode(self.lePathOfProject.text(), "utf-8")))
            if answer==Dialogs.Yes:
                if InputOutputs.clearPackagingDirectory(unicode(self.lePathOfProject.text(), "utf-8"), True, True):
                    Dialogs.show(translate("Packager", "Project Is Cleared"),
                                translate("Packager", "You can now pack your project."))
            Universals.isCanBeShowOnMainWindow = True
        except:
            import ReportBug
            error = ReportBug.ReportBug()
            error.show() 
    
    def Pack(self):
        try:
            Universals.isCanBeShowOnMainWindow = False
            if InputOutputs.makePack(unicode(self.lePathOfPackage.text(), "utf-8"), 
                                self.getPackageType(), unicode(self.lePathOfProject.text(), "utf-8")):
                self.createHashDigest()
                Dialogs.show(translate("Packager", "Project Is Packed"),
                            translate("Packager", "You can now share your project."))
            Universals.isCanBeShowOnMainWindow = True
        except:
            import ReportBug
            error = ReportBug.ReportBug()
            error.show()   
    
    def getPackageType(self):
        if self.cbPackageType.currentIndex()!=0:
            return unicode(self.cbPackageType.currentText(), "utf-8").split(".")[-1]
        else:
            return ""
    
    def selectProjectPath(self):
        try:
            self.cbPackageType.setEnabled(True)
            ProjectPath = MFileDialog.getExistingDirectory(self,
                            translate("Packager", "Please Select Project Folder"),self.lePathOfProject.text())
            if ProjectPath!="":
                self.lePathOfProject.setText(ProjectPath)  
            self.packageTypeChanged()
        except:
            import ReportBug
            error = ReportBug.ReportBug()
            error.show() 
        
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
            import ReportBug
            error = ReportBug.ReportBug()
            error.show() 
        
    def selectPackagePath(self):
        try:
            if self.cbPackageType.currentIndex()!=0:
                packageExtension = self.cbPackageType.currentText()
            else:
                packageExtension = ".tar"   
            PathOfPackage = MFileDialog.getSaveFileName(self,
                        translate("Packager", "Please Select The Pack To Be Created"),self.lePathOfPackage.text(),
                        str(translate("Packager", "Archive Files (*%s)")) % (packageExtension))
            if PathOfPackage!="":
                self.lePathOfPackage.setText(PathOfPackage)    
        except:
            import ReportBug
            error = ReportBug.ReportBug()
            error.show() 
    
    
                
