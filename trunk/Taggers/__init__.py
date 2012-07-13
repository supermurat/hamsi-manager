## This file is part of HamsiManager.
## 
## Copyright (c) 2010 - 2012 Murat Demir <mopened@gmail.com>      
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


from Core import Variables
from Core.MyObjects import *
from Core import Universals
from Core import Dialogs
from Core import ReportBug

class Taggers():
    global getTagger, getSelectedTaggerTypeForRead, setSelectedTaggerTypeForRead, getSelectedTaggerTypeForReadName, setSelectedTaggerTypeForReadName, taggersNames, getAvailableLabelsForTable, getAvailableKeysForTable, getTaggerTypes, getTaggerTypesName, getLoaddedTagger, loaddedTagger, getSelectedTaggerTypeForWrite, setSelectedTaggerTypeForWrite, getSelectedTaggerTypeForWriteName, setSelectedTaggerTypeForWriteName
    taggersNames = []
    loaddedTagger = None
    
    def __init__(self):
        pass
        
    def getTagger(_isAlertIfNotExist=False):
        global taggersNames, loaddedTagger
        try:
            if len(taggersNames)==0:
                taggersNames = Variables.getTaggersNames()
            for tagger in taggersNames:
                taggerModule = __import__("Taggers." + tagger, globals(), locals(), ["isAvailable", "Tagger"], -1)
                TaggerLoaded = __import__("Taggers." + tagger, globals(), locals(), [tagger], -1)
                if taggerModule.isAvailable:
                    loaddedTagger = TaggerLoaded
                    return taggerModule.Tagger()
            if _isAlertIfNotExist:
                Dialogs.show(translate("Taggers", "You Have Not Any Tagger"), 
                                    translate("Taggers", "Not found any tagger in your system. Please install a tagger module. Now supporting only eyeD3 module (python-eyed3)."))
            return None
        except:
            error = ReportBug.ReportBug()
            error.show()
            
    def getLoaddedTagger():
        if loaddedTagger==None:
            getTagger()
        return loaddedTagger
        
    def getSelectedTaggerTypeForRead():
        type = getSelectedTaggerTypeForReadName()
        for x, v in enumerate(getLoaddedTagger().getTaggerTypes()):
            if type==getTaggerTypesName()[x]:
                return v
        return getLoaddedTagger().getTaggerTypes()[0]
        
    def setSelectedTaggerTypeForRead(_type, _isSetTypeName=True):
        typeName = getTaggerTypesName()[0]
        for x, v in enumerate(getLoaddedTagger().getTaggerTypes()):
            if v==_type:
                typeName = getTaggerTypesName()[x]
        if _isSetTypeName:
            setSelectedTaggerTypeForReadName(typeName, False)
        
    def getSelectedTaggerTypeForReadName():
        return Universals.getValue(getLoaddedTagger().pluginName + "TaggerTypeNameForRead", getTaggerTypesName())
        
    def setSelectedTaggerTypeForReadName(_typeName, _isSetType=True):
        type = getLoaddedTagger().getTaggerTypes()[0]
        for x, v in enumerate(getTaggerTypesName()):
            if _typeName==v:
                type = getLoaddedTagger().getTaggerTypes()[x]
        Universals.setMySetting(getLoaddedTagger().pluginName + "TaggerTypeNameForRead", _typeName)
        if _isSetType:
            setSelectedTaggerTypeForRead(type, False)
        
    def getSelectedTaggerTypeForWrite():
        type = getSelectedTaggerTypeForWriteName()
        for x, v in enumerate(getLoaddedTagger().getTaggerTypes()):
            if type==getTaggerTypesName()[x]:
                return v
        return getLoaddedTagger().getTaggerTypes()[0]
        
    def setSelectedTaggerTypeForWrite(_type, _isSetTypeName=True):
        typeName = getTaggerTypesName()[0]
        for x, v in enumerate(getLoaddedTagger().getTaggerTypes()):
            if v==_type:
                typeName = getTaggerTypesName()[x]
        if _isSetTypeName:
            setSelectedTaggerTypeForWriteName(typeName, False)
        
    def getSelectedTaggerTypeForWriteName():
        return Universals.getValue(getLoaddedTagger().pluginName + "TaggerTypeNameForWrite", getTaggerTypesName())
        
    def setSelectedTaggerTypeForWriteName(_typeName, _isSetType=True):
        type = getLoaddedTagger().getTaggerTypes()[0]
        for x, v in enumerate(getTaggerTypesName()):
            if _typeName==v:
                type = getLoaddedTagger().getTaggerTypes()[x]
        Universals.setMySetting(getLoaddedTagger().pluginName + "TaggerTypeNameForWrite", _typeName)
        if _isSetType:
            setSelectedTaggerTypeForWrite(type, False)
        
    def getTaggerTypes():
        return getLoaddedTagger().getTaggerTypes()
        
    def getTaggerTypesName():
        return getLoaddedTagger().getTaggerTypesName()
        
    def getAvailableLabelsForTable():
        return getLoaddedTagger().getAvailableLabelsForTable()
        
    def getAvailableKeysForTable():
        return getLoaddedTagger().getAvailableKeysForTable()
        
        
        
        
