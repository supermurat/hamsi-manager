# -*- coding: utf-8 -*-
import sys
import os
__author__ = "Murat Demir (murat@mopened.com)"
__version__ = "0.8.67"
__intversion__ = 867
__copyright__ = "Copyleft"
__license__ = "GPLv3"
__settingVersion__ = "867"

myArgvs = []
isQuickMake = False
QuickMakeParameters = []
    
def checkParameters():
    global isQuickMake, QuickMakeParameters, myArgvs
    myArgvs = sys.argv
    if len(sys.argv)>1:
        argvs = sys.argv[1:]
        isMyArgs = False
        isDontRun = False
        for argvNo, argv in enumerate(argvs):
            if argv.find("-debug")!=-1:
                import Universals
                Universals.isDebugMode = True
                if len(argv)!=6:
                    argv = argv.replace("-debug", "")
                    argvs[argvNo] = argv
                else:
                    isMyArgs = True
            if argv.find("-develop")!=-1:
                import Universals
                Universals.isDeveloperMode = True
                if len(argv)!=8:
                    argv = argv.replace("-develop", "")
                    argvs[argvNo] = argv
                else:
                    isMyArgs = True
            try:
                tempT = argvs[argvNo+1]
            except:
                if argv=="-s" or argv=="-sDirectoryPath" or argv=="-t" or argv=="-f" or argv=="-PyKDE4" or argv=="-qmw" or argv=="-qm":
                    isMyArgs = True
                    argvs.remove(argv)
                    print "Incorrect Command : Your action unable to process.Please try again."
                    break
            else:
                if argv=="-s" or argv=="-sDirectoryPath" or argv=="-t" or argv=="-f" or argv=="-PyKDE4" or argv=="-qmw" or argv=="-qm":
                    isMyArgs = True
                    if argvs[argvNo+1][0]=="-":
                        argvs.remove(argv)
                        print "Incorrect Command : Your action unable to process.Please try again."
                        break
                if argv=="-s":
                    import Settings
                    Settings.fileOfSettings = "SettingFiles/" + argvs[argvNo+1]
                    continue
                elif argv=="-sDirectoryPath":
                    import Settings
                    Settings.setPathOfSettingsDirectory(argvs[argvNo+1])
                    continue
                elif argv=="-t":
                    import Universals
                    Universals.setMySetting("tableType", Universals.getThisTableType(argvs[argvNo+1]))
                    continue
                elif argv=="-f":
                    import Universals
                    Universals.setMySetting("fileReNamerType", argvs[argvNo+1])
                    continue
                elif argv=="-PyKDE4":
                    import Universals
                    if argvs[argvNo+1].lower()=="false" or argvs[argvNo+1]=="0":
                        Universals.setMySetting("isActivePyKDE4", False)
                    else:
                        Universals.setMySetting("isActivePyKDE4", True)
                    continue
                elif argv=="-qmw":
                    import Universals
                    if argvs[argvNo+1].lower()=="false" or argvs[argvNo+1]=="0":
                        Universals.setMySetting("isShowQuickMakeWindow", False)
                    else:
                        Universals.setMySetting("isShowQuickMakeWindow", True)
                    continue
                elif argv=="-qm":
                    isQuickMake = True
                    QuickMakeParameters.append(argvs[argvNo+1])
                    pars = argvs[argvNo+2:]
                    for parNo, par in enumerate(pars):
                        if par[0]!="-" and pars[parNo-1][0]!="-":
                            QuickMakeParameters.append(par)
                    continue
            try:
                tempT = argvs[argvNo-1]
            except:
                pass
            else:
                if (argvs[argvNo-1]=="-s" or  argvs[argvNo-1]=="-sDirectoryPath" or  argvs[argvNo-1]=="-t" or 
                        argvs[argvNo-1]=="-f" or argvs[argvNo-1]=="-PyKDE4" or 
                        argvs[argvNo-1]=="-qmw" or argvs[argvNo-1]=="-qm"):
                    isMyArgs = True
                    continue
            if argv=="-runAsRoot":
                import Execute
                if Execute.isRunningAsRoot()==False:
                    strArgvs = ""
                    for tempArg in argvs:
                        if tempArg.find("-runAsRoot")==-1:
                            strArgvs += tempArg + " "
                    if Execute.executeHamsiManagerAsRoot(strArgvs):
                        isDontRun = True
                isMyArgs = True
            elif argv=="-checkAndGetOldAppNameInSystem":
                import OldAppName
                import Universals
                OldAppName.checkAndGetOldAppNameInSystem()
                isDontRun = True
                isMyArgs = True
            elif argv[0]!="-":
                import Universals, InputOutputs
                Universals.setMySetting("lastDirectory", InputOutputs.getRealDirName(argv))
                isMyArgs = True
        if isDontRun:
            return False
        if isMyArgs:
            sys.argv = sys.argv[:1]
    return True

def checkAfterRunProccess():
    import Dialogs, Universals, Settings, UpdateControl
    from MyObjects import translate
    if str(Settings.defaultFileSystemEncoding) != str(Universals.MySettings["systemsCharSet"]):
        answer = Dialogs.ask(translate("HamsiManager", "Your System's \"File System Encoding\" Type Different"),
                    translate("HamsiManager", "Your system's \"File System Encoding\" type different from the settings you select. Are you sure you want to continue?If you are not sure press the \"No\"."), False, "Your System's \"File System Encoding\" Type Different")
        if answer==Dialogs.No: 
            import Options
            Options.Options(Universals.MainWindow, _focusTo="systemsCharSet")
    if Universals.isShowVerifySettings and Universals.changedDefaultValuesKeys==[]:
        answer = Dialogs.ask(translate("HamsiManager", "Added New Options And New Features"),
                    translate("HamsiManager", "New options and new features added to Hamsi Manager. Are you want to change or verify new options?"), False, "Added New Options And New Features")
        if answer==Dialogs.Yes: 
            import Options
            Options.Options(Universals.MainWindow)
    elif Universals.changedDefaultValuesKeys!=[] or Universals.newSettingsKeys!=[]:
        answer = Dialogs.ask(translate("HamsiManager", "Added New Options And New Features"),
                    translate("HamsiManager", "New options and new features added to Hamsi Manager. Changed default values of few settings. Are you want to change or verify new options?"), False, "Added New Options And New Features")
        if answer==Dialogs.Yes: 
            import Options
            newOrChangedKeys = Universals.newSettingsKeys + Universals.changedDefaultValuesKeys
            Options.Options(Universals.MainWindow, "Normal", None, newOrChangedKeys)
    if UpdateControl.isMakeUpdateControl():
        UpdateControl.UpdateControl(Universals.MainWindow)
    checkWindowMode()
    if Universals.getBoolValue("isMakeAutoDesign"):
        if Universals.isActivePyKDE4==True:
            Universals.MainWindow.Browser.setVisible(False)
            Universals.MainWindow.TreeBrowser.setVisible(False)
        Universals.MainWindow.PlayerBar.setVisible(False)
    if Universals.getBoolValue("isShowReconfigureWizard"):
        import Execute
        Execute.executeReconfigure()
    
def checkWindowMode(_isCheck=False):
    import Dialogs, Universals, Settings 
    from MyObjects import translate
    if Universals.getBoolValue("isShowWindowModeSuggestion") or _isCheck:
        if Universals.windowMode == Universals.windowModeKeys[0]:
            screenSize = Settings.getScreenSize()
            if screenSize!=None:
                if screenSize.width()<1024:
                    Universals.windowMode = Universals.windowModeKeys[1]
        if Universals.windowMode == Universals.windowModeKeys[1]:
            answer = Dialogs.ask(translate("HamsiManager", "We Have A Suggestion"),
                    translate("HamsiManager", "Your screen size too small.Are you want to reorganize interface of Hamsi Manager for your screen size?"), False)
            if answer==Dialogs.Yes: 
                try:
                    Universals.MainWindow.TableToolsBar.setVisible(False)
                    Universals.MainWindow.ToolsBar.setVisible(False)
                    if Universals.MainWindow.MusicOptionsBar!=None:
                        Universals.MainWindow.MusicOptionsBar.setVisible(False)
                    if Universals.MainWindow.SubDirectoryOptionsBar!=None:
                        Universals.MainWindow.SubDirectoryOptionsBar.setVisible(False)
                    if Universals.MainWindow.Browser!=None and Universals.MainWindow.Places!=None:
                        Universals.MainWindow.tabifyDockWidget(Universals.MainWindow.Browser, Universals.MainWindow.Places)
                    if Universals.MainWindow.Browser!=None and Universals.MainWindow.TreeBrowser!=None:
                        Universals.MainWindow.tabifyDockWidget(Universals.MainWindow.Browser, Universals.MainWindow.TreeBrowser)
                    if Universals.MainWindow.Browser!=None and Universals.MainWindow.DirOperator!=None:
                        Universals.MainWindow.tabifyDockWidget(Universals.MainWindow.Browser, Universals.MainWindow.DirOperator)
                    geometries = Universals.getListFromStrint(Universals.MySettings["MainWindowGeometries"])
                    Universals.MainWindow.setGeometry(int(geometries[0]),int(geometries[1]), 700, 500)
                except:pass
            Universals.setMySetting("isShowWindowModeSuggestion", False)
     
def checkAfterCloseProccess():
    import OldAppName, Records
    if OldAppName.checkOldAppNameAndSettings():
        OldAppName.checkAndGetPlugins()
        OldAppName.clearOldAppNameAndSettings()
    if OldAppName.checkOldAppNameInSystem():
        OldAppName.checkAndGetOldAppNameInSystem()
    Records.saveAllRecords()
    Records.checkSize()
    
def checkMyModules(_HamsiManagerApp):
    try:
        import SpecialTools
        import Tables
        import FileManager
        import Bars
        return True
    except ImportError , error:
        from PyQt4.QtGui import QWidget, QVBoxLayout, QApplication, QPushButton, QLabel, QHBoxLayout
        from PyQt4.QtCore import SIGNAL
        errorForm = QWidget()
        errorForm.vblMain = QVBoxLayout(errorForm)
        if str(error)[16:].find(" ")==-1:
            title = str(QApplication.translate("ReportBug", "Missing Module"))
            startNumber=16
            details = str(QApplication.translate("ReportBug", "Application will not work without the module \"%s\"."))
        else:
            title = str(QApplication.translate("ReportBug", "Error In Module"))
            startNumber=19
            details = str(QApplication.translate("ReportBug", "\"%s\" is not in this module.Please download and install Hamsi Manager again."))
        lblDetails = QLabel(u"<b>"+title.decode("utf-8")+u":</b><br>"+(details % (str(error)[startNumber:])).decode("utf-8"))
        pbtnOk = QPushButton(QApplication.translate("ReportBug", "OK"))
        errorForm.connect(pbtnOk,SIGNAL("clicked()"), _HamsiManagerApp.quit)
        hbox0 = QHBoxLayout()
        hbox0.addStretch(2)
        hbox0.addWidget(pbtnOk,1)
        errorForm.vblMain.addWidget(lblDetails)
        errorForm.vblMain.addLayout(hbox0)
        errorForm.setWindowTitle(QApplication.translate("ReportBug", "Critical Error!"))
        errorForm.show()
        sys.exit(_HamsiManagerApp.exec_())
    return False
    
def checkPyQt4Exist():
    try:
        import PyQt4.QtGui
        return True
    except:
        try:
            import qt
            HamsiManagerApp=qt.QApplication(sys.argv)
            panel = qt.QWidget()
            panel.vblMain = qt.QVBoxLayout(panel)
            lblInfo = qt.QLabel(u"<br><b>PyQt4 is not installed:</b><br>You have to have \"PyQt4\" installed on your system to run Hamsi Manager.",panel)
            pbtnClose = qt.QPushButton(u"OK",panel)
            panel.connect(pbtnClose,SIGNAL("clicked()"),HamsiManagerApp.quit)
            hbox0 = qt.QHBoxLayout()
            hbox0.addStretch(2)
            hbox0.addWidget(pbtnClose,1)
            vbox0 = qt.QVBoxLayout()
            vbox0.addWidget(lblInfo)
            vbox0.addLayout(hbox0)
            hbox1 = qt.QHBoxLayout()
            hbox1.addStretch(20)
            hbox1.addLayout(vbox0,500)
            hbox1.addStretch(5)
            panel.vblMain.addLayout(hbox1)
            panel.setCaption(u"Critical Error!")
            panel.show()
            panel.setMinimumWidth(400)
            HamsiManagerApp.enter_loop()
        except:
            try:
                import gtk
                def destroy( widget, data=None):
                    gtk.main_quit()
                window = gtk.Window(gtk.WINDOW_TOPLEVEL)
                window.connect("destroy", destroy)
                window.set_title("Critical Error!")
                button = gtk.Button(u"OK")
                label = gtk.Label(u"PyQt4 is not installed.")
                label2 = gtk.Label(u"You have to have \"PyQt4\" installed on your system to run Hamsi Manager.")
                label2.set_line_wrap(True)
                button.connect("clicked", gtk.main_quit, None)
                vbox = gtk.VBox(False,5)
                hbox = gtk.HBox(window)
                window.add(hbox)
                hbox.pack_start(vbox, False, False, 0)
                window.set_border_width(5)
                hbox0 = gtk.HBox(False)
                hbox0.pack_start(label, 0, 0, 0)
                hbox1 = gtk.HBox(False)
                label3 = gtk.Label(u"")
                hbox1.pack_start(label3, 0, 0, 0)
                hbox1.pack_start(button, 0, 0, 0)
                vbox.pack_start(hbox0, False, False, 0)
                vbox.pack_start(label2, False, False, 0)
                vbox.pack_start(hbox1, False, False, 0)
                layout = gtk.Layout(None, None)
                button.set_size_request(120,25)
                label2.set_size_request(350,35)
                label3.set_size_request(230,25)
                window.show_all()
                gtk.main()
            except:
                try:
                    import Tkinter
                    MainWindow = Tkinter.Tk()
                    MainWindow.geometry("350x100")
                    title = MainWindow.title("Critical Error!")
                    lbl1 = Tkinter.Label(text=u"PyQt4 is not installed.")
                    lbl1.pack()
                    lbl2 = Tkinter.Label(text=u"You have to have \"PyQt4\" installed")
                    lbl2.pack()
                    lbl3 = Tkinter.Label(text=u"on your system to run HamsiManager.")
                    lbl3.pack()
                    btnClose = Tkinter.Button(text="OK", command = MainWindow.quit)
                    btnClose.pack(side = Tkinter.RIGHT)
                    Tkinter.mainloop()
                except:
                    print "Critical Error!"
                    print "You have to have \"PyQt4\" installed on your system to run Hamsi Manager."
        return False    
        
        
        
    
