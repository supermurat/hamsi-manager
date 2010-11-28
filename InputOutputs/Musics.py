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


import InputOutputs
from MyObjects import *
from time import gmtime
import Dialogs
import Organizer
import Records
import Universals
import Taggers

class Musics:
    global readMusicFile, writeMusicFile
    
    def readMusicFile(_filePath):
        _directoryPath = InputOutputs.getDirName(_filePath)
        isCanNoncompatible = False
        if InputOutputs.IA.isReadableFileOrDir(_filePath):
            tagger = Taggers.getTagger()
            tagger.loadFile(_filePath)
            if tagger.isAvailableFile() == False:
                isCanNoncompatible=True
            musicTagsValues=[]
            if _filePath!=None:
                musicTagsValues.append(_directoryPath)
            else:
                musicTagsValues.append(InputOutputs.getBaseName(_directoryPath))
            musicTagsValues.append(InputOutputs.getBaseName(_filePath))
            musicTagsValues.append(tagger.getArtist())
            musicTagsValues.append(tagger.getTitle())
            musicTagsValues.append(tagger.getAlbum())
            musicTagsValues.append(tagger.getTrackNum())
            musicTagsValues.append(tagger.getYear())
            musicTagsValues.append(tagger.getGenre())
            musicTagsValues.append(tagger.getFirstComment())
            musicTagsValues.append(tagger.getFirstLyrics())
            musicTagsValues.append(tagger.getSize())
            musicTagsValues.append(tagger.getPlayTimeString())
            musicTagsValues.append(tagger.getSampleFreq())
            musicTagsValues.append(tagger.getBitRateString())
            musicTagsValues.append(tagger.getImages())
            if isCanNoncompatible == True:
                Dialogs.show(translate("InputOutputs/Musics", "Possible ID3 Mismatch"),
                    translate("InputOutputs/Musics", "Some of the files presented in the table may not support ID3 technology.<br>Please check the files and make sure they support ID3 information before proceeding."))
            return musicTagsValues
    
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
                    tagger.setTrackNum(int(_newMusicTagsValues[5]))
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

    
        
