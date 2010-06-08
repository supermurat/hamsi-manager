# -*- coding: utf-8 -*-

import Organizer
import InputOutputs
from InputOutputs import Files
from MyObjects import *
from Details import TextDetails
import Dialogs
                
class FileTable():
    global _refreshSubTable, _refreshSubTableColumns, _saveSubTable, _subTableCellClicked, _subTableCellDoubleClicked, _subShowDetails
    def __init__(self,_table):
        _table.specialTollsBookmarkPointer = "file"
        _table.hiddenTableColumnsSettingKey = "hiddenFileTableColumns"
        _table.refreshSubTable = _refreshSubTable
        _table.refreshSubTableColumns = _refreshSubTableColumns
        _table.saveSubTable = _saveSubTable
        _table.subTableCellClicked = _subTableCellClicked
        _table.subTableCellDoubleClicked = _subTableCellDoubleClicked
        _table.subShowDetails = _subShowDetails
        _table.fileValues = InputOutputs.fileNames
        _table.fileDetails = Files.currentFilesAndFoldersValues
        self=_table
        _refreshSubTableColumns(self)
        hbox1 = MHBoxLayout()
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
        TextDetails.TextDetails(Files.InputOutputs.currentDirectoryPath+"/"+Files.currentFilesAndFoldersValues[_fileNo][1],self.isOpenDetailsOnNewWindow.isChecked())
    
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
            Dialogs.showError(translate("FileTable", "Cannot Open File"), 
                        str(translate("FileTable", "\"%s\" : cannot be opened. Please make sure that you selected a text file.")
                        ) % Organizer.getLink(Files.InputOutputs.currentDirectoryPath+"/"+Files.currentFilesAndFoldersValues[_row][1]))
       
    def _refreshSubTableColumns(self):
        self.tableColumns=[translate("FileTable", "Directory"), 
                            translate("FileTable", "File Name")]
        self.tableColumnsKey=["Directory", "File Name"]
        
    def _saveSubTable(self):
        returnValue = Files.writeFiles(self)
        self.changedValueNumber = Files.changedValueNumber
        return returnValue
        
    def _refreshSubTable(self, _path):
        Files.readFiles(_path)
        self.fileValues = InputOutputs.fileNames
        self.fileDetails = Files.currentFilesAndFoldersValues
        if Universals.isShowOldValues==True:
            n=2
            tableRows=[]
            for row in range(0,len(Files.currentFilesAndFoldersValues)*2):
                tableRows.append(str(int(n/2)))
                n+=1
            self.setRowCount(len(Files.currentFilesAndFoldersValues)*2)
            self.setVerticalHeaderLabels(tableRows)
            startRowNo, rowStep = 1, 2
            for fileNo in range(0,len(Files.currentFilesAndFoldersValues)*2,2):
                for itemNo in range(0,2):
                    item = MTableWidgetItem(Organizer.showWithIncorrectChars(Files.currentFilesAndFoldersValues[fileNo/2][itemNo]).decode("utf-8"))
                    item.setStatusTip(item.text())
                    self.setItem(fileNo,itemNo,item)      
        else:
            self.setRowCount(len(Files.currentFilesAndFoldersValues))
            startRowNo, rowStep = 0, 1
        for fileNo in range(startRowNo,self.rowCount(),rowStep):
            if Universals.isShowOldValues==True:
                realFileNo=fileNo/2
            else:
                realFileNo=fileNo
            for itemNo in range(0,2):
                newString = Organizer.emend(Files.currentFilesAndFoldersValues[realFileNo][itemNo], True)
                item = MTableWidgetItem(newString.decode("utf-8"))
                item.setStatusTip(item.text())
                self.setItem(fileNo,itemNo,item)
                if str(Files.currentFilesAndFoldersValues[realFileNo][itemNo])!=str(newString) and str(Files.currentFilesAndFoldersValues[realFileNo][itemNo])!="None":
                    self.item(fileNo,itemNo).setBackground(MBrush(MColor(142,199,255)))
                    self.item(fileNo,itemNo).setToolTip(Organizer.showWithIncorrectChars(Files.currentFilesAndFoldersValues[realFileNo][itemNo]).decode("utf-8"))
                    
        
          
