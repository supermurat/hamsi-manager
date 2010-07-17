# -*- coding: utf-8 -*-

import Organizer
import InputOutputs
from InputOutputs import SubFolders
from MyObjects import *
from Details import TextDetails
import Dialogs
                
class SubFolderTable():
    global _refreshSubTable, _refreshSubTableColumns, _saveSubTable, _subTableCellClicked, _subTableCellDoubleClicked, _subShowDetails
    def __init__(self,_table):
        _table.specialTollsBookmarkPointer = "subfolder"
        _table.hiddenTableColumnsSettingKey = "hiddenSubFolderTableColumns"
        _table.refreshSubTable = _refreshSubTable
        _table.refreshSubTableColumns = _refreshSubTableColumns
        _table.saveSubTable = _saveSubTable
        _table.subTableCellClicked = _subTableCellClicked
        _table.subTableCellDoubleClicked = _subTableCellDoubleClicked
        _table.subShowDetails = _subShowDetails
        _table.fileValues = InputOutputs.allFilesAndDirectories 
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
        TextDetails.TextDetails(SubFolders.InputOutputs.currentDirectoryPath+"/"+SubFolders.currentFilesAndFoldersValues[_fileNo][1],self.isOpenDetailsOnNewWindow.isChecked())
        
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
                        ) % Organizer.getLink(SubFolders.InputOutputs.currentDirectoryPath+"/"+SubFolders.currentFilesAndFoldersValues[_row][1]))
       
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
        self.fileValues = InputOutputs.allFilesAndDirectories 
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
                newString = Organizer.emend(SubFolders.currentFilesAndFoldersValues[realFileNo][itemNo], True)
                item = MTableWidgetItem(newString.decode("utf-8"))
                item.setStatusTip(item.text())
                self.setItem(fileNo,itemNo,item)
                if str(SubFolders.currentFilesAndFoldersValues[realFileNo][itemNo])!=str(newString) and str(SubFolders.currentFilesAndFoldersValues[realFileNo][itemNo])!="None":
                    self.item(fileNo,itemNo).setBackground(MBrush(MColor(142,199,255)))
                    self.item(fileNo,itemNo).setToolTip(Organizer.showWithIncorrectChars(SubFolders.currentFilesAndFoldersValues[realFileNo][itemNo]).decode("utf-8"))
                    

          
