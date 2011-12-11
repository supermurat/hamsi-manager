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
from Core import Variables, Universals
import InputOutputs
import logging

class Execute:
    global execute, executeWithThread, writeToPopen, executeAsRoot, executeAsRootWithThread, openWith, getCommandResult, executeStringCommand, findExecutablePath, findExecutableBaseName, getExecuteCommandOfHamsiManager, getPythonPath
        
    def getCommandResult(_command):
        if Variables.isWindows:
            _command = ["start"] + _command
        if Universals.loggingLevel==logging.DEBUG:
            print ("Execute >>> " + str(_command))
        myPopen = subprocess.Popen(_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, close_fds=True)
        po, pi = myPopen.stdin, myPopen.stdout
        po.close()
        return pi.read()
        
    def executeStringCommand(_command):
        if Variables.isWindows:
            _command = "start" + _command
        if Universals.loggingLevel==logging.DEBUG:
            print ("Execute >>> " + str(_command))
        return os.popen(_command)
        
    def execute(_command=[], _executableName=None):
        if _executableName in ["HamsiManager", "Reconfigure", "HamsiManagerInstaller", "ConfigureUpdate", "Update"]:
            pathOfExecutable = findExecutablePath(_executableName)
            if pathOfExecutable==None:
                from Core import Dialogs
                Dialogs.showError(Universals.translate("Execute", "Cannot Find Executable File"),
                    str(Universals.translate("Execute", "\"%s\" : cannot find an executable file matched this name in directory of Hamsi Manager.<br>Please make sure that it exists and retry.")) % _executableName)
                return None
            if pathOfExecutable.find(".py")>-1 or pathOfExecutable.find(".py3")>-1 or pathOfExecutable.find(".pyw")>-1:
                pathOfExecutable = [getPythonPath(), pathOfExecutable]
            else:
                pathOfExecutable = [pathOfExecutable]
            if Universals.loggingLevel==logging.DEBUG:
                print ("Execute >>> " + str(pathOfExecutable + _command))
            return subprocess.Popen(pathOfExecutable + _command , stdin=subprocess.PIPE, stdout=subprocess.PIPE, bufsize=1)
        else:
            if Universals.loggingLevel==logging.DEBUG:
                print ("Execute >>> " + str(_command))
            return subprocess.Popen(_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, bufsize=1)
            
    def findExecutableBaseName(_executableName):
        for fName in InputOutputs.readDirectory(Variables.HamsiManagerDirectory, "file"):
            if fName.split(".")[0]==_executableName and (fName.split(".")[-1] in ["py", "py3", "pyw", "exe"] or len(fName.split("."))==1):
                return fName
        return None
            
    def findExecutablePath(_executableName):
        fAppName = InputOutputs.getBaseName(Variables.executableAppPath)
        if fAppName.split(".")[0]==_executableName and (fAppName.split(".")[-1] in ["py", "py3", "pyw", "exe"] or len(fAppName.split("."))==1):
            return Variables.executableAppPath
        for fName in InputOutputs.readDirectory(Variables.HamsiManagerDirectory, "file"):
            if fName.split(".")[0]==_executableName and (fName.split(".")[-1] in ["py", "py3", "pyw", "exe"] or len(fName.split("."))==1):
                return InputOutputs.joinPath(Variables.HamsiManagerDirectory, fName)
        return None
        
    def getPythonPath():
        """Use this only if runnig .py(.py3,.pyw)"""
        return sys.executable
        
    def getExecuteCommandOfHamsiManager():
        HamsiManagerExecutableFileName = findExecutableBaseName("HamsiManager")
        if HamsiManagerExecutableFileName.find(".py")>-1 or HamsiManagerExecutableFileName.find(".py3")>-1 or HamsiManagerExecutableFileName.find(".pyw")>-1:
            executeCommandOfHamsiManager = "\"" + getPythonPath() + "\" \"" + findExecutablePath("HamsiManager") + "\""
        else:
            executeCommandOfHamsiManager = "\"" + findExecutablePath("HamsiManager") + "\""
        return executeCommandOfHamsiManager
    
    def executeWithThread(_command=[], _executableName=None):
        roar = RunWithThread(_command, _executableName)
        roar.start()
        time.sleep(1)
        return True
    
    def openWith(_command):
        if Variables.isWindows:
            if Universals.loggingLevel==logging.DEBUG:
                print ("Open With >>> " + str(_command))
            return os.startfile(_command)
        else:
            _command = ["xdg-open"] + _command
            if Universals.loggingLevel==logging.DEBUG:
                print ("Open With >>> " + str(_command))
            return subprocess.Popen(_command)
        
    def executeAsRoot(_command=[], _executableName=None):
        if Variables.isRunableAsRoot():
            pathOfExecutable = None
            if _executableName in ["HamsiManager", "Reconfigure", "HamsiManagerInstaller", "ConfigureUpdate", "Update"]:
                pathOfExecutable = findExecutablePath(_executableName)
            if pathOfExecutable != None:
                _command = [pathOfExecutable] + _command
            return execute([InputOutputs.joinPath(Variables.getLibraryDirectoryPath(), "kde4", "libexec", "kdesu")] + _command)
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
        
    
