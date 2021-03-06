# This file is part of HamsiManager.
#
# Copyright (c) 2010 - 2015 Murat Demir <mopened@gmail.com>
#
# Hamsi Manager is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Hamsi Manager is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with HamsiManager; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA


import os
import sys
import shutil
import stat
import re
import tempfile
import mimetypes
from Core.MyObjects import *
from Core import Universals as uni
from Core import Records
from Core import Organizer
from Core import Dialogs

appendingDirectories = []
defaultFileSystemEncoding = None
fileSystemEncoding = None
willCheckIconDirectories = []
willCheckEmptyDirectories = []
willCheckEmptyDirectoriesSubDirectoryStatus = []
isSmartCheckIcon = False
isSmartCheckEmptyDirectories = False
sep = os.sep

executableAppPath, userDirectoryPath, HamsiManagerDirectory = None, None, None
themePath, pathOfSettingsDirectory, recordFilePath, oldRecordsDirectoryPath = None, None, None, None


def initStartupVariables():
    global executableAppPath, userDirectoryPath, HamsiManagerDirectory
    global themePath, pathOfSettingsDirectory, recordFilePath, oldRecordsDirectoryPath
    initFileSystemEncoding()
    executableAppPath = str(os.path.abspath(sys.argv[0]))
    if isLink(executableAppPath):
        executableAppPath = readLink(executableAppPath)
    HamsiManagerDirectory = getDirName(executableAppPath)
    userDirectoryPath = os.path.expanduser("~")
    try: userDirectoryPath = uni.trDecode(userDirectoryPath, fileSystemEncoding)
    except: pass
    themePath = joinPath(HamsiManagerDirectory, "Themes", "Default")
    pathOfSettingsDirectory = joinPath(userDirectoryPath, ".HamsiApps", "HamsiManager")
    recordFilePath = joinPath(pathOfSettingsDirectory, "logs.txt")
    oldRecordsDirectoryPath = joinPath(pathOfSettingsDirectory, "OldRecords")


def initFileSystemEncoding():
    global defaultFileSystemEncoding, fileSystemEncoding
    defaultFileSystemEncoding = sys.getfilesystemencoding()
    if defaultFileSystemEncoding is None:
        defaultFileSystemEncoding = sys.getdefaultencoding()
    defaultFileSystemEncoding = defaultFileSystemEncoding.lower()
    from encodings import aliases

    if defaultFileSystemEncoding == "iso-8859-1":
        defaultFileSystemEncoding = "latin-1"
    if [str(v).lower().replace("_", "-") for k, v in aliases.aliases.items()].count(defaultFileSystemEncoding) == 0:
        defaultFileSystemEncoding = sys.getfilesystemencoding().lower()
    fileSystemEncoding = str(defaultFileSystemEncoding)


def joinPath(_a, *_b):
    _a = str(_a)
    c = []
    for x in _b:
        try: c.append(uni.trEncode(str(x), fileSystemEncoding))
        except: c.append(str(x))
    c = tuple(c)
    try: returnValue = os.path.join(uni.trEncode(_a, fileSystemEncoding), *c)
    except: returnValue = os.path.join(_a, *c)
    try: return uni.trDecode(returnValue, fileSystemEncoding)
    except: return returnValue


def splitPath(_a):
    _a = str(_a)
    try: returnValue = os.path.split(uni.trEncode(_a, fileSystemEncoding))
    except: returnValue = os.path.split(_a)
    c = []
    for x in returnValue:
        try: c.append(uni.trDecode(x, fileSystemEncoding))
        except: c.append(x)
    return c


def isFile(_oldPath):
    _oldPath = str(_oldPath)
    try: return os.path.isfile(uni.trEncode(_oldPath, fileSystemEncoding))
    except: return os.path.isfile(_oldPath)


def isDir(_oldPath):
    _oldPath = str(_oldPath)
    try: return os.path.isdir(uni.trEncode(_oldPath, fileSystemEncoding))
    except: return os.path.isdir(_oldPath)


def isLink(_oldPath):
    _oldPath = str(_oldPath)
    try: return os.path.islink(uni.trEncode(_oldPath, fileSystemEncoding))
    except: return os.path.islink(_oldPath)


def isDirEmpty(_oldPath):
    _oldPath = str(_oldPath)
    if isDir(_oldPath):
        if len(listDir(_oldPath)) == 0:
            return True
    return False


def isExist(_oldPath):
    if isFile(_oldPath):
        return True
    elif isDir(_oldPath):
        return True
    elif isLink(_oldPath):
        return True
    return False


def isHidden(_path, _name=None):
    if _name is None:
        _name = getBaseName(_path)
    if _name.startswith('.'):
        return True
    if _path.count(sep + '.') > 0:
        return True
    if uni.isWindows:
        try:
            import win32api, win32con

            try: attr = win32api.GetFileAttributes(uni.trEncode(_path, fileSystemEncoding))
            except: attr = win32api.GetFileAttributes(_path)
            if attr & win32con.FILE_ATTRIBUTE_HIDDEN:
                return True
        except:
            return False
    return False


def isBinary(_path):
    _path = str(_path)
    try: f = open(uni.trEncode(_path, fileSystemEncoding), 'rb')
    except: f = open(_path, 'rb')
    try:
        chunk = f.read(1024)
        f.close()
        if '\0' in chunk:  # found null byte
            return True
        else:
            printableExtendedAscii = b'\n\r\t\f\b'
            if bytes is str:
                printableExtendedAscii += b''.join(map(chr, range(32, 256)))
            else:
                printableExtendedAscii += bytes(range(32, 256))
            control_chars = chunk.translate(None, printableExtendedAscii)
            nontext_ratio = float(len(control_chars)) / float(len(chunk))
            return nontext_ratio > 0.3
    except:
        pass
    return False


def isAvailableNameForEncoding(_newPath):
    try:
        _newPath = str(_newPath)
        t = uni.trEncode(_newPath, fileSystemEncoding)
        return True
    except:
        return False


def getAvailablePathByPath(_newPath):
    _newPath = getRealPath(str(_newPath))
    newPath = ""
    isFirstPart = True
    for pathPart in _newPath.split(sep):
        if pathPart != "":
            badchars = re.compile(r'[/]')
            pathPart = badchars.sub('_', pathPart)
            if uni.isWindows:
                if isFirstPart:
                    pathPart += sep
                else:
                    badchars = re.compile(r'[^A-Za-z0-9_.\- \w\s]+|\.$|^ | $|^$', re.U)
                    pathPart = re.sub(badchars, '_', uni.trUnicode(pathPart), re.U)
                    badnames = re.compile(r'(aux|com[1-9]|con|lpt[1-9]|prn)(\.|$)')
                    if badnames.match(pathPart):
                        pathPart = "_" + pathPart
            newPath = joinPath(newPath, pathPart)
        else:
            newPath += sep
        isFirstPart = False
    return newPath


def getAvailableNameByName(_newPath):
    _newPath = str(_newPath)
    newPath = ""
    pathParts = _newPath.split(sep)
    for pathPart in pathParts:
        if pathPart != "":
            badchars = re.compile(r'[/]')
            pathPart = badchars.sub('_', pathPart)
            if uni.isWindows:
                badchars = re.compile(r'[^A-Za-z0-9_.\- \w\s]+|\.$|^ | $|^$', re.U)
                pathPart = re.sub(badchars, '_', uni.trUnicode(pathPart), re.U)
                badnames = re.compile(r'(aux|com[1-9]|con|lpt[1-9]|prn)(\.|$)')
                if badnames.match(pathPart):
                    pathPart = "_" + pathPart
            newPath = joinPath(newPath, pathPart)
        else:
            newPath += sep
    return newPath


def getSize(_oldPath):
    try: return os.path.getsize(uni.trEncode(_oldPath, fileSystemEncoding))
    except: return os.path.getsize(_oldPath)


def getMimeType(_oldPath):
    try: return mimetypes.guess_type(uni.trEncode(_oldPath, fileSystemEncoding))
    except: return mimetypes.guess_type(_oldPath)


def getDirectorySize(_oldPath):
    total_size = 0
    names = walk(_oldPath)
    if names is not None:
        for dirpath, dirnames, filenames in names:
            for f in filenames:
                total_size += getSize(joinPath(dirpath, f))
    return total_size


def getDetails(_oldPath):
    try: return os.stat(uni.trEncode(_oldPath, fileSystemEncoding))
    except:
        try: return os.stat(_oldPath)
        except: return None


def getExtendedDetails(_oldPath):
    details = getDetails(_oldPath)
    extendedDetails = {}
    if details is not None:
        extendedDetails["accessRights"] = oct(stat.S_IMODE(details[stat.ST_MODE]))
        extendedDetails["numberOfHardLinks"] = details[stat.ST_NLINK]
        extendedDetails["userIDOfOwner"] = details[stat.ST_UID]
        extendedDetails["groupIDOfOwner"] = details[stat.ST_GID]
        extendedDetails["size"] = details[stat.ST_SIZE]
        extendedDetails["lastAccessed"] = details[stat.ST_ATIME]
        extendedDetails["lastModified"] = details[stat.ST_MTIME]
        extendedDetails["lastMetadataChanged"] = details[stat.ST_CTIME]
        extendedDetails["userNameOfOwner"] = uni.getUserNameByID(details[stat.ST_UID])
        extendedDetails["longUserNameOfOwner"] = uni.getUserLongNameByID(details[stat.ST_UID])
        extendedDetails["groupNameOfOwner"] = uni.getGroupNameByID(details[stat.ST_GID])
    else:
        extendedDetails["accessRights"] = ""
        extendedDetails["numberOfHardLinks"] = ""
        extendedDetails["userIDOfOwner"] = ""
        extendedDetails["groupIDOfOwner"] = ""
        extendedDetails["size"] = "0"
        extendedDetails["lastAccessed"] = None
        extendedDetails["lastModified"] = None
        extendedDetails["lastMetadataChanged"] = None
        extendedDetails["userNameOfOwner"] = ""
        extendedDetails["longUserNameOfOwner"] = ""
        extendedDetails["groupNameOfOwner"] = ""
    return extendedDetails


def getObjectType(_oldPath):
    objectType = "file"
    if isDir(_oldPath):
        objectType = "directory"
    return objectType


def getDirName(_oldPath):
    _oldPath = str(_oldPath)
    try: returnValue = os.path.dirname(uni.trEncode(_oldPath, fileSystemEncoding))
    except: returnValue = os.path.dirname(_oldPath)
    try: return uni.trDecode(returnValue, fileSystemEncoding)
    except: return returnValue


def readLink(_oldPath):
    _oldPath = str(_oldPath)
    try: returnValue = os.readlink(uni.trEncode(_oldPath, fileSystemEncoding))
    except: returnValue = os.readlink(_oldPath)
    try: return uni.trDecode(returnValue, fileSystemEncoding)
    except: return returnValue


def getRealDirName(_oldPath, isGetParent=False):
    _oldPath = str(_oldPath)
    if len(_oldPath) == 0:
        if uni.isWindows: return "C:" + sep
        return sep
    if _oldPath[-1] == sep:
        _oldPath = _oldPath[:-1]
    if isGetParent:
        realDirName = getDirName(str(_oldPath))
    else:
        realDirName = str(_oldPath)
    while 1:
        if isDir(realDirName):
            break
        if realDirName == "":
            if uni.isWindows: realDirName = "C:" + sep
            else: realDirName = sep
            break
        realDirName = getDirName(realDirName)
    return realDirName


def getRealPath(_path, _parentPath=None):
    _path = str(_path)
    if uni.isWindows:
        _path = _path.replace("\\", sep).replace("/", sep)
    if len(_path) == 0:
        if uni.isWindows: return "C:" + sep
        return sep
    if _parentPath is not None:
        _parentPath = getRealPath(_parentPath)
        if _path[:2] == "." + sep:
            _path = _parentPath + _path[1:]
        if _path[:3] == ".." + sep:
            _path = getDirName(_parentPath) + _path[2:]
    return os.path.abspath(_path)


def getShortPath(_path, _parentPath):
    _path = str(_path)
    _parentPath = str(_parentPath)
    _path = _path.replace(_parentPath, ".")
    return _path


def getBaseName(_oldPath):
    _oldPath = str(_oldPath)
    try: returnValue = os.path.basename(uni.trEncode(_oldPath, fileSystemEncoding))
    except: returnValue = os.path.basename(_oldPath)
    try: return uni.trDecode(returnValue, fileSystemEncoding)
    except: return returnValue


def getTempDir():
    returnValue = tempfile.gettempdir()
    try: return uni.trDecode(returnValue, fileSystemEncoding)
    except: return returnValue


def checkExtension(_oldPath, _extension):
    _oldPath = str(_oldPath).lower()
    _extension = str(_extension).lower()
    if _extension.strip() != "":
        if _extension[0] == ".":
            _extension = _extension[1:]
        extIndex = _oldPath.find("." + _extension)
        if extIndex != -1:
            if _oldPath[extIndex:] == "." + _extension:
                return True
    return False


def getFileExtension(_fileName):
    _fileName = str(_fileName).lower()
    if _fileName.find(".") != -1:
        if uni.MySettings["fileExtensionIs"] == uni.fileExtensionIsKeys[0]:
            return _fileName.split(".", 1)[1]
        elif uni.MySettings["fileExtensionIs"] == uni.fileExtensionIsKeys[1]:
            return _fileName.rsplit(".", 1)[1]
        elif uni.MySettings["fileExtensionIs"] == uni.fileExtensionIsKeys[2]:
            try:
                m = re.compile(r'^.*?[.](?P<ext>tar\.gz|tar\.bz2|\w+)$').match(_fileName)
                if m is not None:
                    return m.group('ext')
            except:
                return _fileName.rsplit(".", 1)[1]
            return _fileName.rsplit(".", 1)[1]
    return ""


def getFileNameParts(_fileNameOrPath):
    _fileName = getBaseName(str(_fileNameOrPath))
    fileName, fileExtension = "", ""
    if _fileName.find(".") != -1:
        fParts = [_fileName, fileExtension]
        if uni.MySettings["fileExtensionIs"] == uni.fileExtensionIsKeys[0]:
            fParts = _fileName.split(".", 1)
        elif uni.MySettings["fileExtensionIs"] == uni.fileExtensionIsKeys[1]:
            fParts = _fileName.rsplit(".", 1)
        elif uni.MySettings["fileExtensionIs"] == uni.fileExtensionIsKeys[2]:
            try:
                m = re.compile(r'^.*?[.](?P<ext>tar\.gz|tar\.bz2|\w+)$').match(_fileName)
                if m is not None:
                    ext = m.group('ext')
                else:
                    ext = _fileName.rsplit(".", 1)[1]
                fParts = [_fileName.replace("." + ext, ""), ext]
            except:
                fParts = _fileName.rsplit(".", 1)
        fileName = fParts[0]
        fileExtension = fParts[1]
    else:
        fileName = _fileName
    return fileName, fileExtension.lower()


def moveFileOrDir(_oldPath, _newPath, _isQuiet=True):
    _oldPath, _newPath = str(_oldPath), str(_newPath)
    if uni.isWindows:
        _oldPath = _oldPath.replace("\\", sep).replace("/", sep)
        _newPath = _newPath.replace("\\", sep).replace("/", sep)
    try:
        if getDirName(_oldPath) == getDirName(_newPath) or (
                uni.isWindows and Organizer.makeCorrectCaseSensitive(_oldPath, uni.validSentenceStructureKeys[
                1]) == Organizer.makeCorrectCaseSensitive(_newPath, uni.validSentenceStructureKeys[1])):
            try: os.rename(uni.trEncode(_oldPath, fileSystemEncoding), uni.trEncode(_newPath, fileSystemEncoding))
            except: os.rename(_oldPath, _newPath)
        else:
            if isDir(getDirName(_newPath)) is False:
                makeDirs(getDirName(_newPath))
            try: shutil.move(uni.trEncode(_oldPath, fileSystemEncoding), uni.trEncode(_newPath, fileSystemEncoding))
            except: shutil.move(_oldPath, _newPath)
        Records.add("Moved", _oldPath, _newPath)
    except:
        if _isQuiet is False:
            answer = Dialogs.askSpecial(translate("FileUtils", "An Error Has Occurred"),
                                        str(translate("FileUtils",
                                                      "\"%s\" > \"%s\" : an unknown error has occurred.<br>Please check it and try again.")) % (
                                            Organizer.getLink(_oldPath), Organizer.getLink(_newPath)),
                                        translate("Dialogs", "Cancel"),
                                        translate("Dialogs", "Show Error Details"),
                                        translate("Dialogs", "Retry"))
            if answer == translate("Dialogs", "Retry"):
                moveFileOrDir(_oldPath, _newPath, _isQuiet)
            if answer == translate("Dialogs", "Show Error Details"):
                from Core import ReportBug

                ReportBug.ReportBug()
        else:
            from Core import ReportBug

            ReportBug.ReportBug()


def copyFileOrDir(_oldPath, _newPath):
    _oldPath, _newPath = str(_oldPath), str(_newPath)
    if isDir(getDirName(_newPath)) is False:
        makeDirs(getDirName(_newPath))
    if isFile(_oldPath):
        try: shutil.copy(uni.trEncode(_oldPath, fileSystemEncoding), uni.trEncode(_newPath, fileSystemEncoding))
        except: shutil.copy(_oldPath, _newPath)
    else:
        copyDirTree(_oldPath, _newPath)
    Records.add("Copied", _oldPath, _newPath)


def copyDirTree(_oldPath, _newPath):
    _oldPath, _newPath = str(_oldPath), str(_newPath)
    try: shutil.copytree(uni.trEncode(_oldPath, fileSystemEncoding), uni.trEncode(_newPath, fileSystemEncoding))
    except: shutil.copytree(_oldPath, _newPath)
    Records.add("Copied", _oldPath, _newPath)


def copyDirContent(_oldPath, _newPath):
    _oldPath, _newPath = str(_oldPath), str(_newPath)
    if isDir(_newPath) is False:
        makeDirs(_newPath)
    for contentPath in listDir(_oldPath):
        if isDir(joinPath(_oldPath, contentPath)):
            copyDirContent(joinPath(_oldPath, contentPath), joinPath(_newPath, contentPath))
        else:
            copyFileOrDir(joinPath(_oldPath, contentPath), joinPath(_newPath, contentPath))


def createSymLink(_oldPath, _newPath):
    _oldPath, _newPath = str(_oldPath), str(_newPath)
    if uni.isAvailableSymLink():
        from os import symlink

        if isExist(_newPath):
            removeFileOrDir(_newPath)
        try: symlink(uni.trEncode(_oldPath, fileSystemEncoding), uni.trEncode(_newPath, fileSystemEncoding))
        except: symlink(_oldPath, _newPath)
        Records.add("Created Link", _oldPath, _newPath)
        return True
    else:
        Records.add("Can Not Created Link", _oldPath, _newPath)
        copyOrChange(_oldPath, _newPath, getObjectType(_oldPath))
        return False


def listDir(_oldPath):
    names = []
    _oldPath = checkSource(_oldPath, "directory")
    if _oldPath is not None:
        try: names = os.listdir(uni.trEncode(_oldPath, fileSystemEncoding))
        except: names = os.listdir(_oldPath)
        names.sort(key=trSort)
    return names


def walk(_oldPath):
    names = None
    _oldPath = checkSource(_oldPath, "directory")
    if _oldPath is not None:
        try: names = os.walk(uni.trEncode(_oldPath, fileSystemEncoding))
        except: names = os.walk(_oldPath)
    return names


def makeDirs(_newPath):
    if isWritableFileOrDir(getRealDirName(_newPath)):
        try: os.makedirs(uni.trEncode(_newPath, fileSystemEncoding))
        except: os.makedirs(_newPath)
        Records.add("Created", _newPath)
        return True
    return False


def onRMTreeError(_func, _path, _excInfo):
    try: os.chmod(uni.trEncode(getDirName(_path), fileSystemEncoding),
                  stat.S_IWRITE | stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
    except: os.chmod(getDirName(_path), stat.S_IWRITE | stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
    Records.add("CHmod Changed To Remove", getDirName(_path))
    try: os.chmod(uni.trEncode(_path, fileSystemEncoding), stat.S_IWRITE | stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
    except: os.chmod(_path, stat.S_IWRITE | stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)
    Records.add("CHmod Changed To Remove", _path)
    try: os.unlink(uni.trEncode(_path, fileSystemEncoding))
    except: os.unlink(_path)
    Records.add("Removed", _path)


def removeDir(_oldPath):
    if uni.getBoolValue("isDontDeleteFileAndDirectory"):
        moveToPathOfDeleted(_oldPath)
    else:
        try: shutil.rmtree(uni.trEncode(_oldPath, fileSystemEncoding), ignore_errors=False, onerror=onRMTreeError)
        except: shutil.rmtree(_oldPath, ignore_errors=False, onerror=onRMTreeError)
    Records.add("Removed", _oldPath)
    return True


def removeFile(_oldPath):
    if uni.getBoolValue("isDontDeleteFileAndDirectory"):
        moveToPathOfDeleted(_oldPath)
    else:
        try: os.remove(uni.trEncode(_oldPath, fileSystemEncoding))
        except: os.remove(_oldPath)
    Records.add("Removed", _oldPath)
    return True


def moveToPathOfDeleted(_oldPath):
    from time import strftime
    import random

    moveFileOrDir(_oldPath, joinPath(uni.MySettings["pathOfDeletedFilesAndDirectories"],
                                     strftime("%Y%m%d_%H%M%S") + "_" + str(
                                         random.randrange(0, 9999999)) + "_" + getBaseName(_oldPath)))


def trSort(_info):
    import locale

    if uni.isPython3k:
        _info = str(_info)
    try:
        return locale.strxfrm(uni.trEncode(_info, fileSystemEncoding))
    except:
        return locale.strxfrm(_info)


def isReadableFileOrDir(_newPath, _isOnlyCheck=False, _isInLoop=False):
    realPath = _newPath
    if isFile(realPath) is False:
        realPath = getRealDirName(realPath)
    try:
        if os.access(uni.trEncode(realPath, fileSystemEncoding), os.R_OK):
            return True
    except:
        if os.access(realPath, os.R_OK):
            return True
    if _isOnlyCheck is False:
        if _isInLoop:
            okButtonLabel = translate("Dialogs", "Continue")
        else:
            okButtonLabel = translate("Dialogs", "OK")
        if isDir(realPath):
            answer = Dialogs.askSpecial(translate("FileUtils", "Access Denied"),
                                        str(translate("FileUtils",
                                                      "\"%s\" : you do not have the necessary permissions to read this directory.<br>Please check your access controls and retry.")) % Organizer.getLink(
                                            realPath),
                                        okButtonLabel,
                                        translate("Dialogs", "Retry"))
            if answer == translate("Dialogs", "Retry"):
                return isReadableFileOrDir(_newPath, _isOnlyCheck, _isInLoop)
        else:
            answer = Dialogs.askSpecial(translate("FileUtils", "Access Denied"),
                                        str(translate("FileUtils",
                                                      "\"%s\" : you do not have the necessary permissions to read this file.<br>Please check your access controls and retry.")) % Organizer.getLink(
                                            realPath),
                                        okButtonLabel,
                                        translate("Dialogs", "Retry"))
            if answer == translate("Dialogs", "Retry"):
                return isReadableFileOrDir(_newPath, _isOnlyCheck, _isInLoop)
    return False


def isWritableFileOrDir(_newPath, _isOnlyCheck=False, _isInLoop=False):
    realPath = _newPath
    if isFile(realPath) is False:
        realPath = getRealDirName(realPath)
    try:
        if os.access(uni.trEncode(realPath, fileSystemEncoding), os.W_OK):
            return True
    except:
        if os.access(realPath, os.W_OK):
            return True
    if _isOnlyCheck is False:
        if _isInLoop:
            okButtonLabel = translate("Dialogs", "Continue")
        else:
            okButtonLabel = translate("Dialogs", "OK")
        if isDir(realPath):
            answer = Dialogs.askSpecial(translate("FileUtils", "Access Denied"),
                                        str(translate("FileUtils",
                                                      "\"%s\" : you do not have the necessary permissions to change this directory.<br>Please check your access controls and retry.")) % Organizer.getLink(
                                            realPath),
                                        okButtonLabel,
                                        translate("Dialogs", "Retry"))
            if answer == translate("Dialogs", "Retry"):
                return isWritableFileOrDir(_newPath, _isOnlyCheck, _isInLoop)
        else:
            answer = Dialogs.askSpecial(translate("FileUtils", "Access Denied"),
                                        str(translate("FileUtils",
                                                      "\"%s\" : you do not have the necessary permissions to change this file.<br>Please check your access controls and retry.")) % Organizer.getLink(
                                            realPath),
                                        okButtonLabel,
                                        translate("Dialogs", "Retry"))
            if answer == translate("Dialogs", "Retry"):
                return isWritableFileOrDir(_newPath, _isOnlyCheck, _isInLoop)
    return False


def checkSource(_oldPath, _objectType="fileAndDirectory", _isShowAlert=True):
    oldPath = str(_oldPath)
    if uni.isWindows:
        _oldPath = _oldPath.replace("\\", sep).replace("/", sep)
    if _objectType == "file" and isFile(oldPath):
        return oldPath
    elif _objectType == "directory" and isDir(oldPath):
        return oldPath
    elif _objectType == "fileAndDirectory" and (isDir(oldPath) or isFile(oldPath)):
        return oldPath
    if uni.isWindows:
        oldPath = "\\\\?\\" + oldPath  # for wrong name such as "C:\Temp \test.txt", "C:\Temp\test.txt "
        if _objectType == "file" and isFile(oldPath):
            return oldPath
        elif _objectType == "directory" and isDir(oldPath):
            return oldPath
        elif _objectType == "fileAndDirectory" and (isDir(oldPath) or isFile(oldPath)):
            return oldPath
    _rPath = getRealPath(str(oldPath))
    if _rPath != oldPath:
        oldPath = _rPath
        if _objectType == "file" and isFile(oldPath):
            return oldPath
        elif _objectType == "directory" and isDir(oldPath):
            return oldPath
        elif _objectType == "fileAndDirectory" and (isDir(oldPath) or isFile(oldPath)):
            return oldPath
    if _isShowAlert:
        if _objectType == "file":
            Dialogs.showError(translate("FileUtils", "Cannot Find File"),
                              str(translate("FileUtils",
                                            "\"%s\" : cannot find a file with this name.<br>Please make sure that it exists and retry.")) % Organizer.getLink(
                                  _oldPath))
        elif _objectType == "directory":
            Dialogs.showError(translate("FileUtils", "Cannot Find Directory"),
                              str(translate("FileUtils",
                                            "\"%s\" : cannot find a folder with this name.<br>Please make sure that it exists and retry.")) % Organizer.getLink(
                                  _oldPath))
        else:
            Dialogs.showError(translate("FileUtils", "Cannot Find File Or Directory"),
                              str(translate("FileUtils",
                                            "\"%s\" : cannot find a file or directory with this name.<br>Please make sure that it exists and retry.")) % Organizer.getLink(
                                  _oldPath))
    return None


def checkDestination(_oldPath, _newPath, _isQuiet=False):
    _oldPath, _newPath = str(_oldPath), str(_newPath)
    if uni.isWindows:
        _oldPath = _oldPath.replace("\\", sep).replace("/", sep)
        _newPath = _newPath.replace("\\", sep).replace("/", sep)
    while isAvailableNameForEncoding(_newPath) is False:
        _newPath = Dialogs.getText(translate("FileUtils", "Unavailable Name"),
                                   str(translate("FileUtils",
                                                 "\"%s\" : can not encoded by %s.<br>Please review and correct the name!<br>You can correct your file system encoding name in Options/Advanced, If you want.<br>You can click cancel to cancel this action.")) % (
                                       _newPath, fileSystemEncoding), _newPath)
        if _newPath is None:
            return False
    availableNameByName = getAvailablePathByPath(_newPath)
    while _newPath != availableNameByName:
        _newPath = Dialogs.getText(translate("FileUtils", "Unavailable Name"),
                                   str(translate("FileUtils",
                                                 "\"%s\" : this file path is not valid.<br>Please review and correct the path of file!<br>You can click cancel to cancel this action.")) % (
                                       _newPath), availableNameByName)
        if _newPath is None:
            return False
        availableNameByName = getAvailablePathByPath(_newPath)
    if isExist(_newPath):
        if isWritableFileOrDir(_newPath):
            if uni.isWindows and Organizer.makeCorrectCaseSensitive(_oldPath, uni.validSentenceStructureKeys[
                1]) == Organizer.makeCorrectCaseSensitive(_newPath, uni.validSentenceStructureKeys[1]):
                return _newPath
            else:
                if isFile(_newPath):
                    if _isQuiet:
                        return _newPath
                    else:
                        answer = Dialogs.askSpecial(translate("FileUtils", "Current File Name"),
                                                    str(translate("FileUtils",
                                                                  "\"%s\" : there already exists a file with the same name.<br>Replace it with the current one?")) % Organizer.getLink(
                                                        _newPath),
                                                    translate("Dialogs", "Replace"),
                                                    translate("Dialogs", "Rename"),
                                                    translate("Dialogs", "Cancel"))
                        if answer == translate("Dialogs", "Replace"):
                            removeFile(_newPath)
                            return _newPath
                        elif answer == translate("Dialogs", "Rename"):
                            newPath = Dialogs.getSaveFileName(translate("FileUtils", "Select A New Name For File"),
                                                              _newPath, translate("FileUtils", "All Files") + " (*)", 0)
                            if newPath is not None:
                                return checkDestination(_oldPath, newPath, _isQuiet)
                            return False
                        else:
                            return False
                elif isDir(_newPath):
                    if isFile(_oldPath):
                        answer = Dialogs.askSpecial(translate("FileUtils", "Current Directory Name"),
                                                    str(translate("FileUtils",
                                                                  "\"%s\" : there already exists a folder with the same name.<br>\"%s\" Add this file to the current folder?")) % (
                                                        Organizer.getLink(_newPath), Organizer.getLink(_newPath)),
                                                    translate("Dialogs", "Yes, Add Into"),
                                                    translate("Dialogs", "Rename"),
                                                    translate("Dialogs", "Cancel"))
                        if answer == translate("Dialogs", "Yes, Add Into"):
                            return joinPath(_newPath, getBaseName(_newPath))
                        elif answer == translate("Dialogs", "Rename"):
                            newPath = Dialogs.getSaveFileName(translate("FileUtils", "Select A New Name For File"),
                                                              _newPath, translate("FileUtils", "All Files") + " (*)", 0)
                            if newPath is not None:
                                return checkDestination(_oldPath, newPath, _isQuiet)
                            return False
                        else:
                            return False
                    else:
                        isAllowed = False
                        for tDir in appendingDirectories:
                            if _newPath == tDir:
                                isAllowed = True
                                return _newPath
                        if isAllowed is False:
                            if _isQuiet:
                                appendingDirectories.append(_newPath)
                                return _newPath
                            else:
                                answer = Dialogs.askSpecial(translate("FileUtils", "Current Directory Name"),
                                                            str(translate("FileUtils",
                                                                          "\"%s\" : there already exists a directory with the same name.<br>Add your files to the current directory?")) % Organizer.getLink(
                                                                _newPath),
                                                            translate("Dialogs", "Yes, Add Into"),
                                                            translate("Dialogs", "Rename"),
                                                            translate("Dialogs", "Cancel"))
                                if answer == translate("Dialogs", "Yes, Add Into"):
                                    appendingDirectories.append(_newPath)
                                    return _newPath
                                elif answer == translate("Dialogs", "Rename"):
                                    newPath = Dialogs.getExistingDirectory(translate("FileUtils", "Select A Directory"),
                                                                           _newPath, 0)
                                    if newPath is not None:
                                        return checkDestination(_oldPath, newPath, _isQuiet)
                                    return False
                                else:
                                    return False
                else:
                    return False
        else:
            return False
    else:
        if isWritableFileOrDir(getDirName(_newPath)):
            return _newPath
        else:
            return False
    return False


def checkNewDestination(_newPath, _isQuiet=False):
    _newPath = str(_newPath)
    if uni.isWindows:
        _newPath = _newPath.replace("\\", sep).replace("/", sep)
    while isAvailableNameForEncoding(_newPath) is False:
        _newPath = Dialogs.getText(translate("FileUtils", "Unavailable Name"),
                                   str(translate("FileUtils",
                                                 "\"%s\" : can not encoded by %s.<br>Please review and correct the name!<br>You can correct your file system encoding name in Options/Advanced, If you want.<br>You can click cancel to cancel this action.")) % (
                                       _newPath, fileSystemEncoding), _newPath)
        if _newPath is None:
            return False
    availableNameByName = getAvailablePathByPath(_newPath)
    while _newPath != availableNameByName:
        _newPath = Dialogs.getText(translate("FileUtils", "Unavailable Name"),
                                   str(translate("FileUtils",
                                                 "\"%s\" : this file path is not valid.<br>Please review and correct the path of file!<br>You can click cancel to cancel this action.")) % (
                                       _newPath), availableNameByName)
        if _newPath is None:
            return False
        availableNameByName = getAvailablePathByPath(_newPath)
    if isExist(_newPath):
        if isWritableFileOrDir(_newPath):
            if isFile(_newPath):
                if _isQuiet:
                    return _newPath
                else:
                    answer = Dialogs.askSpecial(translate("FileUtils", "Current File Name"),
                                                str(translate("FileUtils",
                                                              "\"%s\" : there already exists a file with the same name.<br>Replace it with the current one?")) % Organizer.getLink(
                                                    _newPath),
                                                translate("Dialogs", "Replace"),
                                                translate("Dialogs", "Rename"),
                                                translate("Dialogs", "Cancel"))
                    if answer == translate("Dialogs", "Replace"):
                        removeFile(_newPath)
                        return _newPath
                    elif answer == translate("Dialogs", "Rename"):
                        newPath = Dialogs.getSaveFileName(translate("FileUtils", "Select A New Name For File"),
                                                          _newPath, translate("FileUtils", "All Files") + " (*)", 0)
                        if newPath is not None:
                            return checkNewDestination(newPath, _isQuiet)
            elif isDir(_newPath):
                if not _isQuiet:
                    answer = Dialogs.ask(translate("FileUtils", "Current Directory Name"),
                                         str(translate("FileUtils",
                                                       "\"%s\" : there already exists a directory with the same name.<br>Are you want to choose another name?")) % Organizer.getLink(
                                             _newPath))
                    if answer == Dialogs.Yes:
                        newPath = Dialogs.getText(translate("FileUtils", "Choose Another Name"),
                                                  translate("FileUtils", "Choose Another Name"), _newPath)
                        if newPath is not None:
                            return checkNewDestination(newPath, _isQuiet)
    else:
        if isWritableFileOrDir(getDirName(_newPath)):
            return _newPath
    return False


def readDirectory(_path, _objectType="fileAndDirectory", _isShowHiddens=True):
    global appendingDirectories
    appendingDirectories = []
    musicExtensions = []
    musicFileNames = []
    fileAndDirectoryNames, fileNames, directoryNames = [], [], []
    if _objectType == "music":
        musicFileNames = []
        musicExtensions = uni.getListValue("musicExtensions")
    for name in listDir(_path):
        if _isShowHiddens or isHidden(joinPath(_path, name), name) is False:
            try: fileAndDirectoryNames.append(uni.trDecode(name, fileSystemEncoding))
            except: fileAndDirectoryNames.append(name)
    for name in fileAndDirectoryNames:
        if isDir(joinPath(_path, name)):
            directoryNames.append(name)
        else:
            fileNames.append(name)
            if _objectType == "music":
                for ext in musicExtensions:
                    try:
                        if name.split(".")[-1].lower() == str(ext).lower():
                            musicFileNames.append(name)
                    except:
                        pass
    if _objectType == "file":
        return fileNames
    elif _objectType == "directory":
        return directoryNames
    elif _objectType == "fileAndDirectory":
        return fileAndDirectoryNames
    elif _objectType == "music":
        return musicFileNames
    else:
        return []


def readDirectoryAll(_path):
    tFileAndDirs = []
    for name in listDir(_path):
        try: tFileAndDirs.append(str(uni.trDecode(name, fileSystemEncoding)))
        except:
            try: tFileAndDirs.append(str(name))
            except: tFileAndDirs.append(name)
    return tFileAndDirs


def readDirectoryWithSubDirectories(_path, _subDirectoryDeep=-1, _objectType="fileAndDirectory", _isShowHiddens=True,
                                    _currentSubDeep=0):
    global appendingDirectories
    _subDirectoryDeep = int(_subDirectoryDeep)
    allFilesAndDirectories, files, directories, appendingDirectories = [], [], [], []
    try: namesList = readDirectoryAll(_path)
    except: return []
    for name in namesList:
        if _isShowHiddens or isHidden(joinPath(_path, name), name) is False:
            if isDir(joinPath(_path, name)):
                directories.append(name)
            else:
                files.append(name)
    for name in directories:
        if _subDirectoryDeep == -1 or _subDirectoryDeep > _currentSubDeep:
            if _objectType == "fileAndDirectory" or _objectType == "directory":
                allFilesAndDirectories.append(joinPath(_path, name))
            for dd in readDirectoryWithSubDirectories(joinPath(_path, name), _subDirectoryDeep, _objectType,
                                                      _isShowHiddens, _currentSubDeep + 1):
                allFilesAndDirectories.append(dd)
    if _objectType != "directory":
        if _objectType == "file" or _objectType == "fileAndDirectory":
            for name in files:
                allFilesAndDirectories.append(joinPath(_path, name))
        elif _objectType == "music":
            musicExtensions = uni.getListValue("musicExtensions")
            for name in files:
                for ext in musicExtensions:
                    try:
                        if name.split(".")[-1].lower() == str(ext).lower():
                            allFilesAndDirectories.append(joinPath(_path, name))
                    except:
                        pass
    return allFilesAndDirectories


def readDirectoryWithSubDirectoriesThread(_path, _subDirectoryDeep=-1, _objectType="fileAndDirectory",
                                          _isShowHiddens=True, _currentSubDeep=0):
    from Core import MyThread

    global appendingDirectories
    allFilesAndDirectories, appendingDirectories = [], []
    infoProcess = MyThread.MyWaitThread(translate("FileUtils", "Reading Directory..."))
    myProcs = MyThread.MyThread(readDirectoryWithSubDirectories, infoProcess.finish,
                                args=[_path, _subDirectoryDeep, _objectType, _isShowHiddens, _currentSubDeep])
    myProcs.start()
    infoProcess.run()
    allFilesAndDirectories = myProcs.data
    return allFilesAndDirectories


def readFromFile(_path, _contentEncoding=fileSystemEncoding):
    _path = str(_path)
    if _contentEncoding is not None:
        if uni.isPython3k:
            try: f = open(uni.trEncode(_path, fileSystemEncoding), encoding=_contentEncoding)
            except: f = open(_path, encoding=_contentEncoding)
        else:
            import codecs

            try: f = codecs.open(uni.trEncode(_path, fileSystemEncoding), encoding=_contentEncoding)
            except: f = codecs.open(_path, encoding=_contentEncoding)
        try:
            info = f.read()
            f.close()
        except:
            info = readFromFile(_path, None)
    else:
        try: f = open(uni.trEncode(_path, fileSystemEncoding))
        except: f = open(_path)
        info = f.read()
        f.close()
    return info


def readLinesFromFile(_path, _contentEncoding=fileSystemEncoding):
    _path = str(_path)
    if _contentEncoding is not None:
        if uni.isPython3k:
            try: f = open(uni.trEncode(_path, fileSystemEncoding), encoding=_contentEncoding)
            except: f = open(_path, encoding=_contentEncoding)
        else:
            import codecs

            try: f = codecs.open(uni.trEncode(_path, fileSystemEncoding), encoding=_contentEncoding)
            except: f = codecs.open(_path, encoding=_contentEncoding)
        try:
            info = f.readlines()
            f.close()
        except:
            info = readLinesFromFile(_path, None)
    else:
        try: f = open(uni.trEncode(_path, fileSystemEncoding))
        except: f = open(_path)
        info = f.readlines()
        f.close()
    return info


def readFromBinaryFile(_path):
    _path = str(_path)
    try: f = open(uni.trEncode(_path, fileSystemEncoding), "rb")
    except: f = open(_path, "rb")
    info = f.read()
    f.close()
    return info


def writeToFile(_path, _contents=""):
    _path = str(_path)
    if isDir(getDirName(_path)) is False:
        makeDirs(getDirName(_path))
    try: f = open(uni.trEncode(_path, fileSystemEncoding), "w")
    except: f = open(_path, "w")
    f.write(_contents)
    f.close()
    Records.add("Writed", _path)


def writeToBinaryFile(_path, _contents=""):
    _path = str(_path)
    if isDir(getDirName(_path)) is False:
        makeDirs(getDirName(_path))
    try: f = open(uni.trEncode(_path, fileSystemEncoding), "wb")
    except: f = open(_path, "wb")
    f.write(_contents)
    f.flush()
    f.close()
    Records.add("Writed", _path)


def addToFile(_path, _contents=""):
    _path = str(_path)
    try: f = open(uni.trEncode(_path, fileSystemEncoding), "a")
    except: f = open(_path, "a")
    f.write(_contents)
    f.close()
    Records.add("Added", _path)


def readTextFile(_path, _contentEncoding=fileSystemEncoding):
    fileDetails = {}
    fileDetails["path"] = _path
    fileDetails["content"] = readFromFile(_path, _contentEncoding)
    #return [getDirName(_path), getBaseName(_path), readFromFile(_path)]
    return fileDetails


def writeTextFile(_oldFileValues, _newFileValues, _charSet="utf-8"):
    if _oldFileValues["content"] != _newFileValues["content"] or _charSet != "utf-8":
        writeToFile(_oldFileValues["path"], uni.trEncode(_newFileValues["content"], _charSet))
    if getRealPath(_oldFileValues["path"]) != getRealPath(_newFileValues["path"]):
        return moveOrChange(_oldFileValues["path"], _newFileValues["path"])
    return _oldFileValues["path"]


def clearEmptyDirectories(_path, _isShowState=False, _isCloseState=False, _isAutoCleanSubFolder=True):
    #If directory will deleted : returns True
    #If directory will cleaned : returns False
    clearUnneededs(_path)
    dontRemovingFilesCount = 0
    filesAndDirectories = readDirectoryAll(_path)
    filesAndDirectoriesCount = len(filesAndDirectories)
    if _isShowState and _isCloseState: uni.startThreadAction()
    for nameNo, name in enumerate(filesAndDirectories):
        if _isShowState: isContinueThreadAction = uni.isContinueThreadAction()
        else: isContinueThreadAction = True
        if isContinueThreadAction:
            if _isShowState: Dialogs.showState(translate("FileUtils", "Checking Empty Directories"), nameNo,
                                               filesAndDirectoriesCount, True)
            if isFile(joinPath(_path, name)):
                dontRemovingFilesCount += 1
                if uni.getBoolValue("isDeleteEmptyDirectories"):
                    for f in uni.getListValue("ignoredFiles"):
                        try:
                            if str(f) == name:
                                dontRemovingFilesCount -= 1
                                break
                        except: pass
                    for ext in uni.getListValue("ignoredFileExtensions"):
                        try:
                            if checkExtension(name, ext):
                                dontRemovingFilesCount -= 1
                                break
                        except: pass
            if isDir(joinPath(_path, name)):
                dontRemovingFilesCount += 1
                if _isAutoCleanSubFolder is False:
                    break
                if uni.getBoolValue("isDeleteEmptyDirectories"):
                    for f in uni.getListValue("ignoredDirectories"):
                        try:
                            if str(f) == name:
                                dontRemovingFilesCount -= 1
                                break
                        except: pass
                if clearEmptyDirectories(joinPath(_path, name), _isShowState, False, _isAutoCleanSubFolder):
                    dontRemovingFilesCount -= 1
        else:
            if _isShowState: Dialogs.showState(translate("FileUtils", "Checked Empty Directories"),
                                               filesAndDirectoriesCount, filesAndDirectoriesCount, True)
    if _isShowState and _isCloseState: uni.finishThreadAction()
    if dontRemovingFilesCount == 0 and uni.getBoolValue("isDeleteEmptyDirectories"):
        if _isShowState: Dialogs.showState(translate("FileUtils", "Cleaning Empty Directories"), 0, 1, True)
        clearIgnoreds(_path)
        removeDir(_path)
        if _isCloseState:
            Dialogs.showState(translate("FileUtils", "Directory Deleted"), 1, 1, True)
            Dialogs.show(translate("FileUtils", "Directory Deleted"), str(
                translate("FileUtils", "\"%s\" deleted.Because this directory is empty.")) % Organizer.getLink(_path))
        return True
    if _isCloseState: Dialogs.showState(translate("FileUtils", "Directories Cleaned"), 1, 1, True)
    return False


def clearUnneededs(_path):
    _path = checkSource(_path, "directory", False)
    if _path is not None:
        for f in uni.getListValue("unneededFiles"):
            try:
                if isFile(joinPath(_path, str(f))):
                    removeFile(joinPath(_path, str(f)))
            except: pass
        for f in uni.getListValue("unneededDirectoriesIfIsEmpty"):
            try:
                if isDirEmpty(joinPath(_path, str(f))) and f.strip() != "":
                    removeDir(joinPath(_path, str(f)))
            except: pass
        for f in uni.getListValue("unneededDirectories"):
            try:
                if isDir(joinPath(_path, str(f))) and f.strip() != "":
                    removeFileOrDir(joinPath(_path, str(f)))
            except: pass
        for name in readDirectoryAll(_path):
            if isFile(joinPath(_path, name)):
                for ext in uni.getListValue("unneededFileExtensions"):
                    try:
                        if checkExtension(name, ext):
                            removeFile(joinPath(_path, name))
                    except: pass


def clearIgnoreds(_path):
    _path = checkSource(_path, "directory", False)
    if _path is not None:
        for f in uni.getListValue("ignoredFiles"):
            try:
                if isFile(joinPath(_path, str(f))):
                    removeFile(joinPath(_path, str(f)))
            except: pass
        for f in uni.getListValue("ignoredDirectories"):
            try:
                if isDir(joinPath(_path, str(f))) and f.strip() != "":
                    removeFileOrDir(joinPath(_path, str(f)))
            except: pass
        for name in readDirectoryAll(_path):
            if isFile(joinPath(_path, name)):
                for ext in uni.getListValue("ignoredFileExtensions"):
                    try:
                        if checkExtension(name, ext):
                            removeFile(joinPath(_path, name))
                    except: pass


def removeFileOrDir(_path):
    if isWritableFileOrDir(getDirName(_path)):
        if isFile(_path):
            removeFile(_path)
        else:
            if isWritableFileOrDir(_path):
                removeDir(_path)


def removeOnlySubFiles(_path):
    if isWritableFileOrDir(_path):
        for f in readDirectoryAll(_path):
            if isFile(joinPath(_path, f)):
                removeFile(joinPath(_path, f))
            elif isDir(joinPath(_path, f)):
                removeOnlySubFiles(joinPath(_path, f))


def moveOrChange(_oldPath, _newPath, _objectType="file", _actionType="auto", _isQuiet=False):
    _oldPath, _newPath = str(_oldPath), str(_newPath)
    isChange = False
    _oldPath = checkSource(_oldPath, _objectType)
    if _oldPath is not None:
        isChange = True
        _newPath = checkDestination(_oldPath, _newPath, _isQuiet)
    if isChange and _newPath:
        if _objectType == "directory" and _actionType == "auto":
            if uni.getBoolValue("isClearEmptyDirectoriesWhenMoveOrChange"):
                if checkEmptyDirectories(_oldPath, True, True,
                                         uni.getBoolValue("isAutoCleanSubFolderWhenMoveOrChange")):
                    return _oldPath
        for tDir in appendingDirectories:
            if _newPath == tDir:
                for name in readDirectoryAll(_oldPath):
                    moveOrChange(joinPath(_oldPath, name), joinPath(_newPath, name),
                                 getObjectType(joinPath(_oldPath, name)), _actionType, _isQuiet)
                isChange = False
        if isChange:
            moveFileOrDir(_oldPath, _newPath, _isQuiet)
        if _objectType == "directory" and _actionType == "auto":
            if uni.getBoolValue("isClearEmptyDirectoriesWhenMoveOrChange"):
                if checkEmptyDirectories(_newPath, True, True,
                                         uni.getBoolValue("isAutoCleanSubFolderWhenMoveOrChange")):
                    return _newPath
        if isDir(_newPath) and _actionType == "auto":
            if uni.isActiveDirectoryCover and uni.getBoolValue("isActiveAutoMakeIconToDirectory") and uni.getBoolValue(
                "isAutoMakeIconToDirectoryWhenMoveOrChange"):
                checkIcon(_newPath)
        elif _actionType == "auto":
            if uni.isActiveDirectoryCover and uni.getBoolValue("isActiveAutoMakeIconToDirectory") and uni.getBoolValue(
                "isAutoMakeIconToDirectoryWhenFileMove"):
                if isDir(getDirName(_oldPath)):
                    checkIcon(getDirName(_oldPath))
                if isDir(getDirName(_newPath)):
                    checkIcon(getDirName(_newPath))
        return _newPath
    else:
        return _oldPath


def copyOrChange(_oldPath, _newPath, _objectType="file", _actionType="auto", _isQuiet=False):
    _oldPath, _newPath = str(_oldPath), str(_newPath)
    isChange = False
    _oldPath = checkSource(_oldPath, _objectType)
    if _oldPath is not None:
        isChange = True
        _newPath = checkDestination(_oldPath, _newPath, _isQuiet)
    if isChange and _newPath:
        if _objectType == "directory" and _actionType == "auto":
            if uni.getBoolValue("isClearEmptyDirectoriesWhenCopyOrChange"):
                if checkEmptyDirectories(_oldPath, True, True,
                                         uni.getBoolValue("isAutoCleanSubFolderWhenCopyOrChange")):
                    return _oldPath
        for tDir in appendingDirectories:
            if _newPath == tDir:
                for name in readDirectoryAll(_oldPath):
                    copyOrChange(joinPath(_oldPath, name), joinPath(_newPath, name),
                                 getObjectType(joinPath(_oldPath, name)), _actionType, _isQuiet)
                isChange = False
        if isChange:
            copyFileOrDir(_oldPath, _newPath)
        if isDir(_newPath) and _actionType == "auto":
            if uni.isActiveDirectoryCover and uni.getBoolValue("isActiveAutoMakeIconToDirectory") and uni.getBoolValue(
                "isAutoMakeIconToDirectoryWhenCopyOrChange"):
                checkIcon(_newPath)
        return _newPath
    else:
        return _oldPath


def activateSmartCheckEmptyDirectories():
    global isSmartCheckEmptyDirectories, willCheckEmptyDirectories, willCheckEmptyDirectoriesSubDirectoryStatus
    isSmartCheckEmptyDirectories = True
    willCheckEmptyDirectories = []
    willCheckEmptyDirectoriesSubDirectoryStatus = []


def completeSmartCheckEmptyDirectories(_isShowState=False, _isCloseState=False):
    global isSmartCheckEmptyDirectories, willCheckEmptyDirectories, willCheckEmptyDirectoriesSubDirectoryStatus
    isSmartCheckEmptyDirectories = False
    for x in range(0, len(willCheckEmptyDirectories)):
        clearEmptyDirectories(willCheckEmptyDirectories[x], _isShowState, _isCloseState,
                              willCheckEmptyDirectoriesSubDirectoryStatus[x])
    willCheckEmptyDirectories = []
    willCheckEmptyDirectoriesSubDirectoryStatus = []


def checkEmptyDirectories(_path, _isShowState=False, _isCloseState=False, _isAutoCleanSubFolder=True, _isClear=False):
    global isSmartCheckEmptyDirectories, willCheckEmptyDirectories, willCheckEmptyDirectoriesSubDirectoryStatus
    if uni.getBoolValue("isActiveClearGeneral") or _isClear:
        if isSmartCheckEmptyDirectories:
            if willCheckEmptyDirectories.count(_path) == 0:
                willCheckEmptyDirectories.append(_path)
                willCheckEmptyDirectoriesSubDirectoryStatus.append(_isAutoCleanSubFolder)
        else:
            _path = checkSource(_path, "directory", False)
            if _path is not None:
                return clearEmptyDirectories(_path, _isShowState, _isCloseState, _isAutoCleanSubFolder)


def activateSmartCheckIcon():
    global isSmartCheckIcon, willCheckIconDirectories
    isSmartCheckIcon = True
    willCheckIconDirectories = []


def completeSmartCheckIcon():
    global isSmartCheckIcon, willCheckIconDirectories
    isSmartCheckIcon = False
    for iconDir in willCheckIconDirectories:
        iconDir = checkSource(iconDir, "directory", False)
        if iconDir is not None:
            checkIcon(iconDir)
    willCheckIconDirectories = []


def checkIcon(_path, _isClear=False):
    global isSmartCheckIcon, willCheckIconDirectories
    if isSmartCheckIcon and _isClear is False:
        if willCheckIconDirectories.count(_path) == 0:
            willCheckIconDirectories.append(_path)
    else:
        if _isClear is False:
            coverPath = ""
            coverName = getFirstImageInDirectory(_path)
            if coverName is not None:
                coverPath = joinPath(_path, coverName)
            return setIconToDirectory(_path, coverPath)
        elif _isClear:
            return setIconToDirectory(_path)


def getFirstImageInDirectory(_path, _coverNameIfExist=None, _isCheckDelete=False, _isAsk=True):
    _path = str(_path)
    cover = None
    imageFiles = []
    if isReadableFileOrDir(_path, True):
        for fileName in readDirectoryAll(_path):
            if isFile(joinPath(_path, fileName)):
                if str(fileName.split(".")[0]).lower() == str(_coverNameIfExist).lower():
                    cover = fileName
                if uni.getListValue("imageExtensions").count((fileName.split(".")[-1]).lower()) != 0:
                    imageFiles.append(fileName)
                    if cover is None:
                        for coverName in uni.getListValue("priorityIconNames"):
                            if str(fileName.split(".")[0]).lower() == str(coverName).lower():
                                cover = fileName
                                break
        if _isAsk and eval(uni.MySettings["isAskIfHasManyImagesInAlbumDirectory"].title()) and len(imageFiles) > 1:
            selectedIndex = 0
            if cover is not None:
                selectedIndex = imageFiles.index(cover)
            cover = Dialogs.getItem(translate("FileUtils", "Select A Cover"),
                                    str(translate("FileUtils", "Please select a cover for \"%s\".")) % (
                                        Organizer.getLink(_path)), imageFiles, selectedIndex)
        else:
            if cover is None and len(imageFiles) > 0:
                for imgFile in imageFiles:
                    cover = imgFile
                    break
        if _isCheckDelete and cover is not None:
            if isWritableFileOrDir(_path):
                if eval(uni.MySettings["isDeleteOtherImages"].title()):
                    for imgFile in imageFiles:
                        if cover != imgFile:
                            removeFile(joinPath(_path, imgFile))
    return cover


def setIconToDirectory(_path, _iconName=""):
    _path = str(_path)
    if isDir(_path):
        if isWritableFileOrDir(joinPath(_path, ".directory")):
            if _iconName is None:
                return False
            _iconName = str(_iconName).strip()
            returnValue, isChanging, isChange, isCorrectFileContent, rows = False, False, True, False, []
            if isFile(_iconName):
                if str(_path) == str(getDirName(_iconName)):
                    _iconName = "." + sep + getBaseName(_iconName)
                try:
                    info = readFromFile(joinPath(_path, ".directory"))
                    if info.find("[Desktop Entry]") == -1:
                        info = "[Desktop Entry]\n" + info
                    isCorrectFileContent = True
                except:
                    info = "[Desktop Entry]"
                rows = info.split("\n")
                for rowNo in range(len(rows)):
                    if rows[rowNo][:5] == "Icon=":
                        if len(rows[rowNo]) > 5:
                            isFileExist = False
                            if rows[rowNo][5] == "." and isFile(_path + str(rows[rowNo][6:])):
                                isFileExist = True
                            elif rows[rowNo][5] != "." and isFile(rows[rowNo][5:]):
                                isFileExist = True
                            if isFileExist:
                                if uni.getBoolValue("isChangeExistIcon") is False:
                                    isChange = False
                        isChanging = True
                        rows[rowNo] = "Icon=" + _iconName
                        returnValue = True
                if isChange:
                    if isChanging is False:
                        rows.append("Icon=" + _iconName)
                        returnValue = True
                if isCorrectFileContent:
                    rowNoStrDesktopEntry = -1
                    rowNoStrIcon = -1
                    for rowNo in range(len(rows)):
                        if rows[rowNo].find("[Desktop Entry]") != -1:
                            rowNoStrDesktopEntry = rowNo
                        elif rows[rowNo].find("Icon=") != -1:
                            rowNoStrIcon = rowNo
                    if rowNoStrDesktopEntry != rowNoStrIcon - 1:
                        rows[rowNoStrDesktopEntry] += "\n" + rows[rowNoStrIcon]
                        rows[rowNoStrIcon] = ""
            else:
                if isFile(joinPath(_path, ".directory")):
                    info = readFromFile(joinPath(_path, ".directory"))
                    rows = info.split("\n")
                    for rowNo in range(len(rows)):
                        if len(rows[rowNo]) > 4:
                            if rows[rowNo][:5] == "Icon=":
                                rows[rowNo] = ""
                                break
            info = ""
            for row in rows:
                if row.strip() != "":
                    info += row + "\n"
            writeToFile(joinPath(_path, ".directory"), info)
            return returnValue
        else:
            return False
    else:
        return False


def getIconFromDirectory(_path):
    iconPath, isCorrectedFileContent = None, True
    if isFile(joinPath(_path, ".directory")):
        info = readFromFile(joinPath(_path, ".directory"))
        if info.find("[Desktop Entry]") == -1 and len(info) > 0:
            isCorrectedFileContent = False
        if info.find("[Desktop Entry]") > info.find("Icon=") > -1:
            isCorrectedFileContent = False
        rows = info.split("\n")
        for rowNo in range(len(rows)):
            if rows[rowNo][:5] == "Icon=":
                if len(rows[rowNo]) > 5:
                    if rows[rowNo][5] == "." and isFile(_path + str(rows[rowNo][6:])):
                        iconPath = _path + str(rows[rowNo][6:])
                    elif rows[rowNo][5] != "." and isFile(rows[rowNo][5:]):
                        iconPath = rows[rowNo][5:]
                    elif rows[rowNo][5] == ".":
                        iconPath = _path + str(rows[rowNo][6:])
                        isCorrectedFileContent = False
                    else:
                        iconPath = rows[rowNo][5:]
                        isCorrectedFileContent = False
    return iconPath, isCorrectedFileContent


def clearPackagingDirectory(_path, _isShowState=False, _isCloseState=False):
    _path = checkSource(_path, "directory", False)
    if _path is not None:
        if uni.getBoolValue("isClearEmptyDirectoriesWhenPath"):
            checkEmptyDirectories(_path, _isShowState, _isShowState, uni.getBoolValue("isAutoCleanSubFolderWhenPath"))
        for f in uni.getListValue("packagerUnneededFiles"):
            if isFile(joinPath(_path, f)):
                removeFile(joinPath(_path, f))
        for d in uni.getListValue("packagerUnneededDirectories"):
            if isExist(joinPath(_path, d)):
                removeFileOrDir(joinPath(_path, d))
        dontRemovingFilesCount = 0
        filesAndDirectories = readDirectoryAll(_path)
        for nameNo, name in enumerate(filesAndDirectories):
            if _isShowState:
                Dialogs.showState(translate("FileUtils", "Checking Empty Directories"), nameNo,
                                  len(filesAndDirectories))
            if isFile(joinPath(_path, name)):
                dontRemovingFilesCount += 1
                isDeleted = False
                for ext in uni.getListValue("packagerUnneededFileExtensions"):
                    if checkExtension(name, ext):
                        removeFile(joinPath(_path, name))
                        dontRemovingFilesCount -= 1
                        isDeleted = True
                        break
                if isDeleted is False:
                    if name[-1:] == "~":
                        removeFile(joinPath(_path, name))
                        dontRemovingFilesCount -= 1
                        continue
            if isDir(joinPath(_path, name)):
                dontRemovingFilesCount += 1
                if clearPackagingDirectory(joinPath(_path, name)) is False:
                    dontRemovingFilesCount -= 1
        if dontRemovingFilesCount == 0 and uni.getBoolValue("isPackagerDeleteEmptyDirectories"):
            if _isShowState:
                Dialogs.showState(translate("FileUtils", "Deleting Empty Directories"), 0, 1)
            removeDir(_path)
            if _isCloseState:
                Dialogs.showState(translate("FileUtils", "Empty Directories Deleted"), 1, 1)
                Dialogs.show(translate("FileUtils", "Project Directory Deleted"),
                             str(translate("FileUtils", "\"%s\" deleted.Because this directory is empty.")) %
                             Organizer.getLink(_path))
        if _isCloseState:
            Dialogs.showState(translate("FileUtils", "Empty Directories Deleted"), 1, 1)
        return True
    return False


def clearCleaningDirectory(_path, _isShowState=False, _isCloseState=False):
    _path = checkSource(_path, "directory", False)
    if _path is not None:
        if uni.getBoolValue("isClearEmptyDirectoriesWhenClear"):
            checkEmptyDirectories(_path, _isShowState, _isShowState, uni.getBoolValue("isAutoCleanSubFolderWhenClear"))
        for f in uni.getListValue("cleanerUnneededFiles"):
            if isFile(joinPath(_path, f)):
                removeFile(joinPath(_path, f))
        for d in uni.getListValue("cleanerUnneededDirectories"):
            if isExist(joinPath(_path, d)):
                removeFileOrDir(joinPath(_path, d))
        dontRemovingFilesCount = 0
        filesAndDirectories = readDirectoryAll(_path)
        for nameNo, name in enumerate(filesAndDirectories):
            if _isShowState:
                Dialogs.showState(translate("FileUtils", "Checking Empty Directories"), nameNo,
                                  len(filesAndDirectories))
            if isFile(joinPath(_path, name)):
                dontRemovingFilesCount += 1
                for ext in uni.getListValue("cleanerUnneededFileExtensions"):
                    try:
                        if checkExtension(name, ext):
                            removeFile(joinPath(_path, name))
                            dontRemovingFilesCount -= 1
                            continue
                    except: pass
                try:
                    if name[-1:] == "~":
                        removeFile(joinPath(_path, name))
                        dontRemovingFilesCount -= 1
                        continue
                except: pass
            if isDir(joinPath(_path, name)):
                dontRemovingFilesCount += 1
                if clearCleaningDirectory(joinPath(_path, name)) is False:
                    dontRemovingFilesCount -= 1
        if dontRemovingFilesCount == 0 and uni.getBoolValue("isCleanerDeleteEmptyDirectories"):
            if _isShowState:
                Dialogs.showState(translate("FileUtils", "Deleting Empty Directories"), 0, 1)
            removeDir(_path)
            if _isCloseState:
                Dialogs.showState(translate("FileUtils", "Empty Directories Deleted"), 1, 1)
                Dialogs.show(translate("FileUtils", "Project Directory Deleted"), str(
                    translate("FileUtils", "\"%s\" deleted.Because this directory is empty.")) % Organizer.getLink(
                    _path))
        if _isCloseState:
            Dialogs.showState(translate("FileUtils", "Project Directory Cleaned"), 1, 1)
        return True
    return False


def makePack(_filePath, _packageType, _sourcePath, _realSourceBaseName):
    from Core import MyThread

    _filePath, _sourcePath = str(_filePath), str(_sourcePath)
    if isDir(_filePath):
        Dialogs.showError(translate("FileUtils", "Current Directory Name"),
                          str(translate("FileUtils",
                                        "\"%s\" : there already exists a folder with the same name.<br>Please choose another file name!")) % Organizer.getLink(
                              _filePath))
        return False
    import tarfile

    try: tar = tarfile.open(uni.trEncode(_filePath, fileSystemEncoding), "w:" + _packageType)
    except: tar = tarfile.open(_filePath, "w:" + _packageType)
    maxMembers = len(readDirectoryWithSubDirectoriesThread(_sourcePath, -1, "fileAndDirectory", True)) + 1
    infoProcess = MyThread.MyTarPackStateThread(translate("FileUtils", "Creating Tar File"), tar, maxMembers)
    try:
        myProcs = MyThread.MyThread(tar.add, infoProcess.finish, args=[uni.trEncode(_sourcePath, fileSystemEncoding)],
                                    kwargs={"arcname": uni.trEncode(_realSourceBaseName, fileSystemEncoding)})
        myProcs.start()
    except:
        myProcs = MyThread.MyThread(tar.add, infoProcess.finish, args=[_sourcePath],
                                    kwargs={"arcname": _realSourceBaseName})
        myProcs.start()
    infoProcess.run()
    tar.close()
    Records.add("Packed", _filePath)
    return True


def extractPack(_oldPath, _newPath):
    _oldPath, _newPath = str(_oldPath), str(_newPath)
    import tarfile

    try: tar = tarfile.open(uni.trEncode(_oldPath, fileSystemEncoding), "r:gz")
    except: tar = tarfile.open(_oldPath, "r:gz")
    try: tar.extractall(uni.trEncode(_newPath, fileSystemEncoding), members=tar.getmembers())
    except: tar.extractall(_newPath, members=tar.getmembers())
    tar.close()
    Records.add("Extracted", _oldPath, _newPath)


def clearTempFiles():
    tempDirPath = getTempDir()
    for fileName in readDirectoryAll(tempDirPath):
        if fileName[:15] == "HamsiManager":
            if isDir(joinPath(tempDirPath, fileName)):
                removeFileOrDir(joinPath(tempDirPath, fileName))
            else:
                removeFileOrDir(joinPath(tempDirPath, fileName))


def getFileTree(_path, _subDirectoryDeep=-1, _outputTarget="return", _outputType="html", _contentType="fileTree",
                _extInfo="no"):
    _path = str(_path)
    files = readDirectoryWithSubDirectories(_path, _subDirectoryDeep, "fileAndDirectory",
                                            uni.getBoolValue("isShowHiddensInFileTree"))
    info = ""
    if _contentType == "fileTree":
        if _outputType == "html":
            if _extInfo == "no":
                pass
            elif _extInfo == "title":
                info += " \n <h3>%s </h3> \n" % (str(translate("FileUtils", "File Tree")))
                info += " %s<br> \n" % (_path)
            dirNumber = _path.count(sep)
            findStrings, replaceStrings = [], []
            for x, tFile in enumerate(files):
                if isDir(tFile):
                    findStrings.append(tFile)
                    replaceStrings.append((uni.getUtf8Data("upright") + "&nbsp;&nbsp;&nbsp;" * (
                        tFile.count(sep) - dirNumber)) + uni.getUtf8Data("upright+right") + "&nbsp;")
            findStrings.reverse()
            replaceStrings.reverse()
            fileList = list(files)
            for x, tFile in enumerate(files):
                fileList[x] = tFile
                for y, fstr in enumerate(findStrings):
                    if tFile != fstr:
                        fileList[x] = fileList[x].replace(fstr + sep, replaceStrings[y])
                if x > 0:
                    tin = fileList[x - 1].find(uni.getUtf8Data("upright+right"))
                    tin2 = fileList[x].find(uni.getUtf8Data("upright+right"))
                    if tin > tin2:
                        fileList[x - 1] = fileList[x - 1].replace(uni.getUtf8Data("upright+right"),
                                                                  uni.getUtf8Data("up+right"))
            for x, fileName in enumerate(fileList):
                if x != len(fileList) - 1:
                    info += fileName.replace(_path + sep, uni.getUtf8Data("upright+right") + "&nbsp;")
                else:
                    info += fileName.replace(_path + sep, uni.getUtf8Data("up+right") + "&nbsp;")
                if uni.getBoolValue("isAppendFileSizeToFileTree") or uni.getBoolValue("isAppendLastModifiedToFileTree"):
                    details = getDetails(files[x])
                    if details is not None:
                        info += " ( "
                        if uni.getBoolValue("isAppendFileSizeToFileTree"):
                            info += Organizer.getCorrectedFileSize(details[stat.ST_SIZE])
                            if uni.getBoolValue("isAppendLastModifiedToFileTree"): info += ", "
                        if uni.getBoolValue("isAppendLastModifiedToFileTree"):
                            info += str(translate("FileUtils", "Last Modified : ")) + Organizer.getCorrectedTime(
                                details[stat.ST_MTIME])
                        info += " )"
                    else:
                        info += " ( " + str(translate("FileUtils", "inaccessible")) + " ) "
                info += "<br> \n"
        elif _outputType == "plainText":
            if _extInfo == "no":
                pass
            elif _extInfo == "title":
                info += " %s \n" % (str(translate("FileUtils", "File Tree")))
                info += _path + "\n"
            dirNumber = _path.count(sep)
            findStrings, replaceStrings = [], []
            for x, tFile in enumerate(files):
                if isDir(tFile):
                    findStrings.append(tFile)
                    replaceStrings.append(
                        (uni.getUtf8Data("upright") + "   " * (tFile.count(sep) - dirNumber)) + uni.getUtf8Data(
                            "upright+right") + " ")
            findStrings.reverse()
            replaceStrings.reverse()
            fileList = list(files)
            for x, tFile in enumerate(files):
                fileList[x] = tFile
                for y, fstr in enumerate(findStrings):
                    if tFile != fstr:
                        fileList[x] = fileList[x].replace(fstr + sep, replaceStrings[y])
                if x > 0:
                    tin = fileList[x - 1].find(uni.getUtf8Data("upright+right"))
                    tin2 = fileList[x].find(uni.getUtf8Data("upright+right"))
                    if tin > tin2:
                        fileList[x - 1] = fileList[x - 1].replace(uni.getUtf8Data("upright+right"),
                                                                  uni.getUtf8Data("up+right"))
            for x, fileName in enumerate(fileList):
                if x != len(fileList) - 1:
                    info += fileName.replace(_path + sep, uni.getUtf8Data("upright+right") + " ")
                else:
                    info += fileName.replace(_path + sep, uni.getUtf8Data("up+right") + " ")
                if uni.getBoolValue("isAppendFileSizeToFileTree") or uni.getBoolValue("isAppendLastModifiedToFileTree"):
                    details = getDetails(files[x])
                    if details is not None:
                        info += " ( "
                        if uni.getBoolValue("isAppendFileSizeToFileTree"):
                            info += Organizer.getCorrectedFileSize(details[stat.ST_SIZE])
                            if uni.getBoolValue("isAppendLastModifiedToFileTree"): info += ", "
                        if uni.getBoolValue("isAppendLastModifiedToFileTree"):
                            info += str(translate("FileUtils", "Last Modified : ")) + Organizer.getCorrectedTime(
                                details[stat.ST_MTIME])
                        info += " )"
                    else:
                        info += " ( " + str(translate("FileUtils", "inaccessible")) + " ) "
                info += "\n"
    elif _contentType == "fileList":
        if _outputType == "html":
            if _extInfo == "no":
                pass
            elif _extInfo == "title":
                info += " \n <h3>%s </h3> \n" % (str(translate("FileUtils", "File List")))
                info += " %s<br> \n" % (_path)
            for x, fileName in enumerate(files):
                info += fileName
                if uni.getBoolValue("isAppendFileSizeToFileTree") or uni.getBoolValue("isAppendLastModifiedToFileTree"):
                    details = getDetails(files[x])
                    if details is not None:
                        info += " ( "
                        if uni.getBoolValue("isAppendFileSizeToFileTree"):
                            info += Organizer.getCorrectedFileSize(details[stat.ST_SIZE])
                            if uni.getBoolValue("isAppendLastModifiedToFileTree"): info += ", "
                        if uni.getBoolValue("isAppendLastModifiedToFileTree"):
                            info += str(translate("FileUtils", "Last Modified : ")) + Organizer.getCorrectedTime(
                                details[stat.ST_MTIME])
                        info += " )"
                    else:
                        info += " ( " + str(translate("FileUtils", "inaccessible")) + " ) "
                info += "<br> \n"
        elif _outputType == "plainText":
            if _extInfo == "no":
                pass
            elif _extInfo == "title":
                info += " %s \n" % (str(translate("FileUtils", "File Tree")))
                info += _path + "\n"
            for x, fileName in enumerate(files):
                info += fileName
                if uni.getBoolValue("isAppendFileSizeToFileTree") or uni.getBoolValue("isAppendLastModifiedToFileTree"):
                    details = getDetails(files[x])
                    if details is not None:
                        info += " ( "
                        if uni.getBoolValue("isAppendFileSizeToFileTree"):
                            info += Organizer.getCorrectedFileSize(details[stat.ST_SIZE])
                            if uni.getBoolValue("isAppendLastModifiedToFileTree"): info += ", "
                        if uni.getBoolValue("isAppendLastModifiedToFileTree"):
                            info += str(translate("FileUtils", "Last Modified : ")) + Organizer.getCorrectedTime(
                                details[stat.ST_MTIME])
                        info += " )"
                    else:
                        info += " ( " + str(translate("FileUtils", "inaccessible")) + " ) "
                info += "\n"
    info = str(info)
    if _outputTarget == "return":
        return info
    elif _outputTarget == "file":
        fileExt = None
        formatTypeName = None
        if _outputType == "html":
            if _extInfo != "no":
                strHeader = ("<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Strict//EN\" \n" +
                             "\"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd\"> \n" +
                             "<html xmlns=\"http://www.w3.org/1999/xhtml\" xml:lang=\"tr\" lang=\"tr\" dir=\"ltr\"> \n" +
                             "<head> \n<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" /> \n</head> \n<body> \n")
                strFooter = " \n</body> \n</html>"
                info = strHeader + info + strFooter
            formatTypeName = translate("FileUtils", "HTML")
            fileExt = "html"
        elif _outputType == "plainText":
            formatTypeName = translate("FileUtils", "Plain Text")
            fileExt = "txt"
        filePath = Dialogs.getSaveFileName(translate("FileUtils", "Save As"),
                                           joinPath(userDirectoryPath, getBaseName(_path) + "." + fileExt),
                                           formatTypeName + " (*." + fileExt + ")", 2)
        if filePath is not None:
            if _outputType == "html" and filePath[-5:] != ".html":
                filePath += ".html"
            elif _outputType == "plainText" and filePath[-4:] != ".txt":
                filePath += ".txt"
            writeToFile(filePath, info)
            Dialogs.show(translate("FileUtils", "File Tree Created"),
                         str(translate("FileUtils", "File tree created in file: \"%s\".")) % Organizer.getLink(
                             filePath))
    elif _outputTarget == "dialog":
        dDialog = MDialog(getMainWindow())
        if isActivePyKDE4:
            dDialog.setButtons(MDialog.NoDefault)
        dDialog.setWindowTitle(translate("FileUtils", "File Tree"))
        mainPanel = MWidget(dDialog)
        vblMain = MVBoxLayout(mainPanel)
        if _outputType == "html":
            QtWebKit = getMyObject("QtWebKit")
            wvWeb = QtWebKit.QWebView()
            wvWeb.setHtml(str(info))
            vblMain.addWidget(wvWeb)
        elif _outputType == "plainText":
            teContent = MTextEdit()
            teContent.setPlainText(str(info))
            vblMain.addWidget(teContent)
        pbtnClose = MPushButton(translate("FileUtils", "OK"))
        MObject.connect(pbtnClose, SIGNAL("clicked()"), dDialog.close)
        vblMain.addWidget(pbtnClose)
        if isActivePyKDE4:
            dDialog.setMainWidget(mainPanel)
        else:
            dDialog.setLayout(vblMain)
        dDialog.setMinimumWidth(600)
        dDialog.setMinimumHeight(400)
        dDialog.show()
    elif _outputTarget == "clipboard":
        MApplication.clipboard().setText(str(info))


def fixToSize(_path, _size, _clearFrom="head"):
    if isFile(_path):
        while getSize(_path) > _size:
            if _clearFrom == "head":
                try: contents = readFromFile(_path)[500:]
                except:
                    try: contents = readFromFile(_path)[200:]
                    except: contents = readFromFile(_path)[20:]
            else:
                try: contents = readFromFile(_path)[:-500]
                except:
                    try: contents = readFromFile(_path)[:-200]
                    except: contents = readFromFile(_path)[:-20]
            writeToFile(_path, contents)


def getHashDigest(_filePath, _hashType="MD5"):
    import hashlib

    m = None
    if _hashType == "MD5":
        m = hashlib.md5()
    elif _hashType == "SHA1":
        m = hashlib.sha1()
    elif _hashType == "SHA224":
        m = hashlib.sha224()
    elif _hashType == "SHA256":
        m = hashlib.sha256()
    elif _hashType == "SHA384":
        m = hashlib.sha384()
    elif _hashType == "SHA512":
        m = hashlib.sha512()
    m.update(readFromBinaryFile(_filePath))
    return m.hexdigest()


def createHashDigestFile(_filePath, _digestFilePath=None, _hashType="MD5", _isAddFileExtension=True,
                         _digestContent=None):
    if _digestContent is None:
        _digestContent = getHashDigest(_filePath, _hashType)
    fileExtension = ""
    if _isAddFileExtension:
        fileExtension = _hashType.lower()
    if _digestFilePath is None:
        _digestFilePath = _filePath
    writeToFile(_digestFilePath + fileExtension, _digestContent)
    return True


def checkSizeOfDeletedFiles():
    pathOfDeletedFilesAndDirectories = uni.MySettings["pathOfDeletedFilesAndDirectories"]
    pathOfDeletedFilesAndDirectories = checkSource(pathOfDeletedFilesAndDirectories, "directory", False)
    if pathOfDeletedFilesAndDirectories is not None:
        deletedDirectorySize = getDirectorySize(pathOfDeletedFilesAndDirectories)
        if deletedDirectorySize > (int(uni.MySettings["maxDeletedDirectorySize"]) * 1024 * 1024):
            answer = Dialogs.askSpecial(translate("FileUtils", "Size Of Directory Of Deleted Is Over"),
                                        str(translate("FileUtils",
                                                      "Size of directory of deleted is over. You can check and remove them. <br> Directory Of Deleted : \"%s\" ( %s )")) % (
                                            Organizer.getLink(pathOfDeletedFilesAndDirectories),
                                            Organizer.getCorrectedFileSize(deletedDirectorySize)),
                                        translate("FileUtils", "Open With Default File Manager"),
                                        translate("FileUtils", "Close"), translate("FileUtils", "Remove All Files"))
            if answer == translate("FileUtils", "Open With Default File Manager"):
                from Core import Execute

                Execute.openWith([getRealDirName(pathOfDeletedFilesAndDirectories)])
            if answer == translate("FileUtils", "Remove All Files"):
                uni.MySettings["isDontDeleteFileAndDirectory"] = "false"
                removeDir(pathOfDeletedFilesAndDirectories)
                uni.MySettings["isDontDeleteFileAndDirectory"] = "true"
                Dialogs.show(translate("FileUtils", "Directory Of Deleted Has Been Removed"),
                             translate("FileUtils", "Directory of deleted has been removed successfully."))


