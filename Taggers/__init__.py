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


from Core.MyObjects import *
from Core import Universals as uni
from Core import Dialogs
from Core import ReportBug

taggersNames = []
loaddedTagger = None


def getTagger(_isAlertIfNotExist=False):
    global taggersNames, loaddedTagger
    try:
        if len(taggersNames) == 0:
            taggersNames = uni.getTaggersNames()
        for tagger in taggersNames:
            taggerModule = __import__("Taggers." + tagger, globals(), locals(), ["isAvailable", "Tagger"], 0)
            TaggerLoaded = __import__("Taggers." + tagger, globals(), locals(), [tagger], 0)
            if taggerModule.isAvailable:
                loaddedTagger = TaggerLoaded
                return taggerModule.Tagger()
        if _isAlertIfNotExist:
            Dialogs.show(translate("Taggers", "You Have Not Any Tagger"),
                         translate("Taggers", "Not found any tagger in your system. "
                                              "Please install a tagger module. "
                                              "Now supporting only eyeD3 module (python-eyed3)."))
        return None
    except:
        ReportBug.ReportBug()


def getLoaddedTagger():
    if loaddedTagger is None:
        getTagger()
    return loaddedTagger


def getSelectedTaggerTypeForRead():
    selectedTaggerType = getSelectedTaggerTypeForReadName()
    for x, v in enumerate(getLoaddedTagger().getTaggerTypes()):
        if selectedTaggerType == getTaggerTypesName()[x]:
            return v
    return getLoaddedTagger().getTaggerTypes()[0]


def getSelectedTaggerTypeForReadName():
    return uni.getValue(getLoaddedTagger().pluginName + "TaggerTypeNameForRead", getTaggerTypesName()[0])


def setSelectedTaggerTypeForReadName(_typeName):
    uni.setMySetting(getLoaddedTagger().pluginName + "TaggerTypeNameForRead", _typeName)


def getSelectedTaggerTypeForWrite():
    selectedTaggerType = getSelectedTaggerTypeForWriteName()
    for x, v in enumerate(getLoaddedTagger().getTaggerTypes()):
        if selectedTaggerType == getTaggerTypesName()[x]:
            return v
    return getLoaddedTagger().getTaggerTypes()[0]


def getSelectedTaggerTypeForWriteName():
    return uni.getValue(getLoaddedTagger().pluginName + "TaggerTypeNameForWrite", getTaggerTypesName()[0])


def setSelectedTaggerTypeForWriteName(_typeName):
    uni.setMySetting(getLoaddedTagger().pluginName + "TaggerTypeNameForWrite", _typeName)


def getTaggerTypes():
    return getLoaddedTagger().getTaggerTypes()


def getTaggerTypesName():
    return getLoaddedTagger().getTaggerTypesName()


def getAvailableLabelsForTable():
    return getLoaddedTagger().getAvailableLabelsForTable()


def getAvailableKeysForTable():
    return getLoaddedTagger().getAvailableKeysForTable()


def getReadOnlyKeysForTable():
    return getLoaddedTagger().getReadOnlyKeysForTable()


def getImageTypes():
    return getLoaddedTagger().getImageTypes()


def getImageTypesNo():
    return getLoaddedTagger().getImageTypesNo()


