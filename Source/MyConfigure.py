# -*- coding: utf-8 -*-

import sys
import os
import InputOutputs
import Universals
import Settings

class MyConfigure:
    global reConfigureFile, installKDE4Language, installKDE4Languages
    
    def reConfigureFile(_filePath, _installationDirectory=os.path.dirname(Universals.sourcePath)):
        fileContent = InputOutputs.readFromFile(_filePath).replace("~InstallationDirectory~", _installationDirectory)
        InputOutputs.writeToFile(_filePath, fileContent)
            
    def installKDE4Languages():
        if Settings.isAvailablePyKDE4():
            for langCode in InputOutputs.getInstalledLanguagesCodes():
                installKDE4Language(langCode)
            return True
        return False
            
    def installKDE4Language(_language="tr_TR", _KDELocalateDir = Universals.getKDE4HomePath() +"share/locale/~langCode~/LC_MESSAGES/"):
        if Settings.isAvailablePyKDE4():
            _KDELocalateDir = _KDELocalateDir.replace("~langCode~", str(_language[:2]))
            langFile = Universals.sourcePath+"/Languages/" + str(_language)+".mo"
            if InputOutputs.isFile(_KDELocalateDir+u"HamsiManager.mo")==False:
                if InputOutputs.isFile(langFile):
                    if InputOutputs.isDir(_KDELocalateDir.encode(Settings.defaultFileSystemEncoding))==False:
                        InputOutputs.makeDirs(_KDELocalateDir.encode(Settings.defaultFileSystemEncoding))
                    InputOutputs.copyFileOrDir(langFile,_KDELocalateDir+u"HamsiManager.mo")
            return True
        return False
        
        
        
