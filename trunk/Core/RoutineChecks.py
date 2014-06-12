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
import os

myArgvs = []
isQuickMake = False
QuickMakeParameters = []
parser =None

def checkParameters():
    from optparse import OptionParser, OptionGroup
    import logging
    from Core import Variables
    from Core import Universals
    import InputOutputs
    global isQuickMake, QuickMakeParameters, myArgvs, parser, optionList
    myArgvs = sys.argv
    isDontRun = False
    optionList = []
    parser = OptionParser(
    usage="%prog [options] [<arg1>...]", version="HamsiManager " + Variables.version, 

    epilog="""\
Copyright (c) 2010 - 2013 Murat Demir <mopened@gmail.com> ,
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
    qmgroup.add_option('--qm', help='Are you want to run Quick Make by some parametres?', 
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
    if len(remainderParameters)==1:
        try:Universals.setMySetting("lastDirectory", Universals.trDecode(str(remainderParameters[0]), InputOutputs.defaultFileSystemEncoding))
        except:Universals.setMySetting("lastDirectory", str(remainderParameters[0]))
    if options.directory:
        try:Universals.setMySetting("lastDirectory", Universals.trDecode(str(options.directory), InputOutputs.defaultFileSystemEncoding))
        except:Universals.setMySetting("lastDirectory", str(options.directory))
    if options.loggingLevel:
        Universals.loggingLevel = options.loggingLevel
    if options.sFileName:
        Universals.fileOfSettings = options.sFileName
    if options.sDirectoryPath:
        Universals.setPathOfSettingsDirectory(options.sDirectoryPath)
    if options.tableType:
        Universals.setMySetting("tableType", Universals.getThisTableType(options.tableType))
    if options.fileReNamerType:
        Universals.setMySetting("fileReNamerType", options.fileReNamerType)
    if options.qm:
        if options.qmw:
            if options.qmw.lower()=="false" or options.qmw=="0":
                Universals.setMySetting("isShowQuickMakeWindow", False)
            else:
                Universals.setMySetting("isShowQuickMakeWindow", True)
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
        if Variables.isRunningAsRoot()==False:
            strArgvs = []
            for tempArg in sys.argv:
                if tempArg.find("-runAsRoot")==-1 and tempArg.find(Execute.findExecutablePath("HamsiManager"))==-1 and tempArg != "./" + Execute.findExecutableBaseName("HamsiManager") and tempArg != Execute.findExecutableBaseName("HamsiManager"):
                    strArgvs.append(tempArg)
            if Execute.executeAsRootWithThread(strArgvs, "HamsiManager"):
                isDontRun = True
    if isDontRun:
        return False
    return True

def checkAfterRunProccess():
    from Core import Variables
    from Core import Universals
    from Core import Dialogs, UpdateControl
    from Core.MyObjects import translate, isActivePyKDE4
    import InputOutputs
    if str(InputOutputs.defaultFileSystemEncoding) != str(Universals.MySettings["fileSystemEncoding"]):
        answer = Dialogs.ask(translate("HamsiManager", "Your System's \"File System Encoding\" Type Different"),
                    translate("HamsiManager", "Your system's \"File System Encoding\" type different from the settings you select. Are you sure you want to continue?If you are not sure press the \"No\"."), False, "Your System's \"File System Encoding\" Type Different")
        if answer==Dialogs.No: 
            from Options import OptionsForm
            OptionsForm.OptionsForm(Universals.MainWindow, _focusTo="fileSystemEncoding")
    if Universals.getBoolValue("isMakeAutoDesign") or Universals.getBoolValue("isShowWindowModeSuggestion"):
        Universals.MainWindow.TableToolsBar.setVisible(False)
        Universals.MainWindow.ToolsBar.setVisible(False)
        if isActivePyKDE4==True:
            Universals.MainWindow.Browser.setVisible(False)
            Universals.MainWindow.TreeBrowser.setVisible(False)
            Universals.MainWindow.FileManager.urlNavigator.setMinimumWidth(150)
            try:Universals.MainWindow.FileManager.dckwBrowserToolsFull.setVisible(False)
            except:Universals.MainWindow.FileManager.tbarBrowserToolsFull.setVisible(False)
        try:Universals.MainWindow.PlayerBar.setVisible(False)
        except:pass
    checkAndCorrectWindowMode()
    if Universals.isShowVerifySettings and Universals.changedDefaultValuesKeys==[] and Universals.newSettingsKeys==[]:
        answer = Dialogs.ask(translate("HamsiManager", "Added New Options And New Features"),
                    translate("HamsiManager", "New options and new features added to Hamsi Manager. Are you want to change or verify new options?"), False, "Added New Options And New Features")
        if answer==Dialogs.Yes: 
            from Options import OptionsForm
            OptionsForm.OptionsForm(Universals.MainWindow)
    elif Universals.changedDefaultValuesKeys!=[] or Universals.newSettingsKeys!=[]:
        answer = Dialogs.ask(translate("HamsiManager", "Added New Options And New Features"),
                    translate("HamsiManager", "New options and new features added to Hamsi Manager. Changed default values of few settings. Are you want to change or verify new options?"), False, "Added New Options And New Features")
        if answer==Dialogs.Yes:
            from Options import OptionsForm
            newOrChangedKeys = Universals.newSettingsKeys + Universals.changedDefaultValuesKeys
            OptionsForm.OptionsForm(Universals.MainWindow, "Normal", None, newOrChangedKeys)
    elif Universals.getBoolValue("isShowReconfigureWizard") and Variables.isBuilt() == False:
        from Tools import Configurator
        Configurator.Configurator()
        Universals.setMySetting("isShowReconfigureWizard", "False")
    
def checkWindowMode(_isCheck=False):
    from Core import Variables
    from Core import Universals
    if Universals.getBoolValue("isShowWindowModeSuggestion") or _isCheck:
        if Universals.windowMode == Variables.windowModeKeys[0]:
            screenSize = Variables.getScreenSize()
            if screenSize!=None:
                if screenSize.width()<1024:
                    Universals.windowMode = Variables.windowModeKeys[1]
    
def checkAndCorrectWindowMode(_isCheck=False):
    from Core import Variables
    from Core import Universals
    from Core import Dialogs 
    from Core.MyObjects import translate, MToolBar
    if Universals.getBoolValue("isShowWindowModeSuggestion") or _isCheck:
        if Universals.windowMode == Variables.windowModeKeys[1]:
            if len(Universals.MainWindow.findChildren(MToolBar))>0:
                firstToolBar = Universals.MainWindow.findChildren(MToolBar)[0]
                Universals.MainWindow.removeToolBar(Universals.MainWindow.FileManager.tbarBrowserTools)
                Universals.MainWindow.insertToolBar(firstToolBar, Universals.MainWindow.FileManager.tbarBrowserTools)
                Universals.MainWindow.FileManager.tbarBrowserTools.setVisible(True)
            try:
                if Universals.MainWindow.Browser!=None and Universals.MainWindow.Places!=None:
                    Universals.MainWindow.tabifyDockWidget(Universals.MainWindow.Browser, Universals.MainWindow.Places)
                if Universals.MainWindow.Browser!=None and Universals.MainWindow.TreeBrowser!=None:
                    Universals.MainWindow.tabifyDockWidget(Universals.MainWindow.Browser, Universals.MainWindow.TreeBrowser)
                if Universals.MainWindow.Browser!=None and Universals.MainWindow.DirOperator!=None:
                    Universals.MainWindow.tabifyDockWidget(Universals.MainWindow.Browser, Universals.MainWindow.DirOperator)
                try:Universals.MainWindow.FileManager.dckwBrowserToolsFull.setVisible(False)
                except:Universals.MainWindow.FileManager.tbarBrowserToolsFull.setVisible(False)
                geometries = Universals.getListValue("MainWindowGeometries")
                Universals.MainWindow.setGeometry(int(geometries[0]),int(geometries[1]), 700, 500)
            except:pass
            Universals.setMySetting("isShowWindowModeSuggestion", False)
     
def checkBeforeCloseProccess():
    from Core import Variables
    from Core import Universals
    from Core import UpdateControl
    if Universals.getBoolValue("isDontDeleteFileAndDirectory"):
        import InputOutputs
        InputOutputs.checkSizeOfDeletedFiles()
    if UpdateControl.isMakeUpdateControl():
        UpdateControl.UpdateControl(Universals.MainWindow, _isCloseParent=True)
        return False
    return True

def checkAfterCloseProccess():
    from Core import Records
    Records.saveAllRecords()
    Records.checkSize()
    
def checkMyModules(_HamsiManagerApp):
    try:
        import SpecialTools
        import Tables
        from Core import FileManager
        import Bars
        return True
    except ImportError as error:
        from PyQt4 import QtGui
        from PyQt4 import QtCore
        errorForm = QtGui.QWidget()
        errorForm.vblMain = QtGui.QVBoxLayout(errorForm)
        if str(error)[16:].find(" ")==-1:
            title = str(QtGui.QApplication.translate("ReportBug", "Missing Module"))
            startNumber=16
            details = str(QtGui.QApplication.translate("ReportBug", "Application will not work without the module \"%s\"."))
        else:
            title = str(QtGui.QApplication.translate("ReportBug", "Error In Module"))
            startNumber=19
            details = str(QtGui.QApplication.translate("ReportBug", "\"%s\" is not in this module.Please download and install Hamsi Manager again."))
        lblDetails = QtGui.QLabel(Universals.trForUI("<b>"+title+":</b><br>"+ (details % (str(error)[startNumber:]))))
        pbtnOk = QtGui.QPushButton(QtGui.QApplication.translate("ReportBug", "OK"))
        errorForm.connect(pbtnOk,QtCore.SIGNAL("clicked()"), _HamsiManagerApp.quit)
        hbox0 = QtGui.QHBoxLayout()
        hbox0.addStretch(2)
        hbox0.addWidget(pbtnOk,1)
        errorForm.vblMain.addWidget(lblDetails)
        errorForm.vblMain.addLayout(hbox0)
        errorForm.setWindowTitle(QtGui.QApplication.translate("ReportBug", "Critical Error!"))
        errorForm.show()
        sys.exit(_HamsiManagerApp.exec_())
    return False
    
def checkMandatoryModules():
    try:
        from PyQt4 import QtGui, QtCore
        if os.name=="nt":
            pywin32IsAvailable = False
            try:
                import win32api, win32con, win32com
                pywin32IsAvailable = True
            except:pass
            if pywin32IsAvailable == False:
                app = QtGui.QApplication(sys.argv)
                w = QtGui.QWidget()
                l = QtGui.QVBoxLayout(w)
                qbtn = QtGui.QPushButton('Quit', w)
                qbtn.clicked.connect(QtCore.QCoreApplication.instance().quit)
                lblAlert = QtGui.QLabel("<br><b><a href='https://sourceforge.net/projects/pywin32/'>'Python for Windows Extensions'</a> (pywin32) named module has NOT installed on your system.</b><br><br>You have to install it on your system to run Hamsi Manager.<br><br>", w)
                lblAlert.setOpenExternalLinks(True)
                l.addWidget(lblAlert)
                l.addWidget(qbtn)
                w.setLayout(l)
                w.setWindowTitle('Critical Error!')
                w.show()
                w.setMinimumWidth(400)
                sys.exit(app.exec_())
        return True
    except:
        try:
            import qt
            HamsiManagerApp=qt.QApplication(sys.argv)
            panel = qt.QWidget()
            panel.vblMain = qt.QVBoxLayout(panel)
            lblInfo = qt.QLabel("<br><b>PyQt4 is not installed:</b><br>You have to install \"PyQt4\" on your system to run Hamsi Manager.",panel)
            pbtnClose = qt.QPushButton("OK",panel)
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
            panel.setCaption("Critical Error!")
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
                button = gtk.Button("OK")
                label = gtk.Label("PyQt4 is not installed.")
                label2 = gtk.Label("You have to install \"PyQt4\" on your system to run Hamsi Manager.")
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
                label3 = gtk.Label("")
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
                    lbl1 = Tkinter.Label(text="PyQt4 is not installed.")
                    lbl1.pack()
                    lbl2 = Tkinter.Label(text="You have to install \"PyQt4\"")
                    lbl2.pack()
                    lbl3 = Tkinter.Label(text="on your system to run HamsiManager.")
                    lbl3.pack()
                    btnClose = Tkinter.Button(text="OK", command = MainWindow.quit)
                    btnClose.pack(side = Tkinter.RIGHT)
                    Tkinter.mainloop()
                except:
                    print ("Critical Error!")
                    print ("You have to install \"PyQt4\" on your system to run Hamsi Manager.")
        return False    
        
        
        
    
