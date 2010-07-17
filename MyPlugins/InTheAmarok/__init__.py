# -*- coding: utf-8 -*-
import os
import Universals
import Settings, Execute
from MyObjects import translate
pluginName = str(translate("MyPlugins/InTheAmarok", "Hamsi Manager In The Amarok"))
pluginVersion = "0.4"
pluginFiles = []
pluginDirectory = "HamsiManagerInTheAmarok"
installThisPlugin = None
if Execute.isRunningAsRoot():
    setupDirectory = "/usr/share/apps/amarok/scripts"
else:
    setupDirectory = Universals.getKDE4HomePath() + "share/apps/amarok/scripts"

def isInstallable():
    return Settings.isAvailablePyKDE4()
