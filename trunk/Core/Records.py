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
from Core.MyObjects import *
from Core import Universals as uni
import FileUtils as fu
import logging

recordContents = ""
isSetedTitle = False
recordType = 0 # 0=Normal, 1=Debug
lastRecordType = 0

def create():
    global recordContents
    recordContents = str(translate("Records", "Hamsi Manager Record File - Time Created : ")) + str(time.strftime("%d.%m.%Y %H:%M:%S"))+"\n"

def setTitle(_title):
    global isSetedTitle, recordContents
    if "isSaveActions" not in uni.MySettings.keys() or uni.getBoolValue("isSaveActions"):
        recordContents += str(_title) + "\n"
    if uni.loggingLevel==logging.DEBUG:
        print (_title)
    isSetedTitle = True

def add(_action, _previous="", _now=None):
    global recordContents
    if "isSaveActions" not in uni.MySettings.keys() or uni.getBoolValue("isSaveActions"):
        if recordType==0 or (recordType==1 and uni.loggingLevel==logging.DEBUG):
            if _now is not None:
                recordContents += str(_action + " ::::::: '") + str(_previous) + "' >>>>>>>> '" + str(_now) + "' <<<<<<< " + str(time.strftime("%d.%m.%Y %H:%M:%S"))+"\n"
            else:
                recordContents += str(_action + " ::::::: '") + str(_previous) + "' " + str(time.strftime("%d.%m.%Y %H:%M:%S"))+"\n"
    if uni.loggingLevel==logging.DEBUG:
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
    if "isSaveActions" not in uni.MySettings.keys() or uni.getBoolValue("isSaveActions"):
        if fu.isFile(fu.recordFilePath)==False:
            create()
        setRecordType(1)
        fu.addToFile(fu.recordFilePath, recordContents)
        restoreRecordType()
    recordContents = ""
    isSetedTitle = False

def checkSize():
    setRecordType(1)
    if fu.isFile(fu.recordFilePath):
        if fu.getSize(fu.recordFilePath) > (int(uni.MySettings["maxRecordFileSize"])*1024):
            fu.moveFileOrDir(fu.recordFilePath, fu.joinPath(fu.oldRecordsDirectoryPath, str(time.strftime("%Y%m%d_%H%M%S")) + ".txt"))
    restoreRecordType()

def getBackupRecordsList():
    if fu.isDir(fu.oldRecordsDirectoryPath)==True:
        return fu.readDirectory(fu.oldRecordsDirectoryPath, "file")
    else:
        return []

def read(_recordFilePath=None):
    if _recordFilePath==None:
        _recordFilePath = fu.recordFilePath
    if fu.isFile(_recordFilePath)==True:
        return fu.readFromFile(_recordFilePath, "utf-8")
    else:
        create()
        setRecordType(1)
        fu.addToFile(_recordFilePath, recordContents)
        restoreRecordType()
        return recordContents

def clearRecords():
    fu.writeToFile(fu.recordFilePath, str(translate("Records", "Hamsi Manager Record File - Time Clear : ")) + str(time.strftime("%d.%m.%Y %H:%M:%S"))+"\n")



