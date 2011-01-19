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


import time
import Universals
import InputOutputs
import Settings
import logging
from Universals import translate

class Records():
    global add, create, read, setTitle, showInWindow, clearRecords, recordContents, isSetedTitle, saveAllRecords,recordContents, checkSize, recordType, lastRecordType, setRecordType, restoreRecordType
    recordContents = ""
    isSetedTitle = False
    recordType = 0
    lastRecordType = 0
    #recordType : 0=Normal, 1=Debug
    
    def create():
        global recordContents
        recordContents += str(translate("Records", "Hamsi Manager Record File - Time Created : ")) + str(time.strftime("%d.%m.%Y %H:%M:%S"))+"\n"
    
    def setTitle(_title):
        global isSetedTitle, recordContents
        if Universals.MySettings.keys().count("isSaveActions")==0 or Universals.getBoolValue("isSaveActions"):
            recordContents += str(_title) + "\n"
        if Universals.loggingLevel==logging.DEBUG:
            print (_title)
        isSetedTitle = True
    
    def add(_action, _previous="", _now=""):
        global recordContents
        if Universals.MySettings.keys().count("isSaveActions")==0 or Universals.getBoolValue("isSaveActions"):
            if recordType==0 or (recordType==1 and Universals.loggingLevel==logging.DEBUG):
                recordContents += str(_action + " ::::::: '") + str(_previous) + "' >>>>>>>> '" + str(_now) + "' <<<<<<< " + str(time.strftime("%d.%m.%Y %H:%M:%S"))+"\n"
        if Universals.loggingLevel==logging.DEBUG:
            print (str(_action + " ::::::: '") + str(_previous) + "' >>>>>>>> '" + str(_now) + "' <<<<<<< " + str(time.strftime("%d.%m.%Y %H:%M:%S"))+"\n")
        
    def setRecordType(_recordType):
        global lastRecordType, recordType
        lastRecordType = recordType
        recordType = _recordType
        
    def restoreRecordType():
        global recordType
        recordType = lastRecordType
        
    def saveAllRecords():
        global recordContents, isSetedTitle
        if Universals.MySettings.keys().count("isSaveActions")==0 or Universals.getBoolValue("isSaveActions"):
            if InputOutputs.isFile(Universals.recordFilePath)==False:
                create()
            setRecordType(1)
            InputOutputs.addToFile(Universals.recordFilePath, recordContents)
            restoreRecordType()
        recordContents = ""
        isSetedTitle = False
    
    def checkSize():
        setRecordType(1)
        InputOutputs.fixToSize(Universals.recordFilePath, (int(Universals.MySettings["maxRecordFileSize"])*1024))
        restoreRecordType()
        
    def read(_isShowErrorDialog=True):
        if InputOutputs.isFile(Universals.recordFilePath)==True:
            return InputOutputs.readFromFile(Universals.recordFilePath)
        else:
            if _isShowErrorDialog:
                import Dialogs
                Dialogs.showError(translate("Records", "Cannot Find The Record File"), 
                            translate("Records", "Record file not found."))
            return False
            
    def clearRecords():
        InputOutputs.writeToFile(Universals.recordFilePath, str(translate("Records", "Hamsi Manager Record File - Time Clear : ")) + str(time.strftime("%d.%m.%Y %H:%M:%S"))+"\n")
        try:dialog.close()
        except:pass
        
    def showInWindow():
        from MyObjects import MDialog, MWidget, MVBoxLayout, MHBoxLayout, MTextEdit, MTextOption, MPushButton, SIGNAL, MObject, trForUI
        import Organizer
        global dialog
        recordString = read()
        if recordString != False:
            dialog = MDialog(Universals.MainWindow)
            if Universals.isActivePyKDE4==True:
                dialog.setButtons(MDialog.None)
            dialog.setWindowTitle(translate("Records", "Last Records"))
            pnlMain = MWidget(dialog)
            vblMain = MVBoxLayout(pnlMain)
            info = MTextEdit()
            info.setPlainText(trForUI(recordString))
            info.setWordWrapMode(MTextOption.ManualWrap)
            pbtnClose = MPushButton(translate("Records", "OK"))
            pbtnClear = MPushButton(translate("Records", "Clear"))
            MObject.connect(pbtnClose, SIGNAL("clicked()"), dialog.close)
            MObject.connect(pbtnClear, SIGNAL("clicked()"), clearRecords)
            vblMain.addWidget(info)
            hblBox = MHBoxLayout()
            hblBox.addWidget(pbtnClear)
            hblBox.addWidget(pbtnClose)
            vblMain.addLayout(hblBox)
            if Universals.isActivePyKDE4==True:
                dialog.setMainWidget(pnlMain)
            else:
                dialog.setLayout(vblMain)
            dialog.setMinimumSize(550, 400)
            dialog.show()
            
            
            
