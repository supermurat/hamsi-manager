## This file is part of HamsiManager.
##
## Copyright (c) 2010 - 2014 Murat Demir <mopened@gmail.com>
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
try:
    import eyeD3

    isAvailable = True
except: pass
import Taggers
from Core.MyObjects import *
import FileUtils as fu
from Core import Universals as uni

pluginName = "eyeD3"


class Tagger():
    def __init__(self):
        self.filePath = None
        self.tag = None
        self.Mp3AudioFile = None

    def loadFile(self, _filePath):
        self.filePath = _filePath
        try:
            self.tag = eyeD3.Tag()
            self.tag.link(uni.trEncode(self.filePath, fu.fileSystemEncoding),
                          Taggers.getSelectedTaggerTypeForRead())
        except:
            self.tag = eyeD3.Tag()
            self.tag.link(self.filePath, Taggers.getSelectedTaggerTypeForRead())
        try:
            self.Mp3AudioFile = eyeD3.Mp3AudioFile(uni.trEncode(self.filePath, fu.fileSystemEncoding))
        except:
            try:
                self.Mp3AudioFile = eyeD3.Mp3AudioFile(self.filePath)
            except:
                self.Mp3AudioFile = None

    def loadFileForWrite(self, _filePath, _isCorrect=True):
        self.filePath = _filePath
        try:
            self.tag = eyeD3.Tag()
            self.tag.link(uni.trEncode(self.filePath, fu.fileSystemEncoding),
                          Taggers.getSelectedTaggerTypeForWrite())
        except:
            self.tag = eyeD3.Tag()
            self.tag.link(self.filePath, Taggers.getSelectedTaggerTypeForWrite())
        self.Mp3AudioFile = None
        if _isCorrect: self.correctForMusicTagType()

    def update(self):
        self.tag.update()

    def isAvailableFile(self):
        if fu.checkExtension(self.filePath, "mp3") or fu.checkExtension(self.filePath, "ogg"):
            return True
        return False

    def getCorrectedValues(self, _value):
        if _value == None or _value == "None" or _value == "None/None":
            return ""
        return _value

    def getCorrectedValuesForMusicTagType(self, _value):
        _value = self.getCorrectedValues(_value)
        if Taggers.getSelectedTaggerTypeForRead() == eyeD3.ID3_V1:
            return uni.trEncode(uni.trUnicode(_value), "latin1")
        else:
            return _value

    def correctValuesForMusicGenre(self, _genre):
        import re

        regex = re.compile("^[A-Z 0-9+/\-\|!&'\.]+\00*$", re.IGNORECASE)
        genreStrAmended = ""
        for x in [y for x, y in enumerate(_genre) if regex.match(y)]:
            genreStrAmended += x
        return str(genreStrAmended)

    def correctValuesForMusicTagType(self, _value):
        if Taggers.getSelectedTaggerTypeForWrite() == eyeD3.ID3_V1:
            return uni.trUnicode(str(_value), "latin1")
        else:
            return uni.trUnicode(str(_value))

    def correctForMusicTagType(self):
        self.tag.setVersion(Taggers.getSelectedTaggerTypeForWrite())
        if Taggers.getSelectedTaggerTypeForWrite() == eyeD3.ID3_V2:
            self.tag.setTextEncoding(eyeD3.frames.UTF_8_ENCODING)

    def getArtist(self):
        try: return self.getCorrectedValuesForMusicTagType(str(self.tag.getArtist()))
        except: return ""

    def getTitle(self):
        try: return self.getCorrectedValuesForMusicTagType(str(self.tag.getTitle()))
        except: return ""

    def getAlbum(self):
        try: return self.getCorrectedValuesForMusicTagType(str(self.tag.getAlbum()))
        except: return ""

    def getTrackNum(self):
        try:
            if Taggers.getSelectedTaggerTypeForRead() == eyeD3.ID3_V2:
                trackNum = self.tag.getTrackNum()
                if trackNum[1] is not None:
                    return self.getCorrectedValues(str(trackNum[0]) + "/" + str(trackNum[1]))
                else:
                    return self.getCorrectedValues(trackNum[0])
            else:
                return self.getCorrectedValues(self.tag.getTrackNum()[0])
        except: return ""

    def getYear(self):
        try: return self.getCorrectedValues(self.tag.getYear())
        except: return ""

    def getGenre(self):
        try: return self.getCorrectedValuesForMusicTagType(str(self.tag.getGenre()))
        except: return ""

    def getFirstComment(self):
        try: return self.getCorrectedValuesForMusicTagType(str(self.tag.getComment()))
        except: return ""

    def getFirstLyrics(self):
        try:
            if len(self.tag.getLyrics()) > 0:
                return self.getCorrectedValuesForMusicTagType(str(self.tag.getLyrics()[0].lyrics))
            else:
                return ""
        except: return ""

    def getImages(self):
        try:
            images = []
            imageTypes = getImageTypes()
            imageTypesNo = getImageTypesNo()
            for image_no, image in enumerate(self.tag.getImages()):
                images.append([])
                for no, type in enumerate(imageTypes):
                    if str(image.pictureType) == imageTypesNo[no]:
                        images[image_no].append(no)
                        images[image_no].append(type)
                        break
                images[image_no].append(image.mimeType)
                images[image_no].append(image.imageData)
                images[image_no].append(str(images[image_no][0]))
            return images
        except:
            return []

    def setArtist(self, _value):
        self.tag.setArtist(self.correctValuesForMusicTagType(_value))

    def setTitle(self, _value):
        self.tag.setTitle(self.correctValuesForMusicTagType(_value))

    def setAlbum(self, _value):
        self.tag.setAlbum(self.correctValuesForMusicTagType(_value))

    def setTrackNum(self, _value):
        if _value.find("/") != -1:
            if Taggers.getSelectedTaggerTypeForRead() == eyeD3.ID3_V2:
                self.tag.setTrackNum(_value.split("/"))
            else:
                self.tag.setTrackNum([_value.split("/")[0], None])
        else:
            self.tag.setTrackNum([_value, None])

    def setDate(self, _value):
        if len(_value) == 4:
            self.tag.setDate(_value)
        elif _value == "":
            self.tag.setDate(None)
        else:
            from time import gmtime

            self.tag.setDate(gmtime()[0])

    def setGenre(self, _value):
        self.tag.setGenre(self.correctValuesForMusicGenre(self.correctValuesForMusicTagType(_value)))

    def setFirstComment(self, _value):
        self.tag.removeComments()
        self.tag.addComment(self.correctValuesForMusicTagType(_value))

    def setFirstLyrics(self, _value):
        self.tag.removeLyrics()
        self.tag.addLyrics(self.correctValuesForMusicTagType(_value))

    def addImage(self, _ImageType, _ImagePath, _description):
        if Taggers.getSelectedTaggerTypeForRead() == eyeD3.ID3_V2:
            try: self.tag.addImage(int(_ImageType), uni.trEncode(_ImagePath, fu.fileSystemEncoding))
            except: self.tag.addImage(int(_ImageType), _ImagePath)

    def removeImage(self, _description):
        if Taggers.getSelectedTaggerTypeForRead() == eyeD3.ID3_V2:
            self.tag.addImage(int(_description), False)


def getImageTypes():
    return ["Other (Default)", "Icon", "Other Icon", "Front Cover", "Back Cover", "Leaflet", "Media",
            "Lead Artist", "Artist", "Leader", "Band", "Composer", "Lyrics By", "Recorded At",
            "Recording", "Performing", "Video", "Made Famous", "Example", "Band Logo", "Publisher Logo"]


def getImageTypesNo():
    return ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "10", "11", "12", "13",
            "14"]


def getTaggerTypes():
    return [eyeD3.ID3_V2, eyeD3.ID3_V1]


def getTaggerTypesName():
    return ["ID3 V2", "ID3 V1"]


def getAvailableKeysForTable():
    keys = ["Directory", "File Name", "Artist", "Title", "Album",
            "Track No", "Year", "Genre", "Comment", "Lyrics"]
    if Taggers.getSelectedTaggerTypeForRead() != getTaggerTypes()[0]:
        t = keys.pop()
    return keys


def getAvailableLabelsForTable():
    labels = [translate("MusicTable", "Directory"),
              translate("MusicTable", "File Name"),
              translate("MusicTable", "Artist"),
              translate("MusicTable", "Title"),
              translate("MusicTable", "Album"),
              translate("MusicTable", "Track No"),
              translate("MusicTable", "Year"),
              translate("MusicTable", "Genre"),
              translate("MusicTable", "Comment"),
              translate("MusicTable", "Lyrics")]
    if Taggers.getSelectedTaggerTypeForRead() != getTaggerTypes()[0]:
        t = labels.pop()
    return labels


        
        
        
