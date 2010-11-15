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
from InputOutputs import Files
from MyObjects import *
from Details import TextDetails
import Dialogs
                
class FileTable():
    def __init__(self, _table):
        self.Table = _table
        self.specialTollsBookmarkPointer = "file"
        self.hiddenTableColumnsSettingKey = "hiddenFileTableColumns"
        self.refreshColumns()
        
    def showDetails(self, _fileNo, _infoNo):
        TextDetails.TextDetails(InputOutputs.currentDirectoryPath+"/"+Files.currentFilesAndFoldersValues[_fileNo][1],self.Table.isOpenDetailsOnNewWindow.isChecked())
    
    def cellClicked(self,_row,_column):
        for row_no in range(self.Table.rowCount()):
            self.Table.setRowHeight(row_no,30)
        if len(self.Table.currentItem().text())*8>self.Table.columnWidth(_column):
            self.Table.setColumnWidth(_column,len(self.Table.currentItem().text())*8)
        
    def cellDoubleClicked(self,_row,_column):
        try:
            if self.Table.tbIsRunOnDoubleClick.isChecked()==True:
                self.showDetails(_row, _column)
        except:
            Dialogs.showError(translate("FileTable", "Cannot Open File"), 
                        str(translate("FileTable", "\"%s\" : cannot be opened. Please make sure that you selected a text file.")
                        ) % Organizer.getLink(InputOutputs.currentDirectoryPath+"/"+Files.currentFilesAndFoldersValues[_row][1]))
       
    def refreshColumns(self):
        self.Table.tableColumns=[translate("FileTable", "Directory"), 
                            translate("FileTable", "File Name")]
        self.Table.tableColumnsKey=["Directory", "File Name"]
        
    def save(self):
        returnValue = Files.writeFiles(self.Table)
        self.Table.changedValueNumber = Files.changedValueNumber
        return returnValue
        
    def refresh(self, _path):
        Files.readFiles(_path)
        self.fileDetails = Files.currentFilesAndFoldersValues
        if Universals.isShowOldValues==True:
            n=2
            tableRows=[]
            for row in range(0,len(Files.currentFilesAndFoldersValues)*2):
                tableRows.append(str(int(n/2)))
                n+=1
            self.Table.setRowCount(len(Files.currentFilesAndFoldersValues)*2)
            self.Table.setVerticalHeaderLabels(tableRows)
            startRowNo, rowStep = 1, 2
            for fileNo in range(0,len(Files.currentFilesAndFoldersValues)*2,2):
                for itemNo in range(0,2):
                    item = MTableWidgetItem(Organizer.showWithIncorrectChars(Files.currentFilesAndFoldersValues[fileNo/2][itemNo]).decode("utf-8"))
                    item.setStatusTip(item.text())
                    self.Table.setItem(fileNo,itemNo,item)      
        else:
            self.Table.setRowCount(len(Files.currentFilesAndFoldersValues))
            startRowNo, rowStep = 0, 1
        for fileNo in range(startRowNo,self.Table.rowCount(),rowStep):
            if Universals.isShowOldValues==True:
                realFileNo=fileNo/2
            else:
                realFileNo=fileNo
            for itemNo in range(0,2):
                if itemNo==0:
                    newString = Organizer.emend(Files.currentFilesAndFoldersValues[realFileNo][itemNo], "directory")
                else:
                    newString = Organizer.emend(Files.currentFilesAndFoldersValues[realFileNo][itemNo], "file")
                item = MTableWidgetItem(newString.decode("utf-8"))
                item.setStatusTip(item.text())
                self.Table.setItem(fileNo,itemNo,item)
                if str(Files.currentFilesAndFoldersValues[realFileNo][itemNo])!=str(newString) and str(Files.currentFilesAndFoldersValues[realFileNo][itemNo])!="None":
                    self.Table.item(fileNo,itemNo).setBackground(MBrush(MColor(142,199,255)))
                    self.Table.item(fileNo,itemNo).setToolTip(Organizer.showWithIncorrectChars(Files.currentFilesAndFoldersValues[realFileNo][itemNo]).decode("utf-8"))
                    
    def correctTable(self):
        if Universals.isShowOldValues==True:
            startRowNo, rowStep = 1, 2
        else:
            startRowNo, rowStep = 0, 1
        for rowNo in range(startRowNo,self.Table.rowCount(),rowStep):
            if Universals.isShowOldValues==True:
                realRowNo=rowNo/2
            else:
                realRowNo=rowNo
            for itemNo in range(self.Table.columnCount()):
                if itemNo==0:
                    newString = Organizer.emend(unicode(self.Table.item(rowNo,itemNo).text(),"utf-8"), "directory")
                else:
                    newString = Organizer.emend(unicode(self.Table.item(rowNo,itemNo).text(),"utf-8"), "file")
                self.Table.item(rowNo,itemNo).setText(str(newString).decode("utf-8"))
          
