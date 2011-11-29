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

import os
from Core import Variables
from Core import Universals
from Core import Execute
import InputOutputs
from Core.MyObjects import translate
pluginName = str(translate("MyPlugins/Explorer_CM", "Windows Explorer`s Context Menus"))
pluginVersion = "0.1"
pluginFiles = []
pluginDirectory = ""
setupDirectory = ""

def isInstallable():
    if Variables.isWindows:
        return True
    return False

def installThisPlugin():
    try:
        if Variables.isPython3k:
            import winreg
        else:
            import _winreg as winreg
        rootReg = winreg.ConnectRegistry(None,winreg.HKEY_CLASSES_ROOT)

        #fileKey = winreg.OpenKey(rootReg, "*\\shell", 0, winreg.KEY_WRITE)
        directoryKey = winreg.OpenKey(rootReg, "Directory\\shell", 0, winreg.KEY_WRITE)
        #directoryBackKey = winreg.OpenKey(rootReg, "Directory\\Background\\shell", 0, winreg.KEY_WRITE)

        winreg.CreateKey(directoryKey, "HamsiManager")
        hamsiKey = winreg.OpenKey(directoryKey, "HamsiManager", 0, winreg.KEY_WRITE)
        try:
            winreg.SetValueEx(hamsiKey,"",0, winreg.REG_SZ, Universals.trEncode(str(translate("MyPlugins/Explorer_CM", "Organize With Hamsi Manager")), Variables.defaultFileSystemEncoding))
        except:
            winreg.SetValueEx(hamsiKey,"",0, winreg.REG_SZ, str(translate("MyPlugins/Explorer_CM", "Organize With Hamsi Manager")))
        winreg.CreateKey(hamsiKey, "command")
        commandKey = winreg.OpenKey(hamsiKey, "command", 0, winreg.KEY_WRITE)
        winreg.SetValueEx(commandKey,"",0, winreg.REG_SZ, "\"" + Execute.findExecutablePath("HamsiManager") + "\" %U") 

        winreg.CloseKey(commandKey)
        winreg.CloseKey(hamsiKey)
        winreg.CloseKey(directoryKey)
        winreg.CloseKey(rootReg)

        #if isAlreadyInstalled:
        #    return "AlreadyInstalled"
    except:
        return False
    return True
    
    
    
    
    
