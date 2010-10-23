# -*- coding: utf-8 -*-

import Variables
from MyObjects import *
import Universals
import Dialogs
import Settings
import InputOutputs
import sys
import MyConfigure
import ReportBug

class MyPlugins(MDialog):
    global installPlugin
    
    def __init__(self, _parent):
        MDialog.__init__(self, _parent)
        if Universals.isActivePyKDE4==True:
            self.setButtons(MDialog.None)
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
        for plugin in Variables.getMyPluginsNames():
            exec "from " + plugin + " import pluginName , pluginVersion, isInstallable"
            if isInstallable():
                installedVersion = Settings.getUniversalSetting(pluginName.decode("utf-8"), "")
                if installedVersion == "":
                    details = translate("MyPlugins", "Could Not Be Determined")
                elif installedVersion != pluginVersion:
                    details = translate("MyPlugins", "Have A New Version")
                else:
                    details = translate("MyPlugins", "Installed")
                self.lstwPluginList.addItem(pluginName.decode("utf-8") + "\n\t" + details)
        if self.lstwPluginList.count()==0:
            self.lstwPluginList.addItem(translate("MyPlugins", "Could not find the appropriate plug-in to your system"))
            self.pbtnInstall.setEnabled(False)
    
    def installThis(self):
        try:
            installPlugin(Variables.getMyPluginsNames()[self.lstwPluginList.currentRow()])
            self.fillPlugins()
        except:
            error = ReportBug.ReportBug()
            error.show()
    
    def installPlugin(_pluginName, _isQuiet=False):
        isInstalled = False
        exec "from " + _pluginName + " import pluginName, pluginFiles, pluginDirectory, installThisPlugin, setupDirectory, pluginVersion"
        if installThisPlugin==None:
            if pluginDirectory=="":
                try:InputOutputs.makeDirs(setupDirectory)
                except:pass
                for pluginFile in pluginFiles:
                    InputOutputs.copyOrChange(Variables.HamsiManagerDirectory+"/MyPlugins/"+_pluginName+"/"+pluginFile, setupDirectory+"/"+pluginFile, "file", "only", True)
                    MyConfigure.reConfigureFile(setupDirectory+"/"+pluginFile, Variables.HamsiManagerDirectory)
                isInstalled = True
            else:
                newFileName = InputOutputs.copyOrChange(Variables.HamsiManagerDirectory+"/MyPlugins/"+_pluginName+"/"+pluginDirectory, setupDirectory+"/"+pluginDirectory, "directory", "only", True)
                if newFileName!=False:
                    isInstalled = True
        else:
            isInstalled = installThisPlugin()
        if isInstalled:
            Settings.setUniversalSetting(pluginName.decode("utf-8"), str(pluginVersion))
            if _isQuiet==False:
                Dialogs.show(translate("MyPlugins", "Plug-in Installation Is Complete"), 
                         str(translate("MyPlugins", "\"%s\" is installed on your system.")) % (pluginName))
        elif isInstalled=="AlreadyInstalled":
            if _isQuiet==False:
                Dialogs.show(translate("MyPlugins", "Plug-in Already Installed"), 
                         str(translate("MyPlugins", "\"%s\" already installed on your system.")) % (pluginName))
        else:
            if _isQuiet==False:
                Dialogs.showError(translate("MyPlugins", "Plug-in Installation Failed"), 
                         str(translate("MyPlugins", "\"%s\" failed to install on your system.")) % (pluginName))

 

class MyPluginsForSystem(MWidget):
    global installPlugin
    
    def __init__(self, _parent):
        MWidget.__init__(self, _parent)
        lblHeader = MLabel(u"<b>" + translate("MyPlugins", "My Plug-ins") + "</b>")
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
        for plugin in Variables.getMyPluginsNames():
            exec "from " + plugin + " import pluginName , pluginVersion, isInstallable"
            if isInstallable():
                installedVersion = Settings.getUniversalSetting(pluginName.decode("utf-8"), "")
                if installedVersion == "":
                    details = translate("MyPlugins", "Could Not Be Determined")
                elif installedVersion != pluginVersion:
                    details = translate("MyPlugins", "Have A New Version")
                else:
                    details = translate("MyPlugins", "Installed")
                self.lstwPluginList.addItem(pluginName.decode("utf-8") + "\n\t" + details)
        if self.lstwPluginList.count()==0:
            self.lstwPluginList.addItem(translate("MyPlugins", "Could not find the appropriate plug-in to your system"))
            self.pbtnInstall.setEnabled(False)
    
    def installThis(self):
        try:
            installPlugin(Variables.getMyPluginsNames()[self.lstwPluginList.currentRow()])
            self.fillPlugins()
        except:
            error = ReportBug.ReportBug()
            error.show()
    
    def installPlugin(_pluginName, _isQuiet=False):
        isInstalled = False
        exec "from " + _pluginName + " import pluginName, pluginFiles, pluginDirectory, installThisPlugin, setupDirectory, pluginVersion"
        if installThisPlugin==None:
            if pluginDirectory=="":
                try:InputOutputs.makeDirs(setupDirectory)
                except:pass
                for pluginFile in pluginFiles:
                    InputOutputs.copyOrChange(Variables.HamsiManagerDirectory+"/MyPlugins/"+_pluginName+"/"+pluginFile, setupDirectory+"/"+pluginFile, "file", "only", True)
                    MyConfigure.reConfigureFile(setupDirectory+"/"+pluginFile, Variables.HamsiManagerDirectory)
                isInstalled = True
            else:
                newFileName = InputOutputs.copyOrChange(Variables.HamsiManagerDirectory+"/MyPlugins/"+_pluginName+"/"+pluginDirectory, setupDirectory+"/"+pluginDirectory, "directory", "only", True)
                if newFileName!=False:
                    isInstalled = True
        else:
            isInstalled = installThisPlugin()
        if isInstalled:
            Settings.setUniversalSetting(pluginName.decode("utf-8"), str(pluginVersion))
            if _isQuiet==False:
                Dialogs.show(translate("MyPlugins", "Plug-in Installation Is Complete"), 
                         str(translate("MyPlugins", "\"%s\" is installed on your system.")) % (pluginName))
        elif isInstalled=="AlreadyInstalled":
            if _isQuiet==False:
                Dialogs.show(translate("MyPlugins", "Plug-in Already Installed"), 
                         str(translate("MyPlugins", "\"%s\" already installed on your system.")) % (pluginName))
        else:
            if _isQuiet==False:
                Dialogs.showError(translate("MyPlugins", "Plug-in Installation Failed"), 
                         str(translate("MyPlugins", "\"%s\" failed to install on your system.")) % (pluginName))

 
