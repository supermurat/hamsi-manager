#!/usr/bin/env python
## This file is part of HamsiManager.
## 
## Copyright (c) 2010 - 2012 Murat Demir <mopened@gmail.com>      
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


import sys, os, shutil
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import time, tempfile, random, tarfile, traceback
if sys.path[0]=="":
    sys.path.insert(0, sys.path[1])
try: 
    if float(sys.version[:3])<3.0: 
        reload(sys)
        sys.setdefaultencoding("utf-8")
except:pass
try:fileSystemEncoding = sys.getfilesystemencoding().lower()
except:fileSystemEncoding = sys.getdefaultencoding().lower()
if sys.argv[0][0]==".":
    executableAppPath = str(os.getcwd() + sys.argv[0][1:])
else:
    executableAppPath = str(sys.argv[0])
if os.path.islink(executableAppPath):
    executableAppPath = os.readlink(executableAppPath)
isPython3k = float(sys.version[:3])>=3.0
HamsiManagerApp = QApplication(sys.argv)
QTextCodec.setCodecForCStrings(QTextCodec.codecForName("utf-8"))
QTextCodec.setCodecForTr(QTextCodec.codecForName("utf-8"))

def trDecode(_s, _e = "utf-8", _p = "strict"):
    if isPython3k:
        return _s
    return _s.decode(_e, _p)
    
def trEncode(_s, _e = "utf-8", _p = "strict"):
    if isPython3k:
        return _s
    return _s.encode(_e, _p)
        
def trQVariant(_s):
    if isPython3k:
        return _s
    return QVariant(_s)
    
class Update():
    global removeFileOrDir, UniSettings, selectSourceFile, isFile, isDir, getDirName, getRealDirName, listDir, isWritableFileOrDir, moveFileOrDir, makeDirs, copyFileOrDir, copyDirTree, findExecutableBaseName, HamsiManagerDirectory
    UniSettings = QSettings(trDecode(os.path.expanduser("~")+"/.HamsiApps/universalSettings.ini", "utf-8"), QSettings.IniFormat)
    HamsiManagerDirectory = os.path.dirname(str(UniSettings.value("HamsiManagerPath", trQVariant(str(executableAppPath)))))
    
    def __init__(self):
        global UniSettings
        isRun = True
        if len(sys.argv)>1:
            sourceFile = str(sys.argv[1])
            configureUpdateFileName = findExecutableBaseName("ConfigureUpdate")
            updateFileName = findExecutableBaseName("Update")
            if sys.argv[1]=="-ConfigureUpdate":
                if updateFileName!=None:
                    removeFileOrDir(HamsiManagerDirectory+"/"+updateFileName)
                extOfFile = ""
                if configureUpdateFileName.find(".")!=-1:
                    extOfFile = "." + (configureUpdateFileName.split(".")[1])
                copyFileOrDir(HamsiManagerDirectory+"/"+configureUpdateFileName, HamsiManagerDirectory+"/Update" + extOfFile)
                popen = os.popen(HamsiManagerDirectory+ "/Update" + extOfFile + " -ConfiguredUpdate", "w")
                isRun = False
            elif sys.argv[1]=="-ConfiguredUpdate":
                time.sleep(1)
                removeFileOrDir(HamsiManagerDirectory+"/"+configureUpdateFileName)
                #Best place to change the old information to the new version	
                isRun = False
        else:
            parent = QMainWindow()
            sourceFile = str(selectSourceFile(parent))
            if sourceFile=="":
                isRun = False
        if isRun==True:
            if isFile(sourceFile):
                if isWritableFileOrDir(HamsiManagerDirectory):
                    tempDir = str(tempfile.gettempdir()) + "/HamsiManager-" + str(random.randrange(0, 1000000))
                    intSleepTime = 0
                    while intSleepTime<6:
                        try:
                            try:tar = tarfile.open(trEncode(sourceFile, fileSystemEncoding), "r:gz")
                            except:tar = tarfile.open(sourceFile, "r:gz")
                            break
                        except:
                            intSleepTime +=1
                            time.sleep(1)
                    try:tar.extractall(trEncode(tempDir, fileSystemEncoding), members=tar.getmembers())
                    except:tar.extractall(tempDir, members=tar.getmembers())
                    tar.close()
                    time.sleep(4)
                    installFileName = findExecutableBaseName("HamsiManagerInstaller")
                    updateFileName = findExecutableBaseName("Update")
                    if installFileName==None: installFileName=""
                    if updateFileName==None: updateFileName=""
                    for file in listDir(tempDir+"/HamsiManager"):
                        if file!=updateFileName and file!="install.py" and file!=installFileName:
                            moveFileOrDir(tempDir+"/HamsiManager/"+file,HamsiManagerDirectory+"/"+file)
                    configureUpdateFileName = findExecutableBaseName("ConfigureUpdate")
                    popen = os.popen(HamsiManagerDirectory + "/" + configureUpdateFileName + " -ConfigureUpdate", "w")
                else:
                    parent = QMainWindow()
                    QMessageBox.critical(parent, "Access Denied!..","<b>Access Denied :</b> \"%s\" : you do not have the necessary permissions to change this directory.<br />Please check your access controls and retry. <br />Note: You can run Hamsi Manager as root and try again.</b><br>" % HamsiManagerDirectory)
            else:
                parent = QMainWindow()
                QMessageBox.critical(parent, "File Is Not Found!..","<b>File Is Not Found :</b> \"%s\" : this file is not found.<br />Please check your file and retry." % sourceFile)
        return
                
    def isFile(_oldPath):
        _oldPath = str(_oldPath)
        try:return os.path.isfile(trEncode(_oldPath, fileSystemEncoding))
        except:return os.path.isfile(_oldPath)
    
    def isDir(_oldPath):
        _oldPath = str(_oldPath)
        try:return os.path.isdir(trEncode(_oldPath, fileSystemEncoding))
        except:return os.path.isdir(_oldPath)
    
    def getDirName(_oldPath):
        _oldPath = str(_oldPath)
        try:returnValue = os.path.dirname(trEncode(_oldPath, fileSystemEncoding))
        except:returnValue = os.path.dirname(_oldPath)
        try:return trDecode(returnValue, fileSystemEncoding)
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
        
    def listDir(_oldPath):
        names = []
        if isDir(_oldPath):
            try:names = os.listdir(trEncode(_oldPath, fileSystemEncoding))
            except:names = os.listdir(_oldPath)
        return names
            
    def findExecutableBaseName(_executableName):
        for fName in listDir(HamsiManagerDirectory):
            if isFile(HamsiManagerDirectory+"/"+fName):
                if fName.split(".")[0]==_executableName and (fName.split(".")[-1] in ["py", "py3", "pyw", "exe"] or len(fName.split("."))==1):
                    return fName
        return None
    
    def isWritableFileOrDir(_newPath):
        realPath = _newPath
        if isFile(realPath)==False:
            realPath = getRealDirName(realPath)
        try: 
            if os.access(trEncode(realPath, fileSystemEncoding), os.W_OK): 
                return True 
        except: 
            if os.access(realPath, os.W_OK): 
                return True
        return False
    
    def moveFileOrDir(_oldPath, _newPath):
        _oldPath, _newPath = str(_oldPath), str(_newPath)
        print (_oldPath + " >>> " + _newPath)
        if getDirName(_oldPath)==getDirName(_newPath):
            try:os.rename(trEncode(_oldPath, fileSystemEncoding),trEncode(_newPath, fileSystemEncoding))
            except:os.rename(_oldPath,_newPath)
        else:
            if isDir(getDirName(_newPath))==False:
                makeDirs(getDirName(_newPath))
            if isDir(_oldPath):
                for file in listDir(_oldPath):
                    moveFileOrDir(_oldPath+"/"+file,_newPath+"/"+file)
            else:
                if isFile(_newPath):
                    removeFileOrDir(_newPath)
                try:shutil.move(trEncode(_oldPath, fileSystemEncoding),trEncode(_newPath, fileSystemEncoding))
                except:shutil.move(_oldPath,_newPath)
    
    def copyFileOrDir(_oldPath, _newPath):
        _oldPath, _newPath = str(_oldPath), str(_newPath)
        print (_oldPath + " >>> " + _newPath)
        if isDir(getDirName(_newPath))==False:
            makeDirs(getDirName(_newPath))
        if isFile(_oldPath):
            try:shutil.copy(trEncode(_oldPath, fileSystemEncoding),trEncode(_newPath, fileSystemEncoding))
            except:shutil.copy(_oldPath,_newPath)
        else:
            copyDirTree(_oldPath, _newPath)
            
    def copyDirTree(_oldPath, _newPath):
        _oldPath, _newPath = str(_oldPath), str(_newPath)
        print (_oldPath + " >>> " + _newPath)
        try:shutil.copytree(trEncode(_oldPath, fileSystemEncoding),trEncode(_newPath, fileSystemEncoding))
        except:shutil.copytree(_oldPath,_newPath)
        
    def makeDirs(_newPath):
        try:os.makedirs(trEncode(_newPath, fileSystemEncoding))
        except:os.makedirs(_newPath)
    
    def removeFileOrDir(_path, _isDir=False):
        if _isDir==False:
            try:os.remove(trEncode(_path, fileSystemEncoding))
            except:os.remove(_path)
        else:
            for fd in listDir(_path):
                if isDir(_path+"/"+fd):
                    removeFileOrDir(_path+"/"+fd, True)
                else:
                    removeFileOrDir(_path+"/"+fd)
            try:os.rmdir(trEncode(_path, fileSystemEncoding))
            except:os.rmdir(_path)
    
    def selectSourceFile(_parent):
        f = QFileDialog.getOpenFileName(_parent, "Please Choose the Hamsi Manager Installation File.",trDecode(getDirName(HamsiManagerDirectory), "utf-8"),"Hamsi Manager Installation File (*HamsiManager*.tar.gz)")
        if f!="":
            return str(f)
        return ""

try:
    apps = Update()
except:
    cla, exc, trbk = sys.exc_info()
    excName = cla.__name__
    try:
        excArgs = exc.__dict__["args"]
    except:
        excArgs = "<no args>"
    excTb = traceback.format_tb(trbk, 5)
    try:
        QMessageBox.critical(QMainWindow(), "Critical Error!..","<b>Error Details :</b> " + excName + "<br>"  + excArgs + "<br>"  + excTb + "<br>" )
    except:pass
    print excName
    print excArgs
    print excTb
HamsiManagerApp.exec_()
sys.exit()
        
        
    
    
