# This file is part of HamsiManager.
#
# Copyright (c) 2010 - 2014 Murat Demir <mopened@gmail.com>
#
# Hamsi Manager is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Hamsi Manager is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with HamsiManager; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA


from Core.MyObjects import *
from Core import Universals as uni
from Core import Dialogs
from Core import Settings
import FileUtils as fu
import sys
from Core import MyConfigure
from Core import ReportBug

MyDialog, MyDialogType, MyParent = getMyDialog()


class MyPlugins(MyDialog):
    def __init__(self):
        MyDialog.__init__(self, MyParent)
        if MyDialogType == "MDialog":
            if isActivePyKDE4:
                self.setButtons(MyDialog.NoDefault)
        elif MyDialogType == "MMainWindow":
            self.setObjectName("Searcher")
            setMainWindow(self)
        self.lstwPluginList = MListWidget()
        self.pbtnInstall = MPushButton(translate("MyPlugins", "Install The Selected Plug-in"))
        self.pbtnUninstall = MPushButton(translate("MyPlugins", "Uninstall The Selected Plug-in"))
        pbtnClose = MPushButton(translate("MyPlugins", "Close"))
        self.fillPlugins()
        self.connect(self.pbtnInstall, SIGNAL("clicked()"), self.installThis)
        self.connect(self.pbtnUninstall, SIGNAL("clicked()"), self.uninstallThis)
        self.connect(pbtnClose, SIGNAL("clicked()"), self.close)
        pnlMain = MWidget(self)
        vblMain = MVBoxLayout(pnlMain)
        HBox1 = MHBoxLayout()
        HBox1.addWidget(self.pbtnInstall)
        HBox1.addWidget(self.pbtnUninstall)
        HBox1.addWidget(pbtnClose)
        vblMain.addWidget(self.lstwPluginList)
        vblMain.addStretch(1)
        vblMain.addLayout(HBox1)
        if MyDialogType == "MDialog":
            if isActivePyKDE4:
                self.setMainWidget(pnlMain)
            else:
                self.setLayout(vblMain)
        elif MyDialogType == "MMainWindow":
            self.setCentralWidget(pnlMain)
            moveToCenter(self)
        self.setWindowTitle(translate("MyPlugins", "My Plugins"))
        self.setWindowIcon(MIcon("Images:hamsi.png"))
        self.show()

    def closeEvent(self, _event):
        MApplication.setQuitOnLastWindowClosed(True)

    def fillPlugins(self):
        self.lstwPluginList.clear()
        self.myPluginsNames = []
        for plugin in uni.getMyPluginsNames():
            pluginModule = __import__("MyPlugins." + plugin, globals(), locals(),
                                      ["pluginName", "pluginVersion", "isInstallable"], 0)
            if pluginModule.isInstallable():
                installedVersion = Settings.getUniversalSetting(str(pluginModule.pluginName), "")
                if installedVersion == "":
                    details = translate("MyPlugins", "Could Not Be Determined")
                elif installedVersion != pluginModule.pluginVersion:
                    details = translate("MyPlugins", "Have A New Version")
                else:
                    details = translate("MyPlugins", "Installed")
                self.lstwPluginList.addItem(str(pluginModule.pluginName) + "\n\t" + details)
                self.myPluginsNames.append(plugin)
        if self.lstwPluginList.count() == 0:
            self.lstwPluginList.addItem(translate("MyPlugins", "Could not find the appropriate plug-in to your system"))
            self.pbtnInstall.setEnabled(False)

    def installThis(self):
        try:
            self.installPlugin(self.myPluginsNames[self.lstwPluginList.currentRow()])
            self.fillPlugins()
        except:
            ReportBug.ReportBug()

    def uninstallThis(self):
        try:
            self.uninstallPlugin(self.myPluginsNames[self.lstwPluginList.currentRow()])
            self.fillPlugins()
        except:
            ReportBug.ReportBug()

    def installPlugin(self, _pluginName, _isQuiet=False):
        isInstalled = False
        pluginModule = __import__("MyPlugins." + _pluginName, globals(), locals(),
                                  ["pluginName", "pluginFiles", "pluginDirectory", "installThisPlugin",
                                   "setupDirectory", "pluginVersion"], 0)
        if pluginModule.installThisPlugin is None:
            if pluginModule.pluginDirectory == "":
                try: fu.makeDirs(pluginModule.setupDirectory)
                except: pass
                for pluginFile in pluginModule.pluginFiles:
                    fu.copyOrChange(fu.joinPath(fu.HamsiManagerDirectory, "MyPlugins", _pluginName, pluginFile),
                                    fu.joinPath(pluginModule.setupDirectory, pluginFile), "file", "only", True)
                    MyConfigure.reConfigureFile(fu.joinPath(pluginModule.setupDirectory, pluginFile))
                isInstalled = True
            else:
                oldFilePath = fu.joinPath(fu.HamsiManagerDirectory, "MyPlugins", _pluginName,
                                          pluginModule.pluginDirectory)
                newFilePath = fu.copyOrChange(oldFilePath,
                                              fu.joinPath(pluginModule.setupDirectory, pluginModule.pluginDirectory),
                                              "directory", "only", True)
                if newFilePath != oldFilePath:
                    isInstalled = True
        else:
            isInstalled = pluginModule.installThisPlugin()
        if isInstalled:
            Settings.setUniversalSetting(str(pluginModule.pluginName), str(pluginModule.pluginVersion))
            if _isQuiet is False:
                Dialogs.show(translate("MyPlugins", "Plug-in Installation Is Complete"),
                             str(translate("MyPlugins", "\"%s\" is installed on your system.")) % (
                                 pluginModule.pluginName))
        elif isInstalled == "AlreadyInstalled":
            if _isQuiet is False:
                Dialogs.show(translate("MyPlugins", "Plug-in Already Installed"),
                             str(translate("MyPlugins", "\"%s\" already installed on your system.")) % (
                                 pluginModule.pluginName))
        else:
            if _isQuiet is False:
                Dialogs.showError(translate("MyPlugins", "Plug-in Installation Failed"),
                                  str(translate("MyPlugins", "\"%s\" failed to install on your system.")) % (
                                      pluginModule.pluginName))

    def uninstallPlugin(self, _pluginName, _isQuiet=False):
        isUninstalled = False
        pluginModule = __import__("MyPlugins." + _pluginName, globals(), locals(),
                                  ["pluginName", "pluginFiles", "pluginDirectory", "uninstallThisPlugin",
                                   "setupDirectory", "pluginVersion"], 0)
        if pluginModule.uninstallThisPlugin is None:
            if pluginModule.pluginDirectory == "":
                for pluginFile in pluginModule.pluginFiles:
                    if fu.isFile(fu.joinPath(pluginModule.setupDirectory, pluginFile)):
                        fu.removeFileOrDir(fu.joinPath(pluginModule.setupDirectory, pluginFile))
                isUninstalled = True
            else:
                if fu.isDir(fu.joinPath(pluginModule.setupDirectory, pluginModule.pluginDirectory)):
                    fu.removeFileOrDir(fu.joinPath(pluginModule.setupDirectory, pluginModule.pluginDirectory))
                isUninstalled = True
        else:
            isUninstalled = pluginModule.uninstallThisPlugin()
        if isUninstalled:
            Settings.setUniversalSetting(str(pluginModule.pluginName), str(""))
            if _isQuiet is False:
                Dialogs.show(translate("MyPlugins", "Plug-in Uninstallation Is Complete"),
                             str(translate("MyPlugins", "\"%s\" is uninstalled on your system.")) % (
                                 pluginModule.pluginName))
        elif isUninstalled == "AlreadyUninstalled":
            if _isQuiet is False:
                Dialogs.show(translate("MyPlugins", "Plug-in Already Uninstalled"),
                             str(translate("MyPlugins", "\"%s\" already uninstalled on your system.")) % (
                                 pluginModule.pluginName))
        else:
            if _isQuiet is False:
                Dialogs.showError(translate("MyPlugins", "Plug-in Uninstallation Failed"),
                                  str(translate("MyPlugins", "\"%s\" failed to uninstall on your system.")) % (
                                      pluginModule.pluginName))


class MyPluginsForSystem(MWidget):
    def __init__(self, _parent, _actions=""):
        MWidget.__init__(self, _parent)
        self.pbtnInstall = None
        self.pbtnUninstall = None
        lblHeader = MLabel(str("<b>" + translate("MyPlugins", "My Plugins") + "</b>"))
        lblNote = MLabel(translate("MyPlugins", "You can manage plugins in your system"))
        self.lstwPluginList = MListWidget()
        self.fillPlugins()
        pnlMain = MWidget(self)
        vblMain = MVBoxLayout(pnlMain)
        HBox1 = MHBoxLayout()
        HBox1.addStretch(10)
        if _actions == "install" or _actions == "":
            self.pbtnInstall = MPushButton(translate("MyPlugins", "Install The Selected Plug-in"))
            self.connect(self.pbtnInstall, SIGNAL("clicked()"), self.installThis)
            HBox1.addWidget(self.pbtnInstall)
        if _actions == "uninstall" or _actions == "":
            self.pbtnUninstall = MPushButton(translate("MyPlugins", "Uninstall The Selected Plug-in"))
            self.connect(self.pbtnUninstall, SIGNAL("clicked()"), self.uninstallThis)
            HBox1.addWidget(self.pbtnUninstall)
        vblMain.addWidget(lblHeader)
        vblMain.addWidget(lblNote)
        vblMain.addWidget(self.lstwPluginList)
        vblMain.addStretch(1)
        vblMain.addLayout(HBox1)
        self.setLayout(vblMain)

    def fillPlugins(self):
        self.lstwPluginList.clear()
        self.myPluginsNames = []
        for plugin in uni.getMyPluginsNames():
            pluginModule = __import__("MyPlugins." + plugin, globals(), locals(),
                                      ["pluginName", "pluginVersion", "isInstallable"], 0)
            if pluginModule.isInstallable():
                installedVersion = Settings.getUniversalSetting(str(pluginModule.pluginName), "")
                if installedVersion == "":
                    details = translate("MyPlugins", "Could Not Be Determined")
                elif installedVersion != pluginModule.pluginVersion:
                    details = translate("MyPlugins", "Have A New Version")
                else:
                    details = translate("MyPlugins", "Installed")
                self.lstwPluginList.addItem(str(pluginModule.pluginName) + "\n\t" + details)
                self.myPluginsNames.append(plugin)
        if self.lstwPluginList.count() == 0:
            self.lstwPluginList.addItem(translate("MyPlugins", "Could not find the appropriate plug-in to your system"))
            if self.pbtnInstall is not None:
                self.pbtnInstall.setEnabled(False)
            if self.pbtnUninstall is not None:
                self.pbtnUninstall.setEnabled(False)

    def installThis(self):
        try:
            self.installPlugin(self.myPluginsNames[self.lstwPluginList.currentRow()])
            self.fillPlugins()
        except:
            ReportBug.ReportBug()

    def uninstallThis(self):
        try:
            self.uninstallPlugin(self.myPluginsNames[self.lstwPluginList.currentRow()])
            self.fillPlugins()
        except:
            ReportBug.ReportBug()

    def installPlugin(self, _pluginName, _isQuiet=False):
        isInstalled = False
        pluginModule = __import__("MyPlugins." + _pluginName, globals(), locals(),
                                  ["pluginName", "pluginFiles", "pluginDirectory", "installThisPlugin",
                                   "setupDirectory", "pluginVersion"], 0)
        if pluginModule.installThisPlugin is None:
            if pluginModule.pluginDirectory == "":
                try: fu.makeDirs(pluginModule.setupDirectory)
                except: pass
                for pluginFile in pluginModule.pluginFiles:
                    fu.copyOrChange(fu.joinPath(fu.HamsiManagerDirectory, "MyPlugins", _pluginName, pluginFile),
                                    fu.joinPath(pluginModule.setupDirectory, pluginFile), "file", "only", True)
                    MyConfigure.reConfigureFile(fu.joinPath(pluginModule.setupDirectory, pluginFile))
                isInstalled = True
            else:
                oldFilePath = fu.joinPath(fu.HamsiManagerDirectory, "MyPlugins", _pluginName,
                                          pluginModule.pluginDirectory)
                newFilePath = fu.copyOrChange(oldFilePath,
                                              fu.joinPath(pluginModule.setupDirectory, pluginModule.pluginDirectory),
                                              "directory", "only", True)
                if newFilePath != oldFilePath:
                    isInstalled = True
        else:
            isInstalled = pluginModule.installThisPlugin()
        if isInstalled:
            Settings.setUniversalSetting(str(pluginModule.pluginName), str(pluginModule.pluginVersion))
            if _isQuiet is False:
                Dialogs.show(translate("MyPlugins", "Plug-in Installation Is Complete"),
                             str(translate("MyPlugins", "\"%s\" is installed on your system.")) % (
                                 pluginModule.pluginName))
        elif isInstalled == "AlreadyInstalled":
            if _isQuiet is False:
                Dialogs.show(translate("MyPlugins", "Plug-in Already Installed"),
                             str(translate("MyPlugins", "\"%s\" already installed on your system.")) % (
                                 pluginModule.pluginName))
        else:
            if _isQuiet is False:
                Dialogs.showError(translate("MyPlugins", "Plug-in Installation Failed"),
                                  str(translate("MyPlugins", "\"%s\" failed to install on your system.")) % (
                                      pluginModule.pluginName))

    def uninstallPlugin(self, _pluginName, _isQuiet=False):
        isUninstalled = False
        pluginModule = __import__("MyPlugins." + _pluginName, globals(), locals(),
                                  ["pluginName", "pluginFiles", "pluginDirectory", "uninstallThisPlugin",
                                   "setupDirectory", "pluginVersion"], 0)
        if pluginModule.uninstallThisPlugin is None:
            if pluginModule.pluginDirectory == "":
                for pluginFile in pluginModule.pluginFiles:
                    if fu.isFile(fu.joinPath(pluginModule.setupDirectory, pluginFile)):
                        fu.removeFileOrDir(fu.joinPath(pluginModule.setupDirectory, pluginFile))
                isUninstalled = True
            else:
                if fu.isDir(fu.joinPath(pluginModule.setupDirectory, pluginModule.pluginDirectory)):
                    fu.removeFileOrDir(fu.joinPath(pluginModule.setupDirectory, pluginModule.pluginDirectory))
                isUninstalled = True
        else:
            isUninstalled = pluginModule.uninstallThisPlugin()
        if isUninstalled:
            Settings.setUniversalSetting(str(pluginModule.pluginName), str(""))
            if _isQuiet is False:
                Dialogs.show(translate("MyPlugins", "Plug-in Uninstallation Is Complete"),
                             str(translate("MyPlugins", "\"%s\" is uninstalled on your system.")) % (
                                 pluginModule.pluginName))
        elif isUninstalled == "AlreadyUninstalled":
            if _isQuiet is False:
                Dialogs.show(translate("MyPlugins", "Plug-in Already Uninstalled"),
                             str(translate("MyPlugins", "\"%s\" already uninstalled on your system.")) % (
                                 pluginModule.pluginName))
        else:
            if _isQuiet is False:
                Dialogs.showError(translate("MyPlugins", "Plug-in Uninstallation Failed"),
                                  str(translate("MyPlugins", "\"%s\" failed to uninstall on your system.")) % (
                                      pluginModule.pluginName))
                         
                         
    
