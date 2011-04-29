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
    global getDirectoriesAndValues, changePaths, changeTags, getAllMusicFileValuesWithNames
    
    def getDirectoriesAndValues():
        db = Amarok.checkAndGetDB()
        if db!=None:
            return Commands.getDirectoriesAndValues()
        return None
        
    def getAllMusicFileValuesWithNames():
        db = Amarok.checkAndGetDB()
        if db!=None:
            return Commands.getAllMusicFileValuesWithNames()
        return None
        
    def changePaths(_values):
        for value in _values:
            Commands.changePath(value["oldPath"], value["newPath"])
        
    def changeTags(_values):
        for value in _values:
            Commands.changeTag(value)
            
            
            
            
            
            

