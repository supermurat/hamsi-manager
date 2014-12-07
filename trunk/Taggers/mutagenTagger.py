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
    from mutagen import id3
    from mutagen import mp3

    isAvailable = True
except: pass
from Core.MyObjects import *
import FileUtils as fu
from Core import Universals as uni


class Tagger():
    def __init__(self):
        self.pluginName = "Mutagen"
        self.isSupportImages = True
        self.isSupportInfo = True
        self.filePath = None
        self.tags = None
        self.info = None
        self.isCorrect = True
        self.isSave = False
        self.isNeedUpdate = False

    def loadFile(self, _filePath):
        self.filePath = _filePath
        self.isCorrect = False
        self.isSave = False
        self.isNeedUpdate = False
        try:
            self.tags = id3.ID3(uni.trEncode(self.filePath, fu.fileSystemEncoding))
            self.info = mp3.MP3(uni.trEncode(self.filePath, fu.fileSystemEncoding)).info
        except:
            self.tags = id3.ID3(self.filePath)
            self.info = mp3.MP3(self.filePath).info
        if self.tags.version is not (2, 4, 0):
            self.isNeedUpdate = True
            self.isSave = True

    def loadFileForWrite(self, _filePath, _isCorrect=True):
        self.filePath = _filePath
        self.isCorrect = _isCorrect
        self.isSave = False
        self.isNeedUpdate = False
        try:
            self.tags = id3.ID3(uni.trEncode(self.filePath, fu.fileSystemEncoding))
        except:
            self.tags = id3.ID3(self.filePath)
        if self.tags.version is not (2, 4, 0):
            self.isNeedUpdate = True
            self.isSave = True

    def update(self):
        if self.isCorrect or self.isNeedUpdate:
            self.tags.update_to_v24()
            self.tags.save()
        elif self.isSave:
            self.tags.save()

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
        try: return self.getCorrectedValuesForMusicTagType(str(self.tags["TPE1"]))
        except: return ""

    def getAlbumArtist(self):
        try: return self.getCorrectedValuesForMusicTagType(str(self.tags["TPE2"]))
        except: return ""

    def getTitle(self):
        try: return self.getCorrectedValuesForMusicTagType(str(self.tags["TIT2"]))
        except: return ""

    def getAlbum(self):
        try: return self.getCorrectedValuesForMusicTagType(str(self.tags["TALB"]))
        except: return ""

    def getTrackNum(self):
        try:
            return self.getCorrectedValues(str(self.tags["TRCK"]) + "/" + str(self.tags["TPOS"]))
        except:
            try:
                return self.getCorrectedValues(str(self.tags["TRCK"]))
            except:
                return ""

    def getYear(self):
        try: return self.getCorrectedValues(self.tags["TDRC"])
        except: return ""

    def getGenre(self):
        try: return self.getCorrectedValuesForMusicTagType(str(self.tags["TCON"]))
        except: return ""

    def getFirstComment(self):
        try: return self.getCorrectedValuesForMusicTagType(str(self.tags.getall("COMM")[0].text[0]))
        except: return ""

    def getFirstLyrics(self):
        try: return self.getCorrectedValuesForMusicTagType(str(self.tags.getall("USLT")[0]))
        except: return ""

    def getImages(self):
        try:
            images = []
            imageTypes = self.getImageTypes()
            imageTypesNo = self.getImageTypesNo()
            for image in self.tags.getall("APIC"):
                images.append([])
                for no, imageType in enumerate(imageTypes):
                    if str(image.type) == imageTypesNo[no]:
                        images[-1].append(no)
                        images[-1].append(imageType)
                        break
                images[-1].append(image.mime)
                images[-1].append(image.data)
                images[-1].append(image.desc)
            return images
        except:
            return []

    def getLength(self):
        try: return str(round((self.info.length / 60), 2)).replace(".", ":")
        except: return ""

    def getBitrate(self):
        try: return str(self.info.bitrate / 1000) + " kbps"
        except: return ""

    def getSampleRate(self):
        try: return str(self.info.sample_rate) + " Hz"
        except: return ""

    def getMode(self):
        modes = {0: "STEREO", 1: "JOINTSTEREO", 2: "DUALCHANNEL", 3: "MONO"}
        try: return modes[self.info.mode]
        except: return ""

    def setArtist(self, _value):
        self.isSave = True
        self.tags["TPE1"] = id3.TPE1(encoding=3, text=self.correctValuesForMusicTagType(_value))

    def setAlbumArtist(self, _value):
        self.isSave = True
        self.tags["TPE2"] = id3.TPE2(encoding=3, text=self.correctValuesForMusicTagType(_value))

    def setTitle(self, _value):
        self.isSave = True
        self.tags["TIT2"] = id3.TIT2(encoding=3, text=self.correctValuesForMusicTagType(_value))

    def setAlbum(self, _value):
        self.isSave = True
        self.tags["TALB"] = id3.TALB(encoding=3, text=self.correctValuesForMusicTagType(_value))

    def setTrackNum(self, _value):
        self.isSave = True
        values = _value.split("/")
        try:
            self.tags["TRCK"] = id3.TRCK(encoding=3, text=str(int(self.correctValuesForMusicTagType(values[0]))))
            if len(values) > 1:
                self.tags["TPOS"] = id3.TPOS(encoding=3, text=str(int(self.correctValuesForMusicTagType(values[1]))))
        except:
            pass

    def setDate(self, _value):
        self.isSave = True
        try:
            self.tags["TDRC"] = id3.TDRC(encoding=3, text=str(int(self.correctValuesForMusicTagType(_value))))
        except:
            pass

    def setGenre(self, _value):
        self.isSave = True
        self.tags["TCON"] = id3.TCON(encoding=3, text=self.correctValuesForMusicTagType(_value))

    def setFirstComment(self, _value):
        self.isSave = True
        keys = self.tags.getall("COMM")
        for key in keys:
            self.tags[key.HashKey] = id3.COMM(encoding=3, text=self.correctValuesForMusicTagType(_value),
                                              lang=key.lang, desc=key.desc)
        if len(keys) == 0:
            #self.tags["COMM::'XXX'"] = id3.COMM(encoding=3, text=self.correctValuesForMusicTagType(_value), lang="XXX")
            self.tags["COMM::'eng'"] = id3.COMM(encoding=3, text=self.correctValuesForMusicTagType(_value), lang="eng")

    def setFirstLyrics(self, _value):
        self.isSave = True
        keys = self.tags.getall("USLT")
        for key in keys:
            self.tags[key.HashKey] = id3.USLT(encoding=3, text=self.correctValuesForMusicTagType(_value),
                                              lang=key.lang, desc=key.desc)
        if len(keys) == 0:
            #self.tags["USLT::'XXX'"] = id3.USLT(encoding=3, text=self.correctValuesForMusicTagType(_value), lang="XXX")
            self.tags["USLT::'eng'"] = id3.USLT(encoding=3, text=self.correctValuesForMusicTagType(_value), lang="eng")

    def addImage(self, _imageType, _imagePath, _description):
        self.isSave = True
        imageData = fu.readFromBinaryFile(_imagePath)
        mimeType = fu.getMimeType(_imagePath)[0]
        self.tags.add(id3.APIC(encoding=3, mime=mimeType, type=int(_imageType),
                                           desc=uni.trUnicode(_description), data=imageData))

    def removeImage(self, _description):
        self.isSave = True
        for no, img in enumerate(self.tags.getall("APIC")):
            if img.desc == _description:
                del self.tags[img.HashKey]

    def getImageTypes(self):
        return ["Other (Default)", "Icon", "Other Icon", "Front Cover", "Back Cover", "Leaflet", "Media",
                "Lead Artist", "Artist", "Leader", "Band", "Composer", "Lyrics By", "Recorded At",
                "Recording", "Performing", "Video", "Made Famous", "Example", "Band Logo", "Publisher Logo"]

    def getImageTypesNo(self):
        return ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "10", "11", "12", "13",
                "14"]

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
