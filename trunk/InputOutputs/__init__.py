# -*- coding: utf-8 -*-

from os import listdir,path,removedirs,makedirs, rmdir, remove, rename
import os
import sys, stat
from shutil import move, copytree, copy
import locale
import Universals
import Settings
import Records
import Organizer

class InputOutputs:
    """Read and writes are arranged in this class"""
    global isFile, isDir, moveFileOrDir, listDir, makeDirs, removeDir, removeFile, getDirName, getBaseName, copyDirTree, trSort, readDirectory,moveOrChange,moveDir,appendingDirectories,readDirectoryWithSubDirectories, clearEmptyDirectories, getSearchEnginesNames, clearUnneededs, clearIgnoreds, checkIcon, removeFileOrDir, musicFileNames, changeDirectories, readTextFile, writeTextFile, clearPackagingDirectory, makePack, extractPack, getMyPluginsNames, copyOrChange, fileNames,directoryNames,musicFileNames,fileAndDirectoryNames, allFilesAndDirectories, isExist, getInstalledLanguagesCodes, getInstalledLanguagesNames, copyDirectory, isWritableFileOrDir, getRealDirName, checkSource, checkDestination, copyFileOrDir, readDirectoryAll, getObjectType, currentDirectoryPath, readFromFile, writeToFile, addToFile, readFromBinaryFile, writeToBinaryFile, readLinesFromFile, systemsCharSet, clearTempFiles, getFileTree, removeOnlySubFiles, isMoveToTrash, moveToTrash, getSize, fixToSize, getInstalledThemes, clearCleaningDirectory, checkExtension, isDirEmpty, createSymLink, isAvailableSymLink, willCheckIconDirectories, isSmartCheckIcon, activateSmartCheckIcon, complateSmartCheckIcon, setIconToDirectory, getFirstImageInDirectory, isReadableFileOrDir, getHashDigest, createHashDigestFile
    fileNames = []
    directoryNames = []
    musicFileNames = []
    fileAndDirectoryNames = []
    allFilesAndDirectories = []
    appendingDirectories = []
    currentDirectoryPath = ""
    systemsCharSet = Settings.defaultFileSystemEncoding
    isMoveToTrash = False
    willCheckIconDirectories = []
    isSmartCheckIcon = False
    
    def isFile(_oldPath):
        _oldPath = str(_oldPath)
        try:return path.isfile(_oldPath.encode(systemsCharSet))
        except:return path.isfile(_oldPath)
    
    def isDir(_oldPath):
        _oldPath = str(_oldPath)
        try:return path.isdir(_oldPath.encode(systemsCharSet))
        except:return path.isdir(_oldPath)
    
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
    
    def getSize(_oldPath):
        try:return os.stat(_oldPath.encode(systemsCharSet))[stat.ST_SIZE]
        except:return os.stat(_oldPath)[stat.ST_SIZE]
    
    def getObjectType(_oldPath):
        objectType="file"
        if isDir(_oldPath):
            objectType="directory"
        return objectType
    
    def getDirName(_oldPath):
        _oldPath = str(_oldPath)
        try:returnValue = path.dirname(_oldPath.encode(systemsCharSet))
        except:returnValue = path.dirname(_oldPath)
        try:return returnValue.decode(systemsCharSet)
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
    
    def getBaseName(_oldPath):
        _oldPath = str(_oldPath)
        try:returnValue = path.basename(_oldPath.encode(systemsCharSet))
        except:returnValue = path.basename(_oldPath)
        try:return returnValue.decode(systemsCharSet)
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
    
    def moveFileOrDir(_oldPath, _newPath):
        _oldPath, _newPath = str(_oldPath), str(_newPath)
        if getDirName(_oldPath)==getDirName(_newPath):
            try:rename(_oldPath.encode(systemsCharSet),_newPath.encode(systemsCharSet))
            except:rename(_oldPath,_newPath)
        else:
            if isDir(getDirName(_newPath))==False:
                makeDirs(getDirName(_newPath))
            try:move(_oldPath.encode(systemsCharSet),_newPath.encode(systemsCharSet))
            except:move(_oldPath,_newPath)
        Records.add("Moved", _oldPath, _newPath)
    
    def copyFileOrDir(_oldPath, _newPath):
        _oldPath, _newPath = str(_oldPath), str(_newPath)
        if isDir(getDirName(_newPath))==False:
            makeDirs(getDirName(_newPath))
        if isFile(_oldPath):
            try:copy(_oldPath.encode(systemsCharSet),_newPath.encode(systemsCharSet))
            except:copy(_oldPath,_newPath)
        else:
            copyDirTree(_oldPath, _newPath)
        Records.add("Copied", _oldPath, _newPath)
            
    def copyDirTree(_oldPath, _newPath):
        _oldPath, _newPath = str(_oldPath), str(_newPath)
        try:copytree(_oldPath.encode(systemsCharSet),_newPath.encode(systemsCharSet))
        except:copytree(_oldPath,_newPath)
        Records.add("Copied", _oldPath, _newPath)
    
    def isAvailableSymLink():
        try:
            from os import symlink
            return True
        except:
            return False
    
    def createSymLink(_oldPath, _newPath):
        _oldPath, _newPath = str(_oldPath), str(_newPath)
        if isAvailableSymLink():
            from os import symlink
            if isExist(_newPath):
                removeFile(_newPath)
            try:symlink(_oldPath.encode(systemsCharSet),_newPath.encode(systemsCharSet))
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
            try:names = listdir(_oldPath.encode(systemsCharSet))
            except:names = listdir(_oldPath)
            names.sort(key=trSort)
        return names
        
    def makeDirs(_newPath):
        if isWritableFileOrDir(getRealDirName(_newPath)):
            try:makedirs(_newPath.encode(systemsCharSet))
            except:makedirs(_newPath)
            Records.add("Created", _newPath)
        
    def removeDir(_oldPath):
        if isMoveToTrash:
            moveToTrash(_oldPath)
        else:
            try:rmdir(_oldPath.encode(systemsCharSet))
            except:rmdir(_oldPath)
        Records.add("Removed", _oldPath)
        
    def removeFile(_oldPath):
        if isMoveToTrash:
            moveToTrash(_oldPath)
        else:
            try:remove(_oldPath.encode(systemsCharSet))
            except:remove(_oldPath)
        Records.add("Removed", _oldPath)
    
    def moveToTrash(_oldPath):
        import Execute
        try:Execute.execute("kioclient move '" + _oldPath.encode(systemsCharSet) + "' trash:/")
        except:Execute.execute("kioclient move '" + _oldPath + "' trash:/")
    
    def trSort(_info):
        try:
            return locale.strxfrm(_info.encode(systemsCharSet))
        except:
            return locale.strxfrm(_info)
    
    def isReadableFileOrDir(_newPath, _isOnlyCheck=False): 
        realPath = _newPath
        if isFile(realPath)==False:
            realPath = getRealDirName(realPath)
        try: 
            if os.access(realPath.encode(systemsCharSet), os.R_OK): 
                return True 
        except: 
            if os.access(realPath, os.R_OK): 
                return True
        if _isOnlyCheck==False:
            if isDir(realPath):
                from MyObjects import translate
                import Dialogs
                Dialogs.showError(translate("InputOutputs", "Access Denied"),
                        str(translate("InputOutputs", "\"%s\" : you do not have the necessary permissions to read this directory.<br>Please check your access controls and retry.")) % Organizer.getLink(realPath))
            else:
                from MyObjects import translate
                import Dialogs
                Dialogs.showError(translate("InputOutputs", "Access Denied"),
                        str(translate("InputOutputs", "\"%s\" : you do not have the necessary permissions to read this file.<br>Please check your access controls and retry.")) % Organizer.getLink(realPath))
        return False
        
    def isWritableFileOrDir(_newPath, _isOnlyCheck=False): 
        realPath = _newPath
        if isFile(realPath)==False:
            realPath = getRealDirName(realPath)
        try: 
            if os.access(realPath.encode(systemsCharSet), os.W_OK): 
                return True 
        except: 
            if os.access(realPath, os.W_OK): 
                return True
        if _isOnlyCheck==False:
            if isDir(realPath):
                from MyObjects import translate
                import Dialogs
                Dialogs.showError(translate("InputOutputs", "Access Denied"),
                        str(translate("InputOutputs", "\"%s\" : you do not have the necessary permissions to change this directory.<br>Please check your access controls and retry.")) % Organizer.getLink(realPath))
            else:
                from MyObjects import translate
                import Dialogs
                Dialogs.showError(translate("InputOutputs", "Access Denied"),
                        str(translate("InputOutputs", "\"%s\" : you do not have the necessary permissions to change this file.<br>Please check your access controls and retry.")) % Organizer.getLink(realPath))
        return False
        
    def checkSource(_oldPath, _objectType="fileOrDirectory"):
        if _objectType=="file" and isFile(_oldPath)==False:
            import Dialogs
            from MyObjects import translate
            Dialogs.showError(translate("InputOutputs", "Cannot Find File"),
                    str(translate("InputOutputs", "\"%s\" : cannot find a file with this name.<br>Please make sure that it exists and retry.")) % Organizer.getLink(_oldPath))
            return False
        elif _objectType=="directory" and isDir(_oldPath)==False:
            import Dialogs
            from MyObjects import translate
            Dialogs.showError(translate("InputOutputs", "Cannot Find Directory"),
                    str(translate("InputOutputs", "\"%s\" : cannot find a folder with this name.<br>Please make sure that it exists and retry.")) % Organizer.getLink(_oldPath))
            return False
        elif isDir(_oldPath)==False and isFile(_oldPath)==False:
            import Dialogs
            from MyObjects import translate
            Dialogs.showError(translate("InputOutputs", "Cannot Find File Or Directory"),
                    str(translate("InputOutputs", "\"%s\" : cannot find a file or directory with this name.<br>Please make sure that it exists and retry.")) % Organizer.getLink(_oldPath))
            return False
        return _oldPath
        
    def checkDestination(_oldPath, _newPath, _isQuiet=False):
        global appendingDirectories
        if isExist(_newPath):
            if isWritableFileOrDir(_newPath):
                if _oldPath.lower()!=_newPath.lower() or os.name=="posix": 
                    if isFile(_newPath):
                        if _isQuiet:
                            return _newPath
                        else:
                            from MyObjects import translate
                            import Dialogs
                            answer = Dialogs.ask(translate("InputOutputs", "Current File Name"),
                                        str(translate("InputOutputs", "\"%s\" : there already exists a file with the same name.<br>Replace it with the current one?")) % Organizer.getLink(_newPath))
                            if answer==Dialogs.Yes: 
                                return _newPath
                            else:
                                return False
                    elif isDir(_newPath):
                        if isFile(_oldPath):
                            from MyObjects import translate
                            import Dialogs
                            answer = Dialogs.ask(translate("InputOutputs", "Current Directory Name"),
                                    str(translate("InputOutputs", "\"%s\" : there already exists a folder with the same name.<br>\"%s\" Add this file to the current folder?")) % (Organizer.getLink(_newPath), Organizer.getLink(_newPath)))
                            if answer==Dialogs.Yes: 
                                return _newPath+"/"+getBaseName(_newPath)
                            else:
                                return False
                        else:
                            isAllowed=False
                            for tDir in appendingDirectories:
                                if _newPath==tDir:
                                    isAllowed=True
                                    return _newPath
                            if isAllowed==False: 
                                if _isQuiet:
                                    appendingDirectories.append(_newPath)
                                    return _newPath
                                else:
                                    from MyObjects import translate
                                    import Dialogs
                                    answer = Dialogs.ask(translate("InputOutputs", "Current Directory Name"), 
                                            str(translate("InputOutputs", "\"%s\" : there already exists a folder with the same name.<br>Add your files to the current folder?")) % Organizer.getLink(_newPath))
                                    if answer==Dialogs.Yes:
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
        
    def readDirectory(_path):
        global fileNames,directoryNames,musicFileNames,appendingDirectories,fileAndDirectoryNames
        appendingDirectories=[]
        fileAndDirectoryNames,fileNames,directoryNames,musicFileNames=[],[],[],[]
        for name in listDir(_path):
            if name[:1] != ".":
                try:fileAndDirectoryNames.append(name.decode(systemsCharSet))
                except:fileAndDirectoryNames.append(name)
        for name in fileAndDirectoryNames:
            if isDir(_path+"/"+name):
                directoryNames.append(name)
            else:
                fileNames.append(name)
                for ext in Universals.getListFromStrint(Universals.MySettings["musicExtensions"]):
                    try:
                        if name.split(".")[-1].decode("utf-8").lower() == unicode(ext, "utf-8").lower():
                            musicFileNames.append(name)
                    except:
                        pass
        fileAndDirectoryNames = []
        for d in directoryNames:
            fileAndDirectoryNames.append(d)
        for f in fileNames:
            fileAndDirectoryNames.append(f)
    
    def readDirectoryAll(_path): 
        tFileAndDirs=[]
        for name in listDir(_path):
            try:tFileAndDirs.append(name.decode(systemsCharSet))
            except:tFileAndDirs.append(name)
        return tFileAndDirs
  
    def readDirectoryWithSubDirectories(_path, _subDirectoryDeep=-1, _isGetDirectoryNames=False, _currentSubDeep=0):
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
                        for dd in readDirectoryWithSubDirectories(_path+"/"+name, _subDirectoryDeep, _isGetDirectoryNames, _currentSubDeep+1):
                            allFilesAndDirectories.append(dd)
                else:
                    allFilesAndDirectories.append(_path+"/"+name)
        return allFilesAndDirectories
    
    def readFromFile(_path):
        _path = str(_path)
        try:f = open(_path.encode(systemsCharSet))
        except:f = open(_path)
        info = f.read()
        f.close()
        return info
        
    def readLinesFromFile(_path):
        _path = str(_path)
        try:f = open(_path.encode(systemsCharSet))
        except:f = open(_path)
        info = f.readlines()
        f.close()
        return info
        
    def readFromBinaryFile(_path):
        _path = str(_path)
        try:f = open(_path.encode(systemsCharSet), "rb")
        except:f = open(_path, "rb")
        info = f.read()
        f.close()
        return info
        
    def writeToFile(_path, _contents=""):
        _path = str(_path)
        try:f = open(_path.encode(systemsCharSet), "w")
        except:f = open(_path, "w")
        f.write(_contents)
        f.close()
        Records.add("Writed", _path)
        
    def writeToBinaryFile(_path, _contents=""):
        _path = str(_path)
        try:f = open(_path.encode(systemsCharSet), "wb")
        except:f = open(_path, "w")
        f.write(_contents)
        f.flush()
        f.close()
        Records.add("Writed", _path)
    
    def addToFile(_path, _contents=""):
        _path = str(_path)
        try:f = open(_path.encode(systemsCharSet), "a")
        except:f = open(_path, "w")
        f.write(_contents)
        f.close()
        Records.add("Added", _path)
    
    def readTextFile(_path):
        return [getDirName(_path), getBaseName(_path), readFromFile(_path)]  
        
    def writeTextFile(_oldFileValues, _newFileValues, _charSet="utf-8"):
        if _oldFileValues[2]!=_newFileValues[2] or _charSet!="utf-8":
            writeToFile(_oldFileValues[0]+"/"+_oldFileValues[1], _newFileValues[2].encode(_charSet))
        newFileName=_oldFileValues[1]
        if _oldFileValues[1]!=_newFileValues[1]:
            if _newFileValues[1].strip()!="":
                if _oldFileValues[1].find(".")!=-1:
                    orgExt = _oldFileValues[1].split(".")[-1].decode("utf-8").lower()
                    if _newFileValues[1].split(".")[-1].decode("utf-8").lower() != orgExt:
                        _newFileValues[1] = _newFileValues[1].split(".")[-1] + "." + orgExt
                    if _newFileValues[1].split(".")[-1] != orgExt:
                        extState = _newFileValues[1].lower().find(orgExt)
                        if extState!=-1:
                            _newFileValues[1] = _newFileValues[1].split(".")[-1][:extState] + "." + orgExt
                if moveOrChange(_oldFileValues[0]+"/"+_oldFileValues[1],_oldFileValues[0]+"/"+_newFileValues[1])==True:
                    newFileName=_newFileValues[1]
        newDirectory=_newFileValues[0].replace(getDirName(_oldFileValues[0])+"/","")
        try:
            newDirectory=str(newDirectory)
            newDirectory=int(newDirectory)
        except:
            if newDirectory.decode("utf-8").lower()==newDirectory.upper():
                newDirectory=_oldFileValues[0]
        if getBaseName(_oldFileValues[0])!=newDirectory:
            if moveOrChange(_oldFileValues[0]+"/"+newFileName,path.dirname(_oldFileValues[0])+"/"+newDirectory+"/"+newFileName)==True:
                return getDirName(_oldFileValues[0])+"/"+newDirectory+"/"+newFileName
        return _oldFileValues[0]+"/"+_oldFileValues[1]
                
    def clearEmptyDirectories(_path, _isShowState=False, _isCloseState=False, _isAutoCleanSubFolder=True):
        #If directory deleted : returned True
        #If directory cleaned : returned False
        from MyObjects import translate
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
            if _isShowState: Dialogs.showState(translate("InputOutputs", "Deleting Empty Directories"), 0, 1)
            clearIgnoreds(_path)
            removeDir(_path)
            if _isCloseState: 
                Dialogs.showState(translate("InputOutputs", "Empty Directories Deleted"), 1, 1)
                Dialogs.show(translate("InputOutputs", "Directory Deleted"), str(translate("InputOutputs", "\"%s\" deleted.Because this directory is empty.")) % Organizer.getLink(_path))
            return True
        if _isCloseState: Dialogs.showState(translate("InputOutputs", "Empty Directories Deleted"), 1, 1)
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
            for tDir in appendingDirectories:
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
            return getBaseName(_oldPath)
            
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
            for tDir in appendingDirectories:
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
            return getBaseName(_oldPath)
    
    def changeDirectories(_values):
        #will return directory(new) name
        from MyObjects import translate
        import Dialogs
        if len(_values)!=0:
            Dialogs.showState(translate("InputOutputs", "Changing The Folder (Of The Files)"),0,len(_values))
            for no in range(0,len(_values)):
                moveOrChange(_values[no][0], _values[no][1], getObjectType(_values[no][0]))
                Dialogs.showState(translate("InputOutputs", "Changing The Folder (Of The Files)"),no+1,len(_values))
            if Universals.getBoolValue("isClearEmptyDirectoriesWhenFileMove"):
                if isDir(currentDirectoryPath):
                    if clearEmptyDirectories(currentDirectoryPath, True, True, Universals.getBoolValue("isAutoCleanSubFolderWhenFileMove")):
                        return getDirName(currentDirectoryPath)
            if Universals.getBoolValue("isAutoMakeIconToDirectoryWhenFileMove"):
                if isDir(currentDirectoryPath):
                    checkIcon(currentDirectoryPath)
        return currentDirectoryPath
        
    def getSearchEnginesNames():
        engines = []
        for name in readDirectoryAll(Universals.HamsiManagerDirectory+"/SearchEngines"):
            if name[:1] != "." and isDir(Universals.HamsiManagerDirectory+"/SearchEngines"+"/"+name):
                engines.append(name)
        return engines
        
    def getMyPluginsNames():
        plugins = []
        for name in readDirectoryAll(Universals.HamsiManagerDirectory+"/MyPlugins"):
            if name[:1] != "." and isDir(Universals.HamsiManagerDirectory+"/MyPlugins"+"/"+name):
                plugins.append(name)
        return plugins
        
    def getInstalledThemes():
        themes = []
        for name in readDirectoryAll(Universals.HamsiManagerDirectory+"/Themes"):
            if name[:1] != "." and isDir(Universals.HamsiManagerDirectory+"/Themes"+"/"+name):
                themes.append(name)
        return themes
    
    def getInstalledLanguagesCodes():
        languages = []
        for name in readDirectoryAll(Universals.HamsiManagerDirectory+"/Languages"):
            if isFile(Universals.HamsiManagerDirectory+"/Languages"+"/"+name) and name[-3:]==".qm":
                langCode = name[-8:-3]
                if languages.count(langCode)==0:
                    languages.append(langCode)
        if languages.count("en_GB")==0:
            languages.append("en_GB")
        return languages
        
    def getInstalledLanguagesNames():
        from MyObjects import MLocale
        languages = []
        for name in readDirectoryAll(Universals.HamsiManagerDirectory+"/Languages"):
            if isFile(Universals.HamsiManagerDirectory+"/Languages"+"/"+name) and name[-3:]==".qm":
                langCode = name[-8:-3]
                if languages.count(str(MLocale.languageToString(MLocale(langCode).language())))==0:
                    languages.append(str(MLocale.languageToString(MLocale(langCode).language())))
        if languages.count("English")==0:
            languages.append("English")
        return languages

    def activateSmartCheckIcon():
        global isSmartCheckIcon, willCheckIconDirectories
        isSmartCheckIcon = True
        willCheckIconDirectories = []
    
    def complateSmartCheckIcon():
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
                return setIconToDirectory(_path, getFirstImageInDirectory(_path))
            elif _isClear:
                return setIconToDirectory(_path)
    
    def getFirstImageInDirectory(_path, _coverNameIfExist=None, _isCheckDelete=False, _isAsk=True):
        import Dialogs
        from MyObjects import translate
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
        if _isAsk and eval(Universals.MySettings["isAskIfHasManyImagesInAlbumDirectory"].title())==True and len(imageFiles)>1:
            selectedIndex = 0
            if cover!=None:
                selectedIndex = imageFiles.index(cover)
            cover = str(Dialogs.select(translate("InputOutputs", "Select A Cover"), str(translate("InputOutputs", "Please select a cover for \"%s\".<br>Note: If you cancel the first image will be chosen.")) % (Organizer.getLink(_path)), imageFiles, selectedIndex))
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
        if _iconName==None:
            return False
        _iconName = str(_iconName).strip()
        returnValue, isChanging, isChange, isCorrectFileContent = False, False, True, False
        if _iconName!="":
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
                    rows[rowNo] = "Icon=./" + _iconName 
                    returnValue = True
            if isChange:
                if isChanging==False:
                    rows.append("Icon=./" + _iconName)
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
          
    def clearPackagingDirectory(_path, _isShowState=False, _isCloseState=False):
        from MyObjects import translate
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
        from MyObjects import translate
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
        import tarfile
        from MyObjects import translate
        import Dialogs
        _filePath, _sourcePath = str(_filePath), str(_sourcePath)
        if isDir(_filePath):
            Dialogs.showError(translate("InputOutputs", "Current Directory Name"),
                        str(translate("InputOutputs", "\"%s\" : there already exists a folder with the same name.<br>Please choose another file name!")) % Organizer.getLink(_filePath))
            return False
        try:tar = tarfile.open(_filePath.encode(systemsCharSet), "w:" + _packageType)
        except:tar = tarfile.open(_filePath, "w:" + _packageType)
        try:tar.add(_sourcePath.encode(systemsCharSet), "")
        except:tar.add(_sourcePath, "")
        tar.close()
        Records.add("Packed", _filePath)
        return True
        
    def extractPack(_oldPath, _newPath):
        _oldPath, _newPath = str(_oldPath), str(_newPath)
        import tarfile
        while 1==1:
            try:
                try:tar = tarfile.open(_oldPath.encode(systemsCharSet), "r:gz")
                except:tar = tarfile.open(_oldPath, "r:gz")
                break
            except:
                time.sleep(1)
        try:tar.extractall(_newPath.encode(systemsCharSet), members=tar.getmembers())
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
                    
    def getFileTree(_path, _subDirectoryDeep=-1, _actionType="return", _formatType="html", _extInfo="no"):
        _path = str(_path)
        from MyObjects import translate
        files = readDirectoryWithSubDirectories(_path, _subDirectoryDeep, True)
        info = ""
        for x in range(len(files)):
            files[x] = files[x].decode(systemsCharSet)
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
                    replaceStrings.append(("│&nbsp;&nbsp;&nbsp;"*(file.count("/")-dirNumber))+"├&nbsp;")
            findStrings.reverse()
            replaceStrings.reverse()
            fileList = range(len(files))
            for x, file in enumerate(files):
                fileList[x] = file + "<br> \n"
                for  y, fstr in enumerate(findStrings):
                    if file!=fstr:
                        fileList[x] = fileList[x].replace(fstr + "/", replaceStrings[y])
                if x>0:
                    tin = fileList[x-1].find("├")
                    tin2 = fileList[x].find("├")
                    if tin>tin2:
                        fileList[x-1] = fileList[x-1].replace("├", "└")
            for x, fileName in enumerate(fileList):
                if x!=len(fileList)-1:
                    info += fileName.replace(_path + "/", "├&nbsp;")
                else:
                    info += fileName.replace(_path + "/", "└&nbsp;")
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
                    replaceStrings.append(("│   "*(file.count("/")-dirNumber))+"├ ")
            findStrings.reverse()
            replaceStrings.reverse()
            fileList = range(len(files))
            for x, file in enumerate(files):
                fileList[x] = file + "\n"
                for  y, fstr in enumerate(findStrings):
                    if file!=fstr:
                        fileList[x] = fileList[x].replace(fstr + "/", replaceStrings[y])
                if x>0:
                    tin = fileList[x-1].find("├")
                    tin2 = fileList[x].find("├")
                    if tin>tin2:
                        fileList[x-1] = fileList[x-1].replace("├", "└")
            for x, fileName in enumerate(fileList):
                if x!=len(fileList)-1:
                    info += fileName.replace(_path + "/", "├ ")
                else:
                    info += fileName.replace(_path + "/", "└ ")
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
                                    Universals.userDirectoryPath.decode("utf-8"),formatTypeName+u" (*."+fileExt.decode("utf-8")+")")
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
            from MyObjects import MDialog, MWidget, MVBoxLayout, MTextEdit, MPushButton, MObject, SIGNAL
            dDialog = MDialog(Universals.MainWindow)
            if Universals.isActivePyKDE4==True:
                dDialog.setButtons(MDialog.None)
            dDialog.setWindowTitle(translate("Tables", "File Tree"))
            mainPanel = MWidget(dDialog)
            vblMain = MVBoxLayout(mainPanel)
            if _formatType=="html":
                from PyQt4 import QtWebKit
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
            if _hashType=="MD5":
                import md5
                return md5.new(readFromBinaryFile(_filePath)).hexdigest()
            elif _hashType=="SHA-1":
                import sha
                return sha.new(readFromBinaryFile(_filePath)).hexdigest()
        except:
            return False
        
    def createHashDigestFile(_filePath, _digestFilePath=None, _hashType="MD5", _isAddFileExtension=True):
        digestContent = getHashDigest(_filePath, _hashType)
        fileExtension = ""
        if _isAddFileExtension:
            if _hashType=="MD5":
                fileExtension = "md5"
            elif _hashType=="SHA-1":
                fileExtension = "sha1"
        if _digestFilePath==None:
            _digestFilePath = _filePath
        writeToFile(_digestFilePath + fileExtension, digestContent)
        return True
        
        
