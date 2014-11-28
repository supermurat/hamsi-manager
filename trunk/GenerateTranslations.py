#!/usr/bin/env python
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

# This script requires "pylupdate4" (python-qt4-devel) and "lrelease".

import sys

try:
    if float(sys.version[:3]) < 3.0:
        reload(sys)
        sys.setdefaultencoding("utf-8")
except:
    pass

import Core

if Core.checkMandatoryModules():
    from Core.MyObjects import *
    import FileUtils as fu

    fu.initStartupVariables()
    from Core import Universals as uni
    from Core import Execute

    proFile = fu.joinPath(fu.HamsiManagerDirectory, "HamsiManager.pro")
    proFileContent = "SOURCES = %SOURCES% \nTRANSLATIONS = %TRANSLATIONS%"""

    SOURCES = ""
    TRANSLATIONS = ""
    directoriesAndFiles = fu.readDirectoryWithSubDirectories(fu.HamsiManagerDirectory)
    for fileName in directoriesAndFiles:
        if (fu.isFile(fileName) and fileName.find(".py") > -1 and
                    fileName.find(".pyc") == -1 and fileName.find(".pyw") == -1):
            SOURCES += fileName.replace(fu.HamsiManagerDirectory + fu.sep, "") + " \\\n         "

    for fileName in ["Languages" + fu.sep + "HamsiManager_tr_TR.ts",
                     "Languages" + fu.sep + "HamsiManager_untranslated.ts"]:
        TRANSLATIONS += fileName + " \\\n         "

    proFileContent = proFileContent.replace("%SOURCES%", SOURCES)
    proFileContent = proFileContent.replace("%TRANSLATIONS%", TRANSLATIONS)

    fu.writeToFile(proFile, proFileContent)

    args = ["pylupdate4"]
    #args.append("-noobsolete") # Uncomment me if you want to remove old translations from .ts files.
    args.append("-verbose")
    args.append(proFile)

    print (Execute.getCommandResult(args, fu.HamsiManagerDirectory))

    proFileContent = proFileContent.replace("Languages" + fu.sep + "HamsiManager_untranslated.ts \\\n         ", "")
    fu.writeToFile(proFile, proFileContent)

    args = ["lrelease"]
    args.append("-compress")
    args.append(proFile)
    print (Execute.getCommandResult(args, fu.HamsiManagerDirectory))

    print ("Translation files have been updated successfully.")



