# -*- coding: utf-8 -*-
import os
import Universals
import InputOutputs
import Settings
from MyObjects import translate
pluginName = str(translate("MyPlugins/Krusader", "Krusader`s User Actions Menu"))
pluginVersion = "0.1"
pluginFiles = []
pluginDirectory = ""
setupDirectory = ""

def isInstallable():
    return Settings.isAvailablePyKDE4()

def installThisPlugin():
    try:
        myPluginStrings = [(" <action name=\"hamsimanager_Organize\" >\n"+
                    "  <title>" + str(translate("MyPlugins/Krusader", "Organize With Hamsi Manager")) + "</title>\n"+
                    "  <tooltip>" + str(translate("MyPlugins/Krusader", "You can organize with Hamsi Manager")) + "</tooltip>\n"+
                    "  <icon>"+Universals.HamsiManagerDirectory+"/Source/Themes/Default/Images/HamsiManager.png</icon>\n"+
                    "  <category>Hamsi Manager</category>\n"+
                    "  <description>" + str(translate("MyPlugins/Krusader", "You can continue to edit the folder you select with Hamsi Manager")) + ".</description>\n"+
                    "  <command>python "+Universals.HamsiManagerDirectory+"/HamsiManager.py %aCurrent%</command>\n"+
                    "  <defaultshortcut>Ctrl+O</defaultshortcut>\n"+
                    " </action>\n"), 
                    (" <action name=\"hamsimanager_emendDirectory\" >\n"+
                    "  <title>" + str(translate("MyPlugins/Krusader", "Auto Emend Directory")) + "</title>\n"+
                    "  <tooltip>" + str(translate("MyPlugins/Krusader", "Auto emend with Hamsi Manager")) + "</tooltip>\n"+
                    "  <icon>"+Universals.HamsiManagerDirectory+"/Source/Themes/Default/Images/HamsiManager.png</icon>\n"+
                    "  <category>Hamsi Manager</category>\n"+
                    "  <description>" + str(translate("MyPlugins/Krusader", "Auto emend with Hamsi Manager")) + ".</description>\n"+
                    "  <command>python "+Universals.HamsiManagerDirectory+"/HamsiManager.py -qm emendDirectory %aCurrent%</command>\n"+
                    "  <defaultshortcut></defaultshortcut>\n"+
                    " </action>\n"),  
                    (" <action name=\"hamsimanager_emendDirectoryWithContents\" >\n"+
                    "  <title>" + str(translate("MyPlugins/Krusader", "Auto Emend Directory (With Contents)")) + "</title>\n"+
                    "  <tooltip>" + str(translate("MyPlugins/Krusader", "Auto emend with Hamsi Manager (With Contents)")) + "</tooltip>\n"+
                    "  <icon>"+Universals.HamsiManagerDirectory+"/Source/Themes/Default/Images/HamsiManager.png</icon>\n"+
                    "  <category>Hamsi Manager</category>\n"+
                    "  <description>" + str(translate("MyPlugins/Krusader", "Auto emend with Hamsi Manager (With Contents)")) + ".</description>\n"+
                    "  <command>python "+Universals.HamsiManagerDirectory+"/HamsiManager.py -qm emendDirectoryWithContents %aCurrent%</command>\n"+
                    "  <defaultshortcut></defaultshortcut>\n"+
                    " </action>\n"), 
                    (" <action name=\"hamsimanager_emendFile\" >\n"+
                    "  <title>" + str(translate("MyPlugins/Krusader", "Auto Emend File")) + "</title>\n"+
                    "  <tooltip>" + str(translate("MyPlugins/Krusader", "Auto emend with Hamsi Manager")) + "</tooltip>\n"+
                    "  <icon>"+Universals.HamsiManagerDirectory+"/Source/Themes/Default/Images/HamsiManager.png</icon>\n"+
                    "  <category>Hamsi Manager</category>\n"+
                    "  <description>" + str(translate("MyPlugins/Krusader", "Auto emend with Hamsi Manager")) + ".</description>\n"+
                    "  <command>python "+Universals.HamsiManagerDirectory+"/HamsiManager.py -qm emendFile %aCurrent%</command>\n"+
                    "  <defaultshortcut></defaultshortcut>\n"+
                    " </action>\n"), 
                    (" <action name=\"hamsimanager_pack\" >\n"+
                    "  <title>" + str(translate("MyPlugins/Krusader", "Pack It")) + "</title>\n"+
                    "  <tooltip>" + str(translate("MyPlugins/Krusader", "Pack it with Hamsi Manager")) + "</tooltip>\n"+
                    "  <icon>"+Universals.HamsiManagerDirectory+"/Source/Themes/Default/Images/HamsiManager.png</icon>\n"+
                    "  <category>Hamsi Manager</category>\n"+
                    "  <description>" + str(translate("MyPlugins/Krusader", "Pack it with Hamsi Manager")) + ".</description>\n"+
                    "  <command>python "+Universals.HamsiManagerDirectory+"/HamsiManager.py -qm pack %aCurrent%</command>\n"+
                    "  <defaultshortcut></defaultshortcut>\n"+
                    " </action>\n"), 
                    (" <action name=\"hamsimanager_checkIcon\" >\n"+
                    "  <title>" + str(translate("MyPlugins/Krusader", "Check Directory Icon")) + "</title>\n"+
                    "  <tooltip>" + str(translate("MyPlugins/Krusader", "Check directory icon with Hamsi Manager")) + "</tooltip>\n"+
                    "  <icon>"+Universals.HamsiManagerDirectory+"/Source/Themes/Default/Images/HamsiManager.png</icon>\n"+
                    "  <category>Hamsi Manager</category>\n"+
                    "  <description>" + str(translate("MyPlugins/Krusader", "Check directory icon with Hamsi Manager")) + ".</description>\n"+
                    "  <command>python "+Universals.HamsiManagerDirectory+"/HamsiManager.py -qm checkIcon %aCurrent%</command>\n"+
                    "  <defaultshortcut></defaultshortcut>\n"+
                    " </action>\n"), 
                    (" <action name=\"hamsimanager_clearEmptyDirectories\" >\n"+
                    "  <title>" + str(translate("MyPlugins/Krusader", "Clear Empty Directories")) + "</title>\n"+
                    "  <tooltip>" + str(translate("MyPlugins/Krusader", "Clear empty directories with Hamsi Manager")) + "</tooltip>\n"+
                    "  <icon>"+Universals.HamsiManagerDirectory+"/Source/Themes/Default/Images/HamsiManager.png</icon>\n"+
                    "  <category>Hamsi Manager</category>\n"+
                    "  <description>" + str(translate("MyPlugins/Krusader", "Clear empty directories with Hamsi Manager")) + ".</description>\n"+
                    "  <command>python "+Universals.HamsiManagerDirectory+"/HamsiManager.py -qm clearEmptyDirectories %aCurrent%</command>\n"+
                    "  <defaultshortcut></defaultshortcut>\n"+
                    " </action>\n"), 
                    (" <action name=\"hamsimanager_clearUnneededs\" >\n"+
                    "  <title>" + str(translate("MyPlugins/Krusader", "Clear Unneededs")) + "</title>\n"+
                    "  <tooltip>" + str(translate("MyPlugins/Krusader", "Clear unneededs with Hamsi Manager")) + "</tooltip>\n"+
                    "  <icon>"+Universals.HamsiManagerDirectory+"/Source/Themes/Default/Images/HamsiManager.png</icon>\n"+
                    "  <category>Hamsi Manager</category>\n"+
                    "  <description>" + str(translate("MyPlugins/Krusader", "Clear unneededs with Hamsi Manager")) + ".</description>\n"+
                    "  <command>python "+Universals.HamsiManagerDirectory+"/HamsiManager.py -qm clearUnneededs %aCurrent%</command>\n"+
                    "  <defaultshortcut></defaultshortcut>\n"+
                    " </action>\n"), 
                    (" <action name=\"hamsimanager_clearIgnoreds\" >\n"+
                    "  <title>" + str(translate("MyPlugins/Krusader", "Clear Ignoreds")) + "</title>\n"+
                    "  <tooltip>" + str(translate("MyPlugins/Krusader", "Clear ignoreds with Hamsi Manager")) + "</tooltip>\n"+
                    "  <icon>"+Universals.HamsiManagerDirectory+"/Source/Themes/Default/Images/HamsiManager.png</icon>\n"+
                    "  <category>Hamsi Manager</category>\n"+
                    "  <description>" + str(translate("MyPlugins/Krusader", "Clear ignoreds with Hamsi Manager")) + ".</description>\n"+
                    "  <command>python "+Universals.HamsiManagerDirectory+"/HamsiManager.py -qm clearIgnoreds %aCurrent%</command>\n"+
                    "  <defaultshortcut></defaultshortcut>\n"+
                    " </action>\n"), 
                    (" <action name=\"hamsimanager_copyPath\" >\n"+
                    "  <title>" + str(translate("MyPlugins/Krusader", "Copy Path To Clipboard")) + "</title>\n"+
                    "  <tooltip>" + str(translate("MyPlugins/Krusader", "Copy path to clipboard with Hamsi Manager")) + "</tooltip>\n"+
                    "  <icon>"+Universals.HamsiManagerDirectory+"/Source/Themes/Default/Images/HamsiManager.png</icon>\n"+
                    "  <category>Hamsi Manager</category>\n"+
                    "  <description>" + str(translate("MyPlugins/Krusader", "Copy path to clipboard with Hamsi Manager")) + ".</description>\n"+
                    "  <command>python "+Universals.HamsiManagerDirectory+"/HamsiManager.py -qm copyPath %aCurrent%</command>\n"+
                    "  <defaultshortcut></defaultshortcut>\n"+
                    " </action>\n"), 
                    (" <action name=\"hamsimanager_fileTree\" >\n"+
                    "  <title>" + str(translate("MyPlugins/Krusader", "Build File Tree")) + "</title>\n"+
                    "  <tooltip>" + str(translate("MyPlugins/Krusader", "Build file tree with Hamsi Manager")) + "</tooltip>\n"+
                    "  <icon>"+Universals.HamsiManagerDirectory+"/Source/Themes/Default/Images/HamsiManager.png</icon>\n"+
                    "  <category>Hamsi Manager</category>\n"+
                    "  <description>" + str(translate("MyPlugins/Krusader", "Build file tree with Hamsi Manager")) + ".</description>\n"+
                    "  <command>python "+Universals.HamsiManagerDirectory+"/HamsiManager.py -qm fileTree %aCurrent%</command>\n"+
                    "  <defaultshortcut></defaultshortcut>\n"+
                    " </action>\n"), 
                    (" <action name=\"hamsimanager_removeOnlySubFiles\" >\n"+
                    "  <title>" + str(translate("MyPlugins/Krusader", "Remove Sub Files")) + "</title>\n"+
                    "  <tooltip>" + str(translate("MyPlugins/Krusader", "Remove sub files with Hamsi Manager")) + "</tooltip>\n"+
                    "  <icon>"+Universals.HamsiManagerDirectory+"/Source/Themes/Default/Images/HamsiManager.png</icon>\n"+
                    "  <category>Hamsi Manager</category>\n"+
                    "  <description>" + str(translate("MyPlugins/Krusader", "Remove sub files with Hamsi Manager")) + ".</description>\n"+
                    "  <command>python "+Universals.HamsiManagerDirectory+"/HamsiManager.py -qm removeOnlySubFiles %aCurrent%</command>\n"+
                    "  <defaultshortcut></defaultshortcut>\n"+
                    " </action>\n"), 
                    (" <action name=\"hamsimanager_pack\" >\n"+
                    "  <title>" + str(translate("MyPlugins/Krusader", "Clear It")) + "</title>\n"+
                    "  <tooltip>" + str(translate("MyPlugins/Krusader", "Clear it with Hamsi Manager")) + "</tooltip>\n"+
                    "  <icon>"+Universals.HamsiManagerDirectory+"/Source/Themes/Default/Images/HamsiManager.png</icon>\n"+
                    "  <category>Hamsi Manager</category>\n"+
                    "  <description>" + str(translate("MyPlugins/Krusader", "Clear it with Hamsi Manager")) + ".</description>\n"+
                    "  <command>python "+Universals.HamsiManagerDirectory+"/HamsiManager.py -qm clear %aCurrent%</command>\n"+
                    "  <defaultshortcut></defaultshortcut>\n"+
                    " </action>\n")]
        try:
            pluginStrings = InputOutputs.readFromFile(Universals.getKDE4HomePath() +"share/apps/krusader/useractions.xml")
        except:
            InputOutputs.makeDirs(Universals.getKDE4HomePath() + "share/apps/krusader/")
            InputOutputs.writeToFile(Universals.getKDE4HomePath() + "share/apps/krusader/useractions.xml", "<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\n<!DOCTYPE KrusaderUserActions>\n<KrusaderUserActions>\n</KrusaderUserActions>")
            pluginStrings = InputOutputs.readFromFile(Universals.getKDE4HomePath() + "share/apps/krusader/useractions.xml")
        pluginString = ""
        for pstr in myPluginStrings:
            if pluginStrings.find(pstr.split("\n")[0])==-1:
                pluginString += pstr
        pluginStrings = pluginStrings.replace("</KrusaderUserActions>", pluginString + "</KrusaderUserActions>")
        InputOutputs.writeToFile(Universals.getKDE4HomePath() + "share/apps/krusader/useractions.xml", pluginStrings)
        if pluginString=="":
            return "AlreadyInstalled"
    except:
        return False
    return True
