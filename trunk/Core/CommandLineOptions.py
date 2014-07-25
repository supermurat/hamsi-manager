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

import sys
from optparse import OptionParser, OptionGroup
import logging
from Core import Universals as uni
import FileUtils as fu


myArgvs = []
isQuickMake = False
QuickMakeParameters = []
parser = None
optionList = None

def checkCommandLineOptions():
    global isQuickMake, QuickMakeParameters, myArgvs, parser, optionList
    myArgvs = sys.argv
    isDontRun = False
    optionList = []
    parser = OptionParser(
        usage="%prog [options] [<arg1>...]", version="HamsiManager " + uni.version,

        epilog="""\
Copyright (c) 2010 - 2014 Murat Demir <mopened@gmail.com> ,
HamsiManager is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.""")
    parser.add_option('-d', '--debug', help='Enable debugging output. '
                                            'Chatty', action='store_const', const=logging.DEBUG,
                      dest='loggingLevel')
    optionList.append("d")
    optionList.append("debug")
    parser.add_option('-v', '--verbose', help='Enable informative output',
                      action='store_const', const=logging.INFO,
                      dest='loggingLevel')
    optionList.append("v")
    optionList.append("verbose")
    parser.add_option('--directory',
                      help='The current directory path. '
                           'Example : /home/yourname/someDirectory ')
    optionList.append("directory <directory>")
    parser.add_option('-s', '--sFileName',
                      help='The setting file name(or path). '
                           '"The settings directory path" + "/" + "YourEnteredName" '
                           'Example : enteredName.ini ')
    optionList.append("s <settingFile>")
    optionList.append("sFileName <settingFile>")
    parser.add_option('--sDirectoryPath',
                      help='The settings directory path. '
                           'Example : /home/yourname/.HamsiApps/HamsiManager ')
    optionList.append("sDirectoryPath <settingDirectory>")
    parser.add_option('-t', '--tableType',
                      help='Table Type Name. '
                           'Example : "0" for Folder Table '
                           'Example : "1" for File Table '
                           'Example : "2" for Music Table '
                           'Example : "3" for Subfolder Table '
                           'Example : "4" for Cover Table ')
    optionList.append("t <tableTypeNo>")
    optionList.append("tableType <tableTypeNo>")
    parser.add_option('-f', '--fileReNamerType',
                      help='File Renamer Type. '
                           'Example : "Personal Computer" '
                           'Example : "Web Server" '
                           'Example : "Removable Media" ')
    optionList.append("f <fileReNamerTypeNo>")
    optionList.append("fileReNamerType <fileReNamerTypeNo>")
    qmgroup = OptionGroup(parser, "Quick Make Options",
                          "You can make quickly what are you want.")
    qmgroup.add_option('--qmw',
                       help='Are you want to show Quick Make Window. '
                            'Example : "1" or "True" for Yes '
                            'Example : "0" or "False" for No ')
    optionList.append("qmw <o>")
    qmgroup.add_option('--qm', help='Are you want to run Quick Make by some parameters?',
                       action='store_const', const=True)
    optionList.append("qm")
    qmgroup.add_option('--configurator', help='Open Hamsi Manager Configurator', action='store_const', const=True)
    optionList.append("configurator")
    qmgroup.add_option('--plugins', help='Show plugins', action='store_const', const=True)
    optionList.append("plugins")
    qmgroup.add_option('--pack',
                       help='The directory path. '
                            'Example : /home/yourname/someDirectory')
    optionList.append("pack <directory>")
    qmgroup.add_option('--hash',
                       help='The file path. '
                            'Example : /home/yourname/someFile')
    optionList.append("hash <file>")
    qmgroup.add_option('--checkIcon',
                       help='The directory path. '
                            'Example : /home/yourname/someDirectory')
    optionList.append("checkIcon <directory>")
    qmgroup.add_option('--clearEmptyDirectories',
                       help='The directory path. '
                            'Example : /home/yourname/someDirectory')
    optionList.append("clearEmptyDirectories <directory>")
    qmgroup.add_option('--clearUnneededs',
                       help='The directory path. '
                            'Example : /home/yourname/someDirectory')
    optionList.append("clearUnneededs <directory>")
    qmgroup.add_option('--clearIgnoreds',
                       help='The directory path. '
                            'Example : /home/yourname/someDirectory')
    optionList.append("clearIgnoreds <directory>")
    qmgroup.add_option('--emendFile',
                       help='The file path. '
                            'Example : /home/yourname/someFile')
    optionList.append("emendFile <file>")
    qmgroup.add_option('--emendDirectory',
                       help='The directory path. '
                            'Example : /home/yourname/someDirectory')
    optionList.append("emendDirectory <directory>")
    qmgroup.add_option('--emendDirectoryWithContents',
                       help='The directory path. '
                            'Example : /home/yourname/someDirectory')
    optionList.append("emendDirectoryWithContents <directory>")
    qmgroup.add_option('--copyPath',
                       help='The file/directory path. '
                            'Example : /home/yourname/somePath')
    optionList.append("copyPath <fileOrDirectory>")
    qmgroup.add_option('--fileTree',
                       help='The directory path. '
                            'Example : /home/yourname/someDirectory')
    optionList.append("fileTree <directory>")
    qmgroup.add_option('--removeOnlySubFiles',
                       help='The directory path. '
                            'Example : /home/yourname/someDirectory')
    optionList.append("removeOnlySubFiles <directory>")
    qmgroup.add_option('--clear',
                       help='The directory path. '
                            'Example : /home/yourname/someDirectory')
    optionList.append("clear <directory>")
    qmgroup.add_option('--textCorrector',
                       help='The file path. '
                            'Example : /home/yourname/someFile')
    optionList.append("textCorrector <file>")
    qmgroup.add_option('--search',
                       help='The file/directory path. '
                            'Example : /home/yourname/somePath')
    optionList.append("search <fileOrDirectory>")
    dgroup = OptionGroup(parser, "Dangerous Options",
                         "Caution: use these options at your own risk.  "
                         "It is believed that some of them bite.")
    dgroup.add_option('--runAsRoot', help='Are you want to run as root?',
                      action='store_const', const=True)
    optionList.append("runAsRoot")
    optionList.append("+[optionalFileOrDirectory]")
    parser.add_option_group(qmgroup)
    parser.add_option_group(dgroup)
    parser.set_defaults(loggingLevel=logging.WARNING, runAsRoot=False, qm=False, plugins=False)
    options, remainderParameters = parser.parse_args()
    if len(remainderParameters) == 1:
        try:
            uni.setMySetting("lastDirectory", uni.trDecode(str(remainderParameters[0]), fu.defaultFileSystemEncoding))
        except:
            uni.setMySetting("lastDirectory", str(remainderParameters[0]))
    if options.directory:
        try:
            uni.setMySetting("lastDirectory", uni.trDecode(str(options.directory), fu.defaultFileSystemEncoding))
        except:
            uni.setMySetting("lastDirectory", str(options.directory))
    if options.loggingLevel:
        uni.loggingLevel = options.loggingLevel
    if options.sFileName:
        uni.fileOfSettings = options.sFileName
    if options.sDirectoryPath:
        uni.setPathOfSettingsDirectory(options.sDirectoryPath)
    if options.tableType:
        import Tables

        uni.setMySetting("tableType", Tables.Tables.getThisTableType(options.tableType))
    if options.fileReNamerType:
        uni.setMySetting("fileReNamerType", options.fileReNamerType)
    if options.qm:
        if options.qmw:
            if options.qmw.lower() == "false" or options.qmw == "0":
                uni.setMySetting("isShowQuickMakeWindow", False)
            else:
                uni.setMySetting("isShowQuickMakeWindow", True)
        if options.configurator:
            QuickMakeParameters.append("configurator")
            isQuickMake = True
        elif options.plugins:
            QuickMakeParameters.append("plugins")
            isQuickMake = True
        elif options.pack:
            QuickMakeParameters.append("pack")
            QuickMakeParameters.append(options.pack)
            isQuickMake = True
        elif options.hash:
            QuickMakeParameters.append("hash")
            QuickMakeParameters.append(options.hash)
            isQuickMake = True
        elif options.checkIcon:
            QuickMakeParameters.append("checkIcon")
            QuickMakeParameters.append(options.checkIcon)
            isQuickMake = True
        elif options.clearEmptyDirectories:
            QuickMakeParameters.append("clearEmptyDirectories")
            QuickMakeParameters.append(options.clearEmptyDirectories)
            isQuickMake = True
        elif options.clearUnneededs:
            QuickMakeParameters.append("clearUnneededs")
            QuickMakeParameters.append(options.clearUnneededs)
            isQuickMake = True
        elif options.clearIgnoreds:
            QuickMakeParameters.append("clearIgnoreds")
            QuickMakeParameters.append(options.clearIgnoreds)
            isQuickMake = True
        elif options.emendFile:
            QuickMakeParameters.append("emendFile")
            QuickMakeParameters.append(options.emendFile)
            isQuickMake = True
        elif options.emendDirectory:
            QuickMakeParameters.append("emendDirectory")
            QuickMakeParameters.append(options.emendDirectory)
            isQuickMake = True
        elif options.emendDirectoryWithContents:
            QuickMakeParameters.append("emendDirectoryWithContents")
            QuickMakeParameters.append(options.emendDirectoryWithContents)
            isQuickMake = True
        elif options.copyPath:
            QuickMakeParameters.append("copyPath")
            QuickMakeParameters.append(options.copyPath)
            isQuickMake = True
        elif options.fileTree:
            QuickMakeParameters.append("fileTree")
            QuickMakeParameters.append(options.fileTree)
            isQuickMake = True
        elif options.removeOnlySubFiles:
            QuickMakeParameters.append("removeOnlySubFiles")
            QuickMakeParameters.append(options.removeOnlySubFiles)
            isQuickMake = True
        elif options.clear:
            QuickMakeParameters.append("clear")
            QuickMakeParameters.append(options.clear)
            isQuickMake = True
        elif options.textCorrector:
            QuickMakeParameters.append("textCorrector")
            QuickMakeParameters.append(options.textCorrector)
            isQuickMake = True
        elif options.search:
            QuickMakeParameters.append("search")
            QuickMakeParameters.append(options.search)
            isQuickMake = True
        QuickMakeParameters.append(remainderParameters)
    if options.runAsRoot:
        from Core import Execute

        if uni.isRunningAsRoot() is False:
            strArgvs = []
            for tempArg in sys.argv:
                if (tempArg.find("-runAsRoot") == -1 and
                    tempArg.find(Execute.findExecutablePath("HamsiManager")) == -1 and
                    tempArg != "./" + Execute.findExecutableBaseName("HamsiManager") and
                    tempArg != Execute.findExecutableBaseName("HamsiManager")):
                    strArgvs.append(tempArg)
            if Execute.executeAsRootWithThread(strArgvs, "HamsiManager"):
                isDontRun = True
    if isDontRun:
        return False
    return True

