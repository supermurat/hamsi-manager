#!/usr/bin/env python
 
## This file is part of HamsiManager.
## 
## Copyright (c) 2010 - 2012 Murat Demir <mopened@gmail.com>      
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

import os, sys

HamsiManagerDirectory = os.getcwd()
sys.path.insert(0,HamsiManagerDirectory)
try:
    from Core import Variables
except:
    HamsiManagerDirectory = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HamsiManagerDirectory)))))
    sys.path.insert(0,HamsiManagerDirectory)
    from Core import Variables

from cx_Freeze import setup, Executable
Variables.checkStartupVariables()
Variables.HamsiManagerDirectory = HamsiManagerDirectory
import InputOutputs

includes = []
excludes = ["_gtkagg", "_tkagg", "bsddb", "curses", "email", 
            "pywin.debugger", "pywin.debugger.dbgcon", "pywin.dialogs", 
            "tcl","Tkconstants", "Tkinter"]
path = sys.path + [HamsiManagerDirectory]



include_files = [(os.path.join(HamsiManagerDirectory, "Amarok"), "Amarok"),
                (os.path.join(HamsiManagerDirectory, "Languages"), "Languages"),
                (os.path.join(HamsiManagerDirectory, "MyPlugins"), "MyPlugins"),
                (os.path.join(HamsiManagerDirectory, "SearchEngines"), "SearchEngines"),
                (os.path.join(HamsiManagerDirectory, "Taggers"), "Taggers"),
                (os.path.join(HamsiManagerDirectory, "Themes"), "Themes")]
             
InputOutputs.writeToFile(InputOutputs.joinPath(InputOutputs.getTempDir(), "HamsiManagerHasBeenBuilt"), str(sys.argv) + "\nPlease, don't remove this file.")
include_files.append((os.path.join(InputOutputs.getTempDir(), "HamsiManagerHasBeenBuilt"), "HamsiManagerHasBeenBuilt"))

data_files = []

if os.name=="posix":
    from Core import MyConfigure
    installationDirectory = InputOutputs.joinPath("/", "usr", "lib", "HamsiManager-" + Variables.version)
    fileContent = MyConfigure.getConfiguredDesktopFileContent(installationDirectory, "/usr/bin/hamsi")
    InputOutputs.writeToFile(InputOutputs.joinPath(InputOutputs.getTempDir(), "HamsiManager.desktop"), fileContent)
    data_files.append((InputOutputs.joinPath("/", "usr", "share", "applications"), [InputOutputs.joinPath(InputOutputs.getTempDir(), "HamsiManager.desktop")]))
    
    if Variables.isAvailableKDE4():
        for langCode in Variables.getInstalledLanguagesCodes():
            KDELocalateDir = InputOutputs.joinPath("/", "usr", "share", "locale", str(langCode[:2]), "LC_MESSAGES")
            langFile = InputOutputs.joinPath(Variables.HamsiManagerDirectory, "Languages", "DontTranslate", str(langCode), "HamsiManager.mo")
            if InputOutputs.isFile(langFile):
                data_files.append((KDELocalateDir, [langFile]))
        
    data_files.append((InputOutputs.joinPath("/", "usr", "share", "icons"), [InputOutputs.joinPath(HamsiManagerDirectory, "Themes", "Default", "Images", "hamsi.png")]))
    data_files.append((InputOutputs.joinPath("/", "usr", "share", "pixmaps"), [InputOutputs.joinPath(HamsiManagerDirectory, "Themes", "Default", "Images", "hamsi.png")]))
    
packages = ["Amarok","Core","Databases","Details","InputOutputs","Languages",
        "MyPlugins","Options","SearchEngines","Tables","Taggers","Tools","Viewers",
        "hashlib", "tarfile", "urllib", "PyQt4", 
        "sqlite3", "ctypes", 
        "PyKDE4", "_mysql", 
        "eyeD3", "musicbrainz2"]

if float(sys.version[:3])<2.7:
    packages.remove("sqlite3")
    packages.append("pysqlite2")
    
if float(sys.version[:3])>=3.0:
    packages.remove("eyeD3")
    packages.remove("musicbrainz2")
    
if os.name=="nt":
    packages.remove("PyKDE4")
    packages.remove("_mysql")
    packages.append("win32com")
    packages.append("win32api")
    packages.append("win32con")
    

exeBase = "Console"
fileExtension = ""
iconExtension = ".png"

if os.name=="nt":
    exeBase = "Win32GUI"
    fileExtension = ".exe"
    iconExtension = ".ico"

MainExe = Executable(
    script = os.path.join(HamsiManagerDirectory, "HamsiManager.py"),
    initScript = None,
    base = exeBase,
    targetName = "hamsi" + fileExtension,
    compress = True,
    copyDependentFiles = False,
    appendScriptToExe = False,
    appendScriptToLibrary = False,
    icon = os.path.join(HamsiManagerDirectory, "Themes/Default/Images/hamsi" + iconExtension), 
    shortcutName = "Hamsi Manager",
    shortcutDir = "ProgramMenuFolder"
)

setup(
    name = "HamsiManager",
    version = Variables.version,
    description  = "Hamsi Manager is a file manager which was developed for extra operations.",
    long_description = InputOutputs.readFromFile(os.path.join(HamsiManagerDirectory, "Languages/About_en_GB"), "utf-8"),
    author = "Murat Demir",
    author_email = "mopened@gmail.com",
    maintainer   = "Murat Demir",
    maintainer_email = "mopened@gmail.com",
    url = "http://hamsiapps.com/Hamsi-Manager",
    download_url = "http://sourceforge.net/projects/hamsimanager/files/", 
    license      = "GPLv3",
    options = {"build_exe": {"includes": includes,
                             "excludes": excludes,
                             "packages": packages,
                             "path": path,
                             "include_files":include_files,
                             }
               },
    executables = [MainExe],
    data_files = data_files
)

