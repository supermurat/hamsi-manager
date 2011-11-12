#!/usr/bin/env python
 
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

import os
from cx_Freeze import setup, Executable
from Core import Variables
import InputOutputs

includes = []
excludes = ["_gtkagg", "_tkagg", "bsddb", "curses", "email", 
            "pywin.debugger", "pywin.debugger.dbgcon", "pywin.dialogs", 
            "tcl","Tkconstants", "Tkinter"]
packages = ["Amarok","Core","Databases","Details","InputOutputs","Languages",
        "MyPlugins","Options","SearchEngines","Tables","Taggers","Tools","Viewers", 
        #"pysqlite2", # For only (python<2.7)
        "sqlite3", # For only (python>=2.7)
        "PyKDE4", # If you want to use KDE4 (Is not requirement but however it is very better than)
        "eyeD3", "musicbrainz2", # not available in python 3.x
        "hashlib", "tarfile", "urllib", "PyQt4"]
path = []
include_files = [("Amarok","Amarok"),("Languages","Languages"),("MyPlugins","MyPlugins"),("SearchEngines","SearchEngines"),("Taggers","Taggers"),("Themes","Themes")]

exeBase = "Console" # "Win32GUI" for windows
fileExtension = "" # ".exe" for windows

MainExe = Executable(
    script = "HamsiManager.py",
    initScript = None,
    base = exeBase,
    targetName = "HamsiManager" + fileExtension,
    compress = True,
    copyDependentFiles = False,
    appendScriptToExe = False,
    appendScriptToLibrary = False,
    icon = "Themes/Default/Images/HamsiManager-128x128.ico"
    )
    
ReconfigureExe = Executable(
    script = "Reconfigure.py",
    initScript = None,
    base = exeBase,
    targetName = "Reconfigure" + fileExtension,
    compress = True,
    copyDependentFiles = False,
    appendScriptToExe = False,
    appendScriptToLibrary = False,
    )
    
InstallExe = Executable(
    script = "install.py",
    initScript = None,
    base = exeBase,
    targetName = "HamsiManagerInstaller" + fileExtension,
    compress = True,
    copyDependentFiles = False,
    appendScriptToExe = False,
    appendScriptToLibrary = False,
    )
    
# Update is not possible now 
#ConfigureUpdateExe = Executable(
#    script = "ConfigureUpdate.py",
#    initScript = None,
#    base = exeBase,
#    targetName = "ConfigureUpdate" + fileExtension,
#    compress = True,
#    copyDependentFiles = False,
#    appendScriptToExe = False,
#    appendScriptToLibrary = False,
#    )

setup(
    version = Variables.version,
    description = InputOutputs.readFromFile(os.getcwd() + "/Languages/About_en_GB", "utf-8"),
    author = "Murat Demir",
    name = "HamsiManager",
    options = {"build_exe": {"includes": includes,
                             "excludes": excludes,
                             "packages": packages,
                             "path": path,
                             "include_files":include_files,
                             }
               },
    executables = [MainExe, ReconfigureExe, InstallExe]#, ConfigureUpdateExe]
    )

