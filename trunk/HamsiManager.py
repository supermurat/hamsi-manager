#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
reload(sys)
sys.setdefaultencoding("utf-8")
if sys.path[0]=="":
    sys.path.insert(0, sys.path[1])
sys.path.insert(1,sys.path[0]+"/Source")
sys.path.insert(2,sys.path[0]+"/SearchEngines")

import RoutineChecks
if RoutineChecks.checkPyQt4Exist():
    myUniversals = ""
    if RoutineChecks.checkParameters():
        import Settings
        Settings.checkSettings()
        import Universals
        Universals.fillMySettings()
        from MyObjects import *
        import InputOutputs
        import OldAppName
        if OldAppName.checkOldAppNameAndSettings():
            OldAppName.getSettingsFromOldNameAndSettings()
        if Universals.isActivePyKDE4==True:
            from PyKDE4.kdecore import *
            from PyKDE4.kdeui import *
            appName     = "HamsiManager"
            programName = ki18n ("Hamsi Manager")
            version     = RoutineChecks.__version__
            license     = KAboutData.License_GPL_V3
            copyright   = ki18n (u"Murat DEMİR (mxd@mixdigitall.com)")
            kde4LangKode= str(KLocale(Universals.Catalog).language())+"_"+str(KLocale(Universals.Catalog).country()).upper()
            text        = ki18n ("")
            homePage    = "hamsiapps.com"
            bugEmail    = u"Murat DEMIR (mxd@mixdigitall.com)"
            if InputOutputs.isFile(Universals.sourcePath+"/Languages/About_"+ kde4LangKode):
                aboutFileContent = InputOutputs.readFromFile(Universals.sourcePath+"/Languages/About_"+ kde4LangKode)
            else:
                aboutFileContent = InputOutputs.readFromFile(Universals.sourcePath+"/Languages/About_en_GB")
            description = ki18n (aboutFileContent.decode("utf-8"))
            aboutOfHamsiManager = KAboutData (appName, Universals.Catalog, programName, version, description,
                                    license, copyright, text, homePage, bugEmail)
            aboutOfHamsiManager.addAuthor (ki18n("Murat DEMİR"), ki18n("Project Manager and Project Developer<br>Proje Sorumlusu ve Proje Geliştiricisi"), 
                                "mxd@mixdigitall.com", "hamsiapps.com")
            aboutOfHamsiManager.addCredit(ki18n("Tolga Balcı"), ki18n("Translate to English. (Voluntary)<br>İngilizce Çevirisi. (Gönüllü) (V0.7.x)"), 
                                            "tbalci@gmail.com", "http://www.brighthub.com/members/paladin.aspx")
            aboutOfHamsiManager.addCredit(ki18n("Márcio Moraes"), ki18n("Translate to Brazilian Portuguese. (Voluntary)<br>Brezilya Portekizcesi diline çeviri. (Gönüllü) (V0.8.7 - ~)"), 
                                            "", "")
            aboutOfHamsiManager.setProgramIconName(Universals.themePath + "/Images/HamsiManager.png") 
            if InputOutputs.isFile(Universals.sourcePath+"/Languages/License_"+ kde4LangKode):
                aboutOfHamsiManager.addLicenseTextFile(Universals.sourcePath+"/Languages/License_"+ kde4LangKode)
            else:
                aboutOfHamsiManager.addLicenseTextFile(Universals.sourcePath+"/Languages/License_en_GB")
            KCmdLineArgs.init (sys.argv, aboutOfHamsiManager)
            HamsiManagerApp = KApplication()  
            MMainWindow = KMainWindow
            kde4LangKode = str(KGlobal.locale().language())
            if len(kde4LangKode)!=5: kde4LangKode += "_"+str(KGlobal.locale().country()).upper()
            if InputOutputs.getInstalledLanguagesCodes().count(kde4LangKode)==0:
                for lcode in InputOutputs.getInstalledLanguagesCodes():
                    if lcode.find(kde4LangKode[:2])!=-1:
                        kde4LangKode = lcode
            kconf = KGlobal.config()
            KGlobal.locale().setLanguage(kde4LangKode, kconf)
            if InputOutputs.isFile(Universals.sourcePath+"/Languages/HamsiManager_"+
                            str(kde4LangKode+".qm")):
                languageFile = MTranslator()
                languageFile.load((Universals.sourcePath+"/Languages/HamsiManager_"+
                            str(kde4LangKode+".qm")).decode("utf-8"))
                HamsiManagerApp.installTranslator(languageFile)
            Universals.aboutOfHamsiManager = aboutOfHamsiManager
        else:
            HamsiManagerApp = MApplication(sys.argv)  
            if InputOutputs.isFile(Universals.sourcePath+"/Languages/About_"+ str(Universals.MySettings["language"])):
                aboutFileContent = InputOutputs.readFromFile(Universals.sourcePath+"/Languages/About_"+ str(Universals.MySettings["language"]))
            else:
                aboutFileContent = InputOutputs.readFromFile(Universals.sourcePath+"/Languages/About_en_GB")
            Universals.aboutOfHamsiManager = aboutFileContent.decode("utf-8")
            if InputOutputs.isFile(Universals.sourcePath+"/Languages/HamsiManagerWithQt_"+
                            str(Universals.MySettings["language"]+".qm")):
                languageFile = MTranslator()
                languageFile.load((Universals.sourcePath+"/Languages/HamsiManagerWithQt_"+
                            str(Universals.MySettings["language"]+".qm")).decode("utf-8"))
                HamsiManagerApp.installTranslator(languageFile)
        HamsiManagerApp.setApplicationName("HamsiManager")
        HamsiManagerApp.setApplicationVersion(RoutineChecks.__version__)
        HamsiManagerApp.setOrganizationDomain("hamsiapps.com")
        HamsiManagerApp.setOrganizationName("Hamsi Apps")
        MApplication.setQuitOnLastWindowClosed(True)
        MDir.setSearchPaths("Images", MStringList((Universals.themePath + "/Images/").decode("utf-8")))
        MDir.setSearchPaths("Source", MStringList((Universals.sourcePath+"/").decode("utf-8")))
        MDir.setSearchPaths("root", MStringList((Universals.sourcePath+"/../").decode("utf-8")))
        if InputOutputs.isFile(Universals.themePath + "/Style.qss"):
            HamsiManagerApp.setStyleSheet(InputOutputs.readFromFile(Universals.themePath + "/Style.qss"))
        MTextCodec.setCodecForTr(MTextCodec.codecForName("UTF-8"))
        HamsiManagerApp.setWindowIcon(MIcon("Images:HamsiManager.png"))
        MApplication.setStyle(Universals.MySettings["applicationStyle"])
        if RoutineChecks.checkMyModules(HamsiManagerApp):
            if RoutineChecks.isQuickMake:
                try:
                    myUniversals = Universals.Universals(HamsiManagerApp, None)
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
                import SpecialTools
                import Tables
                import FileManager
                import Bars
                try:
                    class Main(MMainWindow):
                        def __init__(self):
                            MMainWindow.__init__(self, None)
                            self.setObjectName("RealMainWindow")
                            myUniversals = Universals.Universals(HamsiManagerApp, self)
                            self.CentralWidget = MWidget()
                            self.Menu = None
                            self.MainLayout = MVBoxLayout()
                            self.Bars = Bars.Bars()
                            self.ToolsBar = Bars.ToolsBar(self)
                            self.TableToolsBar = Bars.TableToolsBar(self)
                            self.FileManager = FileManager.FileManager(self)
                            self.CentralWidget.setLayout(self.MainLayout)
                            self.setCentralWidget(self.CentralWidget)
                            self.Menu = Bars.MenuBar(self)
                            self.setMenuBar(self.Menu)
                            self.setStatusBar(Bars.StatusBar(self))
                            self.Bars.getAllBarsStyleFromMySettings()
                            self.setCorner(Mt.TopLeftCorner, Mt.LeftDockWidgetArea)
                            self.setCorner(Mt.BottomLeftCorner, Mt.LeftDockWidgetArea)
                            
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
                                MApplication.setQuitOnLastWindowClosed(True)
                                try:self.PlayerBar.Player.stop()
                                except:pass
                                import ReportBug, Records
                                from Details import MusicDetails, TextDetails
                                MusicDetails.closeAllMusicDialogs()
                                TextDetails.closeAllTextDialogs()
                                if self.Table.checkUnSavedTableValues()==False:
                                    _event.ignore() 
                                Universals.setMySetting(self.Table.hiddenTableColumnsSettingKey,self.Table.hiddenTableColumns)
                                self.Bars.setAllBarsStyleToMySettings()
                                if ReportBug.iSClosingInErrorReporting == False:
                                    Records.setRecordType(1)
                                    InputOutputs.writeToFile(Settings.pathOfSettingsDirectory+"LastState", self.saveState())
                                    Records.restoreRecordType()
                                    geometri = [self.geometry().x(), self.geometry().y(), self.geometry().width(), self.geometry().height()]
                                    Universals.setMySetting("MainWindowGeometries",geometri)
                                Universals.setMySetting("lastDirectory",self.FileManager.currentDirectory)
                                Universals.setMySetting("isMainWindowMaximized",self.isMaximized())
                                Universals.setMySetting("isShowAdvancedSelections",self.SpecialTools.isShowAdvancedSelections)
                                if Tables.tableType==2:
                                    Universals.setMySetting("isRunOnDoubleClick",self.Table.tbIsRunOnDoubleClick.isChecked())
                                    Universals.setMySetting("isOpenDetailsInNewWindow",self.Table.isOpenDetailsOnNewWindow.isChecked())
                                    Universals.setMySetting("isPlayNow",self.Table.isPlayNow.isChecked())
                                Universals.setMySetting("isShowOldValues",self.Table.isShowOldValues.isChecked())
                                Universals.setMySetting("isChangeSelected",self.Table.isChangeSelected.isChecked())
                                Universals.setMySetting("isChangeAll",self.Table.isChangeAll.isChecked())
                                Universals.setMySetting("tableType", Tables.tableType)
                                Universals.setMySetting("activeTabNoOfSpecialTools", self.SpecialTools.tabwTabs.currentIndex())
                                Universals.saveSettings()
                                Settings.saveUniversalSettings()
                                RoutineChecks.checkAfterCloseProccess()
                            except:
                                import ReportBug
                                if ReportBug.isClose==False:
                                    error = ReportBug.ReportBug()
                                    error.show()
                                    _event.ignore()
                                    
                    MainWindow=Main()
                    MainWindow.setWindowTitle(u"Hamsi Manager "+ MApplication.applicationVersion())
                    if Universals.isActivePyKDE4==True:
                        kconf = KGlobal.config()
                        kconfGroup = KConfigGroup(kconf,"Universals")
                        MainWindow.setAutoSaveSettings(kconfGroup)
                    else:
                        try:
                            state = MByteArray()
                            state.append(InputOutputs.readFromBinaryFile(Settings.pathOfSettingsDirectory+"LastState"))
                            MainWindow.restoreState(state)
                        except:pass
                    if eval(Universals.MySettings["isMainWindowMaximized"].title())==False:
                        geometries = Universals.getListFromStrint(Universals.MySettings["MainWindowGeometries"])
                        MainWindow.setGeometry(int(geometries[0]),int(geometries[1]), int(geometries[2]),int(geometries[3]))
                        MainWindow.show()
                    else:
                        MainWindow.showMaximized()
                    RoutineChecks.checkAfterRunProccess()
                    Universals.isStartingSuccessfully = True
                    Universals.isCanBeShowOnMainWindow = True
                except:
                    import ReportBug
                    error = ReportBug.ReportBug()
                    error.show()
                try:
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
    
