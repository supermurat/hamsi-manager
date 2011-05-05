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

import Variables
import Execute
from MyObjects import translate
pluginName = str(translate("MyPlugins/KDE4_SM", "For KDE4 Applications` Service Menus"))
pluginVersion = "0.4"
pluginFiles = ["HamsiManager_KDE4_SM.desktop", 
               "HamsiManager_KDE4_SM_Dir.desktop", 
               "HamsiManager_KDE4_SM_File.desktop"]
pluginDirectory = ""
installThisPlugin = None
if Variables.isRunningAsRoot():
    setupDirectory = "/usr/share/kde4/services/ServiceMenus"
else:
    setupDirectory = Variables.getKDE4HomePath() + "/share/kde4/services/ServiceMenus"

def isInstallable():
    return Variables.isAvailableKDE4()
