## This file is part of HamsiManager.
## 
## Copyright (c) 2010 - 2013 Murat Demir <mopened@gmail.com>      
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
from Core import Records

class Execute:
    global execute, executeWithThread, writeToPopen, executeAsRoot, executeAsRootWithThread, openWith, getCommandResult, executeStringCommand, findExecutablePath, findExecutableBaseName, getExecuteCommandOfHamsiManager, getPythonPath, getExecuteCommandOfHamsiManagerAsList
        
    def getCommandResult(_command):
        if Variables.isWindows:
            _command = ["start"] + _command
        Records.add("Execute >>> " + str(_command))
        try:correctedCommand = Universals.trEncodeList(_command, InputOutputs.fileSystemEncoding)
        except:correctedCommand = _command
        myPopen = subprocess.Popen(correctedCommand, stdin=subprocess.PIPE, stdout=subprocess.PIPE, close_fds=True)
        po, pi = myPopen.stdin, myPopen.stdout
        po.close()
        return pi.read()
        
    def executeStringCommand(_command):
        if Variables.isWindows:
            _command = "start" + _command
        Records.add("Execute >>> " + str(_command))
        try:correctedCommand = Universals.trEncode(_command, InputOutputs.fileSystemEncoding)
        except:correctedCommand = _command
        return os.popen(correctedCommand)
        
    def execute(_command=[], _executableName=None):
        if _executableName in ["HamsiManager", "HamsiManagerInstaller"]:
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
            Records.add("Execute >>> " + str(pathOfExecutable + _command))
            try:correctedCommand = Universals.trEncodeList(pathOfExecutable + _command, InputOutputs.fileSystemEncoding)
            except:correctedCommand = pathOfExecutable + _command
            return subprocess.Popen(correctedCommand, stdin=subprocess.PIPE, stdout=subprocess.PIPE, bufsize=1)
        else:
            Records.add("Execute >>> " + str(_command))
            try:correctedCommand = Universals.trEncodeList(_command, InputOutputs.fileSystemEncoding)
            except:correctedCommand = _command
            return subprocess.Popen(correctedCommand, stdin=subprocess.PIPE, stdout=subprocess.PIPE, bufsize=1)
            
    def findExecutableBaseName(_executableName):
        fileList = InputOutputs.readDirectory(Variables.HamsiManagerDirectory, "file")
        for fName in fileList:
            if fName.split(".")[0]==_executableName and (fName.split(".")[-1] in ["py", "py3", "pyw", "exe"] or len(fName.split("."))==1):
                return fName
        if _executableName=="HamsiManager":
            for fName in fileList:
                if fName.lower() == "hamsi" or (fName.lower().split(".")[0] == "hamsi" and (fName.lower().split(".")[-1] in ["py", "py3", "pyw", "exe"] or len(fName.split("."))==1) ):
                    return fName
            for fName in fileList:
                if (fName.lower().split(".")[0].find("hamsi")>-1) and (fName.lower().split(".")[-1] in ["py", "py3", "pyw", "exe"] or len(fName.split("."))==1):
                    return fName
            if Variables.isWindows:
                return "hamsi.exe"
            else:
                return "hamsi"
        return None
            
    def findExecutablePath(_executableName):
        executableBaseName = findExecutableBaseName(_executableName)
        if executableBaseName != None:
            return InputOutputs.joinPath(Variables.HamsiManagerDirectory, executableBaseName)
        return None
        
    def getPythonPath():
        """Use this only if runnig .py(.py3,.pyw)"""
        try:pathOfPython = Universals.trDecode(sys.executable, InputOutputs.fileSystemEncoding)
        except:pathOfPython = sys.executable
        if Variables.isWindows:
            pathOfPythonWindows = pathOfPython.replace("python.exe", "pythonw.exe")
            if InputOutputs.isFile(pathOfPythonWindows):
                pathOfPython = pathOfPythonWindows
        return pathOfPython
        
    def getExecuteCommandOfHamsiManager():
        HamsiManagerExecutableFileName = findExecutableBaseName("HamsiManager")
        if HamsiManagerExecutableFileName.find(".py")>-1 or HamsiManagerExecutableFileName.find(".py3")>-1 or HamsiManagerExecutableFileName.find(".pyw")>-1:
            return "\"" + getPythonPath() + "\" \"" + findExecutablePath("HamsiManager") + "\""
        else:
            return "\"" + findExecutablePath("HamsiManager") + "\""
        
    def getExecuteCommandOfHamsiManagerAsList():
        HamsiManagerExecutableFileName = findExecutableBaseName("HamsiManager")
        if HamsiManagerExecutableFileName.find(".py")>-1 or HamsiManagerExecutableFileName.find(".py3")>-1 or HamsiManagerExecutableFileName.find(".pyw")>-1:
            return [getPythonPath(), findExecutablePath("HamsiManager")]
        else:
            return [findExecutablePath("HamsiManager")]
    
    def executeWithThread(_command=[], _executableName=None):
        roar = RunWithThread(_command, _executableName)
        roar.start()
        time.sleep(1)
        return True
    
    def openWith(_command):
        if Variables.isWindows:
            Records.add("Open With >>> " + str(_command))
            try:_command = Universals.trEncodeList(_command, InputOutputs.fileSystemEncoding)
            except:_command = _command
            correctedCommand = ""
            for x, commandPart in enumerate(_command):
                if x>0 : correctedCommand += " "
                correctedCommand += commandPart
            return os.startfile(correctedCommand)
        else:
            _command = ["xdg-open"] + _command
            Records.add("Open With >>> " + str(_command))
            try:correctedCommand = Universals.trEncodeList(_command, InputOutputs.fileSystemEncoding)
            except:correctedCommand = _command
            return subprocess.Popen(correctedCommand)
        
    def executeAsRoot(_command=[], _executableName=None):
        if Variables.isRunableAsRoot():
            pathOfExecutable = None
            if _executableName in ["HamsiManager", "HamsiManagerInstaller"]:
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
        
    
