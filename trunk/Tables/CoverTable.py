# -*- coding: utf-8 -*-

import Organizer
import InputOutputs
from InputOutputs import Covers
from MyObjects import *
from Details import CoverDetails
import Dialogs
import Tables
import ReportBug
                
class CoverTable():
    global _refreshSubTable, _refreshSubTableColumns, _saveSubTable, _subTableCellClicked, _subTableCellDoubleClicked, _subShowDetails, _correctSubTable, _getFromAmarok
    def __init__(self,_table):
        _table.specialTollsBookmarkPointer = "cover"
        _table.hiddenTableColumnsSettingKey = "hiddenCoverTableColumns"
        _table.refreshSubTable = _refreshSubTable
        _table.refreshSubTableColumns = _refreshSubTableColumns
        _table.saveSubTable = _saveSubTable
        _table.subTableCellClicked = _subTableCellClicked
        _table.subTableCellDoubleClicked = _subTableCellDoubleClicked
        _table.subShowDetails = _subShowDetails
        _table.correctSubTable = _correctSubTable
        _table.fileDetails = Covers.currentFilesAndFoldersValues
        _table.getFromAmarok = _getFromAmarok
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
        pbtnGetFromAmarok = MPushButton(translate("CoverTable", "Get From Amarok"))
        MObject.connect(pbtnGetFromAmarok, SIGNAL("clicked()"), self.getFromAmarok)
        hbox1.addWidget(pbtnGetFromAmarok, 1)
        hbox1.addWidget(self.pbtnSave, 2)
        self.hblBox.addLayout(hbox1)
        
    def _subShowDetails(self, _fileNo, _infoNo):
        directoryPathOfCover = InputOutputs.IA.currentDirectoryPath + "/" + Covers.currentFilesAndFoldersValues[_fileNo][1]
        coverValues = [directoryPathOfCover, 
                       InputOutputs.IA.getRealPath(str(self.item(_fileNo, 2).text()), directoryPathOfCover), 
                       InputOutputs.IA.getRealPath(str(self.item(_fileNo, 3).text()), directoryPathOfCover), 
                       InputOutputs.IA.getRealPath(str(self.item(_fileNo, 4).text()), directoryPathOfCover)]
        CoverDetails.CoverDetails(coverValues, self.isOpenDetailsOnNewWindow.isChecked(), _infoNo)
        
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
            Dialogs.showError(translate("CoverTable", "Cannot Open File"), 
                        str(translate("CoverTable", "\"%s\" : cannot be opened. Please make sure that you selected a text file.")
                        ) % Organizer.getLink(InputOutputs.IA.currentDirectoryPath + "/" + Covers.currentFilesAndFoldersValues[_row][1]))
       
    def _refreshSubTableColumns(self):
        self.tableColumns=[translate("CoverTable", "Directory"), 
                            translate("CoverTable", "Directory Name"), 
                            translate("CoverTable", "Current Cover"), 
                            translate("CoverTable", "Source Cover"), 
                            translate("CoverTable", "Destination Cover")]
        self.tableColumnsKey=["Directory", "Directory Name", "Current Cover", "Source Cover", "Destination Cover"]
        
    def _saveSubTable(self):
        returnValue = Covers.writeCovers(self)
        self.changedValueNumber = Covers.changedValueNumber
        return returnValue
        
    def _refreshSubTable(self, _path):
        Covers.readCovers(_path)
        self.fileDetails = Covers.currentFilesAndFoldersValues
        self.setRowCount(len(Covers.currentFilesAndFoldersValues))
        startRowNo, rowStep = 0, 1
        for dirNo in range(startRowNo, self.rowCount(), rowStep):
            for itemNo in range(0,5):
                if itemNo==0 or itemNo==1:
                    newString = Organizer.emend(Covers.currentFilesAndFoldersValues[dirNo][itemNo], "directory")
                elif itemNo==2 or itemNo==3:
                    newString = Organizer.showWithIncorrectChars(Covers.currentFilesAndFoldersValues[dirNo][itemNo])
                else:
                    newString = Organizer.emend(Covers.currentFilesAndFoldersValues[dirNo][itemNo], "file")
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
                    
    def _correctSubTable(self):
        for rowNo in range(self.rowCount()):
            for itemNo in range(self.columnCount()):
                if itemNo==0 or itemNo==1:
                    newString = Organizer.emend(unicode(self.item(rowNo,itemNo).text(),"utf-8"), "directory")
                elif itemNo==2 or itemNo==3:
                    newString = Organizer.showWithIncorrectChars(unicode(self.item(rowNo,itemNo).text(),"utf-8"))
                else:
                    newString = Organizer.emend(unicode(self.item(rowNo,itemNo).text(),"utf-8"), "file")
                self.item(rowNo,itemNo).setText(str(newString).decode("utf-8"))
        
    def _getFromAmarok():
        try:
            import Amarok
            Dialogs.showState(translate("CoverTable", "Checking For Amarok..."), 0, 2)
            if Amarok.checkAmarok():
                Dialogs.showState(translate("CoverTable", "Getting Values From Amarok"), 1, 2)
                table = Universals.MainWindow.Table
                from Amarok import Commands
                directoriesAndValues = Commands.getDirectoriesAndValues()
                Dialogs.showState(translate("CoverTable", "Values Are Being Processed"), 2, 2)
                if directoriesAndValues!=None:
                    for rowNo in range(table.rowCount()):
                        if Tables.checkHiddenColumn(3) and Tables.checkHiddenColumn(4):
                            if table.item(rowNo,3).isSelected()==Universals.isChangeSelected or Universals.isChangeAll==True:
                                directoryPath = str(InputOutputs.IA.getDirName(InputOutputs.IA.currentDirectoryPath))+"/"+unicode(table.item(rowNo,0).text()).encode("utf-8")+"/"+unicode(table.item(rowNo,1).text()).encode("utf-8")
                                if directoryPath in directoriesAndValues:
                                    directoryAndValues = directoriesAndValues[directoryPath]
                                    table.item(rowNo,3).setText(directoryAndValues["coverPath"][0].replace(directoryPath, "."))
                                    table.item(rowNo,4).setText("./" + Organizer.getIconName(
                                                            directoryAndValues["Artist"][0], 
                                                            directoryAndValues["Album"][0], 
                                                            directoryAndValues["Genre"][0], 
                                                            directoryAndValues["Year"][0]))
        except:
            error = ReportBug.ReportBug()
            error.show()
        