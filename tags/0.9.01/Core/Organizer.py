# -*- coding: utf-8 -*-

from urllib import unquote, quote
import Settings
import Universals

class Organizer:
    """Music tags, filenames, Turkish characters etc. will be arranged through this class
    """
    global applySpecialCommand, showWithIncorrectChars, emend, whatDoesSpecialCommandDo,searchAndReplaceTable
    global fillTable, clearTable, makeCorrectCaseSensitive, correctCaseSensitiveTable
    global searchAndReplace, clear, correctCaseSensitive, searchAndReplaceFromSearchAndReplaceTable, getLink
    
    def emend(_inputString, _isFileOrDirectory=False, _isCorrectCaseSensitive=True, _isRichText=False):
        _inputString = str(_inputString)
        if len(_inputString)==0: return ""
        if Universals.getBoolValue("isClearFirstAndLastSpaceChars"):
            _inputString = _inputString.strip()
        if Universals.getBoolValue("isEmendIncorrectChars"):
            try:_inputString = unicode(_inputString)
            except:_inputString = unicode(_inputString, encoding="iso-8859-9")
            oldChars = ["Ý","ý", "þ", "Ð",
                         "Ã", "Ã¼", "Ä°Å", "Ã", "Ä±", "Å", "Ã§", "Ã¶","Ä", "Ä°","Ã", "Ã", "Â³", "Ä",
                         "Å","Ä","Å","Ã§",
                         "" , "" ,"Ã",            "" ,"Â¦", "" ,"ÃÂ°","Ã½","Ã","ï¿½",  
                         "" , "" , "Â³",              "" , "" ,
                         "§" ,"¦","ä","Ä","Ä","Ã°","ã","Ã","ð", 
                         "" ,"Ã" , "" ,"å","ã","å","Ã¾","ã¾",
                         "_","ã","Ã","å","Å"]
            newChars = ["İ", "ı", "ş", "ğ",
                         "Ü", "ü", "İ", "ç", "ı","ş", "ç", "ö", "ğ", "İ", "Ö", "Ö", "ü", "ğ",
                         "Ş","Ğ","ş", "ç",
                         "ö" , "Ö" ,"Ö",                   "İ" , "ı" , "I" ,"İ","ı","i","İ",  
                         "ü" , "Ü" , "Ü",                   "Ç" , "ç" ,
                         "ğ" ,"Ğ","ğ","Ğ","ğ","ğ","ğ","Ğ","ğ", 
                         "Ş" ,"Ş" , "ş" ,"ş","ş","ş","ş","ş",
                         " ","","","",""]
            _inputString = unquote(_inputString)
            for x in range(0,len(oldChars)):
                _inputString = _inputString.replace(oldChars[x],newChars[x])
        _inputString = showWithIncorrectChars(_inputString)
        if len(_inputString)==0: return ""
        preString, extString, ext2String = "", "", ""
        if _isFileOrDirectory:
            if _inputString[-1]=="/":
                _inputString = _inputString[:-1]
                ext2String = "/"
            if _inputString.find("/")!=-1:
                preString = _inputString.rsplit("/", 1)[0] + "/"
                _inputString = _inputString.rsplit("/", 1)[1]
            if _inputString.find(".")!=-1:
                if Universals.MySettings["fileExtesionIs"]==Universals.fileExtesionIsKeys[0]:
                    extString = "." + _inputString.split(".", 1)[1]
                    _inputString = _inputString.split(".", 1)[0]
                elif Universals.MySettings["fileExtesionIs"]==Universals.fileExtesionIsKeys[1]:
                    extString = "." + _inputString.rsplit(".", 1)[1]
                    _inputString = _inputString.rsplit(".", 1)[0]
            if _isCorrectCaseSensitive:
                extString = makeCorrectCaseSensitive(extString, Universals.MySettings["validSentenceStructureForFileExtension"])
                _inputString = makeCorrectCaseSensitive(_inputString, Universals.MySettings["validSentenceStructureForFile"])
            if Universals.MySettings["fileReNamerType"]==Universals.fileReNamerTypeNamesKeys[0]:
                oldChars = []
                newChars = []
            elif Universals.MySettings["fileReNamerType"]==Universals.fileReNamerTypeNamesKeys[1]:
                oldChars = [" ", "ç", "Ç", "ğ", "Ğ", "İ", "ı", "ö", "Ö", "ü", "Ü", "ş", "Ş"]
                newChars = ["_", "c", "C", "g", "G", "I", "i", "o", "O", "u", "U", "s", "S"]
            elif Universals.MySettings["fileReNamerType"]==Universals.fileReNamerTypeNamesKeys[2]:
                oldChars = ["ç", "Ç", "ğ", "Ğ", "İ", "ı", "ö", "Ö", "ü", "Ü", "ş", "Ş"]
                newChars = ["c", "C", "g", "G", "I", "i", "o", "O", "u", "U", "s", "S"]
            for x in range(0,len(oldChars)):
                _inputString = _inputString.replace(oldChars[x],newChars[x])
            if Universals.MySettings["fileReNamerType"]==Universals.fileReNamerTypeNamesKeys[1]:
                _inputString = quote(_inputString)
            if Universals.getBoolValue("isCorrectFileNameWithSearchAndReplaceTable"):
                _inputString = searchAndReplaceFromSearchAndReplaceTable(_inputString)
        else:
            if _isCorrectCaseSensitive:
                _inputString = makeCorrectCaseSensitive(_inputString, Universals.MySettings["validSentenceStructure"])
            _inputString = searchAndReplaceFromSearchAndReplaceTable(_inputString)
        if _isRichText==False:
            if Universals.getBoolValue("isCorrectDoubleSpaceChars"):
                isFinded=_inputString.find("  ")
                while isFinded!=-1:
                    _inputString=_inputString.replace("  "," ")
                    isFinded=_inputString.find("  ")
        return preString + _inputString + extString + ext2String
    
    def makeCorrectCaseSensitive(_inputString, _cbCharacterType):
        if _cbCharacterType==Universals.validSentenceStructureKeys[0]:
            return str(unicode(_inputString).title())
        elif _cbCharacterType==Universals.validSentenceStructureKeys[1]:
            return str(unicode(_inputString).lower())
        elif _cbCharacterType==Universals.validSentenceStructureKeys[2]:
            return str(unicode(_inputString).upper())
        elif _cbCharacterType==Universals.validSentenceStructureKeys[3]:
            return str(unicode(_inputString).capitalize())
        else :
            return str(unicode(_inputString))
    
    def showWithIncorrectChars(_inputString):
        try:
            _inputString = str(_inputString)
            _inputString = _inputString.decode("utf-8", "replace")
            return str(_inputString)
        except:
            _inputString = _inputString.decode("utf-8", "ignore")
            return str(_inputString)
    
    def getLink(_stringPath):
        _stringPath = str(_stringPath)
        return "<a href=\"file://%s\" target=\"_blank\">%s</a>" % (_stringPath, _stringPath)

    def searchAndReplaceFromSearchAndReplaceTable(_oldString):
        newString = _oldString
        for info in Settings.searchAndReplaceTable():
            if info[3]==1:
                isCaseSensitive, isRegExp = False, False
                if info[4]==1:
                    isCaseSensitive = True
                if info[5]==1:
                    isRegExp = True
                newString = searchAndReplace(newString, [info[1]], [info[2]], isCaseSensitive, isRegExp)
        return newString
    
    def applySpecialCommand(_splitPointer, _whereIsSplitPointer, _command, _SpecialTools):
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
                    if Universals.MainWindow.Table.isColumnHidden(no)==True and Tables.isAskShowHiddenColumn==True:
                        if Tables.checkHiddenColumn(columnName,no)==False:
                            return False
                    changingColumns.append(no)
        if len(changingColumns)==0:
            return False
        for columnName in changers:
            columnName=columnName.strip()
            for no,column in enumerate(Universals.MainWindow.Table.tableColumnsKey):
                if columnName==column:
                    if Universals.MainWindow.Table.isColumnHidden(no)==True and Tables.isAskShowHiddenColumn==True:
                        if Tables.checkHiddenColumn(columnName,no)==False:
                            return False
                    changerColumns.append(no)
        if len(changerColumns)==0:
            return False
        if Tables.isChangeHiddenColumn==True:
            if Universals.isShowOldValues==True:
                startedRowNo,rowStep=1,2
            else:
                startedRowNo,rowStep=0,1
            if _whereIsSplitPointer=="right":
                for rowNo in range(startedRowNo,Universals.MainWindow.Table.rowCount(),rowStep):
                    if Universals.MainWindow.Table.item(rowNo,changingColumns[0]).isSelected()==Universals.isChangeSelected or Universals.isChangeAll==True:
                        newString=""
                        for changerColumnNo in changerColumns:
                            if unicode(Universals.MainWindow.Table.item(rowNo,changerColumnNo).text()).encode("utf-8") != "-----":
                                newString+=" "+_splitPointer+" "+unicode(Universals.MainWindow.Table.item(rowNo,changerColumnNo).text()).encode("utf-8")
                        newString = emend(newString[2:])
                        if newString!="":
                            for uzanti in Universals.getListFromStrint(Universals.MySettings["musicExtensions"]):
                                if newString.split(".")[-1].decode("utf-8").lower() == unicode(uzanti,"utf-8") :
                                    newString = newString[:-len(newString.split(".")[-1])-1]
                            if _SpecialTools.btChange.isChecked()==True:
                                pass
                            elif _SpecialTools.tbAddToBefore.isChecked()==True:
                                newString += unicode(Universals.MainWindow.Table.item(rowNo,changingColumns[0]).text()).encode("utf-8")
                            elif _SpecialTools.tbAddToAfter.isChecked()==True:
                                newString = unicode(Universals.MainWindow.Table.item(rowNo,changingColumns[0]).text()).encode("utf-8") + newString
                            Universals.MainWindow.Table.item(rowNo,changingColumns[0]).setText(newString.strip().decode("utf-8"))
            else:
                for rowNo in range(startedRowNo,Universals.MainWindow.Table.rowCount(),rowStep):
                    newString = unicode(Universals.MainWindow.Table.item(rowNo,changerColumns[0]).text()).encode("utf-8")
                    if newString!="-----":
                        for uzanti in Universals.getListFromStrint(Universals.MySettings["musicExtensions"]):
                            if newString.split(".")[-1].decode("utf-8").lower() == unicode(uzanti,"utf-8") :
                                newString = newString[:-len(newString.split(".")[-1])-1]
                        newStrings = ["","","","","","","",""]
                        newString = newString.split(_splitPointer)
                        for stringNo in range(0,len(newString)):
                            newStrings[stringNo] = newString[stringNo]
                        stringNo=0
                        for changingColumnNo in changingColumns:
                            if Universals.MainWindow.Table.item(rowNo,changingColumnNo).isSelected()==Universals.isChangeSelected or Universals.isChangeAll==True:
                                if _SpecialTools.btChange.isChecked()==True:
                                    pass
                                elif _SpecialTools.tbAddToBefore.isChecked()==True:
                                    newStrings[stringNo] += unicode(Universals.MainWindow.Table.item(rowNo,changingColumnNo).text()).encode("utf-8")
                                elif _SpecialTools.tbAddToAfter.isChecked()==True:
                                    newStrings[stringNo] = unicode(Universals.MainWindow.Table.item(rowNo,changingColumnNo).text()).encode("utf-8") + newStrings[stringNo]
                                Universals.MainWindow.Table.item(rowNo,changingColumnNo).setText(newStrings[stringNo].strip().decode("utf-8"))
                            stringNo+=1
        
    def whatDoesSpecialCommandDo(_splitPointer, _whereIsSplitPointer, _command, _isCorrect=False, _isReturnDetails=False):
        import Dialogs
        from MyObjects import translate
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
                Dialogs.show(translate("Organizer", "What Does This Command Do?"),details.decode("utf-8"))
                
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
                Dialogs.show(translate("Organizer", "What Does This Command Do?"),details.decode("utf-8"))
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
        if Universals.isShowOldValues==True:
            startedRowNo,rowStep=1,2
        else:
            startedRowNo,rowStep=0,1
        if _SpecialTools.searchAndReplace.columns.currentIndex()==0:
            columns = range(0,Universals.MainWindow.Table.columnCount())
        else:
            columns = [_SpecialTools.searchAndReplace.columns.currentIndex()-1]
        for columnNo in columns:
            if Universals.MainWindow.Table.isColumnHidden(columnNo)==True:
                continue
            for rowNo in range(startedRowNo,Universals.MainWindow.Table.rowCount(),rowStep):
                if Universals.MainWindow.Table.item(rowNo,columnNo).isSelected()==Universals.isChangeSelected or Universals.isChangeAll==True:
                    if unicode(Universals.MainWindow.Table.item(rowNo,columnNo).text()).encode("utf-8")!="":
                        newString = unicode(Universals.MainWindow.Table.item(rowNo,columnNo).text()).encode("utf-8")
                        newString = newString.decode("utf-8")
                        myString = ""
                        informationSectionX = _SpecialTools.cbInformationSectionX.value()
                        informationSectionY = _SpecialTools.cbInformationSectionY.value()
                        isCaseSensitive = _SpecialTools.searchAndReplace.cckbCaseSensitive.isChecked()
                        isRegExp = _SpecialTools.searchAndReplace.cckbRegExp.isChecked()
                        if _SpecialTools.cbInformationSection.currentIndex()==0:
                            myString = searchAndReplace(newString, searchStrings, 
                                                   replaceStrings, isCaseSensitive, isRegExp)
                        elif _SpecialTools.cbInformationSection.currentIndex()==1:
                            myString = searchAndReplace(newString[:informationSectionX], searchStrings, 
                                                   replaceStrings, isCaseSensitive, isRegExp)
                            myString += newString[informationSectionX:]
                        elif _SpecialTools.cbInformationSection.currentIndex()==2:
                            myString = newString[:informationSectionX]
                            myString += searchAndReplace(newString[informationSectionX:], searchStrings, 
                                                    replaceStrings, isCaseSensitive, isRegExp)
                        elif _SpecialTools.cbInformationSection.currentIndex()==3:
                            myString = searchAndReplace(newString[:-informationSectionX], searchStrings, 
                                                   replaceStrings, isCaseSensitive, isRegExp)
                            myString += newString[-informationSectionX:]
                        elif _SpecialTools.cbInformationSection.currentIndex()==4:
                            myString = newString[:-informationSectionX]
                            myString += searchAndReplace(newString[-informationSectionX:], searchStrings, 
                                                    replaceStrings, isCaseSensitive, isRegExp)
                        elif _SpecialTools.cbInformationSection.currentIndex()==5:
                            myString = newString[:informationSectionX]
                            myString += searchAndReplace(newString[informationSectionX:informationSectionY], searchStrings, 
                                                    replaceStrings, isCaseSensitive, isRegExp)
                            myString += newString[informationSectionY:]
                        elif _SpecialTools.cbInformationSection.currentIndex()==6:
                            myString = searchAndReplace(newString[:informationSectionX], searchStrings, 
                                                    replaceStrings, isCaseSensitive, isRegExp)
                            myString += newString[informationSectionX:informationSectionY]
                            myString += searchAndReplace(newString[informationSectionY:], searchStrings, 
                                                    replaceStrings, isCaseSensitive, isRegExp)
                        Universals.MainWindow.Table.item(rowNo,columnNo).setText(myString.decode("utf-8"))
    
    def searchAndReplace(_oldString, _searchStrings, _replaceStrings, _isCaseSensitive=True, _isRegExp=False):
        newString = _oldString
        for filterNo in range(0,len(_searchStrings)):
            if _searchStrings[filterNo]!="":
                if _isRegExp == True:
                    import re
                    if _isCaseSensitive ==True:
                        pattern = re.compile(unicode(_searchStrings[filterNo]), re.I | re.U)
                        newString = re.sub(pattern,unicode(_replaceStrings[filterNo]), unicode(newString))
                    else:
                        pattern = re.compile(unicode(_searchStrings[filterNo]))
                        newString = re.sub(pattern,unicode(_replaceStrings[filterNo]), unicode(newString))
                else:
                    if _isCaseSensitive ==True:
                        import re
                        pattern = re.compile(re.escape(unicode(_searchStrings[filterNo])), re.I | re.U)
                        newString = re.sub(pattern,unicode(_replaceStrings[filterNo]), unicode(newString))
                    else:
                        newString = newString.replace(_searchStrings[filterNo],_replaceStrings[filterNo])
        return newString
    
    def fillTable(_columnName, _SpecialTools,_newString=""):
        import Tables
        Tables.isChangeHiddenColumn,Tables.isAskShowHiddenColumn=True,True
        for No, columnName in enumerate(Universals.MainWindow.Table.tableColumns):
            if str(_columnName) == str(columnName):
                columnNo=No
                break
        if Universals.MainWindow.Table.isColumnHidden(columnNo)==True:
            if Tables.checkHiddenColumn(_columnName,columnNo,False)==False:
                return False
        if Tables.isChangeHiddenColumn==True:
            if _SpecialTools.fill.cbFillType.currentIndex()==1:
                _newString = int(_SpecialTools.fill.spStartDigit.value())-1
            if Universals.isShowOldValues==True:
                startedRowNo,rowStep=1,2
            else:
                startedRowNo,rowStep=0,1
            for rowNo in range(startedRowNo,Universals.MainWindow.Table.rowCount(),rowStep):
                if Universals.MainWindow.Table.item(rowNo,columnNo).isSelected()==Universals.isChangeSelected or Universals.isChangeAll==True:
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
                        myString += unicode(Universals.MainWindow.Table.item(rowNo,columnNo).text()).encode("utf-8")
                    elif _SpecialTools.tbAddToAfter.isChecked()==True:
                        myString = unicode(Universals.MainWindow.Table.item(rowNo,columnNo).text()).encode("utf-8") + myString
                    Universals.MainWindow.Table.item(rowNo,columnNo).setText(unicode(myString).title().decode("utf-8"))
                    
    def clearTable(_SpecialTools):
        import Tables
        Tables.isChangeHiddenColumn,Tables.isAskShowHiddenColumn=True,True
        if _SpecialTools.clear.columns.currentIndex()==0:
            columns = range(0,Universals.MainWindow.Table.columnCount())
        else:
            columns = [_SpecialTools.clear.columns.currentIndex()-1]
        if Universals.isShowOldValues==True:
            startedRowNo,rowStep=1,2
        else:
            startedRowNo,rowStep=0,1
        for columnNo in columns:
            if Universals.MainWindow.Table.isColumnHidden(columnNo)==True:
                if Tables.checkHiddenColumn(Universals.MainWindow.Table.tableColumns[columnNo],columnNo,False)==False:
                    continue
            for rowNo in range(startedRowNo,Universals.MainWindow.Table.rowCount(),rowStep):
                if Universals.MainWindow.Table.item(rowNo,columnNo).isSelected()==Universals.isChangeSelected or Universals.isChangeAll==True:
                    newString = unicode(Universals.MainWindow.Table.item(rowNo,columnNo).text(), "utf-8")
                    newString = newString.decode("utf-8")
                    informationSectionX = _SpecialTools.cbInformationSectionX.value()
                    informationSectionY = _SpecialTools.cbInformationSectionY.value()
                    isCaseSensitive = _SpecialTools.clear.cckbCaseSensitive.isChecked()
                    oldString = unicode(_SpecialTools.clear.leClear.text(), "utf-8")
                    cbClearType = _SpecialTools.clear.cbClearType.currentText()
                    isRegExp = _SpecialTools.clear.cckbRegExp.isChecked()
                    if _SpecialTools.cbInformationSection.currentIndex()==0:
                        myString = clear(cbClearType, newString, 
                                               oldString, isCaseSensitive, isRegExp)
                    elif _SpecialTools.cbInformationSection.currentIndex()==1:
                        myString = clear(cbClearType, newString[:informationSectionX], 
                                               oldString, isCaseSensitive, isRegExp)
                        myString += newString[informationSectionX:]
                    elif _SpecialTools.cbInformationSection.currentIndex()==2:
                        myString = newString[:informationSectionX]
                        myString += clear(cbClearType, newString[informationSectionX:], 
                                                oldString, isCaseSensitive, isRegExp)
                    elif _SpecialTools.cbInformationSection.currentIndex()==3:
                        myString = clear(cbClearType, newString[:-informationSectionX], 
                                               oldString, isCaseSensitive, isRegExp)
                        myString += newString[-informationSectionX:]
                    elif _SpecialTools.cbInformationSection.currentIndex()==4:
                        myString = newString[:-informationSectionX]
                        myString += clear(cbClearType, newString[-informationSectionX:], 
                                                oldString, isCaseSensitive, isRegExp)
                    elif _SpecialTools.cbInformationSection.currentIndex()==5:
                        myString = newString[:informationSectionX]
                        myString += clear(cbClearType, newString[informationSectionX:informationSectionY], 
                                                oldString, isCaseSensitive, isRegExp)
                        myString += newString[informationSectionY:]
                    elif _SpecialTools.cbInformationSection.currentIndex()==6:
                        myString = clear(cbClearType, newString[:informationSectionX], 
                                                oldString, isCaseSensitive, isRegExp)
                        myString += newString[informationSectionX:informationSectionY]
                        myString += clear(cbClearType, newString[informationSectionY:], 
                                                oldString, isCaseSensitive, isRegExp)
                    Universals.MainWindow.Table.item(rowNo,columnNo).setText(myString.decode("utf-8"))
    
    def clear(_cbClearType, _oldString="", _searchString="", _isCaseSensitive=True, _isRegExp=False):
        from MyObjects import translate
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
                if _isCaseSensitive ==True:
                    pattern = re.compile(unicode(_searchString), re.I | re.U)
                    myString = re.sub(pattern,unicode(""), unicode(_oldString))
                else:
                    pattern = re.compile(unicode(_searchString))
                    myString = re.sub(pattern,unicode(""), unicode(_oldString))
            else:
                if _isCaseSensitive==True:
                    import re
                    pattern = re.compile(re.escape(unicode(_searchString)), re.I | re.U)
                    myString = re.sub(pattern,unicode(""), unicode(_oldString))
                else:
                    myString = _oldString.replace(_searchString,"")
        return myString
     
    def correctCaseSensitive(_inputString, _cbCharacterType, isCorrectText = False, _searchStrings=[], _isCaseSensitive=True, _isRegExp=False):
        newString = _inputString
        if isCorrectText:
            for filterNo in range(0,len(_searchStrings)):
                if _searchStrings[filterNo]!="":
                    if _isRegExp == True:
                        import re
                        if _isCaseSensitive ==True:
                            m = re.search(_searchStrings[filterNo], newString, re.I | re.U)
                            try:a = m.group(0)
                            except:return newString
                            pattern = re.compile(unicode(_searchStrings[filterNo]), re.I | re.U)
                            newString = re.sub(pattern,unicode(makeCorrectCaseSensitive(m.group(0), _cbCharacterType)), unicode(newString))
                        else:
                            m = re.search(_searchStrings[filterNo], newString)
                            try:a = m.group(0)
                            except:return newString
                            pattern = re.compile(unicode(_searchStrings[filterNo]))
                            newString = re.sub(pattern,unicode(makeCorrectCaseSensitive(m.group(0), _cbCharacterType)), unicode(newString))
                    else:
                        if _isCaseSensitive ==True:
                            import re
                            pattern = re.compile(re.escape(unicode(_searchStrings[filterNo])), re.I | re.U)
                            newString = re.sub(pattern,unicode(makeCorrectCaseSensitive(_searchStrings[filterNo], _cbCharacterType)), unicode(newString))
                        else:
                            newString = newString.replace(_searchStrings[filterNo],makeCorrectCaseSensitive(_searchStrings[filterNo], _cbCharacterType))
        else:
            newString = makeCorrectCaseSensitive(_inputString, _cbCharacterType)
        return newString
        
    def correctCaseSensitiveTable(_SpecialTools):
        import Tables
        Tables.isChangeHiddenColumn,Tables.isAskShowHiddenColumn=True,True
        searchStrings = unicode(_SpecialTools.characterState.leSearch.text(), "utf-8").split(";")
        if _SpecialTools.characterState.columns.currentIndex()==0:
            columns = range(0,Universals.MainWindow.Table.columnCount())
        else:
            columns = [_SpecialTools.characterState.columns.currentIndex()-1]
        if Universals.isShowOldValues==True:
            startedRowNo,rowStep=1,2
        else:
            startedRowNo,rowStep=0,1
        for columnNo in columns:
            if Universals.MainWindow.Table.isColumnHidden(columnNo)==True:
                if Tables.checkHiddenColumn(Universals.MainWindow.Table.tableColumns[columnNo],columnNo,False)==False:
                    continue
            for rowNo in range(startedRowNo,Universals.MainWindow.Table.rowCount(),rowStep):
                if Universals.MainWindow.Table.item(rowNo,columnNo).isSelected()==Universals.isChangeSelected or Universals.isChangeAll==True:
                    newString = unicode(Universals.MainWindow.Table.item(rowNo,columnNo).text(), "utf-8")
                    myString = ""
                    informationSectionX = _SpecialTools.cbInformationSectionX.value()
                    informationSectionY = _SpecialTools.cbInformationSectionY.value()
                    cbCharacterType = Universals.validSentenceStructureKeys[_SpecialTools.characterState.cbCharacterType.currentIndex()]
                    isCaseSensitive = _SpecialTools.characterState.cckbCaseSensitive.isChecked()
                    isRegExp = _SpecialTools.characterState.cckbRegExp.isChecked()
                    isCorrectText = _SpecialTools.characterState.cckbCorrectText.isChecked()
                    if _SpecialTools.cbInformationSection.currentIndex()==0:
                        myString = correctCaseSensitive(newString, cbCharacterType, isCorrectText, searchStrings, isCaseSensitive, isRegExp)
                    elif _SpecialTools.cbInformationSection.currentIndex()==1:
                        myString = correctCaseSensitive(newString[:informationSectionX], cbCharacterType, isCorrectText, searchStrings, isCaseSensitive, isRegExp)
                        myString += newString[informationSectionX:]
                    elif _SpecialTools.cbInformationSection.currentIndex()==2:
                        myString = newString[:informationSectionX]
                        myString += correctCaseSensitive(newString[informationSectionX:], cbCharacterType, isCorrectText, searchStrings, isCaseSensitive, isRegExp)
                    elif _SpecialTools.cbInformationSection.currentIndex()==3:
                        myString = correctCaseSensitive(newString[:-informationSectionX], cbCharacterType, isCorrectText, searchStrings, isCaseSensitive, isRegExp)
                        myString += newString[-informationSectionX:]
                    elif _SpecialTools.cbInformationSection.currentIndex()==4:
                        myString = newString[:-informationSectionX]
                        myString += correctCaseSensitive(newString[-informationSectionX:], cbCharacterType, isCorrectText, searchStrings, isCaseSensitive, isRegExp)
                    elif _SpecialTools.cbInformationSection.currentIndex()==5:
                        myString = newString[:informationSectionX]
                        myString += correctCaseSensitive(newString[informationSectionX:informationSectionY], cbCharacterType, isCorrectText, searchStrings, isCaseSensitive, isRegExp)
                        myString += newString[informationSectionY:]
                    elif _SpecialTools.cbInformationSection.currentIndex()==6:
                        myString = correctCaseSensitive(newString[:informationSectionX], cbCharacterType, isCorrectText, searchStrings, isCaseSensitive, isRegExp)
                        myString += newString[informationSectionX:informationSectionY]
                        myString += correctCaseSensitive(newString[informationSectionY:], cbCharacterType, isCorrectText, searchStrings, isCaseSensitive, isRegExp)
                    Universals.MainWindow.Table.item(rowNo,columnNo).setText(myString.decode("utf-8"))
            
            
            
