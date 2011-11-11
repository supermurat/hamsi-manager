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

import time
import unicodedata
import string
import math
from Core import Variables
from Core import Universals
if Variables.isPython3k:
    from urllib.parse import unquote, quote
else:
    from urllib import unquote, quote

class Organizer:
    """Music tags, filenames, Turkish characters etc. will be arranged through this class
    """
    global applySpecialCommand, emend, whatDoesSpecialCommandDo,searchAndReplaceTable, fillTable, clearTable, makeCorrectCaseSensitive, correctCaseSensitiveTable, searchAndReplace, clear, correctCaseSensitive, searchAndReplaceFromSearchAndReplaceTable, getLink, getIconName, getCorrectedFileSize, getCorrectedTime, getFileNameParts, emendBaseName, emendFileExtension
    
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
            _inputString = unquote(_inputString)
            for oldChar, newChar in replacementChars.items():
                _inputString = _inputString.replace(oldChar,newChar)
        _inputString = str(Universals.trDecode(_inputString, "utf-8", "ignore"))
        if _type=="file" or _type=="directory":
            if Universals.getBoolValue("isCorrectFileNameWithSearchAndReplaceTable"):
                _inputString = searchAndReplaceFromSearchAndReplaceTable(_inputString)
            preString, extString, ext2String = "", "", ""
            if _inputString[-1]=="/":
                _inputString = _inputString[:-1]
                ext2String = "/"
            if _inputString.find("/")!=-1:
                tStr = _inputString.rsplit("/", 1)
                for ps in tStr[0].split("/"):
                    preString += emendBaseName(ps, "directory", _isCorrectCaseSensitive) + "/"
                _inputString = tStr[1]
            if _type=="file":
                _inputString, extString = getFileNameParts(_inputString)
            _inputString = emendBaseName(_inputString, _type, _isCorrectCaseSensitive)
            extString = emendFileExtension(extString, _isCorrectCaseSensitive)
            if extString!="": extString = "." + extString
            _inputString = preString + _inputString
            _inputString = str(Universals.trDecode(_inputString, "utf-8", "ignore")) + str(Universals.trDecode(extString, "utf-8", "ignore")) + str(Universals.trDecode(ext2String, "utf-8", "ignore"))
        else:
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
        oldChars, newChars = [], []
        if Universals.MySettings["fileReNamerType"]==Variables.fileReNamerTypeNamesKeys[1]:
            oldChars = [" "]
            newChars = ["_"]
        for x, oldChar in enumerate(oldChars):
            baseName = baseName.replace(oldChar,newChars[x])
        if Universals.MySettings["fileReNamerType"]==Variables.fileReNamerTypeNamesKeys[1]:
            baseName = quote(baseName)
        return baseName
        
    def emendFileExtension(_fileExtension, _isCorrectCaseSensitive):
        fileExtension = _fileExtension
        if _isCorrectCaseSensitive:
            fileExtension = makeCorrectCaseSensitive(fileExtension, Universals.MySettings["validSentenceStructureForFileExtension"])
        return fileExtension
    
    def getFileNameParts(_fileName):
        _fileName = str(_fileName)
        fileName, fileExtension = "", ""
        if _fileName.find(".")!=-1:
            fParts = [_fileName, fileExtension]
            if Universals.MySettings["fileExtesionIs"]==Variables.fileExtesionIsKeys[0]:
                fParts = _fileName.split(".", 1)
            elif Universals.MySettings["fileExtesionIs"]==Variables.fileExtesionIsKeys[1]:
                fParts = _fileName.rsplit(".", 1)
            fileName = fParts[0]
            fileExtension = fParts[1]
        else:
            fileName = _fileName
        return fileName, fileExtension.lower()
    
    def makeCorrectCaseSensitive(_inputString, _cbCharacterType):
        if _cbCharacterType==Variables.validSentenceStructureKeys[0]:
            if Variables.isPython3k:
                return str(Universals.trUnicode(_inputString)).title()
            else:
                return string.capwords(Universals.trUnicode(_inputString))
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
            if info[3]==1:
                isCaseInsensitive, isRegExp = False, False
                if info[4]==1:
                    isCaseInsensitive = True
                if info[5]==1:
                    isRegExp = True
                newString = searchAndReplace(newString, [info[1]], [info[2]], isCaseInsensitive, isRegExp)
        return newString
    
    def applySpecialCommand(_splitPointer, _whereIsSplitPointer, _command, _SpecialTools):
        from Core.MyObjects import trForUI
        import Tables
        blok = _command.split(",")
        changings = blok[0].split(_splitPointer)
        changers = blok[1].split(_splitPointer)
        changingColumns,changerColumns=[],[]
        Tables.isChangeHiddenColumn,Tables.isAskShowHiddenColumn=True,True
        for columnName in changings:
            columnName=columnName.strip()
            for no,column in enumerate(Universals.MainWindow.Table.tableColumnsKey):
                if columnName==column:
                    if Tables.checkHiddenColumn(no)==False:
                        return False
                    changingColumns.append(no)
        if len(changingColumns)==0:
            return False
        for columnName in changers:
            columnName=columnName.strip()
            for no,column in enumerate(Universals.MainWindow.Table.tableColumnsKey):
                if columnName==column:
                    if Tables.checkHiddenColumn(no)==False:
                        return False
                    changerColumns.append(no)
        if len(changerColumns)==0:
            return False
        if Tables.isChangeHiddenColumn==True:
            if _whereIsSplitPointer=="right":
                for rowNo in range(Universals.MainWindow.Table.rowCount()):
                    if Universals.MainWindow.Table.isChangableItem(rowNo, changingColumns[0]):
                        newString=""
                        for changerColumnNo in changerColumns:
                            if str(Universals.MainWindow.Table.item(rowNo,changerColumnNo).text()) != "-----":
                                newString+=" "+_splitPointer+" "+str(Universals.MainWindow.Table.item(rowNo,changerColumnNo).text())
                        newString = emend(newString[2:])
                        if newString!="":
                            for uzanti in Universals.getListFromStrint(Universals.MySettings["musicExtensions"]):
                                if newString.split(".")[-1].lower() == str(uzanti) :
                                    newString = newString[:-len(newString.split(".")[-1])-1]
                            if _SpecialTools.btChange.isChecked()==True:
                                pass
                            elif _SpecialTools.tbAddToBefore.isChecked()==True:
                                newString += str(Universals.MainWindow.Table.item(rowNo,changingColumns[0]).text())
                            elif _SpecialTools.tbAddToAfter.isChecked()==True:
                                newString = str(Universals.MainWindow.Table.item(rowNo,changingColumns[0]).text()) + newString
                            Universals.MainWindow.Table.item(rowNo,changingColumns[0]).setText(trForUI(newString.strip()))
            else:
                for rowNo in range(Universals.MainWindow.Table.rowCount()):
                    newString = str(Universals.MainWindow.Table.item(rowNo,changerColumns[0]).text())
                    if newString!="-----":
                        for uzanti in Universals.getListFromStrint(Universals.MySettings["musicExtensions"]):
                            if newString.split(".")[-1].lower() == str(uzanti) :
                                newString = newString[:-len(newString.split(".")[-1])-1]
                        newStrings = ["","","","","","","",""]
                        newString = newString.split(_splitPointer)
                        for stringNo in range(0,len(newString)):
                            newStrings[stringNo] = newString[stringNo]
                        stringNo=0
                        for changingColumnNo in changingColumns:
                            if Universals.MainWindow.Table.isChangableItem(rowNo, changingColumnNo):
                                if _SpecialTools.btChange.isChecked()==True:
                                    pass
                                elif _SpecialTools.tbAddToBefore.isChecked()==True:
                                    newStrings[stringNo] += str(Universals.MainWindow.Table.item(rowNo,changingColumnNo).text())
                                elif _SpecialTools.tbAddToAfter.isChecked()==True:
                                    newStrings[stringNo] = str(Universals.MainWindow.Table.item(rowNo,changingColumnNo).text()) + newStrings[stringNo]
                                Universals.MainWindow.Table.item(rowNo,changingColumnNo).setText(trForUI(newStrings[stringNo].strip()))
                            stringNo+=1
        
    def whatDoesSpecialCommandDo(_splitPointer, _whereIsSplitPointer, _command, _isCorrect=False, _isReturnDetails=False):
        from Core import Dialogs
        from Core.MyObjects import trForUI, translate
        if _command[-2:]!="- " and _command[-2:]!=", " and _command.find(",")!=-1:
            _command = _command.split(",")
            changings = _command[0].split(_splitPointer)
            changers = _command[1].split(_splitPointer)
            if _whereIsSplitPointer=="right":
                details=""
                for changerColumnName in changers:
                    if len(changers)>1:
                        if changerColumnName==changers[-2]:
                            appended= str(translate("Organizer", " and "))
                        elif changerColumnName==changers[-1]:
                            appended=""
                        else:
                            appended=","
                    else:
                        appended = ""
                    details+=str(Universals.MainWindow.Table.getColumnNameFromKey(changerColumnName.strip()))+appended
                details+=str(translate("Organizer", " \"%s\" is concatenated with and is set as \"%s\".")) % (_splitPointer, str(Universals.MainWindow.Table.getColumnNameFromKey(changings[0].strip()))) 
                if len(changers)==1:
                    details = str(translate("Organizer", "\"%s\" \"%s\" are set.")) % (str(Universals.MainWindow.Table.getColumnNameFromKey(changers[0].strip())), str(Universals.MainWindow.Table.getColumnNameFromKey(changings[0].strip())))
                if _isCorrect==True:
                    return True
                if _isReturnDetails==True:
                    return details
                Dialogs.show(translate("Organizer", "What Does This Command Do?"),trForUI(details))
                
            else:
                details = ""
                for changingColumnName in changings:
                    if len(changings)>1:
                        if changingColumnName==changings[-2]:
                            appended=str(translate("Organizer", " and "))
                        elif changingColumnName==changings[-1]:
                            appended=""
                        else:
                            appended=","
                    else:
                        appended = ""
                    details+= str(Universals.MainWindow.Table.getColumnNameFromKey(changingColumnName.strip()))+appended
                details = str(translate("Organizer", "\"%s\" \"%s\" hyphenates from the apostrophe and sets each piece as \"%s\".")) % (str(Universals.MainWindow.Table.getColumnNameFromKey(changers[0].strip())), _splitPointer, details)
                if _isCorrect==True:
                    return True
                if _isReturnDetails==True:
                    return details
                Dialogs.show(translate("Organizer", "What Does This Command Do?"),details)
        else:
            if _command.find(",")==-1:
                if _isReturnDetails==True:
                    return (translate("Organizer", "You have to add a \",\"(comma) to your command!.."))
                Dialogs.showError(translate("Organizer", "Missing Command"),
                             translate("Organizer", "You have to add a \",\"(comma) to your command!.."))
                return False
            else:
                if _isReturnDetails==True:
                    return (translate("Organizer", "You have to add one (more) \"Column\"!.."))
                Dialogs.showError(translate("Organizer", "Missing Command"),
                             translate("Organizer", "You have to add one (more) \"Column\"!.."))
                return False
    
    def searchAndReplaceTable(_searchStrings,_replaceStrings, _SpecialTools):
        from Core.MyObjects import trForUI
        searchStrings=_searchStrings.split(";")
        replaceStrings=_replaceStrings.split(";")
        for filterNo in range(0,len(searchStrings)):
            if _SpecialTools.btChange.isChecked()==True:
                pass
            elif _SpecialTools.tbAddToBefore.isChecked()==True:
                replaceStrings[filterNo] += searchStrings[filterNo]
            elif _SpecialTools.tbAddToAfter.isChecked()==True:
                replaceStrings[filterNo] = searchStrings[filterNo] + replaceStrings[filterNo]
        while len(replaceStrings)!=len(searchStrings):
            replaceStrings.append("")
        if _SpecialTools.searchAndReplace.columns.currentIndex()==0:
            columns = list(range(0,Universals.MainWindow.Table.columnCount()))
        else:
            columns = [_SpecialTools.searchAndReplace.columns.currentIndex()-1]
        for columnNo in columns:
            if Universals.MainWindow.Table.isColumnHidden(columnNo)==True:
                continue
            for rowNo in range(Universals.MainWindow.Table.rowCount()):
                if Universals.MainWindow.Table.isChangableItem(rowNo, columnNo, None, True):
                    newString = str(Universals.MainWindow.Table.item(rowNo,columnNo).text())
                    newString = trForUI(newString)
                    myString = ""
                    informationSectionX = _SpecialTools.cbInformationSectionX.value()
                    informationSectionY = _SpecialTools.cbInformationSectionY.value()
                    isCaseInsensitive = _SpecialTools.searchAndReplace.cckbCaseInsensitive.isChecked()
                    isRegExp = _SpecialTools.searchAndReplace.cckbRegExp.isChecked()
                    if _SpecialTools.cbInformationSection.currentIndex()==0:
                        myString = searchAndReplace(newString, searchStrings, 
                                               replaceStrings, isCaseInsensitive, isRegExp)
                    elif _SpecialTools.cbInformationSection.currentIndex()==1:
                        myString = searchAndReplace(newString[:informationSectionX], searchStrings, 
                                               replaceStrings, isCaseInsensitive, isRegExp)
                        myString += newString[informationSectionX:]
                    elif _SpecialTools.cbInformationSection.currentIndex()==2:
                        myString = newString[:informationSectionX]
                        myString += searchAndReplace(newString[informationSectionX:], searchStrings, 
                                                replaceStrings, isCaseInsensitive, isRegExp)
                    elif _SpecialTools.cbInformationSection.currentIndex()==3:
                        myString = searchAndReplace(newString[:-informationSectionX], searchStrings, 
                                               replaceStrings, isCaseInsensitive, isRegExp)
                        myString += newString[-informationSectionX:]
                    elif _SpecialTools.cbInformationSection.currentIndex()==4:
                        myString = newString[:-informationSectionX]
                        myString += searchAndReplace(newString[-informationSectionX:], searchStrings, 
                                                replaceStrings, isCaseInsensitive, isRegExp)
                    elif _SpecialTools.cbInformationSection.currentIndex()==5:
                        myString = newString[:informationSectionX]
                        myString += searchAndReplace(newString[informationSectionX:informationSectionY], searchStrings, 
                                                replaceStrings, isCaseInsensitive, isRegExp)
                        myString += newString[informationSectionY:]
                    elif _SpecialTools.cbInformationSection.currentIndex()==6:
                        myString = searchAndReplace(newString[:informationSectionX], searchStrings, 
                                                replaceStrings, isCaseInsensitive, isRegExp)
                        myString += newString[informationSectionX:informationSectionY]
                        myString += searchAndReplace(newString[informationSectionY:], searchStrings, 
                                                replaceStrings, isCaseInsensitive, isRegExp)
                    Universals.MainWindow.Table.item(rowNo,columnNo).setText(trForUI(myString))
    
    def searchAndReplace(_oldString, _searchStrings, _replaceStrings, _isCaseInsensitive=True, _isRegExp=False):
        newString = _oldString
        for filterNo in range(0,len(_searchStrings)):
            if _searchStrings[filterNo]!="":
                if _isRegExp == True:
                    import re
                    if _isCaseInsensitive ==True:
                        pattern = re.compile(Universals.trUnicode(_searchStrings[filterNo]), re.I | re.U)
                        newString = re.sub(pattern,Universals.trUnicode(_replaceStrings[filterNo]), Universals.trUnicode(newString))
                    else:
                        pattern = re.compile(Universals.trUnicode(_searchStrings[filterNo]))
                        newString = re.sub(pattern,Universals.trUnicode(_replaceStrings[filterNo]), Universals.trUnicode(newString))
                else:
                    if _isCaseInsensitive ==True:
                        import re
                        pattern = re.compile(re.escape(Universals.trUnicode(_searchStrings[filterNo])), re.I | re.U)
                        newString = re.sub(pattern,Universals.trUnicode(_replaceStrings[filterNo]), Universals.trUnicode(newString))
                    else:
                        newString = newString.replace(_searchStrings[filterNo],_replaceStrings[filterNo])
        return newString
    
    def fillTable(_columnName, _SpecialTools,_newString=""):
        from Core.MyObjects import trForUI
        import Tables
        Tables.isChangeHiddenColumn,Tables.isAskShowHiddenColumn=True,True
        for No, columnName in enumerate(Universals.MainWindow.Table.tableColumns):
            if str(_columnName) == str(columnName):
                columnNo=No
                break
        if Tables.checkHiddenColumn(columnNo,False)==False:
            return False
        if Tables.isChangeHiddenColumn==True:
            if _SpecialTools.fill.cbFillType.currentIndex()==1:
                _newString = int(_SpecialTools.fill.spStartDigit.value())-1
            for rowNo in range(Universals.MainWindow.Table.rowCount()):
                if Universals.MainWindow.Table.isChangableItem(rowNo, columnNo):
                    if _SpecialTools.fill.cbFillType.currentIndex()==1:
                        if _SpecialTools.fill.cbSort.currentIndex()==0:
                            _newString+=1
                        else:
                            _newString-=1
                        myString = str(_newString)
                        inNegative = False
                        if myString.find("-")!=-1:
                            myString = myString.replace("-", "")
                            inNegative = True
                        karakterSayisi = len(myString)
                        while karakterSayisi < int(_SpecialTools.fill.spCharNumberOfDigit.value()):
                            myString="0"+myString
                            karakterSayisi = len(myString)
                        if inNegative:
                            myString="-"+myString
                    else:
                        myString = str(_newString)
                    if _SpecialTools.btChange.isChecked()==True:
                        pass
                    elif _SpecialTools.tbAddToBefore.isChecked()==True:
                        myString += str(Universals.MainWindow.Table.item(rowNo,columnNo).text())
                    elif _SpecialTools.tbAddToAfter.isChecked()==True:
                        myString = str(Universals.MainWindow.Table.item(rowNo,columnNo).text()) + myString
                    Universals.MainWindow.Table.item(rowNo,columnNo).setText(trForUI(Universals.trUnicode(myString).title()))
                    
    def clearTable(_SpecialTools):
        from Core.MyObjects import trForUI
        import Tables
        Tables.isChangeHiddenColumn,Tables.isAskShowHiddenColumn=True,True
        if _SpecialTools.clear.columns.currentIndex()==0:
            columns = list(range(0,Universals.MainWindow.Table.columnCount()))
        else:
            columns = [_SpecialTools.clear.columns.currentIndex()-1]
        for columnNo in columns:
            if Tables.checkHiddenColumn(columnNo,False)==False:
                continue
            for rowNo in range(Universals.MainWindow.Table.rowCount()):
                if Universals.MainWindow.Table.isChangableItem(rowNo, columnNo):
                    newString = str(Universals.MainWindow.Table.item(rowNo,columnNo).text())
                    newString = Universals.trDecode(newString, "utf-8")
                    informationSectionX = _SpecialTools.cbInformationSectionX.value()
                    informationSectionY = _SpecialTools.cbInformationSectionY.value()
                    isCaseInsensitive = _SpecialTools.clear.cckbCaseInsensitive.isChecked()
                    oldString = str(_SpecialTools.clear.leClear.text())
                    cbClearType = _SpecialTools.clear.cbClearType.currentText()
                    isRegExp = _SpecialTools.clear.cckbRegExp.isChecked()
                    if _SpecialTools.cbInformationSection.currentIndex()==0:
                        myString = clear(cbClearType, newString, 
                                               oldString, isCaseInsensitive, isRegExp)
                    elif _SpecialTools.cbInformationSection.currentIndex()==1:
                        myString = clear(cbClearType, newString[:informationSectionX], 
                                               oldString, isCaseInsensitive, isRegExp)
                        myString += newString[informationSectionX:]
                    elif _SpecialTools.cbInformationSection.currentIndex()==2:
                        myString = newString[:informationSectionX]
                        myString += clear(cbClearType, newString[informationSectionX:], 
                                                oldString, isCaseInsensitive, isRegExp)
                    elif _SpecialTools.cbInformationSection.currentIndex()==3:
                        myString = clear(cbClearType, newString[:-informationSectionX], 
                                               oldString, isCaseInsensitive, isRegExp)
                        myString += newString[-informationSectionX:]
                    elif _SpecialTools.cbInformationSection.currentIndex()==4:
                        myString = newString[:-informationSectionX]
                        myString += clear(cbClearType, newString[-informationSectionX:], 
                                                oldString, isCaseInsensitive, isRegExp)
                    elif _SpecialTools.cbInformationSection.currentIndex()==5:
                        myString = newString[:informationSectionX]
                        myString += clear(cbClearType, newString[informationSectionX:informationSectionY], 
                                                oldString, isCaseInsensitive, isRegExp)
                        myString += newString[informationSectionY:]
                    elif _SpecialTools.cbInformationSection.currentIndex()==6:
                        myString = clear(cbClearType, newString[:informationSectionX], 
                                                oldString, isCaseInsensitive, isRegExp)
                        myString += newString[informationSectionX:informationSectionY]
                        myString += clear(cbClearType, newString[informationSectionY:], 
                                                oldString, isCaseInsensitive, isRegExp)
                    Universals.MainWindow.Table.item(rowNo,columnNo).setText(trForUI(myString))
    
    def clear(_cbClearType, _oldString="", _searchString="", _isCaseInsensitive=True, _isRegExp=False):
        from Core.MyObjects import translate
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
                import re
                if _isCaseInsensitive ==True:
                    pattern = re.compile(Universals.trUnicode(_searchString), re.I | re.U)
                    myString = re.sub(pattern,Universals.trUnicode(""), Universals.trUnicode(_oldString))
                else:
                    pattern = re.compile(Universals.trUnicode(_searchString))
                    myString = re.sub(pattern,Universals.trUnicode(""), Universals.trUnicode(_oldString))
            else:
                if _isCaseInsensitive==True:
                    import re
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
                        import re
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
                            import re
                            pattern = re.compile(re.escape(Universals.trUnicode(_searchStrings[filterNo])), re.I | re.U)
                            newString = re.sub(pattern,Universals.trUnicode(makeCorrectCaseSensitive(_searchStrings[filterNo], _cbCharacterType)), Universals.trUnicode(newString))
                        else:
                            newString = newString.replace(_searchStrings[filterNo],makeCorrectCaseSensitive(_searchStrings[filterNo], _cbCharacterType))
        else:
            newString = makeCorrectCaseSensitive(_inputString, _cbCharacterType)
        return newString
        
    def correctCaseSensitiveTable(_SpecialTools):
        from Core.MyObjects import trForUI
        import Tables
        Tables.isChangeHiddenColumn,Tables.isAskShowHiddenColumn=True,True
        searchStrings = str(_SpecialTools.characterState.leSearch.text()).split(";")
        if _SpecialTools.characterState.columns.currentIndex()==0:
            columns = list(range(0,Universals.MainWindow.Table.columnCount()))
        else:
            columns = [_SpecialTools.characterState.columns.currentIndex()-1]
        for columnNo in columns:
            if Tables.checkHiddenColumn(columnNo,False)==False:
                continue
            for rowNo in range(Universals.MainWindow.Table.rowCount()):
                if Universals.MainWindow.Table.isChangableItem(rowNo, columnNo):
                    newString = str(Universals.MainWindow.Table.item(rowNo,columnNo).text())
                    myString = ""
                    informationSectionX = _SpecialTools.cbInformationSectionX.value()
                    informationSectionY = _SpecialTools.cbInformationSectionY.value()
                    cbCharacterType = Variables.validSentenceStructureKeys[_SpecialTools.characterState.cbCharacterType.currentIndex()]
                    isCaseInsensitive = _SpecialTools.characterState.cckbCaseInsensitive.isChecked()
                    isRegExp = _SpecialTools.characterState.cckbRegExp.isChecked()
                    isCorrectText = _SpecialTools.characterState.cckbCorrectText.isChecked()
                    if _SpecialTools.cbInformationSection.currentIndex()==0:
                        myString = correctCaseSensitive(newString, cbCharacterType, isCorrectText, searchStrings, isCaseInsensitive, isRegExp)
                    elif _SpecialTools.cbInformationSection.currentIndex()==1:
                        myString = correctCaseSensitive(newString[:informationSectionX], cbCharacterType, isCorrectText, searchStrings, isCaseInsensitive, isRegExp)
                        myString += newString[informationSectionX:]
                    elif _SpecialTools.cbInformationSection.currentIndex()==2:
                        myString = newString[:informationSectionX]
                        myString += correctCaseSensitive(newString[informationSectionX:], cbCharacterType, isCorrectText, searchStrings, isCaseInsensitive, isRegExp)
                    elif _SpecialTools.cbInformationSection.currentIndex()==3:
                        myString = correctCaseSensitive(newString[:-informationSectionX], cbCharacterType, isCorrectText, searchStrings, isCaseInsensitive, isRegExp)
                        myString += newString[-informationSectionX:]
                    elif _SpecialTools.cbInformationSection.currentIndex()==4:
                        myString = newString[:-informationSectionX]
                        myString += correctCaseSensitive(newString[-informationSectionX:], cbCharacterType, isCorrectText, searchStrings, isCaseInsensitive, isRegExp)
                    elif _SpecialTools.cbInformationSection.currentIndex()==5:
                        myString = newString[:informationSectionX]
                        myString += correctCaseSensitive(newString[informationSectionX:informationSectionY], cbCharacterType, isCorrectText, searchStrings, isCaseInsensitive, isRegExp)
                        myString += newString[informationSectionY:]
                    elif _SpecialTools.cbInformationSection.currentIndex()==6:
                        myString = correctCaseSensitive(newString[:informationSectionX], cbCharacterType, isCorrectText, searchStrings, isCaseInsensitive, isRegExp)
                        myString += newString[informationSectionX:informationSectionY]
                        myString += correctCaseSensitive(newString[informationSectionY:], cbCharacterType, isCorrectText, searchStrings, isCaseInsensitive, isRegExp)
                    Universals.MainWindow.Table.item(rowNo,columnNo).setText(trForUI(myString))
            
            
            
