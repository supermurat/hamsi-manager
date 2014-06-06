## This file is part of HamsiManager.
## 
## Copyright (c) 2010 - 2013 Murat Demir <mopened@gmail.com>      
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

import time
import unicodedata
import string
import math
import re
from Core.MyObjects import *
from Core import Variables
from Core import Universals
import InputOutputs
if Variables.isPython3k:
    from urllib.parse import unquote, quote
else:
    from urllib import unquote, quote

class Organizer:
    """Music tags, filenames, Turkish characters etc. will be arranged through this class
    """
    global emend, makeCorrectCaseSensitive, searchAndReplace, clear, correctCaseSensitive, searchAndReplaceFromSearchAndReplaceTable, getLink, getIconName, getCorrectedFileSize, getCorrectedTime, emendBaseName, emendFileExtension, replaceList
    
    def emend(_inputString, _type="text", _isCorrectCaseSensitive=True, _isRichText=False):
        _inputString = str(_inputString)
        if len(_inputString)==0: return ""
        if Universals.getBoolValue("isClearFirstAndLastSpaceChars"):
            _inputString = _inputString.strip()
        if len(_inputString)==0: return ""
        if Universals.getBoolValue("isEmendIncorrectChars"):
            replacementChars = Universals.getUtf8Data("replacementChars")
            try:_inputString = Universals.trUnicode(_inputString)
            except:_inputString = Universals.trUnicode(_inputString, "iso-8859-9")
            _inputString = replaceList(_inputString, 
                                   replacementChars.keys(), 
                                   replacementChars.values())
        if Universals.getBoolValue("isDecodeURLStrings"):
            _inputString = unquote(_inputString)
        _inputString = str(Universals.trDecode(_inputString, "utf-8", "ignore"))
        if _type=="file" or _type=="directory":
            _inputString = InputOutputs.getAvailableNameByName(_inputString)
            preString, extString, ext2String = "", "", ""
            if _inputString[-1]==InputOutputs.sep:
                _inputString = _inputString[:-1]
                ext2String = InputOutputs.sep
            if _inputString.find(InputOutputs.sep)!=-1:
                tStr = _inputString.rsplit(InputOutputs.sep, 1)
                for ps in tStr[0].split(InputOutputs.sep):
                    if Universals.getBoolValue("isCorrectFileNameWithSearchAndReplaceTable"):
                        ps = searchAndReplaceFromSearchAndReplaceTable(ps)
                    preString += emendBaseName(ps, "directory", _isCorrectCaseSensitive) + InputOutputs.sep
                _inputString = tStr[1]
            if _type=="file":
                _inputString, extString = InputOutputs.getFileNameParts(_inputString)
            if Universals.getBoolValue("isCorrectFileNameWithSearchAndReplaceTable"):
                _inputString = searchAndReplaceFromSearchAndReplaceTable(_inputString)
            _inputString = emendBaseName(_inputString, _type, _isCorrectCaseSensitive)
            extString = emendFileExtension(extString, _isCorrectCaseSensitive)
            if extString!="": 
                extString = "." + extString
            if preString!="":
                _inputString = InputOutputs.joinPath(preString, _inputString)
            _inputString = str(Universals.trDecode(_inputString, "utf-8", "ignore")) + str(Universals.trDecode(extString, "utf-8", "ignore")) + str(Universals.trDecode(ext2String, "utf-8", "ignore"))
        else:
            if Universals.getBoolValue("isCorrectValueWithSearchAndReplaceTable"):
                _inputString = searchAndReplaceFromSearchAndReplaceTable(_inputString)
            if _isCorrectCaseSensitive:
                _inputString = makeCorrectCaseSensitive(_inputString, Universals.MySettings["validSentenceStructure"])
        if _isRichText==False:
            if Universals.getBoolValue("isCorrectDoubleSpaceChars"):
                isFinded=_inputString.find("  ")
                while isFinded!=-1:
                    _inputString=_inputString.replace("  "," ")
                    isFinded=_inputString.find("  ")
        return _inputString
        
    def emendBaseName(_baseName, _type, _isCorrectCaseSensitive):
        baseName = _baseName
        if _isCorrectCaseSensitive:
            if _type=="file": 
                baseName = makeCorrectCaseSensitive(baseName, Universals.MySettings["validSentenceStructureForFile"])
            elif _type=="directory": 
                baseName = makeCorrectCaseSensitive(baseName, Universals.MySettings["validSentenceStructureForDirectory"])
        if Universals.MySettings["fileReNamerType"]==Variables.fileReNamerTypeNamesKeys[1] or Universals.MySettings["fileReNamerType"]==Variables.fileReNamerTypeNamesKeys[2]:
            baseName = ''.join(c for c in unicodedata.normalize('NFKD', Universals.trUnicode(baseName)) if unicodedata.category(c) != 'Mn')
            baseName = str(Universals.trEncode(baseName, "utf-8", "ignore")).replace(Universals.getUtf8Data("little+I"), "i")
        if Universals.MySettings["fileReNamerType"]==Variables.fileReNamerTypeNamesKeys[1]:
            baseName = replaceList(baseName, 
                                   [" "], 
                                   ["_"])
        if Universals.MySettings["fileReNamerType"]==Variables.fileReNamerTypeNamesKeys[1]:
            baseName = quote(baseName)
        return baseName
        
    def emendFileExtension(_fileExtension, _isCorrectCaseSensitive):
        fileExtension = _fileExtension
        if _isCorrectCaseSensitive:
            fileExtension = makeCorrectCaseSensitive(fileExtension, Universals.MySettings["validSentenceStructureForFileExtension"])
        return fileExtension
        
    def replaceList(_s, _chars, _newChars):
        for a, b in zip(_chars, _newChars):
            _s = _s.replace(a, b)
        return _s

    def makeCorrectCaseSensitive(_inputString, _cbCharacterType):
        if _cbCharacterType==Variables.validSentenceStructureKeys[0]:
            if Variables.isPython3k:
                return str(Universals.trUnicode(_inputString)).title()
            else:
                s = []
                prevIsCased = False
                prevC = ""
                for c in Universals.trUnicode(_inputString):
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
                #return string.capwords(Universals.trUnicode(_inputString)) #don't use this. Because; it clears whitespaces, it doesn't upper the letters whick is after ()[]-/*......
        elif _cbCharacterType==Variables.validSentenceStructureKeys[1]:
            if Variables.isPython3k:
                return str(Universals.trUnicode(_inputString)).lower()
            else:
                return string.lower(Universals.trUnicode(_inputString))
        elif _cbCharacterType==Variables.validSentenceStructureKeys[2]:
            if Variables.isPython3k:
                return str(Universals.trUnicode(_inputString)).upper()
            else:
                return string.upper(Universals.trUnicode(_inputString))
        elif _cbCharacterType==Variables.validSentenceStructureKeys[3]:
            if Variables.isPython3k:
                return str(Universals.trUnicode(_inputString)).capitalize()
            else:
                return string.capitalize(Universals.trUnicode(_inputString))
        else :
            return str(Universals.trUnicode(_inputString))
    
    def getLink(_stringPath):
        _stringPath = str(_stringPath)
        if Variables.isWindows:
            return "<a href=\"%s\" target=\"_blank\">%s</a>" % (_stringPath, _stringPath)
        return "<a href=\"file://%s\" target=\"_blank\">%s</a>" % (_stringPath, _stringPath)
    
    def getCorrectedFileSize(bytes, precision=2):
        bytes = int(bytes)
        if bytes is 0:
            return '0 byte'
        log = math.floor(math.log(bytes, 1024))
        return "%.*f %s" % (precision, 
                           bytes / math.pow(1024, log),
                           ['bytes', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB']
                           [int(log)])
                           
    def getCorrectedTime(_timeValue):
        return str(time.strftime("%d.%m.%Y %H:%M:%S", time.localtime(_timeValue)))
        
    def getIconName(_artist, _album, _year, _genre):
        iconName = Universals.MySettings["iconNameFormat"]
        iconName = iconName.replace(Variables.iconNameFormatKeys[0], _artist)
        iconName = iconName.replace(Variables.iconNameFormatKeys[1], _album)
        iconName = iconName.replace(Variables.iconNameFormatKeys[2], _year)
        iconName = iconName.replace(Variables.iconNameFormatKeys[3], _genre)
        return iconName + "." + Universals.MySettings["iconFileType"]

    def searchAndReplaceFromSearchAndReplaceTable(_oldString):
        import Databases
        newString = _oldString
        for info in Databases.SearchAndReplaceTable.fetchAll():
            if info[4]==1:
                isCaseInsensitive, isRegExp = False, False
                if info[5]==1:
                    isCaseInsensitive = True
                if info[6]==1:
                    isRegExp = True
                newString = searchAndReplace(newString, [info[2]], [info[3]], isCaseInsensitive, isRegExp)
        return newString
        
    def searchAndReplace(_oldString, _searchStrings, _replaceStrings, _isCaseInsensitive=True, _isRegExp=False):
        newString = _oldString
        for filterNo in range(0,len(_searchStrings)):
            if _searchStrings[filterNo]!="":
                if _isRegExp == True:
                    if _isCaseInsensitive ==True:
                        pattern = re.compile(Universals.trUnicode(_searchStrings[filterNo]), re.I | re.U)
                        newString = re.sub(pattern,Universals.trUnicode(_replaceStrings[filterNo]), Universals.trUnicode(newString))
                    else:
                        pattern = re.compile(Universals.trUnicode(_searchStrings[filterNo]))
                        newString = re.sub(pattern,Universals.trUnicode(_replaceStrings[filterNo]), Universals.trUnicode(newString))
                else:
                    if _isCaseInsensitive ==True:
                        pattern = re.compile(re.escape(Universals.trUnicode(_searchStrings[filterNo])), re.I | re.U)
                        newString = re.sub(pattern,Universals.trUnicode(_replaceStrings[filterNo]), Universals.trUnicode(newString))
                    else:
                        newString = newString.replace(_searchStrings[filterNo],_replaceStrings[filterNo])
        return newString
    
    def clear(_cbClearType, _oldString="", _searchString="", _isCaseInsensitive=True, _isRegExp=False):
        myString=""
        if _cbClearType==translate("SpecialTools", "All"):
            myString=""
        elif _cbClearType==translate("SpecialTools", "Letters"):
            for char in _oldString:
                if char.isalpha()==False:
                    myString+=char
        elif _cbClearType==translate("SpecialTools", "Numbers"):
            for char in _oldString:
                if char.isdigit()==False:
                    myString+=char
        elif _cbClearType==translate("SpecialTools", "Other Characters"):
            for char in _oldString:
                if char.isdigit()==True or char.isalpha()==True:
                    myString+=char
        elif _cbClearType==translate("SpecialTools", "Selected Text"):
            if _isRegExp == True:
                if _isCaseInsensitive ==True:
                    pattern = re.compile(Universals.trUnicode(_searchString), re.I | re.U)
                    myString = re.sub(pattern,Universals.trUnicode(""), Universals.trUnicode(_oldString))
                else:
                    pattern = re.compile(Universals.trUnicode(_searchString))
                    myString = re.sub(pattern,Universals.trUnicode(""), Universals.trUnicode(_oldString))
            else:
                if _isCaseInsensitive==True:
                    pattern = re.compile(re.escape(Universals.trUnicode(_searchString)), re.I | re.U)
                    myString = re.sub(pattern,Universals.trUnicode(""), Universals.trUnicode(_oldString))
                else:
                    myString = _oldString.replace(_searchString,"")
        return myString
     
    def correctCaseSensitive(_inputString, _cbCharacterType, isCorrectText = False, _searchStrings=[], _isCaseInsensitive=True, _isRegExp=False):
        newString = _inputString
        if isCorrectText:
            for filterNo in range(0,len(_searchStrings)):
                if _searchStrings[filterNo]!="":
                    if _isRegExp == True:
                        if _isCaseInsensitive ==True:
                            m = re.search(_searchStrings[filterNo], newString, re.I | re.U)
                            try:a = m.group(0)
                            except:return newString
                            pattern = re.compile(Universals.trUnicode(_searchStrings[filterNo]), re.I | re.U)
                            newString = re.sub(pattern,Universals.trUnicode(makeCorrectCaseSensitive(m.group(0), _cbCharacterType)), Universals.trUnicode(newString))
                        else:
                            m = re.search(_searchStrings[filterNo], newString)
                            try:a = m.group(0)
                            except:return newString
                            pattern = re.compile(Universals.trUnicode(_searchStrings[filterNo]))
                            newString = re.sub(pattern,Universals.trUnicode(makeCorrectCaseSensitive(m.group(0), _cbCharacterType)), Universals.trUnicode(newString))
                    else:
                        if _isCaseInsensitive ==True:
                            pattern = re.compile(re.escape(Universals.trUnicode(_searchStrings[filterNo])), re.I | re.U)
                            newString = re.sub(pattern,Universals.trUnicode(makeCorrectCaseSensitive(_searchStrings[filterNo], _cbCharacterType)), Universals.trUnicode(newString))
                        else:
                            newString = newString.replace(_searchStrings[filterNo],makeCorrectCaseSensitive(_searchStrings[filterNo], _cbCharacterType))
        else:
            newString = makeCorrectCaseSensitive(_inputString, _cbCharacterType)
        return newString
        
    
