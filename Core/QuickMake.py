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

import sys
import os
from Core.RoutineChecks import QuickMakeParameters
from Core import RoutineChecks
from Core import Dialogs, Records, Organizer
import InputOutputs
from Core.MyObjects import *
from Core import Universals
from Core import ReportBug

class QuickMake():
    def __init__(self):
        if len(QuickMakeParameters)>1:
            answer = None
            isShowQuickMakeWindow = True
            tempWindow = MMainWindow()
            self.quickMakeWindow = QuickMakeWindow()
            Universals.setMainWindow(self.quickMakeWindow)
            isShowEmendWidgets = False
            isCorrectCommand = True
            if QuickMakeParameters[0]=="pack":
                isShowQuickMakeWindow = False
                makeThisAction = self.quickMakeWindow.pack
                actionName = translate("QuickMake", "Pack It Now")
            elif QuickMakeParameters[0]=="hash":
                isShowQuickMakeWindow = False
                makeThisAction = self.quickMakeWindow.hash
                actionName = translate("QuickMake", "Get Hash Digest")
            elif QuickMakeParameters[0]=="checkIcon":
                makeThisAction = self.quickMakeWindow.checkIcon
                actionName = translate("QuickMake", "Check Directory Icon Now")
            elif QuickMakeParameters[0]=="clearEmptyDirectories":
                makeThisAction = self.quickMakeWindow.clearEmptyDirectories
                actionName = translate("QuickMake", "Clear Empty Directories Now")
            elif QuickMakeParameters[0]=="clearUnneededs":
                makeThisAction = self.quickMakeWindow.clearUnneededs
                actionName = translate("QuickMake", "Clear Unneededs Now")
            elif QuickMakeParameters[0]=="clearIgnoreds":
                makeThisAction = self.quickMakeWindow.clearIgnoreds
                actionName = translate("QuickMake", "Clear Ignoreds Now")
            elif QuickMakeParameters[0]=="emendFile":
                isShowEmendWidgets = True
                makeThisAction = self.quickMakeWindow.emendFile
                actionName = translate("QuickMake", "Auto Emend Now")
            elif QuickMakeParameters[0]=="emendDirectory":
                isShowEmendWidgets = True
                makeThisAction = self.quickMakeWindow.emendDirectory
                actionName = translate("QuickMake", "Auto Emend Now")
            elif QuickMakeParameters[0]=="emendDirectoryWithContents":
                isShowEmendWidgets = True
                makeThisAction = self.quickMakeWindow.emendDirectoryWithContents
                actionName = translate("QuickMake", "Auto Emend Now (With Contents)")
            elif QuickMakeParameters[0]=="copyPath":
                isShowQuickMakeWindow = False
                makeThisAction = self.quickMakeWindow.copyPath
                actionName = translate("QuickMake", "Copy Path To Clipboard")
            elif QuickMakeParameters[0]=="fileTree":
                isShowQuickMakeWindow = False
                makeThisAction = self.quickMakeWindow.fileTree
                actionName = translate("QuickMake", "Build File Tree")
            elif QuickMakeParameters[0]=="removeOnlySubFiles":
                makeThisAction = self.quickMakeWindow.removeOnlySubFiles
                actionName = translate("QuickMake", "Remove Sub Files")
            elif QuickMakeParameters[0]=="clear":
                isShowQuickMakeWindow = False
                makeThisAction = self.quickMakeWindow.clear
                actionName = translate("QuickMake", "Clear It Now")
            elif QuickMakeParameters[0]=="textCorrector":
                isShowQuickMakeWindow = False
                makeThisAction = self.quickMakeWindow.textCorrector
                actionName = translate("QuickMake", "Text Corrector")
            elif QuickMakeParameters[0]=="search":
                isShowQuickMakeWindow = False
                makeThisAction = self.quickMakeWindow.search
                actionName = translate("QuickMake", "Search")
            else:
                isCorrectCommand = False
            if isCorrectCommand:
                if isShowQuickMakeWindow:
                    if Universals.getBoolValue("isShowQuickMakeWindow"):
                        self.quickMakeWindow.createWindow(actionName, makeThisAction, isShowEmendWidgets)
                        self.quickMakeWindow.show()
                    else:
                        makeThisAction()
                else:
                    makeThisAction()
            else:
                answer = Dialogs.askSpecial(translate("QuickMake", "Incorrect Command"),
                        translate("QuickMake", "Your action unable to process.Please try again or report this bug."), translate("QuickMake", "Report This Bug"), translate("QuickMake", "Close"))
        else:
            answer = Dialogs.askSpecial(translate("QuickMake", "Missing Command"),
                        translate("QuickMake", "Your action unable to process.Please try again or report this bug."), translate("QuickMake", "Report This Bug"), translate("QuickMake", "Close"))
        if answer==translate("QuickMake", "Report This Bug"):
            self.error = ReportBug.ReportBug(True)
            self.error.show()

MyDialog, MyDialogType, MyParent = getMyDialog()
   
class QuickMakeWindow(MyDialog):
    def __init__(self):
        MyDialog.__init__(self, MyParent)
        
    def createWindow(self, _actionName, _makeThisAction, _isShowEmendWidgets):
        from Options import OptionsForm
        newOrChangedKeys = Universals.newSettingsKeys + Universals.changedDefaultValuesKeys
        wOptionsPanel = OptionsForm.OptionsForm(None, QuickMakeParameters[0], None, newOrChangedKeys)
        if MyDialogType=="MDialog":
            if Universals.isActivePyKDE4==True:
                self.setButtons(MyDialog.NoDefault)
        elif MyDialogType=="MMainWindow":
            self.setObjectName("Packager")
            Universals.setMainWindow(self)
        self.setWindowTitle(_actionName)
        pnlMain = MWidget(self)
        vblMain = MVBoxLayout(pnlMain)
        pnlInfo = MWidget()
        vblInfo = MVBoxLayout(pnlInfo)
        vblInfo.addStretch(3)
        if _isShowEmendWidgets:
            lblOldValue = MLabel(translate("QuickMake", "Old Value : "))
            lblNewValue = MLabel(translate("QuickMake", "New Value : "))
            leOldValue = MLineEdit(trForUI(InputOutputs.getRealPath(QuickMakeParameters[1])))
            leOldValue.setEnabled(False)
            self.leNewValue = MLineEdit(trForUI(Organizer.emend(InputOutputs.getRealPath(QuickMakeParameters[1]), InputOutputs.getObjectType(InputOutputs.getRealPath(QuickMakeParameters[1])))))
            vblInfo.addWidget(lblOldValue)
            vblInfo.addWidget(leOldValue)
            vblInfo.addWidget(lblNewValue)
            vblInfo.addWidget(self.leNewValue)
        else:
            lblValue = MLabel(translate("QuickMake", "Value : "))
            leValue = MLineEdit(trForUI(InputOutputs.getRealPath(QuickMakeParameters[1])))
            leValue.setEnabled(False)
            vblInfo.addWidget(lblValue)
            vblInfo.addWidget(leValue)
        vblInfo.addStretch(3)
        pbtnApply = MPushButton(_actionName)
        pbtnClose = MPushButton(translate("QuickMake", "Cancel"))
        MObject.connect(pbtnApply, SIGNAL("clicked()"), _makeThisAction)
        MObject.connect(pbtnClose, SIGNAL("clicked()"), self.close)
        tabwTabs = MTabWidget()
        tabwTabs.addTab(pnlInfo, translate("QuickMake", "Quick Make"))
        tabwTabs.addTab(wOptionsPanel, translate("QuickMake", "Quick Make Options"))
        vblMain.addWidget(tabwTabs)
        hblBox = MHBoxLayout()
        hblBox.addWidget(pbtnClose, 2)
        hblBox.addWidget(pbtnApply, 3)
        vblInfo.addLayout(hblBox)
        if MyDialogType=="MDialog":
            if Universals.isActivePyKDE4==True:
                self.setMainWidget(pnlMain)
            else:
                self.setLayout(vblMain)
        elif MyDialogType=="MMainWindow":
            self.setCentralWidget(pnlMain)
            moveToCenter(self)
        self.setMinimumSize(450, 350)
                        
    def closeEvent(self, _event):
        MApplication.setQuitOnLastWindowClosed(True)
    
    def checkSource(self, _oldPath, _objectType="fileOrDirectory"):
        if _objectType=="file" and InputOutputs.isFile(_oldPath)==False:
            answer = Dialogs.ask(translate("QuickMake", "Cannot Find File"),
                    str(translate("InputOutputs", "\"%s\" : cannot find a file with this name.<br>Are you want to organize parant directory with Hamsi Manager?")) % Organizer.getLink(_oldPath))
            if answer==Dialogs.Yes:
                self.organizeWithHamsiManager(_oldPath)
            return False
        elif _objectType=="directory" and InputOutputs.isDir(_oldPath)==False:
            answer = Dialogs.ask(translate("QuickMake", "Cannot Find Directory"),
                    str(translate("InputOutputs", "\"%s\" : cannot find a folder with this name.<br>Are you want to organize parant directory with Hamsi Manager?")) % Organizer.getLink(_oldPath))
            if answer==Dialogs.Yes:
                self.organizeWithHamsiManager(_oldPath)
            return False
        elif InputOutputs.isDir(_oldPath)==False and InputOutputs.isFile(_oldPath)==False:
            answer = Dialogs.ask(translate("QuickMake", "Cannot Find File Or Directory"),
                    str(translate("InputOutputs", "\"%s\" : cannot find a file or directory with this name.<br>Are you want to organize parant directory with Hamsi Manager?")) % Organizer.getLink(_oldPath))
            if answer==Dialogs.Yes:
                self.organizeWithHamsiManager(_oldPath)
            return False
        return True
        
    def organizeWithHamsiManager(self, _oldPath):
        Universals.setMySetting("lastDirectory", InputOutputs.getRealDirName(_oldPath, True))
        RoutineChecks.isQuickMake = False
        self.close()
    
    def pack(self):
        try:
            if self.checkSource(InputOutputs.getRealPath(QuickMakeParameters[1]), "directory"):
                from Tools import Packager
                self.newDialog = Packager.Packager(InputOutputs.getRealPath(QuickMakeParameters[1]))
        except:
            self.error = ReportBug.ReportBug()
            self.error.show()   
    
    def hash(self):
        try:
            if self.checkSource(InputOutputs.getRealPath(QuickMakeParameters[1]), "file"):
                from Tools import Hasher
                self.newDialog = Hasher.Hasher(InputOutputs.getRealPath(QuickMakeParameters[1]))
        except:
            self.error = ReportBug.ReportBug()
            self.error.show()   
                
    def checkIcon(self):
        try:
            if self.checkSource(InputOutputs.getRealPath(QuickMakeParameters[1]), "directory"):
                InputOutputs.checkIcon(InputOutputs.getRealPath(QuickMakeParameters[1]))
                Dialogs.show(translate("QuickMake", "Directory Icon Checked"),
                        str(translate("QuickMake", "\"%s\"`s icon checked.<br>The default action based on the data is executed.")) % Organizer.getLink(InputOutputs.getRealPath(QuickMakeParameters[1])))
            self.close()
        except:
            self.error = ReportBug.ReportBug()
            self.error.show()   

    def clearEmptyDirectories(self):
        try:
            if self.checkSource(InputOutputs.getRealPath(QuickMakeParameters[1]), "directory"):
                InputOutputs.activateSmartCheckIcon()
                InputOutputs.clearEmptyDirectories(InputOutputs.getRealPath(QuickMakeParameters[1]), True, True)
                if InputOutputs.isDir(InputOutputs.getRealPath(QuickMakeParameters[1])):
                    InputOutputs.completeSmartCheckIcon()
                Dialogs.show(translate("QuickMake", "Directory Cleaned"),
                        str(translate("QuickMake", "\"%s\" is cleaned based on the criteria you set.")) % Organizer.getLink(InputOutputs.getRealPath(QuickMakeParameters[1])))
            self.close()
        except:
            self.error = ReportBug.ReportBug()
            self.error.show()   
                
    def clearUnneededs(self):
        try:
            if self.checkSource(InputOutputs.getRealPath(QuickMakeParameters[1]), "directory"):
                InputOutputs.clearUnneededs(InputOutputs.getRealPath(QuickMakeParameters[1]))
                Dialogs.show(translate("QuickMake", "Directory Cleaned"),
                        str(translate("QuickMake", "\"%s\" is cleaned based on the criteria you set.")) % Organizer.getLink(InputOutputs.getRealPath(QuickMakeParameters[1])))
            self.close()
        except:
            self.error = ReportBug.ReportBug()
            self.error.show()   
                
    def clearIgnoreds(self):
        try:
            if self.checkSource(InputOutputs.getRealPath(QuickMakeParameters[1]), "directory"):
                InputOutputs.clearIgnoreds(InputOutputs.getRealPath(QuickMakeParameters[1]))
                Dialogs.show(translate("QuickMake", "Directory Cleaned"),
                        str(translate("QuickMake", "\"%s\" is cleaned based on the criteria you set.")) % Organizer.getLink(InputOutputs.getRealPath(QuickMakeParameters[1])))
            self.close()
        except:
            self.error = ReportBug.ReportBug()
            self.error.show()   
                        
    def emendFile(self):
        try:
            if self.checkSource(InputOutputs.getRealPath(QuickMakeParameters[1]), "file"):
                if Universals.getBoolValue("isShowQuickMakeWindow"):
                    newEmendedName = str(self.leNewValue.text())
                else:
                    newEmendedName = Organizer.emend(InputOutputs.getRealPath(QuickMakeParameters[1]), InputOutputs.getObjectType(InputOutputs.getRealPath(QuickMakeParameters[1])))
                from Core import Organizer
                oldFileName = InputOutputs.getRealPath(QuickMakeParameters[1])
                newFileName = InputOutputs.moveOrChange(oldFileName, newEmendedName)
                if newFileName!=oldFileName:
                    Dialogs.show(translate("QuickMake", "File Emended"),
                            str(translate("QuickMake", "\"%s\" is emended based on the criteria you set.This file is \"%s\" now.")) % 
                            (Organizer.getLink(InputOutputs.getRealPath(QuickMakeParameters[1])), Organizer.getLink(newFileName)))
            self.close()
        except:
            self.error = ReportBug.ReportBug()
            self.error.show()   

    def emendDirectory(self):
        try:
            if self.checkSource(InputOutputs.getRealPath(QuickMakeParameters[1]), "directory"):
                if Universals.getBoolValue("isShowQuickMakeWindow"):
                    newEmendedName = str(self.leNewValue.text())
                else:
                    newEmendedName = Organizer.emend(InputOutputs.getRealPath(QuickMakeParameters[1]), InputOutputs.getObjectType(InputOutputs.getRealPath(QuickMakeParameters[1])))
                from Core import Organizer
                oldFileName = InputOutputs.getRealPath(QuickMakeParameters[1])
                newDirName = InputOutputs.moveOrChange(oldFileName, newEmendedName, "directory")
                if newDirName!=oldFileName:
                    Dialogs.show(translate("QuickMake", "Directory Emended"),
                            str(translate("QuickMake", "\"%s\" is emended based on the criteria you set.This directory is \"%s\" now.")) % 
                            (Organizer.getLink(InputOutputs.getRealPath(QuickMakeParameters[1])), Organizer.getLink(newDirName)))
            self.close()
        except:
            self.error = ReportBug.ReportBug()
            self.error.show()   
                            
    def emendDirectoryWithContents(self):
        try:
            if self.checkSource(InputOutputs.getRealPath(QuickMakeParameters[1]), "directory"):
                if Universals.getBoolValue("isShowQuickMakeWindow"):
                    newEmendedName = str(self.leNewValue.text())
                else:
                    newEmendedName = Organizer.emend(InputOutputs.getRealPath(QuickMakeParameters[1]), InputOutputs.getObjectType(InputOutputs.getRealPath(QuickMakeParameters[1])))
                from Core import Organizer
                InputOutputs.activateSmartCheckIcon()
                oldFileName = InputOutputs.getRealPath(QuickMakeParameters[1])
                newDirName = InputOutputs.moveOrChange(oldFileName, newEmendedName, "directory")
                if newDirName!=oldFileName:
                    fileAndDirectoryNames = InputOutputs.readDirectory(newDirName, "fileAndDirectory")
                    for fileAndDirs in fileAndDirectoryNames:
                        objectType = InputOutputs.getObjectType(InputOutputs.joinPath(newDirName, fileAndDirs))
                        InputOutputs.moveOrChange(InputOutputs.joinPath(newDirName, fileAndDirs), 
                                  InputOutputs.joinPath(newDirName,  Organizer.emend(fileAndDirs, objectType)), objectType)
                    if Universals.isActiveDirectoryCover and Universals.getBoolValue("isActiveAutoMakeIconToDirectory") and Universals.getBoolValue("isAutoMakeIconToDirectoryWhenFileMove"):
                        InputOutputs.checkIcon(newDirName)
                    if InputOutputs.isDir(newDirName):
                        InputOutputs.completeSmartCheckIcon()
                    Dialogs.show(translate("QuickMake", "Directory And Contents Emended"),
                            str(translate("QuickMake", "\"%s\" is emended based on the criteria you set.This directory is \"%s\" now.")) % 
                            (Organizer.getLink(InputOutputs.getRealPath(QuickMakeParameters[1])), Organizer.getLink(newDirName)))
            self.close()
        except:
            self.error = ReportBug.ReportBug()
            self.error.show()   
                            
    def copyPath(self):
        try:
            if self.checkSource(InputOutputs.getRealPath(QuickMakeParameters[1])):
                MApplication.clipboard().setText(trForUI(InputOutputs.getRealPath(QuickMakeParameters[1])))
                Dialogs.show(translate("QuickMake", "Copied To Clipboard"),
                        str(translate("QuickMake", "\"%s\" copied to clipboard.")) % Organizer.getLink(InputOutputs.getRealPath(QuickMakeParameters[1])))
            self.close()
        except:
            self.error = ReportBug.ReportBug()
            self.error.show()   

    def fileTree(self):
        try:
            if self.checkSource(InputOutputs.getRealPath(QuickMakeParameters[1]), "directory"):
                from Tools import FileTreeBuilder
                self.newDialog = FileTreeBuilder.FileTreeBuilder(InputOutputs.getRealPath(QuickMakeParameters[1]))
        except:
            self.error = ReportBug.ReportBug()
            self.error.show()     
    
    def removeOnlySubFiles(self):
        try:
            if self.checkSource(InputOutputs.getRealPath(QuickMakeParameters[1]), "directory"):
                answer = Dialogs.ask(translate("QuickMake", "All Files Will Be Removed"),
                        str(translate("QuickMake", "Are you sure you want to remove only all files in \"%s\"?<br>Note:Do not will remove directory and subfolders.")) % Organizer.getLink(InputOutputs.getRealPath(QuickMakeParameters[1])))
                if answer==Dialogs.Yes:
                    Universals.MainWindow.setEnabled(False)
                    InputOutputs.removeOnlySubFiles(InputOutputs.getRealPath(QuickMakeParameters[1]))
                    Universals.MainWindow.setEnabled(True)
                    Dialogs.show(translate("QuickMake", "Removed Only All Files"),
                        str(translate("QuickMake", "Removed only all files in \"%s\".<br>Note:Do not removed directory and subfolders.")) % Organizer.getLink(InputOutputs.getRealPath(QuickMakeParameters[1])))
            self.close()
        except:
            self.error = ReportBug.ReportBug()
            self.error.show()   

    def clear(self):
        try:
            if self.checkSource(InputOutputs.getRealPath(QuickMakeParameters[1]), "directory"):
                from Tools import Cleaner
                self.newDialog = Cleaner.Cleaner(InputOutputs.getRealPath(QuickMakeParameters[1]))
        except:
            self.error = ReportBug.ReportBug()
            self.error.show()     
    
    def textCorrector(self):
        try:
            if self.checkSource(InputOutputs.getRealPath(QuickMakeParameters[1]), "file"):
                from Tools import TextCorrector
                self.newDialog = TextCorrector.TextCorrector(InputOutputs.getRealPath(QuickMakeParameters[1]))
        except:
            self.error = ReportBug.ReportBug()
            self.error.show()    
            
    def search(self):
        try:
            if self.checkSource(InputOutputs.getRealPath(QuickMakeParameters[1])):
                from Tools import Searcher
                self.newDialog = Searcher.Searcher(InputOutputs.getRealPath(QuickMakeParameters[1]))
        except:
            self.error = ReportBug.ReportBug()
            self.error.show()    
            
            
        
