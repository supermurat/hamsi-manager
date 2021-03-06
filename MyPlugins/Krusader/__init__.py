# This file is part of HamsiManager.
#
# Copyright (c) 2010 - 2015 Murat Demir <mopened@gmail.com>
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
import FileUtils as fu

pluginName = str(translate("MyPlugins/Krusader", "Krusader`s User Actions Menu"))
pluginVersion = "0.6"
pluginFiles = []
pluginDirectory = ""
setupDirectory = ""


def isInstallable():
    return uni.isAvailableKDE4()


def installThisPlugin():
    from Core import Execute

    executeCommandOfHamsiManager = Execute.getExecuteCommandOfHamsiManager()
    iconPath = fu.joinPath(fu.themePath, "Images", "hamsi.png")
    myPluginStrings = [(" <action name=\"hamsimanager_Organize\" >\n" +
                        "  <title>" + str(
        translate("MyPlugins/Krusader", "Organize With Hamsi Manager")) + "</title>\n" +
                        "  <tooltip>" + str(
        translate("MyPlugins/Krusader", "You can organize with Hamsi Manager")) + "</tooltip>\n" +
                        "  <icon>" + iconPath + "</icon>\n" +
                        "  <category>Hamsi Manager</category>\n" +
                        "  <description>" + str(translate("MyPlugins/Krusader",
                                                          "You can continue to edit the folder you select with Hamsi Manager")) + ".</description>\n" +
                        "  <command>" + executeCommandOfHamsiManager + " -t 1 --directory %aCurrent%</command>\n" +
                        "  <defaultshortcut>Ctrl+O</defaultshortcut>\n" +
                        " </action>\n"),
                       (" <action name=\"hamsimanager_emendDirectory\" >\n" +
                        "  <title>" + str(translate("MyPlugins/Krusader", "Auto Emend Directory")) + "</title>\n" +
                        "  <tooltip>" + str(
                           translate("MyPlugins/Krusader", "Auto emend with Hamsi Manager")) + "</tooltip>\n" +
                        "  <icon>" + fu.joinPath(fu.themePath, "Images", "emendDirectory.png") + "</icon>\n" +
                        "  <category>Hamsi Manager</category>\n" +
                        "  <description>" + str(
                           translate("MyPlugins/Krusader", "Auto emend with Hamsi Manager")) + ".</description>\n" +
                        "  <command>" + executeCommandOfHamsiManager + " --qm --emendDirectory %aCurrent%</command>\n" +
                        "  <defaultshortcut></defaultshortcut>\n" +
                        " </action>\n"),
                       (" <action name=\"hamsimanager_emendDirectoryWithContents\" >\n" +
                        "  <title>" + str(
                           translate("MyPlugins/Krusader", "Auto Emend Directory (With Contents)")) + "</title>\n" +
                        "  <tooltip>" + str(translate("MyPlugins/Krusader",
                                                      "Auto emend with Hamsi Manager (With Contents)")) + "</tooltip>\n" +
                        "  <icon>" + fu.joinPath(fu.themePath, "Images",
                                                 "emendDirectoryWithContents.png") + "</icon>\n" +
                        "  <category>Hamsi Manager</category>\n" +
                        "  <description>" + str(translate("MyPlugins/Krusader",
                                                          "Auto emend with Hamsi Manager (With Contents)")) + ".</description>\n" +
                        "  <command>" + executeCommandOfHamsiManager + " --qm --emendDirectoryWithContents %aCurrent%</command>\n" +
                        "  <defaultshortcut></defaultshortcut>\n" +
                        " </action>\n"),
                       (" <action name=\"hamsimanager_emendFile\" >\n" +
                        "  <title>" + str(translate("MyPlugins/Krusader", "Auto Emend File")) + "</title>\n" +
                        "  <tooltip>" + str(
                           translate("MyPlugins/Krusader", "Auto emend with Hamsi Manager")) + "</tooltip>\n" +
                        "  <icon>" + fu.joinPath(fu.themePath, "Images", "emendFile.png") + "</icon>\n" +
                        "  <category>Hamsi Manager</category>\n" +
                        "  <description>" + str(
                           translate("MyPlugins/Krusader", "Auto emend with Hamsi Manager")) + ".</description>\n" +
                        "  <command>" + executeCommandOfHamsiManager + " --qm --emendFile %aCurrent%</command>\n" +
                        "  <defaultshortcut></defaultshortcut>\n" +
                        " </action>\n"),
                       (" <action name=\"hamsimanager_pack\" >\n" +
                        "  <title>" + str(translate("MyPlugins/Krusader", "Pack It")) + "</title>\n" +
                        "  <tooltip>" + str(
                           translate("MyPlugins/Krusader", "Pack it with Hamsi Manager")) + "</tooltip>\n" +
                        "  <icon>" + fu.joinPath(fu.themePath, "Images", "pack.png") + "</icon>\n" +
                        "  <category>Hamsi Manager</category>\n" +
                        "  <description>" + str(
                           translate("MyPlugins/Krusader", "Pack it with Hamsi Manager")) + ".</description>\n" +
                        "  <command>" + executeCommandOfHamsiManager + " --qm --pack %aCurrent%</command>\n" +
                        "  <defaultshortcut></defaultshortcut>\n" +
                        " </action>\n"),
                       (" <action name=\"hamsimanager_checkIcon\" >\n" +
                        "  <title>" + str(translate("MyPlugins/Krusader", "Check Directory Icon")) + "</title>\n" +
                        "  <tooltip>" + str(translate("MyPlugins/Krusader",
                                                      "Check directory icon with Hamsi Manager")) + "</tooltip>\n" +
                        "  <icon>" + fu.joinPath(fu.themePath, "Images", "checkIcon.png") + "</icon>\n" +
                        "  <category>Hamsi Manager</category>\n" +
                        "  <description>" + str(translate("MyPlugins/Krusader",
                                                          "Check directory icon with Hamsi Manager")) + ".</description>\n" +
                        "  <command>" + executeCommandOfHamsiManager + " --qm --checkIcon %aCurrent%</command>\n" +
                        "  <defaultshortcut></defaultshortcut>\n" +
                        " </action>\n"),
                       (" <action name=\"hamsimanager_clearEmptyDirectories\" >\n" +
                        "  <title>" + str(translate("MyPlugins/Krusader", "Clear Empty Directories")) + "</title>\n" +
                        "  <tooltip>" + str(translate("MyPlugins/Krusader",
                                                      "Clear empty directories with Hamsi Manager")) + "</tooltip>\n" +
                        "  <icon>" + fu.joinPath(fu.themePath, "Images", "clearEmptyDirectories.png") + "</icon>\n" +
                        "  <category>Hamsi Manager</category>\n" +
                        "  <description>" + str(translate("MyPlugins/Krusader",
                                                          "Clear empty directories with Hamsi Manager")) + ".</description>\n" +
                        "  <command>" + executeCommandOfHamsiManager + " --qm --clearEmptyDirectories %aCurrent%</command>\n" +
                        "  <defaultshortcut></defaultshortcut>\n" +
                        " </action>\n"),
                       (" <action name=\"hamsimanager_clearUnneededs\" >\n" +
                        "  <title>" + str(translate("MyPlugins/Krusader", "Clear Unneededs")) + "</title>\n" +
                        "  <tooltip>" + str(
                           translate("MyPlugins/Krusader", "Clear unneededs with Hamsi Manager")) + "</tooltip>\n" +
                        "  <icon>" + fu.joinPath(fu.themePath, "Images", "clearUnneededs.png") + "</icon>\n" +
                        "  <category>Hamsi Manager</category>\n" +
                        "  <description>" + str(translate("MyPlugins/Krusader",
                                                          "Clear unneededs with Hamsi Manager")) + ".</description>\n" +
                        "  <command>" + executeCommandOfHamsiManager + " --qm --clearUnneededs %aCurrent%</command>\n" +
                        "  <defaultshortcut></defaultshortcut>\n" +
                        " </action>\n"),
                       (" <action name=\"hamsimanager_clearIgnoreds\" >\n" +
                        "  <title>" + str(translate("MyPlugins/Krusader", "Clear Ignoreds")) + "</title>\n" +
                        "  <tooltip>" + str(
                           translate("MyPlugins/Krusader", "Clear ignoreds with Hamsi Manager")) + "</tooltip>\n" +
                        "  <icon>" + fu.joinPath(fu.themePath, "Images", "clearIgnoreds.png") + "</icon>\n" +
                        "  <category>Hamsi Manager</category>\n" +
                        "  <description>" + str(
                           translate("MyPlugins/Krusader", "Clear ignoreds with Hamsi Manager")) + ".</description>\n" +
                        "  <command>" + executeCommandOfHamsiManager + " --qm --clearIgnoreds %aCurrent%</command>\n" +
                        "  <defaultshortcut></defaultshortcut>\n" +
                        " </action>\n"),
                       (" <action name=\"hamsimanager_copyPath\" >\n" +
                        "  <title>" + str(translate("MyPlugins/Krusader", "Copy Path To Clipboard")) + "</title>\n" +
                        "  <tooltip>" + str(translate("MyPlugins/Krusader",
                                                      "Copy path to clipboard with Hamsi Manager")) + "</tooltip>\n" +
                        "  <icon>" + fu.joinPath(fu.themePath, "Images", "copyPath.png") + "</icon>\n" +
                        "  <category>Hamsi Manager</category>\n" +
                        "  <description>" + str(translate("MyPlugins/Krusader",
                                                          "Copy path to clipboard with Hamsi Manager")) + ".</description>\n" +
                        "  <command>" + executeCommandOfHamsiManager + " --qm --copyPath %aCurrent%</command>\n" +
                        "  <defaultshortcut></defaultshortcut>\n" +
                        " </action>\n"),
                       (" <action name=\"hamsimanager_fileTree\" >\n" +
                        "  <title>" + str(translate("MyPlugins/Krusader", "Build File Tree")) + "</title>\n" +
                        "  <tooltip>" + str(
                           translate("MyPlugins/Krusader", "Build file tree with Hamsi Manager")) + "</tooltip>\n" +
                        "  <icon>" + fu.joinPath(fu.themePath, "Images", "fileTree.png") + "</icon>\n" +
                        "  <category>Hamsi Manager</category>\n" +
                        "  <description>" + str(translate("MyPlugins/Krusader",
                                                          "Build file tree with Hamsi Manager")) + ".</description>\n" +
                        "  <command>" + executeCommandOfHamsiManager + " --qm --fileTree %aCurrent%</command>\n" +
                        "  <defaultshortcut></defaultshortcut>\n" +
                        " </action>\n"),
                       (" <action name=\"hamsimanager_removeOnlySubFiles\" >\n" +
                        "  <title>" + str(translate("MyPlugins/Krusader", "Remove Sub Files")) + "</title>\n" +
                        "  <tooltip>" + str(
                           translate("MyPlugins/Krusader", "Remove sub files with Hamsi Manager")) + "</tooltip>\n" +
                        "  <icon>" + fu.joinPath(fu.themePath, "Images", "removeOnlySubFiles.png") + "</icon>\n" +
                        "  <category>Hamsi Manager</category>\n" +
                        "  <description>" + str(translate("MyPlugins/Krusader",
                                                          "Remove sub files with Hamsi Manager")) + ".</description>\n" +
                        "  <command>" + executeCommandOfHamsiManager + " --qm --removeOnlySubFiles %aCurrent%</command>\n" +
                        "  <defaultshortcut></defaultshortcut>\n" +
                        " </action>\n"),
                       (" <action name=\"hamsimanager_pack\" >\n" +
                        "  <title>" + str(translate("MyPlugins/Krusader", "Clear It")) + "</title>\n" +
                        "  <tooltip>" + str(
                           translate("MyPlugins/Krusader", "Clear it with Hamsi Manager")) + "</tooltip>\n" +
                        "  <icon>" + fu.joinPath(fu.themePath, "Images", "pack.png") + "</icon>\n" +
                        "  <category>Hamsi Manager</category>\n" +
                        "  <description>" + str(
                           translate("MyPlugins/Krusader", "Clear it with Hamsi Manager")) + ".</description>\n" +
                        "  <command>" + executeCommandOfHamsiManager + " --qm --clear %aCurrent%</command>\n" +
                        "  <defaultshortcut></defaultshortcut>\n" +
                        " </action>\n"),
                       (" <action name=\"hamsimanager_hash\" >\n" +
                        "  <title>" + str(translate("MyPlugins/Krusader", "Hash Digest")) + "</title>\n" +
                        "  <tooltip>" + str(
                           translate("MyPlugins/Krusader", "Get hash digest with Hamsi Manager")) + "</tooltip>\n" +
                        "  <icon>" + fu.joinPath(fu.themePath, "Images", "hash.png") + "</icon>\n" +
                        "  <category>Hamsi Manager</category>\n" +
                        "  <description>" + str(translate("MyPlugins/Krusader",
                                                          "Get hash digest with Hamsi Manager")) + ".</description>\n" +
                        "  <command>" + executeCommandOfHamsiManager + " --qm --hash %aCurrent%</command>\n" +
                        "  <defaultshortcut></defaultshortcut>\n" +
                        " </action>\n"),
                       (" <action name=\"hamsimanager_textCorrector\" >\n" +
                        "  <title>" + str(translate("MyPlugins/Krusader", "Correct Content")) + "</title>\n" +
                        "  <tooltip>" + str(
                           translate("MyPlugins/Krusader", "Correct content with Hamsi Manager")) + "</tooltip>\n" +
                        "  <icon>" + fu.joinPath(fu.themePath, "Images", "textCorrector.png") + "</icon>\n" +
                        "  <category>Hamsi Manager</category>\n" +
                        "  <description>" + str(translate("MyPlugins/Krusader",
                                                          "Correct content with Hamsi Manager")) + ".</description>\n" +
                        "  <command>" + executeCommandOfHamsiManager + " --qm --textCorrector %aCurrent%</command>\n" +
                        "  <defaultshortcut></defaultshortcut>\n" +
                        " </action>\n"),
                       (" <action name=\"hamsimanager_search\" >\n" +
                        "  <title>" + str(translate("MyPlugins/Krusader", "Search")) + "</title>\n" +
                        "  <tooltip>" + str(
                           translate("MyPlugins/Krusader", "Search with Hamsi Manager")) + "</tooltip>\n" +
                        "  <icon>" + fu.joinPath(fu.themePath, "Images", "search.png") + "</icon>\n" +
                        "  <category>Hamsi Manager</category>\n" +
                        "  <description>" + str(
                           translate("MyPlugins/Krusader", "Search with Hamsi Manager")) + ".</description>\n" +
                        "  <command>" + executeCommandOfHamsiManager + " --qm --search %aCurrent%</command>\n" +
                        "  <defaultshortcut></defaultshortcut>\n" +
                        " </action>\n")]
    if uni.isRunningAsRoot():
        destinationPath = "/usr/share/apps/krusader/"
    else:
        destinationPath = uni.getKDE4HomePath() + "/share/apps/krusader/"
    try:
        pluginStrings = fu.readFromFile(destinationPath + "useractions.xml")
    except:
        if fu.isDir(destinationPath) is False:
            fu.makeDirs(destinationPath)
        if fu.isFile("/usr/share/apps/krusader/useraction_examples.xml"):
            pluginStrings = fu.readFromFile("/usr/share/apps/krusader/useraction_examples.xml")
        else:
            pluginStrings = ("<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\n" +
                             "<!DOCTYPE KrusaderUserActions>\n" +
                             "<KrusaderUserActions>\n" +
                             "</KrusaderUserActions>\n")
    pluginString = ""
    for pstr in myPluginStrings:
        if pluginStrings.find(pstr.split("\n")[0]) == -1:
            pluginString += pstr
    pluginStrings = pluginStrings.replace("</KrusaderUserActions>", pluginString + "</KrusaderUserActions>")
    fu.writeToFile(destinationPath + "useractions.xml", pluginStrings)
    if pluginString == "":
        return "AlreadyInstalled"
    return True


def uninstallThisPlugin():
    isAlreadyuninstalled = True
    if uni.isRunningAsRoot():
        destinationPath = "/usr/share/apps/krusader/"
    else:
        destinationPath = uni.getKDE4HomePath() + "/share/apps/krusader/"
    if fu.isFile(fu.joinPath(destinationPath, "useractions.xml")):
        import xml.etree.ElementTree as ET

        doc = ET.parse(fu.joinPath(destinationPath, "useractions.xml"))
        KrusaderUserActions = doc.getroot()
        actions = doc.findall("action")
        for act in doc.findall("action"):
            if act.get("name").find("hamsimanager") != -1:
                KrusaderUserActions.remove(act)
                isAlreadyuninstalled = False
        actions = doc.findall("action")
        doc.write(fu.joinPath(destinationPath, "useractions.xml"))
    if isAlreadyuninstalled:
        return "AlreadyUninstalled"
    return True
    
    
