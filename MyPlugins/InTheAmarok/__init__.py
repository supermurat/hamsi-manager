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

from Core.MyObjects import *
from Core import Variables
pluginName = str(translate("MyPlugins/InTheAmarok", "Hamsi Manager In The Amarok"))
pluginVersion = "0.4"
pluginFiles = []
pluginDirectory = "HamsiManagerInTheAmarok"
installThisPlugin = None
uninstallThisPlugin = None

if Variables.isRunningAsRoot():
    setupDirectory = "/usr/share/apps/amarok/scripts"
else:
    setupDirectory = Variables.getKDE4HomePath() + "/share/apps/amarok/scripts"

def isInstallable():
    return Variables.isAvailableKDE4()
