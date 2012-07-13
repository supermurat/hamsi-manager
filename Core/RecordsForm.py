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
from Core import Records
import InputOutputs
import Options

class RecordsForm(MDialog):
    global checkRecordsForm, codesOfUser, reFillCodesOfUser
    def __init__(self, _parent):
        MDialog.__init__(self, _parent)
        if Universals.isActivePyKDE4==True:
            self.setButtons(MDialog.NoDefault)
        pbtnClose = MPushButton(translate("RecordsForm", "Close"))
        pbtnClear = MPushButton(translate("RecordsForm", "Clear"))
        self.connect(pbtnClose,SIGNAL("clicked()"), self.close)
        self.connect(pbtnClear,SIGNAL("clicked()"), self.clear)
        lblRecordList = MLabel(translate("RecordsForm", "Record File"))
        self.recordsList = [translate("RecordsForm", "Current Records")] + Records.getBackupRecordsList()
        self.cbRecordsList = Options.MyComboBox(self, self.recordsList, _currentIndexChanged=self.getFromRecordList)
        self.teRecords = MTextEdit()
        self.teRecords.setWordWrapMode(MTextOption.ManualWrap)
        self.setRecordsFile()
        pnlMain = MWidget(self)
        vblMain = MVBoxLayout(pnlMain)
        hbox = MHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(pbtnClear,1)
        hbox.addWidget(pbtnClose,1)
        hbox1 = MHBoxLayout()
        hbox1.addWidget(lblRecordList)
        hbox1.addWidget(self.cbRecordsList)
        vblMain.addLayout(hbox1)
        vblMain.addWidget(self.teRecords)
        vblMain.addLayout(hbox)
        if Universals.isActivePyKDE4==True:
            self.setMainWidget(pnlMain)
        else:
            self.setLayout(vblMain)
        self.setWindowTitle(translate("RecordsForm", "Last Records"))
        self.setWindowIcon(MIcon("Images:lastActions.png"))
        self.setMinimumWidth(500)
        self.setMinimumHeight(450)
        self.show()
        
    def setRecordsFile(self, _filePath=None):
        if _filePath is None:
            self.teRecords.setPlainText(trForUI(Records.read()))
        else:
            self.teRecords.setPlainText(trForUI(Records.read(_filePath)))
            
    def getFromRecordList(self, _index = None):
        if self.cbRecordsList.currentIndex()==0:
            self.setRecordsFile()
        else:
            recordFilePath = self.recordsList[self.cbRecordsList.currentIndex()]
            self.setRecordsFile(InputOutputs.joinPath(Universals.oldRecordsDirectoryPath, recordFilePath))
            
    def clear(self):
        answer = Dialogs.ask(translate("RecordsForm", "Are You Sure?"),
                        translate("RecordsForm", "Are you sure you want to remove this record file?"))
        if answer==Dialogs.Yes:
            if self.cbRecordsList.currentIndex()==0:
                Records.clearRecords()
            else:
                recordFilePath = self.recordsList[self.cbRecordsList.currentIndex()]
                InputOutputs.removeFile(InputOutputs.joinPath(Universals.oldRecordsDirectoryPath, recordFilePath))
                self.recordsList = [translate("RecordsForm", "Current Records")] + Records.getBackupRecordsList()
                self.cbRecordsList.clear()
                self.cbRecordsList.addItems(self.recordsList)
            self.setRecordsFile()
        
        
