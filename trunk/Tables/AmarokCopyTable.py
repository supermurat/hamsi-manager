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
import FileUtils as fu
import SearchEngines
from Core.MyObjects import *
from Details import MusicDetails
from Core import Universals as uni
from Core import Dialogs
import Taggers
from time import gmtime
from Core import Records
from Core import Variables as var
from Core import ReportBug

class AmarokCopyTable():
    def __init__(self, _table):
        from Amarok import Filter
        self.Table = _table
        self.keyName = "amarokCopy"
        self.amarokFilterKeyName = "AmarokFilterAmarokCopyTable"
        self.hiddenTableColumnsSettingKey = "hiddenAmarokCopyTableColumns"
        self.refreshColumns()
        lblDestinationDir = MLabel(translate("AmarokCopyTable", "Destination Path : "))
        self.leDestinationDirPath = MLineEdit(fu.userDirectoryPath)
        self.pbtnSelectDestinationDir = MPushButton(translate("AmarokCopyTable", "Browse"))
        self.Table.connect(self.pbtnSelectDestinationDir,SIGNAL("clicked()"),self.selectDestinationDir)
        self.wFilter = Filter.FilterWidget(self.Table, self.amarokFilterKeyName)
        self.hblBox = MHBoxLayout()
        self.hblBox.addWidget(self.wFilter, 5)
        self.hblBox.addWidget(lblDestinationDir)
        self.hblBox.addWidget(self.leDestinationDirPath, 1)
        self.hblBox.addWidget(self.pbtnSelectDestinationDir)
        uni.MainWindow.MainLayout.addLayout(self.hblBox)
        pbtnVerifyTableValues = MPushButton(translate("AmarokCopyTable", "Verify Table"))
        pbtnVerifyTableValues.setMenu(SearchEngines.SearchEngines(self.Table))
        self.Table.mContextMenu.addMenu(SearchEngines.SearchEngines(self.Table, True))
        self.isPlayNow = MToolButton()
        self.isPlayNow.setToolTip(translate("AmarokCopyTable", "Play Now"))
        self.isPlayNow.setIcon(MIcon("Images:playNow.png"))
        self.isPlayNow.setCheckable(True)
        self.isPlayNow.setAutoRaise(True)
        self.isPlayNow.setChecked(uni.getBoolValue("isPlayNow"))
        self.Table.hblBox.insertWidget(self.Table.hblBox.count()-3, self.isPlayNow)
        self.Table.hblBox.insertWidget(self.Table.hblBox.count()-1, pbtnVerifyTableValues)
        
    def readContents(self, _directoryPath):
        currentTableContentValues = []
        uni.startThreadAction()
        import Amarok
        Dialogs.showState(translate("AmarokCoverTable", "Checking For Amarok..."), 0, 2)
        if Amarok.checkAmarok():
            Dialogs.showState(translate("AmarokCoverTable", "Getting Values From Amarok"), 1, 2)
            isContinueThreadAction = uni.isContinueThreadAction()
            if isContinueThreadAction:
                from Amarok import Operations
                musicFileValuesWithNames = Operations.getAllMusicFileValuesWithNames(uni.MySettings[self.amarokFilterKeyName])
                Dialogs.showState(translate("AmarokCoverTable", "Values Are Being Processed"), 2, 2)
                isContinueThreadAction = uni.isContinueThreadAction()
                if isContinueThreadAction:
                    if musicFileValuesWithNames!=None:
                        allItemNumber = len(musicFileValuesWithNames)
                        musicFileNo = 0
                        for musicFileRow in musicFileValuesWithNames:
                            isContinueThreadAction = uni.isContinueThreadAction()
                            if isContinueThreadAction:
                                try:
                                    if Amarok.getSelectedTagSourseType("AmarokCopyTable")=="Amarok":
                                        content = {}
                                        content["path"] = musicFileRow["filePath"]
                                        content["baseNameOfDirectory"] = ""
                                        content["baseName"] = fu.getBaseName(musicFileRow["filePath"])
                                        content["artist"] = musicFileRow["artist"]
                                        content["title"] = musicFileRow["title"]
                                        content["album"] = musicFileRow["album"]
                                        content["trackNum"] = musicFileRow["tracknumber"]
                                        content["year"] = musicFileRow["year"]
                                        content["genre"] = musicFileRow["genre"]
                                        content["firstComment"] = musicFileRow["comment"]
                                        content["firstLyrics"] = musicFileRow["lyrics"]
                                        currentTableContentValues.append(content)
                                    else:
                                        if fu.isFile(musicFileRow["filePath"]) and fu.isReadableFileOrDir(musicFileRow["filePath"], False, True):
                                            tagger = Taggers.getTagger()
                                            try:
                                                tagger.loadFile(musicFileRow["filePath"])
                                            except:
                                                Dialogs.showError(translate("FileUtils/Musics", "Incorrect Tag"),
                                                    str(translate("FileUtils/Musics", "\"%s\" : this file has the incorrect tag so can't read tags.")
                                                    ) % Organizer.getLink(musicFileRow["filePath"]))
                                            content = {}
                                            content["path"] = musicFileRow["filePath"]
                                            content["baseNameOfDirectory"] = ""
                                            content["baseName"] = fu.getBaseName(musicFileRow["filePath"])
                                            content["artist"] = tagger.getArtist()
                                            content["title"] = tagger.getTitle()
                                            content["album"] = tagger.getAlbum()
                                            content["trackNum"] = tagger.getTrackNum()
                                            content["year"] = tagger.getYear()
                                            content["genre"] = tagger.getGenre()
                                            content["firstComment"] = tagger.getFirstComment()
                                            content["firstLyrics"] = tagger.getFirstLyrics()
                                            currentTableContentValues.append(content)
                                except:
                                    ReportBug.ReportBug()
                            else:
                                allItemNumber = musicFileNo+1
                            Dialogs.showState(translate("FileUtils/Covers", "Reading Music File Informations"),
                                              musicFileNo+1,allItemNumber, True) 
                            musicFileNo += 1
                            if isContinueThreadAction==False:
                                break
        uni.finishThreadAction()
        return currentTableContentValues
    
    def writeContents(self):
        self.Table.changedValueNumber = 0
        uni.startThreadAction()
        import Amarok
        allItemNumber = len(self.Table.currentTableContentValues)
        Dialogs.showState(translate("FileUtils/Musics", "Writing Music Tags"),0,allItemNumber, True)
        for rowNo in range(self.Table.rowCount()):
            isContinueThreadAction = uni.isContinueThreadAction()
            if isContinueThreadAction:
                try:
                    if self.Table.isRowHidden(rowNo)==False:
                        baseNameOfDirectory = str(self.Table.currentTableContentValues[rowNo]["baseNameOfDirectory"])
                        baseName = str(self.Table.currentTableContentValues[rowNo]["baseName"])
                        if self.Table.isChangeableItem(rowNo, 0, baseNameOfDirectory):
                            baseNameOfDirectory = str(self.Table.item(rowNo,0).text())
                            self.Table.changedValueNumber += 1
                        if self.Table.isChangeableItem(rowNo, 1, baseName, False):
                            baseName = str(self.Table.item(rowNo,1).text())
                            self.Table.changedValueNumber += 1
                        newFilePath = fu.getRealPath(fu.joinPath(str(self.Table.SubTable.leDestinationDirPath.text()), baseNameOfDirectory, baseName))
                        if fu.isFile(self.Table.currentTableContentValues[rowNo]["path"]) and fu.isReadableFileOrDir(self.Table.currentTableContentValues[rowNo]["path"], False, True):
                            if fu.isWritableFileOrDir(newFilePath, False, True):
                                newFilePathCopied = fu.copyOrChange(self.Table.currentTableContentValues[rowNo]["path"], newFilePath)
                                if self.Table.currentTableContentValues[rowNo]["path"] != newFilePathCopied:
                                    newFilePath = newFilePathCopied
                                    try:
                                        if Amarok.getSelectedTagTargetType("AmarokCopyTable").find("ID3")>-1:
                                            typeTemp = Amarok.getSelectedTagTargetType("AmarokCopyTable").split(" + ")
                                            if len(typeTemp)>1:
                                                taggerType = typeTemp[1]
                                            else:
                                                taggerType = typeTemp[0]
                                            Taggers.setSelectedTaggerTypeForWriteName(taggerType)
                                        tagger = Taggers.getTagger()
                                        tagger.loadFileForWrite(newFilePath)
                                        if self.Table.isChangeableItem(rowNo, 2):
                                            value = str(self.Table.item(rowNo,2).text())
                                            tagger.setArtist(value)
                                            Records.add(str(translate("AmarokCopyTable", "Artist")), str(self.Table.currentTableContentValues[rowNo]["artist"]), value)
                                            self.Table.changedValueNumber += 1
                                        if self.Table.isChangeableItem(rowNo, 3):
                                            value = str(self.Table.item(rowNo,3).text())
                                            tagger.setTitle(value)
                                            Records.add(str(translate("AmarokCopyTable", "Title")), str(self.Table.currentTableContentValues[rowNo]["title"]), value)
                                            self.Table.changedValueNumber += 1
                                        if self.Table.isChangeableItem(rowNo, 4):
                                            value = str(self.Table.item(rowNo,4).text())
                                            tagger.setAlbum(value)
                                            Records.add(str(translate("AmarokCopyTable", "Album")), str(self.Table.currentTableContentValues[rowNo]["album"]), value)
                                            self.Table.changedValueNumber += 1
                                        if self.Table.isChangeableItem(rowNo, 5):
                                            value = str(self.Table.item(rowNo,5).text())
                                            tagger.setTrackNum(value)
                                            Records.add(str(translate("AmarokCopyTable", "Track No")), str(self.Table.currentTableContentValues[rowNo]["trackNum"]), value)
                                            self.Table.changedValueNumber += 1
                                        if self.Table.isChangeableItem(rowNo, 6):
                                            value = str(self.Table.item(rowNo,6).text())
                                            tagger.setDate(value)
                                            Records.add(str(translate("AmarokCopyTable", "Year")), str(self.Table.currentTableContentValues[rowNo]["year"]), value)
                                            self.Table.changedValueNumber += 1
                                        if self.Table.isChangeableItem(rowNo, 7):
                                            value = str(self.Table.item(rowNo,7).text())
                                            tagger.setGenre(value)
                                            Records.add(str(translate("AmarokCopyTable", "Genre")), str(self.Table.currentTableContentValues[rowNo]["genre"]), value)
                                            self.Table.changedValueNumber += 1
                                        if self.Table.isChangeableItem(rowNo, 8):
                                            value = str(self.Table.item(rowNo,8).text())
                                            tagger.setFirstComment(value)
                                            Records.add(str(translate("AmarokCopyTable", "Comment")), str(self.Table.currentTableContentValues[rowNo]["firstComment"]), value)
                                            self.Table.changedValueNumber += 1
                                        if len(self.Table.tableColumns)>9 and self.Table.isChangeableItem(rowNo, 9):
                                            value = str(self.Table.item(rowNo,9).text())
                                            tagger.setFirstLyrics(value)
                                            Records.add(str(translate("AmarokCopyTable", "Lyrics")), str(self.Table.currentTableContentValues[rowNo]["firstLyrics"]), value)
                                            self.Table.changedValueNumber += 1
                                        tagger.update()
                                    except:
                                        Dialogs.showError(translate("AmarokCopyTable", "Tags Cannot Changed"), 
                                            str(translate("AmarokCopyTable", "\"%s\" : cannot be changed tags. ")
                                            ) % Organizer.getLink(newFilePath))
                except:
                    ReportBug.ReportBug()
            else:
                allItemNumber = rowNo+1
            Dialogs.showState(translate("FileUtils/Musics", "Writing Music Tags"),rowNo+1,allItemNumber, True)
            if isContinueThreadAction==False:
                break
        uni.finishThreadAction()
        return True
        
    def showDetails(self, _fileNo, _infoNo):
        MusicDetails.MusicDetails(self.Table.currentTableContentValues[_fileNo]["path"], uni.getBoolValue("isOpenDetailsInNewWindow"), self.isPlayNow.isChecked())
    
    def cellClicked(self,_row,_column):
        currentItem = self.Table.currentItem()
        if currentItem is not None:
            cellLenght = len(currentItem.text())*8
            if cellLenght>self.Table.columnWidth(_column):
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
                if uni.getBoolValue("isRunOnDoubleClick"):
                    self.showDetails(_row, _column)
        except:
            Dialogs.showError(translate("AmarokCopyTable", "Cannot Open Music File"), 
                        str(translate("AmarokCopyTable", "\"%s\" : cannot be opened. Please make sure that you selected a music file.")
                        ) % Organizer.getLink(self.Table.currentTableContentValues[_row]["path"]))
       
    def refreshColumns(self):
        self.Table.tableColumns = Taggers.getAvailableLabelsForTable()
        self.Table.tableColumnsKey = Taggers.getAvailableKeysForTable()
        
    def save(self):
	    MusicDetails.MusicDetails.closeAllMusicDialogs()
	    self.Table.checkFileExtensions(1, "baseName")
	    return self.writeContents()
        
    def refresh(self, _path):
        self.Table.setColumnWidth(5,70)
        self.Table.setColumnWidth(6,40)
        self.Table.currentTableContentValues = self.readContents(_path)
        self.Table.setRowCount(len(self.Table.currentTableContentValues))
        allItemNumber = self.Table.rowCount()
        for rowNo in range(allItemNumber):
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
                    newString = str(self.Table.currentTableContentValues[rowNo]["trackNum"])
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
            Dialogs.showState(translate("FileUtils/Tables", "Generating Table..."), rowNo+1, allItemNumber)
                        
    def correctTable(self):
        for rowNo in range(self.Table.rowCount()):
            for itemNo in range(self.Table.columnCount()):
                if self.Table.isChangeableItem(rowNo, itemNo):
                    if itemNo==0:
                        newString = Organizer.emend(str(self.Table.item(rowNo,itemNo).text()), "directory")
                    elif itemNo==1:
                        newString = Organizer.emend(str(self.Table.item(rowNo,itemNo).text()), "file")
                    else:
                        newString = Organizer.emend(str(self.Table.item(rowNo,itemNo).text()))
                    self.Table.item(rowNo,itemNo).setText(str(newString))
                
    def selectDestinationDir(self):
        try:
            destinationDirPath = Dialogs.getExistingDirectory(translate("AmarokCopyTable", "Please Select Destination Directory"),self.leDestinationDirPath.text(), 0)
            if destinationDirPath is not None:
                self.leDestinationDirPath.setText(str(destinationDirPath))
        except:
            ReportBug.ReportBug()
          
    def getValueByRowAndColumn(self, _rowNo, _columnNo):
        if _columnNo==0:
            return self.Table.currentTableContentValues[_rowNo]["baseNameOfDirectory"]
        elif _columnNo==1:
            return self.Table.currentTableContentValues[_rowNo]["baseName"]
        elif _columnNo==2:
            return self.Table.currentTableContentValues[_rowNo]["artist"]
        elif _columnNo==3:
            return self.Table.currentTableContentValues[_rowNo]["title"]
        elif _columnNo==4:
            return self.Table.currentTableContentValues[_rowNo]["album"]
        elif _columnNo==5:
            return self.Table.currentTableContentValues[_rowNo]["trackNum"]
        elif _columnNo==6:
            return self.Table.currentTableContentValues[_rowNo]["year"]
        elif _columnNo==7:
            return self.Table.currentTableContentValues[_rowNo]["genre"]
        elif _columnNo==8:
            return self.Table.currentTableContentValues[_rowNo]["firstComment"]
        elif _columnNo==9:
            return self.Table.currentTableContentValues[_rowNo]["firstLyrics"]
        return ""        
