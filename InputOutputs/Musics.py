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


isAvailable = False
import InputOutputs
from MyObjects import *
from time import gmtime
from os import *
import Dialogs
import Organizer
import Records
import Universals
import Taggers

class Musics:
    """All information about the music files will be arranged in this class
        currentFilesAndFoldersValues[file no][value no]
    """
    global readMusics, writeMusics, writeMusicFile, currentFilesAndFoldersValues, changedValueNumber, correctValuesForMusicGenre
    currentFilesAndFoldersValues = []
    changedValueNumber = 0
    
    def readMusics(_directoryPath=None,_filePath=None):
        global currentFilesAndFoldersValues, changedValueNumber
        changedValueNumber = 0
        if _filePath!=None:
            _directoryPath = InputOutputs.getDirName(_filePath)
            musicFileNames = [InputOutputs.getBaseName(_filePath)]
        else:
            currentFilesAndFoldersValues = []
            musicFileNames = InputOutputs.readDirectory(_directoryPath, "music")
        isCanNoncompatible = False
        allItemNumber = len(musicFileNames)
        Universals.startThreadAction()
        for musicNo,musicName in enumerate(musicFileNames):
            tagger = Taggers.getTagger()
            tagger.loadFile(_directoryPath+"/"+musicName)
            isContinueThreadAction = Universals.isContinueThreadAction()
            if isContinueThreadAction:
                if tagger.isAvailableFile() == False:
                    isCanNoncompatible=True
                musicTagsValues=[]
                if _filePath!=None:
                    musicTagsValues.append(_directoryPath)
                else:
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
                if _filePath!=None:
                    musicTagsValues.append(tagger.getSize())
                    musicTagsValues.append(tagger.getPlayTimeString())
                    musicTagsValues.append(tagger.getSampleFreq())
                    musicTagsValues.append(tagger.getBitRateString())
                    musicTagsValues.append(tagger.getImages())
                    return musicTagsValues
                currentFilesAndFoldersValues.append(musicTagsValues)
            else:
                allItemNumber = musicNo+1
            Dialogs.showState(translate("InputOutputs/Musics", "Reading Music Tags"),musicNo+1,allItemNumber, True)
            if isContinueThreadAction==False:
                break
        Universals.finishThreadAction()
        if isCanNoncompatible == True:
            Dialogs.show(translate("InputOutputs/Musics", "Possible ID3 Mismatch"),
                translate("InputOutputs/Musics", "Some of the files presented in the table may not support ID3 technology.<br>Please check the files and make sure they support ID3 information before proceeding."))
    
    def writeMusics(_table):
        global changedValueNumber
        changedValueNumber = 0
        changingFileDirectories=[]
        if Universals.isShowOldValues==True:
            startRowNo,rowStep=1,2
        else:
            startRowNo,rowStep=0,1
        Universals.startThreadAction()
        allItemNumber = len(currentFilesAndFoldersValues)
        Dialogs.showState(translate("InputOutputs/Musics", "Writing Music Tags"),0,allItemNumber, True)
        for rowNo in range(startRowNo,_table.rowCount(),rowStep):
            if Universals.isShowOldValues==True:
                realRowNo=rowNo/2
            else:
                realRowNo=rowNo
            isContinueThreadAction = Universals.isContinueThreadAction()
            if isContinueThreadAction:
                if InputOutputs.IA.isWritableFileOrDir(InputOutputs.IA.currentDirectoryPath+"/"+str(currentFilesAndFoldersValues[realRowNo][1])):
                    if _table.isRowHidden(rowNo):
                        InputOutputs.IA.removeFileOrDir(InputOutputs.IA.currentDirectoryPath+"/"+str(currentFilesAndFoldersValues[realRowNo][1]))
                        continue
                    tagger = Taggers.getTagger()
                    tagger.loadFileForWrite(InputOutputs.IA.currentDirectoryPath+"/"+currentFilesAndFoldersValues[realRowNo][1])
                    if _table.isColumnHidden(2)!=True and (_table.item(rowNo,2).isSelected()==Universals.isChangeSelected or Universals.isChangeAll)==True:
                        value = unicode(_table.item(rowNo,2).text(), "utf-8")
                        if value!=str(currentFilesAndFoldersValues[realRowNo][2]) and (str(currentFilesAndFoldersValues[realRowNo][2])!="None" or value!=""):
                            tagger.setArtist(value)
                            Records.add(str(translate("MusicTable", "Artist")), str(currentFilesAndFoldersValues[realRowNo][2]), value)
                            changedValueNumber += 1
                    if _table.isColumnHidden(3)!=True and (_table.item(rowNo,3).isSelected()==Universals.isChangeSelected or Universals.isChangeAll)==True:
                        value = unicode(_table.item(rowNo,3).text(), "utf-8")
                        if value!=str(currentFilesAndFoldersValues[realRowNo][3]) and (str(currentFilesAndFoldersValues[realRowNo][3])!="None" or value!=""):
                            tagger.setTitle(value)
                            Records.add(str(translate("MusicTable", "Title")), str(currentFilesAndFoldersValues[realRowNo][3]), value)
                            changedValueNumber += 1
                    if _table.isColumnHidden(4)!=True and (_table.item(rowNo,4).isSelected()==Universals.isChangeSelected or Universals.isChangeAll)==True:
                        value = unicode(_table.item(rowNo,4).text(), "utf-8")
                        if value!=str(currentFilesAndFoldersValues[realRowNo][4]) and (str(currentFilesAndFoldersValues[realRowNo][4])!="None" or value!=""):
                            tagger.setAlbum(value)
                            Records.add(str(translate("MusicTable", "Album")), str(currentFilesAndFoldersValues[realRowNo][4]), value)
                            changedValueNumber += 1
                    if _table.isColumnHidden(5)!=True and (_table.item(rowNo,5).isSelected()==Universals.isChangeSelected or Universals.isChangeAll)==True:
                        value = unicode(_table.item(rowNo,5).text(), "utf-8")
                        if value!=str(currentFilesAndFoldersValues[realRowNo][5]) and (str(currentFilesAndFoldersValues[realRowNo][5])!="None" or value!=""):
                            tagger.setTrackNum(value, len(currentFilesAndFoldersValues))
                            Records.add(str(translate("MusicTable", "Track No")), str(currentFilesAndFoldersValues[realRowNo][5]), value)
                            changedValueNumber += 1
                    if _table.isColumnHidden(6)!=True and (_table.item(rowNo,6).isSelected()==Universals.isChangeSelected or Universals.isChangeAll)==True:
                        value = unicode(_table.item(rowNo,6).text(), "utf-8")
                        if value!=str(currentFilesAndFoldersValues[realRowNo][6]) and (str(currentFilesAndFoldersValues[realRowNo][6])!="None" or value!=""):
                            tagger.setDate(value)
                            Records.add(str(translate("MusicTable", "Year")), str(currentFilesAndFoldersValues[realRowNo][6]), value)
                            changedValueNumber += 1
                    if _table.isColumnHidden(7)!=True and (_table.item(rowNo,7).isSelected()==Universals.isChangeSelected or Universals.isChangeAll)==True:
                        value = unicode(_table.item(rowNo,7).text(), "utf-8")
                        if value!=str(currentFilesAndFoldersValues[realRowNo][7]) and (str(currentFilesAndFoldersValues[realRowNo][7])!="None" or value!=""):
                            tagger.setGenre(value)
                            Records.add(str(translate("MusicTable", "Genre")), str(currentFilesAndFoldersValues[realRowNo][7]), value)
                            changedValueNumber += 1
                    if _table.isColumnHidden(8)!=True and (_table.item(rowNo,8).isSelected()==Universals.isChangeSelected or Universals.isChangeAll)==True:
                        value = unicode(_table.item(rowNo,8).text(), "utf-8")
                        if value!=str(currentFilesAndFoldersValues[realRowNo][8]) and (str(currentFilesAndFoldersValues[realRowNo][8])!="None" or value!=""):
                            tagger.setFirstComment(value)
                            Records.add(str(translate("MusicTable", "Comment")), str(currentFilesAndFoldersValues[realRowNo][8]), value)
                            changedValueNumber += 1
                    if len(_table.tableColumns)>9 and _table.isColumnHidden(9)!=True and (_table.item(rowNo,9).isSelected()==Universals.isChangeSelected or Universals.isChangeAll)==True:
                        value = unicode(_table.item(rowNo,9).text(), "utf-8")
                        if value!=str(currentFilesAndFoldersValues[realRowNo][9]) and (str(currentFilesAndFoldersValues[realRowNo][9])!="None" or value!=""):
                            tagger.setFirstLyrics(value)
                            Records.add(str(translate("MusicTable", "Lyrics")), str(currentFilesAndFoldersValues[realRowNo][9]), value)
                            changedValueNumber += 1
                    tagger.update()
                    newFileName=str(currentFilesAndFoldersValues[realRowNo][1])
                    if _table.isColumnHidden(1)!=True and (_table.item(rowNo,1).isSelected()==Universals.isChangeSelected or Universals.isChangeAll)==True:
                        if str(currentFilesAndFoldersValues[realRowNo][1])!=unicode(_table.item(rowNo,1).text()).encode("utf-8"):
                            if unicode(_table.item(rowNo,1).text()).encode("utf-8").strip()!="":
                                orgExt = str(currentFilesAndFoldersValues[realRowNo][1]).split(".")[-1].decode("utf-8").lower()
                                if unicode(_table.item(rowNo,1).text()).encode("utf-8").split(".")[-1].decode("utf-8").lower() != orgExt:
                                    _table.setItem(rowNo,1,MTableWidgetItem(str(unicode(_table.item(rowNo,1).text()).encode("utf-8") + "." + orgExt).decode("utf-8")))
                                if unicode(_table.item(rowNo,1).text()).encode("utf-8").split(".")[-1] != orgExt:
                                    extState = unicode(_table.item(rowNo,1).text()).encode("utf-8").decode("utf-8").lower().find(orgExt)
                                    if extState!=-1:
                                        _table.setItem(rowNo,1,MTableWidgetItem(str(unicode(_table.item(rowNo,1).text()).encode("utf-8")[:extState] + "." + orgExt).decode("utf-8")))
                                newFileName = InputOutputs.IA.moveOrChange(InputOutputs.IA.currentDirectoryPath+"/"+str(currentFilesAndFoldersValues[realRowNo][1]), InputOutputs.IA.currentDirectoryPath+"/"+unicode(_table.item(rowNo,1).text()).encode("utf-8"))
                                changedValueNumber += 1
                    if newFileName==False:
                        continue
                    if _table.isColumnHidden(0)!=True and (_table.item(rowNo,0).isSelected()==Universals.isChangeSelected or Universals.isChangeAll)==True:
                        newDirectoryName=unicode(_table.item(rowNo,0).text()).encode("utf-8")
                        try:
                            newDirectoryName=int(newDirectoryName)
                            newDirectoryName=str(newDirectoryName)
                        except:
                            if newDirectoryName.decode("utf-8").lower()==newDirectoryName.upper():
                                newDirectoryName=str(currentFilesAndFoldersValues[realRowNo][0])
                        if str(currentFilesAndFoldersValues[realRowNo][0])!=newDirectoryName:
                            newPath=InputOutputs.IA.getDirName(InputOutputs.IA.currentDirectoryPath)
                            changingFileDirectories.append([])
                            changingFileDirectories[-1].append(newPath+"/"+str(currentFilesAndFoldersValues[realRowNo][0])+"/"+newFileName)
                            changingFileDirectories[-1].append(newPath+"/"+newDirectoryName+"/"+newFileName)
                            changedValueNumber += 1
            else:
                allItemNumber = realRowNo+1
            Dialogs.showState(translate("InputOutputs/Musics", "Writing Music Tags"),realRowNo+1,allItemNumber, True)
            if isContinueThreadAction==False:
                break
        Universals.finishThreadAction()
        return InputOutputs.IA.changeDirectories(changingFileDirectories)
        
    def writeMusicFile(_oldMusicTagsValues,_newMusicTagsValues,_isImageAction=False,_ImageType=False,_ImagePath=False):
        if InputOutputs.IA.isWritableFileOrDir(_oldMusicTagsValues[0]+"/"+_oldMusicTagsValues[1]):
            tagger = Taggers.getTagger()
            tagger.loadFileForWrite(_oldMusicTagsValues[0]+"/"+_oldMusicTagsValues[1])
            if _isImageAction==False:
                if _newMusicTagsValues[2]!=_oldMusicTagsValues[2]:
                    tagger.setArtist(str(_newMusicTagsValues[2]))
                if _newMusicTagsValues[3]!=_oldMusicTagsValues[3]:
                    tagger.setTitle(str(_newMusicTagsValues[3]))
                if _newMusicTagsValues[4]!=_oldMusicTagsValues[4]:
                    tagger.setAlbum(str(_newMusicTagsValues[4]))
                if _newMusicTagsValues[5]!=_oldMusicTagsValues[5]:
                    tagger.setTrackNum(str(_newMusicTagsValues[5]), len(currentFilesAndFoldersValues))
                if _newMusicTagsValues[6]!=_oldMusicTagsValues[6]:
                    tagger.setDate(str(_newMusicTagsValues[6]))
                if _newMusicTagsValues[7]!=_oldMusicTagsValues[7]:
                    tagger.setGenre(str(_newMusicTagsValues[7]))
                if _newMusicTagsValues[8]!=_oldMusicTagsValues[8]:
                    tagger.setFirstComment(str(_newMusicTagsValues[8]))
                if len(_newMusicTagsValues)>9 and _newMusicTagsValues[9]!=_oldMusicTagsValues[9]:
                    tagger.setFirstLyrics(str(_newMusicTagsValues[9]))
                tagger.update()
                newFileName=_oldMusicTagsValues[1]
                if _oldMusicTagsValues[1]!=_newMusicTagsValues[1]:
                    if _newMusicTagsValues[1].strip()!="":
                        orgExt = _oldMusicTagsValues[1].split(".")[-1].decode("utf-8").lower()
                        if _newMusicTagsValues[1].split(".")[-1].decode("utf-8").lower() != orgExt:
                            _newMusicTagsValues[1] = _newMusicTagsValues[1].split(".")[-1] + "." + orgExt
                        if _newMusicTagsValues[1].split(".")[-1] != orgExt:
                            extState = _newMusicTagsValues[1].lower().find(orgExt)
                            if extState!=-1:
                                _newMusicTagsValues[1] = _newMusicTagsValues[1].split(".")[-1][:extState] + "." + orgExt
                        newFileName = InputOutputs.IA.moveOrChange(_oldMusicTagsValues[0]+"/"+_oldMusicTagsValues[1],_oldMusicTagsValues[0]+"/"+_newMusicTagsValues[1])
                        if newFileName==False:
                            newFileName=_oldMusicTagsValues[1]
                newDirectoryName=_newMusicTagsValues[0].replace(InputOutputs.IA.getDirName(_oldMusicTagsValues[0])+"/","")
                try:
                    newDirectoryName=str(newDirectoryName)
                    newDirectoryName=int(newDirectoryName)
                except:
                    if newDirectoryName.decode("utf-8").lower()==newDirectoryName.upper():
                        newDirectoryName=_oldMusicTagsValues[0]
                if InputOutputs.IA.getBaseName(_oldMusicTagsValues[0])!=newDirectoryName:
                    if InputOutputs.IA.moveOrChange(_oldMusicTagsValues[0]+"/"+newFileName,InputOutputs.IA.getDirName(_oldMusicTagsValues[0])+"/"+newDirectoryName+"/"+newFileName)!=False:
                        return InputOutputs.IA.getDirName(_oldMusicTagsValues[0])+"/"+newDirectoryName+"/"+newFileName
            
            #Making changes on image files
            else:
                tagger.addImage(_ImageType,_ImagePath)
                tagger.update()
                return None
        return _oldMusicTagsValues[0]+"/"+_oldMusicTagsValues[1]

    
        
