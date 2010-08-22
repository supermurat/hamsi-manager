# -*- coding: utf-8 -*-

import Organizer
import InputOutputs
from InputOutputs import Musics
import SearchEngines
from MyObjects import *
from Details import MusicDetails
import Universals
import Dialogs
                
class MusicTable():
    global _refreshSubTable, _refreshSubTableColumns, _saveSubTable, _subTableCellClicked, _subTableCellDoubleClicked, _subShowDetails
    def __init__(self,_table):
        _table.specialTollsBookmarkPointer = "music"
        _table.hiddenTableColumnsSettingKey = "hiddenMusicTableColumns"
        _table.refreshSubTable = _refreshSubTable
        _table.refreshSubTableColumns = _refreshSubTableColumns
        _table.saveSubTable = _saveSubTable
        _table.subTableCellClicked = _subTableCellClicked
        _table.subTableCellDoubleClicked = _subTableCellDoubleClicked
        _table.subShowDetails = _subShowDetails
        _table.fileDetails = Musics.currentFilesAndFoldersValues
        self=_table
        _refreshSubTableColumns(self)
        pbtnVerifyTableValues = MPushButton(translate("MusicTable", "Verify Table"))
        pbtnVerifyTableValues.setMenu(SearchEngines.SearchEngines(self))
        self.mContextMenu.addMenu(SearchEngines.SearchEngines(self, True))
        self.isPlayNow = MToolButton()
        self.isPlayNow.setToolTip(translate("MusicTable", "Play Now"))
        self.isPlayNow.setIcon(MIcon("Images:playNow.png"))
        self.isPlayNow.setCheckable(True)
        self.isPlayNow.setAutoRaise(True)
        self.isPlayNow.setChecked(Universals.getBoolValue("isPlayNow"))
        hbox1 = MHBoxLayout()
        hbox1.addWidget(self.actRefresh)
        hbox1.addWidget(self.tbGoBack)
        hbox1.addWidget(self.tbCreateHistoryPoint)
        hbox1.addWidget(self.tbGoForward)
        hbox1.addWidget(self.tbIsRunOnDoubleClick)
        hbox1.addWidget(self.isOpenDetailsOnNewWindow)
        hbox1.addWidget(self.isPlayNow)
        hbox1.addWidget(self.tbCorrect)
        hbox1.addWidget(self.pbtnShowDetails, 1)
        hbox1.addWidget(pbtnVerifyTableValues, 1)
        hbox1.addWidget(self.pbtnSave, 2)
        self.hblBox.addLayout(hbox1)
        
    def _subShowDetails(self, _fileNo, _infoNo):
        MusicDetails.MusicDetails(InputOutputs.currentDirectoryPath+"/"+Musics.currentFilesAndFoldersValues[_fileNo][1],
                                      self.isOpenDetailsOnNewWindow.isChecked(),self.isPlayNow.isChecked(),
                                      _infoNo)
    
    def _subTableCellClicked(self,_row,_column):
        for row_no in range(self.rowCount()):
            self.setRowHeight(row_no,30)
        if len(self.currentItem().text())*8>self.columnWidth(_column):
            self.setColumnWidth(_column,len(self.currentItem().text())*8)
        self.setColumnWidth(8,100)
        self.setColumnWidth(9,100)
        if _column==8 or _column==9:
            self.setRowHeight(_row,150)
            self.setColumnWidth(_column,250)
        
    def _subTableCellDoubleClicked(self,_row,_column):
        try:
            if _column==8 or _column==9:
                _subShowDetails(self, _row, _column)
            else:
                if self.tbIsRunOnDoubleClick.isChecked()==True:
                    _subShowDetails(self, _row, _column)
        except:
            Dialogs.showError(translate("MusicTable", "Cannot Open Music File"), 
                        str(translate("MusicTable", "\"%s\" : cannot be opened. Please make sure that you selected a music file.")
                        ) % Organizer.getLink(InputOutputs.currentDirectoryPath+"/"+Musics.currentFilesAndFoldersValues[_row][1]))
       
    def _refreshSubTableColumns(self):
        self.tableColumns=[translate("MusicTable", "Directory"), 
                            translate("MusicTable", "File Name"), 
                            translate("MusicTable", "Artist"), 
                            translate("MusicTable", "Title"), 
                            translate("MusicTable", "Album"), 
                            translate("MusicTable", "Track No"), 
                            translate("MusicTable", "Year"), 
                            translate("MusicTable", "Genre"), 
                            translate("MusicTable", "Comment"), 
                            translate("MusicTable", "Lyrics")]
        self.tableColumnsKey=["Directory", "File Name", "Artist", "Title", "Album", 
                              "Track No", "Year", "Genre", "Comment", "Lyrics"]
        if Universals.MySettings["musicTagType"]!="ID3 V2":
            t = self.tableColumns.pop()
            t = self.tableColumnsKey.pop()
        
    def _saveSubTable(self):
        MusicDetails.closeAllMusicDialogs()
        returnValue = Musics.writeMusics(self)
        self.changedValueNumber = Musics.changedValueNumber
        return returnValue
        
    def _refreshSubTable(self, _path):
        self.setColumnWidth(5,70)
        self.setColumnWidth(6,40)
        Musics.readMusics(_path)
        self.fileDetails = Musics.currentFilesAndFoldersValues
        if Universals.isShowOldValues==True:
            n=2
            tableRows=[]
            for row in range(0,len(Musics.currentFilesAndFoldersValues)*2):
                tableRows.append(str(int(n/2)))
                n+=1
            self.setRowCount(len(Musics.currentFilesAndFoldersValues)*2)
            self.setVerticalHeaderLabels(tableRows)
            startRowNo, rowStep = 1, 2
            for fileNo in range(0,len(Musics.currentFilesAndFoldersValues)*2,2):
                for itemNo in range(0,len(self.tableColumns)):
                    item = MTableWidgetItem(Organizer.showWithIncorrectChars(Musics.currentFilesAndFoldersValues[fileNo/2][itemNo]).decode("utf-8"))
                    item.setStatusTip(item.text())
                    self.setItem(fileNo,itemNo,item)      
        else:
            self.setRowCount(len(Musics.currentFilesAndFoldersValues))
            startRowNo, rowStep = 0, 1
        for fileNo in range(startRowNo,self.rowCount(),rowStep):
            if Universals.isShowOldValues==True:
                realFileNo=fileNo/2
            else:
                realFileNo=fileNo
            for itemNo in range(0,len(self.tableColumns)):
                if itemNo==1 or itemNo==0:
                    newString = Organizer.emend(Musics.currentFilesAndFoldersValues[realFileNo][itemNo], True)
                elif itemNo==5:
                    newString_temp = str(Musics.currentFilesAndFoldersValues[realFileNo][itemNo]).split("/")
                    if newString_temp[0]=="None":
                        newString_temp[0]=str(realFileNo+1)
                    newString = newString_temp[0]
                    if Universals.MySettings["musicTagType"]=="ID3 V2":
                        newString += "/"+str(len(Musics.currentFilesAndFoldersValues))
                else:
                    newString = Organizer.emend(Musics.currentFilesAndFoldersValues[realFileNo][itemNo])
                if newString=="None":
                    newString = ""
                item = MTableWidgetItem(newString.decode("utf-8"))
                item.setStatusTip(item.text())
                self.setItem(fileNo,itemNo,item)
                if str(Musics.currentFilesAndFoldersValues[realFileNo][itemNo])!=str(newString) and str(Musics.currentFilesAndFoldersValues[realFileNo][itemNo])!="None":
                    self.item(fileNo,itemNo).setBackground(MBrush(MColor(142,199,255)))
                    try:self.item(fileNo,itemNo).setToolTip(Organizer.showWithIncorrectChars(Musics.currentFilesAndFoldersValues[realFileNo][itemNo]).decode("utf-8"))
                    except:self.item(fileNo,itemNo).setToolTip(translate("MusicTable", "Cannot Show Erroneous Information."))
                        