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
import SearchEngines
from MyObjects import *
from Details import MusicDetails
import Universals
import Dialogs
import Taggers
from time import gmtime
import Records

class Content():
    global readContents, writeContents
    
    def readContents(_directoryPath):
        currentTableContentValues = []
        musicFileNames = InputOutputs.readDirectory(_directoryPath, "music")
        isCanNoncompatible = False
        allItemNumber = len(musicFileNames)
        Universals.startThreadAction()
        baseNameOfDirectory = InputOutputs.getBaseName(_directoryPath)
        for musicNo,musicName in enumerate(musicFileNames):
            isContinueThreadAction = Universals.isContinueThreadAction()
            if isContinueThreadAction:
                if InputOutputs.IA.isReadableFileOrDir(_directoryPath+"/"+musicName):
                    tagger = Taggers.getTagger()
                    tagger.loadFile(_directoryPath+"/"+musicName)
                    if tagger.isAvailableFile() == False:
                        isCanNoncompatible=True
                    content = {}
                    content["path"] = _directoryPath + "/" + musicName
                    content["baseNameOfDirectory"] = baseNameOfDirectory
                    content["baseName"] = musicName
                    content["Artist"] = tagger.getArtist()
                    content["Title"] = tagger.getTitle()
                    content["Album"] = tagger.getAlbum()
                    content["TrackNum"] = tagger.getTrackNum()
                    content["Year"] = tagger.getYear()
                    content["Genre"] = tagger.getGenre()
                    content["FirstComment"] = tagger.getFirstComment()
                    content["FirstLyrics"] = tagger.getFirstLyrics()
                    currentTableContentValues.append(content)
            else:
                allItemNumber = musicNo+1
            Dialogs.showState(translate("InputOutputs/Musics", "Reading Music Tags"),musicNo+1,allItemNumber, True)
            if isContinueThreadAction==False:
                break
        Universals.finishThreadAction()
        if isCanNoncompatible == True:
            Dialogs.show(translate("InputOutputs/Musics", "Possible ID3 Mismatch"),
                translate("InputOutputs/Musics", "Some of the files presented in the table may not support ID3 technology.<br>Please check the files and make sure they support ID3 information before proceeding."))
        return currentTableContentValues
    
    def writeContents(_table):
        _table.changedValueNumber = 0
        changingFileDirectories=[]
        Universals.startThreadAction()
        allItemNumber = len(_table.currentTableContentValues)
        Dialogs.showState(translate("InputOutputs/Musics", "Writing Music Tags"),0,allItemNumber, True)
        for rowNo in range(_table.rowCount()):
            isContinueThreadAction = Universals.isContinueThreadAction()
            if isContinueThreadAction:
                if InputOutputs.IA.isWritableFileOrDir(_table.currentTableContentValues[rowNo]["path"]):
                    if _table.isRowHidden(rowNo):
                        InputOutputs.IA.removeFileOrDir(_table.currentTableContentValues[rowNo]["path"])
                        continue
                    baseNameOfDirectory = str(_table.currentTableContentValues[rowNo]["baseNameOfDirectory"])
                    baseName = str(_table.currentTableContentValues[rowNo]["baseName"])
                    tagger = Taggers.getTagger()
                    tagger.loadFileForWrite(_table.currentTableContentValues[rowNo]["path"])
                    if _table.isChangableItem(rowNo, 2, _table.currentTableContentValues[rowNo]["Artist"]):
                        value = str(_table.item(rowNo,2).text())
                        tagger.setArtist(value)
                        Records.add(str(translate("AmarokMusicTable", "Artist")), str(_table.currentTableContentValues[rowNo]["Artist"]), value)
                        _table.changedValueNumber += 1
                    if _table.isChangableItem(rowNo, 3, _table.currentTableContentValues[rowNo]["Title"]):
                        value = str(_table.item(rowNo,3).text())
                        tagger.setTitle(value)
                        Records.add(str(translate("AmarokMusicTable", "Title")), str(_table.currentTableContentValues[rowNo]["Title"]), value)
                        _table.changedValueNumber += 1
                    if _table.isChangableItem(rowNo, 4, _table.currentTableContentValues[rowNo]["Album"]):
                        value = str(_table.item(rowNo,4).text())
                        tagger.setAlbum(value)
                        Records.add(str(translate("AmarokMusicTable", "Album")), str(_table.currentTableContentValues[rowNo]["Album"]), value)
                        _table.changedValueNumber += 1
                    if _table.isChangableItem(rowNo, 5, _table.currentTableContentValues[rowNo]["TrackNum"]):
                        value = str(_table.item(rowNo,5).text())
                        tagger.setTrackNum(value, len(_table.currentTableContentValues))
                        Records.add(str(translate("AmarokMusicTable", "Track No")), str(_table.currentTableContentValues[rowNo]["TrackNum"]), value)
                        _table.changedValueNumber += 1
                    if _table.isChangableItem(rowNo, 6, _table.currentTableContentValues[rowNo]["Year"]):
                        value = str(_table.item(rowNo,6).text())
                        tagger.setDate(value)
                        Records.add(str(translate("AmarokMusicTable", "Year")), str(_table.currentTableContentValues[rowNo]["Year"]), value)
                        _table.changedValueNumber += 1
                    if _table.isChangableItem(rowNo, 7, _table.currentTableContentValues[rowNo]["Genre"]):
                        value = str(_table.item(rowNo,7).text())
                        tagger.setGenre(value)
                        Records.add(str(translate("AmarokMusicTable", "Genre")), str(_table.currentTableContentValues[rowNo]["Genre"]), value)
                        _table.changedValueNumber += 1
                    if _table.isChangableItem(rowNo, 8, _table.currentTableContentValues[rowNo]["FirstComment"]):
                        value = str(_table.item(rowNo,8).text())
                        tagger.setFirstComment(value)
                        Records.add(str(translate("AmarokMusicTable", "Comment")), str(_table.currentTableContentValues[rowNo]["FirstComment"]), value)
                        _table.changedValueNumber += 1
                    if len(_table.tableColumns)>9 and _table.isChangableItem(rowNo, 9, _table.currentTableContentValues[rowNo]["FirstLyrics"]):
                        value = str(_table.item(rowNo,9).text())
                        tagger.setFirstLyrics(value)
                        Records.add(str(translate("AmarokMusicTable", "Lyrics")), str(_table.currentTableContentValues[rowNo]["FirstLyrics"]), value)
                        _table.changedValueNumber += 1
                    tagger.update()
                    if _table.isChangableItem(rowNo, 0, baseNameOfDirectory):
                        baseNameOfDirectory = str(_table.item(rowNo,0).text())
                        _table.changedValueNumber += 1
                    if _table.isChangableItem(rowNo, 1, baseName, False):
                        baseName = str(_table.item(rowNo,1).text())
                        _table.changedValueNumber += 1
                    newFilePath = InputOutputs.getDirName(InputOutputs.getDirName(_table.currentTableContentValues[rowNo]["path"])) + "/" + baseNameOfDirectory + "/" + baseName
                    newFilePath = newFilePath.replace("//", "/")
                    if _table.currentTableContentValues[rowNo]["path"] != newFilePath:
                        changingFileDirectories.append([_table.currentTableContentValues[rowNo]["path"], 
                                                        newFilePath])
            else:
                allItemNumber = rowNo+1
            Dialogs.showState(translate("InputOutputs/Musics", "Writing Music Tags"),rowNo+1,allItemNumber, True)
            if isContinueThreadAction==False:
                break
        Universals.finishThreadAction()
        InputOutputs.IA.changeDirectories(changingFileDirectories)
        return True



class AmarokMusicTable():
    def __init__(self, _table):
        self.Table = _table
        self.specialTollsBookmarkPointer = "music"
        self.hiddenTableColumnsSettingKey = "hiddenAmarokMusicTableColumns"
        self.refreshColumns()
        pbtnVerifyTableValues = MPushButton(translate("AmarokMusicTable", "Verify Table"))
        pbtnVerifyTableValues.setMenu(SearchEngines.SearchEngines(self.Table))
        self.Table.mContextMenu.addMenu(SearchEngines.SearchEngines(self.Table, True))
        self.isPlayNow = MToolButton()
        self.isPlayNow.setToolTip(translate("AmarokMusicTable", "Play Now"))
        self.isPlayNow.setIcon(MIcon("Images:playNow.png"))
        self.isPlayNow.setCheckable(True)
        self.isPlayNow.setAutoRaise(True)
        self.isPlayNow.setChecked(Universals.getBoolValue("isPlayNow"))
        self.Table.hblBox.insertWidget(self.Table.hblBox.count()-3, self.isPlayNow)
        self.Table.hblBox.insertWidget(self.Table.hblBox.count()-1, pbtnVerifyTableValues)
        
    def showDetails(self, _fileNo, _infoNo):
        MusicDetails.MusicDetails(self.Table.currentTableContentValues[_fileNo]["path"],
                                      self.Table.isOpenDetailsOnNewWindow.isChecked(), self.isPlayNow.isChecked())
    
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
            Dialogs.showError(translate("AmarokMusicTable", "Cannot Open Music File"), 
                        str(translate("AmarokMusicTable", "\"%s\" : cannot be opened. Please make sure that you selected a music file.")
                        ) % Organizer.getLink(self.Table.currentTableContentValues[_row]["path"]))
       
    def refreshColumns(self):
        self.Table.tableColumns = Taggers.getAvailableLabelsForTable()
        self.Table.tableColumnsKey = Taggers.getAvailableKeysForTable()
        
    def save(self):
        MusicDetails.closeAllMusicDialogs()
        return writeContents(self.Table)
        
    def refresh(self, _path):
        self.Table.setColumnWidth(5,70)
        self.Table.setColumnWidth(6,40)
        self.Table.currentTableContentValues = readContents(_path)
        self.Table.setRowCount(len(self.Table.currentTableContentValues))
        for rowNo in range(self.Table.rowCount()):
            for itemNo in range(len(self.Table.tableColumns)):
                item = None
                if itemNo==0:
                    newString = Organizer.emend(self.Table.currentTableContentValues[rowNo]["baseNameOfDirectory"], "directory")
                    item = self.Table.createTableWidgetItem(newString, self.Table.currentTableContentValues[rowNo]["baseNameOfDirectory"])
                elif itemNo==1:
                    newString = Organizer.emend(self.Table.currentTableContentValues[rowNo]["baseName"], "file")
                    item = self.Table.createTableWidgetItem(newString, self.Table.currentTableContentValues[rowNo]["baseName"])
                elif itemNo==2:
                    newString = Organizer.emend(self.Table.currentTableContentValues[rowNo]["Artist"])
                    item = self.Table.createTableWidgetItem(newString, self.Table.currentTableContentValues[rowNo]["Artist"])
                elif itemNo==3:
                    newString = Organizer.emend(self.Table.currentTableContentValues[rowNo]["Title"])
                    item = self.Table.createTableWidgetItem(newString, self.Table.currentTableContentValues[rowNo]["Title"])
                elif itemNo==4:
                    newString = Organizer.emend(self.Table.currentTableContentValues[rowNo]["Album"])
                    item = self.Table.createTableWidgetItem(newString, self.Table.currentTableContentValues[rowNo]["Album"])
                elif itemNo==5:
                    newString_temp = str(self.Table.currentTableContentValues[rowNo]["TrackNum"]).split("/")
                    if newString_temp[0]=="None":
                        newString_temp[0]=str(rowNo+1)
                    newString = newString_temp[0]
                    newString += "/"+str(len(self.Table.currentTableContentValues))
                    item = self.Table.createTableWidgetItem(newString, self.Table.currentTableContentValues[rowNo]["TrackNum"])
                elif itemNo==6:
                    newString = Organizer.emend(self.Table.currentTableContentValues[rowNo]["Year"])
                    item = self.Table.createTableWidgetItem(newString, self.Table.currentTableContentValues[rowNo]["Year"])
                elif itemNo==7:
                    newString = Organizer.emend(self.Table.currentTableContentValues[rowNo]["Genre"])
                    item = self.Table.createTableWidgetItem(newString, self.Table.currentTableContentValues[rowNo]["Genre"])
                elif itemNo==8:
                    newString = Organizer.emend(self.Table.currentTableContentValues[rowNo]["FirstComment"])
                    item = self.Table.createTableWidgetItem(newString, self.Table.currentTableContentValues[rowNo]["FirstComment"])
                elif itemNo==9:
                    newString = Organizer.emend(self.Table.currentTableContentValues[rowNo]["FirstLyrics"])
                    item = self.Table.createTableWidgetItem(newString, self.Table.currentTableContentValues[rowNo]["FirstLyrics"])
                if item!=None:
                    self.Table.setItem(rowNo, itemNo, item)
                        
    def correctTable(self):
        for rowNo in range(self.Table.rowCount()):
            for itemNo in range(self.Table.columnCount()):
                if itemNo==0:
                    newString = Organizer.emend(str(self.Table.item(rowNo,itemNo).text()), "directory")
                elif itemNo==1:
                    newString = Organizer.emend(str(self.Table.item(rowNo,itemNo).text()), "file")
                else:
                    newString = Organizer.emend(str(self.Table.item(rowNo,itemNo).text()))
                self.Table.item(rowNo,itemNo).setText(trForUI(newString))
                
