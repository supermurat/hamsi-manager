## This file is part of HamsiManager.
## 
## Copyright (c) 2010 - 2013 Murat Demir <mopened@gmail.com>      
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

from Core import Organizer
import InputOutputs
import SearchEngines
from Core.MyObjects import *
from Details import AmarokArtistDetails
from Core import Universals
from Core import Dialogs
import Taggers
from time import gmtime
from Core import Records

class AmarokArtistTable():
    def __init__(self, _table):
        from Amarok import Filter
        self.Table = _table
        self.keyName = "ADCArtist"
        self.amarokFilterKeyName = "AmarokFilterArtistTable"
        self.hiddenTableColumnsSettingKey = "hiddenAmarokArtistTableColumns"
        self.refreshColumns()
        self.wFilter = Filter.FilterWidget(self.Table, self.amarokFilterKeyName)
        Universals.MainWindow.MainLayout.addWidget(self.wFilter)
        
    def readContents(self, _directoryPath):
        currentTableContentValues = []
        Universals.startThreadAction()
        import Amarok
        Dialogs.showState(translate("AmarokArtistTable", "Checking For Amarok..."), 0, 2)
        if Amarok.checkAmarok():
            Dialogs.showState(translate("AmarokArtistTable", "Getting Values From Amarok"), 1, 2)
            isContinueThreadAction = Universals.isContinueThreadAction()
            if isContinueThreadAction:
                from Amarok import Operations
                artistValues = Operations.getAllArtistsValues(Universals.MySettings[self.amarokFilterKeyName])
                Dialogs.showState(translate("AmarokArtistTable", "Values Are Being Processed"), 2, 2)
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
    
    def writeContents(self):
        self.Table.changedValueNumber = 0
        changedArtistValues=[]
        Universals.startThreadAction()
        import Amarok
        allItemNumber = len(self.Table.currentTableContentValues)
        Dialogs.showState(translate("InputOutputs/Musics", "Writing Music Tags"),0,allItemNumber, True)
        for rowNo in range(self.Table.rowCount()):
            isContinueThreadAction = Universals.isContinueThreadAction()
            if isContinueThreadAction:
                if self.Table.isChangableItem(rowNo, 1, str(self.Table.currentTableContentValues[rowNo]["name"])):
                    changedArtistValues.append({})
                    changedArtistValues[-1]["id"] = str(self.Table.currentTableContentValues[rowNo]["id"])
                    value = str(self.Table.item(rowNo, 1).text())
                    changedArtistValues[-1]["name"] = value
                    Records.add(str(translate("AmarokArtistTable", "Artist")), str(self.Table.currentTableContentValues[rowNo]["name"]), value)
                    self.Table.changedValueNumber += 1
            else:
                allItemNumber = rowNo+1
            Dialogs.showState(translate("InputOutputs/Musics", "Writing Music Tags"),rowNo+1,allItemNumber, True)
            if isContinueThreadAction==False:
                break
        Universals.finishThreadAction()
        from Amarok import Operations
        Operations.changeArtistValues(changedArtistValues)
        return True
        
    def showDetails(self, _fileNo, _infoNo):
        AmarokArtistDetails.AmarokArtistDetails(self.Table.currentTableContentValues[_fileNo]["id"], Universals.getBoolValue("isOpenDetailsInNewWindow"))
    
    def cellClicked(self,_row,_column):
        cellLenght = len(self.Table.currentItem().text())*8
        if cellLenght>self.Table.columnWidth(_column):
            self.Table.setColumnWidth(_column,cellLenght)
        
    def cellDoubleClicked(self,_row,_column):
        if Universals.getBoolValue("isRunOnDoubleClick"):
            self.showDetails(_row, _column)
       
    def refreshColumns(self):
        self.Table.tableColumns = [translate("AmarokArtistTable", "Current Artist"), translate("AmarokArtistTable", "Corrected Artist")]
        self.Table.tableColumnsKey = ["currentArtist", "correctedArtist"]
        
    def save(self):
        AmarokArtistDetails.closeAllAmarokArtistDialogs()
        return self.writeContents()
        
    def refresh(self, _path):
        self.Table.currentTableContentValues = self.readContents(_path)
        self.Table.setRowCount(len(self.Table.currentTableContentValues))
        for rowNo in range(self.Table.rowCount()):
            newString = self.Table.currentTableContentValues[rowNo]["name"]
            item = self.Table.createTableWidgetItem(newString, newString)
            self.Table.setItem(rowNo, 0, item)
            newString = Organizer.emend(self.Table.currentTableContentValues[rowNo]["name"])
            item = self.Table.createTableWidgetItem(newString, self.Table.currentTableContentValues[rowNo]["name"])
            self.Table.setItem(rowNo, 1, item)
            if self.Table.currentTableContentValues[rowNo]["name"].strip()=="":
                self.Table.item(rowNo,1).setToolTip(translate("AmarokArtistTable", "This value is NOT changeable!"))
                self.Table.item(rowNo,1).setBackground(MBrush(MColor(255,150,150)))
                self.Table.item(rowNo,1).isNeverChange = True
                        
    def correctTable(self):
        for rowNo in range(self.Table.rowCount()):
            for itemNo in range(self.Table.columnCount()):
                if itemNo==0:
                    continue                
                elif itemNo==1:
                    newString = Organizer.emend(str(self.Table.item(rowNo,itemNo).text()))
                self.Table.item(rowNo,itemNo).setText(trForUI(newString))
          
    def getValueByRowAndColumn(self, _rowNo, _columnNo):
        if _columnNo==0:
            return self.Table.currentTableContentValues[_rowNo]["name"]
        elif _columnNo==1:
            return self.Table.currentTableContentValues[_rowNo]["name"]
        return ""
