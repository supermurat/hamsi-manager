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


import sys
from Core.MyObjects import *
from Core import Dialogs
from Core import Universals as uni
from Core import ReportBug
import FileUtils as fu

pathOfScripsDirectory = fu.joinPath(fu.pathOfSettingsDirectory, "Scripts")


def createDefaultScript(_filePath):
    defaultCodes = ("#!/usr/bin/env python\n" +
                    "# -*- codding: utf-8 -*-\n" +
                    "\n" +
                    "#You can type and execute the commands you wish to run here.\n" +
                    "#You can get detailed information from our official website.\n" +
                    "from Core import Dialogs\nDialogs.show(\"This is an example\",\"You can develop the examples as you wish.\")" +
                    "\n\n\n\n\n\n\n\n\n")
    fu.writeToFile(_filePath, defaultCodes)


def getNextScriptFilePath():
    i = 1
    while True:
        nextScriptFilePath = fu.joinPath(pathOfScripsDirectory, translate("Scripts", "Script") + "-" + str(i) + ".py")
        if fu.isFile(nextScriptFilePath) is False:
            return nextScriptFilePath
        i += 1


def createNewScript():
    filePath = getNextScriptFilePath()
    createDefaultScript(filePath)
    return fu.getBaseName(filePath)


def getScript(_filePath):
    _filePath = fu.checkSource(_filePath, "file", False)
    if _filePath is not None:
        return fu.readFromFile(_filePath)
    return None


def getScriptList():
    if fu.isDir(pathOfScripsDirectory) is False:
        fu.makeDirs(pathOfScripsDirectory)
        createNewScript()
    scriptList = fu.readDirectory(pathOfScripsDirectory, "file")
    if len(scriptList) == 0:
        createNewScript()
        scriptList = fu.readDirectory(pathOfScripsDirectory, "file")
    return scriptList


def saveScript(_filePath, _codes):
    fu.writeToFile(_filePath, _codes)


def clearScript(_filePath):
    createDefaultScript(_filePath)


def runScriptFile(_filePath, _isShowAlertIsSuccessfully=True):
    return runScript(getScript(_filePath))


def runScript(_content, _isShowAlertIsSuccessfully=True):
    try:
        try:
            if _content is not None:
                exec (_content)
                if _isShowAlertIsSuccessfully:
                    Dialogs.show(translate("ScriptManager", "Script Has Run Successfully"),
                                 translate("ScriptManager", "Script which you selected has run successfully."))
                return True
            else:
                Dialogs.showError(translate("ScriptManager", "Script Is Not Available"), translate("ScriptManager",
                                                                                                   "Script content is not available or Script file couldn`t read."))
        except Exception as error:
            import traceback

            cla, error, trbk = sys.exc_info()
            errorName = cla.__name__
            try:
                excArgs = error.__dict__["args"]
            except KeyError:
                excArgs = "<no args>"
            errorDetail = traceback.format_tb(trbk, 5)
            errorDetails = str(errorName) + "\n" + str(error) + "\n" + str(excArgs) + "\n" + str(errorDetail[0])
            Dialogs.showError(translate("ScriptManager", "Error: Failed To Run The Query"),
                              str(translate("ScriptManager", "Error details: <br> \"%s\"")) % (errorDetails))
            return False
    except:
        ReportBug.ReportBug()

