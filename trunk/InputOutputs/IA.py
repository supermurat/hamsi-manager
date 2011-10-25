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
from Core import Variables
from Core import Universals
import InputOutputs
from Core import Records
from Core import Organizer
from Core.Universals import translate

class IA:
    """Read and writes are arranged in this class"""
    global isFile, isDir, moveFileOrDir, listDir, makeDirs, removeDir, removeFile, getDirName, getBaseName, copyDirTree, readDirectory, moveOrChange, moveDir, readDirectoryWithSubDirectories, clearEmptyDirectories, clearUnneededs, clearIgnoreds, checkIcon, removeFileOrDir, changeDirectories, readTextFile, writeTextFile, clearPackagingDirectory, makePack, extractPack, copyOrChange, isExist, copyDirectory, isWritableFileOrDir, getRealDirName, checkSource, checkDestination, copyFileOrDir, readDirectoryAll, getObjectType, isAvailableName
    global readFromFile, writeToFile, addToFile, readFromBinaryFile, writeToBinaryFile, readLinesFromFile, clearTempFiles, getFileTree, removeOnlySubFiles, getSize, fixToSize, clearCleaningDirectory, checkExtension, isDirEmpty, createSymLink, activateSmartCheckIcon, completeSmartCheckIcon, setIconToDirectory, getFirstImageInDirectory, isReadableFileOrDir, getHashDigest, createHashDigestFile, getIconFromDirectory, getRealPath
    
    def isFile(_oldPath):
        return InputOutputs.isFile(_oldPath)
    
    def isDir(_oldPath):
        return InputOutputs.isDir(_oldPath)
    
    def isDirEmpty(_oldPath):
        return InputOutputs.isDirEmpty(_oldPath)
        
    def isExist(_oldPath):
        return InputOutputs.isExist(_oldPath)    
        
    def isAvailableName(_newPath):
        return InputOutputs.isAvailableName(_newPath) 
    
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
    
    def isReadableFileOrDir(_newPath, _isOnlyCheck=False, _isInLoop=False): 
        realPath = _newPath
        if InputOutputs.isReadableFileOrDir(realPath):
            return True
        if _isOnlyCheck==False:
            if _isInLoop:
                okButtonLabel = translate("Dialogs", "Continue")
            else:
                okButtonLabel = translate("Dialogs", "OK")
            if isDir(realPath):
                from Core import Dialogs
                answer = Dialogs.askSpecial(translate("InputOutputs", "Access Denied"), 
                        str(translate("InputOutputs", "\"%s\" : you do not have the necessary permissions to read this directory.<br>Please check your access controls and retry.")) % Organizer.getLink(realPath), 
                            okButtonLabel, 
                            translate("Dialogs", "Retry"))
                if answer==translate("Dialogs", "Retry"):
                    return isReadableFileOrDir(_newPath, _isOnlyCheck, _isInLoop)
            else:
                from Core import Dialogs
                answer = Dialogs.askSpecial(translate("InputOutputs", "Access Denied"), 
                        str(translate("InputOutputs", "\"%s\" : you do not have the necessary permissions to read this file.<br>Please check your access controls and retry.")) % Organizer.getLink(realPath), 
                            okButtonLabel, 
                            translate("Dialogs", "Retry"))
                if answer==translate("Dialogs", "Retry"):
                    return isReadableFileOrDir(_newPath, _isOnlyCheck, _isInLoop)
        return False
        
    def isWritableFileOrDir(_newPath, _isOnlyCheck=False, _isInLoop=False):
        realPath = _newPath
        if InputOutputs.isWritableFileOrDir(realPath):
            return True
        if _isOnlyCheck==False:
            if _isInLoop:
                okButtonLabel = translate("Dialogs", "Continue")
            else:
                okButtonLabel = translate("Dialogs", "OK")
            if isDir(realPath):
                from Core import Dialogs
                answer = Dialogs.askSpecial(translate("InputOutputs", "Access Denied"), 
                        str(translate("InputOutputs", "\"%s\" : you do not have the necessary permissions to change this directory.<br>Please check your access controls and retry.")) % Organizer.getLink(realPath), 
                            okButtonLabel, 
                            translate("Dialogs", "Retry"))
                if answer==translate("Dialogs", "Retry"):
                    return isWritableFileOrDir(_newPath, _isOnlyCheck, _isInLoop)
            else:
                from Core import Dialogs
                answer = Dialogs.askSpecial(translate("InputOutputs", "Access Denied"), 
                        str(translate("InputOutputs", "\"%s\" : you do not have the necessary permissions to change this file.<br>Please check your access controls and retry.")) % Organizer.getLink(realPath), 
                            okButtonLabel, 
                            translate("Dialogs", "Retry"))
                if answer==translate("Dialogs", "Retry"):
                    return isWritableFileOrDir(_newPath, _isOnlyCheck, _isInLoop)
        return False
        
    def checkSource(_oldPath, _objectType="fileOrDirectory"):
        if InputOutputs.checkSource(_oldPath, _objectType)==False:
            if _objectType=="file":
                from Core import Dialogs
                Dialogs.showError(translate("InputOutputs", "Cannot Find File"),
                        str(translate("InputOutputs", "\"%s\" : cannot find a file with this name.<br>Please make sure that it exists and retry.")) % Organizer.getLink(_oldPath))
            elif _objectType=="directory":
                from Core import Dialogs
                Dialogs.showError(translate("InputOutputs", "Cannot Find Directory"),
                        str(translate("InputOutputs", "\"%s\" : cannot find a folder with this name.<br>Please make sure that it exists and retry.")) % Organizer.getLink(_oldPath))
            else:
                from Core import Dialogs
                Dialogs.showError(translate("InputOutputs", "Cannot Find File Or Directory"),
                        str(translate("InputOutputs", "\"%s\" : cannot find a file or directory with this name.<br>Please make sure that it exists and retry.")) % Organizer.getLink(_oldPath))
            return False
        return _oldPath
        
    def checkDestination(_oldPath, _newPath, _isQuiet=False):
        while isAvailableName(_newPath) == False:
            from Core import Dialogs
            _newPath = Dialogs.getText(translate("InputOutputs", "Unavailable Name"),
                                        str(translate("InputOutputs", "\"%s\" : can not encoded by %s.<br>Please review and correct the name!<br>You can correct your file system encoding name in Options/Advanced, If you want.<br>You can click cancel to cancel this action.")) % (_newPath, InputOutputs.fileSystemEncoding), _newPath)
            if _newPath is None:
                return False
        if isExist(_newPath):
            if isWritableFileOrDir(_newPath):
                if _oldPath.lower()!=_newPath.lower() or Variables.osName=="posix": 
                    if isFile(_newPath):
                        if _isQuiet:
                            return _newPath
                        else:
                            from Core import Dialogs
                            answer = Dialogs.askSpecial(translate("InputOutputs", "Current File Name"),
                                        str(translate("InputOutputs", "\"%s\" : there already exists a file with the same name.<br>Replace it with the current one?")) % Organizer.getLink(_newPath), 
                                translate("Dialogs", "Replace"), 
                                translate("Dialogs", "Rename"), 
                                translate("Dialogs", "Cancel"))
                            if answer==translate("Dialogs", "Replace"): 
                                return _newPath
                            elif answer==translate("Dialogs", "Rename"): 
                                from Core.MyObjects import MFileDialog, trForM, trForUI
                                newPath = MFileDialog.getSaveFileName(Universals.MainWindow, translate("InputOutputs", "Select A New Name For File"),
                                                        trForM(_newPath),trForUI(translate("InputOutputs", "All Files") + " (*)"))
                                if newPath!="":
                                    return checkDestination(_oldPath, str(newPath), _isQuiet)
                                return False
                            else:
                                return False
                    elif isDir(_newPath):
                        if isFile(_oldPath):
                            from Core import Dialogs
                            answer = Dialogs.askSpecial(translate("InputOutputs", "Current Directory Name"),
                                    str(translate("InputOutputs", "\"%s\" : there already exists a folder with the same name.<br>\"%s\" Add this file to the current folder?")) % (Organizer.getLink(_newPath), Organizer.getLink(_newPath)), 
                                translate("Dialogs", "Yes, Add Into"), 
                                translate("Dialogs", "Rename"), 
                                translate("Dialogs", "Cancel"))
                            if answer==translate("Dialogs", "Yes, Add Into"): 
                                return _newPath+"/"+getBaseName(_newPath)
                            elif answer==translate("Dialogs", "Rename"): 
                                from Core.MyObjects import MFileDialog, trForM, trForUI
                                newPath = MFileDialog.getSaveFileName(Universals.MainWindow, translate("InputOutputs", "Select A New Name For File"),
                                                        trForM(_newPath),trForUI(translate("InputOutputs", "All Files") + " (*)"))
                                if newPath!="":
                                    return checkDestination(_oldPath, str(newPath), _isQuiet)
                                return False
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
                                    from Core import Dialogs
                                    answer = Dialogs.askSpecial(translate("InputOutputs", "Current Directory Name"), 
                                            str(translate("InputOutputs", "\"%s\" : there already exists a directory with the same name.<br>Add your files to the current directory?")) % Organizer.getLink(_newPath), 
                                        translate("Dialogs", "Yes, Add Into"), 
                                        translate("Dialogs", "Rename"), 
                                        translate("Dialogs", "Cancel"))
                                    if answer==translate("Dialogs", "Yes, Add Into"):
                                        InputOutputs.appendingDirectories.append(_newPath)
                                        return _newPath
                                    elif answer==translate("Dialogs", "Rename"): 
                                        from Core.MyObjects import MFileDialog, trForM, trForUI
                                        newPath = MFileDialog.getExistingDirectory(Universals.MainWindow, translate("InputOutputs", "Select A Directory"),
                                                trForM(_newPath))
                                        if newPath!="":
                                            return checkDestination(_oldPath, str(newPath), _isQuiet)
                                        return False
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
        
    def readDirectory(_path, _objectType="fileOrDirectory", _isShowHiddens=False):
        return InputOutputs.readDirectory(_path, _objectType, _isShowHiddens)
    
    def readDirectoryAll(_path): 
        return InputOutputs.readDirectoryAll(_path)
  
    def readDirectoryWithSubDirectories(_path, _subDirectoryDeep=-1, _isGetDirectoryNames=False, _isOnlyDirectories=False, _isShowHiddens=False, _currentSubDeep=0):
        return InputOutputs.readDirectoryWithSubDirectories(_path, _subDirectoryDeep, _isGetDirectoryNames, _isOnlyDirectories, _isShowHiddens, _currentSubDeep)
    
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
                
    def clearEmptyDirectories(_path, _isShowState=False, _isCloseState=False, _isAutoCleanSubFolder=True, _isClear=False):
        #If directory deleted : returned True
        #If directory cleaned : returned False
        if Universals.getBoolValue("isActiveClearGeneral") or _isClear:
            from Core import Dialogs
            clearUnneededs(_path)
            dontRemovingFilesCount = 0
            filesAndDirectories = readDirectoryAll(_path)
            filesAndDirectoriesCount = len(filesAndDirectories)
            if _isShowState and _isCloseState:Universals.startThreadAction()
            for nameNo, name in enumerate(filesAndDirectories):
                if _isShowState:isContinueThreadAction = Universals.isContinueThreadAction()
                else: isContinueThreadAction = True
                if isContinueThreadAction:
                    if _isShowState: Dialogs.showState(translate("InputOutputs", "Checking Empty Directories"), nameNo, filesAndDirectoriesCount, True)
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
                        if clearEmptyDirectories(_path+"/"+name, _isShowState, False, _isAutoCleanSubFolder, _isClear):
                            dontRemovingFilesCount-=1
                else:
                    if _isShowState: Dialogs.showState(translate("InputOutputs", "Checked Empty Directories"), filesAndDirectoriesCount, filesAndDirectoriesCount, True)
            if _isShowState and _isCloseState:Universals.finishThreadAction()
            if dontRemovingFilesCount==0 and Universals.getBoolValue("isDeleteEmptyDirectories"):
                if _isShowState: Dialogs.showState(translate("InputOutputs", "Cleaning Empty Directories"), 0, 1, True)
                clearIgnoreds(_path)
                removeDir(_path)
                if _isCloseState: 
                    Dialogs.showState(translate("InputOutputs", "Directory Deleted"), 1, 1, True)
                    Dialogs.show(translate("InputOutputs", "Directory Deleted"), str(translate("InputOutputs", "\"%s\" deleted.Because this directory is empty.")) % Organizer.getLink(_path))
                return True
            if _isCloseState: Dialogs.showState(translate("InputOutputs", "Directories Cleaned"), 1, 1, True)
        return False
        
    def clearUnneededs(_path):
        if checkSource(_path, "directory"):
            for f in Universals.getListFromStrint(Universals.MySettings["unneededFiles"]):
                try:
                    if isFile(_path+"/"+str(f)):
                        removeFile(_path+"/"+str(f))
                except:pass
            for f in Universals.getListFromStrint(Universals.MySettings["unneededDirectoriesIfIsEmpty"]):
                try:
                    if isDirEmpty(_path+"/"+str(f)) and f.strip()!="":
                        removeDir(_path+"/"+str(f))
                except:pass
            for f in Universals.getListFromStrint(Universals.MySettings["unneededDirectories"]):
                try:
                    if isDir(_path+"/"+str(f)) and f.strip()!="":
                        removeFileOrDir(_path+"/"+str(f), True)
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
                    if isFile(_path+"/"+str(f)):
                        removeFile(_path+"/"+str(f))
                except:pass
            for f in Universals.getListFromStrint(Universals.MySettings["ignoredDirectories"]):
                try:
                    if isDir(_path+"/"+str(f)) and f.strip()!="":
                        removeFileOrDir(_path+"/"+str(f), True)
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
                        return _oldPath
            for tDir in InputOutputs.appendingDirectories:
                if _newPath==tDir:
                    for name in readDirectoryAll(_oldPath):
                        moveOrChange(_oldPath+"/"+name, _newPath+"/"+name, getObjectType(_oldPath+"/"+name), _actionType, _isQuiet)
                    isChange = False
            if isChange==True:
                moveFileOrDir(_oldPath,_newPath)
            if _objectType=="directory" and _actionType=="auto":
                if Universals.getBoolValue("isClearEmptyDirectoriesWhenMoveOrChange"):
                    if clearEmptyDirectories(_newPath, True, True, Universals.getBoolValue("isAutoCleanSubFolderWhenMoveOrChange")):
                        return _newPath
            if isDir(_newPath)==True and _actionType=="auto":
                if Universals.getBoolValue("isActiveAutoMakeIconToDirectory") and Universals.getBoolValue("isAutoMakeIconToDirectoryWhenMoveOrChange"):
                    checkIcon(_newPath)
            elif _actionType=="auto":
                if Universals.getBoolValue("isActiveAutoMakeIconToDirectory") and Universals.getBoolValue("isAutoMakeIconToDirectoryWhenFileMove"):
                    if isDir(getDirName(_oldPath)):
                        checkIcon(getDirName(_oldPath))
                    if isDir(getDirName(_newPath)):
                        checkIcon(getDirName(_newPath))
            return _newPath
        else:
            return _oldPath
            
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
                        return _oldPath
            for tDir in InputOutputs.appendingDirectories:
                if _newPath==tDir:
                    for name in readDirectoryAll(_oldPath):
                        copyOrChange(_oldPath+"/"+name, _newPath+"/"+name, getObjectType(_oldPath+"/"+name), _actionType, _isQuiet)
                    isChange = False
            if isChange==True:
                copyFileOrDir(_oldPath,_newPath)
            if isDir(_newPath)==True and _actionType=="auto":
                if Universals.getBoolValue("isActiveAutoMakeIconToDirectory") and Universals.getBoolValue("isAutoMakeIconToDirectoryWhenCopyOrChange"):
                    checkIcon(_newPath)
            return _newPath
        else:
            return _oldPath
    
    def changeDirectories(_values):
        newFilesPath = []
        from Core import Dialogs
        if len(_values)!=0:
            Dialogs.showState(translate("InputOutputs", "Changing The Folder (Of The Files)"),0,len(_values))
            for no in range(0,len(_values)):
                values = {}
                values["oldPath"] = _values[no][0]
                values["newPath"] = moveOrChange(values["oldPath"], _values[no][1], getObjectType(_values[no][0]))
                newFilesPath.append(values)
                dirPath = getDirName(newFilesPath[-1])
                if Universals.getBoolValue("isClearEmptyDirectoriesWhenFileMove"):
                    clearEmptyDirectories(dirPath, True, True, Universals.getBoolValue("isAutoCleanSubFolderWhenFileMove"))
                if Universals.getBoolValue("isActiveAutoMakeIconToDirectory") and Universals.getBoolValue("isAutoMakeIconToDirectoryWhenFileMove"):
                    checkIcon(dirPath)
                Dialogs.showState(translate("InputOutputs", "Changing The Folder (Of The Files)"),no+1,len(_values))
        return newFilesPath
        
    def activateSmartCheckIcon():
        InputOutputs.isSmartCheckIcon = True
        InputOutputs.willCheckIconDirectories = []
    
    def completeSmartCheckIcon():
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
                coverPath = ""
                coverName = getFirstImageInDirectory(_path)
                if coverName!=None:
                    coverPath = _path + "/" + coverName
                return setIconToDirectory(_path, coverPath)
            elif _isClear:
                return setIconToDirectory(_path)
    
    def getFirstImageInDirectory(_path, _coverNameIfExist=None, _isCheckDelete=False, _isAsk=True):
        from Core import Dialogs
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
                cover = Dialogs.getItem(translate("InputOutputs", "Select A Cover"), str(translate("InputOutputs", "Please select a cover for \"%s\".")) % (Organizer.getLink(_path)), imageFiles, selectedIndex)
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
        from Core import Dialogs
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
        from Core import Dialogs
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

    def makePack(_filePath, _packageType, _sourcePath, _realSourceBaseName):
        from Core import Dialogs
        _filePath, _sourcePath = str(_filePath), str(_sourcePath)
        if isDir(_filePath):
            Dialogs.showError(translate("InputOutputs", "Current Directory Name"),
                        str(translate("InputOutputs", "\"%s\" : there already exists a folder with the same name.<br>Please choose another file name!")) % Organizer.getLink(_filePath))
            return False
        return InputOutputs.makePack(_filePath, _packageType, _sourcePath, _realSourceBaseName)
        
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
                    
    def getFileTree(_path, _subDirectoryDeep=-1, _outputTarget="return", _outputType="html", _contentType="fileTree", _extInfo="no"):
        from Core.MyObjects import trForUI, trForM
        info = InputOutputs.getFileTree(_path, _subDirectoryDeep, _outputType, _contentType, _extInfo)
        info = trForUI(info)
        if _outputTarget=="return":
            return info
        elif _outputTarget=="file":
            from Core.MyObjects import MFileDialog
            from Core import Dialogs
            if _outputType=="html":
                if _extInfo!="no":
                    strHeader = ("<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Strict//EN\" \n"+
                        "\"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd\"> \n"+
                        "<html xmlns=\"http://www.w3.org/1999/xhtml\" xml:lang=\"tr\" lang=\"tr\" dir=\"ltr\"> \n"+
                        "<head> \n<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" /> \n</head> \n<body> \n")
                    strFooter = " \n</body> \n</html>"
                    info = strHeader + info + strFooter
                formatTypeName = translate("Tables", "HTML")
                fileExt="html"
            elif _outputType=="plainText":
                formatTypeName = translate("Tables", "Plain Text")
                fileExt="txt"
            filePath = MFileDialog.getSaveFileName(Universals.MainWindow,translate("Tables", "Save As"),
                                    trForM(Variables.userDirectoryPath),trForUI(formatTypeName+" (*."+fileExt+")"))
            if filePath!="":
                filePath = str(filePath)
                if _outputType=="html" and filePath[-5:]!=".html":
                    filePath += ".html"
                elif _outputType=="plainText" and filePath[-4:]!=".txt":
                    filePath += ".txt"
                writeToFile(filePath, info)
                Dialogs.show(translate("Tables", "File Tree Created"),
                            str(translate("Tables", "File tree created in file: \"%s\".")) % Organizer.getLink(filePath))
        elif _outputTarget=="dialog":
            from Core.MyObjects import MDialog, MWidget, MVBoxLayout, MTextEdit, MPushButton, MObject, SIGNAL, getMyObject
            dDialog = MDialog(Universals.MainWindow)
            if Universals.isActivePyKDE4==True:
                dDialog.setButtons(MDialog.NoDefault)
            dDialog.setWindowTitle(translate("Tables", "File Tree"))
            mainPanel = MWidget(dDialog)
            vblMain = MVBoxLayout(mainPanel)
            if _outputType=="html":
                QtWebKit = getMyObject("QtWebKit")
                wvWeb = QtWebKit.QWebView()
                wvWeb.setHtml(trForUI(info))
            elif _outputType=="plainText":
                wvWeb = MTextEdit()
                wvWeb.setPlainText(trForUI(info))
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
        elif _outputTarget=="clipboard":
            from Core.MyObjects import MApplication
            MApplication.clipboard().setText(trForUI(info))
            
    def fixToSize(_path, _size, _clearFrom="head"):
        return InputOutputs.fixToSize(_path, _size, _clearFrom)
            
    def getHashDigest(_filePath, _hashType="MD5"):
        return InputOutputs.getHashDigest(_filePath, _hashType)
        
    def createHashDigestFile(_filePath, _digestFilePath=None, _hashType="MD5", _isAddFileExtension=True, _digestContent=None):
        return InputOutputs.createHashDigestFile(_filePath, _digestFilePath, _hashType, _isAddFileExtension, _digestContent)
        
        
        
