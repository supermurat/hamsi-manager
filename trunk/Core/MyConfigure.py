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


import sys
import os
from Core import Variables
import InputOutputs
from Core import Universals

class MyConfigure:
    global reConfigureFile, installKDE4Language, installKDE4Languages, getDesktopFileContent, getConfiguredDesktopFileContent, getConfiguredContent
    
    def reConfigureFile(_filePath, _installationDirectory=Variables.HamsiManagerDirectory):
        fileContent = getConfiguredContent(InputOutputs.readFromFile(_filePath), _installationDirectory)
        InputOutputs.writeToFile(_filePath, fileContent)
            
    def installKDE4Languages():
        if Variables.isAvailableKDE4():
            for langCode in Variables.getInstalledLanguagesCodes():
                installKDE4Language(langCode)
            Universals.setMySetting("isInstalledKDE4Language", True)
            return True
        return False
            
    def installKDE4Language(_language="tr_TR", _KDELocalateDir = None):
        if Variables.isAvailableKDE4():
            if _KDELocalateDir==None:
                _KDELocalateDir = Variables.getKDE4HomePath() +"/share/locale/~langCode~/LC_MESSAGES/"
            if Variables.isRunningAsRoot():
                _KDELocalateDir = "/usr/share/locale/~langCode~/LC_MESSAGES/"
            _KDELocalateDir = str(_KDELocalateDir)
            _KDELocalateDir = _KDELocalateDir.replace("~langCode~", str(_language[:2]))
            langFile = Variables.HamsiManagerDirectory+"/Languages/" + str(_language)+".mo"
            if InputOutputs.isFile(_KDELocalateDir+"HamsiManager.mo")==False:
                if InputOutputs.isFile(langFile):
                    if InputOutputs.isDir(_KDELocalateDir)==False:
                        InputOutputs.makeDirs(_KDELocalateDir)
                    InputOutputs.copyFileOrDir(langFile,_KDELocalateDir+"HamsiManager.mo")
            return True
        return False
        
    def getDesktopFileContent():
        return ("#!/usr/bin/env xdg-open\n" +
            "[Desktop Entry]\n" +
            "Encoding=UTF-8\n" +
            "Comment[tr]=Hamsi Manager\n" +
            "Comment=Hamsi Manager\n" +
            "Categories=Audio;AudioVideo;AudioVideoEditing;X-MandrivaLinux-Multimedia-Sound;Qt;KDE;Utility;X-KDE-Utilities-File\n" +
            "Exec=~ExecuteCommandOfHamsiManager~\n" +
            "GenericName[tr]=Hamsi Manager\n" +
            "GenericName=Hamsi Manager\n" +
            "Icon=~InstallationDirectory~/Themes/Default/Images/HamsiManager-128x128.png\n" +
            "MimeType=\n" +
            "Name[tr]=Hamsi Manager\n" +
            "Name=Hamsi Manager\n" +
            "Path=~InstallationDirectory~\n" +
            "StartupNotify=true\n" +
            "Terminal=false\n" +
            "TerminalOptions=\n" +
            "Type=Application\n" +
            "X-DBUS-ServiceName=\n" +
            "X-DBUS-StartupType=\n" +
            "X-KDE-SubstituteUID=false\n" +
            "X-KDE-Username=\n")
            
    def getConfiguredContent(_content, _installationDirectory=Variables.HamsiManagerDirectory):
        from Core import Execute
        HamsiManagerExecutableFileName = Execute.findExecutableBaseName("HamsiManager")
        if HamsiManagerExecutableFileName.find(".py")>-1:
            executeCommandOfHamsiManager = "python '" + _installationDirectory + "/" + HamsiManagerExecutableFileName + "'"
        else:
            executeCommandOfHamsiManager = "'" + _installationDirectory + "/" + HamsiManagerExecutableFileName + "'"
        return _content.replace("~InstallationDirectory~", _installationDirectory).replace("~ExecuteCommandOfHamsiManager~", executeCommandOfHamsiManager)
        
    def getConfiguredDesktopFileContent(_installationDirectory=Variables.HamsiManagerDirectory):
        return getConfiguredContent(getDesktopFileContent(), _installationDirectory)

        
        
