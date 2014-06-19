# # This file is part of HamsiManager.
# #
# # Copyright (c) 2010 - 2013 Murat Demir <mopened@gmail.com>
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
    import eyed3
    from eyed3 import id3
    from eyed3 import mp3

    isAvailable = True
except: pass
import Taggers
from Core.MyObjects import *
import FileUtils as fu
from Core import Universals as uni

pluginName = "eyed3"


class Tagger():
    def __init__(self):
        self.filePath = None
        self.tag = None
        self.isCorrect = True

    def loadFile(self, _filePath):
        self.filePath = _filePath
        self.isCorrect = True
        try:
            self.tag = id3.TagFile(uni.trEncode(self.filePath, fu.fileSystemEncoding),
                                   Taggers.getSelectedTaggerTypeForRead()).tag
        except:
            self.tag = id3.TagFile(self.filePath, Taggers.getSelectedTaggerTypeForRead()).tag

    def loadFileForWrite(self, _filePath, _isCorrect=True):
        self.filePath = _filePath
        self.isCorrect = _isCorrect
        try:
            self.tag = id3.TagFile(uni.trEncode(self.filePath, fu.fileSystemEncoding),
                                   Taggers.getSelectedTaggerTypeForWrite()).tag
        except:
            self.tag = id3.TagFile(self.filePath, Taggers.getSelectedTaggerTypeForWrite()).tag

    def update(self):
        if self.isCorrect:
            selectedTaggerTypeForWrite = Taggers.getSelectedTaggerTypeForWrite()
            self.tag.save(version=selectedTaggerTypeForWrite, encoding="utf8")
        else:
            self.tag.save()

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
        if Taggers.getSelectedTaggerTypeForRead() in (id3.ID3_V1_1, id3.ID3_V1_0, id3.ID3_V1):
            return uni.trEncode(uni.trUnicode(_value), "latin1")
        else:
            return _value

    def correctValuesForMusicTagType(self, _value):
        if Taggers.getSelectedTaggerTypeForWrite() in (id3.ID3_V1_1, id3.ID3_V1_0, id3.ID3_V1):
            return uni.trUnicode(str(_value), "latin1")
        else:
            return uni.trUnicode(str(_value))

    def getArtist(self):
        try: return self.getCorrectedValuesForMusicTagType(str(self.tag._getArtist()))
        except: return ""

    def getTitle(self):
        try: return self.getCorrectedValuesForMusicTagType(str(self.tag._getTitle()))
        except: return ""

    def getAlbum(self):
        try: return self.getCorrectedValuesForMusicTagType(str(self.tag._getAlbum()))
        except: return ""

    def getTrackNum(self):
        try:
            if Taggers.getSelectedTaggerTypeForRead() in (id3.ID3_V2_4, id3.ID3_V2_3, id3.ID3_V2_2, id3.ID3_V2):
                trackNum = self.tag._getTrackNum()
                if trackNum[1] is not None:
                    return self.getCorrectedValues(str(trackNum[0]) + "/" + str(trackNum[1]))
                else:
                    return self.getCorrectedValues(trackNum[0])
            else:
                return self.getCorrectedValues(self.tag._getTrackNum()[0])
        except: return ""

    def getYear(self):
        try: return self.getCorrectedValues(self.tag._getRecordingDate().year)
        except: return ""

    def getGenre(self):
        try: return self.getCorrectedValuesForMusicTagType(str(self.tag._getGenre().name))
        except: return ""

    def getFirstComment(self):
        try: return self.getCorrectedValuesForMusicTagType(str(self.tag.comments.get(u"").text))
        except: return ""

    def getFirstLyrics(self):
        try: return self.getCorrectedValuesForMusicTagType(str(self.tag.lyrics.get(u"").text))
        except: return ""

    def getImages(self):
        try:
            images = []
            imageTypes = getImageTypes()
            imageTypesNo = getImageTypesNo()
            for image in self.tag.images:
                images.append([])
                for no, type in enumerate(imageTypes):
                    if str(image.picture_type) == imageTypesNo[no]:
                        images[-1].append(no)
                        images[-1].append(type)
                        break
                images[-1].append(image.mime_type)
                images[-1].append(image.image_data)
                images[-1].append(image.description)
            return images
        except:
            return []

    def setArtist(self, _value):
        self.tag._setArtist(self.correctValuesForMusicTagType(_value))

    def setTitle(self, _value):
        self.tag._setTitle(self.correctValuesForMusicTagType(_value))

    def setAlbum(self, _value):
        self.tag._setAlbum(self.correctValuesForMusicTagType(_value))

    def setTrackNum(self, _value):
        if _value.find("/") != -1:
            if Taggers.getSelectedTaggerTypeForRead() in (id3.ID3_V2_4, id3.ID3_V2_3, id3.ID3_V2_2, id3.ID3_V2):
                self.tag._setTrackNum(tuple(_value.split("/")))
            else:
                val = _value.split("/")[0]
                try: val = int(val)
                except: val = None
                self.tag._setTrackNum((val, None))
        else:
            val = _value
            try: val = int(val)
            except: val = None
            self.tag._setTrackNum((val, None))

    def setDate(self, _value):
        if len(_value) == 4:
            val = _value
            try: val = int(val)
            except: val = None
            self.tag._setRecordingDate(val)
        elif _value == "":
            self.tag._setRecordingDate(None)
        else:
            from time import gmtime

            self.tag._setRecordingDate(gmtime()[0])

    def setGenre(self, _value):
        self.tag._setGenre(self.correctValuesForMusicTagType(_value))

    def setFirstComment(self, _value):
        self.tag.comments.set(self.correctValuesForMusicTagType(_value))

    def setFirstLyrics(self, _value):
        self.tag.lyrics.set(self.correctValuesForMusicTagType(_value))

    def addImage(self, _imageType, _imagePath, _description):
        if Taggers.getSelectedTaggerTypeForRead() in (id3.ID3_V2_4, id3.ID3_V2_3, id3.ID3_V2_2, id3.ID3_V2):
            imageData = fu.readFromBinaryFile(_imagePath)
            mimeType = fu.getMimeType(_imagePath)[0]
            self.tag.images.set(int(_imageType), imageData, mimeType, uni.trUnicode(_description))

    def removeImage(self, _description):
        if Taggers.getSelectedTaggerTypeForRead() in (id3.ID3_V2_4, id3.ID3_V2_3, id3.ID3_V2_2, id3.ID3_V2):
            self.tag.images.remove(uni.trUnicode(_description))


def getImageTypes():
    return ["Other (Default)", "Icon", "Other Icon", "Front Cover", "Back Cover", "Leaflet", "Media",
            "Lead Artist", "Artist", "Leader", "Band", "Composer", "Lyrics By", "Recorded At",
            "Recording", "Performing", "Video", "Made Famous", "Example", "Band Logo", "Publisher Logo"]


def getImageTypesNo():
    return ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "10", "11", "12", "13",
            "14"]


def getTaggerTypes():
    return [id3.ID3_V2_4, id3.ID3_V1_1]


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



        

