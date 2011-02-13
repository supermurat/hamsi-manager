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


import Amarok
from Amarok import Commands

class Operations:
    global getDirectoriesAndValues, changePaths
    
    def getDirectoriesAndValues():
        db = Amarok.checkAndGetDB()
        if db!=None:
            directoriesValues = {}
            rows = Commands.getDirectoriesAndValues()
            for row in rows:
                if row[0] not in directoriesValues:
                    directoriesValues[row[0]] = {"coverPath" : [], "Artist" : [], "Album" : [], "Genre" : [], "Year" : []}
                directoriesValues[row[0]]["coverPath"].append(row[1])
                directoriesValues[row[0]]["Artist"].append(row[2])
                directoriesValues[row[0]]["Album"].append(row[3])
                directoriesValues[row[0]]["Genre"].append(row[4])
                directoriesValues[row[0]]["Year"].append(row[5])
            return directoriesValues
        return None
        
    def changePaths(_values):
        for value in _values:
            Commands.changePath(value["oldPath"], value["newPath"])
        
            
            
            

