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

class MenuBar(MMenuBar):
    
    def __init__(self, _parent):
        MMenuBar.__init__(self, _parent)
        self.menus = []
        self.menus.append(MMenu(translate("MenuBar", "File"), self))
        self.menus[-1].setObjectName(translate("MenuBar", "File"))
        self.menus.append(MMenu(translate("MenuBar", "Edit"), self))
        self.menus[-1].setObjectName(translate("MenuBar", "Edit"))
        self.menus.append(MMenu(translate("MenuBar", "View"), self))
        self.menus[-1].setObjectName(translate("MenuBar", "View"))
        if Universals.getBoolValue("isSaveActions"):
            self.menus.append(MMenu(translate("MenuBar", "Actions"), self))
            self.menus[-1].addAction(translate("MenuBar", "Show Last Action")).setObjectName(translate("MenuBar", "Show Last Action"))
            self.menus[-1].setObjectName(translate("MenuBar", "Actions"))
        self.menus.append(MMenu(translate("MenuBar", "Tools"), self))
        self.menus[-1].setObjectName(translate("MenuBar", "Tools"))
        self.menus.append(MMenu(translate("MenuBar", "Settings"), self))
        self.menus[-1].setObjectName(translate("MenuBar", "Settings"))
        if Universals.isActivePyKDE4==True:
            mAboutOfHamsiManager = Universals.MainWindow.helpMenu()
            self.menus.append(mAboutOfHamsiManager)
            self.menus[-1].setObjectName(mAboutOfHamsiManager.title())
        else:
            self.menus.append(MMenu(translate("MenuBar", "Help"), self))
            self.menus[-1].setObjectName(translate("MenuBar", "Help"))
        mExport = MMenu(translate("MenuBar", "Export"), self.menus[1])
        mExport.setObjectName(translate("MenuBar", "Export"))
        mExport.addAction(translate("MenuBar", "HTML Format")).setObjectName(translate("MenuBar", "HTML Format"))
        mExport.addAction(translate("MenuBar", "Text Format")).setObjectName(translate("MenuBar", "Text Format"))
        mExport.addAction(translate("MenuBar", "HTML Format (File Tree)")).setObjectName(translate("MenuBar", "HTML Format (File Tree)")) 
        mExport.addAction(translate("MenuBar", "Text Format (File Tree)")).setObjectName(translate("MenuBar", "Text Format (File Tree)")) 
        mShowInWindow = MMenu(translate("MenuBar", "Show In New Window"), self.menus[1])
        mShowInWindow.setObjectName(translate("MenuBar", "Show In New Window"))
        mShowInWindow.addAction(translate("MenuBar", "HTML Format")).setObjectName(translate("MenuBar", "HTML Format")) 
        mShowInWindow.addAction(translate("MenuBar", "Text Format")).setObjectName(translate("MenuBar", "Text Format"))
        mShowInWindow.addAction(translate("MenuBar", "HTML Format (File Tree)")).setObjectName(translate("MenuBar", "HTML Format (File Tree)")) 
        mShowInWindow.addAction(translate("MenuBar", "Text Format (File Tree)")).setObjectName(translate("MenuBar", "Text Format (File Tree)"))
        mCopyToClipBoard = MMenu(translate("MenuBar", "Copy To Clipboard"), self.menus[1])
        mCopyToClipBoard.setObjectName(translate("MenuBar", "Copy To Clipboard"))
        mCopyToClipBoard.addAction(translate("MenuBar", "HTML Format")).setObjectName(translate("MenuBar", "HTML Format")) 
        mCopyToClipBoard.addAction(translate("MenuBar", "Text Format")).setObjectName(translate("MenuBar", "Text Format"))
        mCopyToClipBoard.addAction(translate("MenuBar", "HTML Format (File Tree)")).setObjectName(translate("MenuBar", "HTML Format (File Tree)")) 
        mCopyToClipBoard.addAction(translate("MenuBar", "Text Format (File Tree)")).setObjectName(translate("MenuBar", "Text Format (File Tree)"))
        self.menus[0].addAction(translate("MenuBar", "Open State")).setObjectName(translate("MenuBar", "Open State"))
        self.menus[0].addAction(translate("MenuBar", "Save State")).setObjectName(translate("MenuBar", "Save State"))
        if Execute.isRunableAsRoot():
            mRunAsRoot = MMenu(translate("MenuBar", "Run As Root"), self.menus[0])
            mRunAsRoot.addAction(translate("MenuBar", "With This Profile (My Settings)")).setObjectName(translate("MenuBar", "With This Profile (My Settings)")) 
            mRunAsRoot.addAction(translate("MenuBar", "With Root Profile (Own Settings)")).setObjectName(translate("MenuBar", "With Root Profile (Own Settings)")) 
            self.menus[0].addMenu(mRunAsRoot)
        self.menus[0].addAction(translate("MenuBar", "Quit")).setObjectName(translate("MenuBar", "Quit"))
        self.menus[1].addMenu(mExport)
        self.menus[1].addMenu(mShowInWindow)
        self.menus[1].addMenu(mCopyToClipBoard)
        self.refreshForTableType()
        self.menus[-3].addAction(MIcon("Images:pack.png"), translate("MenuBar", "Pack")).setObjectName(translate("MenuBar", "Pack"))
        self.menus[-3].addAction(MIcon("Images:fileTree.png"), translate("MenuBar", "File Tree")).setObjectName(translate("MenuBar", "File Tree"))
        self.menus[-3].addAction(MIcon("Images:clear.png"), translate("MenuBar", "Clear")).setObjectName(translate("MenuBar", "Clear"))
        self.menus[-3].addAction(MIcon("Images:runCommand.png"), translate("MenuBar", "Run Command")).setObjectName(translate("MenuBar", "Run Command"))
        self.menus[-2].addAction(translate("MenuBar", "Options")).setObjectName(translate("MenuBar", "Options"))
        self.menus[-2].addAction(translate("MenuBar", "My Plug-ins")).setObjectName(translate("MenuBar", "My Plug-ins"))
        if Universals.isActivePyKDE4==True:
            actReportBug = MAction(translate("MenuBar", "Report Bug"), self.menus[-1])
            actReportBug.setObjectName(translate("MenuBar", "Report Bug"))
            self.menus[-1].insertAction(self.menus[-1].actions()[3], actReportBug)
            actSuggestIdea = MAction(translate("MenuBar", "Suggest Idea"), self.menus[-1])
            actSuggestIdea.setObjectName(translate("MenuBar", "Suggest Idea"))
            self.menus[-1].insertAction(self.menus[-1].actions()[3], actSuggestIdea)
            actUNo = 9
            while actUNo>0:
                try:
                    actUpdate = MAction(translate("MenuBar", "Update"), self.menus[-1])
                    actUpdate.setObjectName(translate("MenuBar", "Update"))
                    self.menus[-1].insertAction(self.menus[-1].actions()[actUNo], actUpdate)
                    break
                except:actUNo = actUNo - 3
        else:
            self.menus[-1].addAction(translate("MenuBar", "Report Bug")).setObjectName(translate("MenuBar", "Report Bug"))
            self.menus[-1].addAction(translate("MenuBar", "Suggest Idea")).setObjectName(translate("MenuBar", "Suggest Idea"))
            self.menus[-1].addAction(translate("MenuBar", "Update")).setObjectName(translate("MenuBar", "Update"))
            self.menus[-1].addAction(translate("MenuBar", "About Hamsi Manager")).setObjectName(translate("MenuBar", "About Hamsi Manager"))
        self.menus[-1].addAction(translate("MenuBar", "About QT")).setObjectName(translate("MenuBar", "About QT"))
        for menu in self.menus:
            self.addMenu(menu)
        MObject.connect(self, SIGNAL("triggered(QAction *)"), self.click)
        
    def refreshForTableType(self):
        self.menus[2].clear()
        dockMenus = Universals.MainWindow.createPopupMenu()
        dockMenus.setTitle(translate("MenuBar", "Panels"))
        dockMenus.setParent(Universals.MainWindow)
        dockMenus.setObjectName(translate("MenuBar", "Panels"))
        self.menus[2].addMenu(dockMenus)
        actgActionGroup = MActionGroup(self.menus[2])
        for x, name in enumerate(Tables.tableTypesNames):
            a = actgActionGroup.addAction(MIcon(u"Images:"+Tables.tableTypeIcons[x]),
                                        name)
            a.setCheckable(True)
            a.setObjectName(name)
            if Tables.tableType==Tables.getThisTableType(name):
                a.setChecked(True)
        self.menus[2].addActions(actgActionGroup.actions())
        MObject.connect(actgActionGroup, SIGNAL("selected(QAction *)"), self.changeTableType)
        
    def click(self,_action):
        try:
            actionName = _action.objectName()
            if actionName==translate("MenuBar", "Open State"):
                import os, Settings
                f = MFileDialog.getOpenFileName(self,translate("MenuBar", "Open State"),
                                    Universals.userDirectoryPath,str(translate("MenuBar", "Application Runner") + " (*.desktop)").decode("utf-8"))
                if f!="":
                    Settings.openStateOfSettings(unicode(f, "utf-8"))
            elif actionName==translate("MenuBar", "Save State"):
                import Settings
                import os
                f = MFileDialog.getSaveFileName(self,translate("MenuBar", "Save State"),Universals.userDirectoryPath + "/HamsiManager.desktop",str(translate("MenuBar", "Application Runner")).decode("utf-8") + u" (*.desktop)")
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
            elif actionName==translate("MenuBar", "Pack"):
                import Packager
                Packager.Packager(InputOutputs.currentDirectoryPath)
            elif actionName==translate("MenuBar", "Clear"):
                import Cleaner
                Cleaner.Cleaner(InputOutputs.currentDirectoryPath)
            elif actionName==translate("MenuBar", "File Tree"):
                import FileTreeBuilder
                FileTreeBuilder.FileTreeBuilder(InputOutputs.currentDirectoryPath)
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
            elif actionName==translate("MenuBar", "Run Command"):
                try:
                    from PyQt4.Qsci import QsciScintilla
                except:
                    Dialogs.showError(translate("MenuBar", "Qsci Is Not Installed"), 
                            translate("MenuBar", "Qsci is not installed on your systems.<br>Please install Qsci on your system and try again."))
                else:
                    import RunCommand
                    RunCommand.RunCommand(Universals.MainWindow)
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
            Records.saveAllRecords()
        except:
            error = ReportBug.ReportBug()
            error.show()
        
    def changeTableType(self, _action):
        changeTableType(_action, True)
    
class Bars():
    def __init__(self):
        pass
        
    def refreshBars(self):
        Universals.MainWindow.Table = Tables.Tables(Universals.MainWindow)
        try:Universals.MainWindow.removeDockWidget(Universals.MainWindow.dckSpecialTools)
        except:pass
        Universals.MainWindow.SpecialTools = SpecialTools.SpecialTools(Universals.MainWindow)
        if Tables.tableType==2:
            Universals.MainWindow.PlayerBar = PlayerBar(Universals.MainWindow)
            Universals.MainWindow.addToolBar(Mt.TopToolBarArea,Universals.MainWindow.PlayerBar)
            Universals.MainWindow.MusicOptionsBar = MusicOptionsBar(Universals.MainWindow)
            Universals.MainWindow.addToolBar(Mt.TopToolBarArea,Universals.MainWindow.MusicOptionsBar)
        elif Tables.tableType==3:
            Universals.MainWindow.SubDirectoryOptionsBar = SubDirectoryOptionsBar(Universals.MainWindow)
            Universals.MainWindow.addToolBar(Mt.TopToolBarArea,Universals.MainWindow.SubDirectoryOptionsBar)
    
    def getAllBarsStyleFromMySettings(self):
        Universals.MainWindow.TableToolsBar.setToolButtonStyle(int(Universals.MySettings["TableToolsBarButtonStyle"]))
        Universals.MainWindow.ToolsBar.setToolButtonStyle(int(Universals.MySettings["ToolsBarButtonStyle"]))
        if Tables.tableType==2:
            Universals.MainWindow.PlayerBar.setToolButtonStyle(int(Universals.MySettings["PlayerBarButtonStyle"]))
            Universals.MainWindow.MusicOptionsBar.setToolButtonStyle(int(Universals.MySettings["MusicOptionsBarButtonStyle"]))
        elif Tables.tableType==3:
            Universals.MainWindow.SubDirectoryOptionsBar.setToolButtonStyle(int(Universals.MySettings["SubDirectoryOptionsBarButtonStyle"]))
        
    def setAllBarsStyleToMySettings(self):
        Universals.setMySetting("TableToolsBarButtonStyle", Universals.MainWindow.TableToolsBar.toolButtonStyle())
        Universals.setMySetting("ToolsBarButtonStyle", Universals.MainWindow.ToolsBar.toolButtonStyle())
        if Tables.tableType==2:
            Universals.setMySetting("PlayerBarButtonStyle", Universals.MainWindow.PlayerBar.toolButtonStyle())
            Universals.setMySetting("MusicOptionsBarButtonStyle", Universals.MainWindow.MusicOptionsBar.toolButtonStyle())
        elif Tables.tableType==3:
            Universals.setMySetting("SubDirectoryOptionsBarButtonStyle", Universals.MainWindow.SubDirectoryOptionsBar.toolButtonStyle())
        
    
class TableToolsBar(MToolBar):
    global clearAllChilds, changeTableType, changeThisTableType, actsFileReNamerTypes
    def __init__(self, _parent):
        MToolBar.__init__(self, _parent)
        _parent.addToolBar(Mt.TopToolBarArea,self)
        self.setWindowTitle(translate("TableToolsBar", "Table Tools"))
        self.setObjectName(translate("TableToolsBar", "Table Tools"))
        self.createTable()
        MObject.connect(self, SIGNAL("actionTriggered(QAction *)"), self.click)
        if Universals.windowMode==Universals.windowModeKeys[1]:
            self.setIconSize(MSize(16,16))
        else:
            self.setIconSize(MSize(32,32))
            
    def refreshForTableType(self):
        global actsFileReNamerTypes
        self.clear()
        actgActionGroup = MActionGroup(self)
        for x, name in enumerate(Tables.tableTypesNames):
            a = actgActionGroup.addAction(MIcon(u"Images:"+Tables.tableTypeIcons[x]),
                                        name)
            a.setCheckable(True)
            a.setObjectName(name)
            if Tables.tableType==Tables.getThisTableType(name):
                a.setChecked(True)
        self.addActions(actgActionGroup.actions())
        MObject.connect(actgActionGroup, SIGNAL("selected(QAction *)"), changeTableType)
        self.addSeparator()
        self.fileReNamerTypeNames = [str(translate("ToolsBar", "Personal Computer")), 
                                    str(translate("ToolsBar", "Web Server")), 
                                    str(translate("ToolsBar", "Removable Media"))]
        buttonIcons = ["personalComputer.png", "webServer.png", "removableMedia.png"]
        actgActionGroup = MActionGroup(self)
        actsFileReNamerTypes = []
        for x, name in enumerate(self.fileReNamerTypeNames):
            actsFileReNamerTypes.append(MAction(MIcon(u"Images:"+buttonIcons[x].decode("utf-8")),name.decode("utf-8"),self))
            actsFileReNamerTypes[-1].setObjectName(name.decode("utf-8"))
            actsFileReNamerTypes[x].setToolTip(str(translate("ToolsBar", "Renames files and folders in \"%s\" format.")) % (name.decode("utf-8")))
            actsFileReNamerTypes[x].setCheckable(True)
            actgActionGroup.addAction(actsFileReNamerTypes[x])
            if Universals.MySettings["fileReNamerType"]==Universals.fileReNamerTypeNamesKeys[x]:
                actsFileReNamerTypes[x].setChecked(True)
        if Universals.fileReNamerTypeNamesKeys.count(str(Universals.MySettings["fileReNamerType"]))==0:
            actsFileReNamerTypes[0].setChecked(True)
        self.addActions(actgActionGroup.actions())
        self.addSeparator()
        Universals.MainWindow.Table.createUniversalOptions(self)
        
    def click(self, _action):
        global actsFileReNamerTypes
        try:
            if _action.objectName()==translate("Tables", "Show Also Previous Information"):
                if _action.isChecked():_action.setChecked(False)
                else:_action.setChecked(True)
                if Universals.MainWindow.Table.checkUnSavedTableValues()==True:
                    if _action.isChecked():_action.setChecked(False)
                    else:_action.setChecked(True)
                    Tables.refreshTable(InputOutputs.currentDirectoryPath)
                else:
                    if _action.isChecked():_action.setChecked(False)
                    else:_action.setChecked(True)
            elif _action.objectName()==translate("Tables", "Ignore Selection"):
                if _action.isChecked():
                    Universals.MainWindow.Table.isChangeSelected.setEnabled(False)
                else:
                    Universals.MainWindow.Table.isChangeSelected.setEnabled(True)
            elif str(_action.toolTip()).find(str(translate("ToolsBar", "Renames files and folders in \"%s\" format."))[:20])!=-1:
                if Universals.MainWindow.Table.checkUnSavedTableValues()==False:
                    _action.setChecked(False)
                    return False
                for x, typeName in enumerate(Universals.fileReNamerTypeNamesKeys):
                    if actsFileReNamerTypes[x].isChecked():
                        Universals.setMySetting("fileReNamerType", typeName)
                Universals.MainWindow.FileManager.makeRefresh()
            Records.saveAllRecords()
        except:
            error = ReportBug.ReportBug()
            error.show()

    def changeThisTableType(_tableType):
        actgActionGroup = MActionGroup(None)
        a = actgActionGroup.addAction(str(_tableType))
        a.setCheckable(True)
        a.setChecked(True)
        a.setObjectName(str(_tableType))
        changeTableType(a, True)
        a.deleteLater()
        
    def changeTableType(_action, _isFromMenu=False):
        try:
            if (_action.isChecked() or _isFromMenu==True) and Tables.tableType != Tables.getThisTableType(_action.objectName()):
                if Universals.MainWindow.Table.checkUnSavedTableValues()==False:
                    _action.setChecked(False)
                    return False
                Universals.setMySetting(Universals.MainWindow.Table.hiddenTableColumnsSettingKey,Universals.MainWindow.Table.hiddenTableColumns)
                if Tables.tableType==2:
                    Universals.MainWindow.removeToolBar(Universals.MainWindow.PlayerBar)
                    Universals.MainWindow.PlayerBar = False
                    Universals.MainWindow.removeToolBar(Universals.MainWindow.MusicOptionsBar)
                    Universals.MainWindow.MusicOptionsBar = False
                elif Tables.tableType==3:
                    Universals.MainWindow.removeToolBar(Universals.MainWindow.SubDirectoryOptionsBar)
                    Universals.MainWindow.SubDirectoryOptionsBar = False
                Universals.setMySetting("isShowOldValues",Universals.MainWindow.Table.isShowOldValues.isChecked())
                Universals.setMySetting("isChangeSelected",Universals.MainWindow.Table.isChangeSelected.isChecked())
                Universals.setMySetting("isChangeAll",Universals.MainWindow.Table.isChangeAll.isChecked())
                Universals.MainWindow.Table.isShowOldValues.setVisible(False)
                Universals.MainWindow.Table.isShowOldValues.deleteLater()
                Universals.MainWindow.Table.isChangeAll.setVisible(False)
                Universals.MainWindow.Table.isChangeAll.deleteLater()
                Universals.MainWindow.Table.isChangeSelected.setVisible(False)
                Universals.MainWindow.Table.isChangeSelected.deleteLater()
                clearAllChilds(Universals.MainWindow.CentralWidget)
                Universals.MainWindow.TableToolsBar.createTable(unicode(_action.objectName()).encode("utf-8"))
                Universals.MainWindow.FileManager.makeRefresh()
            else:
                _action.setChecked(True)
        except:
            error = ReportBug.ReportBug()
            error.show()
    
    def createTable(self, _tableType=None):
        if _tableType!=None:
            Tables.tableType = Tables.getThisTableType(_tableType)
        Universals.MainWindow.Bars.refreshBars()
        self.refreshForTableType()
        if Universals.MainWindow.Menu!=None:
            Universals.MainWindow.Menu.refreshForTableType()
    
    def clearAllChilds(_object):
        childs = _object.findChildren(MWidget)
        for child in childs:
            clearAllChilds(child)
            try:child.hide()
            except:pass
            child.deleteLater()
 
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
        self.addAction(self.actPack)
        self.addAction(self.actFileTree)
        self.addAction(self.actClear)
        self.addSeparator()
        self.addAction(self.clearEmptyDirectories)
        self.addAction(self.actRemoveOnlySubFiles)
        self.addAction(self.actCheckIcon)
        MObject.connect(self, SIGNAL("actionTriggered(QAction *)"), self.click)
        if Universals.windowMode==Universals.windowModeKeys[1]:
            self.setIconSize(MSize(16,16))
        else:
            self.setIconSize(MSize(32,32))
    
    def click(self,_action):
        try:
            actionName = _action.objectName()
            if actionName==translate("ToolsBar", "Check Icon"):
                Universals.MainWindow.setEnabled(False)
                InputOutputs.checkIcon(InputOutputs.currentDirectoryPath)
                Universals.MainWindow.setEnabled(True)
                Dialogs.show(translate("ToolsBar", "Directory Icon Checked"),
                    translate("ToolsBar", "Current directory icon checked.<br>The default action based on the data is executed."))
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
            elif actionName==translate("ToolsBar", "Clear"):
                import Cleaner
                Cleaner.Cleaner(InputOutputs.currentDirectoryPath)
            elif actionName==translate("ToolsBar", "File Tree"):
                import FileTreeBuilder
                FileTreeBuilder.FileTreeBuilder(InputOutputs.currentDirectoryPath)
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
        self.setWindowTitle(translate("MusicOptionsBar", "Music options"))
        self.setObjectName(translate("MusicOptionsBar", "Music options"))
        lblDetails = translate("MusicOptionsBar", "You can select the ID3 tag you want to see and edit.<br><font color=blue>ID3 V2 is recommended.</font>")
        _parent.Table.cbMusicTagType = MComboBox(self)
        _parent.Table.cbMusicTagType.addItem(u"ID3 V1")
        _parent.Table.cbMusicTagType.addItem(u"ID3 V2")
        _parent.Table.cbMusicTagType.setCurrentIndex(_parent.Table.cbMusicTagType.findText(Universals.MySettings["musicTagType"]))
        _parent.Table.cbMusicTagType.setToolTip(lblDetails)
        self.addWidget(_parent.Table.cbMusicTagType)
        MObject.connect(_parent.Table.cbMusicTagType, SIGNAL("currentIndexChanged(int)"), self.musicTagTypeChanged)
        self.setIconSize(MSize(32,32))
    
    def musicTagTypeChanged(self):
        if self.isActiveChanging:
            if Universals.MainWindow.Table.checkUnSavedTableValues()==True:
                Universals.setMySetting("musicTagType", Universals.MainWindow.Table.cbMusicTagType.currentText())
                Tables.refreshForTableColumns()
                Universals.MainWindow.SpecialTools.refreshForTableColumns()
                Tables.refreshTable(InputOutputs.currentDirectoryPath)
            else:
                if Universals.MainWindow.Table.cbMusicTagType.currentIndex()==0:
                    index = 1
                else:
                    index = 0
                self.isActiveChanging = False
                Universals.MainWindow.Table.cbMusicTagType.setCurrentIndex(index)
                self.isActiveChanging = True
        
class SubDirectoryOptionsBar(MToolBar):
    def __init__(self, _parent):
        MToolBar.__init__(self, _parent)
        self.isActiveChanging = True
        self.setWindowTitle(translate("SubDirectoryOptionsBar", "Sub Directory Options"))
        self.setObjectName(translate("SubDirectoryOptionsBar", "Sub Directory Options"))
        lblDetails = translate("SubDirectoryOptionsBar", "You can select sub directory deep.<br><font color=blue>You can select \"-1\" for all sub directories.</font>")
        lblSubDirectoryDeep = MLabel(translate("SubDirectoryOptionsBar", "Deep : "))
        _parent.Table.cbSubDirectoryDeep = MComboBox(self)
        for x in range(-1, 10):
            _parent.Table.cbSubDirectoryDeep.addItem(str(x))
        _parent.Table.cbSubDirectoryDeep.setCurrentIndex(_parent.Table.cbSubDirectoryDeep.findText(Universals.MySettings["subDirectoryDeep"]))
        _parent.Table.cbSubDirectoryDeep.setToolTip(lblDetails)
        pnlSubDirectoryDeep = MWidget()
        hblSubDirectoryDeep = MHBoxLayout(pnlSubDirectoryDeep)
        hblSubDirectoryDeep.addWidget(lblSubDirectoryDeep)
        hblSubDirectoryDeep.addWidget(_parent.Table.cbSubDirectoryDeep)
        pnlSubDirectoryDeep.setLayout(hblSubDirectoryDeep)
        self.addWidget(pnlSubDirectoryDeep)
        MObject.connect(_parent.Table.cbSubDirectoryDeep, SIGNAL("currentIndexChanged(int)"), self.subDirectoryDeepChanged)
        self.setIconSize(MSize(32,32))
        self.lastSelectedSubDirectoryDeep = int(Universals.MySettings["subDirectoryDeep"])
    
    def subDirectoryDeepChanged(self):
        if self.isActiveChanging:
            self.isActiveChanging = False
            if Universals.MainWindow.Table.checkUnSavedTableValues()==True:
                Universals.setMySetting("subDirectoryDeep", int(Universals.MainWindow.Table.cbSubDirectoryDeep.currentText()))
                self.lastSelectedSubDirectoryDeep = int(Universals.MainWindow.Table.cbSubDirectoryDeep.currentText())
                Tables.refreshForTableColumns()
                Universals.MainWindow.SpecialTools.refreshForTableColumns()
                Tables.refreshTable(InputOutputs.currentDirectoryPath)
            else:
                Universals.MainWindow.Table.cbSubDirectoryDeep.setCurrentIndex(_parent.Table.cbSubDirectoryDeep.findText(str(self.lastSelectedSubDirectoryDeep)))
            self.isActiveChanging = True
        else:
            self.isActiveChanging = False
            Universals.MainWindow.Table.cbSubDirectoryDeep.setCurrentIndex(_parent.Table.cbSubDirectoryDeep.findText(str(self.lastSelectedSubDirectoryDeep)))
            self.isActiveChanging = True
            
        
class StatusBar(MStatusBar):
    
    def __init__(self, _parent):
        MStatusBar.__init__(self, _parent)
        import Execute
        if Execute.isRunningAsRoot():
            lblInfo = MLabel(u"<b><span style=\"background-color: #FF0000\">" + translate("StatusBar", "Hamsi Manager running as root")+u"</span></b>")
            self.addWidget(lblInfo)
        if Universals.isDebugMode:
            lblInfo = MLabel(translate("StatusBar", "Debug Mode"))
            self.addWidget(lblInfo)
            
            
        
        
        
