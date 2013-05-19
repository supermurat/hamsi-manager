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


from Core.MyObjects import *
from Core import Universals
from Core import Dialogs
import InputOutputs
from Options import OptionsForm
from Core import Organizer

MyDialog, MyDialogType, MyParent = getMyDialog()

class Cleaner(MyDialog):
    def __init__(self, _directory):
        MyDialog.__init__(self, MyParent)
        if MyDialogType=="MDialog":
            if Universals.isActivePyKDE4==True:
                self.setButtons(MyDialog.NoDefault)
        elif MyDialogType=="MMainWindow":
            self.setObjectName("Cleaner")
            Universals.setMainWindow(self)
        newOrChangedKeys = Universals.newSettingsKeys + Universals.changedDefaultValuesKeys
        wOptionsPanel = OptionsForm.OptionsForm(None, "clear", None, newOrChangedKeys)
        lblPleaseSelect = MLabel(translate("Cleaner", "Directory"))
        self.pbtnClear = MPushButton(translate("Cleaner", "Clear"))
        self.pbtnClose = MPushButton(translate("Cleaner", "Close"))
        self.lePathOfProject = MLineEdit(trForUI(_directory))
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
            answer = Dialogs.ask(translate("Cleaner", "Your Files Will Be Removed"),
                    str(translate("Cleaner", "The files in the \"%s\" folder will be cleared according to the criteria you set.<br>"+
                    "This action will delete the files completely, without any chance to recover.<br>"+
                    "Are you sure you want to perform the action?")) % Organizer.getLink(Organizer.getLink(str(self.lePathOfProject.text()))))
            if answer==Dialogs.Yes:
                if InputOutputs.clearCleaningDirectory(str(self.lePathOfProject.text()), True, True):
                    Dialogs.show(translate("Cleaner", "Directory Is Cleared"),
                                str(translate("Cleaner", "This directory is cleared : \"%s\"")) % Organizer.getLink(str(self.lePathOfProject.text())))
            Universals.isCanBeShowOnMainWindow = True
        except:
            from Core import ReportBug
            ReportBug.ReportBug()

    def selectProjectPath(self):
        try:
            ProjectPath = Dialogs.getExistingDirectory(translate("Cleaner", "Please Select Directory"),self.lePathOfProject.text(), 0)
            if ProjectPath is not None:
                self.lePathOfProject.setText(trForUI(ProjectPath))
        except:
            from Core import ReportBug
            ReportBug.ReportBug()
    
    
                
