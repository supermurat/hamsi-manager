# -*- coding: utf-8 -*-
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


import Variables
from MyObjects import *
import Universals
import Dialogs
import ReportBug

class Taggers():
    global getTagger, getSelectedTaggerType, setSelectedTaggerType, getSelectedTaggerTypeName, setSelectedTaggerTypeName, taggersNames, selectedTaggerType, getAvailableLabelsForTable, getAvailableKeysForTable, getTaggerTypes, getTaggerTypesName, getLoaddedTagger, loaddedTagger
    taggersNames = []
    selectedTaggerType = None
    loaddedTagger = None
    
    def __init__(self):
        pass
        
    def getTagger(_isAlertIfNotExist=False):
        global taggersNames, loaddedTagger
        try:
            if len(taggersNames)==0:
                taggersNames = Variables.getTaggersNames()
            for tagger in taggersNames:
                exec ("from " + tagger + " import isAvailable,pluginName,Tagger")
                exec ("import " + tagger + " as TaggerLoaded")
                if isAvailable:
                    loaddedTagger = TaggerLoaded
                    return Tagger()
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
        
    def getSelectedTaggerType():
        type = getSelectedTaggerTypeName()
        for x, v in enumerate(getLoaddedTagger().getTaggerTypes()):
            if type==getTaggerTypesName()[x]:
                return v
        return getLoaddedTagger().getTaggerTypes()[0]
        
    def setSelectedTaggerType(_type, _isSetTypeName=True):
        typeName = getTaggerTypesName()[0]
        for x, v in enumerate(getLoaddedTagger().getTaggerTypes()):
            if v==_type:
                typeName = getTaggerTypesName()[x]
        Universals.setMySetting(getLoaddedTagger().pluginName + "TaggerType", _type)
        if _isSetTypeName:
            setSelectedTaggerTypeName(typeName, False)
        
    def getSelectedTaggerTypeName():
        try:
            return Universals.MySettings[getLoaddedTagger().pluginName + "TaggerType"]
        except:
            return getTaggerTypesName()[0]
        
    def setSelectedTaggerTypeName(_typeName, _isSetType=True):
        type = getLoaddedTagger().getTaggerTypes()[0]
        for x, v in enumerate(getTaggerTypesName()):
            if _typeName==v:
                type = getLoaddedTagger().getTaggerTypes()[x]
        Universals.setMySetting(getLoaddedTagger().pluginName + "TaggerType", type)
        if _isSetTypeName:
            setSelectedTaggerType(type, False)
        
    def getTaggerTypes():
        return getLoaddedTagger().getTaggerTypes()
        
    def getTaggerTypesName():
        return getLoaddedTagger().getTaggerTypesName()
        
    def getAvailableLabelsForTable():
        return getLoaddedTagger().getAvailableLabelsForTable()
        
    def getAvailableKeysForTable():
        return getLoaddedTagger().getAvailableKeysForTable()
        
        
        
        
