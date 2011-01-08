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


import Organizer
import InputOutputs
from InputOutputs import SubFolders
from MyObjects import *
from Details import TextDetails
import Dialogs
                
class SubFolderTable():
    global _refreshSubTable, _refreshSubTableColumns, _saveSubTable, _subTableCellClicked, _subTableCellDoubleClicked, _subShowDetails, _correctSubTable
    def __init__(self,_table):
        _table.specialTollsBookmarkPointer = "subfolder"
        _table.hiddenTableColumnsSettingKey = "hiddenSubFolderTableColumns"
        _table.refreshSubTable = _refreshSubTable
        _table.refreshSubTableColumns = _refreshSubTableColumns
        _table.saveSubTable = _saveSubTable
        _table.subTableCellClicked = _subTableCellClicked
        _table.subTableCellDoubleClicked = _subTableCellDoubleClicked
        _table.subShowDetails = _subShowDetails
        _table.correctSubTable = _correctSubTable
        _table.fileDetails = SubFolders.currentFilesAndFoldersValues
        self=_table
        _refreshSubTableColumns(self)
        hbox1 = MHBoxLayout()
        hbox1.addWidget(self.actRefresh)
        hbox1.addWidget(self.tbGoBack)
        hbox1.addWidget(self.tbCreateHistoryPoint)
        hbox1.addWidget(self.tbGoForward)
        hbox1.addWidget(self.tbIsRunOnDoubleClick)
        hbox1.addWidget(self.isOpenDetailsOnNewWindow)
        hbox1.addWidget(self.tbCorrect)
        hbox1.addWidget(self.pbtnShowDetails, 1)
        hbox1.addWidget(self.pbtnSave, 2)
        self.hblBox.addLayout(hbox1)
        
    def _subShowDetails(self, _fileNo, _infoNo):
        TextDetails.TextDetails(InputOutputs.currentDirectoryPath+"/"+SubFolders.currentFilesAndFoldersValues[_fileNo][1],self.isOpenDetailsOnNewWindow.isChecked())
        
    def _subTableCellClicked(self,_row,_column):
        for row_no in range(self.rowCount()):
            self.setRowHeight(row_no,30)
        if len(self.currentItem().text())*8>self.columnWidth(_column):
            self.setColumnWidth(_column,len(self.currentItem().text())*8)
    
    def _subTableCellDoubleClicked(self,_row,_column):
        try:
            if self.tbIsRunOnDoubleClick.isChecked()==True:
                _subShowDetails(self, _row, _column)
        except:
            Dialogs.showError(translate("SubFolderTable", "Cannot Open File"), 
                        str(translate("SubFolderTable", "\"%s\" : cannot be opened. Please make sure that you selected a text file.")
                        ) % Organizer.getLink(InputOutputs.currentDirectoryPath+"/"+SubFolders.currentFilesAndFoldersValues[_row][1]))
       
    def _refreshSubTableColumns(self):
        self.tableColumns=[translate("SubFolderTable", "Directory"), 
                            translate("SubFolderTable", "File Name")]
        self.tableColumnsKey=["Directory", "File Name"]
        
    def _saveSubTable(self):
        returnValue = SubFolders.writeSubFolders(self)
        self.changedValueNumber = SubFolders.changedValueNumber
        return returnValue
        
    def _refreshSubTable(self, _path):
        SubFolders.readSubFolders(_path)
        self.fileDetails = SubFolders.currentFilesAndFoldersValues
        if Universals.isShowOldValues==True:
            n=2
            tableRows=[]
            for row in range(0,len(SubFolders.currentFilesAndFoldersValues)*2):
                tableRows.append(str(int(n/2)))
                n+=1
            self.setRowCount(len(SubFolders.currentFilesAndFoldersValues)*2)
            self.setVerticalHeaderLabels(tableRows)
            startRowNo, rowStep = 1, 2
            for fileNo in range(0,len(SubFolders.currentFilesAndFoldersValues)*2,2):
                for itemNo in range(0,2):
                    item = MTableWidgetItem(Organizer.showWithIncorrectChars(SubFolders.currentFilesAndFoldersValues[fileNo/2][itemNo]).decode("utf-8"))
                    item.setStatusTip(item.text())
                    self.setItem(fileNo,itemNo,item)      
        else:
            self.setRowCount(len(SubFolders.currentFilesAndFoldersValues))
            startRowNo, rowStep = 0, 1
        for fileNo in range(startRowNo,self.rowCount(),rowStep):
            if Universals.isShowOldValues==True:
                realFileNo=fileNo/2
            else:
                realFileNo=fileNo
            for itemNo in range(0,2):
                if itemNo==0:
                    newString = Organizer.emend(SubFolders.currentFilesAndFoldersValues[realFileNo][itemNo], "directory")
                else:
                    newString = Organizer.emend(SubFolders.currentFilesAndFoldersValues[realFileNo][itemNo], "file")
                item = MTableWidgetItem(newString.decode("utf-8"))
                item.setStatusTip(item.text())
                self.setItem(fileNo,itemNo,item)
                if str(SubFolders.currentFilesAndFoldersValues[realFileNo][itemNo])!=str(newString) and str(SubFolders.currentFilesAndFoldersValues[realFileNo][itemNo])!="None":
                    self.item(fileNo,itemNo).setBackground(MBrush(MColor(142,199,255)))
                    self.item(fileNo,itemNo).setToolTip(Organizer.showWithIncorrectChars(SubFolders.currentFilesAndFoldersValues[realFileNo][itemNo]).decode("utf-8"))
                    
    def _correctSubTable(self):
        if Universals.isShowOldValues==True:
            startRowNo, rowStep = 1, 2
        else:
            startRowNo, rowStep = 0, 1
        for rowNo in range(startRowNo,self.rowCount(),rowStep):
            if Universals.isShowOldValues==True:
                realRowNo=rowNo/2
            else:
                realRowNo=rowNo
            for itemNo in range(self.columnCount()):
                if itemNo==0:
                    newString = Organizer.emend(unicode(self.item(rowNo,itemNo).text(),"utf-8"), "directory")
                else:
                    newString = Organizer.emend(unicode(self.item(rowNo,itemNo).text(),"utf-8"), "file")
                self.item(rowNo,itemNo).setText(str(newString).decode("utf-8"))

          