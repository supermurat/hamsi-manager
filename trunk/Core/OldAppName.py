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


def checkOldAppNameAndSettings():
    from Core import Variables, Universals
    import InputOutputs
    return InputOutputs.isDir(Variables.userDirectoryPath + "/.OrganizasyonizM")
    
def checkOldAppNameInSystem():
    import InputOutputs
    return InputOutputs.isFile("/usr/bin/OrganizasyonizM")
    
def getSettingsFromOldNameAndSettings():
    from Core import Variables, Universals
    import InputOutputs
    if InputOutputs.isDir(Variables.userDirectoryPath + "/.OrganizasyonizM"):
        if InputOutputs.isFile(Variables.userDirectoryPath + "/.OrganizasyonizM/universalSettings.ini"):
            from Core.MyObjects import MSettings, trForM
            oldSettins = MSettings(trForM(Variables.userDirectoryPath+"/.OrganizasyonizM/universalSettings.ini") ,MSettings.IniFormat)
            newSettings = MSettings(trForM(Variables.userDirectoryPath+"/.HamsiApps/universalSettings.ini") ,MSettings.IniFormat)
            for oldKey in oldSettins.allKeys():
                newKey = str(oldKey).replace("OrganizasyonizM", "HamsiManager")
                newSettings.setValue(newKey, oldSettins.value(oldKey))
        if InputOutputs.isFile(Variables.userDirectoryPath + "/.OrganizasyonizM/mySettings.ini"):
            from Core.MyObjects import MSettings, trForM
            oldSettins = MSettings(trForM(Variables.userDirectoryPath+"/.OrganizasyonizM/mySettings.ini") ,MSettings.IniFormat)
            newSettings = MSettings(trForM(Variables.userDirectoryPath+"/.HamsiApps/HamsiManager/mySettings.ini") ,MSettings.IniFormat)
            for oldKey in oldSettins.allKeys():
                newKey = str(oldKey).replace("OrganizasyonizM", "HamsiManager")
                newSettings.setValue(newKey, oldSettins.value(oldKey))
        if InputOutputs.isFile(Variables.userDirectoryPath + "/.OrganizasyonizM/bookmarks.sqlite"):
            InputOutputs.moveFileOrDir(Variables.userDirectoryPath + "/.OrganizasyonizM/bookmarks.sqlite", 
                                       Variables.userDirectoryPath + "/.HamsiApps/HamsiManager/bookmarks.sqlite")
        if InputOutputs.isFile(Variables.userDirectoryPath + "/.OrganizasyonizM/codesOfUser.py"):
            InputOutputs.moveFileOrDir(Variables.userDirectoryPath + "/.OrganizasyonizM/codesOfUser.py", 
                                       Variables.userDirectoryPath + "/.HamsiApps/HamsiManager/codesOfUser.py")
        if InputOutputs.isFile(Variables.userDirectoryPath + "/.OrganizasyonizM/LastState"):
            InputOutputs.moveFileOrDir(Variables.userDirectoryPath + "/.OrganizasyonizM/LastState", 
                                       Variables.userDirectoryPath + "/.HamsiApps/HamsiManager/LastState")
        if InputOutputs.isFile(Variables.userDirectoryPath + "/.OrganizasyonizM/logs.txt"):
            InputOutputs.moveFileOrDir(Variables.userDirectoryPath + "/.OrganizasyonizM/logs.txt", 
                                       Variables.userDirectoryPath + "/.HamsiApps/HamsiManager/logs.txt")
        if InputOutputs.isFile(Variables.userDirectoryPath + "/.OrganizasyonizM/searchAndReplaceTable.sqlite"):
            InputOutputs.moveFileOrDir(Variables.userDirectoryPath + "/.OrganizasyonizM/searchAndReplaceTable.sqlite", 
                                       Variables.userDirectoryPath + "/.HamsiApps/HamsiManager/searchAndReplaceTable.sqlite")
        if InputOutputs.isDir(Variables.userDirectoryPath + "/.OrganizasyonizM/SettingFiles"):
            isMakeThis = True
            if InputOutputs.isDir(Variables.userDirectoryPath + "/.HamsiApps/HamsiManager/SettingFiles"):
                if InputOutputs.isDirEmpty(Variables.userDirectoryPath + "/.HamsiApps/HamsiManager/SettingFiles"):
                    InputOutputs.removeDir(Variables.userDirectoryPath + "/.HamsiApps/HamsiManager/SettingFiles")
                else:
                    isMakeThis = False
            if isMakeThis:
                InputOutputs.moveFileOrDir(Variables.userDirectoryPath + "/.OrganizasyonizM/SettingFiles", 
                                       Variables.userDirectoryPath + "/.HamsiApps/HamsiManager/SettingFiles")
        if InputOutputs.isDir(Variables.userDirectoryPath + "/.OrganizasyonizM/BackUps"):
            isMakeThis = True
            if InputOutputs.isDir(Variables.userDirectoryPath + "/.HamsiApps/HamsiManager/BackUps"):
                if InputOutputs.isDirEmpty(Variables.userDirectoryPath + "/.HamsiApps/HamsiManager/BackUps"):
                    InputOutputs.removeDir(Variables.userDirectoryPath + "/.HamsiApps/HamsiManager/BackUps")
                else:
                    isMakeThis = False
            if isMakeThis:
                InputOutputs.moveFileOrDir(Variables.userDirectoryPath + "/.OrganizasyonizM/BackUps", 
                                       Variables.userDirectoryPath + "/.HamsiApps/HamsiManager/BackUps")
        if Variables.isAvailableKDE4():
            if InputOutputs.isFile(Variables.userDirectoryPath + "/.kde4/share/config/OrganizasyonizMrc"):
                InputOutputs.moveFileOrDir(Variables.userDirectoryPath + "/.kde4/share/config/OrganizasyonizMrc", 
                                           Variables.getKDE4HomePath() + "/share/config/HamsiManagerrc")
        for langCode in Variables.getInstalledLanguagesCodes():
            if InputOutputs.isFile(Variables.userDirectoryPath + "/.kde4/share/locale/" + langCode + "/LC_MESSAGES/OrganizasyonizM.mo"):
                from Core import MyConfigure
                MyConfigure.installKDE4Language(langCode)
        Universals.fillMySettings(True)
        Universals.saveSettings()
    
def checkAndGetPlugins():
    from Core import Variables, Universals
    import InputOutputs
    for plugin in Variables.getMyPluginsNames():
        isInstalled = False
        pluginModule = __import__("MyPlugins." + plugin, globals(), locals(), ["pluginFiles", "pluginDirectory", "setupDirectory"], -1)
        for pluginFile in pluginModule.pluginFiles:
            if InputOutputs.isFile((pluginModule.setupDirectory + "/" + pluginFile).replace("HamsiManager", "OrganizasyonizM")):
                isInstalled = True
                break
        if pluginModule.pluginDirectory!="":
            if InputOutputs.isDir((pluginModule.setupDirectory + "/" + pluginModule.pluginDirectory).replace("HamsiManager", "OrganizasyonizM")):
                isInstalled = True
        if isInstalled:
            from MyPlugins import installPlugin
            installPlugin(plugin, True)
        
        
def clearOldAppNameAndSettings():
    from Core import Variables, Universals, Dialogs, Organizer
    import InputOutputs
    from Core.MyObjects import translate
    #Clear language file
    for langCode in Variables.getInstalledLanguagesCodes():
        if InputOutputs.isFile(Variables.userDirectoryPath + "/.kde4/share/locale/" + langCode + "/LC_MESSAGES/OrganizasyonizM.mo"):
            InputOutputs.removeFile(Variables.userDirectoryPath + "/.kde4/share/locale/" + langCode + "/LC_MESSAGES/OrganizasyonizM.mo")
    #Clear config file
    if InputOutputs.isFile(Variables.userDirectoryPath + "/.kde4/share/config/OrganizasyonizMrc"):
        InputOutputs.removeFile(Variables.userDirectoryPath + "/.kde4/share/config/OrganizasyonizMrc")
    #Clear My Plugins
    for plugin in Variables.getMyPluginsNames():
        pluginModule = __import__("MyPlugins." + plugin, globals(), locals(), ["pluginFiles", "pluginDirectory", "setupDirectory"], -1)
        for pluginFile in pluginModule.pluginFiles:
            pluginFilePath = (pluginModule.setupDirectory + "/" + pluginFile).replace("HamsiManager", "OrganizasyonizM")
            if InputOutputs.isFile(pluginFilePath):
                InputOutputs.removeFile(pluginFilePath)
        if pluginModule.pluginDirectory!="":
            pluginDirectoryPath = (pluginModule.setupDirectory + "/" + pluginModule.pluginDirectory).replace("HamsiManager", "OrganizasyonizM")
            if InputOutputs.isDir(pluginDirectoryPath):
                InputOutputs.removeFileOrDir(pluginDirectoryPath, True)
    #Clear Setting Directory
    if InputOutputs.isDir(Variables.userDirectoryPath + "/.OrganizasyonizM"):
        isRemoveOldSettingDirectory = False
        if InputOutputs.isDirEmpty(Variables.userDirectoryPath + "/.OrganizasyonizM"):
            isRemoveOldSettingDirectory = True
        else:
            answer = Dialogs.ask(translate("HamsiManager", "The Old Version Was Detected"),
                    str(translate("HamsiManager", "OrganizasyonizM setting directory was detected.Are you want to delete \"%s\"?<br>Note:This directory will not be used anymore.You can delete this directory.")) % Organizer.getLink(Variables.userDirectoryPath + "/.OrganizasyonizM"), False, "OrganizasyonizM Setting Directory Was Detected")
            if answer==Dialogs.Yes:
                isRemoveOldSettingDirectory = True
        if isRemoveOldSettingDirectory:
            InputOutputs.removeFileOrDir(Variables.userDirectoryPath + "/.OrganizasyonizM", True)

def checkAndGetOldAppNameInSystem():
    from Core import Variables, Dialogs, Execute, Organizer, Universals
    import InputOutputs
    from Core.MyObjects import translate
    #Clear OrganizasyonizM in system(/usr/bin/OrganizasyonizM) by root
    if Variables.isRunningAsRoot():
        if InputOutputs.isFile("/usr/bin/OrganizasyonizM"):
            InputOutputs.removeFile("/usr/bin/OrganizasyonizM")
            if InputOutputs.isFile("/usr/bin/hamsimanager")==False:
                InputOutputs.createSymLink(Execute.findExecutablePath("HamsiManager"), "/usr/bin/hamsimanager")
    else:
        answer = Dialogs.ask(translate("HamsiManager", "The Old Version Was Detected"),
                    str(translate("HamsiManager", "Executable OrganizasyonizM file was detected in your system.Are you want to delete \"%s\" and creat new Executable Hamsi Manager(\"%s\")?")) % (Organizer.getLink("/usr/bin/OrganizasyonizM") , Organizer.getLink("/usr/bin/hamsimanager")), False, "Executable OrganizasyonizM Was Detected")
        if answer==Dialogs.Yes:
            Execute.executeAsRootWithThread(["--checkAndGetOldAppNameInSystem"], "HamsiManager")
    
