# This file is part of HamsiManager.
#
# Copyright (c) 2010 - 2014 Murat Demir <mopened@gmail.com>
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


import os, sys
import subprocess
from threading import Thread
import time
from Core.MyObjects import *
from Core import Universals as uni
import FileUtils as fu
from Core import Records


def getCommandResult(_command, _cwd=None):
    if uni.isWindows:
        _command = ["start"] + _command
    Records.add("Execute >>> " + str(_command))
    try: correctedCommand = uni.trEncodeList(_command, fu.fileSystemEncoding)
    except: correctedCommand = _command
    if _cwd is not None:
        myPopen = subprocess.Popen(correctedCommand, stdin=subprocess.PIPE, stdout=subprocess.PIPE, close_fds=True,
                                   cwd=_cwd)
    else:
        myPopen = subprocess.Popen(correctedCommand, stdin=subprocess.PIPE, stdout=subprocess.PIPE, close_fds=True)
    po, pi = myPopen.stdin, myPopen.stdout
    po.close()
    return pi.read()


def executeStringCommand(_command):
    if uni.isWindows:
        _command = "start" + _command
    Records.add("Execute >>> " + str(_command))
    try: correctedCommand = uni.trEncode(_command, fu.fileSystemEncoding)
    except: correctedCommand = _command
    return os.popen(correctedCommand)


def execute(_command=[], _executableName=None):
    if _executableName in ["HamsiManager", "HamsiManagerInstaller"]:
        pathOfExecutable = findExecutablePath(_executableName)
        if pathOfExecutable.find(".py") > -1 or pathOfExecutable.find(".py3") > -1 or pathOfExecutable.find(".pyw") > -1:
            pathOfExecutable = [getPythonPath(), pathOfExecutable]
        else:
            pathOfExecutable = [pathOfExecutable]
        _command = pathOfExecutable + _command
    if len(_command) > 1 and _command[1][0] is not "-" and _command[0].find("kdesu") > -1:
        tCommand = _command[0]
        del _command[0]
        for c in _command:
            if c.find(" ") > -1 or c.find("'") > -1:
                c = "'" + c + "'"
        tCommand += " \"" + (" ".join(_command)) + "\""
        _command = tCommand
        Records.add("Execute >>> " + str(_command))
        Records.saveAllRecords()
        return subprocess.Popen(args=uni.trEncode(_command, fu.fileSystemEncoding), stdin=subprocess.PIPE, stdout=subprocess.PIPE, bufsize=1, shell=True)
    else:
        Records.add("Execute >>> " + str(_command))
        Records.saveAllRecords()
        try: correctedCommand = uni.trEncodeList(_command, fu.fileSystemEncoding)
        except: correctedCommand = _command
        return subprocess.Popen(args=correctedCommand, stdin=subprocess.PIPE, stdout=subprocess.PIPE, bufsize=1)


def findExecutableBaseName(_executableName):
    fileList = fu.readDirectory(fu.HamsiManagerDirectory, "file")
    for fName in fileList:
        if fName.split(".")[0] == _executableName and (
                    fName.split(".")[-1] in ["py", "py3", "pyw", "exe"] or len(fName.split(".")) == 1):
            return fName
    if _executableName == "HamsiManager":
        for fName in fileList:
            if fName.lower() == "hamsi" or (fName.lower().split(".")[0] == "hamsi" and (
                        fName.lower().split(".")[-1] in ["py", "py3", "pyw", "exe"] or len(fName.split(".")) == 1) ):
                return fName
        for fName in fileList:
            if (fName.lower().split(".")[0].find("hamsi") > -1) and (
                        fName.lower().split(".")[-1] in ["py", "py3", "pyw", "exe"] or len(fName.split(".")) == 1):
                return fName
        if uni.isWindows:
            return "hamsi.exe"
        else:
            return "hamsi"
    if _executableName == "HamsiManagerInstaller":
        for fName in fileList:
            if fName.lower() == "install" or (fName.lower().split(".")[0] == "install" and (
                        fName.lower().split(".")[-1] in ["py", "py3", "pyw", "exe"] or len(fName.split(".")) == 1) ):
                return fName
        for fName in fileList:
            if (fName.lower().split(".")[0].find("install") > -1) and (
                        fName.lower().split(".")[-1] in ["py", "py3", "pyw", "exe"] or len(fName.split(".")) == 1):
                return fName
    return None


def findExecutablePath(_executableName, _isAlertIfNotFound=True):
    executableBaseName = findExecutableBaseName(_executableName)
    if executableBaseName is not None:
        return fu.joinPath(fu.HamsiManagerDirectory, executableBaseName)
    if _isAlertIfNotFound:
        from Core import Dialogs

        Dialogs.showError(translate("Execute", "Cannot Find Executable File"),
                          str(translate("Execute",
                                        "\"%s\" : cannot find an executable file matched this name in directory of Hamsi Manager.<br>Please make sure that it exists and retry.")) % _executableName)
    return None


def getPythonPath():
    """Use this only if runnig .py(.py3,.pyw)"""
    try: pathOfPython = uni.trDecode(sys.executable, fu.fileSystemEncoding)
    except: pathOfPython = sys.executable
    if uni.isWindows:
        pathOfPythonWindows = pathOfPython.replace("python.exe", "pythonw.exe")
        if fu.isFile(pathOfPythonWindows):
            pathOfPython = pathOfPythonWindows
    return pathOfPython


def getExecuteCommandOfHamsiManager():
    HamsiManagerExecutableFileName = findExecutableBaseName("HamsiManager")
    if HamsiManagerExecutableFileName.find(".py") > -1 or HamsiManagerExecutableFileName.find(
        ".py3") > -1 or HamsiManagerExecutableFileName.find(".pyw") > -1:
        return "\"" + getPythonPath() + "\" \"" + findExecutablePath("HamsiManager") + "\""
    else:
        return "\"" + findExecutablePath("HamsiManager") + "\""


def getExecuteCommandOfHamsiManagerAsList():
    HamsiManagerExecutableFileName = findExecutableBaseName("HamsiManager")
    if HamsiManagerExecutableFileName.find(".py") > -1 or HamsiManagerExecutableFileName.find(
        ".py3") > -1 or HamsiManagerExecutableFileName.find(".pyw") > -1:
        return [getPythonPath(), findExecutablePath("HamsiManager")]
    else:
        return [findExecutablePath("HamsiManager")]


def executeWithThread(_command=[], _executableName=None):
    roar = RunWithThread(_command, _executableName)
    roar.start()
    time.sleep(1)
    return True


def openWith(_command):
    if uni.isWindows:
        Records.add("Open With >>> " + str(_command))
        try: _command = uni.trEncodeList(_command, fu.fileSystemEncoding)
        except: _command = _command
        correctedCommand = ""
        for x, commandPart in enumerate(_command):
            if x > 0: correctedCommand += " "
            correctedCommand += commandPart
        return os.startfile(correctedCommand)
    else:
        _command = ["xdg-open"] + _command
        Records.add("Open With >>> " + str(_command))
        try: correctedCommand = uni.trEncodeList(_command, fu.fileSystemEncoding)
        except: correctedCommand = _command
        return subprocess.Popen(correctedCommand)


def executeAsRoot(_command=[], _executableName=None):
    if uni.isRunableAsRoot():
        pathOfExecutable = None
        if _executableName in ["HamsiManager", "HamsiManagerInstaller"]:
            pathOfExecutable = findExecutablePath(_executableName)
        if pathOfExecutable is not None:
            _command = [pathOfExecutable] + _command
        return execute([fu.joinPath(uni.getLibraryDirectoryPath(), "kde4", "libexec", "kdesu")] + _command)
    return False


def executeAsRootWithThread(_command=[], _executableName=None):
    if uni.isRunableAsRoot():
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
        
    
