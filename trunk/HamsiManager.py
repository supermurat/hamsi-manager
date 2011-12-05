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

import sys
import os
from Core import Variables
try: 
    if Variables.isPython3k==False: 
        reload(sys)
        sys.setdefaultencoding("utf-8")
except:pass
Variables.checkStartupVariables()
from Core import Universals
Universals.printForDevelopers("Before RoutineChecks")
from Core import RoutineChecks
Universals.printForDevelopers("Before RoutineChecks.checkQt4Exist")
if RoutineChecks.checkQt4Exist():
    Universals.printForDevelopers("Before RoutineChecks.checkParameters")
    if RoutineChecks.checkParameters():
        Universals.printForDevelopers("Before Settings")
        from Core import Settings
        Universals.printForDevelopers("Before Settings.checkSettings")
        Settings.checkSettings()
        Universals.printForDevelopers("Before Universals.fillMySettings")
        Universals.fillMySettings()
        Universals.printForDevelopers("Before MyObjects")
        from Core.MyObjects import *
        Universals.printForDevelopers("Before InputOutputs")
        import InputOutputs
        if Universals.isActivePyKDE4==True:
            Universals.printForDevelopers("ActivePyKDE4")
            appName     = "HamsiManager"
            programName = ki18n ("Hamsi Manager")
            version     = Variables.version
            license     = MAboutData.License_GPL_V3
            copyright   = ki18n (trForUI("Murat Demir (mopened@gmail.com)"))
            kde4LangKode = str(KLocale(Variables.Catalog).language())+"_"+str(KLocale(Variables.Catalog).country()).upper()
            text        = ki18n (trForUI(""))
            homePage    = trForUI("hamsiapps.com")
            bugEmail    = trForUI("Murat Demir (mopened@gmail.com)")
            if InputOutputs.isFile(InputOutputs.joinPath(Variables.HamsiManagerDirectory, "Languages", "About_"+ kde4LangKode)):
                aboutFileContent = InputOutputs.readFromFile(InputOutputs.joinPath(Variables.HamsiManagerDirectory, "Languages", "About_"+ kde4LangKode), "utf-8")
            else:
                aboutFileContent = InputOutputs.readFromFile(InputOutputs.joinPath(Variables.HamsiManagerDirectory, "Languages", "About_en_GB"), "utf-8")
            description = ki18n (trForUI(aboutFileContent))
            Universals.printForDevelopers("Before MAboutData")
            aboutOfHamsiManager = MAboutData (appName, Variables.Catalog, programName, version, description,
                                    license, copyright, text, homePage, bugEmail)
            aboutOfHamsiManager.addAuthor (ki18n(trForUI("Murat Demir")), ki18n(trForUI("Project Manager and Developer")), 
                                "mopened@gmail.com", "hamsiapps.com")
            aboutOfHamsiManager.addCredit(ki18n(trForUI("Tolga Balc\xc4\xb1")), ki18n(trForUI("Translate to English. (Voluntary) (V0.7.x)")), 
                                            "tbalci@gmail.com", "http://www.brighthub.com/members/paladin.aspx")
            aboutOfHamsiManager.addCredit(ki18n(trForUI("M\xc3\xa1rcio Moraes")), ki18n(trForUI("Translate to Brazilian Portuguese. (Voluntary) (V0.8.7 - ~)")), 
                                            "", "")
            aboutOfHamsiManager.setProgramIconName(trForM(InputOutputs.joinPath(Universals.themePath, "Images", "HamsiManager-128x128.png")))
            if InputOutputs.isFile(InputOutputs.joinPath(Variables.HamsiManagerDirectory, "Languages", "License_"+ kde4LangKode)):
                aboutOfHamsiManager.addLicenseTextFile(trForM(InputOutputs.joinPath(Variables.HamsiManagerDirectory, "Languages", "License_"+ kde4LangKode)))
            else:
                aboutOfHamsiManager.addLicenseTextFile(trForM(InputOutputs.joinPath(Variables.HamsiManagerDirectory, "Languages", "License_en_GB")))
            Universals.printForDevelopers("Before MCmdLineArgs")
            MCmdLineArgs.init(sys.argv, aboutOfHamsiManager)
            options = MCmdLineOptions()
            for x in RoutineChecks.optionList:
                options.add(x, ki18n(x + " For Only PyKDE4 Requirement"))
            MCmdLineArgs.addCmdLineOptions(options)
            Universals.printForDevelopers("Before MApplication")
            HamsiManagerApp = MApplication()
            kde4LangKode = str(MGlobal.locale().language())
            if len(kde4LangKode)!=5: kde4LangKode += "_"+str(MGlobal.locale().country()).upper()
            if Variables.getInstalledLanguagesCodes().count(kde4LangKode)==0:
                for lcode in Variables.getInstalledLanguagesCodes():
                    if lcode.find(kde4LangKode[:2])!=-1:
                        kde4LangKode = lcode
            kconf = MGlobal.config()
            MGlobal.locale().setLanguage(kde4LangKode, kconf)
            if InputOutputs.isFile(InputOutputs.joinPath(Variables.HamsiManagerDirectory, "Languages", "HamsiManager_"+kde4LangKode+".qm")):
                languageFile = MTranslator()
                languageFile.load(trForM(InputOutputs.joinPath(Variables.HamsiManagerDirectory, "Languages", "HamsiManager_"+kde4LangKode+".qm")))
                HamsiManagerApp.installTranslator(languageFile)
            Variables.aboutOfHamsiManager = aboutOfHamsiManager
        else:
            Universals.printForDevelopers("NotActivePyKDE4")
            HamsiManagerApp = MApplication(sys.argv)  
            if InputOutputs.isFile(InputOutputs.joinPath(Variables.HamsiManagerDirectory, "Languages", "About_"+ Universals.MySettings["language"])):
                aboutFileContent = InputOutputs.readFromFile(InputOutputs.joinPath(Variables.HamsiManagerDirectory, "Languages", "About_"+ Universals.MySettings["language"]), "utf-8")
            else:
                aboutFileContent = InputOutputs.readFromFile(InputOutputs.joinPath(Variables.HamsiManagerDirectory, "Languages", "About_en_GB"), "utf-8")
            Variables.aboutOfHamsiManager = trForUI(aboutFileContent)
            if InputOutputs.isFile(InputOutputs.joinPath(Variables.HamsiManagerDirectory, "Languages", "HamsiManagerWithQt_"+Universals.MySettings["language"]+".qm")):
                languageFile = MTranslator()
                languageFile.load(trForM(InputOutputs.joinPath(Variables.HamsiManagerDirectory, "Languages", "HamsiManagerWithQt_"+Universals.MySettings["language"]+".qm")))
                HamsiManagerApp.installTranslator(languageFile)
            elif InputOutputs.isFile(InputOutputs.joinPath(Variables.HamsiManagerDirectory, "Languages", "HamsiManager_"+Universals.MySettings["language"]+".qm")):
                languageFile = MTranslator()
                languageFile.load(trForM(InputOutputs.joinPath(Variables.HamsiManagerDirectory, "Languages", "HamsiManager_"+Universals.MySettings["language"]+".qm")))
                HamsiManagerApp.installTranslator(languageFile)
        Universals.printForDevelopers("Before MTextCodec setCodecFor..")
        MTextCodec.setCodecForCStrings(MTextCodec.codecForName("utf-8"))
        MTextCodec.setCodecForTr(MTextCodec.codecForName("utf-8"))
        HamsiManagerApp.setApplicationName("HamsiManager")
        HamsiManagerApp.setApplicationVersion(Variables.version)
        HamsiManagerApp.setOrganizationDomain("hamsiapps.com")
        HamsiManagerApp.setOrganizationName("Hamsi Apps")
        MApplication.setQuitOnLastWindowClosed(True)
        MDir.setSearchPaths("Images", MStringList(trForM(InputOutputs.joinPath(Universals.themePath, "Images"))))
        MDir.setSearchPaths("root", MStringList(trForM(Variables.HamsiManagerDirectory)))
        if InputOutputs.isFile(InputOutputs.joinPath(Universals.themePath, "Style.qss")):
            HamsiManagerApp.setStyleSheet(InputOutputs.readFromFile(InputOutputs.joinPath(Universals.themePath, "Style.qss")))
        HamsiManagerApp.setWindowIcon(MIcon("Images:HamsiManager-128x128.png"))
        if Universals.MySettings["applicationStyle"]!="":
            MApplication.setStyle(Universals.MySettings["applicationStyle"])
        if Universals.isActivePyKDE4:
            if InputOutputs.isFile(Universals.MySettings["colorSchemes"]):
                config = MSharedConfig.openConfig(Universals.MySettings["colorSchemes"])
                plt = MGlobalSettings.createApplicationPalette(config)
            else:
                plt = MApplication.desktop().palette()
            MApplication.setPalette(plt)
        Universals.printForDevelopers("Before RoutineChecks.checkMyModules")
        if RoutineChecks.checkMyModules(HamsiManagerApp):
            if RoutineChecks.isQuickMake:
                Universals.printForDevelopers("QuickMake")
                try:
                    Universals.setApp(HamsiManagerApp)
                    Universals.fillUIUniversals()
                    from Core import QuickMake
                    quickMake = QuickMake.QuickMake()
                    if RoutineChecks.isQuickMake:
                        res = HamsiManagerApp.exec_()
                        Universals.printForDevelopers("Shutting down, result %d" % res)
                except:
                    from Core import ReportBug
                    error = ReportBug.ReportBug()
                    error.show()
                    res = HamsiManagerApp.exec_()
                    Universals.printForDevelopers("Shutting down, result %d" % res)
            if RoutineChecks.isQuickMake == False:
                Universals.printForDevelopers("NotQuickMake")
                from Core import SpecialTools
                import Tables
                from Core import FileManager
                from Core import Bars
                Universals.printForDevelopers("After Modules")
                try:
                    class Main(MMainWindow):
                        def __init__(self):
                            MMainWindow.__init__(self, None)
                            Universals.printForDevelopers("Started __init__")
                            self.setObjectName("RealMainWindow")
                            Universals.setApp(HamsiManagerApp)
                            Universals.setMainWindow(self)
                            Universals.fillUIUniversals()
                            self.isLockedMainForm = False
                            self.Menu = None
                            self.CentralWidget = MWidget()
                            self.createMainLayout()
                            Universals.printForDevelopers("Before Bars.Bars")
                            self.Bars = Bars.Bars()
                            Universals.printForDevelopers("Before Bars.StatusBar")
                            self.StatusBar = Bars.StatusBar(self)
                            Universals.printForDevelopers("Before Bars.MenuBar")
                            self.Menu = Bars.MenuBar(self)
                            Universals.printForDevelopers("Before Bars.ToolsBar")
                            self.ToolsBar = Bars.ToolsBar(self)
                            Universals.printForDevelopers("Before Bars.TableToolsBar")
                            self.TableToolsBar = Bars.TableToolsBar(self)
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
                                Universals.isStartedCloseProcces = True
                                Universals.printForDevelopers("Started closeEvent")
                                MApplication.setQuitOnLastWindowClosed(True)
                                try:self.PlayerBar.Player.stop()
                                except:pass
                                from Core import ReportBug, Records
                                from Details import MusicDetails, TextDetails, CoverDetails
                                MusicDetails.closeAllMusicDialogs()
                                TextDetails.closeAllTextDialogs()
                                CoverDetails.closeAllCoverDialogs()
                                Universals.printForDevelopers("Closed Dialogs")
                                if Universals.isRaisedAnError==False:
                                    if self.Table.checkUnSavedValues()==False:
                                        Universals.isStartedCloseProcces=False
                                        Universals.printForDevelopers("Close ignored")
                                        _event.ignore() 
                                if Universals.isActivePyKDE4==True:
                                    Universals.printForDevelopers("Before Save KDE Configs")
                                    kconf = MGlobal.config()
                                    kconfGroup = MConfigGroup(kconf,"DirectoryOperator")
                                    self.FileManager.dirOperator.writeConfig(kconfGroup)
                                    self.FileManager.actCollection.writeSettings(kconfGroup)
                                    Universals.printForDevelopers("After Save KDE Configs")
                                Universals.printForDevelopers("Before Save Configs")
                                Universals.setMySetting(self.Table.SubTable.hiddenTableColumnsSettingKey,self.Table.hiddenTableColumns)
                                self.Bars.setAllBarsStyleToMySettings()
                                if ReportBug.iSClosingInErrorReporting == False:
                                    Records.setRecordType(1)
                                    subFixForStateFile = ""
                                    if Universals.windowMode!=Variables.windowModeKeys[0]:
                                        subFixForStateFile = Universals.windowMode
                                    InputOutputs.writeToBinaryFile(InputOutputs.joinPath(Universals.pathOfSettingsDirectory, "LastState" + subFixForStateFile), self.saveState())
                                    Records.restoreRecordType()
                                    geometri = [self.geometry().x(), self.geometry().y(), self.geometry().width(), self.geometry().height()]
                                    Universals.setMySetting("MainWindowGeometries",geometri)
                                Universals.setMySetting("lastDirectory",self.FileManager.currentDirectory)
                                Universals.setMySetting("isMainWindowMaximized",self.isMaximized())
                                Universals.setMySetting("isShowAdvancedSelections",self.SpecialTools.isShowAdvancedSelections)
                                if Universals.tableType==2:
                                    Universals.setMySetting("isRunOnDoubleClick",self.Table.tbIsRunOnDoubleClick.isChecked())
                                    Universals.setMySetting("isOpenDetailsInNewWindow",self.Table.isOpenDetailsOnNewWindow.isChecked())
                                    Universals.setMySetting("isPlayNow",self.Table.SubTable.isPlayNow.isChecked())
                                Universals.setMySetting("isChangeSelected",Universals.isChangeSelected)
                                Universals.setMySetting("isChangeAll",Universals.isChangeAll)
                                Universals.setMySetting("tableType", Universals.tableType)
                                Universals.setMySetting("activeTabNoOfSpecialTools", self.SpecialTools.tabwTabs.currentIndex())
                                Universals.saveSettings()
                                Settings.saveUniversalSettings()
                                if Universals.getBoolValue("amarokIsUseHost")==False:
                                    import Amarok
                                    Amarok.stopEmbeddedDB()
                                Universals.printForDevelopers("After Save Configs")
                                Universals.printForDevelopers("Before RoutineChecks.checkAfterCloseProccess")
                                RoutineChecks.checkAfterCloseProccess()
                                Universals.printForDevelopers("After RoutineChecks.checkAfterCloseProccess")
                            except:
                                from Core import ReportBug
                                if ReportBug.isClose==False:
                                    error = ReportBug.ReportBug()
                                    error.show()
                                    _event.ignore()
                    
                    Universals.printForDevelopers("Before Main")
                    MainWindow=Main()
                    Universals.printForDevelopers("After Main")
                    MainWindow.setWindowTitle("Hamsi Manager "+ MApplication.applicationVersion())
                    if Universals.isActivePyKDE4==True:
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
                            state.append(InputOutputs.readFromBinaryFile(InputOutputs.joinPath(Universals.pathOfSettingsDirectory, "LastState" + subFixForStateFile)))
                            MainWindow.restoreState(state)
                            Universals.printForDevelopers("After MainWindow.restoreState")
                        except:pass
                    Universals.printForDevelopers("Before Show")
                    if Universals.getBoolValue("isMainWindowMaximized"):
                        MainWindow.showMaximized()
                    else:
                        geometries = Universals.getListFromStrint(Universals.MySettings["MainWindowGeometries"])
                        MainWindow.setGeometry(int(geometries[0]),int(geometries[1]), int(geometries[2]),int(geometries[3]))
                        MainWindow.show()
                    Universals.printForDevelopers("Before RoutineChecks.checkAfterRunProccess")
                    RoutineChecks.checkAfterRunProccess()
                    Universals.printForDevelopers("After RoutineChecks.checkAfterRunProccess")
                    Universals.setMySetting("isMakeAutoDesign", "False")
                    Universals.setMySetting("isShowReconfigureWizard", "False")
                    Universals.isStartingSuccessfully = True
                    Universals.isCanBeShowOnMainWindow = True
                except:
                    from Core import ReportBug
                    error = ReportBug.ReportBug()
                    error.show()
                res = None
                try:
                    Universals.printForDevelopers("Before HamsiManagerApp.exec_")
                    res = HamsiManagerApp.exec_()
                    Universals.printForDevelopers("Shutting down, result %d" % res)
                except Exception as err:
                    from Core import ReportBug
                    error = ReportBug.ReportBug()
                    error.show()
                    print (str(MApplication.translate("ReportBug", "A critical error has occurred.If you want to look into details \"%s\" you can see the file.If possible, we ask you to send us this error details." )) % (error.pathOfReportFile))
                    print (str(MApplication.translate("ReportBug", "Thanks in advance for your interest.")))
                    print ("Shutting down, result %d" % res)
                    raise err
                    
sys.exit()

