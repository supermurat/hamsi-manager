# -*- coding: utf-8 -*-

def checkOldAppNameAndSettings():
    import InputOutputs, Universals
    return InputOutputs.isDir(Universals.userDirectoryPath + "/.OrganizasyonizM")
    
def checkOldAppNameInSystem():
    import InputOutputs
    return InputOutputs.isFile("/usr/bin/OrganizasyonizM")
    
def getSettingsFromOldNameAndSettings():
    import InputOutputs, Universals
    if InputOutputs.isDir(Universals.userDirectoryPath + "/.OrganizasyonizM"):
        if InputOutputs.isFile(Universals.userDirectoryPath + "/.OrganizasyonizM/universalSettings.ini"):
            from MyObjects import MSettings
            oldSettins = MSettings((Universals.userDirectoryPath+"/.OrganizasyonizM/universalSettings.ini").decode("utf-8") ,MSettings.IniFormat)
            newSettings = MSettings((Universals.userDirectoryPath+"/.HamsiApps/universalSettings.ini").decode("utf-8") ,MSettings.IniFormat)
            for oldKey in oldSettins.allKeys():
                newKey = str(oldKey).replace("OrganizasyonizM", "HamsiManager")
                newSettings.setValue(newKey, oldSettins.value(oldKey))
        if InputOutputs.isFile(Universals.userDirectoryPath + "/.OrganizasyonizM/mySettings.ini"):
            from MyObjects import MSettings
            oldSettins = MSettings((Universals.userDirectoryPath+"/.OrganizasyonizM/mySettings.ini").decode("utf-8") ,MSettings.IniFormat)
            newSettings = MSettings((Universals.userDirectoryPath+"/.HamsiApps/HamsiManager/mySettings.ini").decode("utf-8") ,MSettings.IniFormat)
            for oldKey in oldSettins.allKeys():
                newKey = str(oldKey).replace("OrganizasyonizM", "HamsiManager")
                newSettings.setValue(newKey, oldSettins.value(oldKey))
        if InputOutputs.isFile(Universals.userDirectoryPath + "/.OrganizasyonizM/bookmarks.sqlite"):
            InputOutputs.moveFileOrDir(Universals.userDirectoryPath + "/.OrganizasyonizM/bookmarks.sqlite", 
                                       Universals.userDirectoryPath + "/.HamsiApps/HamsiManager/bookmarks.sqlite")
        if InputOutputs.isFile(Universals.userDirectoryPath + "/.OrganizasyonizM/codesOfUser.py"):
            InputOutputs.moveFileOrDir(Universals.userDirectoryPath + "/.OrganizasyonizM/codesOfUser.py", 
                                       Universals.userDirectoryPath + "/.HamsiApps/HamsiManager/codesOfUser.py")
        if InputOutputs.isFile(Universals.userDirectoryPath + "/.OrganizasyonizM/LastState"):
            InputOutputs.moveFileOrDir(Universals.userDirectoryPath + "/.OrganizasyonizM/LastState", 
                                       Universals.userDirectoryPath + "/.HamsiApps/HamsiManager/LastState")
        if InputOutputs.isFile(Universals.userDirectoryPath + "/.OrganizasyonizM/logs.txt"):
            InputOutputs.moveFileOrDir(Universals.userDirectoryPath + "/.OrganizasyonizM/logs.txt", 
                                       Universals.userDirectoryPath + "/.HamsiApps/HamsiManager/logs.txt")
        if InputOutputs.isFile(Universals.userDirectoryPath + "/.OrganizasyonizM/searchAndReplaceTable.sqlite"):
            InputOutputs.moveFileOrDir(Universals.userDirectoryPath + "/.OrganizasyonizM/searchAndReplaceTable.sqlite", 
                                       Universals.userDirectoryPath + "/.HamsiApps/HamsiManager/searchAndReplaceTable.sqlite")
        if InputOutputs.isDir(Universals.userDirectoryPath + "/.OrganizasyonizM/SettingFiles"):
            isMakeThis = True
            if InputOutputs.isDir(Universals.userDirectoryPath + "/.HamsiApps/HamsiManager/SettingFiles"):
                if InputOutputs.isDirEmpty(Universals.userDirectoryPath + "/.HamsiApps/HamsiManager/SettingFiles"):
                    InputOutputs.removeDir(Universals.userDirectoryPath + "/.HamsiApps/HamsiManager/SettingFiles")
                else:
                    isMakeThis = False
            if isMakeThis:
                InputOutputs.moveFileOrDir(Universals.userDirectoryPath + "/.OrganizasyonizM/SettingFiles", 
                                       Universals.userDirectoryPath + "/.HamsiApps/HamsiManager/SettingFiles")
        if InputOutputs.isDir(Universals.userDirectoryPath + "/.OrganizasyonizM/BackUps"):
            isMakeThis = True
            if InputOutputs.isDir(Universals.userDirectoryPath + "/.HamsiApps/HamsiManager/BackUps"):
                if InputOutputs.isDirEmpty(Universals.userDirectoryPath + "/.HamsiApps/HamsiManager/BackUps"):
                    InputOutputs.removeDir(Universals.userDirectoryPath + "/.HamsiApps/HamsiManager/BackUps")
                else:
                    isMakeThis = False
            if isMakeThis:
                InputOutputs.moveFileOrDir(Universals.userDirectoryPath + "/.OrganizasyonizM/BackUps", 
                                       Universals.userDirectoryPath + "/.HamsiApps/HamsiManager/BackUps")
        if InputOutputs.isFile(Universals.userDirectoryPath + "/.kde4/share/config/OrganizasyonizMrc"):
            InputOutputs.moveFileOrDir(Universals.userDirectoryPath + "/.kde4/share/config/OrganizasyonizMrc", 
                                       Universals.getKDE4HomePath() + "/share/config/HamsiManagerrc")
        for langCode in InputOutputs.getInstalledLanguagesCodes():
            if InputOutputs.isFile(Universals.userDirectoryPath + "/.kde4/share/locale/" + langCode + "/LC_MESSAGES/OrganizasyonizM.mo"):
                import MyConfigure
                MyConfigure.installKDE4Language(langCode)
        Universals.fillMySettings(True)
        Universals.saveSettings()
    
def checkAndGetPlugins():
    import InputOutputs, Universals
    for plugin in InputOutputs.getMyPluginsNames():
        isInstalled = False
        exec "from MyPlugins." + plugin + " import pluginName, setupDirectory, pluginFiles, pluginDirectory"
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
    import InputOutputs, Universals, Dialogs, Organizer
    from MyObjects import translate
    #Clear language file
    for langCode in InputOutputs.getInstalledLanguagesCodes():
        if InputOutputs.isFile(Universals.userDirectoryPath + "/.kde4/share/locale/" + langCode + "/LC_MESSAGES/OrganizasyonizM.mo"):
            InputOutputs.removeFile(Universals.userDirectoryPath + "/.kde4/share/locale/" + langCode + "/LC_MESSAGES/OrganizasyonizM.mo")
    #Clear config file
    if InputOutputs.isFile(Universals.userDirectoryPath + "/.kde4/share/config/OrganizasyonizMrc"):
        InputOutputs.removeFile(Universals.userDirectoryPath + "/.kde4/share/config/OrganizasyonizMrc")
    #Clear My Plugins
    for plugin in InputOutputs.getMyPluginsNames():
        exec "from MyPlugins." + plugin + " import pluginName, setupDirectory, pluginFiles, pluginDirectory"
        for pluginFile in pluginFiles:
            pluginFilePath = (setupDirectory + "/" + pluginFile).replace("HamsiManager", "OrganizasyonizM")
            if InputOutputs.isFile(pluginFilePath):
                InputOutputs.removeFile(pluginFilePath)
        if pluginDirectory!="":
            pluginDirectoryPath = (setupDirectory + "/" + pluginDirectory).replace("HamsiManager", "OrganizasyonizM")
            if InputOutputs.isDir(pluginDirectoryPath):
                InputOutputs.removeFileOrDir(pluginDirectoryPath, True)
    #Clear Setting Directory
    if InputOutputs.isDir(Universals.userDirectoryPath + "/.OrganizasyonizM"):
        isRemoveOldSettingDirectory = False
        if InputOutputs.isDirEmpty(Universals.userDirectoryPath + "/.OrganizasyonizM"):
            isRemoveOldSettingDirectory = True
        else:
            answer = Dialogs.ask(translate("HamsiManager", "The Old Version Was Detected"),
                    str(translate("HamsiManager", "OrganizasyonizM setting directory was detected.Are you want to delete \"%s\"?<br>Note:This directory will not be used anymore.You can delete this directory.")) % Organizer.getLink(Universals.userDirectoryPath + "/.OrganizasyonizM"), False, "OrganizasyonizM Setting Directory Was Detected")
            if answer==Dialogs.Yes:
                isRemoveOldSettingDirectory = True
        if isRemoveOldSettingDirectory:
            InputOutputs.removeFileOrDir(Universals.userDirectoryPath + "/.OrganizasyonizM", True)

def checkAndGetOldAppNameInSystem():
    import InputOutputs, Dialogs, Execute, Organizer, Universals
    from MyObjects import translate
    #Clear OrganizasyonizM in system(/usr/bin/OrganizasyonizM) by root
    if Execute.isRunningAsRoot():
        if InputOutputs.isFile("/usr/bin/OrganizasyonizM"):
            InputOutputs.removeFile("/usr/bin/OrganizasyonizM")
        if InputOutputs.isFile("/usr/bin/hamsimanager")==False:
            InputOutputs.createSymLink(Universals.executableHamsiManagerPath, "/usr/bin/hamsimanager")
    else:
        answer = Dialogs.ask(translate("HamsiManager", "The Old Version Was Detected"),
                    str(translate("HamsiManager", "Executable OrganizasyonizM file was detected in your system.Are you want to delete \"%s\" and creat new Executable Hamsi Manager(\"%s\")?")) % (Organizer.getLink("/usr/bin/OrganizasyonizM") , Organizer.getLink("/usr/bin/hamsimanager")), False, "Executable OrganizasyonizM Was Detected")
        if answer==Dialogs.Yes:
            Execute.executeHamsiManagerAsRoot("-checkAndGetOldAppNameInSystem")
    
