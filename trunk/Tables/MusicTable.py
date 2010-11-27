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
        for musicNo,musicName in enumerate(musicFileNames):
            isContinueThreadAction = Universals.isContinueThreadAction()
            if isContinueThreadAction:
                if InputOutputs.IA.isReadableFileOrDir(_directoryPath+"/"+musicName):
                    tagger = Taggers.getTagger()
                    tagger.loadFile(_directoryPath+"/"+musicName)
                    if tagger.isAvailableFile() == False:
                        isCanNoncompatible=True
                    musicTagsValues=[]
                    musicTagsValues.append(InputOutputs.getBaseName(_directoryPath))
                    musicTagsValues.append(musicName)
                    musicTagsValues.append(tagger.getArtist())
                    musicTagsValues.append(tagger.getTitle())
                    musicTagsValues.append(tagger.getAlbum())
                    musicTagsValues.append(tagger.getTrackNum())
                    musicTagsValues.append(tagger.getYear())
                    musicTagsValues.append(tagger.getGenre())
                    musicTagsValues.append(tagger.getFirstComment())
                    musicTagsValues.append(tagger.getFirstLyrics())
                    currentTableContentValues.append(musicTagsValues)
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
        if Universals.isShowOldValues==True:
            startRowNo,rowStep=1,2
        else:
            startRowNo,rowStep=0,1
        Universals.startThreadAction()
        allItemNumber = len(_table.currentTableContentValues)
        Dialogs.showState(translate("InputOutputs/Musics", "Writing Music Tags"),0,allItemNumber, True)
        for rowNo in range(startRowNo,_table.rowCount(),rowStep):
            if Universals.isShowOldValues==True:
                realRowNo=rowNo/2
            else:
                realRowNo=rowNo
            isContinueThreadAction = Universals.isContinueThreadAction()
            if isContinueThreadAction:
                if InputOutputs.IA.isWritableFileOrDir(InputOutputs.currentDirectoryPath+"/"+str(_table.currentTableContentValues[realRowNo][1])):
                    if _table.isRowHidden(rowNo):
                        InputOutputs.IA.removeFileOrDir(InputOutputs.currentDirectoryPath+"/"+str(_table.currentTableContentValues[realRowNo][1]))
                        continue
                    tagger = Taggers.getTagger()
                    tagger.loadFileForWrite(InputOutputs.currentDirectoryPath+"/"+_table.currentTableContentValues[realRowNo][1])
                    if _table.isColumnHidden(2)!=True and (_table.item(rowNo,2).isSelected()==Universals.isChangeSelected or Universals.isChangeAll)==True:
                        value = unicode(_table.item(rowNo,2).text(), "utf-8")
                        if value!=str(_table.currentTableContentValues[realRowNo][2]) and (str(_table.currentTableContentValues[realRowNo][2])!="None" or value!=""):
                            tagger.setArtist(value)
                            Records.add(str(translate("MusicTable", "Artist")), str(_table.currentTableContentValues[realRowNo][2]), value)
                            _table.changedValueNumber += 1
                    if _table.isColumnHidden(3)!=True and (_table.item(rowNo,3).isSelected()==Universals.isChangeSelected or Universals.isChangeAll)==True:
                        value = unicode(_table.item(rowNo,3).text(), "utf-8")
                        if value!=str(_table.currentTableContentValues[realRowNo][3]) and (str(_table.currentTableContentValues[realRowNo][3])!="None" or value!=""):
                            tagger.setTitle(value)
                            Records.add(str(translate("MusicTable", "Title")), str(_table.currentTableContentValues[realRowNo][3]), value)
                            _table.changedValueNumber += 1
                    if _table.isColumnHidden(4)!=True and (_table.item(rowNo,4).isSelected()==Universals.isChangeSelected or Universals.isChangeAll)==True:
                        value = unicode(_table.item(rowNo,4).text(), "utf-8")
                        if value!=str(_table.currentTableContentValues[realRowNo][4]) and (str(_table.currentTableContentValues[realRowNo][4])!="None" or value!=""):
                            tagger.setAlbum(value)
                            Records.add(str(translate("MusicTable", "Album")), str(_table.currentTableContentValues[realRowNo][4]), value)
                            _table.changedValueNumber += 1
                    if _table.isColumnHidden(5)!=True and (_table.item(rowNo,5).isSelected()==Universals.isChangeSelected or Universals.isChangeAll)==True:
                        value = unicode(_table.item(rowNo,5).text(), "utf-8")
                        if value!=str(_table.currentTableContentValues[realRowNo][5]) and (str(_table.currentTableContentValues[realRowNo][5])!="None" or value!=""):
                            tagger.setTrackNum(value, len(_table.currentTableContentValues))
                            Records.add(str(translate("MusicTable", "Track No")), str(_table.currentTableContentValues[realRowNo][5]), value)
                            _table.changedValueNumber += 1
                    if _table.isColumnHidden(6)!=True and (_table.item(rowNo,6).isSelected()==Universals.isChangeSelected or Universals.isChangeAll)==True:
                        value = unicode(_table.item(rowNo,6).text(), "utf-8")
                        if value!=str(_table.currentTableContentValues[realRowNo][6]) and (str(_table.currentTableContentValues[realRowNo][6])!="None" or value!=""):
                            tagger.setDate(value)
                            Records.add(str(translate("MusicTable", "Year")), str(_table.currentTableContentValues[realRowNo][6]), value)
                            _table.changedValueNumber += 1
                    if _table.isColumnHidden(7)!=True and (_table.item(rowNo,7).isSelected()==Universals.isChangeSelected or Universals.isChangeAll)==True:
                        value = unicode(_table.item(rowNo,7).text(), "utf-8")
                        if value!=str(_table.currentTableContentValues[realRowNo][7]) and (str(_table.currentTableContentValues[realRowNo][7])!="None" or value!=""):
                            tagger.setGenre(value)
                            Records.add(str(translate("MusicTable", "Genre")), str(_table.currentTableContentValues[realRowNo][7]), value)
                            _table.changedValueNumber += 1
                    if _table.isColumnHidden(8)!=True and (_table.item(rowNo,8).isSelected()==Universals.isChangeSelected or Universals.isChangeAll)==True:
                        value = unicode(_table.item(rowNo,8).text(), "utf-8")
                        if value!=str(_table.currentTableContentValues[realRowNo][8]) and (str(_table.currentTableContentValues[realRowNo][8])!="None" or value!=""):
                            tagger.setFirstComment(value)
                            Records.add(str(translate("MusicTable", "Comment")), str(_table.currentTableContentValues[realRowNo][8]), value)
                            _table.changedValueNumber += 1
                    if len(_table.tableColumns)>9 and _table.isColumnHidden(9)!=True and (_table.item(rowNo,9).isSelected()==Universals.isChangeSelected or Universals.isChangeAll)==True:
                        value = unicode(_table.item(rowNo,9).text(), "utf-8")
                        if value!=str(_table.currentTableContentValues[realRowNo][9]) and (str(_table.currentTableContentValues[realRowNo][9])!="None" or value!=""):
                            tagger.setFirstLyrics(value)
                            Records.add(str(translate("MusicTable", "Lyrics")), str(_table.currentTableContentValues[realRowNo][9]), value)
                            _table.changedValueNumber += 1
                    tagger.update()
                    newFileName=str(_table.currentTableContentValues[realRowNo][1])
                    if _table.isColumnHidden(1)!=True and (_table.item(rowNo,1).isSelected()==Universals.isChangeSelected or Universals.isChangeAll)==True:
                        if str(_table.currentTableContentValues[realRowNo][1])!=unicode(_table.item(rowNo,1).text()).encode("utf-8"):
                            if unicode(_table.item(rowNo,1).text()).encode("utf-8").strip()!="":
                                orgExt = str(_table.currentTableContentValues[realRowNo][1]).split(".")[-1].decode("utf-8").lower()
                                if unicode(_table.item(rowNo,1).text()).encode("utf-8").split(".")[-1].decode("utf-8").lower() != orgExt:
                                    _table.setItem(rowNo,1,MTableWidgetItem(str(unicode(_table.item(rowNo,1).text()).encode("utf-8") + "." + orgExt).decode("utf-8")))
                                if unicode(_table.item(rowNo,1).text()).encode("utf-8").split(".")[-1] != orgExt:
                                    extState = unicode(_table.item(rowNo,1).text()).encode("utf-8").decode("utf-8").lower().find(orgExt)
                                    if extState!=-1:
                                        _table.setItem(rowNo,1,MTableWidgetItem(str(unicode(_table.item(rowNo,1).text()).encode("utf-8")[:extState] + "." + orgExt).decode("utf-8")))
                                newFileName = InputOutputs.IA.moveOrChange(InputOutputs.currentDirectoryPath+"/"+str(_table.currentTableContentValues[realRowNo][1]), InputOutputs.currentDirectoryPath+"/"+unicode(_table.item(rowNo,1).text()).encode("utf-8"))
                                _table.changedValueNumber += 1
                    if newFileName==False:
                        continue
                    if _table.isColumnHidden(0)!=True and (_table.item(rowNo,0).isSelected()==Universals.isChangeSelected or Universals.isChangeAll)==True:
                        newDirectoryName=unicode(_table.item(rowNo,0).text()).encode("utf-8")
                        try:
                            newDirectoryName=int(newDirectoryName)
                            newDirectoryName=str(newDirectoryName)
                        except:
                            if newDirectoryName.decode("utf-8").lower()==newDirectoryName.upper():
                                newDirectoryName=str(_table.currentTableContentValues[realRowNo][0])
                        if str(_table.currentTableContentValues[realRowNo][0])!=newDirectoryName:
                            newPath=InputOutputs.IA.getDirName(InputOutputs.currentDirectoryPath)
                            changingFileDirectories.append([])
                            changingFileDirectories[-1].append(newPath+"/"+str(_table.currentTableContentValues[realRowNo][0])+"/"+newFileName)
                            changingFileDirectories[-1].append(newPath+"/"+newDirectoryName+"/"+newFileName)
                            _table.changedValueNumber += 1
            else:
                allItemNumber = realRowNo+1
            Dialogs.showState(translate("InputOutputs/Musics", "Writing Music Tags"),realRowNo+1,allItemNumber, True)
            if isContinueThreadAction==False:
                break
        Universals.finishThreadAction()
        return InputOutputs.IA.changeDirectories(changingFileDirectories)



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
        MusicDetails.MusicDetails(InputOutputs.currentDirectoryPath+"/"+self.Table.currentTableContentValues[_fileNo][1],
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
                        ) % Organizer.getLink(InputOutputs.currentDirectoryPath+"/"+self.Table.currentTableContentValues[_row][1]))
       
    def refreshColumns(self):
        self.Table.tableColumns = Taggers.getAvailableLabelsForTable()
        self.Table.tableColumnsKey = Taggers.getAvailableKeysForTable()
        
    def save(self):
        MusicDetails.closeAllMusicDialogs()
        returnValue = writeContents(self.Table)
        return returnValue
        
    def refresh(self, _path):
        self.Table.setColumnWidth(5,70)
        self.Table.setColumnWidth(6,40)
        self.Table.currentTableContentValues = readContents(_path)
        if Universals.isShowOldValues==True:
            n=2
            tableRows=[]
            for row in range(0,len(self.Table.currentTableContentValues)*2):
                tableRows.append(str(int(n/2)))
                n+=1
            self.Table.setRowCount(len(self.Table.currentTableContentValues)*2)
            self.Table.setVerticalHeaderLabels(tableRows)
            startRowNo, rowStep = 1, 2
            for fileNo in range(0,len(self.Table.currentTableContentValues)*2,2):
                for itemNo in range(0,len(self.Table.tableColumns)):
                    item = MTableWidgetItem(Organizer.showWithIncorrectChars(self.Table.currentTableContentValues[fileNo/2][itemNo]).decode("utf-8"))
                    item.setStatusTip(item.text())
                    self.Table.setItem(fileNo,itemNo,item)      
        else:
            self.Table.setRowCount(len(self.Table.currentTableContentValues))
            startRowNo, rowStep = 0, 1
        for fileNo in range(startRowNo,self.Table.rowCount(),rowStep):
            if Universals.isShowOldValues==True:
                realFileNo=fileNo/2
            else:
                realFileNo=fileNo
            for itemNo in range(0,len(self.Table.tableColumns)):
                if itemNo==0:
                    newString = Organizer.emend(self.Table.currentTableContentValues[realFileNo][itemNo], "directory")
                elif itemNo==1:
                    newString = Organizer.emend(self.Table.currentTableContentValues[realFileNo][itemNo], "file")
                elif itemNo==5:
                    newString_temp = str(self.Table.currentTableContentValues[realFileNo][itemNo]).split("/")
                    if newString_temp[0]=="None":
                        newString_temp[0]=str(realFileNo+1)
                    newString = newString_temp[0]
                    newString += "/"+str(len(self.Table.currentTableContentValues))
                else:
                    newString = Organizer.emend(self.Table.currentTableContentValues[realFileNo][itemNo])
                if newString=="None":
                    newString = ""
                item = MTableWidgetItem(newString.decode("utf-8"))
                item.setStatusTip(item.text())
                self.Table.setItem(fileNo,itemNo,item)
                if str(self.Table.currentTableContentValues[realFileNo][itemNo])!=str(newString) and str(self.Table.currentTableContentValues[realFileNo][itemNo])!="None":
                    self.Table.item(fileNo,itemNo).setBackground(MBrush(MColor(142,199,255)))
                    try:self.Table.item(fileNo,itemNo).setToolTip(Organizer.showWithIncorrectChars(self.Table.currentTableContentValues[realFileNo][itemNo]).decode("utf-8"))
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
                
