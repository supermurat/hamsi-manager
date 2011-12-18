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

from Core import Organizer
import InputOutputs
import SearchEngines
from Core.MyObjects import *
from Details import MusicDetails
from Core import Universals
from Core import Dialogs
import Options
import Taggers
from time import gmtime
from Core import Records

class MusicTable():
    def __init__(self, _table):
        self.Table = _table
        self.keyName = "music"
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
        if Universals.isActiveAmarok:
            self.cckbChangeInAmarokDB = Options.MyCheckBox(_table, translate("MusicTable", "Change In Amarok"), None, "isMusicTableValuesChangeInAmarokDB")
            self.cckbChangeInAmarokDB.setToolTip(translate("MusicTable", "Are you want to change file paths and tags in Amarok database?"))
            self.Table.hblBox.insertWidget(self.Table.hblBox.count()-3, self.cckbChangeInAmarokDB)
        
    def readContents(self, _directoryPath):
        currentTableContentValues = []
        musicFileNames = InputOutputs.readDirectory(_directoryPath, "music", Universals.getBoolValue("isShowHiddensInMusicTable"))
        isCanNoncompatible = False
        allItemNumber = len(musicFileNames)
        Universals.startThreadAction()
        baseNameOfDirectory = InputOutputs.getBaseName(_directoryPath)
        for musicNo,musicName in enumerate(musicFileNames):
            isContinueThreadAction = Universals.isContinueThreadAction()
            if isContinueThreadAction:
                if InputOutputs.isReadableFileOrDir(InputOutputs.joinPath(_directoryPath, musicName), False, True):
                    tagger = Taggers.getTagger()
                    try:
                        tagger.loadFile(InputOutputs.joinPath(_directoryPath, musicName))
                    except:
                        Dialogs.showError(translate("InputOutputs/Musics", "Incorrect Tag"), 
                            str(translate("InputOutputs/Musics", "\"%s\" : this file has the incorrect tag so can't read tags.")
                            ) % Organizer.getLink(InputOutputs.joinPath(_directoryPath, musicName)))
                    if tagger.isAvailableFile() == False:
                        isCanNoncompatible=True
                    content = {}
                    content["path"] = InputOutputs.joinPath(_directoryPath, musicName)
                    content["baseNameOfDirectory"] = baseNameOfDirectory
                    content["baseName"] = musicName
                    content["artist"] = tagger.getArtist()
                    content["title"] = tagger.getTitle()
                    content["album"] = tagger.getAlbum()
                    content["trackNum"] = tagger.getTrackNum()
                    content["year"] = tagger.getYear()
                    content["genre"] = tagger.getGenre()
                    content["firstComment"] = tagger.getFirstComment()
                    content["firstLyrics"] = tagger.getFirstLyrics()
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
    
    def writeContents(self):
        self.Table.changedValueNumber = 0
        changingFileDirectories=[]
        changingTags=[]
        if Universals.isActiveAmarok and Universals.getBoolValue("isMusicTableValuesChangeInAmarokDB"):
            import Amarok
            if Amarok.checkAmarok(True, False) == False:
                return False
        Universals.startThreadAction()
        allItemNumber = len(self.Table.currentTableContentValues)
        Dialogs.showState(translate("InputOutputs/Musics", "Writing Music Tags"),0,allItemNumber, True)
        for rowNo in range(self.Table.rowCount()):
            isContinueThreadAction = Universals.isContinueThreadAction()
            if isContinueThreadAction:
                changingTags.append({"path" : self.Table.currentTableContentValues[rowNo]["path"]})
                changingTags[-1]["artist"] = self.Table.currentTableContentValues[rowNo]["artist"]
                changingTags[-1]["title"] = self.Table.currentTableContentValues[rowNo]["title"]
                changingTags[-1]["album"] = self.Table.currentTableContentValues[rowNo]["album"]
                changingTags[-1]["trackNum"] = self.Table.currentTableContentValues[rowNo]["trackNum"]
                changingTags[-1]["year"] = self.Table.currentTableContentValues[rowNo]["year"]
                changingTags[-1]["genre"] = self.Table.currentTableContentValues[rowNo]["genre"]
                changingTags[-1]["firstComment"] = self.Table.currentTableContentValues[rowNo]["firstComment"]
                changingTags[-1]["firstLyrics"] = self.Table.currentTableContentValues[rowNo]["firstLyrics"]
                if InputOutputs.isWritableFileOrDir(self.Table.currentTableContentValues[rowNo]["path"], False, True):
                    if self.Table.isRowHidden(rowNo):
                        InputOutputs.removeFileOrDir(self.Table.currentTableContentValues[rowNo]["path"])
                        self.Table.changedValueNumber += 1
                        continue
                    baseNameOfDirectory = str(self.Table.currentTableContentValues[rowNo]["baseNameOfDirectory"])
                    baseName = str(self.Table.currentTableContentValues[rowNo]["baseName"])
                    tagger = Taggers.getTagger()
                    tagger.loadFileForWrite(self.Table.currentTableContentValues[rowNo]["path"])
                    isCheckLike = Taggers.getSelectedTaggerTypeForRead()==Taggers.getSelectedTaggerTypeForWrite()
                    if self.Table.isChangableItem(rowNo, 2, self.Table.currentTableContentValues[rowNo]["artist"], True, isCheckLike):
                        value = str(self.Table.item(rowNo,2).text())
                        tagger.setArtist(value)
                        changingTags[-1]["artist"] = value
                        Records.add(str(translate("MusicTable", "Artist")), str(self.Table.currentTableContentValues[rowNo]["artist"]), value)
                        self.Table.changedValueNumber += 1
                    if self.Table.isChangableItem(rowNo, 3, self.Table.currentTableContentValues[rowNo]["title"], True, isCheckLike):
                        value = str(self.Table.item(rowNo,3).text())
                        tagger.setTitle(value)
                        changingTags[-1]["title"] = value
                        Records.add(str(translate("MusicTable", "Title")), str(self.Table.currentTableContentValues[rowNo]["title"]), value)
                        self.Table.changedValueNumber += 1
                    if self.Table.isChangableItem(rowNo, 4, self.Table.currentTableContentValues[rowNo]["album"], True, isCheckLike):
                        value = str(self.Table.item(rowNo,4).text())
                        tagger.setAlbum(value)
                        changingTags[-1]["album"] = value
                        Records.add(str(translate("MusicTable", "Album")), str(self.Table.currentTableContentValues[rowNo]["album"]), value)
                        self.Table.changedValueNumber += 1
                    if self.Table.isChangableItem(rowNo, 5, self.Table.currentTableContentValues[rowNo]["trackNum"], True, isCheckLike):
                        value = str(self.Table.item(rowNo,5).text())
                        tagger.setTrackNum(value, len(self.Table.currentTableContentValues))
                        changingTags[-1]["trackNum"] = value.split("/")[0]
                        Records.add(str(translate("MusicTable", "Track No")), str(self.Table.currentTableContentValues[rowNo]["trackNum"]), value)
                        self.Table.changedValueNumber += 1
                    if self.Table.isChangableItem(rowNo, 6, self.Table.currentTableContentValues[rowNo]["year"], True, isCheckLike):
                        value = str(self.Table.item(rowNo,6).text())
                        tagger.setDate(value)
                        changingTags[-1]["year"] = value
                        Records.add(str(translate("MusicTable", "Year")), str(self.Table.currentTableContentValues[rowNo]["year"]), value)
                        self.Table.changedValueNumber += 1
                    if self.Table.isChangableItem(rowNo, 7, self.Table.currentTableContentValues[rowNo]["genre"], True, isCheckLike):
                        value = str(self.Table.item(rowNo,7).text())
                        tagger.setGenre(value)
                        changingTags[-1]["genre"] = value
                        Records.add(str(translate("MusicTable", "Genre")), str(self.Table.currentTableContentValues[rowNo]["genre"]), value)
                        self.Table.changedValueNumber += 1
                    if self.Table.isChangableItem(rowNo, 8, self.Table.currentTableContentValues[rowNo]["firstComment"], True, isCheckLike):
                        value = str(self.Table.item(rowNo,8).text())
                        tagger.setFirstComment(value)
                        changingTags[-1]["firstComment"] = value
                        Records.add(str(translate("MusicTable", "Comment")), str(self.Table.currentTableContentValues[rowNo]["firstComment"]), value)
                        self.Table.changedValueNumber += 1
                    if len(self.Table.tableColumns)>9 and self.Table.isChangableItem(rowNo, 9, self.Table.currentTableContentValues[rowNo]["firstLyrics"], True, isCheckLike):
                        value = str(self.Table.item(rowNo,9).text())
                        tagger.setFirstLyrics(value)
                        changingTags[-1]["firstLyrics"] = value
                        Records.add(str(translate("MusicTable", "Lyrics")), str(self.Table.currentTableContentValues[rowNo]["firstLyrics"]), value)
                        self.Table.changedValueNumber += 1
                    tagger.update()
                    if self.Table.isChangableItem(rowNo, 0, baseNameOfDirectory):
                        baseNameOfDirectory = str(self.Table.item(rowNo,0).text())
                        self.Table.changedValueNumber += 1
                    if self.Table.isChangableItem(rowNo, 1, baseName, False):
                        baseName = str(self.Table.item(rowNo,1).text())
                        self.Table.changedValueNumber += 1
                    newFilePath = InputOutputs.joinPath(InputOutputs.getDirName(InputOutputs.getDirName(self.Table.currentTableContentValues[rowNo]["path"])), baseNameOfDirectory, baseName)
                    if InputOutputs.getRealPath(self.Table.currentTableContentValues[rowNo]["path"]) != InputOutputs.getRealPath(newFilePath):
                        changingFileDirectories.append([self.Table.currentTableContentValues[rowNo]["path"], 
                                                        newFilePath])
            else:
                allItemNumber = rowNo+1
            Dialogs.showState(translate("InputOutputs/Musics", "Writing Music Tags"),rowNo+1,allItemNumber, True)
            if isContinueThreadAction==False:
                break
        Universals.finishThreadAction()
        pathValues = InputOutputs.changeDirectories(changingFileDirectories)
        if Universals.isActiveAmarok and Universals.getBoolValue("isMusicTableValuesChangeInAmarokDB"):
            import Amarok
            from Amarok import Operations
            Operations.changeTags(changingTags)
            Operations.changePaths(pathValues, "file")
        return True
        
    def showDetails(self, _fileNo, _infoNo):
        MusicDetails.MusicDetails(self.Table.currentTableContentValues[_fileNo]["path"],
                                      self.Table.isOpenDetailsOnNewWindow.isChecked(), self.isPlayNow.isChecked())
    
    def cellClicked(self,_row,_column):
        cellLenght = len(self.Table.currentItem().text())*8
        if cellLenght > self.Table.columnWidth(_column):
            self.Table.setColumnWidth(_column,cellLenght)
        if _column==8 or _column==9:
            if self.Table.rowHeight(_row)<150:
                self.Table.setRowHeight(_row,150)
            if self.Table.columnWidth(_column)<250:
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
                        ) % Organizer.getLink(self.Table.currentTableContentValues[_row]["path"]))
       
    def refreshColumns(self):
        self.Table.tableColumns = Taggers.getAvailableLabelsForTable()
        self.Table.tableColumnsKey = Taggers.getAvailableKeysForTable()
        
    def save(self):
        self.Table.checkFileExtensions(1, "baseName")
        MusicDetails.closeAllMusicDialogs()
        return self.writeContents()
        
    def refresh(self, _path):
        self.Table.setColumnWidth(5,70)
        self.Table.setColumnWidth(6,40)
        self.Table.currentTableContentValues = self.readContents(_path)
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
                    newString = Organizer.emend(self.Table.currentTableContentValues[rowNo]["artist"])
                    item = self.Table.createTableWidgetItem(newString, self.Table.currentTableContentValues[rowNo]["artist"])
                elif itemNo==3:
                    newString = Organizer.emend(self.Table.currentTableContentValues[rowNo]["title"])
                    item = self.Table.createTableWidgetItem(newString, self.Table.currentTableContentValues[rowNo]["title"])
                elif itemNo==4:
                    newString = Organizer.emend(self.Table.currentTableContentValues[rowNo]["album"])
                    item = self.Table.createTableWidgetItem(newString, self.Table.currentTableContentValues[rowNo]["album"])
                elif itemNo==5:
                    newString_temp = str(self.Table.currentTableContentValues[rowNo]["trackNum"]).split("/")
                    if newString_temp[0]=="None":
                        newString_temp[0]=str(rowNo+1)
                    newString = newString_temp[0]
                    newString += "/"+str(len(self.Table.currentTableContentValues))
                    item = self.Table.createTableWidgetItem(newString, self.Table.currentTableContentValues[rowNo]["trackNum"])
                elif itemNo==6:
                    newString = Organizer.emend(self.Table.currentTableContentValues[rowNo]["year"])
                    item = self.Table.createTableWidgetItem(newString, self.Table.currentTableContentValues[rowNo]["year"])
                elif itemNo==7:
                    newString = Organizer.emend(self.Table.currentTableContentValues[rowNo]["genre"])
                    item = self.Table.createTableWidgetItem(newString, self.Table.currentTableContentValues[rowNo]["genre"])
                elif itemNo==8:
                    newString = Organizer.emend(self.Table.currentTableContentValues[rowNo]["firstComment"])
                    item = self.Table.createTableWidgetItem(newString, self.Table.currentTableContentValues[rowNo]["firstComment"])
                elif itemNo==9:
                    newString = Organizer.emend(self.Table.currentTableContentValues[rowNo]["firstLyrics"])
                    item = self.Table.createTableWidgetItem(newString, self.Table.currentTableContentValues[rowNo]["firstLyrics"])
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
                
