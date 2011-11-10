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


import os, sys
import subprocess
from threading import Thread
import time
from Core import Variables
import InputOutputs

class Execute:
    global execute, executeWithThread, writeToPopen, executeAsRoot, executeAsRootWithThread, openWith, getCommandResult, executeStringCommand, findExecutablePath, findExecutableBaseName
        
    def getCommandResult(_command):
        if os.name=="nt":
            _command = ["start"] + _command
        myPopen = subprocess.Popen(_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, close_fds=True)
        po, pi = myPopen.stdin, myPopen.stdout
        po.close()
        return pi.read()
        
    def executeStringCommand(_command):
        if os.name=="nt":
            _command = "start" + _command
        return os.popen(_command)
        
    def execute(_command=[], _executableName=None):
        if _executableName=="HamsiManager":
            return subprocess.Popen([Variables.executableHamsiManagerPath] + _command , stdin=subprocess.PIPE, stdout=subprocess.PIPE, bufsize=1)
        elif _executableName in ["Reconfigure", "HamsiManagerInstaller", "ConfigureUpdate", "Update"]:
            pathOfExecutable = findExecutablePath(_executableName)
            if pathOfExecutable==None:
                from Core import Dialogs
                from Core.Universals import translate
                Dialogs.showError(translate("Execute", "Cannot Find Executable File"),
                    str(translate("Execute", "\"%s\" : cannot find an executable file matched this name in directory of Hamsi Manager.<br>Please make sure that it exists and retry.")) % _executableName)
                return None
            return subprocess.Popen([pathOfExecutable] + _command , stdin=subprocess.PIPE, stdout=subprocess.PIPE, bufsize=1)
        else:
            return subprocess.Popen(_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, bufsize=1)
            
    def findExecutableBaseName(_executableName):
        for fName in InputOutputs.readDirectory(Variables.HamsiManagerDirectory, "file"):
            if fName.split(".")[0]==_executableName and fName.find(".zip")==-1:
                return fName
        return None
            
    def findExecutablePath(_executableName):
        for fName in InputOutputs.readDirectory(Variables.HamsiManagerDirectory, "file"):
            if fName.split(".")[0]==_executableName and fName.find(".zip")==-1:
                return Variables.HamsiManagerDirectory + "/" + fName
        return None
    
    def executeWithThread(_command=[], _executableName=None):
        roar = RunWithThread(_command, _executableName)
        roar.start()
        time.sleep(1)
        return True
    
    def openWith(_command):
        if os.name=="nt":
            return os.startfile(_command[0])
        else:
            _command = ["xdg-open"] + _command
            return subprocess.Popen(_command)
        
    def executeAsRoot(_command=[], _executableName=None):
        if Variables.isRunableAsRoot():
            pathOfExecutable = None
            if _executableName=="HamsiManager":
                pathOfExecutable = Variables.executableHamsiManagerPath
            elif _executableName in ["Reconfigure", "HamsiManagerInstaller", "ConfigureUpdate", "Update"]:
                pathOfExecutable = findExecutablePath(_executableName)
            if pathOfExecutable != None:
                _command = [pathOfExecutable] + _command
            return execute([Variables.getLibraryDirectoryPath() + "/kde4/libexec/kdesu"] + _command)
        return False
        
    def executeAsRootWithThread(_command=[], _executableName=None):
        if Variables.isRunableAsRoot():
            roar = RunAsRootWithThread(_command, _executableName)
            roar.start()
            time.sleep(1)
            return True
        return False
        
    def writeToPopen(_popen, _command):
        _popen.stdin.write("\n%s\n" % _command)
        
class RunAsRootWithThread(Thread):
    def __init__(self, _command=[], _executableName=None):
        Thread.__init__(self)
        self.command = _command
        self.executableName = _executableName
    
    def run(self):
        executeAsRoot(self.command, self.executableName)
        
class RunWithThread(Thread):
    def __init__(self, _command=[], _executableName=None):
        Thread.__init__(self)
        self.command = _command
        self.executableName = _executableName
    
    def run(self):
        execute(self.command, self.executableName)
        
    
