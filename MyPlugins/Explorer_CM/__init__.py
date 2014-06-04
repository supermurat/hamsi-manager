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

import os, sys, platform
from Core import Variables
from Core import Universals
from Core import Dialogs
from Core import Execute
from Core import ReportBug
import InputOutputs
from Core.MyObjects import translate
pluginName = str(translate("MyPlugins/Explorer_CM", "Windows Explorer`s Context Menus"))
pluginVersion = "0.4"
pluginFiles = []
pluginDirectory = ""
setupDirectory = ""

def isInstallable():
    if Variables.isWindows:
        if platform.release()=="7":
            return True
    return False

def installThisPlugin():
    if Variables.isPython3k:
        import winreg
    else:
        import _winreg as winreg
    executeCommandOfHamsiManager = Execute.getExecuteCommandOfHamsiManager()
    iconPath =  InputOutputs.joinPath(Universals.themePath, "Images", "HamsiManager-16x16-1.ico")
    
    actionsValues = [{"object": "*",
                        "key": "HamsiManager", 
                        "title": "Hamsi Manager", 
                        "icon": InputOutputs.joinPath(Universals.themePath, "Images", "HamsiManager-16x16-1.ico"), 
                        "actions": [{"key": "copyPath", 
                                            "title": translate("MyPlugins/Explorer_CM", "Copy Path To Clipboard"), 
                                            "icon": InputOutputs.joinPath(Universals.themePath, "Images", "copyPath.ico"), 
                                            "command" : executeCommandOfHamsiManager + " --qm --copyPath \"%1\""}, 
                                    {"key": "emendFile", 
                                            "title": translate("MyPlugins/Explorer_CM", "Auto Emend File"), 
                                            "icon": InputOutputs.joinPath(Universals.themePath, "Images", "emendFile.ico"), 
                                            "command" : executeCommandOfHamsiManager + " --qm --emendFile \"%1\""}, 
                                    {"key": "hash", 
                                            "title": translate("MyPlugins/Explorer_CM", "Hash Digest"), 
                                            "icon": InputOutputs.joinPath(Universals.themePath, "Images", "hash.ico"), 
                                            "command" : executeCommandOfHamsiManager + " --qm --hash \"%1\""}, 
                                    {"key": "textCorrector", 
                                            "title": translate("MyPlugins/Explorer_CM", "Correct Content"), 
                                            "icon": InputOutputs.joinPath(Universals.themePath, "Images", "textCorrector.ico"), 
                                            "command" : executeCommandOfHamsiManager + " --qm --textCorrector \"%1\""}, 
                                    {"key": "search", 
                                            "title": translate("MyPlugins/Explorer_CM", "Search"), 
                                            "icon": InputOutputs.joinPath(Universals.themePath, "Images", "search.ico"), 
                                            "command" : executeCommandOfHamsiManager + " --qm --search \"%1\""}
                                ]}, 
                    {"object": "Directory",
                        "key": "HamsiManager", 
                        "title": "Hamsi Manager", 
                        "icon": InputOutputs.joinPath(Universals.themePath, "Images", "HamsiManager-16x16-1.ico"), 
                        "actions": [{"key": "copyPath", 
                                            "title": translate("MyPlugins/Explorer_CM", "Copy Path To Clipboard"), 
                                            "icon": InputOutputs.joinPath(Universals.themePath, "Images", "copyPath.ico"), 
                                            "command" : executeCommandOfHamsiManager + " --qm --copyPath \"%1\""}, 
                                    {"key": "emendDirectory", 
                                            "title": translate("MyPlugins/Explorer_CM", "Auto Emend Directory"), 
                                            "icon": InputOutputs.joinPath(Universals.themePath, "Images", "emendDirectory.ico"), 
                                            "command" : executeCommandOfHamsiManager + " --qm --emendDirectory \"%1\""}, 
                                    {"key": "emendDirectoryWithContents", 
                                            "title": translate("MyPlugins/Explorer_CM", "Auto Emend Directory (With Contents)"), 
                                            "icon": InputOutputs.joinPath(Universals.themePath, "Images", "emendDirectoryWithContents.ico"), 
                                            "command" : executeCommandOfHamsiManager + " --qm --emendDirectoryWithContents \"%1\""}, 
                                    {"key": "pack", 
                                            "title": translate("MyPlugins/Explorer_CM", "Pack It"), 
                                            "icon": InputOutputs.joinPath(Universals.themePath, "Images", "pack.ico"), 
                                            "command" : executeCommandOfHamsiManager + " --qm --pack \"%1\""}, 
                                    {"key": "checkIcon", 
                                            "title": translate("MyPlugins/Explorer_CM", "Check Directory Icon"), 
                                            "icon": InputOutputs.joinPath(Universals.themePath, "Images", "checkIcon.ico"), 
                                            "command" : executeCommandOfHamsiManager + " --qm --checkIcon \"%1\""}, 
                                    {"key": "clearEmptyDirectories", 
                                            "title": translate("MyPlugins/Explorer_CM", "Clear Empty Directories"), 
                                            "icon": InputOutputs.joinPath(Universals.themePath, "Images", "clearEmptyDirectories.ico"), 
                                            "command" : executeCommandOfHamsiManager + " --qm --clearEmptyDirectories \"%1\""}, 
                                    {"key": "clearUnneededs", 
                                            "title": translate("MyPlugins/Explorer_CM", "Clear Unneededs"), 
                                            "icon": InputOutputs.joinPath(Universals.themePath, "Images", "clearUnneededs.ico"), 
                                            "command" : executeCommandOfHamsiManager + " --qm --clearUnneededs \"%1\""}, 
                                    {"key": "clearIgnoreds", 
                                            "title": translate("MyPlugins/Explorer_CM", "Clear Ignoreds"), 
                                            "icon": InputOutputs.joinPath(Universals.themePath, "Images", "clearIgnoreds.ico"), 
                                            "command" : executeCommandOfHamsiManager + " --qm --clearIgnoreds \"%1\""}, 
                                    {"key": "fileTree", 
                                            "title": translate("MyPlugins/Explorer_CM", "Build File Tree"), 
                                            "icon": InputOutputs.joinPath(Universals.themePath, "Images", "fileTree.ico"), 
                                            "command" : executeCommandOfHamsiManager + " --qm --fileTree \"%1\""}, 
                                    {"key": "removeOnlySubFiles", 
                                            "title": translate("MyPlugins/Explorer_CM", "Remove Sub Files"), 
                                            "icon": InputOutputs.joinPath(Universals.themePath, "Images", "removeOnlySubFiles.ico"), 
                                            "command" : executeCommandOfHamsiManager + " --qm --removeOnlySubFiles \"%1\""}, 
                                    {"key": "clear", 
                                            "title": translate("MyPlugins/Explorer_CM", "Clear It"), 
                                            "icon": InputOutputs.joinPath(Universals.themePath, "Images", "clear.ico"), 
                                            "command" : executeCommandOfHamsiManager + " --qm --clear \"%1\""}, 
                                    {"key": "search", 
                                            "title": translate("MyPlugins/Explorer_CM", "Search"), 
                                            "icon": InputOutputs.joinPath(Universals.themePath, "Images", "search.ico"), 
                                            "command" : executeCommandOfHamsiManager + " --qm --search \"%1\""}
                                ]}, 
                    {"object": "Directory\\Background",
                        "key": "HamsiManager", 
                        "title": "Hamsi Manager", 
                        "icon": InputOutputs.joinPath(Universals.themePath, "Images", "HamsiManager-16x16-1.ico"), 
                        "actions": [{"key": "copyPath", 
                                            "title": translate("MyPlugins/Explorer_CM", "Copy Path To Clipboard"), 
                                            "icon": InputOutputs.joinPath(Universals.themePath, "Images", "copyPath.ico"), 
                                            "command" : executeCommandOfHamsiManager + " --qm --copyPath \"%V\""}, 
                                    {"key": "emendDirectory", 
                                            "title": translate("MyPlugins/Explorer_CM", "Auto Emend Directory"), 
                                            "icon": InputOutputs.joinPath(Universals.themePath, "Images", "emendDirectory.ico"), 
                                            "command" : executeCommandOfHamsiManager + " --qm --emendDirectory \"%V\""}, 
                                    {"key": "emendDirectoryWithContents", 
                                            "title": translate("MyPlugins/Explorer_CM", "Auto Emend Directory (With Contents)"), 
                                            "icon": InputOutputs.joinPath(Universals.themePath, "Images", "emendDirectoryWithContents.ico"), 
                                            "command" : executeCommandOfHamsiManager + " --qm --emendDirectoryWithContents \"%V\""}, 
                                    {"key": "pack", 
                                            "title": translate("MyPlugins/Explorer_CM", "Pack It"), 
                                            "icon": InputOutputs.joinPath(Universals.themePath, "Images", "pack.ico"), 
                                            "command" : executeCommandOfHamsiManager + " --qm --pack \"%V\""}, 
                                    {"key": "checkIcon", 
                                            "title": translate("MyPlugins/Explorer_CM", "Check Directory Icon"), 
                                            "icon": InputOutputs.joinPath(Universals.themePath, "Images", "checkIcon.ico"), 
                                            "command" : executeCommandOfHamsiManager + " --qm --checkIcon \"%V\""}, 
                                    {"key": "clearEmptyDirectories", 
                                            "title": translate("MyPlugins/Explorer_CM", "Clear Empty Directories"), 
                                            "icon": InputOutputs.joinPath(Universals.themePath, "Images", "clearEmptyDirectories.ico"), 
                                            "command" : executeCommandOfHamsiManager + " --qm --clearEmptyDirectories \"%V\""}, 
                                    {"key": "clearUnneededs", 
                                            "title": translate("MyPlugins/Explorer_CM", "Clear Unneededs"), 
                                            "icon": InputOutputs.joinPath(Universals.themePath, "Images", "clearUnneededs.ico"), 
                                            "command" : executeCommandOfHamsiManager + " --qm --clearUnneededs \"%V\""}, 
                                    {"key": "clearIgnoreds", 
                                            "title": translate("MyPlugins/Explorer_CM", "Clear Ignoreds"), 
                                            "icon": InputOutputs.joinPath(Universals.themePath, "Images", "clearIgnoreds.ico"), 
                                            "command" : executeCommandOfHamsiManager + " --qm --clearIgnoreds \"%V\""}, 
                                    {"key": "fileTree", 
                                            "title": translate("MyPlugins/Explorer_CM", "Build File Tree"), 
                                            "icon": InputOutputs.joinPath(Universals.themePath, "Images", "fileTree.ico"), 
                                            "command" : executeCommandOfHamsiManager + " --qm --fileTree \"%V\""}, 
                                    {"key": "removeOnlySubFiles", 
                                            "title": translate("MyPlugins/Explorer_CM", "Remove Sub Files"), 
                                            "icon": InputOutputs.joinPath(Universals.themePath, "Images", "removeOnlySubFiles.ico"), 
                                            "command" : executeCommandOfHamsiManager + " --qm --removeOnlySubFiles \"%V\""}, 
                                    {"key": "clear", 
                                            "title": translate("MyPlugins/Explorer_CM", "Clear It"), 
                                            "icon": InputOutputs.joinPath(Universals.themePath, "Images", "clear.ico"), 
                                            "command" : executeCommandOfHamsiManager + " --qm --clear \"%V\""}, 
                                    {"key": "search", 
                                            "title": translate("MyPlugins/Explorer_CM", "Search"), 
                                            "icon": InputOutputs.joinPath(Universals.themePath, "Images", "search.ico"), 
                                            "command" : executeCommandOfHamsiManager + " --qm --search \"%V\""}
                                ]}, 
                    {"object": "*",
                        "key": "HamsiManagerManage", 
                        "title": translate("MyPlugins/Explorer_CM", "Hamsi Manager ( Manage )"), 
                        "icon": InputOutputs.joinPath(Universals.themePath, "Images", "HamsiManager-16x16-1.ico"), 
                        "actions": [{"key": "Organize", 
                                            "title": translate("MyPlugins/Explorer_CM", "As Last Selected Table"), 
                                            "icon": InputOutputs.joinPath(Universals.themePath, "Images", "HamsiManager-16x16-1.ico"), 
                                            "command" : executeCommandOfHamsiManager + " \"%1\""}, 
                                    {"key": "Organize0", 
                                            "title": translate("MyPlugins/Explorer_CM", "As Folder Table"), 
                                            "icon": InputOutputs.joinPath(Universals.themePath, "Images", "HamsiManager-16x16-1.ico"), 
                                            "command" : executeCommandOfHamsiManager + " -t 0 \"%1\""}, 
                                    {"key": "Organize1", 
                                            "title": translate("MyPlugins/Explorer_CM", "As File Table"), 
                                            "icon": InputOutputs.joinPath(Universals.themePath, "Images", "HamsiManager-16x16-1.ico"), 
                                            "command" : executeCommandOfHamsiManager + " -t 1 \"%1\""}, 
                                    {"key": "Organize2", 
                                            "title": translate("MyPlugins/Explorer_CM", "As Music Table"), 
                                            "icon": InputOutputs.joinPath(Universals.themePath, "Images", "HamsiManager-16x16-1.ico"), 
                                            "command" : executeCommandOfHamsiManager + " -t 2 \"%1\""}, 
                                    {"key": "Organize3", 
                                            "title": translate("MyPlugins/Explorer_CM", "As Subfolder Table"), 
                                            "icon": InputOutputs.joinPath(Universals.themePath, "Images", "HamsiManager-16x16-1.ico"), 
                                            "command" : executeCommandOfHamsiManager + " -t 3 \"%1\""}
                                ]}, 
                    {"object": "Directory",
                        "key": "HamsiManagerManage", 
                        "title": translate("MyPlugins/Explorer_CM", "Hamsi Manager ( Manage )"), 
                        "icon": InputOutputs.joinPath(Universals.themePath, "Images", "HamsiManager-16x16-1.ico"), 
                        "actions": [{"key": "Organize", 
                                            "title": translate("MyPlugins/Explorer_CM", "As Last Selected Table"), 
                                            "icon": InputOutputs.joinPath(Universals.themePath, "Images", "HamsiManager-16x16-1.ico"), 
                                            "command" : executeCommandOfHamsiManager + " \"%1\""}, 
                                    {"key": "Organize0", 
                                            "title": translate("MyPlugins/Explorer_CM", "As Folder Table"), 
                                            "icon": InputOutputs.joinPath(Universals.themePath, "Images", "HamsiManager-16x16-1.ico"), 
                                            "command" : executeCommandOfHamsiManager + " -t 0 \"%1\""}, 
                                    {"key": "Organize1", 
                                            "title": translate("MyPlugins/Explorer_CM", "As File Table"), 
                                            "icon": InputOutputs.joinPath(Universals.themePath, "Images", "HamsiManager-16x16-1.ico"), 
                                            "command" : executeCommandOfHamsiManager + " -t 1 \"%1\""}, 
                                    {"key": "Organize2", 
                                            "title": translate("MyPlugins/Explorer_CM", "As Music Table"), 
                                            "icon": InputOutputs.joinPath(Universals.themePath, "Images", "HamsiManager-16x16-1.ico"), 
                                            "command" : executeCommandOfHamsiManager + " -t 2 \"%1\""}, 
                                    {"key": "Organize3", 
                                            "title": translate("MyPlugins/Explorer_CM", "As Subfolder Table"), 
                                            "icon": InputOutputs.joinPath(Universals.themePath, "Images", "HamsiManager-16x16-1.ico"), 
                                            "command" : executeCommandOfHamsiManager + " -t 3 \"%1\""}
                                ]}, 
                    {"object": "Directory\\Background",
                        "key": "HamsiManagerManage", 
                        "title": translate("MyPlugins/Explorer_CM", "Hamsi Manager ( Manage )"), 
                        "icon": InputOutputs.joinPath(Universals.themePath, "Images", "HamsiManager-16x16-1.ico"), 
                        "actions": [{"key": "Organize", 
                                            "title": translate("MyPlugins/Explorer_CM", "As Last Selected Table"), 
                                            "icon": InputOutputs.joinPath(Universals.themePath, "Images", "HamsiManager-16x16-1.ico"), 
                                            "command" : executeCommandOfHamsiManager + " \"%1\""}, 
                                    {"key": "Organize0", 
                                            "title": translate("MyPlugins/Explorer_CM", "As Folder Table"), 
                                            "icon": InputOutputs.joinPath(Universals.themePath, "Images", "HamsiManager-16x16-1.ico"), 
                                            "command" : executeCommandOfHamsiManager + " -t 0 \"%1\""}, 
                                    {"key": "Organize1", 
                                            "title": translate("MyPlugins/Explorer_CM", "As File Table"), 
                                            "icon": InputOutputs.joinPath(Universals.themePath, "Images", "HamsiManager-16x16-1.ico"), 
                                            "command" : executeCommandOfHamsiManager + " -t 1 \"%1\""}, 
                                    {"key": "Organize2", 
                                            "title": translate("MyPlugins/Explorer_CM", "As Music Table"), 
                                            "icon": InputOutputs.joinPath(Universals.themePath, "Images", "HamsiManager-16x16-1.ico"), 
                                            "command" : executeCommandOfHamsiManager + " -t 2 \"%1\""}, 
                                    {"key": "Organize3", 
                                            "title": translate("MyPlugins/Explorer_CM", "As Subfolder Table"), 
                                            "icon": InputOutputs.joinPath(Universals.themePath, "Images", "HamsiManager-16x16-1.ico"), 
                                            "command" : executeCommandOfHamsiManager + " -t 3 \"%1\""}
                                ]}
                    ]
    rootReg = winreg.ConnectRegistry(None,winreg.HKEY_CLASSES_ROOT)
    try:
        for object in actionsValues:
            mainKey = winreg.OpenKey(rootReg, object["object"] + "\\shell", 0, winreg.KEY_WRITE)
            winreg.CreateKey(mainKey, object["key"])
            hamsiKey = winreg.OpenKey(mainKey, object["key"], 0, winreg.KEY_WRITE)
            winreg.SetValueEx(hamsiKey,"MUIVerb",0, winreg.REG_SZ, Universals.trEncode(str(object["title"]), InputOutputs.defaultFileSystemEncoding))
            winreg.SetValueEx(hamsiKey,"ExtendedSubCommandsKey",0, winreg.REG_SZ, object["object"] + "\\ContextMenus\\" + object["key"])
            try:winreg.SetValueEx(hamsiKey,"Icon",0, winreg.REG_SZ, Universals.trEncode(str(object["icon"]), InputOutputs.defaultFileSystemEncoding))
            except:winreg.SetValueEx(hamsiKey,"Icon",0, winreg.REG_SZ, str(object["icon"]))
            winreg.CreateKey(rootReg, object["object"] + "\\ContextMenus")
            mainContextMenusKey = winreg.OpenKey(rootReg, object["object"] + "\\ContextMenus", 0, winreg.KEY_WRITE)
            for action in object["actions"]:
                if action["key"]=="checkIcon":
                    if Universals.isActiveDirectoryCover==False:
                        continue
                winreg.CreateKey(mainContextMenusKey, object["key"] + "\\Shell\\" + action["key"])
                actionKey = winreg.OpenKey(mainContextMenusKey, object["key"] + "\\Shell\\" + action["key"], 0, winreg.KEY_WRITE)
                try:winreg.SetValueEx(actionKey,"MUIVerb",0, winreg.REG_SZ, Universals.trEncode(str(action["title"]), InputOutputs.defaultFileSystemEncoding))
                except:winreg.SetValueEx(actionKey,"MUIVerb",0, winreg.REG_SZ, str(action["title"]))
                try:winreg.SetValueEx(actionKey,"Icon",0, winreg.REG_SZ, Universals.trEncode(str(action["icon"]), InputOutputs.defaultFileSystemEncoding))
                except:winreg.SetValueEx(actionKey,"Icon",0, winreg.REG_SZ, str(action["icon"]))
                winreg.CreateKey(mainContextMenusKey, object["key"] + "\\Shell\\" + action["key"] + "\\command")
                actionCommandKey = winreg.OpenKey(mainContextMenusKey, object["key"] + "\\Shell\\" + action["key"] + "\\command", 0, winreg.KEY_WRITE)
                try:winreg.SetValueEx(actionCommandKey,"",0, winreg.REG_SZ, Universals.trEncode(str(action["command"]), InputOutputs.defaultFileSystemEncoding))
                except:winreg.SetValueEx(actionCommandKey,"",0, winreg.REG_SZ, str(action["command"]))
                winreg.CloseKey(actionCommandKey)
                winreg.CloseKey(actionKey)
            winreg.CloseKey(mainContextMenusKey)
            winreg.CloseKey(hamsiKey)
            winreg.CloseKey(mainKey)
    except WindowsError:
        winreg.CloseKey(rootReg)
        cla, error, trbk = sys.exc_info()
        if str(error).find("[Error 5]")!=-1:
            Dialogs.showError(translate("MyPlugins/Explorer_CM", "Access Denied"), 
                         translate("MyPlugins/Explorer_CM", "Please run Hamsi Manager as Administrator and try again."))
        else:
            ReportBug.ReportBug()
        return False
    winreg.CloseKey(rootReg)
    
    #if isAlreadyInstalled:
    #    return "AlreadyInstalled"
    return True
    

def uninstallThisPlugin():
    isAlreadyUninstalled = False
    if Variables.isPython3k:
        import winreg
    else:
        import _winreg as winreg
    executeCommandOfHamsiManager = Execute.getExecuteCommandOfHamsiManager()
    iconPath =  InputOutputs.joinPath(Universals.themePath, "Images", "HamsiManager-16x16-1.ico")
    
    actionsValues = [{"object": "*",
                        "key": "HamsiManager", 
                        "actions": [{"key": "copyPath"}, 
                                    {"key": "emendFile"}, 
                                    {"key": "hash"}, 
                                    {"key": "textCorrector"}, 
                                    {"key": "search"}
                                ]}, 
                    {"object": "Directory",
                        "key": "HamsiManager", 
                        "actions": [{"key": "copyPath"}, 
                                    {"key": "emendDirectory"}, 
                                    {"key": "emendDirectoryWithContents"}, 
                                    {"key": "pack"}, 
                                    {"key": "checkIcon"}, 
                                    {"key": "clearEmptyDirectories"}, 
                                    {"key": "clearUnneededs"}, 
                                    {"key": "clearIgnoreds"}, 
                                    {"key": "fileTree"}, 
                                    {"key": "removeOnlySubFiles"}, 
                                    {"key": "clear"}, 
                                    {"key": "search"}
                                ]}, 
                    {"object": "Directory\\Background",
                        "key": "HamsiManager", 
                        "actions": [{"key": "copyPath"}, 
                                    {"key": "emendDirectory"}, 
                                    {"key": "emendDirectoryWithContents"}, 
                                    {"key": "pack"}, 
                                    {"key": "checkIcon"}, 
                                    {"key": "clearEmptyDirectories"}, 
                                    {"key": "clearUnneededs"}, 
                                    {"key": "clearIgnoreds"}, 
                                    {"key": "fileTree"}, 
                                    {"key": "removeOnlySubFiles"}, 
                                    {"key": "clear"}, 
                                    {"key": "search"}
                                ]}, 
                    {"object": "*",
                        "key": "HamsiManagerManage", 
                        "actions": [{"key": "Organize"}, 
                                    {"key": "Organize0"}, 
                                    {"key": "Organize1"}, 
                                    {"key": "Organize2"}, 
                                    {"key": "Organize3"}
                                ]}, 
                    {"object": "Directory",
                        "key": "HamsiManagerManage", 
                        "actions": [{"key": "Organize"}, 
                                    {"key": "Organize0"}, 
                                    {"key": "Organize1"}, 
                                    {"key": "Organize2"}, 
                                    {"key": "Organize3"}
                                ]}, 
                    {"object": "Directory\\Background",
                        "key": "HamsiManagerManage", 
                        "actions": [{"key": "Organize"}, 
                                    {"key": "Organize0"}, 
                                    {"key": "Organize1"}, 
                                    {"key": "Organize2"}, 
                                    {"key": "Organize3"}
                                ]}
                    ]
    rootReg = winreg.ConnectRegistry(None,winreg.HKEY_CLASSES_ROOT)
    try:
        for object in actionsValues:
            mainKey = winreg.OpenKey(rootReg, object["object"] + "\\shell", 0, winreg.KEY_WRITE)
            try:winreg.DeleteKey(mainKey, object["key"])
            except:pass
            winreg.CloseKey(mainKey)
            mainContextMenusKey = winreg.OpenKey(rootReg, object["object"] + "\\ContextMenus", 0, winreg.KEY_WRITE)
            for action in object["actions"]:
                try:
                    actionKey = winreg.OpenKey(mainContextMenusKey, object["key"] + "\\Shell\\" + action["key"], 0, winreg.KEY_WRITE)
                    try:winreg.DeleteKey(actionKey, "command")
                    except:pass
                    winreg.CloseKey(actionKey)
                    shellKey = winreg.OpenKey(mainContextMenusKey, object["key"] + "\\Shell", 0, winreg.KEY_WRITE)
                    try:winreg.DeleteKey(shellKey, action["key"])
                    except:pass
                    winreg.CloseKey(shellKey)
                except:pass
            objectKey = winreg.OpenKey(mainContextMenusKey, object["key"], 0, winreg.KEY_WRITE)
            try:winreg.DeleteKey(objectKey, "Shell")
            except:pass
            winreg.CloseKey(objectKey)
            try:winreg.DeleteKey(mainContextMenusKey, object["key"])
            except:pass
            winreg.CloseKey(mainContextMenusKey)
    except WindowsError:
        winreg.CloseKey(rootReg)
        cla, error, trbk = sys.exc_info()
        if str(error).find("[Error 5]")!=-1:
            Dialogs.showError(translate("MyPlugins/Explorer_CM", "Access Denied"), 
                         translate("MyPlugins/Explorer_CM", "Please run Hamsi Manager as Administrator and try again."))
        elif str(error).find("[Error 2]")!=-1:
            isAlreadyUninstalled = True #Error : The system cannot find the file specified. Cause : Already Uninstalled
        else:
            ReportBug.ReportBug()
        return False
    winreg.CloseKey(rootReg)
    
    if isAlreadyUninstalled:
        return "isAlreadyUninstalled"
    return True
    
    
    
    
