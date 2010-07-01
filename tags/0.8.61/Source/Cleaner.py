# -*- coding: utf-8 -*-

from MyObjects import *
import Universals
import Dialogs
import InputOutputs
import Options
import Organizer

MyDialog, MyDialogType, MyParent = getMyDialog()

class Cleaner(MyDialog):
    def __init__(self, _directory):
        MyDialog.__init__(self, MyParent)
        if MyDialogType=="MDialog":
            if Universals.isActivePyKDE4==True:
                self.setButtons(MyDialog.None)
        elif MyDialogType=="MMainWindow":
            self.setObjectName("Cleaner")
            Universals.MainWindow = self
        newOrChangedKeys = Universals.newSettingsKeys + Universals.changedDefaultValuesKeys
        wOptionsPanel = Options.Options(None, "clear", None, newOrChangedKeys)
        lblPleaseSelect = MLabel(translate("Cleaner", "<font color=red><b>Directory</b></font>"))
        self.pbtnClear = MPushButton(translate("Cleaner", "Clear"))
        self.pbtnClose = MPushButton(translate("Cleaner", "Close"))
        self.lePathOfProject = MLineEdit(_directory.decode("utf-8"))
        self.pbtnClear.setToolTip(translate("Cleaner", "Directory you selected will is cleared"))
        self.pbtnSelectProjectPath = MPushButton(translate("Cleaner", "Browse"))
        self.connect(self.pbtnSelectProjectPath,SIGNAL("clicked()"),self.selectProjectPath)
        self.connect(self.pbtnClear,SIGNAL("clicked()"),self.Clear)
        self.connect(self.pbtnClose,SIGNAL("clicked()"),self.close)
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
        HBox1.addWidget(self.pbtnClose)
        vblMain2.addWidget(lblPleaseSelect)
        vblMain2.addLayout(HBox)
        vblMain2.addStretch(1)
        vblMain2.addLayout(HBox1)
        tabwTabs.addTab(pnlMain2, translate("Cleaner", "Clear"))
        tabwTabs.addTab(wOptionsPanel, translate("Cleaner", "Quick Options"))
        vblMain.addWidget(tabwTabs)
        if MyDialogType=="MDialog":
            if Universals.isActivePyKDE4==True:
                self.setMainWidget(pnlMain)
            else:
                self.setLayout(vblMain)
        elif MyDialogType=="MMainWindow":
            self.setCentralWidget(pnlMain)
            moveToCenter(self)
        self.setWindowTitle(translate("Cleaner", "Cleaner"))
        self.setWindowIcon(MIcon("Images:clear.png"))
        self.show()
                        
    def closeEvent(self, _event):
        MApplication.setQuitOnLastWindowClosed(True)
    
    def Clear(self):
        try:
            Universals.isCanBeShowOnMainWindow = False
            MApplication.processEvents()
            answer = Dialogs.ask(translate("Cleaner", "Your Files Will Be Removed"),
                    str(translate("Cleaner", "The files in the \"%s\" folder will be cleared according to the criteria you set.<br>"+
                    "This action will delete the files completely, without any chance to recover.<br>"+
                    "Are you sure you want to perform the action?")) % Organizer.getLink(Organizer.getLink(unicode(self.lePathOfProject.text(), "utf-8"))))
            if answer==Dialogs.Yes:
                if InputOutputs.clearCleaningDirectory(unicode(self.lePathOfProject.text(), "utf-8"), True, True):
                    Dialogs.show(translate("Cleaner", "Directory Is Cleared"),
                                str(translate("Cleaner", "This directory is cleared : \"%s\"")) % Organizer.getLink(str(self.lePathOfProject.text())))
            Universals.isCanBeShowOnMainWindow = True
        except:
            import ReportBug
            error = ReportBug.ReportBug()
            error.show() 

    def selectProjectPath(self):
        try:
            ProjectPath = MFileDialog.getExistingDirectory(self,
                            translate("Cleaner", "Please Select Directory"),self.lePathOfProject.text())
            if ProjectPath!="":
                self.lePathOfProject.setText(ProjectPath)
        except:
            import ReportBug
            error = ReportBug.ReportBug()
            error.show() 
    
    
                