# -*- coding: utf-8 -*-

import sys
import os
import InputOutputs
import Universals
import Settings

class MyConfigure:
    global reConfigureFile, installKDE4Language, installKDE4Languages, getDesktopFileContent, getConfiguredDesktopFileContent
    
    def reConfigureFile(_filePath, _installationDirectory=os.path.dirname(Universals.sourcePath)):
        fileContent = InputOutputs.readFromFile(_filePath).replace("~InstallationDirectory~", _installationDirectory)
        InputOutputs.writeToFile(_filePath, fileContent)
            
    def installKDE4Languages():
        if Settings.isAvailablePyKDE4():
            for langCode in InputOutputs.getInstalledLanguagesCodes():
                installKDE4Language(langCode)
            Universals.setMySetting("isInstalledKDE4Language", True)
            return True
        return False
            
    def installKDE4Language(_language="tr_TR", _KDELocalateDir = Universals.getKDE4HomePath() +"share/locale/~langCode~/LC_MESSAGES/"):
        _KDELocalateDir = str(_KDELocalateDir)
        if Settings.isAvailablePyKDE4():
            _KDELocalateDir = _KDELocalateDir.replace("~langCode~", str(_language[:2]))
            langFile = Universals.sourcePath+"/Languages/" + str(_language)+".mo"
            if InputOutputs.isFile(_KDELocalateDir+u"HamsiManager.mo")==False:
                if InputOutputs.isFile(langFile):
                    if InputOutputs.isDir(_KDELocalateDir)==False:
                        InputOutputs.makeDirs(_KDELocalateDir)
                    InputOutputs.copyFileOrDir(langFile,_KDELocalateDir+u"HamsiManager.mo")
            return True
        return False
        
    def getDesktopFileContent():
        return ("#!/usr/bin/env xdg-open\n" +
            "[Desktop Entry]\n" +
            "Encoding=UTF-8\n" +
            "Comment[tr]=Hamsi Manager\n" +
            "Comment=Hamsi Manager\n" +
            "Categories=Audio;AudioVideo;AudioVideoEditing;X-MandrivaLinux-Multimedia-Sound;Qt;KDE;Utility;X-KDE-Utilities-File\n" +
            "Exec=python '~InstallationDirectory~/HamsiManager.py'\n" +
            "GenericName[tr]=Hamsi Manager\n" +
            "GenericName=Hamsi Manager\n" +
            "Icon=~InstallationDirectory~/Source/Themes/Default/Images/HamsiManager.png\n" +
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
        
    def getConfiguredDesktopFileContent(_installationDirectory=os.path.dirname(Universals.sourcePath)):
        return ("#!/usr/bin/env xdg-open\n" +
            "[Desktop Entry]\n" +
            "Encoding=UTF-8\n" +
            "Comment[tr]=Hamsi Manager\n" +
            "Comment=Hamsi Manager\n" +
            "Categories=Audio;AudioVideo;AudioVideoEditing;X-MandrivaLinux-Multimedia-Sound;Qt;KDE;Utility;X-KDE-Utilities-File\n" +
            "Exec=python '~InstallationDirectory~/HamsiManager.py'\n" +
            "GenericName[tr]=Hamsi Manager\n" +
            "GenericName=Hamsi Manager\n" +
            "Icon=~InstallationDirectory~/Source/Themes/Default/Images/HamsiManager.png\n" +
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
            "X-KDE-Username=\n").replace("~InstallationDirectory~", _installationDirectory)

        
        
