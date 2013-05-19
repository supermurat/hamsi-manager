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
import sys
from Core import Dialogs
from Core import Universals
from Core import ReportBug
from Core import Scripts
from Core import Variables
import InputOutputs
import Options

class ScriptManager(MDialog):
    global checkScriptManager
    def __init__(self, _parent):
        MDialog.__init__(self, _parent)
        from PyQt4.Qsci import QsciScintilla, QsciLexerPython, QsciAPIs
        if Universals.isActivePyKDE4==True:
            self.setButtons(MDialog.NoDefault)
        self.sciCommand = QsciScintilla()
        self.sciCommand.setUtf8(True)
        self.sciCommand.setAutoIndent(True)
        self.sciCommand.setIndentationGuides(True)
        self.sciCommand.setIndentationsUseTabs(True)
        self.sciCommand.setCaretLineVisible(True)
        self.sciCommand.setAutoCompletionThreshold(2)
        self.sciCommand.setAutoCompletionSource(QsciScintilla.AcsDocument)
        self.sciCommand.setLexer(QsciLexerPython(self))
        self.sciCommand.setMarginLineNumbers(1, True)
        self.sciCommand.setMarginWidth(1, '0000')
        self.sciCommand.setEolMode(QsciScintilla.EolUnix)
        self.sciCommand.setWrapMode(QsciScintilla.WrapWord)
        lblScriptList = MLabel(translate("ScriptManager", "Script List : "))
        self.currentScriptFileName = None
        self.lwScriptList = Options.MyListWidget(self, [], _currentRowChanged=self.getFromScriptList)
        self.refreshScriptList()
        pbtnCreate = MPushButton(translate("ScriptManager", "Create"))
        pbtnDelete = MPushButton(translate("ScriptManager", "Delete"))
        pbtnSave = MPushButton(translate("ScriptManager", "Save"))
        pbtnScriptManagerAndClose = MPushButton(translate("ScriptManager", "Run And Close"))
        pbtnScriptManager = MPushButton(translate("ScriptManager", "Run"))
        pbtnClose = MPushButton(translate("ScriptManager", "Close"))
        pbtnClear = MPushButton(translate("ScriptManager", "Clear"))
        self.cckbIsAutoSaveScripts = Options.MyCheckBox(self, translate("ScriptManager", "Auto Save"), 2, "isAutoSaveScripts")
        self.connect(pbtnCreate,SIGNAL("clicked()"),self.create)
        self.connect(pbtnDelete,SIGNAL("clicked()"),self.delete)
        self.connect(pbtnSave,SIGNAL("clicked()"),self.save)
        self.connect(pbtnScriptManagerAndClose,SIGNAL("clicked()"),self.runScriptAndClose)
        self.connect(pbtnScriptManager,SIGNAL("clicked()"),self.runScript)
        self.connect(pbtnClose,SIGNAL("clicked()"),self.close)
        self.connect(pbtnClear,SIGNAL("clicked()"),self.clear)
        pnlMain = MWidget(self)
        vblMain = MVBoxLayout(pnlMain)
        vbox = MVBoxLayout()
        vbox.addWidget(lblScriptList)
        vbox.addWidget(self.lwScriptList)
        hbox2 = MHBoxLayout()
        hbox2.addWidget(pbtnCreate)
        hbox2.addWidget(pbtnDelete)
        vbox.addLayout(hbox2)
        hbox0 = MHBoxLayout()
        hbox0.addLayout(vbox)
        hbox0.addWidget(self.sciCommand)
        hbox1 = MHBoxLayout()
        hbox1.addWidget(self.cckbIsAutoSaveScripts)
        hbox1.addStretch(1)
        hbox1.addWidget(pbtnClear,1)
        hbox1.addWidget(pbtnSave,1)
        hbox1.addWidget(pbtnScriptManager,1)
        hbox1.addWidget(pbtnScriptManagerAndClose,1)
        hbox1.addWidget(pbtnClose,1)
        vblMain.addLayout(hbox0)
        vblMain.addLayout(hbox1)
        if Universals.isActivePyKDE4==True:
            self.setMainWidget(pnlMain)
        else:
            self.setLayout(vblMain)
        self.setWindowTitle(translate("ScriptManager", "Script Manager"))
        self.setWindowIcon(MIcon("Images:scriptManager.png"))
        self.lwScriptList.setMaximumWidth(150)
        self.setMinimumWidth(650)
        self.setMinimumHeight(450)
        self.show()

    def closeEvent(self, _event):
        if self.checkForSave()==False:
            _event.ignore() 
    
    def checkScriptManager(_isAlertIfNotAvailable=True):
        try:
            from PyQt4.Qsci import QsciScintilla
            return True
        except:
            if _isAlertIfNotAvailable:
                Dialogs.showError(translate("MenuBar", "Qsci Is Not Installed"), 
                    translate("MenuBar", "Qsci is not installed on your systems.<br>Please install Qsci on your system and try again."))
            return False
            
    def getFromScriptList(self, _index = None):
        try:
            if self.checkForSave():
                self.currentScriptFileName = self.scriptList[self.lwScriptList.currentRow()]
                codes = Scripts.getScript(InputOutputs.joinPath(Scripts.pathOfScripsDirectory, self.currentScriptFileName))
                self.sciCommand.setText(trForUI(codes))
        except:
            ReportBug.ReportBug()
        
    def runScriptAndClose(self):
        try:
            if self.runScript():
                self.close()
        except:
            ReportBug.ReportBug()
        
    def runScript(self):
        try:
            return Scripts.runScript(str(self.sciCommand.text()))
        except:
            ReportBug.ReportBug()
    
    def checkForSave(self):
        try:
            if self.currentScriptFileName is not None:
                if InputOutputs.isFile(InputOutputs.joinPath(Scripts.pathOfScripsDirectory, self.currentScriptFileName)):
                    codes = Scripts.getScript(InputOutputs.joinPath(Scripts.pathOfScripsDirectory, self.currentScriptFileName))
                    if str(codes)!=str(self.sciCommand.text()):
                        if self.cckbIsAutoSaveScripts.checkState() == Mt.Checked:
                            self.save()
                        else:
                            answer = Dialogs.ask(translate("ScriptManager", "Do You Wish To Save Your Codes?"), 
                                            translate("ScriptManager", "Do you wish to save your codes so that you can continue later?"), True)
                            if answer==Dialogs.Yes:
                                self.save()
                            elif answer==Dialog.Cancel:
                                return False
            return True
        except:
            ReportBug.ReportBug()
    
    def save(self):
        try:
            codes = Scripts.getScript(InputOutputs.joinPath(Scripts.pathOfScripsDirectory, self.currentScriptFileName))
            Scripts.saveScript(InputOutputs.joinPath(Scripts.pathOfScripsDirectory, self.currentScriptFileName), str(self.sciCommand.text()))
        except:
            ReportBug.ReportBug()

    def clear(self):
        try:
            answer = Dialogs.ask(translate("ScriptManager", "Your Codes Will Be Deleted!.."), 
                                translate("ScriptManager", "Your codes will be deleted and the default codes will be installed. Do you wish to clear the current codes?"))
            if answer==Dialogs.Yes:
                Scripts.clearScript(InputOutputs.joinPath(Scripts.pathOfScripsDirectory, self.currentScriptFileName))
        except:
            ReportBug.ReportBug()
        
    def delete(self):
        try:
            answer = Dialogs.ask(translate("ScriptManager", "Your Script Will Be Deleted!.."), 
                                translate("ScriptManager", "Your script will be deleted. Are you sure you want to delete current script?"))
            if answer==Dialogs.Yes:
                InputOutputs.removeFile(InputOutputs.joinPath(Scripts.pathOfScripsDirectory, self.currentScriptFileName))
                self.refreshScriptList()
        except:
            ReportBug.ReportBug()
        
    def create(self):
        try:
            newScriptFileName = Scripts.createNewScript()
            self.refreshScriptList()
            self.lwScriptList.setCurrentRow(self.scriptList.index(newScriptFileName))
        except:
            ReportBug.ReportBug()
        
    def refreshScriptList(self):
        try:
            self.scriptList = Scripts.getScriptList()
            self.lwScriptList.refresh(self.scriptList)
            scriptFileName = None
            if len(self.scriptList)>0:
                scriptFileName = self.scriptList[self.lwScriptList.currentRow()]
            self.currentScriptFileName = scriptFileName
        except:
            ReportBug.ReportBug()
        
        
