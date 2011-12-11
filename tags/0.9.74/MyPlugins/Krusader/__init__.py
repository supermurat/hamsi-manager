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
import InputOutputs
import Execute
from MyObjects import translate
pluginName = str(translate("MyPlugins/Krusader", "Krusader`s User Actions Menu"))
pluginVersion = "0.3"
pluginFiles = []
pluginDirectory = ""
setupDirectory = ""

def isInstallable():
    return Variables.isAvailableKDE4()

def installThisPlugin():
    try:
        myPluginStrings = [(" <action name=\"hamsimanager_Organize\" >\n"+
                    "  <title>" + str(translate("MyPlugins/Krusader", "Organize With Hamsi Manager")) + "</title>\n"+
                    "  <tooltip>" + str(translate("MyPlugins/Krusader", "You can organize with Hamsi Manager")) + "</tooltip>\n"+
                    "  <icon>"+Variables.HamsiManagerDirectory+"/Themes/Default/Images/HamsiManager-128x128.png</icon>\n"+
                    "  <category>Hamsi Manager</category>\n"+
                    "  <description>" + str(translate("MyPlugins/Krusader", "You can continue to edit the folder you select with Hamsi Manager")) + ".</description>\n"+
                    "  <command>python "+Variables.HamsiManagerDirectory+"/HamsiManager.py --directory %aCurrent%</command>\n"+
                    "  <defaultshortcut>Ctrl+O</defaultshortcut>\n"+
                    " </action>\n"), 
                    (" <action name=\"hamsimanager_emendDirectory\" >\n"+
                    "  <title>" + str(translate("MyPlugins/Krusader", "Auto Emend Directory")) + "</title>\n"+
                    "  <tooltip>" + str(translate("MyPlugins/Krusader", "Auto emend with Hamsi Manager")) + "</tooltip>\n"+
                    "  <icon>"+Variables.HamsiManagerDirectory+"/Themes/Default/Images/HamsiManager-128x128.png</icon>\n"+
                    "  <category>Hamsi Manager</category>\n"+
                    "  <description>" + str(translate("MyPlugins/Krusader", "Auto emend with Hamsi Manager")) + ".</description>\n"+
                    "  <command>python "+Variables.HamsiManagerDirectory+"/HamsiManager.py --qm --emendDirectory %aCurrent%</command>\n"+
                    "  <defaultshortcut></defaultshortcut>\n"+
                    " </action>\n"),  
                    (" <action name=\"hamsimanager_emendDirectoryWithContents\" >\n"+
                    "  <title>" + str(translate("MyPlugins/Krusader", "Auto Emend Directory (With Contents)")) + "</title>\n"+
                    "  <tooltip>" + str(translate("MyPlugins/Krusader", "Auto emend with Hamsi Manager (With Contents)")) + "</tooltip>\n"+
                    "  <icon>"+Variables.HamsiManagerDirectory+"/Themes/Default/Images/HamsiManager-128x128.png</icon>\n"+
                    "  <category>Hamsi Manager</category>\n"+
                    "  <description>" + str(translate("MyPlugins/Krusader", "Auto emend with Hamsi Manager (With Contents)")) + ".</description>\n"+
                    "  <command>python "+Variables.HamsiManagerDirectory+"/HamsiManager.py --qm --emendDirectoryWithContents %aCurrent%</command>\n"+
                    "  <defaultshortcut></defaultshortcut>\n"+
                    " </action>\n"), 
                    (" <action name=\"hamsimanager_emendFile\" >\n"+
                    "  <title>" + str(translate("MyPlugins/Krusader", "Auto Emend File")) + "</title>\n"+
                    "  <tooltip>" + str(translate("MyPlugins/Krusader", "Auto emend with Hamsi Manager")) + "</tooltip>\n"+
                    "  <icon>"+Variables.HamsiManagerDirectory+"/Themes/Default/Images/HamsiManager-128x128.png</icon>\n"+
                    "  <category>Hamsi Manager</category>\n"+
                    "  <description>" + str(translate("MyPlugins/Krusader", "Auto emend with Hamsi Manager")) + ".</description>\n"+
                    "  <command>python "+Variables.HamsiManagerDirectory+"/HamsiManager.py --qm --emendFile %aCurrent%</command>\n"+
                    "  <defaultshortcut></defaultshortcut>\n"+
                    " </action>\n"), 
                    (" <action name=\"hamsimanager_pack\" >\n"+
                    "  <title>" + str(translate("MyPlugins/Krusader", "Pack It")) + "</title>\n"+
                    "  <tooltip>" + str(translate("MyPlugins/Krusader", "Pack it with Hamsi Manager")) + "</tooltip>\n"+
                    "  <icon>"+Variables.HamsiManagerDirectory+"/Themes/Default/Images/HamsiManager-128x128.png</icon>\n"+
                    "  <category>Hamsi Manager</category>\n"+
                    "  <description>" + str(translate("MyPlugins/Krusader", "Pack it with Hamsi Manager")) + ".</description>\n"+
                    "  <command>python "+Variables.HamsiManagerDirectory+"/HamsiManager.py --qm --pack %aCurrent%</command>\n"+
                    "  <defaultshortcut></defaultshortcut>\n"+
                    " </action>\n"), 
                    (" <action name=\"hamsimanager_checkIcon\" >\n"+
                    "  <title>" + str(translate("MyPlugins/Krusader", "Check Directory Icon")) + "</title>\n"+
                    "  <tooltip>" + str(translate("MyPlugins/Krusader", "Check directory icon with Hamsi Manager")) + "</tooltip>\n"+
                    "  <icon>"+Variables.HamsiManagerDirectory+"/Themes/Default/Images/HamsiManager-128x128.png</icon>\n"+
                    "  <category>Hamsi Manager</category>\n"+
                    "  <description>" + str(translate("MyPlugins/Krusader", "Check directory icon with Hamsi Manager")) + ".</description>\n"+
                    "  <command>python "+Variables.HamsiManagerDirectory+"/HamsiManager.py --qm --checkIcon %aCurrent%</command>\n"+
                    "  <defaultshortcut></defaultshortcut>\n"+
                    " </action>\n"), 
                    (" <action name=\"hamsimanager_clearEmptyDirectories\" >\n"+
                    "  <title>" + str(translate("MyPlugins/Krusader", "Clear Empty Directories")) + "</title>\n"+
                    "  <tooltip>" + str(translate("MyPlugins/Krusader", "Clear empty directories with Hamsi Manager")) + "</tooltip>\n"+
                    "  <icon>"+Variables.HamsiManagerDirectory+"/Themes/Default/Images/HamsiManager-128x128.png</icon>\n"+
                    "  <category>Hamsi Manager</category>\n"+
                    "  <description>" + str(translate("MyPlugins/Krusader", "Clear empty directories with Hamsi Manager")) + ".</description>\n"+
                    "  <command>python "+Variables.HamsiManagerDirectory+"/HamsiManager.py --qm --clearEmptyDirectories %aCurrent%</command>\n"+
                    "  <defaultshortcut></defaultshortcut>\n"+
                    " </action>\n"), 
                    (" <action name=\"hamsimanager_clearUnneededs\" >\n"+
                    "  <title>" + str(translate("MyPlugins/Krusader", "Clear Unneededs")) + "</title>\n"+
                    "  <tooltip>" + str(translate("MyPlugins/Krusader", "Clear unneededs with Hamsi Manager")) + "</tooltip>\n"+
                    "  <icon>"+Variables.HamsiManagerDirectory+"/Themes/Default/Images/HamsiManager-128x128.png</icon>\n"+
                    "  <category>Hamsi Manager</category>\n"+
                    "  <description>" + str(translate("MyPlugins/Krusader", "Clear unneededs with Hamsi Manager")) + ".</description>\n"+
                    "  <command>python "+Variables.HamsiManagerDirectory+"/HamsiManager.py --qm --clearUnneededs %aCurrent%</command>\n"+
                    "  <defaultshortcut></defaultshortcut>\n"+
                    " </action>\n"), 
                    (" <action name=\"hamsimanager_clearIgnoreds\" >\n"+
                    "  <title>" + str(translate("MyPlugins/Krusader", "Clear Ignoreds")) + "</title>\n"+
                    "  <tooltip>" + str(translate("MyPlugins/Krusader", "Clear ignoreds with Hamsi Manager")) + "</tooltip>\n"+
                    "  <icon>"+Variables.HamsiManagerDirectory+"/Themes/Default/Images/HamsiManager-128x128.png</icon>\n"+
                    "  <category>Hamsi Manager</category>\n"+
                    "  <description>" + str(translate("MyPlugins/Krusader", "Clear ignoreds with Hamsi Manager")) + ".</description>\n"+
                    "  <command>python "+Variables.HamsiManagerDirectory+"/HamsiManager.py --qm --clearIgnoreds %aCurrent%</command>\n"+
                    "  <defaultshortcut></defaultshortcut>\n"+
                    " </action>\n"), 
                    (" <action name=\"hamsimanager_copyPath\" >\n"+
                    "  <title>" + str(translate("MyPlugins/Krusader", "Copy Path To Clipboard")) + "</title>\n"+
                    "  <tooltip>" + str(translate("MyPlugins/Krusader", "Copy path to clipboard with Hamsi Manager")) + "</tooltip>\n"+
                    "  <icon>"+Variables.HamsiManagerDirectory+"/Themes/Default/Images/HamsiManager-128x128.png</icon>\n"+
                    "  <category>Hamsi Manager</category>\n"+
                    "  <description>" + str(translate("MyPlugins/Krusader", "Copy path to clipboard with Hamsi Manager")) + ".</description>\n"+
                    "  <command>python "+Variables.HamsiManagerDirectory+"/HamsiManager.py --qm --copyPath %aCurrent%</command>\n"+
                    "  <defaultshortcut></defaultshortcut>\n"+
                    " </action>\n"), 
                    (" <action name=\"hamsimanager_fileTree\" >\n"+
                    "  <title>" + str(translate("MyPlugins/Krusader", "Build File Tree")) + "</title>\n"+
                    "  <tooltip>" + str(translate("MyPlugins/Krusader", "Build file tree with Hamsi Manager")) + "</tooltip>\n"+
                    "  <icon>"+Variables.HamsiManagerDirectory+"/Themes/Default/Images/HamsiManager-128x128.png</icon>\n"+
                    "  <category>Hamsi Manager</category>\n"+
                    "  <description>" + str(translate("MyPlugins/Krusader", "Build file tree with Hamsi Manager")) + ".</description>\n"+
                    "  <command>python "+Variables.HamsiManagerDirectory+"/HamsiManager.py --qm --fileTree %aCurrent%</command>\n"+
                    "  <defaultshortcut></defaultshortcut>\n"+
                    " </action>\n"), 
                    (" <action name=\"hamsimanager_removeOnlySubFiles\" >\n"+
                    "  <title>" + str(translate("MyPlugins/Krusader", "Remove Sub Files")) + "</title>\n"+
                    "  <tooltip>" + str(translate("MyPlugins/Krusader", "Remove sub files with Hamsi Manager")) + "</tooltip>\n"+
                    "  <icon>"+Variables.HamsiManagerDirectory+"/Themes/Default/Images/HamsiManager-128x128.png</icon>\n"+
                    "  <category>Hamsi Manager</category>\n"+
                    "  <description>" + str(translate("MyPlugins/Krusader", "Remove sub files with Hamsi Manager")) + ".</description>\n"+
                    "  <command>python "+Variables.HamsiManagerDirectory+"/HamsiManager.py --qm --removeOnlySubFiles %aCurrent%</command>\n"+
                    "  <defaultshortcut></defaultshortcut>\n"+
                    " </action>\n"), 
                    (" <action name=\"hamsimanager_pack\" >\n"+
                    "  <title>" + str(translate("MyPlugins/Krusader", "Clear It")) + "</title>\n"+
                    "  <tooltip>" + str(translate("MyPlugins/Krusader", "Clear it with Hamsi Manager")) + "</tooltip>\n"+
                    "  <icon>"+Variables.HamsiManagerDirectory+"/Themes/Default/Images/HamsiManager-128x128.png</icon>\n"+
                    "  <category>Hamsi Manager</category>\n"+
                    "  <description>" + str(translate("MyPlugins/Krusader", "Clear it with Hamsi Manager")) + ".</description>\n"+
                    "  <command>python "+Variables.HamsiManagerDirectory+"/HamsiManager.py --qm --clear %aCurrent%</command>\n"+
                    "  <defaultshortcut></defaultshortcut>\n"+
                    " </action>\n"), 
                    (" <action name=\"hamsimanager_hash\" >\n"+
                    "  <title>" + str(translate("MyPlugins/Krusader", "Hash Digest")) + "</title>\n"+
                    "  <tooltip>" + str(translate("MyPlugins/Krusader", "Get hash digest with Hamsi Manager")) + "</tooltip>\n"+
                    "  <icon>"+Variables.HamsiManagerDirectory+"/Themes/Default/Images/HamsiManager-128x128.png</icon>\n"+
                    "  <category>Hamsi Manager</category>\n"+
                    "  <description>" + str(translate("MyPlugins/Krusader", "Get hash digest with Hamsi Manager")) + ".</description>\n"+
                    "  <command>python "+Variables.HamsiManagerDirectory+"/HamsiManager.py --qm --hash %aCurrent%</command>\n"+
                    "  <defaultshortcut></defaultshortcut>\n"+
                    " </action>\n"), 
                    (" <action name=\"hamsimanager_textCorrector\" >\n"+
                    "  <title>" + str(translate("MyPlugins/Krusader", "Correct Content")) + "</title>\n"+
                    "  <tooltip>" + str(translate("MyPlugins/Krusader", "Correct content with Hamsi Manager")) + "</tooltip>\n"+
                    "  <icon>"+Variables.HamsiManagerDirectory+"/Themes/Default/Images/HamsiManager-128x128.png</icon>\n"+
                    "  <category>Hamsi Manager</category>\n"+
                    "  <description>" + str(translate("MyPlugins/Krusader", "Correct content with Hamsi Manager")) + ".</description>\n"+
                    "  <command>python "+Variables.HamsiManagerDirectory+"/HamsiManager.py --qm --textCorrector %aCurrent%</command>\n"+
                    "  <defaultshortcut></defaultshortcut>\n"+
                    " </action>\n")]
        if Variables.isRunningAsRoot():
            destinationPath = "/usr/share/apps/krusader/"
        else:
            destinationPath = Variables.getKDE4HomePath() +"/share/apps/krusader/"
        try:
            pluginStrings = InputOutputs.IA.readFromFile(destinationPath + "useractions.xml")
        except:
            if InputOutputs.IA.isDir(destinationPath)==False:
                InputOutputs.IA.makeDirs(destinationPath)
            pluginStrings = InputOutputs.IA.readFromFile("/usr/share/apps/krusader/useraction_examples.xml")
        pluginString = ""
        for pstr in myPluginStrings:
            if pluginStrings.find(pstr.split("\n")[0])==-1:
                pluginString += pstr
        pluginStrings = pluginStrings.replace("</KrusaderUserActions>", pluginString + "</KrusaderUserActions>")
        InputOutputs.IA.writeToFile(destinationPath + "useractions.xml", pluginStrings)
        if pluginString=="":
            return "AlreadyInstalled"
    except:
        return False
    return True