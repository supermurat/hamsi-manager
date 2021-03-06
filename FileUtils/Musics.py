# This file is part of HamsiManager.
#
# Copyright (c) 2010 - 2015 Murat Demir <mopened@gmail.com>
#
# Hamsi Manager is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Hamsi Manager is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with HamsiManager; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA


import FileUtils as fu
from Core.MyObjects import *
from time import gmtime
from Core import Dialogs
from Core import Organizer
from Core import Records
from Core import Universals as uni
import Taggers


def readMusicFile(_filePath, _isAlertWhenNotAvailable=True):
    _directoryPath = fu.getDirName(_filePath)
    isCanNoncompatible = False
    if fu.isReadableFileOrDir(_filePath):
        tagger = Taggers.getTagger()
        try:
            tagger.loadFile(_filePath)
        except:
            Dialogs.showError(translate("FileUtils/Musics", "Incorrect Tag"),
                              str(translate("FileUtils/Musics",
                                            "\"%s\" : this file has the incorrect tag so can't read tags.")
                              ) % Organizer.getLink(_filePath))
        if tagger.isAvailableFile() is False:
            isCanNoncompatible = True
        content = {}
        content["path"] = _filePath
        content["baseNameOfDirectory"] = fu.getBaseName(_directoryPath)
        content["baseName"] = fu.getBaseName(_filePath)
        content["artist"] = tagger.getArtist()
        content["title"] = tagger.getTitle()
        content["album"] = tagger.getAlbum()
        content["albumArtist"] = tagger.getAlbumArtist()
        content["trackNum"] = tagger.getTrackNum()
        content["year"] = tagger.getYear()
        content["genre"] = tagger.getGenre()
        content["firstComment"] = tagger.getFirstComment()
        content["firstLyrics"] = tagger.getFirstLyrics()
        content["images"] = tagger.getImages()
        if isCanNoncompatible and _isAlertWhenNotAvailable:
            Dialogs.show(translate("FileUtils/Musics", "Possible ID3 Mismatch"),
                         translate("FileUtils/Musics",
                                   "Some of the files presented in the table may not support ID3 technology.<br>Please check the files and make sure they support ID3 information before proceeding."))
        return content


def writeMusicFile(_oldMusicTagsValues, _newMusicTagsValues, _isImageAction=False, _ImageType=False, _ImagePath=False,
                   _imageDescription=u""):
    if fu.isWritableFileOrDir(_oldMusicTagsValues["path"]):
        baseNameOfDirectory = _oldMusicTagsValues["baseNameOfDirectory"]
        baseName = _oldMusicTagsValues["baseName"]
        tagger = Taggers.getTagger()
        tagger.loadFileForWrite(_oldMusicTagsValues["path"])
        if _isImageAction is False:
            if _newMusicTagsValues["artist"] != _oldMusicTagsValues["artist"]:
                tagger.setArtist(str(_newMusicTagsValues["artist"]))
            if _newMusicTagsValues["title"] != _oldMusicTagsValues["title"]:
                tagger.setTitle(str(_newMusicTagsValues["title"]))
            if _newMusicTagsValues["album"] != _oldMusicTagsValues["album"]:
                tagger.setAlbum(str(_newMusicTagsValues["album"]))
            if _newMusicTagsValues["albumArtist"] != _oldMusicTagsValues["albumArtist"]:
                tagger.setAlbumArtist(str(_newMusicTagsValues["albumArtist"]))
            if _newMusicTagsValues["trackNum"] != _oldMusicTagsValues["trackNum"]:
                tagger.setTrackNum(_newMusicTagsValues["trackNum"])
            if _newMusicTagsValues["year"] != _oldMusicTagsValues["year"]:
                tagger.setDate(str(_newMusicTagsValues["year"]))
            if _newMusicTagsValues["genre"] != _oldMusicTagsValues["genre"]:
                tagger.setGenre(str(_newMusicTagsValues["genre"]))
            if _newMusicTagsValues["firstComment"] != _oldMusicTagsValues["firstComment"]:
                tagger.setFirstComment(str(_newMusicTagsValues["firstComment"]))
            if _newMusicTagsValues["firstLyrics"] != _oldMusicTagsValues["firstLyrics"]:
                tagger.setFirstLyrics(str(_newMusicTagsValues["firstLyrics"]))
            tagger.update()
            if _newMusicTagsValues["baseNameOfDirectory"] != _oldMusicTagsValues["baseNameOfDirectory"]:
                baseNameOfDirectory = str(_newMusicTagsValues["baseNameOfDirectory"])
            if _newMusicTagsValues["baseName"] != _oldMusicTagsValues["baseName"]:
                baseName = str(_newMusicTagsValues["baseName"])
            newFilePath = fu.joinPath(fu.getDirName(fu.getDirName(_oldMusicTagsValues["path"])), baseNameOfDirectory,
                                      baseName)
            if fu.getRealPath(_oldMusicTagsValues["path"]) != fu.getRealPath(newFilePath):
                return fu.moveOrChange(_oldMusicTagsValues["path"], newFilePath,
                                       fu.getObjectType(_oldMusicTagsValues["path"]))
        #Making changes on image files
        else:
            if _ImagePath is False:
                tagger.removeImage(_imageDescription)
            else:
                tagger.addImage(_ImageType, _ImagePath, _imageDescription)
            tagger.update()
            return None
    return _oldMusicTagsValues["path"]


