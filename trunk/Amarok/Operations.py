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


import Amarok
from Amarok import Commands

class Operations:
    global getDirectoriesAndValues, changePaths, changeTags, getAllMusicFileValuesWithNames, getAllArtistsValues, changeArtistValues
    
    def getDirectoriesAndValues():
        db = Amarok.checkAndGetDB()
        if db!=None:
            return Commands.getDirectoriesAndValues()
        return None
        
    def getAllMusicFileValuesWithNames(_filter = ""):
        db = Amarok.checkAndGetDB()
        if db!=None:
            return Commands.getAllMusicFileValuesWithNames(_filter)
        return None
        
    def getAllArtistsValues(_filter = "", _isOnlyArtistFilter = False):
        db = Amarok.checkAndGetDB()
        if db!=None:
            return Commands.getAllArtistsValues(_filter, _isOnlyArtistFilter)
        return None
        
    def changePaths(_values):
        import Taggers, InputOutputs, Universals, Dialogs, Records, ReportBug
        Universals.startThreadAction()
        allItemNumber = len(_values)
        for valueNo,value in enumerate(_values):
            isContinueThreadAction = Universals.isContinueThreadAction()
            if isContinueThreadAction:
                try:
                    Commands.changePath(value["oldPath"], value["newPath"])
                except:
                    error = ReportBug.ReportBug()
                    error.show()   
            else:
                allItemNumber = valueNo+1
            Dialogs.showState(Universals.translate("Amarok/Operations", "Changing Paths In Amarok Database"),
                              valueNo+1,allItemNumber, True) 
            if isContinueThreadAction==False:
                break
        Universals.finishThreadAction()
        
    def changeTags(_values):
        import Taggers, InputOutputs, Universals, Dialogs, Records, ReportBug
        Universals.startThreadAction()
        allItemNumber = len(_values)
        for valueNo,value in enumerate(_values):
            isContinueThreadAction = Universals.isContinueThreadAction()
            if isContinueThreadAction:
                try:
                    Commands.changeTag(value)
                except:
                    error = ReportBug.ReportBug()
                    error.show()   
            else:
                allItemNumber = valueNo+1
            Dialogs.showState(Universals.translate("Amarok/Operations", "Changing Tags In Amarok Database"),
                              valueNo+1,allItemNumber, True) 
            if isContinueThreadAction==False:
                break
        Universals.finishThreadAction()
            
    def changeArtistValues(_values):
        import Taggers, InputOutputs, Universals, Dialogs, Records
        Universals.startThreadAction()
        allItemNumber = len(_values)
        Dialogs.showState(Universals.translate("Amarok/Operations", "Writing Music Tags"),0,allItemNumber, True)
        for x, value in enumerate(_values):
            isContinueThreadAction = Universals.isContinueThreadAction()
            if isContinueThreadAction:
                musicFilePathAndArtist = Commands.changeArtistValue(value)
                if musicFilePathAndArtist!=None:
                    artistName = musicFilePathAndArtist[1]
                    for musicFilePath in musicFilePathAndArtist[0]:
                        if InputOutputs.IA.isWritableFileOrDir(musicFilePath, False, True):
                            Records.add(str(Universals.translate("Amarok/Operations", "File will be updated")), str(musicFilePath))
                            currentArtistName = ""
                            tagger = Taggers.getTagger()
                            try:
                                tagger.loadFileForWrite(musicFilePath, False)
                                currentArtistName = tagger.getArtist()
                                tagger.correctForMusicTagType()
                            except: 
                                tagger.loadFileForWrite(musicFilePath)
                            tagger.setArtist(artistName)
                            tagger.update()
                            Records.add(str(Universals.translate("Amarok/Operations", "Artist")), str(currentArtistName), artistName)
            else:
                allItemNumber = x+1
            Dialogs.showState(Universals.translate("Amarok/Operations", "Writing Music Tags"), x+1, allItemNumber, True)
            if isContinueThreadAction==False:
                break
        Universals.finishThreadAction()
                        
            
            
            
            
            

