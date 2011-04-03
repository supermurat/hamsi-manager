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
import Records

class InputOutputs:
    """Read and writes are arranged in this class"""
    global isFile, isDir, moveFileOrDir, listDir, makeDirs, removeDir, removeFile, getDirName, getBaseName, copyDirTree, trSort, readDirectory, moveOrChange, moveDir, appendingDirectories, readDirectoryWithSubDirectories, clearEmptyDirectories, clearUnneededs, clearIgnoreds, checkIcon, removeFileOrDir, changeDirectories, readTextFile, writeTextFile, clearPackagingDirectory, makePack, extractPack, copyOrChange, isExist, copyDirectory, isWritableFileOrDir, getRealDirName, checkSource, checkDestination, copyFileOrDir, readDirectoryAll, getObjectType, isAvailableName, getFileExtension, readFromFile, writeToFile, addToFile, readFromBinaryFile, writeToBinaryFile, readLinesFromFile, fileSystemEncoding, clearTempFiles, getFileTree, removeOnlySubFiles, moveToPathOfDeleted, getSize, fixToSize, clearCleaningDirectory, checkExtension, isDirEmpty, createSymLink, willCheckIconDirectories, isSmartCheckIcon, activateSmartCheckIcon, completeSmartCheckIcon, setIconToDirectory, getFirstImageInDirectory, isReadableFileOrDir, getHashDigest, createHashDigestFile, getIconFromDirectory, getRealPath, getShortPath, copyDirContent
    appendingDirectories = []
    fileSystemEncoding = Variables.defaultFileSystemEncoding
    willCheckIconDirectories = []
    isSmartCheckIcon = False
    
    def isFile(_oldPath):
        _oldPath = str(_oldPath)
        try:return os.path.isfile(Universals.trEncode(_oldPath, fileSystemEncoding))
        except:return os.path.isfile(_oldPath)
    
    def isDir(_oldPath):
        _oldPath = str(_oldPath)
        try:return os.path.isdir(Universals.trEncode(_oldPath, fileSystemEncoding))
        except:return os.path.isdir(_oldPath)
    
    def isDirEmpty(_oldPath):
        _oldPath = str(_oldPath)
        if isDir(_oldPath):
            if len(listDir(_oldPath))==0:
                return True
        return False
        
    def isExist(_oldPath):
        if isFile(_oldPath):
            return True
        elif isDir(_oldPath):
            return True
        return False
        
    def isAvailableName(_newPath):
        try:
            t = Universals.trEncode(_newPath, fileSystemEncoding)
            return True
        except:
            return False
    
    def getSize(_oldPath):
        from stat import ST_SIZE
        try:return os.stat(Universals.trEncode(_oldPath, fileSystemEncoding))[ST_SIZE]
        except:return os.stat(_oldPath)[ST_SIZE]
    
    def getObjectType(_oldPath):
        objectType="file"
        if isDir(_oldPath):
            objectType="directory"
        return objectType
    
    def getDirName(_oldPath):
        _oldPath = str(_oldPath)
        try:returnValue = os.path.dirname(Universals.trEncode(_oldPath, fileSystemEncoding))
        except:returnValue = os.path.dirname(_oldPath)
        try:return Universals.trDecode(returnValue, fileSystemEncoding)
        except:return returnValue
    
    def getRealDirName(_oldPath, isGetParent=False):
        _oldPath = str(_oldPath)
        if len(_oldPath)==0: return "/"
        if _oldPath[-1]=="/":
            _oldPath = _oldPath[:-1]
        if isGetParent:
            realDirName = getDirName(str(_oldPath))
        else:
            realDirName = str(_oldPath)
        while 1:
            if isDir(realDirName):
                break
            if realDirName=="":
                realDirName = "/"
                break
            realDirName = getDirName(realDirName)
        return realDirName
        
    def getRealPath(_path, _parentPath=None):
        _path = str(_path)
        if len(_path)==0: return "/"
        if _parentPath!=None:
            _parentPath = getRealPath(_parentPath)
            if _path[:2]=="./":
                _path = _parentPath + _path[1:]
        return os.path.abspath(_path)
        return _path
    
    def getShortPath(_path, _parentPath):
        _path = str(_path)
        _parentPath = str(_parentPath)
        _path = _path.replace(_parentPath, ".")
        return _path
    
    def getBaseName(_oldPath):
        _oldPath = str(_oldPath)
        try:returnValue = os.path.basename(Universals.trEncode(_oldPath, fileSystemEncoding))
        except:returnValue = os.path.basename(_oldPath)
        try:return Universals.trDecode(returnValue, fileSystemEncoding)
        except:return returnValue
    
    def checkExtension(_oldPath, _extension):
        _oldPath = str(_oldPath).lower()
        _extension = str(_extension).lower()
        if _extension.strip()!="":
            if _extension[0]==".": 
                _extension = _extension[1:]
            extIndex = _oldPath.find("." + _extension)
            if extIndex!=-1:
                if _oldPath[extIndex:]== "." + _extension:
                    return True
        return False
        
    def getFileExtension(_filePath):
        _filePath = str(_filePath).lower()
        if _filePath.find(".")!=-1:
            if Universals.MySettings["fileExtesionIs"]==Variables.fileExtesionIsKeys[0]:
                return _filePath.split(".", 1)[1]
            elif Universals.MySettings["fileExtesionIs"]==Variables.fileExtesionIsKeys[1]:
                return _filePath.rsplit(".", 1)[1]
        return ""
    
    def moveFileOrDir(_oldPath, _newPath):
        _oldPath, _newPath = str(_oldPath), str(_newPath)
        if getDirName(_oldPath)==getDirName(_newPath):
            try:os.rename(Universals.trEncode(_oldPath, fileSystemEncoding),Universals.trEncode(_newPath, fileSystemEncoding))
            except:os.rename(_oldPath,_newPath)
        else:
            if isDir(getDirName(_newPath))==False:
                makeDirs(getDirName(_newPath))
            try:shutil.move(Universals.trEncode(_oldPath, fileSystemEncoding),Universals.trEncode(_newPath, fileSystemEncoding))
            except:shutil.move(_oldPath,_newPath)
        Records.add("Moved", _oldPath, _newPath)
    
    def copyFileOrDir(_oldPath, _newPath):
        _oldPath, _newPath = str(_oldPath), str(_newPath)
        if isDir(getDirName(_newPath))==False:
            makeDirs(getDirName(_newPath))
        if isFile(_oldPath):
            try:shutil.copy(Universals.trEncode(_oldPath, fileSystemEncoding),Universals.trEncode(_newPath, fileSystemEncoding))
            except:shutil.copy(_oldPath,_newPath)
        else:
            copyDirTree(_oldPath, _newPath)
        Records.add("Copied", _oldPath, _newPath)
            
    def copyDirTree(_oldPath, _newPath):
        _oldPath, _newPath = str(_oldPath), str(_newPath)
        try:shutil.copytree(Universals.trEncode(_oldPath, fileSystemEncoding),Universals.trEncode(_newPath, fileSystemEncoding))
        except:shutil.copytree(_oldPath,_newPath)
        Records.add("Copied", _oldPath, _newPath)
        
    def copyDirContent(_oldPath, _newPath):
        _oldPath, _newPath = str(_oldPath), str(_newPath)
        if isDir(_newPath)==False:
            makeDirs(_newPath)
        for contentPath in listDir(_oldPath):
            if isDir(_oldPath+"/"+contentPath):
                copyDirContent(_oldPath+"/"+contentPath, _newPath+"/"+contentPath)
            else:
                copyFileOrDir(_oldPath+"/"+contentPath, _newPath+"/"+contentPath)
    
    def createSymLink(_oldPath, _newPath):
        _oldPath, _newPath = str(_oldPath), str(_newPath)
        if Variables.isAvailableSymLink():
            from os import symlink
            if isExist(_newPath):
                removeFile(_newPath)
            try:symlink(Universals.trEncode(_oldPath, fileSystemEncoding),Universals.trEncode(_newPath, fileSystemEncoding))
            except:symlink(_oldPath,_newPath)
            Records.add("Created Link", _oldPath, _newPath)
            return True
        else:
            Records.add("Can Not Created Link", _oldPath, _newPath)
            copyOrChange(_oldPath, _newPath, getObjectType(_oldPath))
            return False
      
    def listDir(_oldPath):
        names = []
        if checkSource(_oldPath, "directory"):
            try:names = os.listdir(Universals.trEncode(_oldPath, fileSystemEncoding))
            except:names = os.listdir(_oldPath)
            names.sort(key=trSort)
        return names
        
    def makeDirs(_newPath):
        if isWritableFileOrDir(getRealDirName(_newPath)):
            try:os.makedirs(Universals.trEncode(_newPath, fileSystemEncoding))
            except:os.makedirs(_newPath)
            Records.add("Created", _newPath)
            return True
        return False
        
    def removeDir(_oldPath):
        if Universals.getBoolValue("isDontDeleteFileAndDirectory"):
            moveToPathOfDeleted(_oldPath)
        else:
            try:os.rmdir(Universals.trEncode(_oldPath, fileSystemEncoding))
            except:os.rmdir(_oldPath)
        Records.add("Removed", _oldPath)
        return True
        
    def removeFile(_oldPath):
        if Universals.getBoolValue("isDontDeleteFileAndDirectory"):
            moveToPathOfDeleted(_oldPath)
        else:
            try:os.remove(Universals.trEncode(_oldPath, fileSystemEncoding))
            except:os.remove(_oldPath)
        Records.add("Removed", _oldPath)
        return True
    
    def moveToPathOfDeleted(_oldPath):
        from time import strftime
        import random
        moveFileOrDir(_oldPath, Universals.MySettings["pathOfDeletedFilesAndDirectories"] + "/" + strftime("%Y%m%d_%H%M%S") + "_" + str(random.randrange(0, 9999999)) + "_" + getBaseName(_oldPath))
    
    def trSort(_info):
        import locale
        if Variables.isPython3k:
            _info = str(_info)
        try:
            return locale.strxfrm(Universals.trEncode(_info, fileSystemEncoding))
        except:
            return locale.strxfrm(_info)
    
    def isReadableFileOrDir(_newPath): 
        realPath = _newPath
        if isFile(realPath)==False:
            realPath = getRealDirName(realPath)
        try: 
            if os.access(Universals.trEncode(realPath, fileSystemEncoding), os.R_OK): 
                return True 
        except: 
            if os.access(realPath, os.R_OK): 
                return True
        return False
        
    def isWritableFileOrDir(_newPath):
        realPath = _newPath
        if isFile(realPath)==False:
            realPath = getRealDirName(realPath)
        try: 
            if os.access(Universals.trEncode(realPath, fileSystemEncoding), os.W_OK): 
                return True 
        except: 
            if os.access(realPath, os.W_OK): 
                return True
        return False
        
    def checkSource(_oldPath, _objectType="fileOrDirectory"):
        if _objectType=="file" and isFile(_oldPath)==False:
            return False
        elif _objectType=="directory" and isDir(_oldPath)==False:
            return False
        elif isDir(_oldPath)==False and isFile(_oldPath)==False:
            return False
        return _oldPath
        
    def checkDestination(_oldPath, _newPath, _isMake=False):
        global appendingDirectories
        if isExist(_newPath):
            if isWritableFileOrDir(_newPath):
                if _oldPath.lower()!=_newPath.lower() or Variables.osName=="posix": 
                    if isFile(_newPath):
                        if _isMake:
                            return _newPath
                        else:
                            return False
                    elif isDir(_newPath):
                        if isFile(_oldPath):
                            return False
                        else:
                            isAllowed=False
                            for tDir in appendingDirectories:
                                if _newPath==tDir:
                                    isAllowed=True
                                    return _newPath
                            if isAllowed==False: 
                                if _isMake:
                                    appendingDirectories.append(_newPath)
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
        global appendingDirectories
        appendingDirectories=[]
        fileAndDirectoryNames,fileNames,directoryNames,musicFileNames=[],[],[],[]
        for name in listDir(_path):
            if name[:1] != ".":
                try:fileAndDirectoryNames.append(Universals.trDecode(name, fileSystemEncoding))
                except:fileAndDirectoryNames.append(name)
        for name in fileAndDirectoryNames:
            if isDir(_path+"/"+name):
                directoryNames.append(name)
            else:
                fileNames.append(name)
                for ext in Universals.getListFromStrint(Universals.MySettings["musicExtensions"]):
                    try:
                        if name.split(".")[-1].lower() == str(ext).lower():
                            musicFileNames.append(name)
                    except:
                        pass
        fileAndDirectoryNames = []
        for d in directoryNames:
            fileAndDirectoryNames.append(d)
        for f in fileNames:
            fileAndDirectoryNames.append(f)
        if _objectType=="file":
            return fileNames
        elif _objectType=="directory":
            return directoryNames  
        elif _objectType=="fileAndDirectory":
            return fileAndDirectoryNames  
        elif _objectType=="music":
            return musicFileNames
        else:
            return []
    
    def readDirectoryAll(_path): 
        tFileAndDirs=[]
        for name in listDir(_path):
            try:tFileAndDirs.append(str(Universals.trDecode(name, fileSystemEncoding)))
            except:
                try:tFileAndDirs.append(str(name))
                except:tFileAndDirs.append(name)
        return tFileAndDirs
  
    def readDirectoryWithSubDirectories(_path, _subDirectoryDeep=-1, _isGetDirectoryNames=False, _isOnlyDirectories=False, _currentSubDeep=0):
        global appendingDirectories
        _subDirectoryDeep = int(_subDirectoryDeep)
        allFilesAndDirectories, names, files, directories, appendingDirectories =[],[],[],[],[]
        try:namesList = readDirectoryAll(_path)
        except:return []
        for name in namesList:
            if name[:1] != ".":
                names.append(name)
        for name in names:
            if isDir(_path+"/"+name):
                directories.append(name)
            else:
                files.append(name)
        names = []
        for d in directories:
            names.append(d)
        for f in files:
            names.append(f)
        for name in names:
            if name[:1] != ".":
                if isDir(_path+"/"+name):
                    if _subDirectoryDeep==-1 or _subDirectoryDeep>_currentSubDeep:
                        if _isGetDirectoryNames==True:
                            allFilesAndDirectories.append(_path+"/"+name)
                        for dd in readDirectoryWithSubDirectories(_path+"/"+name, _subDirectoryDeep, _isGetDirectoryNames, _isOnlyDirectories, _currentSubDeep+1):
                            allFilesAndDirectories.append(dd)
                elif _isOnlyDirectories==False:
                    allFilesAndDirectories.append(_path+"/"+name)
        return allFilesAndDirectories
    
    def readFromFile(_path, _contentEncoding = fileSystemEncoding):
        _path = str(_path)
        if Variables.isPython3k:
            try:f = open(Universals.trEncode(_path, fileSystemEncoding) , encoding = _contentEncoding)
            except:f = open(_path , encoding = _contentEncoding)
        else:
            import codecs
            try:f = codecs.open(Universals.trEncode(_path, fileSystemEncoding) , encoding = _contentEncoding)
            except:f = codecs.open(_path , encoding = _contentEncoding)
        info = f.read()
        f.close()
        return info
        
    def readLinesFromFile(_path, _contentEncoding = fileSystemEncoding):
        _path = str(_path)
        if Variables.isPython3k:
            try:f = open(Universals.trEncode(_path, fileSystemEncoding) , encoding = _contentEncoding)
            except:f = open(_path , encoding = _contentEncoding)
        else:
            import codecs
            try:f = codecs.open(Universals.trEncode(_path, fileSystemEncoding) , encoding = _contentEncoding)
            except:f = codecs.open(_path , encoding = _contentEncoding)
        info = f.readlines()
        f.close()
        return info
        
    def readFromBinaryFile(_path):
        _path = str(_path)
        try:f = open(Universals.trEncode(_path, fileSystemEncoding), "rb")
        except:f = open(_path, "rb")
        info = f.read()
        f.close()
        return info
        
    def writeToFile(_path, _contents=""):
        _path = str(_path)
        try:f = open(Universals.trEncode(_path, fileSystemEncoding), "w")
        except:f = open(_path, "w")
        f.write(_contents)
        f.close()
        Records.add("Writed", _path)
        
    def writeToBinaryFile(_path, _contents=""):
        _path = str(_path)
        try:f = open(Universals.trEncode(_path, fileSystemEncoding), "wb")
        except:f = open(_path, "w")
        f.write(_contents)
        f.flush()
        f.close()
        Records.add("Writed", _path)
    
    def addToFile(_path, _contents=""):
        _path = str(_path)
        try:f = open(Universals.trEncode(_path, fileSystemEncoding), "a")
        except:f = open(_path, "w")
        f.write(_contents)
        f.close()
        Records.add("Added", _path)
    
    def readTextFile(_path):
        fileDetails = {}
        fileDetails["path"] = _path
        fileDetails["content"] = readFromFile(_path)
        #return [getDirName(_path), getBaseName(_path), readFromFile(_path)]  
        return fileDetails
        
    def writeTextFile(_oldFileValues, _newFileValues, _charSet="utf-8"):
        if _oldFileValues["content"]!=_newFileValues["content"] or _charSet!="utf-8":
            writeToFile(_oldFileValues["path"], Universals.trEncode(_newFileValues["content"], _charSet))
        if _oldFileValues["path"]!=_newFileValues["path"]:
            return moveOrChange(_oldFileValues["path"], _newFileValues["path"])
        return _oldFileValues["path"]
                
    def clearEmptyDirectories(_path, _isAutoCleanSubFolder=True, _isClear=False):
        #If directory deleted : returned True
        #If directory cleaned : returned False
        if Universals.getBoolValue("isActiveClearGeneral") or _isClear:
            clearUnneededs(_path)
            dontRemovingFilesCount = 0
            filesAndDirectories = readDirectoryAll(_path)
            for nameNo, name in enumerate(filesAndDirectories):
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
                    if clearEmptyDirectories(_path+"/"+name, _isAutoCleanSubFolder, _isClear):
                        dontRemovingFilesCount-=1
            if dontRemovingFilesCount==0 and Universals.getBoolValue("isDeleteEmptyDirectories"):
                clearIgnoreds(_path)
                removeDir(_path)
                return True
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
            for tDir in appendingDirectories:
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
            for tDir in appendingDirectories:
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
        if len(_values)!=0:
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
        return newFilesPath
        
    def activateSmartCheckIcon():
        global isSmartCheckIcon, willCheckIconDirectories
        isSmartCheckIcon = True
        willCheckIconDirectories = []
    
    def completeSmartCheckIcon():
        global isSmartCheckIcon, willCheckIconDirectories
        isSmartCheckIcon = False
        for iconDir in willCheckIconDirectories:
            checkIcon(iconDir)
        willCheckIconDirectories = []
    
    def checkIcon(_path, _isClear=False):
        global isSmartCheckIcon, willCheckIconDirectories
        if isSmartCheckIcon and _isClear==False:
            if willCheckIconDirectories.count(_path)==0:
                willCheckIconDirectories.append(_path)
        else:
            if _isClear==False:
                coverPath = ""
                coverName = getFirstImageInDirectory(_path)
                if coverName!=None:
                    coverPath = _path + "/" + coverName
                return setIconToDirectory(_path, coverPath)
            elif _isClear:
                return setIconToDirectory(_path)
    
    def getFirstImageInDirectory(_path, _coverNameIfExist=None, _isCheckDelete=False):
        _path = str(_path)
        cover = None
        imageFiles = []
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
        _path = str(_path)
        if isDir(_path):
            if _iconName==None:
                return False
            _iconName = str(_iconName).strip()
            returnValue, isChanging, isChange, isCorrectFileContent, rows = False, False, True, False, []
            if isFile(_iconName):
                if str(_path)==str(getDirName(_iconName)):
                    _iconName = "./" + getBaseName(_iconName)
                try:
                    info = readFromFile(_path + "/.directory")
                    if info.find("[Desktop Entry]")==-1:
                        info = "[Desktop Entry]\n" + info
                    isCorrectFileContent = True
                except:
                    info = "[Desktop Entry]"
                rows = info.split("\n")
                for rowNo in range(len(rows)):
                    if rows[rowNo][:5] == "Icon=":
                        if len(rows[rowNo])>5:
                            isFileExist = False
                            if rows[rowNo][5]=="." and isFile(_path + str(rows[rowNo][6:])):
                                isFileExist=True
                            elif rows[rowNo][5]!="." and isFile(rows[rowNo][5:]):
                                isFileExist=True
                            if isFileExist:
                                if Universals.getBoolValue("isChangeExistIcon")==False:
                                    isChange = False
                        isChanging = True
                        rows[rowNo] = "Icon=" + _iconName 
                        returnValue = True
                if isChange:
                    if isChanging==False:
                        rows.append("Icon=" + _iconName)
                        returnValue = True
                if isCorrectFileContent:
                    rowNoStrDesktopEntry = -1
                    rowNoStrIcon = -1
                    for rowNo in range(len(rows)):
                        if rows[rowNo].find("[Desktop Entry]")!=-1:
                            rowNoStrDesktopEntry = rowNo
                        elif rows[rowNo].find("Icon=")!=-1:
                            rowNoStrIcon = rowNo
                    if rowNoStrDesktopEntry != rowNoStrIcon - 1:
                        rows[rowNoStrDesktopEntry] += "\n" + rows[rowNoStrIcon]
                        rows[rowNoStrIcon] = ""
            else:
                if isFile(_path + "/.directory"):
                    info = readFromFile(_path + "/.directory")
                    rows = info.split("\n")
                    for rowNo in range(len(rows)):
                        if len(rows[rowNo])>4:
                            if rows[rowNo][:5] == "Icon=":
                                rows[rowNo] = ""
                                break
            info=""
            for row in rows:
                if row.strip()!="":
                    info+=row+"\n"
            writeToFile(_path + "/.directory", info)
            return returnValue
        else:
            return False
        
    def getIconFromDirectory(_path):
        iconPath, isCorrectedFileContent = None, True
        if isFile(_path + "/.directory"):
            info = readFromFile(_path + "/.directory")
            if info.find("[Desktop Entry]")==-1 and len(info)>0:
                isCorrectedFileContent = False
            if info.find("[Desktop Entry]") > info.find("Icon=") and info.find("Icon=")>-1:
                isCorrectedFileContent = False
            rows = info.split("\n")
            for rowNo in range(len(rows)):
                if rows[rowNo][:5] == "Icon=":
                    if len(rows[rowNo])>5:
                        if rows[rowNo][5]=="." and isFile(_path + str(rows[rowNo][6:])):
                            iconPath = _path + str(rows[rowNo][6:])
                        elif rows[rowNo][5]!="." and isFile(rows[rowNo][5:]):
                            iconPath = rows[rowNo][5:]
                        elif rows[rowNo][5]==".":
                            iconPath = _path + str(rows[rowNo][6:])
                            isCorrectedFileContent = False
                        else:
                            iconPath = rows[rowNo][5:]
                            isCorrectedFileContent = False
        return iconPath, isCorrectedFileContent

    def clearPackagingDirectory(_path):
        if checkSource(_path, "directory"):
            _path = str(_path)
            if Universals.getBoolValue("isClearEmptyDirectoriesWhenPath"):
                clearEmptyDirectories(_path, Universals.getBoolValue("isAutoCleanSubFolderWhenPath"))
            for f in Universals.getListFromStrint(Universals.MySettings["packagerUnneededFiles"]):
                if isFile(_path+"/"+f):
                    removeFile(_path+"/"+f)
            for d in Universals.getListFromStrint(Universals.MySettings["packagerUnneededDirectories"]):
                if isExist(_path+"/"+d):
                    removeFileOrDir(_path+"/"+d, True)
            dontRemovingFilesCount = 0
            filesAndDirectories = readDirectoryAll(_path)
            for nameNo, name in enumerate(filesAndDirectories):
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
                removeDir(_path)
                return False
            return True
        else:
            False
            
    def clearCleaningDirectory(_path):
        if checkSource(_path, "directory"):
            _path = str(_path)
            if Universals.getBoolValue("isClearEmptyDirectoriesWhenClear"):
                clearEmptyDirectories(_path, Universals.getBoolValue("isAutoCleanSubFolderWhenClear"))
            for f in Universals.getListFromStrint(Universals.MySettings["cleanerUnneededFiles"]):
                if isFile(_path+"/"+f):
                    removeFile(_path+"/"+f)
            for d in Universals.getListFromStrint(Universals.MySettings["cleanerUnneededDirectories"]):
                if isExist(_path+"/"+d):
                    removeFileOrDir(_path+"/"+d, True)
            dontRemovingFilesCount = 0
            filesAndDirectories = readDirectoryAll(_path)
            for nameNo, name in enumerate(filesAndDirectories):
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
                removeDir(_path)
                return False
            return True
        else:
            False

    def makePack(_filePath, _packageType, _sourcePath):
        import tarfile
        _filePath, _sourcePath = str(_filePath), str(_sourcePath)
        if isDir(_filePath):
            return False
        try:tar = tarfile.open(Universals.trEncode(_filePath, fileSystemEncoding), "w:" + _packageType)
        except:tar = tarfile.open(_filePath, "w:" + _packageType)
        try:tar.add(Universals.trEncode(_sourcePath, fileSystemEncoding), "")
        except:tar.add(_sourcePath, "")
        tar.close()
        Records.add("Packed", _filePath)
        return True
        
    def extractPack(_oldPath, _newPath):
        _oldPath, _newPath = str(_oldPath), str(_newPath)
        import tarfile
        while 1==1:
            try:
                try:tar = tarfile.open(Universals.trEncode(_oldPath, fileSystemEncoding), "r:gz")
                except:tar = tarfile.open(_oldPath, "r:gz")
                break
            except:
                time.sleep(1)
        try:tar.extractall(Universals.trEncode(_newPath, fileSystemEncoding), members=tar.getmembers())
        except:tar.extractall(_newPath, members=tar.getmembers())
        tar.close()
        Records.add("Extracted", _oldPath, _newPath)
        
    def clearTempFiles():
        import tempfile
        for fileName in readDirectoryAll(tempfile.gettempdir()):
            if fileName[:15] == "HamsiManager":
                if isDir(tempfile.gettempdir()+"/"+fileName):
                    removeFileOrDir(tempfile.gettempdir()+"/"+fileName, True)
                else:
                    removeFileOrDir(tempfile.gettempdir()+"/"+fileName)
                    
    def getFileTree(_path, _subDirectoryDeep=-1, _formatType="html", _extInfo="no"):
        from Universals import translate
        _path = str(_path)
        files = readDirectoryWithSubDirectories(_path, _subDirectoryDeep, True)
        info = ""
        if _formatType=="html":
            if _extInfo=="no":
                pass
            elif _extInfo=="title":
                info += " \n <h3>%s </h3> \n" % (str(translate("Tables", "File Tree")))
                info += " %s<br> \n" % (_path)
            dirNumber = _path.count("/")
            findStrings, replaceStrings = [], []
            for x, file in enumerate(files):
                if isDir(file):
                    findStrings.append(file)
                    replaceStrings.append((Universals.getUtf8Data("upright") + "&nbsp;&nbsp;&nbsp;"*(file.count("/")-dirNumber)) + Universals.getUtf8Data("upright+right") + "&nbsp;")
            findStrings.reverse()
            replaceStrings.reverse()
            fileList = list(range(len(files)))
            for x, file in enumerate(files):
                fileList[x] = file + "<br> \n"
                for  y, fstr in enumerate(findStrings):
                    if file!=fstr:
                        fileList[x] = fileList[x].replace(fstr + "/", replaceStrings[y])
                if x>0:
                    tin = fileList[x-1].find(Universals.getUtf8Data("upright+right"))
                    tin2 = fileList[x].find(Universals.getUtf8Data("upright+right"))
                    if tin>tin2:
                        fileList[x-1] = fileList[x-1].replace(Universals.getUtf8Data("upright+right"), Universals.getUtf8Data("up+right"))
            for x, fileName in enumerate(fileList):
                if x!=len(fileList)-1:
                    info += fileName.replace(_path + "/", Universals.getUtf8Data("upright+right") + "&nbsp;")
                else:
                    info += fileName.replace(_path + "/", Universals.getUtf8Data("up+right") + "&nbsp;")
        elif _formatType=="plainText":
            if _extInfo=="no":
                pass
            elif _extInfo=="title":
                info += " %s \n" % (str(translate("Tables", "File Tree")))
                info += _path + "\n"
            dirNumber = _path.count("/")
            findStrings, replaceStrings = [], []
            for x, file in enumerate(files):
                if isDir(file):
                    findStrings.append(file)
                    replaceStrings.append((Universals.getUtf8Data("upright") + "   "*(file.count("/")-dirNumber)) + Universals.getUtf8Data("upright+right") + " ")
            findStrings.reverse()
            replaceStrings.reverse()
            fileList = list(range(len(files)))
            for x, file in enumerate(files):
                fileList[x] = file + "\n"
                for  y, fstr in enumerate(findStrings):
                    if file!=fstr:
                        fileList[x] = fileList[x].replace(fstr + "/", replaceStrings[y])
                if x>0:
                    tin = fileList[x-1].find(Universals.getUtf8Data("upright+right"))
                    tin2 = fileList[x].find(Universals.getUtf8Data("upright+right"))
                    if tin>tin2:
                        fileList[x-1] = fileList[x-1].replace(Universals.getUtf8Data("upright+right"), Universals.getUtf8Data("up+right"))
            for x, fileName in enumerate(fileList):
                if x!=len(fileList)-1:
                    info += fileName.replace(_path + "/", Universals.getUtf8Data("upright+right") + " ")
                else:
                    info += fileName.replace(_path + "/", Universals.getUtf8Data("up+right") + " ")
        return info
            
    def fixToSize(_path, _size, _clearFrom="head"):
        if isFile(_path):
            while getSize(_path) > _size:
                if _clearFrom=="head":
                    try:contents = readFromFile(_path)[500:]
                    except:
                        try:contents = readFromFile(_path)[200:]
                        except:contents = readFromFile(_path)[20:]
                else:
                    try:contents = readFromFile(_path)[:-500]
                    except:
                        try:contents = readFromFile(_path)[:-200]
                        except:contents = readFromFile(_path)[:-20]
                writeToFile(_path, contents)
        
    def getHashDigest(_filePath, _hashType="MD5"):
        try:
            import hashlib
            if _hashType=="MD5":
                m = hashlib.md5()
            elif _hashType=="SHA1":
                m = hashlib.sha1()
            elif _hashType=="SHA224":
                m = hashlib.sha224()
            elif _hashType=="SHA256":
                m = hashlib.sha256()
            elif _hashType=="SHA384":
                m = hashlib.sha384()
            elif _hashType=="SHA512":
                m = hashlib.sha512()
            m.update(readFromBinaryFile(_filePath))
            return m.hexdigest()
        except:
            #for x < python 2.5
            try:
                if _hashType=="MD5":
                    import md5
                    return md5.new(readFromBinaryFile(_filePath)).hexdigest()
                elif _hashType=="SHA1":
                    import sha
                    return sha.new(readFromBinaryFile(_filePath)).hexdigest()
            except:
                return False
        
    def createHashDigestFile(_filePath, _digestFilePath=None, _hashType="MD5", _isAddFileExtension=True, _digestContent=None):
        if _digestContent==None:
            _digestContent = getHashDigest(_filePath, _hashType)
        fileExtension = ""
        if _isAddFileExtension:
            fileExtension = _hashType.lower()
        if _digestFilePath==None:
            _digestFilePath = _filePath
        writeToFile(_digestFilePath + fileExtension, _digestContent)
        return True
        
        try:
            import hashlib
            return ["MD5", "SHA1", "SHA224", "SHA256", "SHA384", "SHA512"]
        except:
            #for x < python 2.5
            hashTypes = []
            try:
                import md5
                hashTypes.append("MD5")
            except:pass
            try:
                import md5
                hashTypes.append("SHA1")
            except:pass
            return hashTypes
        
        
