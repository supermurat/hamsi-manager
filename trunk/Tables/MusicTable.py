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
from InputOutputs import Musics
import SearchEngines
from MyObjects import *
from Details import MusicDetails
import Universals
import Dialogs
import Taggers
                
class MusicTable():
    def __init__(self, _table):
        self.Table = _table
        self.specialTollsBookmarkPointer = "music"
        self.hiddenTableColumnsSettingKey = "hiddenMusicTableColumns"
        self.refreshColumns()
        pbtnVerifyTableValues = MPushButton(translate("MusicTable", "Verify Table"))
        pbtnVerifyTableValues.setMenu(SearchEngines.SearchEngines(self.Table))
        self.Table.mContextMenu.addMenu(SearchEngines.SearchEngines(self.Table, True))
        self.isPlayNow = MToolButton()
        self.isPlayNow.setToolTip(translate("MusicTable", "Play Now"))
        self.isPlayNow.setIcon(MIcon("Images:playNow.png"))
        self.isPlayNow.setCheckable(True)
        self.isPlayNow.setAutoRaise(True)
        self.isPlayNow.setChecked(Universals.getBoolValue("isPlayNow"))
        self.Table.hblBox.insertWidget(self.Table.hblBox.count()-3, self.isPlayNow)
        self.Table.hblBox.insertWidget(self.Table.hblBox.count()-1, pbtnVerifyTableValues)
        
    def showDetails(self, _fileNo, _infoNo):
        MusicDetails.MusicDetails(InputOutputs.currentDirectoryPath+"/"+Musics.currentFilesAndFoldersValues[_fileNo][1],
                                      self.Table.isOpenDetailsOnNewWindow.isChecked(),self.isPlayNow.isChecked(),
                                      _infoNo)
    
    def cellClicked(self,_row,_column):
        for row_no in range(self.Table.rowCount()):
            self.Table.setRowHeight(row_no,30)
        if len(self.Table.currentItem().text())*8>self.Table.columnWidth(_column):
            self.Table.setColumnWidth(_column,len(self.Table.currentItem().text())*8)
        self.Table.setColumnWidth(8,100)
        self.Table.setColumnWidth(9,100)
        if _column==8 or _column==9:
            self.Table.setRowHeight(_row,150)
            self.Table.setColumnWidth(_column,250)
        
    def cellDoubleClicked(self,_row,_column):
        try:
            if _column==8 or _column==9:
                self.showDetails(_row, _column)
            else:
                if self.Table.tbIsRunOnDoubleClick.isChecked()==True:
                    self.showDetails(_row, _column)
        except:
            Dialogs.showError(translate("MusicTable", "Cannot Open Music File"), 
                        str(translate("MusicTable", "\"%s\" : cannot be opened. Please make sure that you selected a music file.")
                        ) % Organizer.getLink(InputOutputs.currentDirectoryPath+"/"+Musics.currentFilesAndFoldersValues[_row][1]))
       
    def refreshColumns(self):
        self.Table.tableColumns = Taggers.getAvailableLabelsForTable()
        self.Table.tableColumnsKey = Taggers.getAvailableKeysForTable()
        
    def save(self):
        MusicDetails.closeAllMusicDialogs()
        returnValue = Musics.writeMusics(self.Table)
        self.Table.changedValueNumber = Musics.changedValueNumber
        return returnValue
        
    def refresh(self, _path):
        self.Table.setColumnWidth(5,70)
        self.Table.setColumnWidth(6,40)
        Musics.readMusics(_path)
        self.fileDetails = Musics.currentFilesAndFoldersValues
        if Universals.isShowOldValues==True:
            n=2
            tableRows=[]
            for row in range(0,len(Musics.currentFilesAndFoldersValues)*2):
                tableRows.append(str(int(n/2)))
                n+=1
            self.Table.setRowCount(len(Musics.currentFilesAndFoldersValues)*2)
            self.Table.setVerticalHeaderLabels(tableRows)
            startRowNo, rowStep = 1, 2
            for fileNo in range(0,len(Musics.currentFilesAndFoldersValues)*2,2):
                for itemNo in range(0,len(self.Table.tableColumns)):
                    item = MTableWidgetItem(Organizer.showWithIncorrectChars(Musics.currentFilesAndFoldersValues[fileNo/2][itemNo]).decode("utf-8"))
                    item.setStatusTip(item.text())
                    self.Table.setItem(fileNo,itemNo,item)      
        else:
            self.Table.setRowCount(len(Musics.currentFilesAndFoldersValues))
            startRowNo, rowStep = 0, 1
        for fileNo in range(startRowNo,self.Table.rowCount(),rowStep):
            if Universals.isShowOldValues==True:
                realFileNo=fileNo/2
            else:
                realFileNo=fileNo
            for itemNo in range(0,len(self.Table.tableColumns)):
                if itemNo==0:
                    newString = Organizer.emend(Musics.currentFilesAndFoldersValues[realFileNo][itemNo], "directory")
                elif itemNo==1:
                    newString = Organizer.emend(Musics.currentFilesAndFoldersValues[realFileNo][itemNo], "file")
                elif itemNo==5:
                    newString_temp = str(Musics.currentFilesAndFoldersValues[realFileNo][itemNo]).split("/")
                    if newString_temp[0]=="None":
                        newString_temp[0]=str(realFileNo+1)
                    newString = newString_temp[0]
                    newString += "/"+str(len(Musics.currentFilesAndFoldersValues))
                else:
                    newString = Organizer.emend(Musics.currentFilesAndFoldersValues[realFileNo][itemNo])
                if newString=="None":
                    newString = ""
                item = MTableWidgetItem(newString.decode("utf-8"))
                item.setStatusTip(item.text())
                self.Table.setItem(fileNo,itemNo,item)
                if str(Musics.currentFilesAndFoldersValues[realFileNo][itemNo])!=str(newString) and str(Musics.currentFilesAndFoldersValues[realFileNo][itemNo])!="None":
                    self.Table.item(fileNo,itemNo).setBackground(MBrush(MColor(142,199,255)))
                    try:self.Table.item(fileNo,itemNo).setToolTip(Organizer.showWithIncorrectChars(Musics.currentFilesAndFoldersValues[realFileNo][itemNo]).decode("utf-8"))
                    except:self.Table.item(fileNo,itemNo).setToolTip(translate("MusicTable", "Cannot Show Erroneous Information."))
                        
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
                elif itemNo==1:
                    newString = Organizer.emend(unicode(self.Table.item(rowNo,itemNo).text(),"utf-8"), "file")
                else:
                    newString = Organizer.emend(unicode(self.Table.item(rowNo,itemNo).text(),"utf-8"))
                self.Table.item(rowNo,itemNo).setText(str(newString).decode("utf-8"))
                
