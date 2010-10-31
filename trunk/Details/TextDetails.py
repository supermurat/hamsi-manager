# -*- coding: utf-8 -*-
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
import InputOutputs
import os,sys
from MyObjects import *
import Dialogs
import Organizer
import Universals
import ReportBug
import Settings

class TextDetails(MDialog):
    global textDialogs, closeAllTextDialogs
    textDialogs =[]
    
    def __init__(self,_filePath,_isOpenDetailsOnNewWindow):
        global textDialogs
        if InputOutputs.IA.isFile(_filePath):
            if _isOpenDetailsOnNewWindow==False:
                isHasOpenedDialog=False
                for dialog in textDialogs:
                    if dialog.isVisible()==True:
                        isHasOpenedDialog=True
                        self = dialog
                        self.changeFile(_filePath)
                        self.activateWindow()
                        self.raise_()
                        break
                if isHasOpenedDialog==False:
                    _isOpenDetailsOnNewWindow=True
            if _isOpenDetailsOnNewWindow==True:
                textDialogs.append(self)
                MDialog.__init__(self, MApplication.activeWindow())
                if Universals.isActivePyKDE4==True:
                    self.setButtons(MDialog.None)
                self.charSet = MComboBox()
                self.charSet.addItems(Variables.getCharSets())
                self.charSet.setCurrentIndex(self.charSet.findText(Universals.MySettings["fileSystemEncoding"]))
                self.infoLabels = []
                self.infoValues = []
                self.fileValues = []
                pbtnClose = MPushButton(translate("TextDetails", "Close"))
                pbtnSave = MPushButton(translate("TextDetails", "Save Changes"))
                pbtnSave.setIcon(MIcon("Images:save.png"))
                MObject.connect(pbtnClose, SIGNAL("clicked()"), self.close)
                MObject.connect(pbtnSave, SIGNAL("clicked()"), self.save)
                self.labelsValues = [translate("TextDetails", "Directory : "), 
                                    translate("TextDetails", "File Name : "), 
                                    translate("TextDetails", "Contents : ")]
                self.changeFile(_filePath, True)
                HBOXs = []
                for infoNo in range(3):
                    HBOXs.append(MHBoxLayout())
                    HBOXs[infoNo].addWidget(self.infoLabels[infoNo])
                    HBOXs[infoNo].addWidget(self.infoValues[infoNo])
                VBOXs = []
                VBOXs.append(MVBoxLayout())
                for hbox in HBOXs:
                    VBOXs[0].addLayout(hbox)
                self.pnlMain = MWidget()
                vblMain = MVBoxLayout(self.pnlMain)
                HBOXs.append(MHBoxLayout())
                HBOXs[3].addWidget(self.charSet, 1)
                HBOXs[3].addWidget(pbtnSave, 4)
                VBOXs[0].addLayout(HBOXs[3])
                VBOXs[0].addWidget(pbtnClose)
                vblMain.addLayout(VBOXs[0], 1)
                if Universals.isActivePyKDE4==True:
                    self.setMainWidget(self.pnlMain)
                else:
                    self.setLayout(vblMain)
                self.show()
                self.setMinimumWidth(700)
                self.setMinimumHeight(500)
        else:
            Dialogs.showError(translate("TextDetails", "File Does Not Exist"), 
                        str(translate("TextDetails", "\"%s\" does not exist.<br>Table will be refreshed automatically!<br>Please retry.")
                            )% Organizer.getLink(Organizer.showWithIncorrectChars(_filePath)))
            from Universals import MainWindow
            MainWindow.FileManager.makeRefresh()
    
    def changeFile(self, _filePath, _isNew=False):
        self.fileValues = InputOutputs.IA.readTextFile(_filePath)
        self.setWindowTitle(Organizer.showWithIncorrectChars(InputOutputs.IA.getBaseName(_filePath)).decode("utf-8"))                
        for infoNo, label in enumerate(self.labelsValues):
            if self.fileValues[infoNo]=="None":
                self.fileValues[infoNo] = ""
            if _isNew==True:
                self.infoLabels.append(MLabel(label))
                self.infoLabels[infoNo].setMaximumWidth(100)
                self.infoLabels[infoNo].setMinimumWidth(100)
            if infoNo==2:
                if _isNew==True:
                    self.infoValues.append(MPlainTextEdit())
                    self.infoValues[infoNo].setPlainText(Organizer.emend(self.fileValues[infoNo], "text", False, True).decode("utf-8"))
                else:
                    self.infoValues[infoNo].setPlainText(Organizer.emend(self.fileValues[infoNo], "text", False, True).decode("utf-8"))
            elif infoNo==0:
                if _isNew==True:
                    self.infoValues.append(MLineEdit(Organizer.emend(self.fileValues[infoNo], "directory", False).decode("utf-8")))
                else:
                    self.infoValues[infoNo].setText(Organizer.emend(self.fileValues[infoNo], "directory", False).decode("utf-8"))
            elif infoNo==1:
                lineInfo = Organizer.emend(self.fileValues[infoNo], "file")
                if lineInfo.find(".")!=-1:
                    tempInfo=""
                    tempInfos = lineInfo.split(".")
                    for key,i in enumerate(tempInfos):
                        if key!=len(tempInfos)-1:
                            tempInfo+=i+"."
                        else:
                            tempInfo+=self.fileValues[infoNo].split(".")[-1].decode("utf-8").lower()
                            lineInfo = tempInfo
                if _isNew==True:
                    self.infoValues.append(MLineEdit(lineInfo.decode("utf-8")))
                else:
                    self.infoValues[infoNo].setText(lineInfo.decode("utf-8"))
            else:
                if _isNew==True:
                    self.infoValues.append(MLineEdit(Organizer.emend(self.fileValues[infoNo]).decode("utf-8")))
                else:
                    self.infoValues[infoNo].setText(Organizer.emend(self.fileValues[infoNo]).decode("utf-8"))
    
    def closeAllTextDialogs():
        for dialog in textDialogs:
            try:
                if dialog.isVisible()==True:
                    dialog.close()
            except:
                continue
        
    def save(self):
        try:
            import Records
            Records.setTitle(translate("TextDetails", "Text File"))
            newFileValues=[]
            for infoNo,value in enumerate(self.infoValues):
                if infoNo==0:
                    if str(unicode(value.text()).encode("utf-8")).find(InputOutputs.IA.getDirName(self.fileValues[0]))!=-1:
                        newFileValues.append(unicode(value.text()).encode("utf-8"))
                    else:
                        newFileValues.append(InputOutputs.IA.getDirName(self.fileValues[0])+unicode(value.text()).encode("utf-8"))
                elif infoNo==2:
                    newFileValues.append(unicode(value.toPlainText()).encode("utf-8"))
                else:
                    newFileValues.append(unicode(value.text()).encode("utf-8"))
            newPath = InputOutputs.IA.writeTextFile(self.fileValues,newFileValues, unicode(self.charSet.currentText()).encode("utf-8"))
            if newPath!=self.fileValues[0]+"/"+self.fileValues[1]:
                self.changeFile(newPath)
            from Universals import MainWindow
            MainWindow.FileManager.makeRefresh()
            Records.saveAllRecords()
        except:
            error = ReportBug.ReportBug()
            error.show()  
    
