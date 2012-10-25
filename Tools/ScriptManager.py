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


from Core.MyObjects import *
import sys
from Core import Dialogs
from Core import Universals
from Core import ReportBug
import InputOutputs
import Options

   

class Scripts():
    global pathOfScripsDirectory, createDefaultScript, createNewScript, getScript, getScriptList, getNextScriptFilePath, saveScript, clearScript
    pathOfScripsDirectory = InputOutputs.joinPath(Universals.pathOfSettingsDirectory, "Scripts")
    
    def createDefaultScript(_filePath):
        defaultCodes = ("#!/usr/bin/env python\n" +
                        "# -*- codding: utf-8 -*-\n"+
                        "\n"+
                        "#You can type and execute the commands you wish to run here.\n"+
                        "#You can get detailed information from our official website.\n"+
                        "from Core import Dialogs\nDialogs.show(\"This is an example\",\"You can develop the examples as you wish.\")"+
                        "\n\n\n\n\n\n\n\n\n")
        InputOutputs.writeToFile(_filePath, defaultCodes)
        
    def getNextScriptFilePath():
        i = 1
        while True:
            nextScriptFilePath = InputOutputs.joinPath(pathOfScripsDirectory, translate("Scripts", "Script") + "-" + str(i) + ".py")
            if InputOutputs.isFile(nextScriptFilePath)==False:
                return nextScriptFilePath
            i = i + 1
    
    def createNewScript():
        filePath = getNextScriptFilePath()
        createDefaultScript(filePath)
        return InputOutputs.getBaseName(filePath)
    
    def getScript(_filePath):
        return InputOutputs.readFromFile(_filePath)
    
    def getScriptList():
        if InputOutputs.isDir(pathOfScripsDirectory)==False:
            InputOutputs.makeDirs(pathOfScripsDirectory)
            createNewScript()
        scriptList = InputOutputs.readDirectory(pathOfScripsDirectory, "file")
        if len(scriptList)==0:
            createNewScript()
            scriptList = InputOutputs.readDirectory(pathOfScripsDirectory, "file")
        return scriptList
    
    def saveScript(_filePath, _codes):
        InputOutputs.writeToFile(_filePath, _codes)
    
    def clearScript(_filePath):
        createDefaultScript(_filePath)

        
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
        self.sciCommand.setAutoCompletionThreshold(2)
        self.sciCommand.setAutoCompletionSource(QsciScintilla.AcsDocument)
        self.sciCommand.setLexer(QsciLexerPython(self))
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
                codes = getScript(InputOutputs.joinPath(pathOfScripsDirectory, self.currentScriptFileName))
                self.sciCommand.setText(trForUI(codes))
        except:
            error = ReportBug.ReportBug()
            error.show()
        
    def runScriptAndClose(self):
        try:
            if self.runScript():
                self.close()
        except:
            error = ReportBug.ReportBug()
            error.show()
        
    def runScript(self):
        try:
            try:
                exec (str(self.sciCommand.text()))
                return True
            except Exception as error:
                import traceback
                cla, error, trbk = sys.exc_info()
                errorName = cla.__name__
                try:
                    excArgs = error.__dict__["args"]
                except KeyError:
                    excArgs = "<no args>"
                errorDetail = traceback.format_tb(trbk, 5)
                errorDetails = str(errorName)+"\n"+str(error)+"\n"+str(excArgs)+"\n"+str(errorDetail[0])
                Dialogs.showError(translate("ScriptManager", "Error: Failed To Run The Query"),
                            str(translate("ScriptManager", "Error details: <br> \"%s\"")) % (errorDetails))
                return False
        except:
            error = ReportBug.ReportBug()
            error.show()
    
    def checkForSave(self):
        try:
            if self.currentScriptFileName is not None:
                codes = getScript(InputOutputs.joinPath(pathOfScripsDirectory, self.currentScriptFileName))
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
            error = ReportBug.ReportBug()
            error.show()
    
    def save(self):
        try:
            codes = getScript(InputOutputs.joinPath(pathOfScripsDirectory, self.currentScriptFileName))
            saveScript(InputOutputs.joinPath(pathOfScripsDirectory, self.currentScriptFileName), str(self.sciCommand.text()))
        except:
            error = ReportBug.ReportBug()
            error.show()

    def clear(self):
        try:
            answer = Dialogs.ask(translate("ScriptManager", "Your Codes Will Be Deleted!.."), 
                                translate("ScriptManager", "Your codes will be deleted and the default codes will be installed. Do you wish to clear the current codes?"))
            if answer==Dialogs.Yes:
                clearScript(InputOutputs.joinPath(pathOfScripsDirectory, self.currentScriptFileName))
        except:
            error = ReportBug.ReportBug()
            error.show()
        
    def delete(self):
        try:
            answer = Dialogs.ask(translate("ScriptManager", "Your Script Will Be Deleted!.."), 
                                translate("ScriptManager", "Your script will be deleted. Are you sure you want to delete current script?"))
            if answer==Dialogs.Yes:
                InputOutputs.removeFile(InputOutputs.joinPath(pathOfScripsDirectory, self.currentScriptFileName))
                self.refreshScriptList()
        except:
            error = ReportBug.ReportBug()
            error.show()
        
    def create(self):
        try:
            newScriptFileName = createNewScript()
            self.refreshScriptList()
            self.lwScriptList.setCurrentRow(self.scriptList.index(newScriptFileName))
        except:
            error = ReportBug.ReportBug()
            error.show()
        
    def refreshScriptList(self):
        try:
            self.scriptList = getScriptList()
            self.lwScriptList.refresh(self.scriptList)
            scriptFileName = None
            if len(self.scriptList)>0:
                scriptFileName = self.scriptList[self.lwScriptList.currentRow()]
            self.currentScriptFileName = scriptFileName
        except:
            error = ReportBug.ReportBug()
            error.show()
        
        
