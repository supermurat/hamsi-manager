#!/usr/bin/env python
## This file is part of HamsiManager.
## 
## Copyright (c) 2010 - 2013 Murat Demir <mopened@gmail.com>      
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
try:
    if float(sys.version[:3]) < 3.0:
        reload(sys)
        sys.setdefaultencoding("utf-8")
except:
    pass

from Core import RoutineChecks
if RoutineChecks.checkMandatoryModules():
    from Core.MyObjects import *
    import FileUtils as fu
    fu.initStartupVariables()
    from Core import Variables
    from Core import Universals
    Universals.printForDevelopers("Before Universals.setPaths")
    Universals.printForDevelopers("Before RoutineChecks.checkParameters")
    if RoutineChecks.checkParameters():
        Universals.printForDevelopers("Before Settings")
        from Core import Settings
        Universals.printForDevelopers("Before Settings.checkSettings")
        Settings.checkSettings()
        Universals.printForDevelopers("Before Universals.fillMySettings")
        Universals.fillMySettings()
        if isActivePyKDE4:
            Universals.printForDevelopers("ActivePyKDE4")
            appName = "HamsiManager"
            programName = ki18n("Hamsi Manager")
            version = Variables.version
            license = MAboutData.License_GPL_V3
            copyright = ki18n(trForUI("Murat Demir (mopened@gmail.com)"))
            kde4LangCode = (str(MLocale(Variables.Catalog).language()) + "_" +
                            str(MLocale(Variables.Catalog).country()).upper())
            text = ki18n(trForUI(""))
            homePage = trForUI("hamsiapps.com")
            bugEmail = trForUI("Murat Demir (mopened@gmail.com)")
            if fu.isFile(fu.joinPath(fu.HamsiManagerDirectory, "Languages", "About_" + kde4LangCode)):
                aboutFileContent = fu.readFromFile(fu.joinPath(fu.HamsiManagerDirectory, "Languages", "About_"+ kde4LangCode), "utf-8")
            else:
                aboutFileContent = fu.readFromFile(fu.joinPath(fu.HamsiManagerDirectory, "Languages", "About_en_GB"), "utf-8")
            description = ki18n(trForUI(aboutFileContent))
            Universals.printForDevelopers("Before MAboutData")
            aboutOfHamsiManager = MAboutData(appName, Variables.Catalog, programName, version, description,
                                    license, copyright, text, homePage, bugEmail)
            aboutOfHamsiManager.addAuthor(ki18n(trForUI("Murat Demir")), ki18n(trForUI("Project Manager and Developer")),
                                "mopened@gmail.com", "hamsiapps.com")
            aboutOfHamsiManager.setProgramIconName(trForUI(fu.joinPath(fu.themePath, "Images", "hamsi.png")))
            if fu.isFile(fu.joinPath(fu.HamsiManagerDirectory, "Languages", "License_"+ kde4LangCode)):
                aboutOfHamsiManager.addLicenseTextFile(trForUI(fu.joinPath(fu.HamsiManagerDirectory, "Languages", "License_"+ kde4LangCode)))
            else:
                aboutOfHamsiManager.addLicenseTextFile(trForUI(fu.joinPath(fu.HamsiManagerDirectory, "Languages", "License_en_GB")))
            Universals.printForDevelopers("Before MCmdLineArgs")
            MCmdLineArgs.init(sys.argv, aboutOfHamsiManager)
            options = MCmdLineOptions()
            for x in RoutineChecks.optionList:
                options.add(x, ki18n(x + " For Only PyKDE4 Requirement"))
            MCmdLineArgs.addCmdLineOptions(options)
            Universals.printForDevelopers("Before MApplication")
            HamsiManagerApp = MApplication()
            kde4LangCode = str(MGlobal.locale().language())
            if len(kde4LangCode) != 5: kde4LangCode += "_"+str(MGlobal.locale().country()).upper()
            if Variables.getInstalledLanguagesCodes().count(kde4LangCode)==0:
                for lcode in Variables.getInstalledLanguagesCodes():
                    if lcode.find(kde4LangCode[:2]) != -1:
                        kde4LangCode = lcode
            kconf = MGlobal.config()
            MGlobal.locale().setLanguage(kde4LangCode, kconf)
            if fu.isFile(fu.joinPath(fu.HamsiManagerDirectory, "Languages", "HamsiManager_"+kde4LangCode+".qm")):
                languageFile = MTranslator()
                languageFile.load(trForUI(fu.joinPath(fu.HamsiManagerDirectory, "Languages", "HamsiManager_"+kde4LangCode+".qm")))
                HamsiManagerApp.installTranslator(languageFile)
            Variables.aboutOfHamsiManager = aboutOfHamsiManager
        else:
            Universals.printForDevelopers("NotActivePyKDE4")
            HamsiManagerApp = MApplication(sys.argv)  
            if fu.isFile(fu.joinPath(fu.HamsiManagerDirectory, "Languages", "About_"+ Universals.MySettings["language"])):
                aboutFileContent = fu.readFromFile(fu.joinPath(fu.HamsiManagerDirectory, "Languages", "About_"+ Universals.MySettings["language"]), "utf-8")
            else:
                aboutFileContent = fu.readFromFile(fu.joinPath(fu.HamsiManagerDirectory, "Languages", "About_en_GB"), "utf-8")
            Variables.aboutOfHamsiManager = trForUI(aboutFileContent)
            if fu.isFile(fu.joinPath(fu.HamsiManagerDirectory, "Languages", "HamsiManagerWithQt_"+Universals.MySettings["language"]+".qm")):
                languageFile = MTranslator()
                languageFile.load(trForUI(fu.joinPath(fu.HamsiManagerDirectory, "Languages", "HamsiManagerWithQt_"+Universals.MySettings["language"]+".qm")))
                HamsiManagerApp.installTranslator(languageFile)
            elif fu.isFile(fu.joinPath(fu.HamsiManagerDirectory, "Languages", "HamsiManager_"+Universals.MySettings["language"]+".qm")):
                languageFile = MTranslator()
                languageFile.load(trForUI(fu.joinPath(fu.HamsiManagerDirectory, "Languages", "HamsiManager_"+Universals.MySettings["language"]+".qm")))
                HamsiManagerApp.installTranslator(languageFile)
        Universals.printForDevelopers("Before MTextCodec setCodecFor..")
        HamsiManagerApp.setApplicationName("HamsiManager")
        HamsiManagerApp.setApplicationVersion(Variables.version)
        HamsiManagerApp.setOrganizationDomain("hamsiapps.com")
        HamsiManagerApp.setOrganizationName("Hamsi Apps")
        MApplication.setQuitOnLastWindowClosed(True)
        MDir.setSearchPaths("Images", MStringList(trForUI(fu.joinPath(fu.themePath, "Images"))))
        MDir.setSearchPaths("root", MStringList(trForUI(fu.HamsiManagerDirectory)))
        if fu.isFile(fu.joinPath(fu.themePath, "Style.qss")):
            HamsiManagerApp.setStyleSheet(fu.readFromFile(fu.joinPath(fu.themePath, "Style.qss")))
        HamsiManagerApp.setWindowIcon(MIcon("Images:hamsi.png"))
        if Universals.MySettings["applicationStyle"]!="":
            MApplication.setStyle(Universals.MySettings["applicationStyle"])
        if isActivePyKDE4:
            if fu.isFile(Universals.MySettings["colorSchemes"]):
                config = MSharedConfig.openConfig(Universals.MySettings["colorSchemes"])
                plt = MGlobalSettings.createApplicationPalette(config)
            else:
                plt = MApplication.desktop().palette()
            MApplication.setPalette(plt)
        Universals.printForDevelopers("Before RoutineChecks.checkMyModules")
        if RoutineChecks.checkMyModules(HamsiManagerApp):
            RoutineChecks.checkWindowMode()
            if RoutineChecks.isQuickMake:
                Universals.printForDevelopers("QuickMake")
                try:
                    Universals.setApp(HamsiManagerApp)
                    from Core import QuickMake
                    quickMake = QuickMake.QuickMake()
                    if RoutineChecks.isQuickMake:
                        res = HamsiManagerApp.exec_()
                        Universals.saveSettings()
                        Universals.printForDevelopers("Shutting down, result %d" % res)
                except:
                    from Core import ReportBug
                    ReportBug.ReportBug()
                    res = HamsiManagerApp.exec_()
                    Universals.printForDevelopers("Shutting down, result %d" % res)
            if RoutineChecks.isQuickMake == False:
                Universals.printForDevelopers("NotQuickMake")
                import SpecialTools
                import Tables
                from Core import FileManager
                import Bars
                from Bars import TableToolsBar, ToolsBar, StatusBar, MenuBar
                Universals.printForDevelopers("After Modules")
                try:
                    class Main(MMainWindow):
                        def __init__(self):
                            MMainWindow.__init__(self, None)
                            Universals.printForDevelopers("Started __init__")
                            self.setObjectName("RealMainWindow")
                            Universals.setApp(HamsiManagerApp)
                            Universals.setMainWindow(self)
                            self.isLockedMainForm = False
                            self.Menu = None
                            self.Table = None
                            self.CentralWidget = MWidget()
                            self.createMainLayout()
                            Universals.printForDevelopers("Before Bars.Bars")
                            self.Bars = Bars.Bars()
                            Universals.printForDevelopers("Before Bars.StatusBar")
                            self.StatusBar = StatusBar.StatusBar(self)
                            Universals.printForDevelopers("Before Bars.MenuBar")
                            self.Menu = MenuBar.MenuBar(self)
                            Universals.printForDevelopers("Before Bars.ToolsBar")
                            self.ToolsBar = ToolsBar.ToolsBar(self)
                            Universals.printForDevelopers("Before Bars.TableToolsBar")
                            self.TableToolsBar = TableToolsBar.TableToolsBar(self)
                            Universals.printForDevelopers("Before Bars.refreshBars")
                            self.Bars.refreshBars()
                            Universals.printForDevelopers("Before FileManager.FileManager")
                            self.FileManager = FileManager.FileManager(self)
                            Universals.printForDevelopers("After FileManager.FileManager")
                            self.setMainLayout()
                            self.setCentralWidget(self.CentralWidget)
                            self.setMenuBar(self.Menu)
                            self.setStatusBar(self.StatusBar)
                            Universals.printForDevelopers("Before Menu.refreshForTableType")
                            self.Menu.refreshForTableType()
                            Universals.printForDevelopers("Before Bars.getAllBarsStyleFromMySettings")
                            self.Bars.getAllBarsStyleFromMySettings()
                            self.setCorner(Mt.TopLeftCorner, Mt.LeftDockWidgetArea)
                            self.setCorner(Mt.BottomLeftCorner, Mt.LeftDockWidgetArea)
                            Universals.printForDevelopers("End of __init__")
                            
                        def createMainLayout(self):
                            self.MainLayout = MVBoxLayout()
                            
                        def setMainLayout(self):
                            self.CentralWidget.setLayout(self.MainLayout)
                            
                        def resetCentralWidget(self):
                            Universals.clearAllChilds(self.CentralWidget)
                            self.MainLayout = self.CentralWidget.layout()
                            if self.MainLayout is None:
                                self.createMainLayout()
                                self.setMainLayout()
                            
                        def lockForm(self):
                            self.CentralWidget.setEnabled(False)
                            for wid in self.findChildren(MDockWidget):
                                wid.setEnabled(False)
                            for wid in self.findChildren(MToolBar):
                                wid.setEnabled(False)
                            for wid in self.findChildren(MMenuBar):
                                wid.setEnabled(False)
                            self.isLockedMainForm = True
                            
                        def unlockForm(self):
                            self.CentralWidget.setEnabled(True)
                            for wid in self.findChildren(MDockWidget):
                                wid.setEnabled(True)
                            for wid in self.findChildren(MToolBar):
                                wid.setEnabled(True)
                            for wid in self.findChildren(MMenuBar):
                                wid.setEnabled(True)
                            self.isLockedMainForm = False
                            
                        def closeEvent(self, _event):
                            try:
                                if Universals.isRaisedAnError==False:
                                    if Universals.isContinueThreadAction():
                                        Universals.cancelThreadAction()
                                        _event.ignore()
                                Universals.isStartedCloseProcess = True
                                Universals.printForDevelopers("Started closeEvent")
                                MApplication.setQuitOnLastWindowClosed(True)
                                try:self.PlayerBar.MusicPlayer.stop()
                                except:pass
                                from Core import ReportBug, Records
                                from Details import MusicDetails, TextDetails, CoverDetails
                                MusicDetails.MusicDetails.closeAllMusicDialogs()
                                TextDetails.TextDetails.closeAllTextDialogs()
                                CoverDetails.CoverDetails.closeAllCoverDialogs()
                                Universals.printForDevelopers("Closed Dialogs")
                                if Universals.isRaisedAnError==False:
                                    if self.Table.checkUnSavedValues()==False:
                                        Universals.isStartedCloseProcess=False
                                        Universals.printForDevelopers("Close ignored")
                                        _event.ignore() 
                                Universals.printForDevelopers("Before RoutineChecks.checkBeforeCloseProcess")
                                if RoutineChecks.checkBeforeCloseProcess()==False:
                                    _event.ignore()
                                    return None
                                Universals.printForDevelopers("After RoutineChecks.checkBeforeCloseProcess")
                                if isActivePyKDE4:
                                    Universals.printForDevelopers("Before Save KDE Configs")
                                    kconf = MGlobal.config()
                                    kconfGroup = MConfigGroup(kconf,"DirectoryOperator")
                                    self.FileManager.dirOperator.writeConfig(kconfGroup)
                                    self.FileManager.actCollection.writeSettings(kconfGroup)
                                    Universals.printForDevelopers("After Save KDE Configs")
                                Universals.printForDevelopers("Before Save Configs")
                                Universals.setMySetting(self.Table.SubTable.hiddenTableColumnsSettingKey,self.Table.hiddenTableColumns)
                                self.Bars.setAllBarsStyleToMySettings()
                                Records.setRecordType(1)
                                subFixForStateFile = ""
                                if Universals.windowMode!=Variables.windowModeKeys[0]:
                                    subFixForStateFile = Universals.windowMode
                                fu.writeToBinaryFile(fu.joinPath(fu.pathOfSettingsDirectory, "LastState" + subFixForStateFile), self.saveState())
                                Records.restoreRecordType()
                                geometry = [self.geometry().x(), self.geometry().y(), self.geometry().width(), self.geometry().height()]
                                Universals.setMySetting("MainWindowGeometries", geometry)
                                Universals.setMySetting("lastDirectory",self.FileManager.currentDirectory)
                                Universals.setMySetting("isMainWindowMaximized",self.isMaximized())
                                Universals.setMySetting("isShowAdvancedSelections",self.SpecialTools.isShowAdvancedSelections)
                                if Universals.tableType in ["2", "6", "8", "9"]:
                                    try:Universals.setMySetting("isPlayNow",self.Table.SubTable.isPlayNow.isChecked())
                                    except:pass
                                Universals.setMySetting("tableType", Universals.tableType)
                                Universals.setMySetting("activeTabNoOfSpecialTools", self.SpecialTools.tabwTabs.currentIndex())
                                Universals.saveSettings()
                                Settings.saveUniversalSettings()
                                if Variables.isActiveAmarok and Universals.getBoolValue("amarokIsUseHost")==False:
                                    import Amarok
                                    Amarok.stopEmbeddedDB()
                                Universals.printForDevelopers("After Save Configs")
                                Universals.printForDevelopers("Before RoutineChecks.checkAfterCloseProcess")
                                RoutineChecks.checkAfterCloseProcess()
                                Universals.printForDevelopers("After RoutineChecks.checkAfterCloseProcess")
                            except:
                                from Core import ReportBug
                                if ReportBug.isClose==False:
                                    ReportBug.ReportBug()
                                    _event.ignore()
                    
                    Universals.printForDevelopers("Before Main")
                    MainWindow=Main()
                    Universals.printForDevelopers("After Main")
                    if str(MainWindow.windowTitle()) == "":
                        MainWindow.setWindowTitle("Hamsi Manager "+ Variables.version)
                    if isActivePyKDE4:
                        Universals.printForDevelopers("Before MGlobal.config")
                        kconf = MGlobal.config()
                        kconfGroup = MConfigGroup(kconf,"Universals")
                        MainWindow.setAutoSaveSettings(kconfGroup)
                        Universals.printForDevelopers("After MGlobal.config")
                    else:
                        try:
                            Universals.printForDevelopers("Before MainWindow.restoreState")
                            state = MByteArray()
                            subFixForStateFile = ""
                            if Universals.windowMode!=Variables.windowModeKeys[0]:
                                subFixForStateFile = Universals.windowMode
                            state.append(fu.readFromBinaryFile(fu.joinPath(fu.pathOfSettingsDirectory, "LastState" + subFixForStateFile)))
                            MainWindow.restoreState(state)
                            Universals.printForDevelopers("After MainWindow.restoreState")
                        except:pass
                    Universals.printForDevelopers("Before Show")
                    if Universals.getBoolValue("isMainWindowMaximized"):
                        MainWindow.showMaximized()
                    else:
                        geometries = Universals.getListValue("MainWindowGeometries")
                        MainWindow.setGeometry(int(geometries[0]),int(geometries[1]), int(geometries[2]),int(geometries[3]))
                        MainWindow.show()
                    Universals.printForDevelopers("Before RoutineChecks.checkAfterRunProcess")
                    RoutineChecks.checkAfterRunProcess()
                    Universals.printForDevelopers("After RoutineChecks.checkAfterRunProcess")
                    Universals.setMySetting("isMakeAutoDesign", "False")
                    Universals.isStartingSuccessfully = True
                    Universals.isCanBeShowOnMainWindow = True
                except:
                    from Core import ReportBug
                    ReportBug.ReportBug()
                res = None
                try:
                    Universals.printForDevelopers("Before HamsiManagerApp.exec_")
                    res = HamsiManagerApp.exec_()
                    Universals.printForDevelopers("Shutting down, result %d" % res)
                    sys.exit(res)
                except Exception as err:
                    from Core import ReportBug
                    error = ReportBug.ReportBug()
                    print (str(translate("ReportBug", "A critical error has occurred.If you want to look into details \"%s\" you can see the file.If possible, we ask you to send us this error details." )) % (error.pathOfReportFile))
                    print (str(translate("ReportBug", "Thanks in advance for your interest.")))
                    print ("Shutting down, result %d" % res)
                    raise err
                    
sys.exit()

