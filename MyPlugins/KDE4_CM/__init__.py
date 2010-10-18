# -*- coding: utf-8 -*-
import os
import Variables
import Universals
import Settings, Execute
from MyObjects import translate
pluginName = str(translate("MyPlugins/KDE4_CM", "For KDE4 Applications` Context Menus"))
pluginVersion = "0.2"
pluginFiles = ["HamsiManager_KDE4_CM.desktop", 
               "HamsiManager_KDE4_CM_Dir.desktop", 
               "HamsiManager_KDE4_CM_File.desktop"]
pluginDirectory = ""
installThisPlugin = None
if Execute.isRunningAsRoot():
    setupDirectory = "/usr/share/kde4/services/ServiceMenus"
else:
    setupDirectory = Universals.getKDE4HomePath() + "/share/kde4/services/ServiceMenus"

def isInstallable():
    return Variables.isAvailablePyKDE4()