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


import sys
import os
import FileUtils as fu
from Core import Universals as uni

def reConfigureFile(_filePath, _installationDirectory=fu.HamsiManagerDirectory, _executeCommandOfHamsiManager=None):
    fileContent = getConfiguredContent(fu.readFromFile(_filePath), _executeCommandOfHamsiManager)
    fileContent = fileContent.replace(fu.HamsiManagerDirectory, _installationDirectory)
    fu.writeToFile(_filePath, fileContent)

def installKDE4Languages():
    if uni.isAvailableKDE4():
        for langCode in uni.getInstalledLanguagesCodes():
            installKDE4Language(langCode)
        uni.setMySetting("isInstalledKDE4Language", True)
        return True
    return False

def installKDE4Language(_language="tr_TR"):
    if uni.isAvailableKDE4():
        KDELocalateDir = fu.joinPath(uni.getKDE4HomePath(), "share", "locale", str(_language[:2]), "LC_MESSAGES")
        if uni.isRunningAsRoot():
            KDELocalateDir = fu.joinPath("/usr", "share", "locale", str(_language[:2]), "LC_MESSAGES")
        KDELocalateDir = str(KDELocalateDir)
        langFile = fu.joinPath(fu.HamsiManagerDirectory, "Languages", "DontTranslate", str(_language), "HamsiManager.mo")
        if fu.isFile(fu.joinPath(KDELocalateDir, "HamsiManager.mo"))==False:
            if fu.isFile(langFile):
                if fu.isDir(KDELocalateDir)==False:
                    fu.makeDirs(KDELocalateDir)
                fu.copyFileOrDir(langFile, fu.joinPath(KDELocalateDir, "HamsiManager.mo"))
        return True
    return False

def createShortCutFile(_destinationPath, _installationDirectory=fu.HamsiManagerDirectory):
    if fu.isFile(_destinationPath):
        fu.removeFileOrDir(_destinationPath)
    from Core import Execute
    from win32com.client import Dispatch
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(_destinationPath)
    targetPath = Execute.getExecuteCommandOfHamsiManagerAsList()
    if len(targetPath)>1:
        shortcut.Targetpath = targetPath[0]
        shortcut.Arguments = targetPath[1]
    else:
        shortcut.Targetpath = targetPath[0]
    shortcut.WorkingDirectory = _installationDirectory
    shortcut.IconLocation = fu.joinPath(fu.themePath.replace(fu.HamsiManagerDirectory, _installationDirectory), "Images", "hamsi.ico")
    shortcut.save()

def getDesktopFileContent():
    return ("""#!/usr/bin/env xdg-open
[Desktop Entry]
Encoding=UTF-8
Comment[tr]=Hamsi Manager
Comment=Hamsi Manager
Categories=Utility;Qt;KDE;System;X-KDE-Utilities-File;GTK;GNOME;FileTools;FileManager
Exec=~ExecuteCommandOfHamsiManager~
GenericName[tr]=Hamsi Manager
GenericName=Hamsi Manager
Icon=~IconPath~
MimeType=inode/directory;
Name[tr]=Hamsi Manager
Name=Hamsi Manager
Path=~InstallationDirectory~
StartupNotify=true
Terminal=false
TerminalOptions=
Type=Application
X-DBUS-ServiceName=
X-DBUS-StartupType=
X-KDE-SubstituteUID=false
X-KDE-Username=
X-MultipleArgs=false
""")

def getConfiguredContent(_content, _executeCommandOfHamsiManager=None):
    if _executeCommandOfHamsiManager is None:
        from Core import Execute
        _executeCommandOfHamsiManager = Execute.getExecuteCommandOfHamsiManager()
    return _content.replace("~InstallationDirectory~", fu.HamsiManagerDirectory).replace("~ExecuteCommandOfHamsiManager~", _executeCommandOfHamsiManager).replace("~IconPath~", fu.joinPath(fu.themePath, "Images", "hamsi.png")).replace("~ThemePath~", fu.themePath)


def getConfiguredDesktopFileContent(_installationDirectory=fu.HamsiManagerDirectory, _executeCommandOfHamsiManager=None):
    fileContent = getConfiguredContent(getDesktopFileContent(), _executeCommandOfHamsiManager)
    fileContent = fileContent.replace(fu.HamsiManagerDirectory, _installationDirectory)
    return fileContent



