# -*- coding: utf-8 -*-

import Organizer
import InputOutputs
from InputOutputs import Covers
from MyObjects import *
from Details import TextDetails
import Dialogs
                
class CoverTable():
    global _refreshSubTable, _refreshSubTableColumns, _saveSubTable, _subTableCellClicked, _subTableCellDoubleClicked, _subShowDetails
    def __init__(self,_table):
        _table.specialTollsBookmarkPointer = "cover"
        _table.hiddenTableColumnsSettingKey = "hiddenCoverTableColumns"
        _table.refreshSubTable = _refreshSubTable
        _table.refreshSubTableColumns = _refreshSubTableColumns
        _table.saveSubTable = _saveSubTable
        _table.subTableCellClicked = _subTableCellClicked
        _table.subTableCellDoubleClicked = _subTableCellDoubleClicked
        _table.subShowDetails = _subShowDetails
        _table.fileValues = InputOutputs.allFilesAndDirectories 
        _table.fileDetails = Covers.currentFilesAndFoldersValues
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
        pass
        #TextDetails.TextDetails(Covers.InputOutputs.currentDirectoryPath + "/" + Covers.currentFilesAndFoldersValues[_fileNo][1], self.isOpenDetailsOnNewWindow.isChecked())
        
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
                        ) % Organizer.getLink(Covers.InputOutputs.currentDirectoryPath+"/"+Covers.currentFilesAndFoldersValues[_row][1]))
       
    def _refreshSubTableColumns(self):
        self.tableColumns=[translate("SubFolderTable", "Directory"), 
                            translate("SubFolderTable", "Directory Name"), 
                            translate("SubFolderTable", "Current Cover"), 
                            translate("SubFolderTable", "Source Cover"), 
                            translate("SubFolderTable", "Destination Cover")]
        self.tableColumnsKey=["Directory", "Directory Name", "Current Cover", "Source Cover", "Destination Cover"]
        
    def _saveSubTable(self):
        returnValue = Covers.writeCovers(self)
        self.changedValueNumber = Covers.changedValueNumber
        return returnValue
        
    def _refreshSubTable(self, _path):
        Covers.readCovers(_path)
        self.fileValues = InputOutputs.allFilesAndDirectories 
        self.fileDetails = Covers.currentFilesAndFoldersValues
        self.setRowCount(len(Covers.currentFilesAndFoldersValues))
        startRowNo, rowStep = 0, 1
        for dirNo in range(startRowNo, self.rowCount(), rowStep):
            for itemNo in range(0,5):
                if itemNo==2 or itemNo==3:
                    newString = Organizer.showWithIncorrectChars(Covers.currentFilesAndFoldersValues[dirNo][itemNo])
                else:
                    newString = Organizer.emend(Covers.currentFilesAndFoldersValues[dirNo][itemNo], True)
                if 1<itemNo and itemNo<5:
                    newString = newString.replace(_path + "/" + Covers.currentFilesAndFoldersValues[dirNo][1], ".")
                item = MTableWidgetItem(newString.decode("utf-8"))
                item.setStatusTip(item.text())
                self.setItem(dirNo,itemNo,item)
                if itemNo!=2 and itemNo!=3 and str(Covers.currentFilesAndFoldersValues[dirNo][itemNo])!=str(newString) and str(Covers.currentFilesAndFoldersValues[dirNo][itemNo])!=str(_path + "/" + Covers.currentFilesAndFoldersValues[dirNo][1] + newString[1:]) and str(Covers.currentFilesAndFoldersValues[dirNo][itemNo])!="None":
                    self.item(dirNo,itemNo).setBackground(MBrush(MColor(142,199,255)))
                    self.item(dirNo,itemNo).setToolTip(Organizer.showWithIncorrectChars(Covers.currentFilesAndFoldersValues[dirNo][itemNo]).decode("utf-8"))
            if Covers.currentFilesAndFoldersValues[dirNo][5]==False:
                self.item(dirNo,2).setBackground(MBrush(MColor(255,163,163)))
                    

          
