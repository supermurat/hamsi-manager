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
    if Variables.isPython3k:
        import winreg
    else:
        import _winreg as winreg
    executeCommandOfHamsiManager = Execute.getExecuteCommandOfHamsiManager()
    iconPath =  InputOutputs.joinPath(Universals.themePath, "Images", "HamsiManager-128x128.ico")
    
    actionsValues = [{"object": "*",
                        "key": "HamsiManager", 
                        "title": "Hamsi Manager", 
                        "icon": InputOutputs.joinPath(Universals.themePath, "Images", "HamsiManager-128x128.ico"), 
                        "actions": [{"key": "Organize", 
                                            "title": translate("MyPlugins/Explorer_CM", "Organize With Hamsi Manager"), 
                                            "icon": InputOutputs.joinPath(Universals.themePath, "Images", "HamsiManager-128x128.ico"), 
                                            "command" : executeCommandOfHamsiManager + " \"%1\""}
                                ]
                      }, 
                    {"object": "Directory",
                        "key": "HamsiManager", 
                        "title": "Hamsi Manager", 
                        "icon": InputOutputs.joinPath(Universals.themePath, "Images", "HamsiManager-128x128.ico"), 
                        "actions": [{"key": "Organize", 
                                            "title": translate("MyPlugins/Explorer_CM", "Organize With Hamsi Manager"), 
                                            "icon": InputOutputs.joinPath(Universals.themePath, "Images", "HamsiManager-128x128.ico"), 
                                            "command" : executeCommandOfHamsiManager + " \"%1\""}
                                ]
                    }, 
                    {"object": "Directory\\Background",
                        "key": "HamsiManager", 
                        "title": "Hamsi Manager", 
                        "icon": InputOutputs.joinPath(Universals.themePath, "Images", "HamsiManager-128x128.ico"), 
                        "actions": [{"key": "Organize", 
                                            "title": translate("MyPlugins/Explorer_CM", "Organize With Hamsi Manager"), 
                                            "icon": InputOutputs.joinPath(Universals.themePath, "Images", "HamsiManager-128x128.ico"), 
                                            "command" : executeCommandOfHamsiManager + " \"%1\""}
                                ]
                    }]
    rootReg = winreg.ConnectRegistry(None,winreg.HKEY_CLASSES_ROOT)
    for object in actionsValues:
        mainKey = winreg.OpenKey(rootReg, object["object"] + "\\shell", 0, winreg.KEY_WRITE)
        winreg.CreateKey(mainKey, object["key"])
        hamsiKey = winreg.OpenKey(mainKey, object["key"], 0, winreg.KEY_WRITE)
        winreg.SetValueEx(hamsiKey,"MUIVerb",0, winreg.REG_SZ, object["title"])
        winreg.SetValueEx(hamsiKey,"ExtendedSubCommandsKey",0, winreg.REG_SZ, object["object"] + "\\ContextMenus\\" + object["key"])
        try:winreg.SetValueEx(hamsiKey,"Icon",0, winreg.REG_SZ, Universals.trEncode(str(object["icon"]), Variables.defaultFileSystemEncoding))
        except:winreg.SetValueEx(hamsiKey,"Icon",0, winreg.REG_SZ, str(object["icon"]))
        winreg.CreateKey(rootReg, object["object"] + "\\ContextMenus")
        mainContextMenusKey = winreg.OpenKey(rootReg, object["object"] + "\\ContextMenus", 0, winreg.KEY_WRITE)
        for action in object["actions"]:
            winreg.CreateKey(mainContextMenusKey, object["key"] + "\\Shell\\" + action["key"])
            actionKey = winreg.OpenKey(mainContextMenusKey, object["key"] + "\\Shell\\" + action["key"], 0, winreg.KEY_WRITE)
            try:winreg.SetValueEx(actionKey,"MUIVerb",0, winreg.REG_SZ, Universals.trEncode(str(action["title"]), Variables.defaultFileSystemEncoding))
            except:winreg.SetValueEx(actionKey,"MUIVerb",0, winreg.REG_SZ, str(action["title"]))
            try:winreg.SetValueEx(actionKey,"Icon",0, winreg.REG_SZ, Universals.trEncode(str(action["icon"]), Variables.defaultFileSystemEncoding))
            except:winreg.SetValueEx(actionKey,"Icon",0, winreg.REG_SZ, str(action["icon"]))
            winreg.CreateKey(mainContextMenusKey, object["key"] + "\\Shell\\" + action["key"] + "\\command")
            actionCommandKey = winreg.OpenKey(mainContextMenusKey, object["key"] + "\\Shell\\" + action["key"] + "\\command", 0, winreg.KEY_WRITE)
            try:winreg.SetValueEx(actionCommandKey,"",0, winreg.REG_SZ, Universals.trEncode(str(action["command"]), Variables.defaultFileSystemEncoding))
            except:winreg.SetValueEx(actionCommandKey,"",0, winreg.REG_SZ, str(action["command"]))
            winreg.CloseKey(actionCommandKey)
            winreg.CloseKey(actionKey)
        winreg.CloseKey(mainContextMenusKey)
        winreg.CloseKey(hamsiKey)
        winreg.CloseKey(mainKey)
    winreg.CloseKey(rootReg)
    
    #if isAlreadyInstalled:
    #    return "AlreadyInstalled"
    return True
    
    
    
    
    
