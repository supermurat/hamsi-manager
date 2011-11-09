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

from cx_Freeze import setup, Executable

includes = []
excludes = ["_gtkagg", "_tkagg", "bsddb", "curses", "email", 
            "pywin.debugger", "pywin.debugger.dbgcon", "pywin.dialogs", 
            "tcl","Tkconstants", "Tkinter"]
packages = ["Amarok","Core","Databases","Details","InputOutputs","Languages",
        "MyPlugins","Options","SearchEngines","Tables","Taggers","Tools","Viewers", 
        #"pysqlite2", # For only (python<2.7)
        "sqlite3", # For only (python>=2.7)
        "PyKDE4", # If you want to use KDE4 (Is not requirement but however it is very better than)
        "eyeD3", "musicbrainz2", 
        "hashlib", "tarfile", "urllib", "PyQt4"]
path = []
include_files = [("Amarok","Amarok"),("Languages","Languages"),("MyPlugins","MyPlugins"),("SearchEngines","SearchEngines"),("Taggers","Taggers"),("Themes","Themes")]

Exe_Target = Executable(
    script = "HamsiManager.py",
    initScript = None,
    #base = "Win32GUI", # for windows
    targetName = "HamsiManager",
    compress = True,
    copyDependentFiles = False,
    appendScriptToExe = False,
    appendScriptToLibrary = False,
    icon = r"Themes/Default/Images/HamsiManager-128x128.ico"
    )

setup(
    version = "0.9",
    description = "No Description",
    author = "Murat Demir",
    name = "HamsiManager",
    options = {"build_exe": {"includes": includes,
                             "excludes": excludes,
                             "packages": packages,
                             "path": path,
                             "include_files":include_files,
                             }
               },
    executables = [Exe_Target]
    )

