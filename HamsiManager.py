#!/usr/bin/env python
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

    uni.printForDevelopers("Before CommandLineOptions")
    from Core import CommandLineOptions
    uni.printForDevelopers("Before CommandLineOptions.checkCommandLineOptions")
    if CommandLineOptions.checkCommandLineOptions():
        from Core import ReportBug

        uni.printForDevelopers("Before Settings")
        from Core import Settings

        uni.printForDevelopers("Before Settings.checkSettings")
        Settings.checkSettings()
        uni.printForDevelopers("Before uni.fillMySettings")
        uni.fillMySettings()
        if isActivePyKDE4:
            uni.printForDevelopers("ActivePyKDE4")
            appName = "HamsiManager"
            programName = ki18n("Hamsi Manager")
            version = uni.version
            appLicense = MAboutData.License_GPL_V3
            appCopyright = ki18n(str("Murat Demir (mopened@gmail.com)"))
            kde4LangCode = (str(MLocale(uni.Catalog).language()) + "_" +
                            str(MLocale(uni.Catalog).country()).upper())
            text = ki18n(str(""))
            homePage = str("hamsiapps.com")
            bugEmail = str("Murat Demir (mopened@gmail.com)")
            if fu.isFile(fu.joinPath(fu.HamsiManagerDirectory, "Languages", "About_" + kde4LangCode)):
                aboutFileContent = fu.readFromFile(
                    fu.joinPath(fu.HamsiManagerDirectory, "Languages", "About_" + kde4LangCode), "utf-8")
            else:
                aboutFileContent = fu.readFromFile(fu.joinPath(fu.HamsiManagerDirectory, "Languages", "About_en_GB"),
                                                   "utf-8")
            description = ki18n(str(aboutFileContent))
            uni.printForDevelopers("Before MAboutData")
            aboutOfHamsiManager = MAboutData(appName, uni.Catalog, programName, version, description,
                                             appLicense, appCopyright, text, homePage, bugEmail)
            aboutOfHamsiManager.addAuthor(ki18n(str("Murat Demir")), ki18n(str("Project Manager and Developer")),
                                          "mopened@gmail.com", "hamsiapps.com")
            aboutOfHamsiManager.setProgramIconName(str(fu.joinPath(fu.themePath, "Images", "hamsi.png")))
            if fu.isFile(fu.joinPath(fu.HamsiManagerDirectory, "Languages", "License_" + kde4LangCode)):
                aboutOfHamsiManager.addLicenseTextFile(
                    str(fu.joinPath(fu.HamsiManagerDirectory, "Languages", "License_" + kde4LangCode)))
            else:
                aboutOfHamsiManager.addLicenseTextFile(
                    str(fu.joinPath(fu.HamsiManagerDirectory, "Languages", "License_en_GB")))
            uni.printForDevelopers("Before MCmdLineArgs")
            MCmdLineArgs.init(sys.argv, aboutOfHamsiManager)
            options = MCmdLineOptions()
            for x in CommandLineOptions.optionList:
                options.add(x, ki18n(x + " For Only PyKDE4 Requirement"))
            MCmdLineArgs.addCmdLineOptions(options)
            uni.printForDevelopers("Before MApplication")
            HamsiManagerApp = MApplication()
            kde4LangCode = str(MGlobal.locale().language())
            if len(kde4LangCode) != 5: kde4LangCode += "_" + str(MGlobal.locale().country()).upper()
            if uni.getInstalledLanguagesCodes().count(kde4LangCode) == 0:
                for lcode in uni.getInstalledLanguagesCodes():
                    if lcode.find(kde4LangCode[:2]) != -1:
                        kde4LangCode = lcode
            kconf = MGlobal.config()
            MGlobal.locale().setLanguage(kde4LangCode, kconf)
            if fu.isFile(fu.joinPath(fu.HamsiManagerDirectory, "Languages", "HamsiManager_" + kde4LangCode + ".qm")):
                languageFile = MTranslator()
                languageFile.load(
                    str(fu.joinPath(fu.HamsiManagerDirectory, "Languages", "HamsiManager_" + kde4LangCode + ".qm")))
                HamsiManagerApp.installTranslator(languageFile)
            uni.aboutOfHamsiManager = aboutOfHamsiManager
        else:
            uni.printForDevelopers("NotActivePyKDE4")
            HamsiManagerApp = MApplication(sys.argv)
            if fu.isFile(fu.joinPath(fu.HamsiManagerDirectory, "Languages", "About_" + uni.MySettings["language"])):
                aboutFileContent = fu.readFromFile(
                    fu.joinPath(fu.HamsiManagerDirectory, "Languages", "About_" + uni.MySettings["language"]), "utf-8")
            else:
                aboutFileContent = fu.readFromFile(fu.joinPath(fu.HamsiManagerDirectory, "Languages", "About_en_GB"),
                                                   "utf-8")
            uni.aboutOfHamsiManager = str(aboutFileContent)
            if fu.isFile(fu.joinPath(fu.HamsiManagerDirectory,
                                     "Languages", "Qt_" + uni.MySettings["language"] + ".qm")):
                languageFileQt = MTranslator()
                languageFileQt.load(str(fu.joinPath(fu.HamsiManagerDirectory,
                                                  "Languages", "Qt_" + uni.MySettings["language"] + ".qm")))
                HamsiManagerApp.installTranslator(languageFileQt)
            if fu.isFile(fu.joinPath(fu.HamsiManagerDirectory,
                                     "Languages", "HamsiManager_" + uni.MySettings["language"] + ".qm")):
                languageFile = MTranslator()
                languageFile.load(str(fu.joinPath(fu.HamsiManagerDirectory,
                                                  "Languages", "HamsiManager_" + uni.MySettings["language"] + ".qm")))
                HamsiManagerApp.installTranslator(languageFile)
        uni.printForDevelopers("Before MTextCodec setCodecFor..")
        HamsiManagerApp.setApplicationName("HamsiManager")
        HamsiManagerApp.setApplicationVersion(uni.version)
        HamsiManagerApp.setOrganizationDomain("hamsiapps.com")
        HamsiManagerApp.setOrganizationName("Hamsi Apps")
        MApplication.setQuitOnLastWindowClosed(True)
        MDir.setSearchPaths("Images", MStringList(str(fu.joinPath(fu.themePath, "Images"))))
        MDir.setSearchPaths("root", MStringList(str(fu.HamsiManagerDirectory)))
        if fu.isFile(fu.joinPath(fu.themePath, "Style.qss")):
            HamsiManagerApp.setStyleSheet(fu.readFromFile(fu.joinPath(fu.themePath, "Style.qss")))
        HamsiManagerApp.setWindowIcon(MIcon("Images:hamsi.png"))
        if uni.MySettings["applicationStyle"] != "":
            MApplication.setStyle(uni.MySettings["applicationStyle"])
        if isActivePyKDE4:
            if fu.isFile(uni.MySettings["colorSchemes"]):
                config = MSharedConfig.openConfig(uni.MySettings["colorSchemes"])
                plt = MGlobalSettings.createApplicationPalette(config)
            else:
                plt = MApplication.desktop().palette()
            MApplication.setPalette(plt)
        uni.printForDevelopers("Before Core.checkMyModules")
        if Core.checkMyModules(HamsiManagerApp):
            setApplication(HamsiManagerApp)
            if CommandLineOptions.isQuickMake:
                uni.printForDevelopers("QuickMake")
                try:
                    from Core import QuickMake

                    quickMake = QuickMake.QuickMake()
                    if CommandLineOptions.isQuickMake:
                        res = HamsiManagerApp.exec_()
                        uni.saveSettings()
                        uni.printForDevelopers("Shutting down, result %d" % res)
                except:
                    ReportBug.ReportBug()
                    res = HamsiManagerApp.exec_()
                    uni.printForDevelopers("Shutting down, result %d" % res)
            if CommandLineOptions.isQuickMake is False:
                uni.printForDevelopers("NotQuickMake")
                try:
                    uni.printForDevelopers("Before MyMainWindow")
                    from Core import MyMainWindow

                    currentMainWindow = MyMainWindow.MyMainWindow()
                    uni.printForDevelopers("After MyMainWindow")
                    if str(currentMainWindow.windowTitle()) == "":
                        currentMainWindow.setWindowTitle("Hamsi Manager " + uni.version)
                    if isActivePyKDE4:
                        uni.printForDevelopers("Before MGlobal.config")
                        kconf = MGlobal.config()
                        kconfGroup = MConfigGroup(kconf, "Universals")
                        currentMainWindow.setAutoSaveSettings(kconfGroup)
                        uni.printForDevelopers("After MGlobal.config")
                    else:
                        try:
                            uni.printForDevelopers("Before MainWindow.restoreState")
                            state = MByteArray()
                            state.append(fu.readFromBinaryFile(fu.joinPath(fu.pathOfSettingsDirectory, "LastState")))
                            currentMainWindow.restoreState(state)
                            uni.printForDevelopers("After MainWindow.restoreState")
                        except: pass
                    uni.printForDevelopers("Before Show")
                    if uni.getBoolValue("isMainWindowMaximized"):
                        currentMainWindow.showMaximized()
                    else:
                        geometries = uni.getListValue("MainWindowGeometries")
                        currentMainWindow.setGeometry(int(geometries[0]), int(geometries[1]), int(geometries[2]),
                                                      int(geometries[3]))
                        currentMainWindow.show()
                    uni.printForDevelopers("Before # After Run Processes Step 1")
                    currentMainWindow.doAfterRunProcessesStep1()
                    uni.printForDevelopers("After # After Run Processes Step 1")
                    uni.isStartingSuccessfully = True
                    uni.isCanBeShowOnMainWindow = True
                    currentMainWindow.doAfterRunProcessesStep2()
                    uni.printForDevelopers("After # After Run Processes Step 2")
                except:
                    ReportBug.ReportBug()
                res = None
                try:
                    uni.printForDevelopers("Before HamsiManagerApp.exec_")
                    res = HamsiManagerApp.exec_()
                    uni.printForDevelopers("Shutting down, result %d" % res)
                    sys.exit(res)
                except Exception as err:
                    error = ReportBug.ReportBug()
                    print (str(translate("ReportBug",
                                         "A critical error has occurred.If you want to look into details \"%s\" you can see the file.If possible, we ask you to send us this error details.")) % (
                               error.pathOfReportFile))
                    print (str(translate("ReportBug", "Thanks in advance for your interest.")))
                    print ("Shutting down, result %d" % res)
                    raise err

sys.exit()

