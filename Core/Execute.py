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


import os, sys
import subprocess
from threading import Thread
import time
import Variables
import InputOutputs

class Execute:
    global execute, executeAsThread, executeWithPython, writeToPopen, executeAsRoot, executeWithPythonAsRoot, executeHamsiManagerAsRoot, executeHamsiManager, executeReconfigure, executeReconfigureAsRoot, open, getCommandResult, executeStringCommand
        
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
        
    def execute(_command):
        if os.name=="nt":
            _command = ["start"] + _command
        return subprocess.Popen(_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, bufsize=1)
    
    def executeAsThread(_command):
        roar = RunAsThread(_command)
        roar.start()
        time.sleep(1)
        return True
    
    def open(_command):
        if os.name=="nt":
            _command = ["start"] + _command
        else:
            _command = ["xdg-open"] + _command
        return subprocess.Popen(_command)
        
    def executeWithPython(_command):
        return execute([sys.executable] + _command)
        
    def executeHamsiManager(_command=[]):
        return execute([sys.executable, str(Variables.executableHamsiManagerPath)] + _command )
        
    def executeReconfigure(_command=[]):
        return execute([sys.executable, str(Variables.HamsiManagerDirectory+"/Reconfigure.py")] + _command)
        
    def executeAsRoot(_command):
        if Variables.isRunableAsRoot():
            stringCommand = ""
            for myCommand in _command:
                if myCommand[:2]=="--":
                    stringCommand += "%s " % myCommand
                else:
                    stringCommand += "%r " % myCommand
            return execute([Variables.getLibraryDirectoryPath() + "/kde4/libexec/kdesu" , stringCommand ])
        return False
    
    def executeWithPythonAsRoot(_command):
        if Variables.isRunableAsRoot():
            return executeAsRoot([sys.executable] + _command)
        return False
        
    def executeHamsiManagerAsRoot(_command=[]):
        if Variables.isRunableAsRoot():
            roar = RunHamsiManagerAsRoot(_command)
            roar.start()
            time.sleep(1)
            return True
        return False
        
    def executeReconfigureAsRoot(_command=[]):
        if Variables.isRunableAsRoot():
            roar = RunReconfigureAsRoot(_command)
            roar.start()
            time.sleep(1)
            return True
        return False
        
    def writeToPopen(_popen, _command):
        _popen.stdin.write("\n%s\n" % _command)
        
class RunHamsiManagerAsRoot(Thread):
    def __init__(self, _command):
        Thread.__init__(self)
        self.command = _command
    
    def run(self):
        executeWithPythonAsRoot([Variables.executableHamsiManagerPath] + self.command)
        
class RunReconfigureAsRoot(Thread):
    def __init__(self, _command):
        Thread.__init__(self)
        self.command = _command
    
    def run(self):
        executeWithPythonAsRoot([Variables.HamsiManagerDirectory + "/Reconfigure.py"] + self.command)
        
class RunAsThread(Thread):
    def __init__(self, _command):
        Thread.__init__(self)
        self.command = _command
    
    def run(self):
        execute(self.command)
        
    
