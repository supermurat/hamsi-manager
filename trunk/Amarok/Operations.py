## This file is part of HamsiManager.
##
## Copyright (c) 2010 - 2014 Murat Demir <mopened@gmail.com>
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


import Amarok
from Amarok import Commands
from Core.MyObjects import *
import Taggers
import FileUtils as fu
from Core import Universals as uni
from Core import Dialogs
from Core import Records
from Core import ReportBug


def getDirectoriesAndValues(_filter=""):
    db = Amarok.checkAndGetDB()
    if db is not None:
        return Commands.getDirectoriesAndValues(_filter)
    return None


def getAllMusicFileValuesWithNames(_filter="", _artistId=None):
    db = Amarok.checkAndGetDB()
    if db is not None:
        return Commands.getAllMusicFileValuesWithNames(_filter, _artistId)
    return None


def getAllArtistsValues(_filter=""):
    db = Amarok.checkAndGetDB()
    if db is not None:
        return Commands.getAllArtistsValues(_filter)
    return None


def changePaths(_values, _type="auto"):
    uni.startThreadAction()
    allItemNumber = len(_values)
    for valueNo, value in enumerate(_values):
        isContinueThreadAction = uni.isContinueThreadAction()
        if isContinueThreadAction:
            try:
                if _type == "file" or (_type == "auto" and fu.isFile(value["newPath"])):
                    Commands.changeFilePath(value["oldPath"], value["newPath"])
                else:
                    Commands.changeDirectoryPath(value["oldPath"], value["newPath"])
            except:
                ReportBug.ReportBug()
        else:
            allItemNumber = valueNo + 1
        Dialogs.showState(translate("Amarok/Operations", "Changing Paths In Amarok Database"),
                          valueNo + 1, allItemNumber, True)
        if isContinueThreadAction is False:
            break
    uni.finishThreadAction()


def changeTags(_values):
    uni.startThreadAction()
    allItemNumber = len(_values)
    for valueNo, value in enumerate(_values):
        isContinueThreadAction = uni.isContinueThreadAction()
        if isContinueThreadAction:
            try:
                Commands.changeTag(value)
            except:
                ReportBug.ReportBug()
        else:
            allItemNumber = valueNo + 1
        Dialogs.showState(translate("Amarok/Operations", "Changing Tags In Amarok Database"),
                          valueNo + 1, allItemNumber, True)
        if isContinueThreadAction is False:
            break
    uni.finishThreadAction()


def changeArtistValues(_values):
    uni.startThreadAction()
    allItemNumber = len(_values)
    Dialogs.showState(translate("Amarok/Operations", "Writing Music Tags"), 0, allItemNumber, True)
    for x, value in enumerate(_values):
        isContinueThreadAction = uni.isContinueThreadAction()
        if isContinueThreadAction:
            musicFilePathAndArtist = Commands.changeArtistValue(value)
            if musicFilePathAndArtist is not None:
                artistName = musicFilePathAndArtist[1]
                for musicFilePath in musicFilePathAndArtist[0]:
                    if fu.isWritableFileOrDir(musicFilePath, False, True):
                        Records.add(str(translate("Amarok/Operations", "File will be updated")), str(musicFilePath))
                        currentArtistName = ""
                        tagger = Taggers.getTagger()
                        if tagger is not None:
                            try:
                                tagger.loadFileForWrite(musicFilePath)
                                currentArtistName = tagger.getArtist()
                            except:
                                tagger.loadFileForWrite(musicFilePath)
                            tagger.setArtist(artistName)
                            tagger.update()
                            Records.add(str(translate("Amarok/Operations", "Artist")), str(currentArtistName),
                                        artistName)
        else:
            allItemNumber = x + 1
        Dialogs.showState(translate("Amarok/Operations", "Writing Music Tags"), x + 1, allItemNumber, True)
        if isContinueThreadAction is False:
            break
    uni.finishThreadAction()
