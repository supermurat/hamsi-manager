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
            content = {}
            content["path"] = _filePath
            content["baseNameOfDirectory"] = InputOutputs.getBaseName(_directoryPath)
            content["baseName"] = InputOutputs.getBaseName(_filePath)
            content["Artist"] = tagger.getArtist()
            content["Title"] = tagger.getTitle()
            content["Album"] = tagger.getAlbum()
            content["TrackNum"] = tagger.getTrackNum()
            content["Year"] = tagger.getYear()
            content["Genre"] = tagger.getGenre()
            content["FirstComment"] = tagger.getFirstComment()
            content["FirstLyrics"] = tagger.getFirstLyrics()
            content["Size"] = tagger.getSize()
            content["PlayTimeString"] = tagger.getPlayTimeString()
            content["SampleFreq"] = tagger.getSampleFreq()
            content["BitRateString"] = tagger.getBitRateString()
            content["Images"] = tagger.getImages()
            if isCanNoncompatible == True:
                Dialogs.show(translate("InputOutputs/Musics", "Possible ID3 Mismatch"),
                    translate("InputOutputs/Musics", "Some of the files presented in the table may not support ID3 technology.<br>Please check the files and make sure they support ID3 information before proceeding."))
            return content
    
    def writeMusicFile(_oldMusicTagsValues,_newMusicTagsValues,_isImageAction=False,_ImageType=False,_ImagePath=False):
        if InputOutputs.IA.isWritableFileOrDir(_oldMusicTagsValues["path"]):
            baseNameOfDirectory = _oldMusicTagsValues["baseNameOfDirectory"]
            baseName = _oldMusicTagsValues["baseName"]
            tagger = Taggers.getTagger()
            tagger.loadFileForWrite(_oldMusicTagsValues["path"])
            if _isImageAction==False:
                if _newMusicTagsValues["Artist"]!=_oldMusicTagsValues["Artist"]:
                    tagger.setArtist(str(_newMusicTagsValues["Artist"]))
                if _newMusicTagsValues["Title"]!=_oldMusicTagsValues["Title"]:
                    tagger.setTitle(str(_newMusicTagsValues["Title"]))
                if _newMusicTagsValues["Album"]!=_oldMusicTagsValues["Album"]:
                    tagger.setAlbum(str(_newMusicTagsValues["Album"]))
                if _newMusicTagsValues["TrackNum"]!=_oldMusicTagsValues["TrackNum"]:
                    tagger.setTrackNum(int(_newMusicTagsValues["TrackNum"]))
                if _newMusicTagsValues["Year"]!=_oldMusicTagsValues["Year"]:
                    tagger.setDate(str(_newMusicTagsValues["Year"]))
                if _newMusicTagsValues["Genre"]!=_oldMusicTagsValues["Genre"]:
                    tagger.setGenre(str(_newMusicTagsValues["Genre"]))
                if _newMusicTagsValues["FirstComment"]!=_oldMusicTagsValues["FirstComment"]:
                    tagger.setFirstComment(str(_newMusicTagsValues["FirstComment"]))
                if _newMusicTagsValues["FirstLyrics"]!=_oldMusicTagsValues["FirstLyrics"]:
                    tagger.setFirstLyrics(str(_newMusicTagsValues["FirstLyrics"]))
                tagger.update()
                if _newMusicTagsValues["baseNameOfDirectory"]!=_oldMusicTagsValues["baseNameOfDirectory"]:
                    baseNameOfDirectory = str(_newMusicTagsValues["baseNameOfDirectory"])
                if _newMusicTagsValues["baseName"]!=_oldMusicTagsValues["baseName"]:
                    baseName = str(_newMusicTagsValues["baseName"])
                newFilePath = InputOutputs.getDirName(InputOutputs.getDirName(_oldMusicTagsValues["path"])) + "/" + baseNameOfDirectory + "/" + baseName
                newFilePath = newFilePath.replace("//", "/")
                if _oldMusicTagsValues["path"] != newFilePath:
                    return InputOutputs.moveOrChange(_oldMusicTagsValues["path"], newFilePath, InputOutputs.getObjectType(_oldMusicTagsValues["path"]))
            #Making changes on image files
            else:
                tagger.addImage(_ImageType,_ImagePath)
                tagger.update()
                return None
        return _oldMusicTagsValues["path"]
    
        
