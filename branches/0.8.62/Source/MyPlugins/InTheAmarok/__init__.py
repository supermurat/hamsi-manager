# -*- coding: utf-8 -*-
import os
import Universals
import Settings
from MyObjects import translate
pluginName = str(translate("MyPlugins/InTheAmarok", "Hamsi Manager In The Amarok"))
pluginVersion = "0.3"
pluginFiles = []
pluginDirectory = "HamsiManagerInTheAmarok"
installThisPlugin = None
setupDirectory = Universals.getKDE4HomePath() + "share/apps/amarok/scripts"

def isInstallable():
    return Settings.isAvailablePyKDE4()
