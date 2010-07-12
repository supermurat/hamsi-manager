#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

try:systemsCharSet = sys.getfilesystemencoding().lower()
except:systemsCharSet = sys.getdefaultencoding().lower()

HamsiManagerApp = QApplication(sys.argv)

class Update():
    global removeFileOrDir, UniSettings, selectSourceFile, isFile, isDir, getDirName, listDir, moveFileOrDir, makeDirs, copyFileOrDir, copyDirTree
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
        if isRun==True and isFile(sourceFile):
            tempDir = str(tempfile.gettempdir()) + "/HamsiManager-" + str(random.randrange(0, 1000000))
            import tarfile
            intSleepTime = 0
            while intSleepTime<6:
                try:
                    try:tar = tarfile.open(sourceFile.encode(systemsCharSet), "r:gz")
                    except:tar = tarfile.open(sourceFile, "r:gz")
                    break
                except:
                    intSleepTime +=1
                    time.sleep(1)
            try:tar.extractall(tempDir.encode(systemsCharSet), members=tar.getmembers())
            except:tar.extractall(tempDir, members=tar.getmembers())
            tar.close()
            time.sleep(4)
            for file in listDir(tempDir+"/HamsiManager"):
                if file!="Update.py" and file!="install.py":
                    moveFileOrDir(tempDir+"/HamsiManager/"+file,sys.path[1]+"/"+file)
            popen = os.popen("\"" + sys.executable+"\" " + sys.path[1] + "/ConfigureUpdate.py -ConfigureUpdate", "w")
            
    def isFile(_oldPath):
        _oldPath = str(_oldPath)
        try:return path.isfile(_oldPath.encode(systemsCharSet))
        except:return path.isfile(_oldPath)
    
    def isDir(_oldPath):
        _oldPath = str(_oldPath)
        try:return path.isdir(_oldPath.encode(systemsCharSet))
        except:return path.isdir(_oldPath)
    
    def getDirName(_oldPath):
        _oldPath = str(_oldPath)
        try:returnValue = path.dirname(_oldPath.encode(systemsCharSet))
        except:returnValue = path.dirname(_oldPath)
        try:return returnValue.decode(systemsCharSet)
        except:return returnValue 
        
    def listDir(_oldPath):
        names = []
        if isDir(_oldPath):
            try:names = listdir(_oldPath.encode(systemsCharSet))
            except:names = listdir(_oldPath)
        return names
    
    def moveFileOrDir(_oldPath, _newPath):
        _oldPath, _newPath = str(_oldPath), str(_newPath)
        print _oldPath, _newPath
        if getDirName(_oldPath)==getDirName(_newPath):
            try:rename(_oldPath.encode(systemsCharSet),_newPath.encode(systemsCharSet))
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
                try:move(_oldPath.encode(systemsCharSet),_newPath.encode(systemsCharSet))
                except:move(_oldPath,_newPath)
    
    def copyFileOrDir(_oldPath, _newPath):
        _oldPath, _newPath = str(_oldPath), str(_newPath)
        if isDir(getDirName(_newPath))==False:
            makeDirs(getDirName(_newPath))
        if isFile(_oldPath):
            try:copy(_oldPath.encode(systemsCharSet),_newPath.encode(systemsCharSet))
            except:copy(_oldPath,_newPath)
        else:
            copyDirTree(_oldPath, _newPath)
            
    def copyDirTree(_oldPath, _newPath):
        _oldPath, _newPath = str(_oldPath), str(_newPath)
        try:copytree(_oldPath.encode(systemsCharSet),_newPath.encode(systemsCharSet))
        except:copytree(_oldPath,_newPath)
        
    def makeDirs(_newPath):
        try:makedirs(_newPath.encode(systemsCharSet))
        except:makedirs(_newPath)
    
    def removeFileOrDir(_path, _isDir=False):
        if _isDir==False:
            try:remove(_path.encode(systemsCharSet))
            except:remove(_path)
        else:
            for fd in listDir(_path):
                if isDir(_path+"/"+fd):
                    removeFileOrDir(_path+"/"+fd, True)
                else:
                    removeFileOrDir(_path+"/"+fd)
            try:rmdir(_path.encode(systemsCharSet))
            except:rmdir(_path)
    
    def selectSourceFile(_parent):
        f = QFileDialog.getOpenFileName(_parent, u"Please Choose the Hamsi Manager Installation File.",getDirName(sys.path[1]).decode("utf-8"),u"Hamsi Manager Installation File (*HamsiManager*.tar.gz)")
        if f!="":
            return unicode(str(f), "utf-8")
        return ""

try:
    apps = Update()
except:
    import ReportBug
    error = ReportBug.ReportBug(False, True)
    error.show()
sys.exit(HamsiManagerApp.exec_())
        
        
    
    