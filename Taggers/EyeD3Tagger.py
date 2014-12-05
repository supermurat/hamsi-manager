# This file is part of HamsiManager.
#
# Copyright (c) 2010 - 2014 Murat Demir <mopened@gmail.com>
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


isAvailable = False
try:
    import eyed3
    from eyed3 import id3
    from eyed3 import mp3

    isAvailable = True
except: pass
from Core.MyObjects import *
import FileUtils as fu
from Core import Universals as uni
from datetime import datetime


class Tagger():
    # eyed3 usage examples in python/site-packages/eyed3/plugins/classic.py
    def __init__(self):
        self.pluginName = "Eyed3"
        self.isSupportImages = True
        self.filePath = None
        self.tag = None
        self.isCorrect = True
        self.isSave = False
        self.isNeedUpdate = False

    def loadFile(self, _filePath, _tagVersion=id3.ID3_V2_4):
        self.filePath = _filePath
        self.isCorrect = False
        self.isSave = False
        self.isNeedUpdate = False
        try:
            self.tag = id3.TagFile(uni.trEncode(self.filePath, fu.fileSystemEncoding), _tagVersion).tag
        except:
            self.tag = id3.TagFile(self.filePath, _tagVersion).tag
        if self.tag is None:
            self.isNeedUpdate = True
            self.isSave = True
            self.tag = id3.Tag()
            self.tag.parse(self.filePath, id3.ID3_ANY_VERSION)
        elif not self.tag.isV2():
            self.isNeedUpdate = True
            self.isSave = True

    def loadFileForWrite(self, _filePath, _isCorrect=True):
        self.filePath = _filePath
        self.isCorrect = _isCorrect
        self.isSave = False
        self.isNeedUpdate = False
        try:
            self.tag = id3.TagFile(uni.trEncode(self.filePath, fu.fileSystemEncoding), id3.ID3_V2_4).tag
        except:
            self.tag = id3.TagFile(self.filePath, id3.ID3_V2_4).tag
        if self.tag is None:
            self.isNeedUpdate = True
            self.isSave = True
            self.tag = id3.Tag()
            self.tag.parse(self.filePath, id3.ID3_ANY_VERSION)
        elif not self.tag.isV2():
            self.isNeedUpdate = True
            self.isSave = True

    def update(self):
        if self.isCorrect or self.isNeedUpdate:
            self.tag.save(version=id3.ID3_V2_4, encoding="utf8")
        elif self.isSave:
            self.tag.save()

    def isAvailableFile(self):
        if fu.checkExtension(self.filePath, "mp3"):
            return True
        return False

    def getCorrectedValues(self, _value):
        if _value is None or _value == "None" or _value == "None/None":
            return ""
        return _value

    def getCorrectedValuesForMusicTagType(self, _value):
        _value = self.getCorrectedValues(_value)
        if not self.tag.isV2():
            return uni.trEncode(uni.trUnicode(_value), "latin1")
        else:
            return _value

    def correctValuesForMusicTagType(self, _value):
        return uni.trUnicode(str(_value))

    def getArtist(self):
        try: return self.getCorrectedValuesForMusicTagType(str(self.tag._getArtist()))
        except: return ""


    def getAlbumArtist(self):
        try: return self.getCorrectedValuesForMusicTagType(str(self.tag.getTextFrame("TPE2")))
        except: return ""

    def getTitle(self):
        try: return self.getCorrectedValuesForMusicTagType(str(self.tag._getTitle()))
        except: return ""

    def getAlbum(self):
        try: return self.getCorrectedValuesForMusicTagType(str(self.tag._getAlbum()))
        except: return ""

    def getTrackNum(self):
        try:
            if self.tag.isV2():
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
        try:return self.getCorrectedValuesForMusicTagType(str(self.tag.comments[0].text))
        except: return ""

    def getFirstLyrics(self):
        try: return self.getCorrectedValuesForMusicTagType(str(self.tag.lyrics[0].text))
        except: return ""

    def getImages(self):
        try:
            images = []
            imageTypes = self.getImageTypes()
            imageTypesNo = self.getImageTypesNo()
            for image in self.tag.images:
                images.append([])
                for no, imageType in enumerate(imageTypes):
                    if str(image.picture_type) == imageTypesNo[no]:
                        images[-1].append(no)
                        images[-1].append(imageType)
                        break
                images[-1].append(image.mime_type)
                images[-1].append(image.image_data)
                images[-1].append(image.description)
            return images
        except:
            return []

    def setArtist(self, _value):
        self.isSave = True
        self.tag._setArtist(self.correctValuesForMusicTagType(_value))

    def setAlbumArtist(self, _value):
        self.isSave = True
        self.tag.setTextFrame("TPE2", self.correctValuesForMusicTagType(_value))

    def setTitle(self, _value):
        self.isSave = True
        self.tag._setTitle(self.correctValuesForMusicTagType(_value))

    def setAlbum(self, _value):
        self.isSave = True
        self.tag._setAlbum(self.correctValuesForMusicTagType(_value))

    def setTrackNum(self, _value):
        self.isSave = True
        if _value.find("/") != -1:
            self.tag._setTrackNum(tuple(_value.split("/")))
        else:
            val = _value
            try: val = int(val)
            except: val = None
            self.tag._setTrackNum((val, None))

    def setDate(self, _value):
        self.isSave = True
        if len(str(_value)) == 4:
            val = _value
            try:
                val = int(val)
            except:
                val = None
            try:
                self.tag._setRecordingDate(val)
            except AttributeError as err:
                self.tag._setRecordingDate(datetime.strptime(str(val), '%Y'))
        elif _value == "":
            self.tag._setRecordingDate(None)
        else:
            try:
                self.tag._setRecordingDate(datetime.today().year)
            except AttributeError as err:
                self.tag._setRecordingDate(datetime.today())

    def setGenre(self, _value):
        self.isSave = True
        self.tag._setGenre(self.correctValuesForMusicTagType(_value))

    def setFirstComment(self, _value):
        self.isSave = True
        self.tag.comments.set(self.correctValuesForMusicTagType(_value), u"", "eng")

    def setFirstLyrics(self, _value):
        self.isSave = True
        self.tag.lyrics.set(self.correctValuesForMusicTagType(_value), u"", "eng")

    def addImage(self, _imageType, _imagePath, _description):
        self.isSave = True
        imageData = fu.readFromBinaryFile(_imagePath)
        mimeType = fu.getMimeType(_imagePath)[0]
        self.tag.images.set(int(_imageType), imageData, mimeType, uni.trUnicode(_description))

    def removeImage(self, _description):
        self.isSave = True
        self.tag.images.remove(uni.trUnicode(_description))

    def getImageTypes(self):
        return ["Other (Default)", "Icon", "Other Icon", "Front Cover", "Back Cover", "Leaflet", "Media",
                "Lead Artist", "Artist", "Leader", "Band", "Composer", "Lyrics By", "Recorded At",
                "Recording", "Performing", "Video", "Made Famous", "Example", "Band Logo", "Publisher Logo"]

    def getImageTypesNo(self):
        return ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "10", "11", "12", "13",
                "14"]

    def getAvailableKeysForTable(self):
        return ["baseNameOfDirectory", "baseName", "artist", "title", "album", "albumArtist",
                "trackNum", "year", "genre", "firstComment", "firstLyrics"]

    def getReadOnlyKeysForTable(self):
        return []

    def getAvailableLabelsForTable(self):
        return [translate("MusicTable", "Directory"),
                translate("MusicTable", "File Name"),
                translate("MusicTable", "Artist"),
                translate("MusicTable", "Title"),
                translate("MusicTable", "Album"),
                translate("MusicTable", "Album Artist"),
                translate("MusicTable", "Track No"),
                translate("MusicTable", "Year"),
                translate("MusicTable", "Genre"),
                translate("MusicTable", "Comment"),
                translate("MusicTable", "Lyrics")]
