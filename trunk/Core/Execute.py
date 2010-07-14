# -*- coding: utf-8 -*-

import os, sys
from threading import Thread
import time
import Universals

class Execute:
    global execute, executeWithPython, writeToPopen, executeAsRoot, executeWithPythonAsRoot, executeHamsiManagerAsRoot, isRunableAsRoot, isRunningAsRoot, executeHamsiManager, correctForConsole, executeReConfigure, executeReConfigureAsRoot
    
    def correctForConsole(_string):
        strString = "\"" + _string + "\""
        if _string.find("\"")!=-1:
            strString = "'" + _string + "'"
            if _string.find("'")!=-1:
                strString = "'" + _string.replace("'", "\'") + "'"
        return strString
    
    def execute(_command, _rwa = "w"):
        if os.name=="nt":
            _command = "start " + _command
        return os.popen(_command, _rwa)
        
    def executeWithPython(_command):
        return execute("\"" + sys.executable + "\" " + _command)
        
    def executeHamsiManager(_command=""):
        if _command!="":
            _command = " " + _command.replace("\"", "'")
        return execute("\"" + sys.executable + "\" \"" + Universals.executableHamsiManagerPath + _command + "\"")
        
    def executeReConfigure(_command=""):
        if _command!="":
            _command = " " + _command.replace("\"", "'")
        return execute("\"" + sys.executable + "\" \"" + Universals.HamsiManagerDirectory+"/ReConfigure.py" + _command + "\"")
        
    def isRunableAsRoot():
        try:
            from PyKDE4 import pykdeconfig
            if isRunningAsRoot()==False:
                return True
            return False
        except:
            return False
        
    def isRunningAsRoot():
        import Universals
        if Universals.userDirectoryPath=="/root":
            return True
        return False
        
    def executeAsRoot(_command):
        if isRunableAsRoot():
            from PyKDE4 import pykdeconfig
            return execute(pykdeconfig._pkg_config["kdelibdir"] + "/kde4/libexec/kdesu" + " '" + _command + "'")
        return False
    
    def executeWithPythonAsRoot(_command):
        if isRunableAsRoot():
            from PyKDE4 import pykdeconfig
            return execute(pykdeconfig._pkg_config["kdelibdir"] + "/kde4/libexec/kdesu" + " '\"" + sys.executable + "\" " + _command + "'")
        return False
        
    def executeHamsiManagerAsRoot(_command=""):
        if isRunableAsRoot():
            roar = RunHamsiManagerAsRoot(_command)
            roar.start()
            time.sleep(1)
            return True
        return False
        
    def executeReConfigureAsRoot(_command=""):
        if isRunableAsRoot():
            roar = RunReConfigureAsRoot(_command)
            roar.start()
            time.sleep(1)
            return True
        return False
        
    def writeToPopen(_popen, _command):
        _popen.write("\n%s\n" % _command)
        
class RunHamsiManagerAsRoot(Thread):
    def __init__(self, _command):
        Thread.__init__(self)
        if _command!="":
            _command = " " + _command
        self.command = _command
    
    def run(self):
        executeWithPythonAsRoot("\"" + Universals.HamsiManagerDirectory + "/ReConfigure.py" + "\" " + self.command)
        
class RunReConfigureAsRoot(Thread):
    def __init__(self, _command):
        Thread.__init__(self)
        if _command!="":
            _command = " " + _command
        self.command = _command
    
    def run(self):
        executeWithPythonAsRoot("\"" + Universals.executableHamsiManagerPath + "\" " + self.command)
        
    
