#!/usr/bin/env python

## This file is part of HamsiManager.
##
## Copyright (c) 2010 - 2014 Murat Demir <mopened@gmail.com>
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
sys.path.insert(0, HamsiManagerDirectory)
try:
    import FileUtils as fu
    from Core import Universals as uni
except:
    HamsiManagerDirectory = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HamsiManagerDirectory)))))
    sys.path.insert(0, HamsiManagerDirectory)
    from Core import Universals as uni
    import FileUtils as fu

from cx_Freeze import setup, Executable

fu.initStartupVariables()
fu.HamsiManagerDirectory = HamsiManagerDirectory
import FileUtils as fu

includes = []
excludes = ["_gtkagg", "_tkagg", "bsddb", "curses", "email",
            "pywin.debugger", "pywin.debugger.dbgcon", "pywin.dialogs",
            "tcl", "Tkconstants", "Tkinter", "PySide"]
path = sys.path + [HamsiManagerDirectory]

include_files = [(os.path.join(HamsiManagerDirectory, "Amarok"), "Amarok"),
                 (os.path.join(HamsiManagerDirectory, "Languages"), "Languages"),
                 (os.path.join(HamsiManagerDirectory, "MyPlugins"), "MyPlugins"),
                 (os.path.join(HamsiManagerDirectory, "SearchEngines"), "SearchEngines"),
                 (os.path.join(HamsiManagerDirectory, "Taggers"), "Taggers"),
                 (os.path.join(HamsiManagerDirectory, "Themes"), "Themes")]

fu.writeToFile(fu.joinPath(fu.getTempDir(), "HamsiManagerHasBeenBuilt"),
               str(sys.argv) + "\nPlease, don't remove this file.")
include_files.append((os.path.join(fu.getTempDir(), "HamsiManagerHasBeenBuilt"), "HamsiManagerHasBeenBuilt"))

data_files = []

if os.name == "posix":
    from Core import MyConfigure

    installationDirectory = fu.joinPath("/", "usr", "lib", "HamsiManager-" + uni.version)
    fileContent = MyConfigure.getConfiguredDesktopFileContent(installationDirectory, "/usr/bin/hamsi")
    fu.writeToFile(fu.joinPath(fu.getTempDir(), "HamsiManager.desktop"), fileContent)
    data_files.append(
        (fu.joinPath("/", "usr", "share", "applications"), [fu.joinPath(fu.getTempDir(), "HamsiManager.desktop")]))

    if uni.isAvailableKDE4():
        for langCode in uni.getInstalledLanguagesCodes():
            KDELocalateDir = fu.joinPath("/", "usr", "share", "locale", str(langCode[:2]), "LC_MESSAGES")
            langFile = fu.joinPath(fu.HamsiManagerDirectory, "Languages", "DontTranslate", str(langCode),
                                   "HamsiManager.mo")
            if fu.isFile(langFile):
                data_files.append((KDELocalateDir, [langFile]))

    data_files.append((fu.joinPath("/", "usr", "share", "icons"),
                       [fu.joinPath(HamsiManagerDirectory, "Themes", "Default", "Images", "hamsi.png")]))
    data_files.append((fu.joinPath("/", "usr", "share", "pixmaps"),
                       [fu.joinPath(HamsiManagerDirectory, "Themes", "Default", "Images", "hamsi.png")]))

packages = ["Amarok", "Core", "Databases", "Details", "FileUtils", "Languages",
            "MyPlugins", "Options", "SearchEngines", "SpecialTools", "Tables", "Taggers", "Tools", "Viewers", "Bars",
            "hashlib", "tarfile", "urllib", "PyQt4",
            "sqlite3", "ctypes",
            "PyKDE4", "_mysql",
            "eyed3", "musicbrainz2"]

exeBase = "Console"
fileExtension = ""
iconExtension = ".png"

if float(sys.version[:3]) < 2.7:
    packages.remove("sqlite3")
    packages.append("pysqlite2")

if float(sys.version[:3]) >= 3.0:
    packages.remove("eyed3")
    packages.remove("musicbrainz2")

if os.name == "nt":
    packages.remove("PyKDE4")
    packages.remove("_mysql")
    includes.append("win32com")
    packages.append("win32api")
    packages.append("win32con")
    exeBase = "Win32GUI"
    fileExtension = ".exe"
    iconExtension = ".ico"

MainExe = Executable(
    script=os.path.join(HamsiManagerDirectory, "HamsiManager.py"),
    initScript=None,
    base=exeBase,
    targetName="hamsi" + fileExtension,
    compress=True,
    copyDependentFiles=False,
    appendScriptToExe=False,
    appendScriptToLibrary=False,
    icon=os.path.join(HamsiManagerDirectory, "Themes/Default/Images/hamsi" + iconExtension),
    shortcutName="Hamsi Manager",
    shortcutDir="ProgramMenuFolder"
)

setup(
    name="HamsiManager",
    version=uni.version,
    description="Hamsi Manager is a file manager which was developed for extra operations.",
    long_description=fu.readFromFile(os.path.join(HamsiManagerDirectory, "Languages/About_en_GB"), "utf-8"),
    author="Murat Demir",
    author_email="mopened@gmail.com",
    maintainer="Murat Demir",
    maintainer_email="mopened@gmail.com",
    url="http://hamsiapps.com/Hamsi-Manager",
    download_url="http://sourceforge.net/projects/hamsimanager/files/",
    license="GPLv3",
    options={"build_exe": {"includes": includes,
                           "excludes": excludes,
                           "packages": packages,
                           "path": path,
                           "include_files": include_files,
    }
    },
    executables=[MainExe],
    data_files=data_files,
    requires=['PyQt4', 'cx_Freeze']
)

