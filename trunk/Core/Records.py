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
from Core import Universals
import InputOutputs
import logging
from Core.Universals import translate

class Records():
    global add, create, read, setTitle, clearRecords, recordContents, isSetedTitle, saveAllRecords,recordContents, checkSize, recordType, lastRecordType, setRecordType, restoreRecordType, getBackupRecordsList
    recordContents = ""
    isSetedTitle = False
    recordType = 0 # 0=Normal, 1=Debug
    lastRecordType = 0
    
    def create():
        global recordContents
        recordContents = str(translate("Records", "Hamsi Manager Record File - Time Created : ")) + str(time.strftime("%d.%m.%Y %H:%M:%S"))+"\n"
    
    def setTitle(_title):
        global isSetedTitle, recordContents
        if "isSaveActions" not in Universals.MySettings.keys() or Universals.getBoolValue("isSaveActions"):
            recordContents += str(_title) + "\n"
        if Universals.loggingLevel==logging.DEBUG:
            print (_title)
        isSetedTitle = True
    
    def add(_action, _previous="", _now=None):
        global recordContents
        if "isSaveActions" not in Universals.MySettings.keys() or Universals.getBoolValue("isSaveActions"):
            if recordType==0 or (recordType==1 and Universals.loggingLevel==logging.DEBUG):
                if _now is not None:
                    recordContents += str(_action + " ::::::: '") + str(_previous) + "' >>>>>>>> '" + str(_now) + "' <<<<<<< " + str(time.strftime("%d.%m.%Y %H:%M:%S"))+"\n"
                else:
                    recordContents += str(_action + " ::::::: '") + str(_previous) + "' " + str(time.strftime("%d.%m.%Y %H:%M:%S"))+"\n"
        if Universals.loggingLevel==logging.DEBUG:
            if _now is not None:
                print (str(_action + " ::::::: '") + str(_previous) + "' >>>>>>>> '" + str(_now) + "' <<<<<<< " + str(time.strftime("%d.%m.%Y %H:%M:%S"))+"\n")
            else:
                print (str(_action + " ::::::: '") + str(_previous) + "' " + str(time.strftime("%d.%m.%Y %H:%M:%S"))+"\n")
        
    def setRecordType(_recordType):
        global lastRecordType, recordType
        lastRecordType = recordType
        recordType = _recordType
        
    def restoreRecordType():
        global recordType
        recordType = lastRecordType
        
    def saveAllRecords():
        global recordContents, isSetedTitle
        if "isSaveActions" not in Universals.MySettings.keys() or Universals.getBoolValue("isSaveActions"):
            if InputOutputs.isFile(Universals.recordFilePath)==False:
                create()
            setRecordType(1)
            InputOutputs.addToFile(Universals.recordFilePath, recordContents)
            restoreRecordType()
        recordContents = ""
        isSetedTitle = False
    
    def checkSize():
        setRecordType(1)
        if InputOutputs.isFile(Universals.recordFilePath):
            if InputOutputs.getSize(Universals.recordFilePath) > (int(Universals.MySettings["maxRecordFileSize"])*1024):
                InputOutputs.moveFileOrDir(Universals.recordFilePath, InputOutputs.joinPath(Universals.oldRecordsDirectoryPath, str(time.strftime("%Y%m%d_%H%M%S")) + ".txt"))
        restoreRecordType()
        
    def getBackupRecordsList():
        if InputOutputs.isDir(Universals.oldRecordsDirectoryPath)==True:
            return InputOutputs.readDirectory(Universals.oldRecordsDirectoryPath, "file")
        else:
            return []
        
    def read(_recordFilePath=Universals.recordFilePath):
        if InputOutputs.isFile(_recordFilePath)==True:
            return InputOutputs.readFromFile(_recordFilePath)
        else:
            create()
            setRecordType(1)
            InputOutputs.addToFile(_recordFilePath, recordContents)
            restoreRecordType()
            return recordContents
            
    def clearRecords():
        InputOutputs.writeToFile(Universals.recordFilePath, str(translate("Records", "Hamsi Manager Record File - Time Clear : ")) + str(time.strftime("%d.%m.%Y %H:%M:%S"))+"\n")
            
            
            
