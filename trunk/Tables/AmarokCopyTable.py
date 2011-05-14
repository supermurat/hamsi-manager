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
import Variables

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
                musicFileValuesWithNames = Operations.getAllMusicFileValuesWithNames()
                Dialogs.showState(translate("AmarokCoverTable", "Values Are Being Processed"), 2, 2)
                isContinueThreadAction = Universals.isContinueThreadAction()
                if isContinueThreadAction:
                    if musicFileValuesWithNames!=None:
                        allItemNumber = len(musicFileValuesWithNames)
                        musicFileNo = 0
                        for musicFileRow in musicFileValuesWithNames:
                            isContinueThreadAction = Universals.isContinueThreadAction()
                            if isContinueThreadAction:
                                if Amarok.getSelectedTagSourseType()=="Amarok":
                                    content = {}
                                    content["path"] = musicFileRow["filePath"]
                                    content["baseNameOfDirectory"] = ""
                                    content["baseName"] = InputOutputs.getBaseName(musicFileRow["filePath"])
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
                                    if InputOutputs.IA.isFile(musicFileRow["filePath"]) and InputOutputs.IA.isReadableFileOrDir(musicFileRow["filePath"]):
                                        tagger = Taggers.getTagger()
                                        try:
                                            tagger.loadFile(musicFileRow["filePath"])
                                        except:
                                            Dialogs.showError(translate("InputOutputs/Musics", "Incorrect Tag"), 
                                                str(translate("InputOutputs/Musics", "\"%s\" : this file has the incorrect tag so can't read tags.")
                                                ) % Organizer.getLink(musicFileRow["filePath"]))
                                        content = {}
                                        content["path"] = musicFileRow["filePath"]
                                        content["baseNameOfDirectory"] = ""
                                        content["baseName"] = InputOutputs.getBaseName(musicFileRow["filePath"])
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
        Universals.startThreadAction()
        import Amarok
        allItemNumber = len(_table.currentTableContentValues)
        Dialogs.showState(translate("InputOutputs/Musics", "Writing Music Tags"),0,allItemNumber, True)
        for rowNo in range(_table.rowCount()):
            isContinueThreadAction = Universals.isContinueThreadAction()
            if isContinueThreadAction:
                if _table.isRowHidden(rowNo):
                    continue
                baseNameOfDirectory = str(_table.currentTableContentValues[rowNo]["baseNameOfDirectory"])
                baseName = str(_table.currentTableContentValues[rowNo]["baseName"])
                if _table.isChangableItem(rowNo, 0, baseNameOfDirectory):
                    baseNameOfDirectory = str(_table.item(rowNo,0).text())
                    _table.changedValueNumber += 1
                if _table.isChangableItem(rowNo, 1, baseName, False):
                    baseName = str(_table.item(rowNo,1).text())
                    _table.changedValueNumber += 1
                newFilePath = str(_table.SubTable.leDestinationDirPath.text()) + "/" + baseNameOfDirectory + "/" + baseName
                if InputOutputs.IA.isFile(_table.currentTableContentValues[rowNo]["path"]) and InputOutputs.IA.isReadableFileOrDir(_table.currentTableContentValues[rowNo]["path"]):
                    if InputOutputs.IA.isWritableFileOrDir(newFilePath):
                        newFilePathCopied = InputOutputs.IA.copyOrChange(_table.currentTableContentValues[rowNo]["path"], newFilePath)
                        if _table.currentTableContentValues[rowNo]["path"] != newFilePathCopied:
                            newFilePath = newFilePathCopied
                            if Amarok.getSelectedTagTargetType().find("ID3")>-1:
                                typeTemp = Amarok.getSelectedTagTargetType().split(" + ")
                                if len(typeTemp)>1:
                                    taggerType = typeTemp[1]
                                else:
                                    taggerType = typeTemp[0]
                                Taggers.setSelectedTaggerTypeName(taggerType)
                            tagger = Taggers.getTagger()
                            tagger.loadFileForWrite(newFilePath)
                            if _table.isChangableItem(rowNo, 2):
                                value = str(_table.item(rowNo,2).text())
                                tagger.setArtist(value)
                                Records.add(str(translate("AmarokCopyTable", "Artist")), str(_table.currentTableContentValues[rowNo]["artist"]), value)
                                _table.changedValueNumber += 1
                            if _table.isChangableItem(rowNo, 3):
                                value = str(_table.item(rowNo,3).text())
                                tagger.setTitle(value)
                                Records.add(str(translate("AmarokCopyTable", "Title")), str(_table.currentTableContentValues[rowNo]["title"]), value)
                                _table.changedValueNumber += 1
                            if _table.isChangableItem(rowNo, 4):
                                value = str(_table.item(rowNo,4).text())
                                tagger.setAlbum(value)
                                Records.add(str(translate("AmarokCopyTable", "Album")), str(_table.currentTableContentValues[rowNo]["album"]), value)
                                _table.changedValueNumber += 1
                            if _table.isChangableItem(rowNo, 5):
                                value = str(_table.item(rowNo,5).text())
                                tagger.setTrackNum(value, len(_table.currentTableContentValues))
                                Records.add(str(translate("AmarokCopyTable", "Track No")), str(_table.currentTableContentValues[rowNo]["trackNum"]), value)
                                _table.changedValueNumber += 1
                            if _table.isChangableItem(rowNo, 6):
                                value = str(_table.item(rowNo,6).text())
                                tagger.setDate(value)
                                Records.add(str(translate("AmarokCopyTable", "Year")), str(_table.currentTableContentValues[rowNo]["year"]), value)
                                _table.changedValueNumber += 1
                            if _table.isChangableItem(rowNo, 7):
                                value = str(_table.item(rowNo,7).text())
                                tagger.setGenre(value)
                                Records.add(str(translate("AmarokCopyTable", "Genre")), str(_table.currentTableContentValues[rowNo]["genre"]), value)
                                _table.changedValueNumber += 1
                            if _table.isChangableItem(rowNo, 8):
                                value = str(_table.item(rowNo,8).text())
                                tagger.setFirstComment(value)
                                Records.add(str(translate("AmarokCopyTable", "Comment")), str(_table.currentTableContentValues[rowNo]["firstComment"]), value)
                                _table.changedValueNumber += 1
                            if len(_table.tableColumns)>9 and _table.isChangableItem(rowNo, 9):
                                value = str(_table.item(rowNo,9).text())
                                tagger.setFirstLyrics(value)
                                Records.add(str(translate("AmarokCopyTable", "Lyrics")), str(_table.currentTableContentValues[rowNo]["firstLyrics"]), value)
                                _table.changedValueNumber += 1
                            if Amarok.getSelectedTagTargetType().find("ID3")>-1:
                                tagger.update()
            else:
                allItemNumber = rowNo+1
            Dialogs.showState(translate("InputOutputs/Musics", "Writing Music Tags"),rowNo+1,allItemNumber, True)
            if isContinueThreadAction==False:
                break
        Universals.finishThreadAction()
        return True



class AmarokCopyTable():
    def __init__(self, _table):
        self.Table = _table
        self.specialTollsBookmarkPointer = "AmarokCopy"
        self.hiddenTableColumnsSettingKey = "hiddenAmarokCopyTableColumns"
        self.refreshColumns()
        lblDestinationDir = MLabel(translate("AmarokCopyTable", "Destination Path : "))
        self.leDestinationDirPath = MLineEdit(Variables.userDirectoryPath)
        self.pbtnSelectDestinationDir = MPushButton(translate("Packager", "Browse"))
        self.Table.connect(self.pbtnSelectDestinationDir,SIGNAL("clicked()"),self.selectDestinationDir)

        self.hblBox = MHBoxLayout()
        self.hblBox.addWidget(lblDestinationDir)
        self.hblBox.addWidget(self.leDestinationDirPath)
        self.hblBox.addWidget(self.pbtnSelectDestinationDir)
        Universals.MainWindow.MainLayout.addLayout(self.hblBox)
        pbtnVerifyTableValues = MPushButton(translate("AmarokCopyTable", "Verify Table"))
        pbtnVerifyTableValues.setMenu(SearchEngines.SearchEngines(self.Table))
        self.Table.mContextMenu.addMenu(SearchEngines.SearchEngines(self.Table, True))
        self.isPlayNow = MToolButton()
        self.isPlayNow.setToolTip(translate("AmarokCopyTable", "Play Now"))
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
        cellLenght = len(self.Table.currentItem().text())*8
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
                if self.Table.tbIsRunOnDoubleClick.isChecked()==True:
                    self.showDetails(_row, _column)
        except:
            Dialogs.showError(translate("AmarokCopyTable", "Cannot Open Music File"), 
                        str(translate("AmarokCopyTable", "\"%s\" : cannot be opened. Please make sure that you selected a music file.")
                        ) % Organizer.getLink(self.Table.currentTableContentValues[_row]["path"]))
       
    def refreshColumns(self):
        self.Table.tableColumns = Taggers.getAvailableLabelsForTable()
        self.Table.tableColumnsKey = Taggers.getAvailableKeysForTable()
        
    def save(self):
        MusicDetails.closeAllMusicDialogs()
        self.Table.checkFileExtensions(1, "baseName")
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
                
    def selectDestinationDir(self):
        try:
            destinationDirPath = MFileDialog.getExistingDirectory(self.Table,
                            translate("AmarokCopyTable", "Please Select Destination Directory"),self.leDestinationDirPath.text())
            if destinationDirPath!="":
                self.leDestinationDirPath.setText(destinationDirPath)
        except:
            import ReportBug
            error = ReportBug.ReportBug()
            error.show() 
