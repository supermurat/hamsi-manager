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
import SearchEngines
from MyObjects import *
from Details import AmarokArtistDetails
import Universals
import Dialogs
import Taggers
from time import gmtime
import Records

class Content():
    global readContents, writeContents
    
    def readContents(_directoryPath):
        currentTableContentValues = []
        Universals.startThreadAction()
        import Amarok
        Dialogs.showState(translate("AmarokCoverTable", "Checking For Amarok..."), 0, 2)
        if Amarok.checkAmarok():
            Dialogs.showState(translate("AmarokCoverTable", "Getting Values From Amarok"), 1, 2)
            isContinueThreadAction = Universals.isContinueThreadAction()
            if isContinueThreadAction:
                from Amarok import Operations
                artistValues = Operations.getAllArtistsValues()
                Dialogs.showState(translate("AmarokCoverTable", "Values Are Being Processed"), 2, 2)
                isContinueThreadAction = Universals.isContinueThreadAction()
                if isContinueThreadAction:
                    if artistValues!=None:
                        allItemNumber = len(artistValues)
                        musicFileNo = 0
                        for musicFileRow in artistValues:
                            isContinueThreadAction = Universals.isContinueThreadAction()
                            if isContinueThreadAction:
                                content = {}
                                content["id"] = musicFileRow["id"]
                                content["name"] = musicFileRow["name"]
                                currentTableContentValues.append(content)
                            else:
                                allItemNumber = musicFileNo+1
                            Dialogs.showState(translate("InputOutputs/Covers", "Reading Music File Informations"),
                                              musicFileNo+1,allItemNumber, True) 
                            musicFileNo += 1
                            if isContinueThreadAction==False:
                                break
        Universals.finishThreadAction()
        return currentTableContentValues
    
    def writeContents(_table):
        _table.changedValueNumber = 0
        changedArtistValues=[]
        Universals.startThreadAction()
        import Amarok
        allItemNumber = len(_table.currentTableContentValues)
        Dialogs.showState(translate("InputOutputs/Musics", "Writing Music Tags"),0,allItemNumber, True)
        for rowNo in range(_table.rowCount()):
            isContinueThreadAction = Universals.isContinueThreadAction()
            if isContinueThreadAction:
                if _table.isChangableItem(rowNo, 1, str(_table.currentTableContentValues[rowNo]["name"])):
                    changedArtistValues.append({})
                    changedArtistValues[-1]["id"] = str(_table.currentTableContentValues[rowNo]["id"])
                    value = str(_table.item(rowNo, 1).text())
                    changedArtistValues[-1]["name"] = value
                    Records.add(str(translate("AmarokDatabaseCorrector", "Artist")), str(_table.currentTableContentValues[rowNo]["name"]), value)
                    _table.changedValueNumber += 1
            else:
                allItemNumber = rowNo+1
            Dialogs.showState(translate("InputOutputs/Musics", "Writing Music Tags"),rowNo+1,allItemNumber, True)
            if isContinueThreadAction==False:
                break
        Universals.finishThreadAction()
        from Amarok import Operations
        Operations.changeArtistValues(changedArtistValues)
        return True



class AmarokDatabaseCorrector():
    def __init__(self, _table):
        self.Table = _table
        self.specialTollsBookmarkPointer = "ADCArtist"
        self.hiddenTableColumnsSettingKey = "hiddenAmarokDatabaseCorrectorColumns"
        self.refreshColumns()
        
    def showDetails(self, _fileNo, _infoNo):
        AmarokArtistDetails.AmarokArtistDetails(self.Table.currentTableContentValues[_fileNo]["id"],
                                      self.Table.isOpenDetailsOnNewWindow.isChecked())
    
    def cellClicked(self,_row,_column):
        cellLenght = len(self.Table.currentItem().text())*8
        if cellLenght>self.Table.columnWidth(_column):
            self.Table.setColumnWidth(_column,cellLenght)
        
    def cellDoubleClicked(self,_row,_column):
        if self.Table.tbIsRunOnDoubleClick.isChecked()==True:
            self.showDetails(_row, _column)
       
    def refreshColumns(self):
        self.Table.tableColumns = [translate("AmarokDatabaseCorrector", "Current Artist"), translate("AmarokDatabaseCorrector", "Corrected Artist")]
        self.Table.tableColumnsKey = ["currentArtist", "correctedArtist"]
        
    def save(self):
        AmarokArtistDetails.closeAllAmarokArtistDialogs()
        return writeContents(self.Table)
        
    def refresh(self, _path):
        self.Table.currentTableContentValues = readContents(_path)
        self.Table.setRowCount(len(self.Table.currentTableContentValues))
        for rowNo in range(self.Table.rowCount()):
            newString = self.Table.currentTableContentValues[rowNo]["name"]
            item = self.Table.createTableWidgetItem(newString, newString)
            self.Table.setItem(rowNo, 0, item)
            newString = Organizer.emend(self.Table.currentTableContentValues[rowNo]["name"])
            item = self.Table.createTableWidgetItem(newString, self.Table.currentTableContentValues[rowNo]["name"])
            self.Table.setItem(rowNo, 1, item)
                        
    def correctTable(self):
        for rowNo in range(self.Table.rowCount()):
            for itemNo in range(self.Table.columnCount()):
                if itemNo==0:
                    continue                
                elif itemNo==1:
                    newString = Organizer.emend(str(self.Table.item(rowNo,itemNo).text()))
                self.Table.item(rowNo,itemNo).setText(trForUI(newString))
                
