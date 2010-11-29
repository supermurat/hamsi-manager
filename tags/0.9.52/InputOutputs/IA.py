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


import os
import shutil
import Variables
import Universals
import InputOutputs
import Settings
import Records
import Organizer
from Universals import translate

class IA:
    """Read and writes are arranged in this class"""
    global isFile, isDir, moveFileOrDir, listDir, makeDirs, removeDir, removeFile, getDirName, getBaseName, copyDirTree, readDirectory, moveOrChange, moveDir, readDirectoryWithSubDirectories, clearEmptyDirectories, clearUnneededs, clearIgnoreds, checkIcon, removeFileOrDir, changeDirectories, readTextFile, writeTextFile, clearPackagingDirectory, makePack, extractPack, copyOrChange, isExist, copyDirectory, isWritableFileOrDir, getRealDirName, checkSource, checkDestination, copyFileOrDir, readDirectoryAll, getObjectType
    global readFromFile, writeToFile, addToFile, readFromBinaryFile, writeToBinaryFile, readLinesFromFile, clearTempFiles, getFileTree, removeOnlySubFiles, getSize, fixToSize, clearCleaningDirectory, checkExtension, isDirEmpty, createSymLink, activateSmartCheckIcon, complateSmartCheckIcon, setIconToDirectory, getFirstImageInDirectory, isReadableFileOrDir, getHashDigest, createHashDigestFile, getIconFromDirectory, getRealPath
    
    def isFile(_oldPath):
        return InputOutputs.isFile(_oldPath)
    
    def isDir(_oldPath):
        return InputOutputs.isDir(_oldPath)
    
    def isDirEmpty(_oldPath):
        return InputOutputs.isDirEmpty(_oldPath)
        
    def isExist(_oldPath):
        return InputOutputs.isExist(_oldPath)
    
    def getSize(_oldPath):
        return InputOutputs.getSize(_oldPath)
    
    def getObjectType(_oldPath):
        return InputOutputs.getObjectType(_oldPath)
    
    def getDirName(_oldPath):
        return InputOutputs.getDirName(_oldPath)
    
    def getRealDirName(_oldPath, isGetParent=False):
        return InputOutputs.getRealDirName(_oldPath, isGetParent)
        
    def getRealPath(_path, _parentPath=None):
        return InputOutputs.getRealPath(_path, _parentPath)
    
    def getBaseName(_oldPath):
        return InputOutputs.getBaseName(_oldPath)
    
    def checkExtension(_oldPath, _extension):
        return InputOutputs.checkExtension(_oldPath, _extension)
    
    def moveFileOrDir(_oldPath, _newPath):
        return InputOutputs.moveFileOrDir(_oldPath, _newPath)
    
    def copyFileOrDir(_oldPath, _newPath):
        return InputOutputs.copyFileOrDir(_oldPath, _newPath)
            
    def copyDirTree(_oldPath, _newPath):
        return InputOutputs.copyDirTree(_oldPath, _newPath)
    
    def createSymLink(_oldPath, _newPath):
        return InputOutputs.createSymLink(_oldPath, _newPath)
      
    def listDir(_oldPath):
        if checkSource(_oldPath, "directory"):
            return InputOutputs.listDir(_oldPath)
        return []
        
    def makeDirs(_newPath):
        if isWritableFileOrDir(getRealDirName(_newPath)):
            return InputOutputs.makeDirs(_newPath)
        return False
        
    def removeDir(_oldPath):
        return InputOutputs.removeDir(_oldPath)
        
    def removeFile(_oldPath):
        return InputOutputs.removeFile(_oldPath)
    
    def isReadableFileOrDir(_newPath, _isOnlyCheck=False): 
        realPath = _newPath
        if InputOutputs.isReadableFileOrDir(realPath):
            return True
        if _isOnlyCheck==False:
            if isDir(realPath):
                import Dialogs
                Dialogs.showError(translate("InputOutputs", "Access Denied"),
                        str(translate("InputOutputs", "\"%s\" : you do not have the necessary permissions to read this directory.<br>Please check your access controls and retry.")) % Organizer.getLink(realPath))
            else:
                import Dialogs
                Dialogs.showError(translate("InputOutputs", "Access Denied"),
                        str(translate("InputOutputs", "\"%s\" : you do not have the necessary permissions to read this file.<br>Please check your access controls and retry.")) % Organizer.getLink(realPath))
        return False
        
    def isWritableFileOrDir(_newPath, _isOnlyCheck=False):
        realPath = _newPath
        if InputOutputs.isWritableFileOrDir(realPath):
            return True
        if _isOnlyCheck==False:
            if isDir(realPath):
                import Dialogs
                Dialogs.showError(translate("InputOutputs", "Access Denied"),
                        str(translate("InputOutputs", "\"%s\" : you do not have the necessary permissions to change this directory.<br>Please check your access controls and retry.")) % Organizer.getLink(realPath))
            else:
                import Dialogs
                Dialogs.showError(translate("InputOutputs", "Access Denied"),
                        str(translate("InputOutputs", "\"%s\" : you do not have the necessary permissions to change this file.<br>Please check your access controls and retry.")) % Organizer.getLink(realPath))
        return False
        
    def checkSource(_oldPath, _objectType="fileOrDirectory"):
        if InputOutputs.checkSource(_oldPath, _objectType)==False:
            if _objectType=="file":
                import Dialogs
                Dialogs.showError(translate("InputOutputs", "Cannot Find File"),
                        str(translate("InputOutputs", "\"%s\" : cannot find a file with this name.<br>Please make sure that it exists and retry.")) % Organizer.getLink(_oldPath))
            elif _objectType=="directory":
                import Dialogs
                Dialogs.showError(translate("InputOutputs", "Cannot Find Directory"),
                        str(translate("InputOutputs", "\"%s\" : cannot find a folder with this name.<br>Please make sure that it exists and retry.")) % Organizer.getLink(_oldPath))
            else:
                import Dialogs
                Dialogs.showError(translate("InputOutputs", "Cannot Find File Or Directory"),
                        str(translate("InputOutputs", "\"%s\" : cannot find a file or directory with this name.<br>Please make sure that it exists and retry.")) % Organizer.getLink(_oldPath))
            return False
        return _oldPath
        
    def checkDestination(_oldPath, _newPath, _isQuiet=False):
        if isExist(_newPath):
            if isWritableFileOrDir(_newPath):
                if _oldPath.lower()!=_newPath.lower() or Variables.osName=="posix": 
                    if isFile(_newPath):
                        if _isQuiet:
                            return _newPath
                        else:
                            import Dialogs
                            answer = Dialogs.ask(translate("InputOutputs", "Current File Name"),
                                        str(translate("InputOutputs", "\"%s\" : there already exists a file with the same name.<br>Replace it with the current one?")) % Organizer.getLink(_newPath))
                            if answer==Dialogs.Yes: 
                                return _newPath
                            else:
                                return False
                    elif isDir(_newPath):
                        if isFile(_oldPath):
                            import Dialogs
                            answer = Dialogs.ask(translate("InputOutputs", "Current Directory Name"),
                                    str(translate("InputOutputs", "\"%s\" : there already exists a folder with the same name.<br>\"%s\" Add this file to the current folder?")) % (Organizer.getLink(_newPath), Organizer.getLink(_newPath)))
                            if answer==Dialogs.Yes: 
                                return _newPath+"/"+getBaseName(_newPath)
                            else:
                                return False
                        else:
                            isAllowed=False
                            for tDir in InputOutputs.appendingDirectories:
                                if _newPath==tDir:
                                    isAllowed=True
                                    return _newPath
                            if isAllowed==False: 
                                if _isQuiet:
                                    InputOutputs.appendingDirectories.append(_newPath)
                                    return _newPath
                                else:
                                    import Dialogs
                                    answer = Dialogs.ask(translate("InputOutputs", "Current Directory Name"), 
                                            str(translate("InputOutputs", "\"%s\" : there already exists a folder with the same name.<br>Add your files to the current folder?")) % Organizer.getLink(_newPath))
                                    if answer==Dialogs.Yes:
                                        InputOutputs.appendingDirectories.append(_newPath)
                                        return _newPath
                                    else:
                                        return False
                    else:
                        return False
                else:
                    return _newPath
            else:
                return False
        else:
            if isWritableFileOrDir(getDirName(_newPath)):
                return _newPath
            else:
                return False
        return False
        
    def readDirectory(_path, _objectType="fileOrDirectory"):
        return InputOutputs.readDirectory(_path, _objectType)
    
    def readDirectoryAll(_path): 
        return InputOutputs.readDirectoryAll(_path)
  
    def readDirectoryWithSubDirectories(_path, _subDirectoryDeep=-1, _isGetDirectoryNames=False, _isOnlyDirectories=False, _currentSubDeep=0):
        return InputOutputs.readDirectoryWithSubDirectories(_path, _subDirectoryDeep, _isGetDirectoryNames, _isOnlyDirectories, _currentSubDeep)
    
    def readFromFile(_path):
        return InputOutputs.readFromFile(_path)
        
    def readLinesFromFile(_path):
        return InputOutputs.readLinesFromFile(_path)
        
    def readFromBinaryFile(_path):
        return InputOutputs.readFromBinaryFile(_path)
        
    def writeToFile(_path, _contents=""):
        return InputOutputs.writeToFile(_path, _contents)
        
    def writeToBinaryFile(_path, _contents=""):
        return InputOutputs.writeToBinaryFile(_path, _contents)
    
    def addToFile(_path, _contents=""):
        return InputOutputs.addToFile(_path, _contents)
    
    def readTextFile(_path):
        return InputOutputs.readTextFile(_path)
        
    def writeTextFile(_oldFileValues, _newFileValues, _charSet="utf-8"):
        return InputOutputs.writeTextFile(_oldFileValues, _newFileValues, _charSet)
                
    def clearEmptyDirectories(_path, _isShowState=False, _isCloseState=False, _isAutoCleanSubFolder=True):
        #If directory deleted : returned True
        #If directory cleaned : returned False
        if Universals.getBoolValue("isActiveClearGeneral"):
            import Dialogs
            clearUnneededs(_path)
            dontRemovingFilesCount = 0
            filesAndDirectories = readDirectoryAll(_path)
            for nameNo, name in enumerate(filesAndDirectories):
                if _isShowState: Dialogs.showState(translate("InputOutputs", "Checking Empty Directories"), nameNo, len(filesAndDirectories))
                if isFile(_path+"/"+name):
                    dontRemovingFilesCount+=1
                    if Universals.getBoolValue("isDeleteEmptyDirectories"):
                        for f in Universals.getListFromStrint(Universals.MySettings["ignoredFiles"]):
                            try:
                                if str(f)==name:
                                    dontRemovingFilesCount-=1
                                    break
                            except:pass
                        for ext in Universals.getListFromStrint(Universals.MySettings["ignoredFileExtensions"]):
                            try:
                                if checkExtension(name, ext):
                                    dontRemovingFilesCount-=1
                                    break
                            except:pass
                if isDir(_path+"/"+name):
                    dontRemovingFilesCount+=1
                    if _isAutoCleanSubFolder==False:
                        break
                    if Universals.getBoolValue("isDeleteEmptyDirectories"):
                        for f in Universals.getListFromStrint(Universals.MySettings["ignoredDirectories"]):
                            try:
                                if str(f)==name:
                                    dontRemovingFilesCount-=1
                                    break
                            except:pass
                    if clearEmptyDirectories(_path+"/"+name, _isShowState):
                        dontRemovingFilesCount-=1
            if dontRemovingFilesCount==0 and Universals.getBoolValue("isDeleteEmptyDirectories"):
                if _isShowState: Dialogs.showState(translate("InputOutputs", "Cleaning Empty Directories"), 0, 1)
                clearIgnoreds(_path)
                removeDir(_path)
                if _isCloseState: 
                    Dialogs.showState(translate("InputOutputs", "Directory Deleted"), 1, 1)
                    Dialogs.show(translate("InputOutputs", "Directory Deleted"), str(translate("InputOutputs", "\"%s\" deleted.Because this directory is empty.")) % Organizer.getLink(_path))
                return True
            if _isCloseState: Dialogs.showState(translate("InputOutputs", "Directories Cleaned"), 1, 1)
        return False
        
    def clearUnneededs(_path):
        if checkSource(_path, "directory"):
            for f in Universals.getListFromStrint(Universals.MySettings["unneededFiles"]):
                try:
                    if isFile(_path+"/"+str(unicode(f,"utf-8"))):
                        removeFile(_path+"/"+str(unicode(f,"utf-8")))
                except:pass
            for f in Universals.getListFromStrint(Universals.MySettings["unneededDirectoriesIfIsEmpty"]):
                try:
                    if isDirEmpty(_path+"/"+str(unicode(f,"utf-8"))) and f.strip()!="":
                        removeDir(_path+"/"+str(unicode(f,"utf-8")))
                except:pass
            for f in Universals.getListFromStrint(Universals.MySettings["unneededDirectories"]):
                try:
                    if isDir(_path+"/"+str(unicode(f,"utf-8"))) and f.strip()!="":
                        removeFileOrDir(_path+"/"+str(unicode(f,"utf-8")), True)
                except:pass
            for name in readDirectoryAll(_path):
                if isFile(_path+"/"+name):
                    for ext in Universals.getListFromStrint(Universals.MySettings["unneededFileExtensions"]):
                        try:
                            if checkExtension(name, ext):
                                removeFile(_path+"/"+name)
                        except:pass
                
    def clearIgnoreds(_path):
        if checkSource(_path, "directory"):
            for f in Universals.getListFromStrint(Universals.MySettings["ignoredFiles"]):
                try:
                    if isFile(_path+"/"+str(unicode(f,"utf-8"))):
                        removeFile(_path+"/"+str(unicode(f,"utf-8")))
                except:pass
            for f in Universals.getListFromStrint(Universals.MySettings["ignoredDirectories"]):
                try:
                    if isDir(_path+"/"+str(unicode(f,"utf-8"))) and f.strip()!="":
                        removeFileOrDir(_path+"/"+str(unicode(f,"utf-8")), True)
                except:pass
            for name in readDirectoryAll(_path):
                if isFile(_path+"/"+name):
                    for ext in Universals.getListFromStrint(Universals.MySettings["ignoredFileExtensions"]):
                        try:
                            if checkExtension(name, ext):
                                removeFile(_path+"/"+name)
                        except:pass
    
    def removeFileOrDir(_path, _isDir=False):
        if isWritableFileOrDir(getDirName(_path)):
            if _isDir==False:
                removeFile(_path)
            else:
                for f in readDirectoryAll(_path):
                    if isFile(_path+"/"+f):
                        removeFileOrDir(_path+"/"+f)
                    elif isDir(_path+"/"+f):
                        removeFileOrDir(_path+"/"+f, True)
                removeDir(_path)
    
    def removeOnlySubFiles(_path):
        if isWritableFileOrDir(_path):
            for f in readDirectoryAll(_path):
                if isFile(_path+"/"+f):
                    removeFile(_path+"/"+f)
                elif isDir(_path+"/"+f):
                    removeOnlySubFiles(_path+"/"+f)
    
    def moveOrChange(_oldPath, _newPath, _objectType="file", _actionType="auto", _isQuiet=False):
        _oldPath, _newPath = str(_oldPath), str(_newPath)
        isChange=False
        if checkSource(_oldPath, _objectType):
            isChange=True
            _newPath = checkDestination(_oldPath, _newPath, _isQuiet)
        if isChange==True and _newPath:
            if _objectType=="directory" and _actionType=="auto":
                if Universals.getBoolValue("isClearEmptyDirectoriesWhenMoveOrChange"):
                    if clearEmptyDirectories(_oldPath, True, True, Universals.getBoolValue("isAutoCleanSubFolderWhenMoveOrChange")):
                        return False
            for tDir in InputOutputs.appendingDirectories:
                if _newPath==tDir:
                    for name in readDirectoryAll(_oldPath):
                        name = str(name)
                        if isDir(_oldPath+"/"+name):
                            moveOrChange(_oldPath+"/"+name, _newPath+"/"+name, "directory", _actionType, _isQuiet)
                        else:
                            moveOrChange(_oldPath+"/"+name, _newPath+"/"+name, "file", _actionType, _isQuiet)
                    isChange = False
            if isChange==True:
                moveFileOrDir(_oldPath,_newPath)
            if _objectType=="directory" and _actionType=="auto":
                if Universals.getBoolValue("isClearEmptyDirectoriesWhenMoveOrChange"):
                    if clearEmptyDirectories(_newPath, True, True, Universals.getBoolValue("isAutoCleanSubFolderWhenMoveOrChange")):
                        return getBaseName(_newPath)
            if isDir(_newPath)==True and _actionType=="auto":
                if Universals.getBoolValue("isAutoMakeIconToDirectoryWhenMoveOrChange"):
                    checkIcon(_newPath)
            elif _actionType=="auto":
                if Universals.getBoolValue("isAutoMakeIconToDirectoryWhenFileMove"):
                    if isDir(getDirName(_oldPath)):
                        checkIcon(getDirName(_oldPath))
                    if isDir(getDirName(_newPath)):
                        checkIcon(getDirName(_newPath))
            return getBaseName(_newPath)
        else:
            return False
            
    def copyOrChange(_oldPath,_newPath,_objectType="file", _actionType="auto", _isQuiet=False):
        _oldPath, _newPath = str(_oldPath), str(_newPath)
        isChange=False
        if checkSource(_oldPath, _objectType):
            isChange=True
            _newPath = checkDestination(_oldPath, _newPath, _isQuiet)
        if isChange==True and _newPath:
            if _objectType=="directory" and _actionType=="auto":
                if Universals.getBoolValue("isClearEmptyDirectoriesWhenCopyOrChange"):
                    if clearEmptyDirectories(_oldPath, True, True, Universals.getBoolValue("isAutoCleanSubFolderWhenCopyOrChange")):
                        return False
            for tDir in InputOutputs.appendingDirectories:
                if _newPath==tDir:
                    for name in readDirectoryAll(_oldPath):
                        if isDir(_oldPath+"/"+name):
                            copyOrChange(_oldPath+"/"+name, _newPath+"/"+name, "directory", _actionType, _isQuiet)
                        else:
                            copyOrChange(_oldPath+"/"+name, _newPath+"/"+name, "file", _actionType, _isQuiet)
                    isChange = False
            if isChange==True:
                copyFileOrDir(_oldPath,_newPath)
            if isDir(_newPath)==True and _actionType=="auto":
                if Universals.getBoolValue("isAutoMakeIconToDirectoryWhenCopyOrChange"):
                    checkIcon(_newPath)
            return getBaseName(_newPath)
        else:
            return False
    
    def changeDirectories(_values):
        #will return directory(new) name
        import Dialogs
        if len(_values)!=0:
            Dialogs.showState(translate("InputOutputs", "Changing The Folder (Of The Files)"),0,len(_values))
            for no in range(0,len(_values)):
                moveOrChange(_values[no][0], _values[no][1], getObjectType(_values[no][0]))
                Dialogs.showState(translate("InputOutputs", "Changing The Folder (Of The Files)"),no+1,len(_values))
            if Universals.getBoolValue("isClearEmptyDirectoriesWhenFileMove"):
                if isDir(InputOutputs.currentDirectoryPath):
                    if clearEmptyDirectories(InputOutputs.currentDirectoryPath, True, True, Universals.getBoolValue("isAutoCleanSubFolderWhenFileMove")):
                        return getDirName(InputOutputs.currentDirectoryPath)
            if Universals.getBoolValue("isAutoMakeIconToDirectoryWhenFileMove"):
                if isDir(InputOutputs.currentDirectoryPath):
                    checkIcon(InputOutputs.currentDirectoryPath)
        return InputOutputs.currentDirectoryPath
        
    def activateSmartCheckIcon():
        InputOutputs.isSmartCheckIcon = True
        InputOutputs.willCheckIconDirectories = []
    
    def complateSmartCheckIcon():
        InputOutputs.isSmartCheckIcon = False
        for iconDir in InputOutputs.willCheckIconDirectories:
            checkIcon(iconDir)
        InputOutputs.willCheckIconDirectories = []
    
    def checkIcon(_path, _isClear=False):
        if InputOutputs.isSmartCheckIcon and _isClear==False:
            if InputOutputs.willCheckIconDirectories.count(_path)==0:
                InputOutputs.willCheckIconDirectories.append(_path)
        else:
            if _isClear==False:
                coverPath = _path + "/" + getFirstImageInDirectory(_path)
                return setIconToDirectory(_path, coverPath)
            elif _isClear:
                return setIconToDirectory(_path)
    
    def getFirstImageInDirectory(_path, _coverNameIfExist=None, _isCheckDelete=False, _isAsk=True):
        import Dialogs
        _path = str(_path)
        cover = None
        imageFiles = []
        if isReadableFileOrDir(_path, True):
            for fileName in readDirectoryAll(_path):
                if isFile(_path + "/" + fileName):
                    if str(fileName.split(".")[0]).lower()==str(_coverNameIfExist).lower():
                        cover = fileName
                    if Universals.getListFromStrint(Universals.MySettings["imageExtensions"]).count((fileName.split(".")[-1]).lower()) != 0:
                        imageFiles.append(fileName)
                        if cover == None:
                            for coverName in Universals.getListFromStrint(Universals.MySettings["priorityIconNames"]):
                                if str(fileName.split(".")[0]).lower()==str(coverName).lower():
                                    cover = fileName
                                    break
            if _isAsk and eval(Universals.MySettings["isAskIfHasManyImagesInAlbumDirectory"].title())==True and len(imageFiles)>1:
                selectedIndex = 0
                if cover!=None:
                    selectedIndex = imageFiles.index(cover)
                cover = Dialogs.select(translate("InputOutputs", "Select A Cover"), str(translate("InputOutputs", "Please select a cover for \"%s\".")) % (Organizer.getLink(_path)), imageFiles, selectedIndex)
                if cover!=None:
                    cover = str(cover)
            else:
                if cover == None and len(imageFiles)>0:
                    for imgFile in imageFiles:
                        cover = imgFile
                        break
            if _isCheckDelete and cover!=None:
                if isWritableFileOrDir(_path):
                    if eval(Universals.MySettings["isDeleteOtherImages"].title())==True: 
                        for imgFile in imageFiles:
                            if cover != imgFile:
                                removeFile(_path + "/" + imgFile)
        return cover
        
    def setIconToDirectory(_path, _iconName=""):
        return InputOutputs.setIconToDirectory(_path, _iconName)
        
    def getIconFromDirectory(_path):
        return InputOutputs.getIconFromDirectory(_path)

    def clearPackagingDirectory(_path, _isShowState=False, _isCloseState=False):
        import Dialogs
        if checkSource(_path, "directory"):
            _path = str(_path)
            if Universals.getBoolValue("isClearEmptyDirectoriesWhenPath"):
                clearEmptyDirectories(_path, _isShowState, _isShowState, Universals.getBoolValue("isAutoCleanSubFolderWhenPath"))
            for f in Universals.getListFromStrint(Universals.MySettings["packagerUnneededFiles"]):
                if isFile(_path+"/"+f):
                    removeFile(_path+"/"+f)
            for d in Universals.getListFromStrint(Universals.MySettings["packagerUnneededDirectories"]):
                if isExist(_path+"/"+d):
                    removeFileOrDir(_path+"/"+d, True)
            dontRemovingFilesCount = 0
            filesAndDirectories = readDirectoryAll(_path)
            for nameNo, name in enumerate(filesAndDirectories):
                if _isShowState: Dialogs.showState(translate("InputOutputs", "Checking Empty Directories"), nameNo, len(filesAndDirectories))
                if isFile(_path+"/"+name):
                    dontRemovingFilesCount+=1
                    for ext in Universals.getListFromStrint(Universals.MySettings["packagerUnneededFileExtensions"]):
                        try:
                            if checkExtension(name, ext):
                                removeFile(_path+"/"+name)
                                dontRemovingFilesCount-=1
                                continue
                        except:pass
                    try:
                        if name[-1:]=="~":
                            removeFile(_path+"/"+name)
                            dontRemovingFilesCount-=1
                            continue
                    except:pass
                if isDir(_path+"/"+name):
                    dontRemovingFilesCount+=1
                    if clearPackagingDirectory(_path+"/"+name)==False:
                        dontRemovingFilesCount-=1
            if dontRemovingFilesCount==0 and Universals.getBoolValue("isPackagerDeleteEmptyDirectories"):
                if _isShowState: Dialogs.showState(translate("InputOutputs", "Deleting Empty Directories"), 0, 1)
                removeDir(_path)
                if _isCloseState: 
                    Dialogs.showState(translate("InputOutputs", "Empty Directories Deleted"), 1, 1)
                    Dialogs.show(translate("InputOutputs", "Project Directory Deleted"), str("InputOutputs", translate("\"%s\" deleted.Because this directory is empty.")) % Organizer.getLink(_path))
                return False
            if _isCloseState: Dialogs.showState(translate("InputOutputs", "Empty Directories Deleted"), 1, 1)
            return True
        else:
            False
            
    def clearCleaningDirectory(_path, _isShowState=False, _isCloseState=False):
        import Dialogs
        if checkSource(_path, "directory"):
            _path = str(_path)
            if Universals.getBoolValue("isClearEmptyDirectoriesWhenClear"):
                clearEmptyDirectories(_path, _isShowState, _isShowState, Universals.getBoolValue("isAutoCleanSubFolderWhenClear"))
            for f in Universals.getListFromStrint(Universals.MySettings["cleanerUnneededFiles"]):
                if isFile(_path+"/"+f):
                    removeFile(_path+"/"+f)
            for d in Universals.getListFromStrint(Universals.MySettings["cleanerUnneededDirectories"]):
                if isExist(_path+"/"+d):
                    removeFileOrDir(_path+"/"+d, True)
            dontRemovingFilesCount = 0
            filesAndDirectories = readDirectoryAll(_path)
            for nameNo, name in enumerate(filesAndDirectories):
                if _isShowState: Dialogs.showState(translate("InputOutputs", "Checking Empty Directories"), nameNo, len(filesAndDirectories))
                if isFile(_path+"/"+name):
                    dontRemovingFilesCount+=1
                    for ext in Universals.getListFromStrint(Universals.MySettings["cleanerUnneededFileExtensions"]):
                        try:
                            if checkExtension(name, ext):
                                removeFile(_path+"/"+name)
                                dontRemovingFilesCount-=1
                                continue
                        except:pass
                    try:
                        if name[-1:]=="~":
                            removeFile(_path+"/"+name)
                            dontRemovingFilesCount-=1
                            continue
                    except:pass
                if isDir(_path+"/"+name):
                    dontRemovingFilesCount+=1
                    if clearPackagingDirectory(_path+"/"+name)==False:
                        dontRemovingFilesCount-=1
            if dontRemovingFilesCount==0 and Universals.getBoolValue("isCleanerDeleteEmptyDirectories"):
                if _isShowState: Dialogs.showState(translate("InputOutputs", "Deleting Empty Directories"), 0, 1)
                removeDir(_path)
                if _isCloseState: 
                    Dialogs.showState(translate("InputOutputs", "Empty Directories Deleted"), 1, 1)
                    Dialogs.show(translate("InputOutputs", "Project Directory Deleted"), str("InputOutputs", translate("\"%s\" deleted.Because this directory is empty.")) % Organizer.getLink(_path))
                return False
            if _isCloseState: Dialogs.showState(translate("InputOutputs", "Project Directory Cleaned"), 1, 1)
            return True
        else:
            False

    def makePack(_filePath, _packageType, _sourcePath):
        import Dialogs
        _filePath, _sourcePath = str(_filePath), str(_sourcePath)
        if isDir(_filePath):
            Dialogs.showError(translate("InputOutputs", "Current Directory Name"),
                        str(translate("InputOutputs", "\"%s\" : there already exists a folder with the same name.<br>Please choose another file name!")) % Organizer.getLink(_filePath))
            return False
        return InputOutputs.makePack(_filePath, _packageType, _sourcePath)
        
    def extractPack(_oldPath, _newPath):
        return InputOutputs.extractPack(_oldPath, _newPath)
        
    def clearTempFiles():
        import tempfile
        for fileName in readDirectoryAll(tempfile.gettempdir()):
            if fileName[:15] == "HamsiManager":
                if isDir(tempfile.gettempdir()+"/"+fileName):
                    removeFileOrDir(tempfile.gettempdir()+"/"+fileName, True)
                else:
                    removeFileOrDir(tempfile.gettempdir()+"/"+fileName)
                    
    def getFileTree(_path, _subDirectoryDeep=-1, _actionType="return", _formatType="html", _extInfo="no"):
        info = InputOutputs.getFileTree(_path, _subDirectoryDeep, _formatType, _extInfo)
        info = Organizer.showWithIncorrectChars(info)
        if _actionType=="return":
            return info
        elif _actionType=="file":
            from MyObjects import MFileDialog
            import Dialogs
            if _formatType=="html":
                if _extInfo!="no":
                    strHeader = ("<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Strict//EN\" \n"+
                        "\"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd\"> \n"+
                        "<html xmlns=\"http://www.w3.org/1999/xhtml\" xml:lang=\"tr\" lang=\"tr\" dir=\"ltr\"> \n"+
                        "<head> \n<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" /> \n</head> \n<body> \n")
                    strFooter = " \n</body> \n</html>"
                    info = strHeader + info + strFooter
                formatTypeName = translate("Tables", "HTML")
                fileExt="html"
            elif _formatType=="plainText":
                formatTypeName = translate("Tables", "Plain Text")
                fileExt="txt"
            filePath = MFileDialog.getSaveFileName(Universals.MainWindow,translate("Tables", "Save As"),
                                    Variables.userDirectoryPath.decode("utf-8"),formatTypeName+(" (*."+fileExt).decode("utf-8")+")")
            if filePath!="":
                filePath = unicode(filePath, "utf-8")
                if _formatType=="html" and filePath[-5:]!=".html":
                    filePath += ".html"
                elif _formatType=="plainText" and filePath[-4:]!=".txt":
                    filePath += ".txt"
                writeToFile(filePath, info)
                Dialogs.show(translate("Tables", "File Tree Created"),
                            str(translate("Tables", "File tree created in file: \"%s\".")) % Organizer.getLink(filePath))
        elif _actionType=="dialog":
            from MyObjects import MDialog, MWidget, MVBoxLayout, MTextEdit, MPushButton, MObject, SIGNAL, getMyObject
            dDialog = MDialog(Universals.MainWindow)
            if Universals.isActivePyKDE4==True:
                dDialog.setButtons(MDialog.None)
            dDialog.setWindowTitle(translate("Tables", "File Tree"))
            mainPanel = MWidget(dDialog)
            vblMain = MVBoxLayout(mainPanel)
            if _formatType=="html":
                QtWebKit = getMyObject("QtWebKit")
                wvWeb = QtWebKit.QWebView()
                wvWeb.setHtml(info.decode("utf-8"))
            elif _formatType=="plainText":
                wvWeb = MTextEdit()
                wvWeb.setPlainText(info.decode("utf-8"))
            pbtnClose = MPushButton(translate("Tables", "OK"))
            MObject.connect(pbtnClose, SIGNAL("clicked()"), dDialog.close)
            vblMain.addWidget(wvWeb)
            vblMain.addWidget(pbtnClose)
            if Universals.isActivePyKDE4==True:
                dDialog.setMainWidget(mainPanel)
            else:
                dDialog.setLayout(vblMain)
            dDialog.setMinimumWidth(600)
            dDialog.setMinimumHeight(400)
            dDialog.show()
        elif _actionType=="clipboard":
            from MyObjects import MApplication
            MApplication.clipboard().setText(info.decode("utf-8"))
            
    def fixToSize(_path, _size, _clearFrom="head"):
        return InputOutputs.fixToSize(_path, _size, _clearFrom)
            
    def getHashDigest(_filePath, _hashType="MD5"):
        return InputOutputs.getHashDigest(_filePath, _hashType)
        
    def createHashDigestFile(_filePath, _digestFilePath=None, _hashType="MD5", _isAddFileExtension=True, _digestContent=None):
        return InputOutputs.createHashDigestFile(_filePath, _digestFilePath, _hashType, _isAddFileExtension, _digestContent)
        
        
        
