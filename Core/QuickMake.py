# -*- coding: utf-8 -*-
import sys
import os
from RoutineChecks import QuickMakeParameters
import RoutineChecks
import Dialogs, Records, Organizer
import InputOutputs
from MyObjects import *
import Universals
import ReportBug

class QuickMake():
    def __init__(self):
        if len(QuickMakeParameters)>1:
            answer = None
            isShowQuickMakeWindow = True
            tempWindow = MMainWindow()
            self.quickMakeWindow = QuickMakeWindow()
            Universals.MainWindow = self.quickMakeWindow
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
        import Options
        newOrChangedKeys = Universals.newSettingsKeys + Universals.changedDefaultValuesKeys
        wOptionsPanel = Options.Options(None, QuickMakeParameters[0], None, newOrChangedKeys)
        if MyDialogType=="MDialog":
            if Universals.isActivePyKDE4==True:
                self.setButtons(MyDialog.None)
        elif MyDialogType=="MMainWindow":
            self.setObjectName("Packager")
            Universals.MainWindow = self
        self.setWindowTitle(_actionName)
        pnlMain = MWidget(self)
        vblMain = MVBoxLayout(pnlMain)
        pnlInfo = MWidget()
        vblInfo = MVBoxLayout(pnlInfo)
        vblInfo.addStretch(3)
        if _isShowEmendWidgets:
            lblOldValue = MLabel(translate("QuickMake", "Old Value : "))
            lblNewValue = MLabel(translate("QuickMake", "New Value : "))
            leOldValue = MLineEdit(Organizer.showWithIncorrectChars(QuickMakeParameters[1]).decode("utf-8"))
            leOldValue.setEnabled(False)
            self.leNewValue = MLineEdit(Organizer.emend(QuickMakeParameters[1], True).decode("utf-8"))
            vblInfo.addWidget(lblOldValue)
            vblInfo.addWidget(leOldValue)
            vblInfo.addWidget(lblNewValue)
            vblInfo.addWidget(self.leNewValue)
        else:
            lblValue = MLabel(translate("QuickMake", "Value : "))
            leValue = MLineEdit(Organizer.showWithIncorrectChars(QuickMakeParameters[1]).decode("utf-8"))
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
            if self.checkSource(QuickMakeParameters[1], "directory"):
                import Packager
                self.newDialog = Packager.Packager(QuickMakeParameters[1])
        except:
            self.error = ReportBug.ReportBug()
            self.error.show()   
    
    def hash(self):
        try:
            if self.checkSource(QuickMakeParameters[1], "file"):
                import Hasher
                self.newDialog = Hasher.Hasher(QuickMakeParameters[1])
        except:
            self.error = ReportBug.ReportBug()
            self.error.show()   
                
    def checkIcon(self):
        try:
            if self.checkSource(QuickMakeParameters[1], "directory"):
                InputOutputs.checkIcon(QuickMakeParameters[1])
                Dialogs.show(translate("QuickMake", "Directory Icon Checked"),
                        str(translate("QuickMake", "\"%s\"`s icon checked.<br>The default action based on the data is executed.")) % Organizer.getLink(QuickMakeParameters[1]))
            self.close()
        except:
            self.error = ReportBug.ReportBug()
            self.error.show()   

    def clearEmptyDirectories(self):
        try:
            if self.checkSource(QuickMakeParameters[1], "directory"):
                InputOutputs.activateSmartCheckIcon()
                InputOutputs.clearEmptyDirectories(QuickMakeParameters[1], True, True)
                if InputOutputs.isDir(QuickMakeParameters[1]):
                    InputOutputs.complateSmartCheckIcon()
                Dialogs.show(translate("QuickMake", "Directory Cleaned"),
                        str(translate("QuickMake", "\"%s\" is cleaned based on the criteria you set.")) % Organizer.getLink(QuickMakeParameters[1]))
            self.close()
        except:
            self.error = ReportBug.ReportBug()
            self.error.show()   
                
    def clearUnneededs(self):
        try:
            if self.checkSource(QuickMakeParameters[1], "directory"):
                InputOutputs.clearUnneededs(QuickMakeParameters[1])
                Dialogs.show(translate("QuickMake", "Directory Cleaned"),
                        str(translate("QuickMake", "\"%s\" is cleaned based on the criteria you set.")) % Organizer.getLink(QuickMakeParameters[1]))
            self.close()
        except:
            self.error = ReportBug.ReportBug()
            self.error.show()   
                
    def clearIgnoreds(self):
        try:
            if self.checkSource(QuickMakeParameters[1], "directory"):
                InputOutputs.clearIgnoreds(QuickMakeParameters[1])
                Dialogs.show(translate("QuickMake", "Directory Cleaned"),
                        str(translate("QuickMake", "\"%s\" is cleaned based on the criteria you set.")) % Organizer.getLink(QuickMakeParameters[1]))
            self.close()
        except:
            self.error = ReportBug.ReportBug()
            self.error.show()   
                        
    def emendFile(self):
        try:
            if self.checkSource(QuickMakeParameters[1], "file"):
                if Universals.getBoolValue("isShowQuickMakeWindow"):
                    newEmendedName = str(self.leNewValue.text())
                else:
                    newEmendedName = Organizer.emend(QuickMakeParameters[1], True)
                import Organizer
                newFileName = InputOutputs.moveOrChange(QuickMakeParameters[1], newEmendedName)
                Dialogs.show(translate("QuickMake", "File Emended"),
                        str(translate("QuickMake", "\"%s\" is emended based on the criteria you set.This file is \"%s\" now.")) % 
                        (Organizer.getLink(QuickMakeParameters[1]), Organizer.getLink(InputOutputs.getDirName(QuickMakeParameters[1])+"/"+newFileName)))
            self.close()
        except:
            self.error = ReportBug.ReportBug()
            self.error.show()   

    def emendDirectory(self):
        try:
            if self.checkSource(QuickMakeParameters[1], "directory"):
                if Universals.getBoolValue("isShowQuickMakeWindow"):
                    newEmendedName = str(self.leNewValue.text())
                else:
                    newEmendedName = Organizer.emend(QuickMakeParameters[1], True)
                import Organizer
                newName = InputOutputs.moveOrChange(QuickMakeParameters[1], newEmendedName, "directory")
                newDirName = InputOutputs.getDirName(QuickMakeParameters[1])+"/"+newName
                Dialogs.show(translate("QuickMake", "Directory Emended"),
                        str(translate("QuickMake", "\"%s\" is emended based on the criteria you set.This directory is \"%s\" now.")) % 
                        (Organizer.getLink(QuickMakeParameters[1]), Organizer.getLink(newDirName)))
            self.close()
        except:
            self.error = ReportBug.ReportBug()
            self.error.show()   
                            
    def emendDirectoryWithContents(self):
        try:
            if self.checkSource(QuickMakeParameters[1], "directory"):
                if Universals.getBoolValue("isShowQuickMakeWindow"):
                    newEmendedName = str(self.leNewValue.text())
                else:
                    newEmendedName = Organizer.emend(QuickMakeParameters[1], True)
                import Organizer
                InputOutputs.activateSmartCheckIcon()
                newName = InputOutputs.moveOrChange(QuickMakeParameters[1], newEmendedName, "directory")
                newDirName = InputOutputs.getDirName(QuickMakeParameters[1])+"/"+newName
                InputOutputs.readDirectory(newDirName)
                for fileAndDirs in InputOutputs.fileAndDirectoryNames:
                    objectType = "file"
                    if InputOutputs.isDir(newDirName + "/" + fileAndDirs):
                        objectType = "directory"
                    InputOutputs.moveOrChange(newDirName + "/" + fileAndDirs, 
                              newDirName + "/" + Organizer.emend(fileAndDirs), objectType)
                if Universals.getBoolValue("isAutoMakeIconToDirectoryWhenFileMove"):
                    InputOutputs.checkIcon(newDirName)
                if InputOutputs.isDir(newDirName):
                    InputOutputs.complateSmartCheckIcon()
                Dialogs.show(translate("QuickMake", "Directory And Contents Emended"),
                        str(translate("QuickMake", "\"%s\" is emended based on the criteria you set.This directory is \"%s\" now.")) % 
                        (Organizer.getLink(QuickMakeParameters[1]), Organizer.getLink(newDirName)))
            self.close()
        except:
            self.error = ReportBug.ReportBug()
            self.error.show()   
                            
    def copyPath(self):
        try:
            if self.checkSource(QuickMakeParameters[1]):
                MApplication.clipboard().setText(QuickMakeParameters[1].decode("utf-8"))
                Dialogs.show(translate("QuickMake", "Copied To Clipboard"),
                        str(translate("QuickMake", "\"%s\" copied to clipboard.")) % Organizer.getLink(QuickMakeParameters[1]))
            self.close()
        except:
            self.error = ReportBug.ReportBug()
            self.error.show()   

    def fileTree(self):
        try:
            if self.checkSource(QuickMakeParameters[1], "directory"):
                import FileTreeBuilder
                self.newDialog = FileTreeBuilder.FileTreeBuilder(QuickMakeParameters[1])
        except:
            self.error = ReportBug.ReportBug()
            self.error.show()     
    
    def removeOnlySubFiles(self):
        try:
            if self.checkSource(QuickMakeParameters[1], "directory"):
                answer = Dialogs.ask(translate("QuickMake", "All Files Will Be Removed"),
                        str(translate("QuickMake", "Are you sure you want to remove only all files in \"%s\"?<br>Note:Do not will remove directory and subfolders.")) % Organizer.getLink(QuickMakeParameters[1]))
                if answer==Dialogs.Yes:
                    Universals.MainWindow.setEnabled(False)
                    InputOutputs.removeOnlySubFiles(QuickMakeParameters[1])
                    Universals.MainWindow.setEnabled(True)
                    Dialogs.show(translate("QuickMake", "Removed Only All Files"),
                        str(translate("QuickMake", "Removed only all files in \"%s\".<br>Note:Do not removed directory and subfolders.")) % Organizer.getLink(QuickMakeParameters[1]))
            self.close()
        except:
            self.error = ReportBug.ReportBug()
            self.error.show()   

    def clear(self):
        try:
            if self.checkSource(QuickMakeParameters[1], "directory"):
                import Cleaner
                self.newDialog = Cleaner.Cleaner(QuickMakeParameters[1])
        except:
            self.error = ReportBug.ReportBug()
            self.error.show()     
    
