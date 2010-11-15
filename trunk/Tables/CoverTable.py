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
from InputOutputs import Covers
from MyObjects import *
from Details import CoverDetails
import Dialogs
                
class CoverTable():
    def __init__(self, _table):
        self.Table = _table
        self.specialTollsBookmarkPointer = "cover"
        self.hiddenTableColumnsSettingKey = "hiddenCoverTableColumns"
        self.refreshColumns()
        pbtnGetFromAmarok = MPushButton(translate("CoverTable", "Get From Amarok"))
        MObject.connect(pbtnGetFromAmarok, SIGNAL("clicked()"), self.getFromAmarok)
        self.Table.hblBox.insertWidget(self.Table.hblBox.count()-1, pbtnGetFromAmarok)
        
    def showDetails(self, _fileNo, _infoNo):
        directoryPathOfCover = InputOutputs.currentDirectoryPath + "/" + Covers.currentFilesAndFoldersValues[_fileNo][1]
        coverValues = [directoryPathOfCover, 
                       InputOutputs.IA.getRealPath(str(self.Table.item(_fileNo, 2).text()), directoryPathOfCover), 
                       InputOutputs.IA.getRealPath(str(self.Table.item(_fileNo, 3).text()), directoryPathOfCover), 
                       InputOutputs.IA.getRealPath(str(self.Table.item(_fileNo, 4).text()), directoryPathOfCover)]
        CoverDetails.CoverDetails(coverValues, self.Table.isOpenDetailsOnNewWindow.isChecked(), _infoNo)
        
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
            Dialogs.showError(translate("CoverTable", "Cannot Open File"), 
                        str(translate("CoverTable", "\"%s\" : cannot be opened. Please make sure that you selected a text file.")
                        ) % Organizer.getLink(InputOutputs.currentDirectoryPath + "/" + Covers.currentFilesAndFoldersValues[_row][1]))
       
    def refreshColumns(self):
        self.Table.tableColumns=[translate("CoverTable", "Directory"), 
                            translate("CoverTable", "Directory Name"), 
                            translate("CoverTable", "Current Cover"), 
                            translate("CoverTable", "Source Cover"), 
                            translate("CoverTable", "Destination Cover")]
        self.Table.tableColumnsKey=["Directory", "Directory Name", "Current Cover", "Source Cover", "Destination Cover"]
        
    def save(self):
        returnValue = Covers.writeCovers(self.Table)
        self.Table.changedValueNumber = Covers.changedValueNumber
        return returnValue
        
    def refresh(self, _path):
        Covers.readCovers(_path)
        self.fileDetails = Covers.currentFilesAndFoldersValues
        self.Table.setRowCount(len(Covers.currentFilesAndFoldersValues))
        startRowNo, rowStep = 0, 1
        for dirNo in range(startRowNo, self.Table.rowCount(), rowStep):
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
                self.Table.setItem(dirNo,itemNo,item)
                if itemNo!=2 and itemNo!=3 and str(Covers.currentFilesAndFoldersValues[dirNo][itemNo])!=str(newString) and str(Covers.currentFilesAndFoldersValues[dirNo][itemNo])!=str(_path + "/" + Covers.currentFilesAndFoldersValues[dirNo][1] + newString[1:]) and str(Covers.currentFilesAndFoldersValues[dirNo][itemNo])!="None":
                    self.Table.item(dirNo,itemNo).setBackground(MBrush(MColor(142,199,255)))
                    self.Table.item(dirNo,itemNo).setToolTip(Organizer.showWithIncorrectChars(Covers.currentFilesAndFoldersValues[dirNo][itemNo]).decode("utf-8"))
            if Covers.currentFilesAndFoldersValues[dirNo][5]==False:
                self.Table.item(dirNo,2).setBackground(MBrush(MColor(255,163,163)))
                    
    def correctTable(self):
        for rowNo in range(self.Table.rowCount()):
            for itemNo in range(self.Table.columnCount()):
                if itemNo==0 or itemNo==1:
                    newString = Organizer.emend(unicode(self.Table.item(rowNo,itemNo).text(),"utf-8"), "directory")
                elif itemNo==2 or itemNo==3:
                    newString = Organizer.showWithIncorrectChars(unicode(self.Table.item(rowNo,itemNo).text(),"utf-8"))
                else:
                    newString = Organizer.emend(unicode(self.Table.item(rowNo,itemNo).text(),"utf-8"), "file")
                self.Table.item(rowNo,itemNo).setText(str(newString).decode("utf-8"))
        
    def getFromAmarok(self):
        try:
            import Amarok
            Dialogs.showState(translate("CoverTable", "Checking For Amarok..."), 0, 2)
            if Amarok.checkAmarok():
                Dialogs.showState(translate("CoverTable", "Getting Values From Amarok"), 1, 2)
                from Amarok import Commands
                directoriesAndValues = Commands.getDirectoriesAndValues()
                Dialogs.showState(translate("CoverTable", "Values Are Being Processed"), 2, 2)
                if directoriesAndValues!=None:
                    for rowNo in range(self.Table.rowCount()):
                        if self.Table.checkHiddenColumn(3) and self.Table.checkHiddenColumn(4):
                            if self.Table.item(rowNo,3).isSelected()==Universals.isChangeSelected or Universals.isChangeAll==True:
                                directoryPath = str(InputOutputs.IA.getDirName(InputOutputs.currentDirectoryPath))+"/"+unicode(self.Table.item(rowNo,0).text()).encode("utf-8")+"/"+unicode(self.Table.item(rowNo,1).text()).encode("utf-8")
                                if directoryPath in directoriesAndValues:
                                    directoryAndValues = directoriesAndValues[directoryPath]
                                    self.Table.item(rowNo,3).setText(directoryAndValues["coverPath"][0].replace(directoryPath, "."))
                                    self.Table.item(rowNo,4).setText("./" + Organizer.getIconName(
                                                            directoryAndValues["Artist"][0], 
                                                            directoryAndValues["Album"][0], 
                                                            directoryAndValues["Genre"][0], 
                                                            directoryAndValues["Year"][0]))
        except:
            import ReportBug
            error = ReportBug.ReportBug()
            error.show()
        
