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
    import taglib

    isAvailable = True
except: pass
from Core.MyObjects import *
import FileUtils as fu
from Core import Universals as uni
from datetime import datetime


class Tagger():
    def __init__(self):
        self.pluginName = "Taglib"
        self.isSupportImages = False
        self.isSupportInfo = True
        self.filePath = None
        self.tagFile = None
        self.tags = None
        self.isCorrect = True
        self.isSave = False
        self.isNeedUpdate = False

    def loadFile(self, _filePath):
        self.tags = None
        self.tagFile = None
        self.filePath = _filePath
        self.isCorrect = False
        self.isSave = False
        self.isNeedUpdate = False
        try:
            self.tagFile = taglib.File(uni.trEncode(self.filePath, fu.fileSystemEncoding))
            self.tags = self.tagFile.tags
        except:
            self.tagFile = taglib.File(self.filePath)
            self.tags = self.tagFile.tags

    def loadFileForWrite(self, _filePath, _isCorrect=True):
        self.tags = None
        self.tagFile = None
        self.filePath = _filePath
        self.isCorrect = _isCorrect
        self.isSave = False
        self.isNeedUpdate = False
        try:
            self.tagFile = taglib.File(uni.trEncode(self.filePath, fu.fileSystemEncoding))
            self.tags = self.tagFile.tags
        except:
            self.tagFile = taglib.File(uni.trEncode(self.filePath, fu.fileSystemEncoding))
            self.tags = self.tagFile.tags

    def update(self):
        retval = {}
        if self.isCorrect or self.isNeedUpdate:
            retval = self.tagFile.save()
        elif self.isSave:
            retval = self.tagFile.save()
        if len(retval) > 0:
            raise Exception('Exception of pytaglib - tag.save():' + str({}))

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
        return _value

    def correctValuesForMusicTagType(self, _value):
        return uni.trUnicode(str(_value))

    def getArtist(self):
        try: return self.getCorrectedValuesForMusicTagType(str(self.tags["ARTIST"][0]))
        except: return ""


    def getAlbumArtist(self):
        try: return self.getCorrectedValuesForMusicTagType(str(self.tags["ALBUMARTIST"][0]))
        except: return ""

    def getTitle(self):
        try: return self.getCorrectedValuesForMusicTagType(str(self.tags["TITLE"][0]))
        except: return ""

    def getAlbum(self):
        try: return self.getCorrectedValuesForMusicTagType(str(self.tags["ALBUM"][0]))
        except: return ""

    def getTrackNum(self):
        try:
            return self.getCorrectedValues(str(self.tags["TRACKNUMBER"][0]) + "/" + str(self.tags["DISCNUMBER"][0]))
        except:
            try:
                return self.getCorrectedValues(str(self.tags["TRACKNUMBER"][0]))
            except:
                return ""

    def getYear(self):
        try: return self.getCorrectedValues(self.tags["DATE"][0])
        except: return ""

    def getGenre(self):
        try: return self.getCorrectedValuesForMusicTagType(str(self.tags["GENRE"][0]))
        except: return ""

    def getFirstComment(self):
        try: return self.getCorrectedValuesForMusicTagType(str(self.tags["COMMENT"][0]))
        except: return ""

    def getFirstLyrics(self):
        try: return self.getCorrectedValuesForMusicTagType(str(self.tags["LYRICS"][0]))
        except: return ""

    def getImages(self):
        return []

    def getLength(self):
        try: return str(round((float(self.tagFile.length) / 60), 2)).replace(".", ":")
        except: return ""

    def getBitrate(self):
        try: return str(self.tagFile.bitrate) + " kbps"
        except: return ""

    def getSampleRate(self):
        try: return str(self.tagFile.sampleRate) + " Hz"
        except: return ""

    def getMode(self):
        modes = {1: "MONO", 2: "STEREO"}
        try: return modes[self.tagFile.channels]
        except: return ""

    def setArtist(self, _value):
        self.isSave = True
        self.tags["ARTIST"] = [self.correctValuesForMusicTagType(_value)]

    def setAlbumArtist(self, _value):
        self.isSave = True
        self.tags["ALBUMARTIST"] = [self.correctValuesForMusicTagType(_value)]

    def setTitle(self, _value):
        self.isSave = True
        self.tags["TITLE"] = [self.correctValuesForMusicTagType(_value)]

    def setAlbum(self, _value):
        self.isSave = True
        self.tags["ALBUM"] = [self.correctValuesForMusicTagType(_value)]

    def setTrackNum(self, _value):
        self.isSave = True
        values = _value.split("/")
        try:
            self.tags["TRACKNUMBER"] = [str(int(values[0].strip()))]
            if len(values) > 1:
                self.tags["DISCNUMBER"] = [str(int(values[1].strip()))]
            elif len(values) == 1 and self.tags["DISCNUMBER"] is not None:
                del self.tags["DISCNUMBER"]
        except:
            pass

    def setDate(self, _value):
        self.isSave = True
        try:
            self.tags["DATE"] = [str(int(_value))]
        except:
            pass

    def setGenre(self, _value):
        self.isSave = True
        self.tags["GENRE"] = [self.correctValuesForMusicTagType(_value)]

    def setFirstComment(self, _value):
        self.isSave = True
        self.tags["COMMENT"] = [self.correctValuesForMusicTagType(_value)]

    def setFirstLyrics(self, _value):
        self.isSave = True
        self.tags["LYRICS"] = [self.correctValuesForMusicTagType(_value)]

    def addImage(self, _imageType, _imagePath, _description):
        pass

    def removeImage(self, _description):
        pass

    def getImageTypes(self):
        return ["No Support"]

    def getImageTypesNo(self):
        return ["-1"]

    def getAvailableKeysForTable(self):
        return ["baseNameOfDirectory", "baseName", "artist", "title", "album", "albumArtist",
                "trackNum", "year", "genre", "firstComment", "firstLyrics", "length", "bitrate", "sampleRate", "mode"]

    def getReadOnlyKeysForTable(self):
        return ["length", "bitrate", "sampleRate", "mode"]

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
                translate("MusicTable", "Lyrics"),
                translate("MusicTable", "Length"),
                translate("MusicTable", "Bitrate"),
                translate("MusicTable", "Sample Rate"),
                translate("MusicTable", "Mode")]
