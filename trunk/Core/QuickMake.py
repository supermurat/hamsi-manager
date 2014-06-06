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
        if len(QuickMakeParameters)>1 or (len(QuickMakeParameters)==1 and (QuickMakeParameters[0]=="plugins" or QuickMakeParameters[0]=="configurator")):
            answer = None
            isShowQuickMakeWindow = True
            tempWindow = MMainWindow()
            self.quickMakeWindow = QuickMakeWindow()
            Universals.setMainWindow(self.quickMakeWindow)
            isShowEmendWidgets = False
            isCorrectCommand = True
            if QuickMakeParameters[0]=="configurator":
                isShowQuickMakeWindow = False
                makeThisAction = self.quickMakeWindow.configurator
                actionName = translate("QuickMake", "Hamsi Manager Configurator")
            elif QuickMakeParameters[0]=="plugins":
                isShowQuickMakeWindow = False
                makeThisAction = self.quickMakeWindow.plugins
                actionName = translate("QuickMake", "My Plugins")
            elif QuickMakeParameters[0]=="pack":
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
            ReportBug.ReportBug(True)

MyDialog, MyDialogType, MyParent = getMyDialog()
   
class QuickMakeWindow(MyDialog):
    def __init__(self):
        MyDialog.__init__(self, MyParent)
        
    def createWindow(self, _actionName, _makeThisAction, _isShowEmendWidgets):
        from Options import OptionsForm
        newOrChangedKeys = Universals.newSettingsKeys + Universals.changedDefaultValuesKeys
        wOptionsPanel = OptionsForm.OptionsForm(None, QuickMakeParameters[0], None, newOrChangedKeys)
        if MyDialogType=="MDialog":
            if isActivePyKDE4==True:
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
            if isActivePyKDE4==True:
                self.setMainWidget(pnlMain)
            else:
                self.setLayout(vblMain)
        elif MyDialogType=="MMainWindow":
            self.setCentralWidget(pnlMain)
            moveToCenter(self)
        self.setMinimumSize(450, 350)
                        
    def closeEvent(self, _event):
        MApplication.setQuitOnLastWindowClosed(True)
    
    def checkSource(self, _oldPath, _objectType="fileAndDirectory", _isCheckWritable=True):
        _path = InputOutputs.checkSource(_oldPath, _objectType, False)
        if _path is None:
            if _objectType=="file":
                answer = Dialogs.ask(translate("QuickMake", "Cannot Find File"),
                        str(translate("InputOutputs", "\"%s\" : cannot find a file with this name.<br>Are you want to organize parant directory with Hamsi Manager?")) % Organizer.getLink(_oldPath))
                if answer==Dialogs.Yes:
                    self.organizeWithHamsiManager(_oldPath)
                return None
            elif _objectType=="directory":
                answer = Dialogs.ask(translate("QuickMake", "Cannot Find Directory"),
                        str(translate("InputOutputs", "\"%s\" : cannot find a folder with this name.<br>Are you want to organize parant directory with Hamsi Manager?")) % Organizer.getLink(_oldPath))
                if answer==Dialogs.Yes:
                    self.organizeWithHamsiManager(_oldPath)
                return None
            else:
                answer = Dialogs.ask(translate("QuickMake", "Cannot Find File Or Directory"),
                        str(translate("InputOutputs", "\"%s\" : cannot find a file or directory with this name.<br>Are you want to organize parant directory with Hamsi Manager?")) % Organizer.getLink(_oldPath))
                if answer==Dialogs.Yes:
                    self.organizeWithHamsiManager(_oldPath)
                return None
        if _isCheckWritable:
            if InputOutputs.isWritableFileOrDir(_oldPath)==False:
                return None
        return _path
        
    def organizeWithHamsiManager(self, _oldPath):
        Universals.setMySetting("lastDirectory", InputOutputs.getRealDirName(_oldPath, True))
        RoutineChecks.isQuickMake = False
        self.close()
    
    def pack(self):
        try:
            _path = self.checkSource(str(QuickMakeParameters[1]), "directory", False)
            if _path is not None:
                from Tools import Packager
                self.newDialog = Packager.Packager(_path)
        except:
            ReportBug.ReportBug()
        
    def configurator(self):
        try:
            from Tools import Configurator
            self.newDialog = Configurator.Configurator()
        except:
            ReportBug.ReportBug()
        
    def plugins(self):
        try:
            import MyPlugins
            self.newDialog = MyPlugins.MyPlugins()
        except:
            ReportBug.ReportBug()
    
    def hash(self):
        try:
            _path = self.checkSource(str(QuickMakeParameters[1]), "file", False)
            if _path is not None:
                from Tools import Hasher
                self.newDialog = Hasher.Hasher(_path)
        except:
            ReportBug.ReportBug()
                
    def checkIcon(self):
        try:
            _path = self.checkSource(str(QuickMakeParameters[1]), "directory")
            if _path is not None:
                InputOutputs.checkIcon(_path)
                Dialogs.show(translate("QuickMake", "Directory Icon Checked"),
                        str(translate("QuickMake", "\"%s\"`s icon checked.<br>The default action based on the data is executed.")) % Organizer.getLink(_path))
            self.close()
        except:
            ReportBug.ReportBug()

    def clearEmptyDirectories(self):
        try:
            _path = self.checkSource(str(QuickMakeParameters[1]), "directory")
            if _path is not None:
                if InputOutputs.isWritableFileOrDir(_path):
                    InputOutputs.activateSmartCheckIcon()
                    InputOutputs.checkEmptyDirectories(_path, True, True, True, True)
                    if InputOutputs.isDir(_path):
                        InputOutputs.completeSmartCheckIcon()
                    Dialogs.show(translate("QuickMake", "Directory Cleaned"),
                            str(translate("QuickMake", "\"%s\" is cleaned based on the criteria you set.")) % Organizer.getLink(_path))
            self.close()
        except:
            ReportBug.ReportBug()
                
    def clearUnneededs(self):
        try:
            _path = self.checkSource(str(QuickMakeParameters[1]), "directory")
            if _path is not None:
                InputOutputs.clearUnneededs(_path)
                Dialogs.show(translate("QuickMake", "Directory Cleaned"),
                        str(translate("QuickMake", "\"%s\" is cleaned based on the criteria you set.")) % Organizer.getLink(_path))
            self.close()
        except:
            ReportBug.ReportBug()
                
    def clearIgnoreds(self):
        try:
            _path = self.checkSource(str(QuickMakeParameters[1]), "directory")
            if _path is not None:
                InputOutputs.clearIgnoreds(_path)
                Dialogs.show(translate("QuickMake", "Directory Cleaned"),
                        str(translate("QuickMake", "\"%s\" is cleaned based on the criteria you set.")) % Organizer.getLink(_path))
            self.close()
        except:
            ReportBug.ReportBug()
                        
    def emendFile(self):
        try:
            _path = self.checkSource(str(QuickMakeParameters[1]), "file")
            if _path is not None:
                if Universals.getBoolValue("isShowQuickMakeWindow"):
                    newEmendedName = str(self.leNewValue.text())
                else:
                    newEmendedName = Organizer.emend(_path, InputOutputs.getObjectType(_path))
                oldFileName = _path
                newFileName = InputOutputs.moveOrChange(oldFileName, newEmendedName)
                if newFileName!=oldFileName:
                    Dialogs.show(translate("QuickMake", "File Emended"),
                            str(translate("QuickMake", "\"%s\" is emended based on the criteria you set.This file is \"%s\" now.")) % 
                            (Organizer.getLink(_path), Organizer.getLink(newFileName)))
            self.close()
        except:
            ReportBug.ReportBug()

    def emendDirectory(self):
        try:
            _path = self.checkSource(str(QuickMakeParameters[1]), "directory")
            if _path is not None:
                if Universals.getBoolValue("isShowQuickMakeWindow"):
                    newEmendedName = str(self.leNewValue.text())
                else:
                    newEmendedName = Organizer.emend(_path, InputOutputs.getObjectType(_path))
                oldFileName = _path
                newDirName = InputOutputs.moveOrChange(oldFileName, newEmendedName, "directory")
                if newDirName!=oldFileName:
                    Dialogs.show(translate("QuickMake", "Directory Emended"),
                            str(translate("QuickMake", "\"%s\" is emended based on the criteria you set.This directory is \"%s\" now.")) % 
                            (Organizer.getLink(_path), Organizer.getLink(newDirName)))
            self.close()
        except:
            ReportBug.ReportBug()
                            
    def emendDirectoryWithContents(self):
        try:
            _path = self.checkSource(str(QuickMakeParameters[1]), "directory")
            if _path is not None:
                if Universals.getBoolValue("isShowQuickMakeWindow"):
                    newEmendedName = str(self.leNewValue.text())
                else:
                    newEmendedName = Organizer.emend(_path, InputOutputs.getObjectType(_path))
                InputOutputs.activateSmartCheckIcon()
                oldFileName = _path
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
                            (Organizer.getLink(_path), Organizer.getLink(newDirName)))
            self.close()
        except:
            ReportBug.ReportBug()
                            
    def copyPath(self):
        try:
            _path = self.checkSource(str(QuickMakeParameters[1]), "fileAndDirectory", False)
            if _path is not None:
                MApplication.clipboard().setText(trForUI(_path))
                Dialogs.show(translate("QuickMake", "Copied To Clipboard"),
                        str(translate("QuickMake", "\"%s\" copied to clipboard.")) % Organizer.getLink(_path))
            self.close()
        except:
            ReportBug.ReportBug()

    def fileTree(self):
        try:
            _path = self.checkSource(str(QuickMakeParameters[1]), "directory", False)
            if _path is not None:
                from Tools import FileTreeBuilder
                self.newDialog = FileTreeBuilder.FileTreeBuilder(_path)
        except:
            ReportBug.ReportBug()
    
    def removeOnlySubFiles(self):
        try:
            _path = self.checkSource(str(QuickMakeParameters[1]), "directory")
            if _path is not None:
                answer = Dialogs.ask(translate("QuickMake", "All Files Will Be Removed"),
                        str(translate("QuickMake", "Are you sure you want to remove only all files in \"%s\"?<br>Note:Do not will remove directory and subfolders.")) % Organizer.getLink(_path))
                if answer==Dialogs.Yes:
                    Universals.MainWindow.setEnabled(False)
                    InputOutputs.removeOnlySubFiles(_path)
                    Universals.MainWindow.setEnabled(True)
                    Dialogs.show(translate("QuickMake", "Removed Only All Files"),
                        str(translate("QuickMake", "Removed only all files in \"%s\".<br>Note:Do not removed directory and subfolders.")) % Organizer.getLink(_path))
            self.close()
        except:
            ReportBug.ReportBug()

    def clear(self):
        try:
            _path = self.checkSource(str(QuickMakeParameters[1]), "directory")
            if _path is not None:
                from Tools import Cleaner
                self.newDialog = Cleaner.Cleaner(_path)
        except:
            ReportBug.ReportBug()
    
    def textCorrector(self):
        try:
            _path = self.checkSource(str(QuickMakeParameters[1]), "file")
            if _path is not None:
                from Tools import TextCorrector
                self.newDialog = TextCorrector.TextCorrector(_path)
        except:
            ReportBug.ReportBug()
            
    def search(self):
        try:
            _path = self.checkSource(str(QuickMakeParameters[1]), "fileAndDirectory", False)
            if _path is not None:
                from Tools import Searcher
                searchList = [_path] + QuickMakeParameters[2]
                self.newDialog = Searcher.Searcher(searchList)
        except:
            ReportBug.ReportBug()
            
            
        
