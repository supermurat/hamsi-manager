# -*- coding: utf-8 -*-

def checkOldAppNameAndSettings():
    import Variables, InputOutputs, Universals
    return InputOutputs.isDir(Variables.userDirectoryPath + "/.OrganizasyonizM")
    
def checkOldAppNameInSystem():
    import InputOutputs
    return InputOutputs.isFile("/usr/bin/OrganizasyonizM")
    
def getSettingsFromOldNameAndSettings():
    import Variables, InputOutputs, Universals
    if InputOutputs.isDir(Variables.userDirectoryPath + "/.OrganizasyonizM"):
        if InputOutputs.isFile(Variables.userDirectoryPath + "/.OrganizasyonizM/universalSettings.ini"):
            from MyObjects import MSettings
            oldSettins = MSettings((Variables.userDirectoryPath+"/.OrganizasyonizM/universalSettings.ini").decode("utf-8") ,MSettings.IniFormat)
            newSettings = MSettings((Variables.userDirectoryPath+"/.HamsiApps/universalSettings.ini").decode("utf-8") ,MSettings.IniFormat)
            for oldKey in oldSettins.allKeys():
                newKey = str(oldKey).replace("OrganizasyonizM", "HamsiManager")
                newSettings.setValue(newKey, oldSettins.value(oldKey))
        if InputOutputs.isFile(Variables.userDirectoryPath + "/.OrganizasyonizM/mySettings.ini"):
            from MyObjects import MSettings
            oldSettins = MSettings((Variables.userDirectoryPath+"/.OrganizasyonizM/mySettings.ini").decode("utf-8") ,MSettings.IniFormat)
            newSettings = MSettings((Variables.userDirectoryPath+"/.HamsiApps/HamsiManager/mySettings.ini").decode("utf-8") ,MSettings.IniFormat)
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
                import MyConfigure
                MyConfigure.installKDE4Language(langCode)
        Universals.fillMySettings(True)
        Universals.saveSettings()
    
def checkAndGetPlugins():
    import Variables, InputOutputs, Universals
    for plugin in Variables.getMyPluginsNames():
        isInstalled = False
        exec ("from MyPlugins." + plugin + " import pluginName, setupDirectory, pluginFiles, pluginDirectory")
        for pluginFile in pluginFiles:
            if InputOutputs.isFile((setupDirectory + "/" + pluginFile).replace("HamsiManager", "OrganizasyonizM")):
                isInstalled = True
                break
        if pluginDirectory!="":
            if InputOutputs.isDir((setupDirectory + "/" + pluginDirectory).replace("HamsiManager", "OrganizasyonizM")):
                isInstalled = True
        if isInstalled:
            from MyPlugins import installPlugin
            installPlugin(plugin, True)
        
        
def clearOldAppNameAndSettings():
    import Variables, InputOutputs, Universals, Dialogs, Organizer
    from MyObjects import translate
    #Clear language file
    for langCode in Variables.getInstalledLanguagesCodes():
        if InputOutputs.isFile(Variables.userDirectoryPath + "/.kde4/share/locale/" + langCode + "/LC_MESSAGES/OrganizasyonizM.mo"):
            InputOutputs.removeFile(Variables.userDirectoryPath + "/.kde4/share/locale/" + langCode + "/LC_MESSAGES/OrganizasyonizM.mo")
    #Clear config file
    if InputOutputs.isFile(Variables.userDirectoryPath + "/.kde4/share/config/OrganizasyonizMrc"):
        InputOutputs.removeFile(Variables.userDirectoryPath + "/.kde4/share/config/OrganizasyonizMrc")
    #Clear My Plugins
    for plugin in Variables.getMyPluginsNames():
        exec ("from MyPlugins." + plugin + " import pluginName, setupDirectory, pluginFiles, pluginDirectory")
        for pluginFile in pluginFiles:
            pluginFilePath = (setupDirectory + "/" + pluginFile).replace("HamsiManager", "OrganizasyonizM")
            if InputOutputs.isFile(pluginFilePath):
                InputOutputs.removeFile(pluginFilePath)
        if pluginDirectory!="":
            pluginDirectoryPath = (setupDirectory + "/" + pluginDirectory).replace("HamsiManager", "OrganizasyonizM")
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
    import Variables, InputOutputs, Dialogs, Execute, Organizer, Universals
    from MyObjects import translate
    #Clear OrganizasyonizM in system(/usr/bin/OrganizasyonizM) by root
    if Execute.isRunningAsRoot():
        if InputOutputs.isFile("/usr/bin/OrganizasyonizM"):
            InputOutputs.removeFile("/usr/bin/OrganizasyonizM")
        if InputOutputs.isFile("/usr/bin/hamsimanager")==False:
            InputOutputs.createSymLink(Variables.executableHamsiManagerPath, "/usr/bin/hamsimanager")
    else:
        answer = Dialogs.ask(translate("HamsiManager", "The Old Version Was Detected"),
                    str(translate("HamsiManager", "Executable OrganizasyonizM file was detected in your system.Are you want to delete \"%s\" and creat new Executable Hamsi Manager(\"%s\")?")) % (Organizer.getLink("/usr/bin/OrganizasyonizM") , Organizer.getLink("/usr/bin/hamsimanager")), False, "Executable OrganizasyonizM Was Detected")
        if answer==Dialogs.Yes:
            Execute.executeHamsiManagerAsRoot("-checkAndGetOldAppNameInSystem")
    
