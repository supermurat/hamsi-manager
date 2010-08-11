#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
reload(sys)
sys.setdefaultencoding("utf-8")
if sys.path[0]=="":
    sys.path.insert(0, sys.path[1])
sys.path.insert(1,sys.path[0]+"/Core")
sys.path.insert(2,sys.path[0]+"/SearchEngines")

import RoutineChecks
if RoutineChecks.checkPyQt4Exist():
    myUniversals = ""
    if RoutineChecks.checkParameters():
        import Settings
        Settings.checkSettings()
        import Universals
        Universals.fillMySettings()
        Universals.printForDevelopers("Before MyObjects")
        from MyObjects import *
        Universals.printForDevelopers("Before InputOutputs")
        import InputOutputs
        import OldAppName
        if OldAppName.checkOldAppNameAndSettings():
            OldAppName.getSettingsFromOldNameAndSettings()
        if Universals.isActivePyKDE4==True:
            Universals.printForDevelopers("ActivePyKDE4")
            appName     = "HamsiManager"
            programName = ki18n ("Hamsi Manager")
            version     = RoutineChecks.__version__
            license     = MAboutData.License_GPL_V3
            copyright   = ki18n (u"Murat Demir (mopened@gmail.com)")
            kde4LangKode = str(KLocale(Universals.Catalog).language())+"_"+str(KLocale(Universals.Catalog).country()).upper()
            text        = ki18n ("")
            homePage    = "hamsiapps.com"
            bugEmail    = u"Murat Demir (mopened@gmail.com)"
            if InputOutputs.isFile(Universals.HamsiManagerDirectory+"/Languages/About_"+ kde4LangKode):
                aboutFileContent = InputOutputs.readFromFile(Universals.HamsiManagerDirectory+"/Languages/About_"+ kde4LangKode)
            else:
                aboutFileContent = InputOutputs.readFromFile(Universals.HamsiManagerDirectory+"/Languages/About_en_GB")
            description = ki18n (aboutFileContent.decode("utf-8"))
            aboutOfHamsiManager = MAboutData (appName, Universals.Catalog, programName, version, description,
                                    license, copyright, text, homePage, bugEmail)
            aboutOfHamsiManager.addAuthor (ki18n(u"Murat Demir"), ki18n(u"Project Manager and Project Developer<br>Proje Sorumlusu ve Proje Geliştiricisi"), 
                                "mopened@gmail.com", "hamsiapps.com")
            aboutOfHamsiManager.addCredit(ki18n(u"Tolga Balcı"), ki18n(u"Translate to English. (Voluntary)<br>İngilizce Çevirisi. (Gönüllü) (V0.7.x)"), 
                                            "tbalci@gmail.com", "http://www.brighthub.com/members/paladin.aspx")
            aboutOfHamsiManager.addCredit(ki18n(u"Márcio Moraes"), ki18n(u"Translate to Brazilian Portuguese. (Voluntary)<br>Brezilya Portekizcesi diline çeviri. (Gönüllü) (V0.8.7 - ~)"), 
                                            "", "")
            aboutOfHamsiManager.setProgramIconName(Universals.themePath + "/Images/HamsiManager.png") 
            if InputOutputs.isFile(Universals.HamsiManagerDirectory+"/Languages/License_"+ kde4LangKode):
                aboutOfHamsiManager.addLicenseTextFile(Universals.HamsiManagerDirectory+"/Languages/License_"+ kde4LangKode)
            else:
                aboutOfHamsiManager.addLicenseTextFile(Universals.HamsiManagerDirectory+"/Languages/License_en_GB")
            MCmdLineArgs.init (sys.argv, aboutOfHamsiManager)
            HamsiManagerApp = MApplication()
            kde4LangKode = str(MGlobal.locale().language())
            if len(kde4LangKode)!=5: kde4LangKode += "_"+str(MGlobal.locale().country()).upper()
            if InputOutputs.getInstalledLanguagesCodes().count(kde4LangKode)==0:
                for lcode in InputOutputs.getInstalledLanguagesCodes():
                    if lcode.find(kde4LangKode[:2])!=-1:
                        kde4LangKode = lcode
            kconf = MGlobal.config()
            MGlobal.locale().setLanguage(kde4LangKode, kconf)
            if InputOutputs.isFile(Universals.HamsiManagerDirectory+"/Languages/HamsiManager_"+
                            str(kde4LangKode+".qm")):
                languageFile = MTranslator()
                languageFile.load((Universals.HamsiManagerDirectory+"/Languages/HamsiManager_"+
                            str(kde4LangKode+".qm")).decode(Settings.defaultFileSystemEncoding))
                HamsiManagerApp.installTranslator(languageFile)
            Universals.aboutOfHamsiManager = aboutOfHamsiManager
        else:
            Universals.printForDevelopers("NotActivePyKDE4")
            HamsiManagerApp = MApplication(sys.argv)  
            if InputOutputs.isFile(Universals.HamsiManagerDirectory+"/Languages/About_"+ str(Universals.MySettings["language"])):
                aboutFileContent = InputOutputs.readFromFile(Universals.HamsiManagerDirectory+"/Languages/About_"+ str(Universals.MySettings["language"]))
            else:
                aboutFileContent = InputOutputs.readFromFile(Universals.HamsiManagerDirectory+"/Languages/About_en_GB")
            Universals.aboutOfHamsiManager = aboutFileContent.decode("utf-8")
            if InputOutputs.isFile(Universals.HamsiManagerDirectory+"/Languages/HamsiManagerWithQt_"+
                            str(Universals.MySettings["language"]+".qm")):
                languageFile = MTranslator()
                languageFile.load((Universals.HamsiManagerDirectory+"/Languages/HamsiManagerWithQt_"+
                            str(Universals.MySettings["language"]+".qm")).decode(Settings.defaultFileSystemEncoding))
                HamsiManagerApp.installTranslator(languageFile)
        HamsiManagerApp.setApplicationName("HamsiManager")
        HamsiManagerApp.setApplicationVersion(RoutineChecks.__version__)
        HamsiManagerApp.setOrganizationDomain("hamsiapps.com")
        HamsiManagerApp.setOrganizationName("Hamsi Apps")
        MApplication.setQuitOnLastWindowClosed(True)
        MDir.setSearchPaths("Images", MStringList((Universals.themePath + "/Images/").decode(Settings.defaultFileSystemEncoding)))
        MDir.setSearchPaths("root", MStringList((Universals.HamsiManagerDirectory+"/").decode(Settings.defaultFileSystemEncoding)))
        if InputOutputs.isFile(Universals.themePath + "/Style.qss"):
            HamsiManagerApp.setStyleSheet(InputOutputs.readFromFile(Universals.themePath + "/Style.qss"))
        MTextCodec.setCodecForTr(MTextCodec.codecForName("UTF-8"))
        HamsiManagerApp.setWindowIcon(MIcon("Images:HamsiManager.png"))
        MApplication.setStyle(Universals.MySettings["applicationStyle"])
        Universals.printForDevelopers("Before RoutineChecks.checkMyModules")
        if RoutineChecks.checkMyModules(HamsiManagerApp):
            if RoutineChecks.isQuickMake:
                Universals.printForDevelopers("QuickMake")
                try:
                    myUniversals = Universals.Universals(HamsiManagerApp, None)
                    Universals.fillUIUniversals()
                    import QuickMake
                    quickMake = QuickMake.QuickMake()
                    if RoutineChecks.isQuickMake:
                        HamsiManagerApp.exec_()
                except:
                    import ReportBug
                    error = ReportBug.ReportBug()
                    error.show()
                    HamsiManagerApp.exec_()
            if RoutineChecks.isQuickMake == False:
                Universals.printForDevelopers("NotQuickMake")
                import SpecialTools
                import Tables
                import FileManager
                import Bars
                Universals.printForDevelopers("After Modules")
                try:
                    class Main(MMainWindow):
                        def __init__(self):
                            MMainWindow.__init__(self, None)
                            Universals.printForDevelopers("Started __init__")
                            self.setObjectName("RealMainWindow")
                            myUniversals = Universals.Universals(HamsiManagerApp, self)
                            Universals.fillUIUniversals()
                            self.CentralWidget = MWidget()
                            self.Menu = None
                            self.MainLayout = MVBoxLayout()
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
                            self.CentralWidget.setLayout(self.MainLayout)
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
                            
                        def lockForm(self):
                            self.CentralWidget.setEnabled(False)
                            for wid in self.findChildren(MDockWidget):
                                wid.setEnabled(False)
                            for wid in self.findChildren(MToolBar):
                                wid.setEnabled(False)
                            for wid in self.findChildren(MMenuBar):
                                wid.setEnabled(False)
                            
                        def unlockForm(self):
                            self.CentralWidget.setEnabled(True)
                            for wid in self.findChildren(MDockWidget):
                                wid.setEnabled(True)
                            for wid in self.findChildren(MToolBar):
                                wid.setEnabled(True)
                            for wid in self.findChildren(MMenuBar):
                                wid.setEnabled(True)
                            
                        def closeEvent(self, _event):
                            try:
                                Universals.isStartedCloseProcces = True
                                Universals.printForDevelopers("Started closeEvent")
                                MApplication.setQuitOnLastWindowClosed(True)
                                try:self.PlayerBar.Player.stop()
                                except:pass
                                import ReportBug, Records
                                from Details import MusicDetails, TextDetails, CoverDetails
                                MusicDetails.closeAllMusicDialogs()
                                TextDetails.closeAllTextDialogs()
                                CoverDetails.closeAllCoverDialogs()
                                Universals.printForDevelopers("Closed Dialogs")
                                if self.Table.checkUnSavedTableValues()==False:
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
                                Universals.setMySetting(self.Table.hiddenTableColumnsSettingKey,self.Table.hiddenTableColumns)
                                self.Bars.setAllBarsStyleToMySettings()
                                if ReportBug.iSClosingInErrorReporting == False:
                                    Records.setRecordType(1)
                                    subFixForStateFile = ""
                                    if Universals.windowMode!=Universals.windowModeKeys[0]:
                                        subFixForStateFile = Universals.windowMode
                                    InputOutputs.writeToBinaryFile(Settings.pathOfSettingsDirectory + "LastState" + subFixForStateFile, self.saveState())
                                    Records.restoreRecordType()
                                    geometri = [self.geometry().x(), self.geometry().y(), self.geometry().width(), self.geometry().height()]
                                    Universals.setMySetting("MainWindowGeometries",geometri)
                                Universals.setMySetting("lastDirectory",self.FileManager.currentDirectory)
                                Universals.setMySetting("isMainWindowMaximized",self.isMaximized())
                                Universals.setMySetting("isShowAdvancedSelections",self.SpecialTools.isShowAdvancedSelections)
                                if Universals.tableType==2:
                                    Universals.setMySetting("isRunOnDoubleClick",self.Table.tbIsRunOnDoubleClick.isChecked())
                                    Universals.setMySetting("isOpenDetailsInNewWindow",self.Table.isOpenDetailsOnNewWindow.isChecked())
                                    Universals.setMySetting("isPlayNow",self.Table.isPlayNow.isChecked())
                                Universals.setMySetting("isShowOldValues",Universals.isShowOldValues)
                                Universals.setMySetting("isChangeSelected",Universals.isChangeSelected)
                                Universals.setMySetting("isChangeAll",Universals.isChangeAll)
                                Universals.setMySetting("tableType", Universals.tableType)
                                Universals.setMySetting("activeTabNoOfSpecialTools", self.SpecialTools.tabwTabs.currentIndex())
                                Universals.saveSettings()
                                Settings.saveUniversalSettings()
                                Universals.printForDevelopers("After Save Configs")
                                RoutineChecks.checkAfterCloseProccess()
                                Universals.printForDevelopers("After RoutineChecks.checkAfterCloseProccess")
                            except:
                                import ReportBug
                                if ReportBug.isClose==False:
                                    error = ReportBug.ReportBug()
                                    error.show()
                                    _event.ignore()
                    
                    Universals.printForDevelopers("Before Main")
                    MainWindow=Main()
                    Universals.printForDevelopers("After Main")
                    MainWindow.setWindowTitle(u"Hamsi Manager "+ MApplication.applicationVersion())
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
                            if Universals.windowMode!=Universals.windowModeKeys[0]:
                                subFixForStateFile = Universals.windowMode
                            state.append(InputOutputs.readFromBinaryFile(Settings.pathOfSettingsDirectory + "LastState" + subFixForStateFile))
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
                    import ReportBug
                    error = ReportBug.ReportBug()
                    error.show()
                try:
                    Universals.printForDevelopers("Before HamsiManagerApp.exec_")
                    HamsiManagerApp.exec_()
                except:
                    import ReportBug
                    error = ReportBug.ReportBug()
                    error.show()
                    print str(MApplication.translate("ReportBug", "A critical error has occurred.If you want to look into details \"%s\" you can see the file.If possible, we ask you to send us this error details." )) % (error.pathOfReportFile)
                    print str(MApplication.translate("ReportBug", "Thanks in advance for your interest."))
                else:
                    sys.exit()
        else:
            sys.exit()
    else:
        sys.exit()
    sys.exit()
else:
    sys.exit()
    
