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


from Core import Variables
from Core.MyObjects import *
from Core import Universals
from Core import Dialogs
from Core import Settings
import InputOutputs
import sys
from Core import MyConfigure
from Core import ReportBug

class MyPlugins(MDialog):
    global installPlugin
    
    def __init__(self, _parent):
        MDialog.__init__(self, _parent)
        if Universals.isActivePyKDE4==True:
            self.setButtons(MDialog.NoDefault)
        self.lstwPluginList = MListWidget()
        self.pbtnInstall = MPushButton(translate("MyPlugins", "Install The Selected Plug-in"))
        pbtnClose = MPushButton(translate("MyPlugins", "Close"))
        self.fillPlugins()
        self.connect(self.pbtnInstall,SIGNAL("clicked()"),self.installThis)
        self.connect(pbtnClose,SIGNAL("clicked()"),self.close)
        pnlMain = MWidget(self)
        vblMain = MVBoxLayout(pnlMain)
        HBox1 = MHBoxLayout()
        HBox1.addWidget(self.pbtnInstall)
        HBox1.addWidget(pbtnClose)
        vblMain.addWidget(self.lstwPluginList)
        vblMain.addStretch(1)
        vblMain.addLayout(HBox1)
        if Universals.isActivePyKDE4==True:
            self.setMainWidget(pnlMain)
        else:
            self.setLayout(vblMain)
        self.setWindowTitle(translate("MyPlugins", "My Plug-ins"))
        self.show()
    
    def fillPlugins(self):
        self.lstwPluginList.clear()
        self.myPluginsNames = Variables.getMyPluginsNames()
        for plugin in self.myPluginsNames:
            pluginModule = __import__("MyPlugins." + plugin, globals(), locals(), ["pluginName", "pluginVersion", "isInstallable"], -1)
            if pluginModule.isInstallable():
                installedVersion = Settings.getUniversalSetting(trForM(pluginModule.pluginName), "")
                if installedVersion == "":
                    details = translate("MyPlugins", "Could Not Be Determined")
                elif installedVersion != pluginModule.pluginVersion:
                    details = translate("MyPlugins", "Have A New Version")
                else:
                    details = translate("MyPlugins", "Installed")
                self.lstwPluginList.addItem(trForUI(pluginModule.pluginName) + "\n\t" + details)
        if self.lstwPluginList.count()==0:
            self.lstwPluginList.addItem(translate("MyPlugins", "Could not find the appropriate plug-in to your system"))
            self.pbtnInstall.setEnabled(False)
    
    def installThis(self):
        try:
            installPlugin(self.myPluginsNames[self.lstwPluginList.currentRow()])
            self.fillPlugins()
        except:
            error = ReportBug.ReportBug()
            error.show()
    
    def installPlugin(_pluginName, _isQuiet=False):
        isInstalled = False
        pluginModule = __import__("MyPlugins." + _pluginName, globals(), locals(), ["pluginName", "pluginFiles", "pluginDirectory", "installThisPlugin", "setupDirectory", "pluginVersion"], -1)
        if installThisPlugin==None:
            if pluginModule.pluginDirectory=="":
                try:InputOutputs.makeDirs(pluginModule.setupDirectory)
                except:pass
                for pluginFile in pluginModule.pluginFiles:
                    InputOutputs.copyOrChange(Variables.HamsiManagerDirectory+"/MyPlugins/"+_pluginName+"/"+pluginFile, pluginModule.setupDirectory+"/"+pluginFile, "file", "only", True)
                    MyConfigure.reConfigureFile(pluginModule.setupDirectory+"/"+pluginFile, Variables.HamsiManagerDirectory)
                isInstalled = True
            else:
                oldFilePath = Variables.HamsiManagerDirectory+"/MyPlugins/"+_pluginName+"/"+pluginModule.pluginDirectory
                newFilePath = InputOutputs.copyOrChange(oldFilePath, pluginModule.setupDirectory+"/"+pluginModule.pluginDirectory, "directory", "only", True)
                if newFilePath!=oldFilePath:
                    isInstalled = True
        else:
            isInstalled = pluginModule.installThisPlugin()
        if isInstalled:
            Settings.setUniversalSetting(trForM(pluginModule.pluginName), str(pluginModule.pluginVersion))
            if _isQuiet==False:
                Dialogs.show(translate("MyPlugins", "Plug-in Installation Is Complete"), 
                         str(translate("MyPlugins", "\"%s\" is installed on your system.")) % (pluginModule.pluginName))
        elif isInstalled=="AlreadyInstalled":
            if _isQuiet==False:
                Dialogs.show(translate("MyPlugins", "Plug-in Already Installed"), 
                         str(translate("MyPlugins", "\"%s\" already installed on your system.")) % (pluginModule.pluginName))
        else:
            if _isQuiet==False:
                Dialogs.showError(translate("MyPlugins", "Plug-in Installation Failed"), 
                         str(translate("MyPlugins", "\"%s\" failed to install on your system.")) % (pluginModule.pluginName))

 

class MyPluginsForSystem(MWidget):
    global installPlugin
    
    def __init__(self, _parent):
        MWidget.__init__(self, _parent)
        lblHeader = MLabel(trForUI("<b>" + translate("MyPlugins", "My Plug-ins") + "</b>"))
        lblNote = MLabel(translate("MyPlugins", "You can manage plugins in your system"))
        self.lstwPluginList = MListWidget()
        self.pbtnInstall = MPushButton(translate("MyPlugins", "Install The Selected Plug-in"))
        self.fillPlugins()
        self.connect(self.pbtnInstall,SIGNAL("clicked()"),self.installThis)
        pnlMain = MWidget(self)
        vblMain = MVBoxLayout(pnlMain)
        HBox1 = MHBoxLayout()
        HBox1.addStretch(10)
        HBox1.addWidget(self.pbtnInstall)
        vblMain.addWidget(lblHeader)
        vblMain.addWidget(lblNote)
        vblMain.addWidget(self.lstwPluginList)
        vblMain.addStretch(1)
        vblMain.addLayout(HBox1)
        self.setLayout(vblMain)
    
    def fillPlugins(self):
        self.lstwPluginList.clear()
        self.myPluginsNames = Variables.getMyPluginsNames()
        for plugin in self.myPluginsNames:
            pluginModule = __import__("MyPlugins." + plugin, globals(), locals(), ["pluginName", "pluginVersion", "isInstallable"], -1)
            if pluginModule.isInstallable():
                installedVersion = Settings.getUniversalSetting(trForM(pluginModule.pluginName), "")
                if installedVersion == "":
                    details = translate("MyPlugins", "Could Not Be Determined")
                elif installedVersion != pluginModule.pluginVersion:
                    details = translate("MyPlugins", "Have A New Version")
                else:
                    details = translate("MyPlugins", "Installed")
                self.lstwPluginList.addItem(trForUI(pluginModule.pluginName) + "\n\t" + details)
        if self.lstwPluginList.count()==0:
            self.lstwPluginList.addItem(translate("MyPlugins", "Could not find the appropriate plug-in to your system"))
            self.pbtnInstall.setEnabled(False)
    
    def installThis(self):
        try:
            installPlugin(self.myPluginsNames[self.lstwPluginList.currentRow()])
            self.fillPlugins()
        except:
            error = ReportBug.ReportBug()
            error.show()
    
    def installPlugin(_pluginName, _isQuiet=False):
        isInstalled = False
        pluginModule = __import__("MyPlugins." + _pluginName, globals(), locals(), ["pluginName", "pluginFiles", "pluginDirectory", "installThisPlugin", "setupDirectory", "pluginVersion"], -1)
        if pluginModule.installThisPlugin==None:
            if pluginModule.pluginDirectory=="":
                try:InputOutputs.makeDirs(pluginModule.setupDirectory)
                except:pass
                for pluginFile in pluginModule.pluginFiles:
                    InputOutputs.copyOrChange(Variables.HamsiManagerDirectory+"/MyPlugins/"+_pluginName+"/"+pluginFile, pluginModule.setupDirectory+"/"+pluginFile, "file", "only", True)
                    MyConfigure.reConfigureFile(pluginModule.setupDirectory+"/"+pluginFile, Variables.HamsiManagerDirectory)
                isInstalled = True
            else:
                oldFilePath = Variables.HamsiManagerDirectory+"/MyPlugins/"+_pluginName+"/"+pluginModule.pluginDirectory
                newFilePath = InputOutputs.copyOrChange(oldFilePath, pluginModule.setupDirectory+"/"+pluginModule.pluginDirectory, "directory", "only", True)
                if newFilePath!=oldFilePath:
                    isInstalled = True
        else:
            isInstalled = pluginModule.installThisPlugin()
        if isInstalled:
            Settings.setUniversalSetting(trForM(pluginModule.pluginName), str(pluginModule.pluginVersion))
            if _isQuiet==False:
                Dialogs.show(translate("MyPlugins", "Plug-in Installation Is Complete"), 
                         str(translate("MyPlugins", "\"%s\" is installed on your system.")) % (pluginModule.pluginName))
        elif isInstalled=="AlreadyInstalled":
            if _isQuiet==False:
                Dialogs.show(translate("MyPlugins", "Plug-in Already Installed"), 
                         str(translate("MyPlugins", "\"%s\" already installed on your system.")) % (pluginModule.pluginName))
        else:
            if _isQuiet==False:
                Dialogs.showError(translate("MyPlugins", "Plug-in Installation Failed"), 
                         str(translate("MyPlugins", "\"%s\" failed to install on your system.")) % (pluginModule.pluginName))

 
