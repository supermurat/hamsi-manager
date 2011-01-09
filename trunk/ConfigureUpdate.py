#!/usr/bin/env python
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


import sys,os
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from shutil import move, copytree, copy
import time
import tempfile, random
from os import listdir,path,removedirs,makedirs, rmdir, remove, rename
if sys.path[0]=="":
    sys.path.insert(0, sys.path[1])
sys.path.insert(0,sys.path[0]+"/Core")

try:fileSystemEncoding = sys.getfilesystemencoding().lower()
except:fileSystemEncoding = sys.getdefaultencoding().lower()

HamsiManagerApp = QApplication(sys.argv)

class Update():
    global removeFileOrDir, UniSettings, selectSourceFile, isFile, isDir, getDirName, getRealDirName, listDir, isWritableFileOrDir, moveFileOrDir, makeDirs, copyFileOrDir, copyDirTree
    UniSettings = QSettings((os.path.expanduser("~")+"/.HamsiApps/universalSettings.ini").decode("utf-8"), QSettings.IniFormat)
    def __init__(self):
        global UniSettings
        isRun = True
        if len(sys.argv)>1:
            sourceFile = str(sys.argv[1])
            if sys.argv[1]=="-ConfigureUpdate":
                removeFileOrDir(sys.path[1]+"/Update.py")
                copyFileOrDir(sys.path[1]+"/ConfigureUpdate.py", sys.path[1]+"/Update.py")
                popen = os.popen("\"" + sys.executable+"\" "+sys.path[1]+ "/Update.py -ConfiguredUpdate", "w")
                isRun = False
            elif sys.argv[1]=="-ConfiguredUpdate":
                time.sleep(1)
                removeFileOrDir(sys.path[1]+"/ConfigureUpdate.py")
                #Best place to change the old information to the new version	
                isRun = False
        else:
            parent = QMainWindow()
            sourceFile = str(selectSourceFile(parent))
        if isRun==True:
            if isFile(sourceFile):
                if isWritableFileOrDir(sys.path[1]):
                    tempDir = str(tempfile.gettempdir()) + "/HamsiManager-" + str(random.randrange(0, 1000000))
                    import tarfile
                    intSleepTime = 0
                    while intSleepTime<6:
                        try:
                            try:tar = tarfile.open(sourceFile.encode(fileSystemEncoding), "r:gz")
                            except:tar = tarfile.open(sourceFile, "r:gz")
                            break
                        except:
                            intSleepTime +=1
                            time.sleep(1)
                    try:tar.extractall(tempDir.encode(fileSystemEncoding), members=tar.getmembers())
                    except:tar.extractall(tempDir, members=tar.getmembers())
                    tar.close()
                    time.sleep(4)
                    for file in listDir(tempDir+"/HamsiManager"):
                        if file!="Update.py" and file!="install.py":
                            moveFileOrDir(tempDir+"/HamsiManager/"+file,sys.path[1]+"/"+file)
                    popen = os.popen("\"" + sys.executable+"\" " + sys.path[1] + "/ConfigureUpdate.py -ConfigureUpdate", "w")
                else:
                    parent = QMainWindow()
                    QMessageBox.critical(parent, "Access Denied!..","<b>Access Denied :</b> \"%s\" : you do not have the necessary permissions to change this directory.<br />Please check your access controls and retry. <br />Note: You can run Hamsi Manager as root and try again.</b><br>" % sys.path[1])
            else:
                parent = QMainWindow()
                QMessageBox.critical(parent, "File Is Not Found!..","<b>File Is Not Found :</b> \"%s\" : this file is not found.<br />Please check your file and retry." % sourceFile)
            
    def isFile(_oldPath):
        _oldPath = str(_oldPath)
        try:return path.isfile(_oldPath.encode(fileSystemEncoding))
        except:return path.isfile(_oldPath)
    
    def isDir(_oldPath):
        _oldPath = str(_oldPath)
        try:return path.isdir(_oldPath.encode(fileSystemEncoding))
        except:return path.isdir(_oldPath)
    
    def getDirName(_oldPath):
        _oldPath = str(_oldPath)
        try:returnValue = path.dirname(_oldPath.encode(fileSystemEncoding))
        except:returnValue = path.dirname(_oldPath)
        try:return returnValue.encode(fileSystemEncoding)
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
            try:names = listdir(_oldPath.encode(fileSystemEncoding))
            except:names = listdir(_oldPath)
        return names
    
    def isWritableFileOrDir(_newPath):
        realPath = _newPath
        if isFile(realPath)==False:
            realPath = getRealDirName(realPath)
        try: 
            if os.access(realPath.encode(fileSystemEncoding), os.W_OK): 
                return True 
        except: 
            if os.access(realPath, os.W_OK): 
                return True
        return False
    
    def moveFileOrDir(_oldPath, _newPath):
        _oldPath, _newPath = str(_oldPath), str(_newPath)
        print (_oldPath + " >>> " + _newPath)
        if getDirName(_oldPath)==getDirName(_newPath):
            try:rename(_oldPath.encode(fileSystemEncoding),_newPath.encode(fileSystemEncoding))
            except:rename(_oldPath,_newPath)
        else:
            if isDir(getDirName(_newPath))==False:
                makeDirs(getDirName(_newPath))
            if isDir(_oldPath):
                for file in listDir(_oldPath):
                    moveFileOrDir(_oldPath+"/"+file,_newPath+"/"+file)
            else:
                if isFile(_newPath):
                    removeFileOrDir(_newPath)
                try:move(_oldPath.encode(fileSystemEncoding),_newPath.encode(fileSystemEncoding))
                except:move(_oldPath,_newPath)
    
    def copyFileOrDir(_oldPath, _newPath):
        _oldPath, _newPath = str(_oldPath), str(_newPath)
        if isDir(getDirName(_newPath))==False:
            makeDirs(getDirName(_newPath))
        if isFile(_oldPath):
            try:copy(_oldPath.encode(fileSystemEncoding),_newPath.encode(fileSystemEncoding))
            except:copy(_oldPath,_newPath)
        else:
            copyDirTree(_oldPath, _newPath)
            
    def copyDirTree(_oldPath, _newPath):
        _oldPath, _newPath = str(_oldPath), str(_newPath)
        try:copytree(_oldPath.encode(fileSystemEncoding),_newPath.encode(fileSystemEncoding))
        except:copytree(_oldPath,_newPath)
        
    def makeDirs(_newPath):
        try:makedirs(_newPath.encode(fileSystemEncoding))
        except:makedirs(_newPath)
    
    def removeFileOrDir(_path, _isDir=False):
        if _isDir==False:
            try:remove(_path.encode(fileSystemEncoding))
            except:remove(_path)
        else:
            for fd in listDir(_path):
                if isDir(_path+"/"+fd):
                    removeFileOrDir(_path+"/"+fd, True)
                else:
                    removeFileOrDir(_path+"/"+fd)
            try:rmdir(_path.encode(fileSystemEncoding))
            except:rmdir(_path)
    
    def selectSourceFile(_parent):
        f = QFileDialog.getOpenFileName(_parent, "Please Choose the Hamsi Manager Installation File.",getDirName(sys.path[1]).decode("utf-8"),"Hamsi Manager Installation File (*HamsiManager*.tar.gz)")
        if f!="":
            return str(f)
        return ""

try:
    apps = Update()
except:
    import ReportBug
    error = ReportBug.ReportBug(False, True)
    error.show()
sys.exit(HamsiManagerApp.exec_())
        
        
    
    
