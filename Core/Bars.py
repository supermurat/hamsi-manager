# -*- coding: utf-8 -*-
import Tables
import SpecialTools
import Universals
import Dialogs
from MyObjects import *
import ReportBug
import Organizer
import Execute
import Records
import InputOutputs
import Options

class MenuBar(MMenuBar):
    def __init__(self, _parent):
        MMenuBar.__init__(self, _parent)
        self.mMainPopupMenu = None
        self.mSpecialOptions = None
        self.mTableTools = None
        self.mQuickOptions = None
        self.mFile = self.addMenu(translate("MenuBar", "File"))
        self.mFile.setObjectName(translate("MenuBar", "File"))
        self.mEdit = self.addMenu(translate("MenuBar", "Edit"))
        self.mEdit.setObjectName(translate("MenuBar", "Edit"))
        self.mView = self.addMenu(translate("MenuBar", "View"))
        self.mView.setObjectName(translate("MenuBar", "View"))

        if Universals.getBoolValue("isSaveActions"):
            self.mActions = self.addMenu(translate("MenuBar", "Actions"))
            self.mActions.setObjectName(translate("MenuBar", "Actions"))
            self.mActions.addAction(translate("MenuBar", "Show Last Action")).setObjectName(translate("MenuBar", "Show Last Action"))
        self.mSettings = self.addMenu(translate("MenuBar", "Settings"))
        self.mSettings.setObjectName(translate("MenuBar", "Settings"))
        if Universals.isActivePyKDE4==True:
            self.mHelpMenu = Universals.MainWindow.helpMenu()
            self.mHelpMenu.setObjectName(self.mHelpMenu.title())
            self.aHelpMenu = self.addMenu(self.mHelpMenu)
        else:
            self.mHelpMenu = self.addMenu(translate("MenuBar", "Help"))
            self.mHelpMenu.setObjectName(translate("MenuBar", "Help"))
        mExport = MMenu(translate("MenuBar", "Export"), self.mEdit)
        mExport.setObjectName(translate("MenuBar", "Export"))
        mExport.addAction(translate("MenuBar", "HTML Format")).setObjectName(translate("MenuBar", "HTML Format"))
        mExport.addAction(translate("MenuBar", "Text Format")).setObjectName(translate("MenuBar", "Text Format"))
        mExport.addAction(translate("MenuBar", "HTML Format (File Tree)")).setObjectName(translate("MenuBar", "HTML Format (File Tree)")) 
        mExport.addAction(translate("MenuBar", "Text Format (File Tree)")).setObjectName(translate("MenuBar", "Text Format (File Tree)")) 
        mShowInWindow = MMenu(translate("MenuBar", "Show In New Window"), self.mEdit)
        mShowInWindow.setObjectName(translate("MenuBar", "Show In New Window"))
        mShowInWindow.addAction(translate("MenuBar", "HTML Format")).setObjectName(translate("MenuBar", "HTML Format")) 
        mShowInWindow.addAction(translate("MenuBar", "Text Format")).setObjectName(translate("MenuBar", "Text Format"))
        mShowInWindow.addAction(translate("MenuBar", "HTML Format (File Tree)")).setObjectName(translate("MenuBar", "HTML Format (File Tree)")) 
        mShowInWindow.addAction(translate("MenuBar", "Text Format (File Tree)")).setObjectName(translate("MenuBar", "Text Format (File Tree)"))
        mCopyToClipBoard = MMenu(translate("MenuBar", "Copy To Clipboard"), self.mEdit)
        mCopyToClipBoard.setObjectName(translate("MenuBar", "Copy To Clipboard"))
        mCopyToClipBoard.addAction(translate("MenuBar", "HTML Format")).setObjectName(translate("MenuBar", "HTML Format")) 
        mCopyToClipBoard.addAction(translate("MenuBar", "Text Format")).setObjectName(translate("MenuBar", "Text Format"))
        mCopyToClipBoard.addAction(translate("MenuBar", "HTML Format (File Tree)")).setObjectName(translate("MenuBar", "HTML Format (File Tree)")) 
        mCopyToClipBoard.addAction(translate("MenuBar", "Text Format (File Tree)")).setObjectName(translate("MenuBar", "Text Format (File Tree)"))
        self.mFile.addAction(translate("MenuBar", "Open State")).setObjectName(translate("MenuBar", "Open State"))
        self.mFile.addAction(translate("MenuBar", "Save State")).setObjectName(translate("MenuBar", "Save State"))
        if Execute.isRunableAsRoot():
            mRunAsRoot = MMenu(translate("MenuBar", "Run As Root"), self.mFile)
            mRunAsRoot.addAction(translate("MenuBar", "With This Profile (My Settings)")).setObjectName(translate("MenuBar", "With This Profile (My Settings)")) 
            mRunAsRoot.addAction(translate("MenuBar", "With Root Profile (Own Settings)")).setObjectName(translate("MenuBar", "With Root Profile (Own Settings)")) 
            self.mFile.addMenu(mRunAsRoot)
        self.mFile.addAction(translate("MenuBar", "Quit")).setObjectName(translate("MenuBar", "Quit"))
        self.mEdit.addMenu(mExport)
        self.mEdit.addMenu(mShowInWindow)
        self.mEdit.addMenu(mCopyToClipBoard)
        self.mSettings.addAction(translate("MenuBar", "Options")).setObjectName(translate("MenuBar", "Options"))
        self.mSettings.addAction(translate("MenuBar", "My Plug-ins")).setObjectName(translate("MenuBar", "My Plug-ins"))
        self.mSettings.addAction(translate("MenuBar", "Reconfigure")).setObjectName(translate("MenuBar", "Reconfigure"))
        self.mSettings.addAction(translate("MenuBar", "My Plug-ins (System)")).setObjectName(translate("MenuBar", "My Plug-ins (System)"))
        if Universals.isActivePyKDE4==True:
            actReportBug = MAction(translate("MenuBar", "Report Bug"), self.mHelpMenu)
            actReportBug.setObjectName(translate("MenuBar", "Report Bug"))
            self.mHelpMenu.insertAction(self.mHelpMenu.actions()[3], actReportBug)
            actSuggestIdea = MAction(translate("MenuBar", "Suggest Idea"), self.mHelpMenu)
            actSuggestIdea.setObjectName(translate("MenuBar", "Suggest Idea"))
            self.mHelpMenu.insertAction(self.mHelpMenu.actions()[3], actSuggestIdea)
            actUNo = 9
            while actUNo>0:
                try:
                    actUpdate = MAction(translate("MenuBar", "Update"), self.mHelpMenu)
                    actUpdate.setObjectName(translate("MenuBar", "Update"))
                    self.mHelpMenu.insertAction(self.mHelpMenu.actions()[actUNo], actUpdate)
                    break
                except:actUNo = actUNo - 3
        else:
            self.mHelpMenu.addAction(translate("MenuBar", "Report Bug")).setObjectName(translate("MenuBar", "Report Bug"))
            self.mHelpMenu.addAction(translate("MenuBar", "Suggest Idea")).setObjectName(translate("MenuBar", "Suggest Idea"))
            self.mHelpMenu.addAction(translate("MenuBar", "Update")).setObjectName(translate("MenuBar", "Update"))
            self.mHelpMenu.addAction(translate("MenuBar", "About Hamsi Manager")).setObjectName(translate("MenuBar", "About Hamsi Manager"))
        self.mHelpMenu.addAction(translate("MenuBar", "About QT")).setObjectName(translate("MenuBar", "About QT"))

        MObject.connect(self, SIGNAL("triggered(QAction *)"), self.click)
        
    def click(self, _action):
        Universals.MainWindow.Bars.click(_action, True)
        
    def refreshForTableType(self):
        if self.mMainPopupMenu==None:
            self.mMainPopupMenu = Universals.MainWindow.createPopupMenu()
            self.mMainPopupMenu.setTitle(translate("MenuBar", "Panels"))
            self.mMainPopupMenu.setParent(Universals.MainWindow)
            self.mMainPopupMenu.setObjectName(translate("MenuBar", "Panels"))
            if len(self.mView.actions())==0:
                self.mView.addMenu(self.mMainPopupMenu)
            else:
                self.mView.insertMenu(self.mView.actions()[0], self.mMainPopupMenu)
        else:
            mTemp = Universals.MainWindow.createPopupMenu()
            self.mMainPopupMenu.clear()
            self.mMainPopupMenu.addActions(mTemp.actions())
    
class Bars():
    global isClicked, changeTableType
    isClicked = False
    def __init__(self):
        Universals.MainWindow.MusicOptionsBar = None
        Universals.MainWindow.SubDirectoryOptionsBar = None
        
    def click(self, _action, _isFromMenu=False):
        try:
            actionName = _action.objectName()
            if actionName==translate("MenuBar", "Open State"):
                import os, Settings
                f = MFileDialog.getOpenFileName(Universals.activeWindow(),translate("MenuBar", "Open State"),
                                    Universals.userDirectoryPath,str(translate("MenuBar", "Application Runner") + " (*.desktop)").decode("utf-8"))
                if f!="":
                    Settings.openStateOfSettings(unicode(f, "utf-8"))
            elif actionName==translate("MenuBar", "Save State"):
                import Settings
                import os
                f = MFileDialog.getSaveFileName(Universals.activeWindow(),translate("MenuBar", "Save State"),Universals.userDirectoryPath + "/HamsiManager.desktop",str(translate("MenuBar", "Application Runner")).decode("utf-8") + u" (*.desktop)")
                if f!="":
                    Settings.saveStateOfSettings(unicode(f, "utf-8"))
                    Dialogs.show(translate("MenuBar", "Current State Saved"), 
                            translate("MenuBar", "Current state saved with preferences.<br>You can continue where you left off."))
            elif actionName==translate("MenuBar", "With This Profile (My Settings)"):
                import Execute, Settings
                if Execute.executeHamsiManagerAsRoot("-sDirectoryPath \"" + Settings.pathOfSettingsDirectory + "\""):
                    Universals.MainWindow.close()
                else:
                    Dialogs.showError(translate("MenuBar", "Can Not Run As Root"), translate("MenuBar", "Hamsi Manager can not run as root."))
            elif actionName==translate("MenuBar", "With Root Profile (Own Settings)"):
                import Execute
                if Execute.executeHamsiManagerAsRoot(""):
                    Universals.MainWindow.close()
                else:
                    Dialogs.showError(translate("MenuBar", "Can Not Run As Root"), translate("MenuBar", "Hamsi Manager can not run as root."))
            elif actionName==translate("MenuBar", "Quit"):
                Universals.MainWindow.close()
            elif actionName==translate("MenuBar", "HTML Format"):
                if _action.parent().objectName()==translate("MenuBar", "Export"):
                    Tables.exportTableValues("file", "html", "title")
                elif _action.parent().objectName()==translate("MenuBar", "Show In New Window"):
                    Tables.exportTableValues("dialog", "html", "title")
                elif _action.parent().objectName()==translate("MenuBar", "Copy To Clipboard"):
                    Tables.exportTableValues("clipboard", "html", "title")
            elif actionName==translate("MenuBar", "Text Format"):
                if _action.parent().objectName()==translate("MenuBar", "Export"):
                    Tables.exportTableValues("file", "plainText", "title")
                elif _action.parent().objectName()==translate("MenuBar", "Show In New Window"):
                    Tables.exportTableValues("dialog", "plainText", "title")
                elif _action.parent().objectName()==translate("MenuBar", "Copy To Clipboard"):
                    Tables.exportTableValues("clipboard", "plainText", "title")
            elif actionName==translate("MenuBar", "HTML Format (File Tree)"):
                if _action.parent().objectName()==translate("MenuBar", "Export"):
                    InputOutputs.getFileTree((Universals.MainWindow.FileManager.currentDirectory), 0, "file", "html", "title")
                elif _action.parent().objectName()==translate("MenuBar", "Show In New Window"):
                    InputOutputs.getFileTree((Universals.MainWindow.FileManager.currentDirectory), 0, "dialog", "html", "title")
                elif _action.parent().objectName()==translate("MenuBar", "Copy To Clipboard"):
                    InputOutputs.getFileTree((Universals.MainWindow.FileManager.currentDirectory), 0, "clipboard", "html", "title")
            elif actionName==translate("MenuBar", "Text Format (File Tree)"):
                if _action.parent().objectName()==translate("MenuBar", "Export"):
                    InputOutputs.getFileTree((Universals.MainWindow.FileManager.currentDirectory), 0, "file", "plainText", "title")
                elif _action.parent().objectName()==translate("MenuBar", "Show In New Window"):
                    InputOutputs.getFileTree((Universals.MainWindow.FileManager.currentDirectory), 0, "dialog", "plainText", "title")
                elif _action.parent().objectName()==translate("MenuBar", "Copy To Clipboard"):
                    InputOutputs.getFileTree((Universals.MainWindow.FileManager.currentDirectory), 0, "clipboard", "plainText", "title")
            elif actionName==translate("MenuBar", "Show Last Action"):
                Records.showInWindow()
            elif actionName==translate("MenuBar", "About QT"):
                if Universals.isActivePyKDE4==True:
                    QMessageBox.aboutQt(Universals.MainWindow, translate("MenuBar", "About QT"))
                else:
                    MMessageBox.aboutQt(Universals.MainWindow, translate("MenuBar", "About QT"))
            elif actionName==translate("MenuBar", "Options"):
                import Options
                Options.Options(Universals.MainWindow)
            elif actionName==translate("MenuBar", "My Plug-ins"):
                import MyPlugins
                MyPlugins.MyPlugins(Universals.MainWindow)
            elif actionName==translate("MenuBar", "Reconfigure"):
                import Execute
                Execute.executeReconfigure("-configurePage")
            elif actionName==translate("MenuBar", "My Plug-ins (System)"):
                import Execute
                Execute.executeReconfigure("-pluginPage -onlyRoot")
            elif actionName==translate("MenuBar", "Update"):
                import UpdateControl
                UpdateControl.UpdateControl(Universals.MainWindow)
            elif actionName==translate("MenuBar", "Report Bug"):
                error = ReportBug.ReportBug(True)
                error.show()
            elif actionName==translate("MenuBar", "Suggest Idea"):
                import SuggestIdea
                error = SuggestIdea.SuggestIdea()
                error.show()
            elif actionName==translate("MenuBar", "About Hamsi Manager"):
                if Universals.isActivePyKDE4==False:
                    MMessageBox.about(Universals.MainWindow, translate("MenuBar", "About Hamsi Manager"), Universals.aboutOfHamsiManager)
            elif _isFromMenu==False:
                if actionName==translate("Tables", "Show Also Previous Information"):
                    if Universals.MainWindow.Table.checkUnSavedTableValues()==True:
                        Universals.isShowOldValues = _action.isChecked()
                        Tables.refreshTable(InputOutputs.currentDirectoryPath)
                    else:
                        _action.setChecked(Universals.isShowOldValues)
                elif actionName==translate("Tables", "Ignore Selection"):
                    Universals.isChangeAll = _action.isChecked()
                    if _action.isChecked():
                        Universals.MainWindow.TableToolsBar.isChangeSelected.setEnabled(False)
                    else:
                        Universals.MainWindow.TableToolsBar.isChangeSelected.setEnabled(True)
                    Universals.MainWindow.StatusBar.fillSelectionInfo()
                elif actionName==translate("Tables", "Change Selected"):
                    Universals.isChangeSelected = _action.isChecked()
                    Universals.MainWindow.StatusBar.fillSelectionInfo()
                elif actionName==translate("ToolsBar", "Check Icon"):
                    Universals.MainWindow.setEnabled(False)
                    InputOutputs.checkIcon(InputOutputs.currentDirectoryPath)
                    Dialogs.show(translate("ToolsBar", "Directory Icon Checked"),
                            translate("ToolsBar", "Current directory icon checked.<br>The default action based on the data is executed."))
                    Universals.MainWindow.setEnabled(True)
                elif actionName==translate("ToolsBar", "Clear Empty Directories"):
                    if Universals.MainWindow.Table.checkUnSavedTableValues()==False:
                        _action.setChecked(False)
                        return False
                    answer = Dialogs.ask(translate("ToolsBar", "Empty Directories Will Be Removed"),
                            str(translate("ToolsBar", "Are you sure you want to remove empty directories based on the criteria you set in \"%s\"?")) % Organizer.getLink(InputOutputs.currentDirectoryPath))
                    if answer==Dialogs.Yes:
                        import FileManager
                        Universals.MainWindow.setEnabled(False)
                        InputOutputs.clearEmptyDirectories(InputOutputs.currentDirectoryPath, True, True)
                        Universals.MainWindow.setEnabled(True)
                        Dialogs.show(translate("ToolsBar", "Directory Cleaned"),
                            translate("ToolsBar", "The current directory is cleaned based on the criteria you set."))
                        Universals.MainWindow.FileManager.makeRefresh()
                elif actionName==translate("ToolsBar", "Pack"):
                    import Packager
                    Packager.Packager(InputOutputs.currentDirectoryPath)
                elif actionName==translate("ToolsBar", "Hash"):
                    import Hasher
                    Hasher.Hasher(InputOutputs.currentDirectoryPath)
                elif actionName==translate("ToolsBar", "Clear"):
                    import Cleaner
                    Cleaner.Cleaner(InputOutputs.currentDirectoryPath)
                elif actionName==translate("ToolsBar", "File Tree"):
                    import FileTreeBuilder
                    FileTreeBuilder.FileTreeBuilder(InputOutputs.currentDirectoryPath)
                elif actionName==translate("ToolsBar", "Run Command"):
                    try:
                        from PyQt4.Qsci import QsciScintilla
                    except:
                        Dialogs.showError(translate("MenuBar", "Qsci Is Not Installed"), 
                                translate("MenuBar", "Qsci is not installed on your systems.<br>Please install Qsci on your system and try again."))
                    else:
                        import RunCommand
                        RunCommand.RunCommand(Universals.MainWindow)
                elif actionName==translate("ToolsBar", "Remove Sub Files"):
                    answer = Dialogs.ask(translate("ToolsBar", "All Files Will Be Removed"),
                            str(translate("ToolsBar", "Are you sure you want to remove only all files in \"%s\"?<br>Note:Do not will remove directory and subfolders.")) % Organizer.getLink(InputOutputs.currentDirectoryPath))
                    if answer==Dialogs.Yes:
                        Universals.MainWindow.setEnabled(False)
                        InputOutputs.removeOnlySubFiles(InputOutputs.currentDirectoryPath)
                        Universals.MainWindow.setEnabled(True)
                        Dialogs.show(translate("ToolsBar", "Removed Only All Files"),
                            str(translate("ToolsBar", "Removed only all files in \"%s\".<br>Note:Do not removed directory and subfolders.")) % Organizer.getLink(InputOutputs.currentDirectoryPath))
            Records.saveAllRecords()
        except:
            error = ReportBug.ReportBug()
            error.show()
    
    def refreshBars(self):
        Universals.MainWindow.Table = Tables.Tables(Universals.MainWindow)
        try:Universals.MainWindow.removeDockWidget(Universals.MainWindow.dckSpecialTools)
        except:pass
        Universals.MainWindow.SpecialTools = SpecialTools.SpecialTools(Universals.MainWindow)
        Universals.MainWindow.Menu.mSpecialOptions.clear()
        if Universals.tableType==2:
            Universals.MainWindow.PlayerBar = PlayerBar(Universals.MainWindow)
            Universals.MainWindow.addToolBar(Mt.TopToolBarArea,Universals.MainWindow.PlayerBar)
            Universals.MainWindow.MusicOptionsBar = MusicOptionsBar(Universals.MainWindow)
            Universals.MainWindow.addToolBar(Mt.TopToolBarArea,Universals.MainWindow.MusicOptionsBar)
            Universals.MainWindow.MusicOptionsBar.getSpecialOptions(Universals.MainWindow.Menu.mSpecialOptions)
        elif Universals.tableType==3:
            Universals.MainWindow.SubDirectoryOptionsBar = SubDirectoryOptionsBar(Universals.MainWindow)
            Universals.MainWindow.addToolBar(Mt.TopToolBarArea,Universals.MainWindow.SubDirectoryOptionsBar)
            Universals.MainWindow.SubDirectoryOptionsBar.getSpecialOptions(Universals.MainWindow.Menu.mSpecialOptions)
        elif Universals.tableType==4:
            Universals.MainWindow.CoverOptionsBar = CoverOptionsBar(Universals.MainWindow)
            Universals.MainWindow.addToolBar(Mt.TopToolBarArea,Universals.MainWindow.CoverOptionsBar)
            Universals.MainWindow.CoverOptionsBar.getSpecialOptions(Universals.MainWindow.Menu.mSpecialOptions)
        if len(Universals.MainWindow.Menu.mSpecialOptions.actions())==0:
            Universals.MainWindow.Menu.mSpecialOptions.setEnabled(False)
        else:
            Universals.MainWindow.Menu.mSpecialOptions.setEnabled(True)
        Universals.MainWindow.Menu.refreshForTableType()
    
    def changeTableType(_action):
        try:
            selectedType = Universals.getThisTableType(_action.objectName())
            if _action.isChecked() and Universals.tableType != selectedType:
                if Universals.MainWindow.Table.checkUnSavedTableValues()==False:
                    _action.setChecked(False)
                    return False
                Universals.setMySetting(Universals.MainWindow.Table.hiddenTableColumnsSettingKey,Universals.MainWindow.Table.hiddenTableColumns)
                if Universals.tableType==2:
                    Universals.MainWindow.removeToolBar(Universals.MainWindow.PlayerBar)
                    Universals.MainWindow.PlayerBar.deleteLater()
                    Universals.MainWindow.PlayerBar = None
                    Universals.MainWindow.removeToolBar(Universals.MainWindow.MusicOptionsBar)
                    Universals.MainWindow.MusicOptionsBar.deleteLater()
                    Universals.MainWindow.MusicOptionsBar = None
                elif Universals.tableType==3:
                    Universals.MainWindow.removeToolBar(Universals.MainWindow.SubDirectoryOptionsBar)
                    Universals.MainWindow.SubDirectoryOptionsBar.deleteLater()
                    Universals.MainWindow.SubDirectoryOptionsBar = None
                elif Universals.tableType==4:
                    Universals.MainWindow.removeToolBar(Universals.MainWindow.CoverOptionsBar)
                    Universals.MainWindow.CoverOptionsBar.deleteLater()
                    Universals.MainWindow.CoverOptionsBar = None
                Universals.clearAllChilds(Universals.MainWindow.CentralWidget)
                Universals.tableType = selectedType
                Universals.MainWindow.Bars.refreshBars()
                Universals.MainWindow.FileManager.makeRefresh()
            else:
                _action.setChecked(True)
        except:
            error = ReportBug.ReportBug()
            error.show()
    
    def getAllBarsStyleFromMySettings(self):
        Universals.MainWindow.TableToolsBar.setToolButtonStyle(int(Universals.MySettings["TableToolsBarButtonStyle"]))
        Universals.MainWindow.ToolsBar.setToolButtonStyle(int(Universals.MySettings["ToolsBarButtonStyle"]))
        if Universals.tableType==2:
            Universals.MainWindow.PlayerBar.setToolButtonStyle(int(Universals.MySettings["PlayerBarButtonStyle"]))
            Universals.MainWindow.MusicOptionsBar.setToolButtonStyle(int(Universals.MySettings["MusicOptionsBarButtonStyle"]))
        elif Universals.tableType==3:
            Universals.MainWindow.SubDirectoryOptionsBar.setToolButtonStyle(int(Universals.MySettings["SubDirectoryOptionsBarButtonStyle"]))
        elif Universals.tableType==4:
            Universals.MainWindow.CoverOptionsBar.setToolButtonStyle(int(Universals.MySettings["CoverOptionsBarButtonStyle"]))
        
    def setAllBarsStyleToMySettings(self):
        Universals.setMySetting("TableToolsBarButtonStyle", Universals.MainWindow.TableToolsBar.toolButtonStyle())
        Universals.setMySetting("ToolsBarButtonStyle", Universals.MainWindow.ToolsBar.toolButtonStyle())
        if Universals.tableType==2:
            Universals.setMySetting("PlayerBarButtonStyle", Universals.MainWindow.PlayerBar.toolButtonStyle())
            Universals.setMySetting("MusicOptionsBarButtonStyle", Universals.MainWindow.MusicOptionsBar.toolButtonStyle())
        elif Universals.tableType==3:
            Universals.setMySetting("SubDirectoryOptionsBarButtonStyle", Universals.MainWindow.SubDirectoryOptionsBar.toolButtonStyle())
        elif Universals.tableType==4:
            Universals.setMySetting("CoverOptionsBarButtonStyle", Universals.MainWindow.CoverOptionsBar.toolButtonStyle())
        
    
class TableToolsBar(MToolBar):
    global isClicked, actsFileReNamerTypes, changeReNamerType
    def __init__(self, _parent):
        global actsFileReNamerTypes
        MToolBar.__init__(self, _parent)
        _parent.addToolBar(Mt.TopToolBarArea,self)
        self.setWindowTitle(translate("TableToolsBar", "Table Tools"))
        self.setObjectName(translate("TableToolsBar", "Table Tools"))
        self.isShowOldValues = MAction(MIcon(u"Images:showOldValues.png"),
                        translate("Tables", "Show Also Previous Information"),self)
        self.isShowOldValues.setObjectName(translate("Tables", "Show Also Previous Information"))
        self.isShowOldValues.setToolTip(translate("Tables", "Show Also Previous Information"))
        self.isShowOldValues.setCheckable(True)
        self.isShowOldValues.setChecked(Universals.isShowOldValues)
        self.isChangeAll = MAction(MIcon(u"Images:changeAll.png"),
                        translate("Tables", "Ignore Selection"),self)
        self.isChangeAll.setObjectName(translate("Tables", "Ignore Selection"))
        self.isChangeAll.setToolTip(translate("Tables", "Ignore Selection"))
        self.isChangeAll.setCheckable(True)
        self.isChangeAll.setChecked(Universals.isChangeAll)
        self.isChangeSelected = MAction(MIcon(u"Images:changeSelected.png"),
                        translate("Tables", "Change Selected"),self)
        self.isChangeSelected.setObjectName(translate("Tables", "Change Selected"))
        self.isChangeSelected.setToolTip(translate("Tables", "Change Selected"))
        self.isChangeSelected.setCheckable(True)
        self.isChangeSelected.setChecked(Universals.isChangeSelected)
        if self.isChangeAll.isChecked():
            self.isChangeSelected.setEnabled(False)
        actgActionGroupTableTypes = MActionGroup(self)
        for x, name in enumerate(Universals.tableTypesNames):
            a = actgActionGroupTableTypes.addAction(MIcon(u"Images:"+Universals.tableTypeIcons[x]),
                                        name)
            a.setCheckable(True)
            a.setObjectName(name)
            if Universals.tableType==Universals.getThisTableType(name):
                a.setChecked(True)
        self.addActions(actgActionGroupTableTypes.actions())
        MObject.connect(actgActionGroupTableTypes, SIGNAL("selected(QAction *)"), changeTableType)
        self.addSeparator()
        self.fileReNamerTypeNames = [str(translate("ToolsBar", "Personal Computer")), 
                                    str(translate("ToolsBar", "Web Server")), 
                                    str(translate("ToolsBar", "Removable Media"))]
        buttonIcons = ["personalComputer.png", "webServer.png", "removableMedia.png"]
        actgActionGroupReNamerTypes = MActionGroup(self)
        actsFileReNamerTypes = []
        for x, name in enumerate(self.fileReNamerTypeNames):
            actsFileReNamerTypes.append(MAction(MIcon(u"Images:"+buttonIcons[x].decode("utf-8")),name.decode("utf-8"),self))
            actsFileReNamerTypes[-1].setObjectName(name.decode("utf-8"))
            actsFileReNamerTypes[x].setToolTip(str(translate("ToolsBar", "Renames files and folders in \"%s\" format.")) % (name.decode("utf-8")))
            actsFileReNamerTypes[x].setCheckable(True)
            actgActionGroupReNamerTypes.addAction(actsFileReNamerTypes[x])
            if Universals.MySettings["fileReNamerType"]==Universals.fileReNamerTypeNamesKeys[x]:
                actsFileReNamerTypes[x].setChecked(True)
        if Universals.fileReNamerTypeNamesKeys.count(str(Universals.MySettings["fileReNamerType"]))==0:
            actsFileReNamerTypes[0].setChecked(True)
        self.addActions(actgActionGroupReNamerTypes.actions())
        MObject.connect(actgActionGroupReNamerTypes, SIGNAL("selected(QAction *)"), changeReNamerType)
        self.addSeparator()
        self.addAction(self.isShowOldValues)
        self.addAction(self.isChangeAll)
        self.addAction(self.isChangeSelected)
        if Universals.windowMode==Universals.windowModeKeys[1]:
            self.setIconSize(MSize(16,16))
        else:
            self.setIconSize(MSize(32,32))
        Universals.MainWindow.Menu.mSpecialOptions = MMenu(translate("MenuBar", "Special Options"), self)
        Universals.MainWindow.Menu.mSpecialOptions.setObjectName(translate("MenuBar", "Special Options"))
        Universals.MainWindow.Menu.mSpecialOptions.setTitle(translate("MenuBar", "Special Options"))
        Universals.MainWindow.Menu.mTableTools = MMenu(translate("MenuBar", "Table Tools"), self)
        Universals.MainWindow.Menu.mTableTools.setObjectName(translate("MenuBar", "Table Tools"))
        Universals.MainWindow.Menu.mTableTools.addMenu(Universals.MainWindow.Menu.mSpecialOptions)
        Universals.MainWindow.Menu.mTableTools.addActions(actgActionGroupTableTypes.actions())
        Universals.MainWindow.Menu.mTableTools.addSeparator()
        Universals.MainWindow.Menu.mTableTools.addActions(actgActionGroupReNamerTypes.actions())
        Universals.MainWindow.Menu.mTableTools.addSeparator()
        Universals.MainWindow.Menu.mTableTools.addAction(self.isShowOldValues)
        Universals.MainWindow.Menu.mTableTools.addAction(self.isChangeAll)
        Universals.MainWindow.Menu.mTableTools.addAction(self.isChangeSelected)
        Universals.MainWindow.Menu.insertMenu(Universals.MainWindow.Menu.mTools.menuAction(), Universals.MainWindow.Menu.mTableTools)
        Universals.MainWindow.Menu.mView.addActions(actgActionGroupTableTypes.actions())
        MObject.connect(self, SIGNAL("actionTriggered(QAction *)"), Universals.MainWindow.Bars.click)
        
    def changeReNamerType(_action, _isFromMenu=False):
        try:
            if Universals.MainWindow.Table.checkUnSavedTableValues()==False:
                _action.setChecked(False)
                for x, typeName in enumerate(Universals.fileReNamerTypeNamesKeys):
                    if typeName == Universals.MySettings["fileReNamerType"]:
                        actsFileReNamerTypes[x].setChecked(True)
                return False
            for x, typeName in enumerate(Universals.fileReNamerTypeNamesKeys):
                if actsFileReNamerTypes[x].isChecked():
                    Universals.setMySetting("fileReNamerType", typeName)
            Universals.MainWindow.FileManager.makeRefresh()
        except:
            error = ReportBug.ReportBug()
            error.show()
 
class ToolsBar(MToolBar):
    def __init__(self, _parent):
        MToolBar.__init__(self, _parent)
        _parent.addToolBar(Mt.TopToolBarArea,self)
        self.setWindowTitle(translate("ToolsBar", "Tools"))
        self.setObjectName(translate("ToolsBar", "Tools"))
        self.clearEmptyDirectories = MAction(MIcon("Images:clearEmptyDirectories.png"),
                                                translate("ToolsBar", "Clear Empty Directories"),self)
        self.clearEmptyDirectories.setObjectName(translate("ToolsBar", "Clear Empty Directories"))
        self.clearEmptyDirectories.setToolTip(translate("ToolsBar", "Clears the folder contents based on the criteria set."))
        self.actCheckIcon = MAction(MIcon("Images:checkIcon.png"),
                                                translate("ToolsBar", "Check Icon"),self)
        self.actCheckIcon.setObjectName(translate("ToolsBar", "Check Icon"))
        self.actCheckIcon.setToolTip(translate("ToolsBar", "Checks the icon for the folder you are currently in."))
        self.actHash = MAction(MIcon("Images:hash.png"),
                                                translate("ToolsBar", "Hash"),self)
        self.actHash.setObjectName(translate("ToolsBar", "Hash"))
        self.actHash.setToolTip(translate("ToolsBar", "Hash manager"))
        self.actPack = MAction(MIcon("Images:pack.png"),
                                                translate("ToolsBar", "Pack"),self)
        self.actPack.setObjectName(translate("ToolsBar", "Pack"))
        self.actPack.setToolTip(translate("ToolsBar", "Packs the current folder."))
        self.actFileTree = MAction(MIcon("Images:fileTree.png"),
                                                translate("ToolsBar", "File Tree"),self)
        self.actFileTree.setObjectName(translate("ToolsBar", "File Tree"))
        self.actFileTree.setToolTip(translate("ToolsBar", "Get file tree of current folder."))
        self.actClear = MAction(MIcon("Images:clear.png"),
                                                translate("ToolsBar", "Clear"),self)
        self.actClear.setObjectName(translate("ToolsBar", "Clear"))
        self.actClear.setToolTip(translate("ToolsBar", "Clears the current folder."))
        self.actRemoveOnlySubFiles = MAction(MIcon("Images:removeOnlySubFiles.png"),
                                                translate("ToolsBar", "Remove Sub Files"),self)
        self.actRemoveOnlySubFiles.setObjectName(translate("ToolsBar", "Remove Sub Files"))
        self.actRemoveOnlySubFiles.setToolTip(translate("ToolsBar", "Remove only all sub files.Do not will remove directory and subfolders."))
        self.actRunCommand = MAction(MIcon("Images:runCommand.png"),
                                                translate("ToolsBar", "Run Command"),self)
        self.actRunCommand.setObjectName(translate("ToolsBar", "Run Command"))
        self.actRunCommand.setToolTip(translate("ToolsBar", "You can coding some things."))
        self.addAction(self.actHash)
        self.addAction(self.actPack)
        self.addAction(self.actFileTree)
        self.addAction(self.actClear)
        self.addAction(self.actRunCommand)
        self.addSeparator()
        self.addAction(self.clearEmptyDirectories)
        self.addAction(self.actRemoveOnlySubFiles)
        self.addAction(self.actCheckIcon)
        if Universals.windowMode==Universals.windowModeKeys[1]:
            self.setIconSize(MSize(16,16))
        else:
            self.setIconSize(MSize(32,32))
        Universals.MainWindow.Menu.mTools = MMenu(translate("MenuBar", "Tools"), self)
        Universals.MainWindow.Menu.mTools.setObjectName(translate("MenuBar", "Tools"))
        Universals.MainWindow.Menu.mTools.addAction(self.actHash)
        Universals.MainWindow.Menu.mTools.addAction(self.actPack)
        Universals.MainWindow.Menu.mTools.addAction(self.actFileTree)
        Universals.MainWindow.Menu.mTools.addAction(self.actClear)
        Universals.MainWindow.Menu.mTools.addAction(self.actRunCommand)
        Universals.MainWindow.Menu.mTools.addSeparator()
        Universals.MainWindow.Menu.mTools.addAction(self.clearEmptyDirectories)
        Universals.MainWindow.Menu.mTools.addAction(self.actRemoveOnlySubFiles)
        Universals.MainWindow.Menu.mTools.addAction(self.actCheckIcon)
        Universals.MainWindow.Menu.insertMenu(Universals.MainWindow.Menu.mSettings.menuAction(), Universals.MainWindow.Menu.mTools)
        MObject.connect(self, SIGNAL("actionTriggered(QAction *)"), Universals.MainWindow.Bars.click)
        self.refreshQuickOptions()
        
    def refreshQuickOptions(self):
        if Universals.MainWindow.Menu.mQuickOptions!=None:
            Universals.MainWindow.Menu.removeAction(Universals.MainWindow.Menu.mQuickOptions.menuAction())
        Universals.MainWindow.Menu.mQuickOptions = Options.QuickOptions(self)
        Universals.MainWindow.Menu.insertMenu(Universals.MainWindow.Menu.mSettings.menuAction(), Universals.MainWindow.Menu.mQuickOptions)

class PlayerBar(MToolBar):
    def __init__(self, _parent):
        import Player
        MToolBar.__init__(self, _parent)
        self.setWindowTitle(translate("PlayerBar", "Player Bar"))
        self.setObjectName(translate("PlayerBar", "Player Bar"))
        self.Player = Player.Player(self, "bar")
        self.addWidget(self.Player)
        
class MusicOptionsBar(MToolBar):
    def __init__(self, _parent):
        MToolBar.__init__(self, _parent)
        self.isActiveChanging = True
        self.cbMusicTagTypeForMenu = None
        self.setWindowTitle(translate("MusicOptionsBar", "Music options"))
        self.setObjectName(translate("MusicOptionsBar", "Music options"))
        lblDetails = translate("MusicOptionsBar", "You can select the ID3 tag you want to see and edit.<br><font color=blue>ID3 V2 is recommended.</font>")
        self.MusicTagTypes = ["ID3 V1", "ID3 V2"]
        self.cbMusicTagType = MComboBox(self)
        self.cbMusicTagType.addItems(self.MusicTagTypes)
        self.isActiveChanging = False
        self.cbMusicTagType.setCurrentIndex(self.cbMusicTagType.findText(Universals.MySettings["musicTagType"]))
        self.isActiveChanging = True
        self.cbMusicTagType.setToolTip(lblDetails)
        self.addWidget(self.cbMusicTagType)
        MObject.connect(self.cbMusicTagType, SIGNAL("currentIndexChanged(int)"), self.musicTagTypeChanged)
        self.setIconSize(MSize(32,32))
    
    def musicTagTypeChanged(self, _action=None):
        try:
            selectedType = str(self.MusicTagTypes[_action])
            if self.isActiveChanging:
                if Universals.MainWindow.Table.checkUnSavedTableValues()==True:
                    Universals.setMySetting("musicTagType", selectedType)
                    Tables.refreshForTableColumns()
                    Universals.MainWindow.SpecialTools.refreshForTableColumns()
                    Tables.refreshTable(InputOutputs.currentDirectoryPath)
                self.isActiveChanging = False
                self.cbMusicTagType.setCurrentIndex(self.cbMusicTagType.findText(Universals.MySettings["musicTagType"]))
                if self.cbMusicTagTypeForMenu != None:
                    self.cbMusicTagTypeForMenu.setCurrentIndex(self.cbMusicTagTypeForMenu.findText(Universals.MySettings["musicTagType"]))
                self.isActiveChanging = True
        except:
            error = ReportBug.ReportBug()
            error.show()
        
    def getSpecialOptions(self, _menu):
        self.cbMusicTagTypeForMenu = MComboBox(self)
        self.cbMusicTagTypeForMenu.addItems(self.MusicTagTypes)
        self.isActiveChanging = False
        self.cbMusicTagTypeForMenu.setCurrentIndex(self.cbMusicTagTypeForMenu.findText(Universals.MySettings["musicTagType"]))
        self.isActiveChanging = True
        MObject.connect(self.cbMusicTagTypeForMenu, SIGNAL("currentIndexChanged(int)"), self.musicTagTypeChanged)
        wactLabel = MWidgetAction(_menu)
        wactLabel.setDefaultWidget(MLabel(translate("MusicOptionsBar", "ID3 Version") + u" : "))
        wact = MWidgetAction(_menu)
        wact.setDefaultWidget(self.cbMusicTagTypeForMenu)
        _menu.addAction(wactLabel)
        _menu.addAction(wact)
        
class SubDirectoryOptionsBar(MToolBar):
    def __init__(self, _parent):
        MToolBar.__init__(self, _parent)
        self.isActiveChanging = True
        self.cbSubDirectoryDeepForMenu = None
        self.setWindowTitle(translate("SubDirectoryOptionsBar", "Sub Directory Options"))
        self.setObjectName(translate("SubDirectoryOptionsBar", "Sub Directory Options"))
        lblDetails = translate("SubDirectoryOptionsBar", "You can select sub directory deep.<br><font color=blue>You can select \"-1\" for all sub directories.</font>")
        lblSubDirectoryDeep = MLabel(translate("SubDirectoryOptionsBar", "Deep") + u" : ")
        self.SubDirectoryDeeps = [ str(x) for x in range(-1, 10) ]
        self.cbSubDirectoryDeep = MComboBox(self)
        self.cbSubDirectoryDeep.addItems(self.SubDirectoryDeeps)
        self.isActiveChanging = False
        self.cbSubDirectoryDeep.setCurrentIndex(self.cbSubDirectoryDeep.findText(Universals.MySettings["subDirectoryDeep"]))
        self.isActiveChanging = True
        self.cbSubDirectoryDeep.setToolTip(lblDetails)
        pnlSubDirectoryDeep = MWidget()
        hblSubDirectoryDeep = MHBoxLayout(pnlSubDirectoryDeep)
        hblSubDirectoryDeep.addWidget(lblSubDirectoryDeep)
        hblSubDirectoryDeep.addWidget(self.cbSubDirectoryDeep)
        pnlSubDirectoryDeep.setLayout(hblSubDirectoryDeep)
        self.addWidget(pnlSubDirectoryDeep)
        MObject.connect(self.cbSubDirectoryDeep, SIGNAL("currentIndexChanged(int)"), self.subDirectoryDeepChanged)
        self.setIconSize(MSize(32,32))
    
    def subDirectoryDeepChanged(self, _action=None):
        try:
            selectedDeep = str(self.SubDirectoryDeeps[_action])
            if self.isActiveChanging:
                if Universals.MainWindow.Table.checkUnSavedTableValues()==True:
                    Universals.setMySetting("subDirectoryDeep", int(selectedDeep))
                    Tables.refreshForTableColumns()
                    Universals.MainWindow.SpecialTools.refreshForTableColumns()
                    Tables.refreshTable(InputOutputs.currentDirectoryPath)
                self.isActiveChanging = False
                self.cbSubDirectoryDeep.setCurrentIndex(self.cbSubDirectoryDeep.findText(str(Universals.MySettings["subDirectoryDeep"])))
                if self.cbSubDirectoryDeepForMenu != None:
                    self.cbSubDirectoryDeepForMenu.setCurrentIndex(self.cbSubDirectoryDeepForMenu.findText(str(Universals.MySettings["subDirectoryDeep"])))
                self.isActiveChanging = True
        except:
            error = ReportBug.ReportBug()
            error.show()
            
    def getSpecialOptions(self, _menu):
        self.cbSubDirectoryDeepForMenu = MComboBox(self)
        self.cbSubDirectoryDeepForMenu.addItems(self.SubDirectoryDeeps)
        self.isActiveChanging = False
        self.cbSubDirectoryDeepForMenu.setCurrentIndex(self.cbSubDirectoryDeepForMenu.findText(str(Universals.MySettings["subDirectoryDeep"])))
        self.isActiveChanging = True
        MObject.connect(self.cbSubDirectoryDeepForMenu, SIGNAL("currentIndexChanged(int)"), self.subDirectoryDeepChanged)
        wactLabel = MWidgetAction(_menu)
        wactLabel.setObjectName(translate("SubDirectoryOptionsBar", "Label Deep") + u" : ")
        wactLabel.setDefaultWidget(MLabel(translate("SubDirectoryOptionsBar", "Deep") + u" : "))
        wact = MWidgetAction(_menu)
        wact.setObjectName(translate("SubDirectoryOptionsBar", "Deep") + u" : ")
        wact.setDefaultWidget(self.cbSubDirectoryDeepForMenu)
        _menu.addAction(wactLabel)
        _menu.addAction(wact)
        
class CoverOptionsBar(MToolBar):
    def __init__(self, _parent):
        MToolBar.__init__(self, _parent)
        self.isActiveChanging = True
        self.cbSubDirectoryDeepForMenu = None
        self.setWindowTitle(translate("CoverOptionsBar", "Cover Options"))
        self.setObjectName(translate("CoverOptionsBar", "Cover Options"))
        lblDetails = translate("CoverOptionsBar", "You can select sub directory deep.<br><font color=blue>You can select \"-1\" for all sub directories.</font>")
        lblSubDirectoryDeep = MLabel(translate("CoverOptionsBar", "Deep") + u" : ")
        self.SubDirectoryDeeps = [ str(x) for x in range(-1, 10) if x!=0 ]
        self.cbSubDirectoryDeep = MComboBox(self)
        self.cbSubDirectoryDeep.addItems(self.SubDirectoryDeeps)
        self.isActiveChanging = False
        self.cbSubDirectoryDeep.setCurrentIndex(self.cbSubDirectoryDeep.findText(Universals.MySettings["CoversSubDirectoryDeep"]))
        self.isActiveChanging = True
        self.cbSubDirectoryDeep.setToolTip(lblDetails)
        pnlSubDirectoryDeep = MWidget()
        hblSubDirectoryDeep = MHBoxLayout(pnlSubDirectoryDeep)
        hblSubDirectoryDeep.addWidget(lblSubDirectoryDeep)
        hblSubDirectoryDeep.addWidget(self.cbSubDirectoryDeep)
        pnlSubDirectoryDeep.setLayout(hblSubDirectoryDeep)
        self.addWidget(pnlSubDirectoryDeep)
        MObject.connect(self.cbSubDirectoryDeep, SIGNAL("currentIndexChanged(int)"), self.coverDeepChanged)
        self.setIconSize(MSize(32,32))
    
    def coverDeepChanged(self, _action=None):
        try:
            selectedDeep = str(self.SubDirectoryDeeps[_action])
            if self.isActiveChanging:
                if Universals.MainWindow.Table.checkUnSavedTableValues()==True:
                    Universals.setMySetting("CoversSubDirectoryDeep", int(selectedDeep))
                    Tables.refreshForTableColumns()
                    Universals.MainWindow.SpecialTools.refreshForTableColumns()
                    Tables.refreshTable(InputOutputs.currentDirectoryPath)
                self.isActiveChanging = False
                self.cbSubDirectoryDeep.setCurrentIndex(self.cbSubDirectoryDeep.findText(str(Universals.MySettings["CoversSubDirectoryDeep"])))
                if self.cbSubDirectoryDeepForMenu != None:
                    self.cbSubDirectoryDeepForMenu.setCurrentIndex(self.cbSubDirectoryDeepForMenu.findText(str(Universals.MySettings["CoversSubDirectoryDeep"])))
                self.isActiveChanging = True
        except:
            error = ReportBug.ReportBug()
            error.show()
        
            
    def getSpecialOptions(self, _menu):
        self.cbSubDirectoryDeepForMenu = MComboBox(self)
        self.cbSubDirectoryDeepForMenu.addItems(self.SubDirectoryDeeps)
        self.isActiveChanging = False
        self.cbSubDirectoryDeepForMenu.setCurrentIndex(self.cbSubDirectoryDeepForMenu.findText(str(Universals.MySettings["CoversSubDirectoryDeep"])))
        self.isActiveChanging = True
        MObject.connect(self.cbSubDirectoryDeepForMenu, SIGNAL("currentIndexChanged(int)"), self.coverDeepChanged)
        wactLabel = MWidgetAction(_menu)
        wactLabel.setObjectName(translate("CoverOptionsBar", "Label Deep") + u" : ")
        wactLabel.setDefaultWidget(MLabel(translate("CoverOptionsBar", "Deep") + u" : "))
        wact = MWidgetAction(_menu)
        wact.setObjectName(translate("CoverOptionsBar", "Deep") + u" : ")
        wact.setDefaultWidget(self.cbSubDirectoryDeepForMenu)
        _menu.addAction(wactLabel)
        _menu.addAction(wact)
        
class StatusBar(MStatusBar):
    
    def __init__(self, _parent):
        MStatusBar.__init__(self, _parent)
        import Execute
        if Execute.isRunningAsRoot():
            lblInfo = MLabel(u"<span style=\"color: #FF0000\">" + translate("StatusBar", "Hamsi Manager running as root")+u"</span>")
            self.addWidget(lblInfo)
        if Universals.isDebugMode:
            lblInfo = MLabel(translate("StatusBar", "Debug Mode"))
            self.addWidget(lblInfo)
        self.lblInfo = MLabel(u"")
        self.hideInfo()
        self.addWidget(self.lblInfo)
        self.prgbState = MProgressBar()
        self.prgbState.setMinimumWidth(200)
        self.prgbState.setVisible(False)
        self.addWidget(self.prgbState)
        self.addWidget(MLabel(""), 100)
        self.lblImportantInfo = MLabel(u"")
        self.addWidget(self.lblImportantInfo)
        self.fillSelectionInfo()
    
    def showInfo(self, _info):
        self.lblInfo.setText(_info)
        self.lblInfo.setVisible(True)
    
    def hideInfo(self):
        self.lblInfo.setText(u"")
        self.lblInfo.setVisible(False)
    
    def clearImportantInfo(self):
        self.lblImportantInfo.setText(u"")
    
    def setImportantInfo(self, _info):
        self.lblImportantInfo.setText(u"<span style=\"color: #FF0000\">" + _info + u"</span>")
            
    def fillSelectionInfo(self):
        if Universals.isChangeAll:
            self.setImportantInfo(translate("Tables", "All informations will be change"))
        else:
            if Universals.isChangeSelected:
                self.setImportantInfo(translate("Tables", "Selected informations will change only"))
            else:
                self.setImportantInfo(translate("Tables", "Selected informations will not change"))
        
    def showState(self, _title, _value=0, _maxValue=100):
        MApplication.processEvents()
        Universals.MainWindow.lockForm()
        self.prgbState.setVisible(True)
        self.prgbState.setRange(0, _maxValue)
        self.prgbState.setValue(_value)
        self.showInfo(_title+" ( "+str(_value)+" / "+str(_maxValue)+" )")
        if _value==_maxValue:
            self.hideInfo()
            self.prgbState.setVisible(False)
            self.prgbState.setRange(0, 100)
            Universals.MainWindow.unlockForm()
        
        
        
