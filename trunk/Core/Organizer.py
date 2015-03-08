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

import time
import unicodedata
import string
import math
import re
from Core.MyObjects import *
from Core import Universals as uni
import FileUtils as fu

if uni.isPython3k:
    from urllib.parse import unquote as ounquote
    from urllib.parse import quote as oquote
else:
    from urllib import unquote as ounquote
    from urllib import quote as oquote

utf8ReplacementChars = uni.getUtf8Data("replacementChars")
utf8LittleI = uni.getUtf8Data("little+I")


def unquote(_inputString):
    return ounquote(_inputString)


def quote(_inputString):
    return oquote(_inputString)


def emend(_inputString, _type="text", _isCorrectCaseSensitive=True, _isRichText=False):
    _inputString = str(_inputString)
    if len(_inputString) == 0: return ""
    if uni.getBoolValue("isClearFirstAndLastSpaceChars"):
        _inputString = _inputString.strip()
    if len(_inputString) == 0: return ""
    if uni.getBoolValue("isEmendIncorrectChars"):
        try: _inputString = uni.trUnicode(_inputString)
        except: _inputString = uni.trUnicode(_inputString, "iso-8859-9")
        _inputString = replaceList(_inputString,
                                   utf8ReplacementChars.keys(),
                                   utf8ReplacementChars.values())
    if uni.getBoolValue("isDecodeURLStrings"):
        _inputString = unquote(_inputString)
    _inputString = str(uni.trDecode(_inputString, "utf-8", "ignore"))
    if _type == "file" or _type == "directory":
        _inputString = fu.getAvailableNameByName(_inputString)
        preString, extString, ext2String = "", "", ""
        if _inputString[-1] == fu.sep:
            _inputString = _inputString[:-1]
            ext2String = fu.sep
        if _inputString.find(fu.sep) != -1:
            tStr = _inputString.rsplit(fu.sep, 1)
            for ps in tStr[0].split(fu.sep):
                if uni.getBoolValue("isCorrectFileNameWithSearchAndReplaceTable"):
                    ps = searchAndReplaceFromSearchAndReplaceTable(ps)
                preString += emendBaseName(ps, "directory", _isCorrectCaseSensitive) + fu.sep
            _inputString = tStr[1]
        if _type == "file":
            _inputString, extString = fu.getFileNameParts(_inputString)
        if uni.getBoolValue("isCorrectFileNameWithSearchAndReplaceTable"):
            _inputString = searchAndReplaceFromSearchAndReplaceTable(_inputString)
        _inputString = emendBaseName(_inputString, _type, _isCorrectCaseSensitive)
        extString = emendFileExtension(extString, _isCorrectCaseSensitive)
        if extString != "":
            extString = "." + extString
        if preString != "":
            _inputString = fu.joinPath(preString, _inputString)
        _inputString = str(uni.trDecode(_inputString, "utf-8", "ignore")) + str(
            uni.trDecode(extString, "utf-8", "ignore")) + str(uni.trDecode(ext2String, "utf-8", "ignore"))
    else:
        if uni.getBoolValue("isCorrectValueWithSearchAndReplaceTable"):
            _inputString = searchAndReplaceFromSearchAndReplaceTable(_inputString)
        if _isCorrectCaseSensitive:
            _inputString = makeCorrectCaseSensitive(_inputString, uni.MySettings["validSentenceStructure"])
    if _isRichText is False:
        if uni.getBoolValue("isCorrectDoubleSpaceChars"):
            isFound = _inputString.find("  ")
            while isFound != -1:
                _inputString = _inputString.replace("  ", " ")
                isFound = _inputString.find("  ")
    return _inputString


def emendBaseName(_baseName, _type, _isCorrectCaseSensitive):
    baseName = _baseName
    if _isCorrectCaseSensitive:
        if _type == "file":
            baseName = makeCorrectCaseSensitive(baseName, uni.MySettings["validSentenceStructureForFile"])
        elif _type == "directory":
            baseName = makeCorrectCaseSensitive(baseName, uni.MySettings["validSentenceStructureForDirectory"])
    if (uni.MySettings["fileReNamerType"] == uni.fileReNamerTypeNamesKeys[1] or
                uni.MySettings["fileReNamerType"] == uni.fileReNamerTypeNamesKeys[2]):
        baseName = ''.join(
            c for c in unicodedata.normalize('NFKD', uni.trUnicode(baseName)) if unicodedata.category(c) != 'Mn')
        baseName = str(uni.trEncode(baseName, "utf-8", "ignore")).replace(utf8LittleI, "i")
    if uni.MySettings["fileReNamerType"] == uni.fileReNamerTypeNamesKeys[1]:
        baseName = replaceList(baseName,
                               [" "],
                               ["_"])
    if uni.MySettings["fileReNamerType"] == uni.fileReNamerTypeNamesKeys[1]:
        baseName = quote(baseName)
    return baseName


def emendFileExtension(_fileExtension, _isCorrectCaseSensitive):
    fileExtension = _fileExtension
    if _isCorrectCaseSensitive:
        fileExtension = makeCorrectCaseSensitive(fileExtension,
                                                 uni.MySettings["validSentenceStructureForFileExtension"])
    return fileExtension


def replaceList(_s, _chars, _newChars):
    for a, b in zip(_chars, _newChars):
        _s = _s.replace(a, b)
    return _s


def makeCorrectCaseSensitive(_inputString, _cbCharacterType):
    _inputString = uni.trUnicode(_inputString)
    if _cbCharacterType == uni.validSentenceStructureKeys[0]:
        if uni.isPython3k:
            return str(_inputString).title()
        else:
            s = []
            prevIsCased = False
            prevC = ""
            for c in _inputString:
                if c.islower():
                    if not prevIsCased and prevC not in ("'", "`"):
                        c = c.upper()
                    prevIsCased = True
                elif c.isupper():
                    if prevIsCased:
                        c = c.lower()
                    prevIsCased = True
                else:
                    prevIsCased = False
                prevC = c
                s.append(c)
            return ''.join(s)
            #return string.capwords(uni.trUnicode(_inputString)) #don't use this. Because; it clears whitespaces, it doesn't upper the letters whick is after ()[]-/*......
    elif _cbCharacterType == uni.validSentenceStructureKeys[1]:
        if uni.isPython3k:
            return str(_inputString).lower()
        else:
            return string.lower(_inputString)
    elif _cbCharacterType == uni.validSentenceStructureKeys[2]:
        if uni.isPython3k:
            return str(_inputString).upper()
        else:
            return string.upper(_inputString)
    elif _cbCharacterType == uni.validSentenceStructureKeys[3]:
        if uni.isPython3k:
            return str(_inputString).capitalize()
        else:
            return string.capitalize(_inputString)
    else:
        return str(_inputString)


def getLink(_stringPath):
    _stringPath = str(_stringPath)
    if uni.isWindows:
        return "<a href=\"%s\" target=\"_blank\">%s</a>" % (_stringPath, _stringPath)
    return "<a href=\"file://%s\" target=\"_blank\">%s</a>" % (_stringPath, _stringPath)


def getCorrectedFileSize(_bytes, _precision=2):
    _bytes = int(_bytes)
    if _bytes is 0:
        return '0 B'
    log = math.floor(math.log(_bytes, 1024))
    return "%.*f %s" % (_precision, _bytes / math.pow(1024, log),
                        ['B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB'][int(log)])


def getCorrectedTime(_timeValue):
    return str(time.strftime("%d.%m.%Y %H:%M:%S", time.localtime(_timeValue)))


def getIconName(_artist, _album, _year, _genre):
    iconName = uni.MySettings["iconNameFormat"]
    iconName = iconName.replace(uni.iconNameFormatKeys[0], _artist)
    iconName = iconName.replace(uni.iconNameFormatKeys[1], _album)
    iconName = iconName.replace(uni.iconNameFormatKeys[2], _year)
    iconName = iconName.replace(uni.iconNameFormatKeys[3], _genre)
    return iconName + "." + uni.MySettings["iconFileType"]


def searchAndReplaceFromSearchAndReplaceTable(_oldString):
    import Databases

    newString = _oldString
    for info in Databases.SearchAndReplaceTable.fetchAll():
        if info[4] == 1:
            isCaseInsensitive, isRegExp = False, False
            if info[5] == 1:
                isCaseInsensitive = True
            if info[6] == 1:
                isRegExp = True
            newString = searchAndReplace(newString, [info[2]], [info[3]], isCaseInsensitive, isRegExp)
    return newString


def searchAndReplace(_oldString, _searchStrings, _replaceStrings, _isCaseInsensitive=True, _isRegExp=False):
    newString = uni.trUnicode(_oldString)
    for filterNo in range(0, len(_searchStrings)):
        if _searchStrings[filterNo] != "":
            if _isRegExp:
                if _isCaseInsensitive:
                    pattern = re.compile(uni.trUnicode(_searchStrings[filterNo]), re.I | re.U)
                    newString = re.sub(pattern, uni.trUnicode(_replaceStrings[filterNo]), newString)
                else:
                    pattern = re.compile(uni.trUnicode(_searchStrings[filterNo]))
                    newString = re.sub(pattern, uni.trUnicode(_replaceStrings[filterNo]), newString)
            else:
                if _isCaseInsensitive:
                    pattern = re.compile(re.escape(uni.trUnicode(_searchStrings[filterNo])), re.I | re.U)
                    newString = re.sub(pattern, uni.trUnicode(_replaceStrings[filterNo]), newString)
                else:
                    newString = newString.replace(_searchStrings[filterNo], _replaceStrings[filterNo])
    return newString


def clear(_cbClearType, _oldString="", _searchString="", _isCaseInsensitive=True, _isRegExp=False):
    _oldString = uni.trUnicode(_oldString)
    _searchString = uni.trUnicode(_searchString)
    myString = ""
    if _cbClearType == translate("SpecialTools", "All"):
        myString = ""
    elif _cbClearType == translate("SpecialTools", "Letters"):
        for char in _oldString:
            if char.isalpha() is False:
                myString += char
    elif _cbClearType == translate("SpecialTools", "Numbers"):
        for char in _oldString:
            if char.isdigit() is False:
                myString += char
    elif _cbClearType == translate("SpecialTools", "Other Characters"):
        for char in _oldString:
            if char.isdigit() or char.isalpha():
                myString += char
    elif _cbClearType == translate("SpecialTools", "Selected Text"):
        if _isRegExp:
            if _isCaseInsensitive:
                pattern = re.compile(_searchString, re.I | re.U)
                myString = re.sub(pattern, uni.trUnicode(""), _oldString)
            else:
                pattern = re.compile(_searchString)
                myString = re.sub(pattern, uni.trUnicode(""), _oldString)
        else:
            if _isCaseInsensitive:
                pattern = re.compile(re.escape(_searchString), re.I | re.U)
                myString = re.sub(pattern, uni.trUnicode(""), _oldString)
            else:
                myString = _oldString.replace(_searchString, "")
    return myString


def correctCaseSensitive(_inputString, _cbCharacterType, isCorrectText=False, _searchStrings=[],
                         _isCaseInsensitive=True, _isRegExp=False):
    newString = uni.trUnicode(_inputString)
    if isCorrectText:
        for filterNo in range(0, len(_searchStrings)):
            if _searchStrings[filterNo] != "":
                if _isRegExp:
                    if _isCaseInsensitive:
                        m = re.search(_searchStrings[filterNo], newString, re.I | re.U)
                        try: a = m.group(0)
                        except: return newString
                        pattern = re.compile(uni.trUnicode(_searchStrings[filterNo]), re.I | re.U)
                        newString = re.sub(pattern,
                                           uni.trUnicode(makeCorrectCaseSensitive(m.group(0), _cbCharacterType)),
                                           newString)
                    else:
                        m = re.search(_searchStrings[filterNo], newString)
                        try: a = m.group(0)
                        except: return newString
                        pattern = re.compile(uni.trUnicode(_searchStrings[filterNo]))
                        newString = re.sub(pattern,
                                           uni.trUnicode(makeCorrectCaseSensitive(m.group(0), _cbCharacterType)),
                                           newString)
                else:
                    if _isCaseInsensitive:
                        pattern = re.compile(re.escape(uni.trUnicode(_searchStrings[filterNo])), re.I | re.U)
                        newString = re.sub(pattern, uni.trUnicode(
                            makeCorrectCaseSensitive(_searchStrings[filterNo], _cbCharacterType)),
                                           newString)
                    else:
                        newString = newString.replace(_searchStrings[filterNo],
                                                      makeCorrectCaseSensitive(_searchStrings[filterNo],
                                                                               _cbCharacterType))
    else:
        newString = makeCorrectCaseSensitive(_inputString, _cbCharacterType)
    return newString

    
