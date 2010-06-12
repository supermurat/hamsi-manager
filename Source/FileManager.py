# -*- coding: utf-8 -*-

import Tables
import InputOutputs
import Settings
import Universals
import Dialogs
from MyObjects import *
import os,sys
import ReportBug
import Organizer

class FileManager():
    
    def __init__(self, _parent):
        self.bookmarks = Bookmarks(self)
        self.history = []
        self.future = []
        if Universals.isActivePyKDE4==True:
            self.dirModelMain = MDirModel()
            self.dirLister = MDirLister()
            self.dirLister.setAutoUpdate(True)
            self.dirModelMain.setDirLister(self.dirLister)
            self.dirModel = MDirSortFilterProxyModel()
            self.dirModel.setSourceModel(self.dirModelMain)
            self.fpmPlacesModel = MFilePlacesModel()
            self.fpvPlaces = MFilePlacesView()
            self.fpvPlaces.setModel(self.fpmPlacesModel)
        else:
            self.dirModel = MDirModel()
            self.dirModel.setFilter(MDir.AllEntries | MDir.Readable | MDir.NoDotAndDotDot)
            self.dirModel.sort(0)
        self.trvFileManager = MTreeView()
        self.lstvFileManager = MListView()
        self.trvFileManager.setModel(self.dirModel)
        self.lstvFileManager.setModel(self.dirModel)
        self.currentDirectory = InputOutputs.getRealDirName(Universals.MySettings["lastDirectory"]).decode("utf-8")
        if InputOutputs.isDir(str(self.currentDirectory))==False:
            self.currentDirectory = MDir.homePath()
        MObject.connect(self.trvFileManager, SIGNAL("clicked(QModelIndex)"),self.setMyCurrentIndex)
        MObject.connect(self.lstvFileManager, SIGNAL("doubleClicked(QModelIndex)"),self.setMyCurrentIndex)
        tools = MToolBar(_parent)
        self.actBack = MAction(MIcon("Images:back.png"),"",tools)
        self.actBack.setToolTip(translate("FileManager", "Back"))
        self.actForward = MAction(MIcon("Images:forward.png"),"",tools)
        self.actForward.setToolTip(translate("FileManager", "Forward"))
        self.actUp = MAction(MIcon("Images:up.png"),"",tools)
        self.actUp.setToolTip(translate("FileManager", "Up"))
        actRefresh = MAction(MIcon("Images:refresh.png"),"",tools)
        actRefresh.setToolTip(translate("FileManager", "Refresh"))
        actHome = MAction(MIcon("Images:home.png"),"",tools)
        actHome.setToolTip(translate("FileManager", "Home"))
        actBookmarks = MPushButton()
        actBookmarks.setIcon(MIcon("Images:bookmarks.png"))
        actBookmarks.setFlat(True)
        actBookmarks.setFixedWidth(50)
        actBookmarks.setContentsMargins(-10, -10, -10, -10)
        actBookmarks.setToolTip(translate("FileManager", "Bookmarks"))
        actAddBookmark = MAction(MIcon("Images:addBookmark.png"),"",tools)
        actAddBookmark.setToolTip(translate("FileManager", "Add To Bookmarks"))
        MObject.connect(self.actBack, SIGNAL("triggered(bool)"), self.goBack)
        MObject.connect(self.actForward, SIGNAL("triggered(bool)"), self.goForward)
        MObject.connect(self.actUp, SIGNAL("triggered(bool)"), self.goUp)
        MObject.connect(actRefresh, SIGNAL("triggered(bool)"), self.makeRefresh)
        MObject.connect(actHome, SIGNAL("triggered(bool)"), self.goHome)
        MObject.connect(actAddBookmark, SIGNAL("triggered(bool)"), self.bookmarks.addBookmark)
        if Universals.isActivePyKDE4==True:
            self.filePlacesModel = MFilePlacesModel()
            self.urlNavigator = MUrlNavigator(self.filePlacesModel, MUrl(self.currentDirectory), self.lstvFileManager)
            self.isGoToFromUrlNavigator = True
            MObject.connect(self.urlNavigator, SIGNAL("urlChanged(KUrl)"),self.urlNavigatorUrlChanged)
            MObject.connect(self.fpvPlaces, SIGNAL("urlChanged(KUrl)"),self.setPlacesUrlChanged)
        self.goTo(self.currentDirectory)
        self.actBack.setEnabled(False)
        self.actForward.setEnabled(False)
        tools.addAction(self.actBack)
        tools.addAction(self.actForward)
        tools.addAction(self.actUp)
        tools.addAction(actRefresh)
        tools.addAction(actHome)
        tools.addWidget(actBookmarks)
        tools.addAction(actAddBookmark)
        widget = MWidget()
        if Universals.windowMode==Universals.windowModeKeys[1]:
            tools.setIconSize(MSize(16, 16))
            actBookmarks.setIconSize(MSize(16, 16))
            hbox = MHBoxLayout()
            hbox.addWidget(tools, 1)
            if Universals.isActivePyKDE4==True:
                hbox.addWidget(self.urlNavigator, 1)
            widget.setLayout(hbox)
            tbarBrowserTools = MToolBar(_parent)
            tbarBrowserTools.setWindowTitle(translate("FileManager", "Browser Tools"))
            tbarBrowserTools.setObjectName(translate("FileManager", "Browser Tools"))
            tbarBrowserTools.setIconSize(MSize(16,16))
            tbarBrowserTools.addWidget(widget)
            _parent.addToolBar(Mt.TopToolBarArea,tbarBrowserTools)
        else:
            tools.setIconSize(MSize(22, 22))
            actBookmarks.setIconSize(MSize(22, 22))
            vbox = MVBoxLayout()
            vbox.addWidget(tools, 1)
            if Universals.isActivePyKDE4==True:
                vbox.addWidget(self.urlNavigator, 1)
            widget.setLayout(vbox)
            dckwBrowserTools = MDockWidget(translate("FileManager", "Browser Tools"))
            dckwBrowserTools.setObjectName(translate("FileManager", "Browser Tools"))
            dckwBrowserTools.setWidget(widget)
            dckwBrowserTools.setAllowedAreas(Mt.AllDockWidgetAreas)
            dckwBrowserTools.setFeatures(MDockWidget.AllDockWidgetFeatures)
            _parent.addDockWidget(Mt.LeftDockWidgetArea, dckwBrowserTools)
        dock = MDockWidget(translate("FileManager", "Browser"))
        dock.setObjectName(translate("FileManager", "Browser"))
        dock.setWidget(self.lstvFileManager)
        dock.setAllowedAreas(Mt.AllDockWidgetAreas)
        dock.setFeatures(MDockWidget.AllDockWidgetFeatures)
        _parent.addDockWidget(Mt.LeftDockWidgetArea, dock)
        dock1 = MDockWidget(translate("FileManager", "Tree Browser"))
        dock1.setObjectName(translate("FileManager", "Tree Browser"))
        dock1.setWidget(self.trvFileManager)
        dock1.setAllowedAreas(Mt.AllDockWidgetAreas)
        dock1.setFeatures(MDockWidget.AllDockWidgetFeatures)
        _parent.addDockWidget(Mt.LeftDockWidgetArea, dock1)
        if Universals.isActivePyKDE4==True:
            dock2 = MDockWidget(translate("FileManager", "Places"))
            dock2.setObjectName(translate("FileManager", "Places"))
            dock2.setWidget(self.fpvPlaces)
            dock2.setAllowedAreas(Mt.AllDockWidgetAreas)
            dock2.setFeatures(MDockWidget.AllDockWidgetFeatures)
            _parent.addDockWidget(Mt.LeftDockWidgetArea, dock2)
            _parent.tabifyDockWidget(dock1, dock2)
        self.bookmarksMenu = BookmarksMenu(self)
        actBookmarks.setMenu(self.bookmarksMenu)
        self.bookmarksMenu.makeRefresh()

    def goTo(self, _path, _isRemember = True):
        if Universals.tableType==3:
            import Bars
            Bars.changeTableType(0)
        if _isRemember:
            self.future = []
            self.history.append(self.currentDirectory)
            self.currentDirectory = _path
        if Universals.isActivePyKDE4==True:
            self.dirLister.openUrl(MUrl(self.currentDirectory))
            self.isGoToFromUrlNavigator = False
            self.urlNavigator.setUrl(MUrl(self.currentDirectory))
            self.isGoToFromUrlNavigator = True
        else:
            self.lstvFileManager.setRootIndex(self.dirModel.index(_path))
            self.trvFileManager.setCurrentIndex(self.dirModel.index(_path))
        self.actForward.setEnabled(False)
        self.showInTable()
        self.actBack.setEnabled(True)
        if str(self.currentDirectory)=="/":
            self.actUp.setEnabled(False)
        else:
            self.actUp.setEnabled(True)

    def goBack(self):
        try:
            self.future.append(self.currentDirectory)
            self.currentDirectory = self.history.pop()
            self.goTo(self.currentDirectory, False)
            self.actForward.setEnabled(True)
            if len(self.history)==0:
                self.actBack.setEnabled(False)
        except:
            error = ReportBug.ReportBug()
            error.show()

    def goForward(self):
        try:
            self.history.append(self.currentDirectory)
            try:
                self.currentDirectory = self.future.pop()
            except:
                pass
            self.goTo(self.currentDirectory, False)
            if len(self.future)==0:
                self.actForward.setEnabled(False)
        except:
            error = ReportBug.ReportBug()
            error.show()

    def goUp(self):
        try:
            self.goTo(InputOutputs.getDirName(self.currentDirectory).decode("utf-8"))
        except:
            error = ReportBug.ReportBug()
            error.show()

    def goHome(self):
        try:
            self.goTo(MDir.homePath())
        except:
            error = ReportBug.ReportBug()
            error.show()

    def makeRefresh(self, _newDirectoryPath=""):
        try:
            if _newDirectoryPath!="" and _newDirectoryPath!=True and _newDirectoryPath!=False:
                self.goTo(_newDirectoryPath.decode("utf-8"), False)
            else:
                self.makeRefreshOnlyFileList(self.lstvFileManager.rootIndex())
                self.showInTable()
        except:
            error = ReportBug.ReportBug()
            error.show()
    
    def makeRefreshOnlyFileList(self, _index=""):
        if _index=="":_index = self.lstvFileManager.currentIndex()
        if Universals.isActivePyKDE4==True:
            return self.dirModelMain.itemForIndex(self.dirModel.mapToSource(_index)).refresh()
        else:
            return self.dirModel.refresh(_index)
    
    def getPathOfIndex(self, _index):
        if Universals.isActivePyKDE4==True:
            return self.dirModelMain.itemForIndex(self.dirModel.mapToSource(_index)).url().pathOrUrl()
        else:
            return self.dirModel.filePath(_index)
        
    def getFileInfo(self, _index):
        if Universals.isActivePyKDE4==True:
            return self.dirModelMain.itemForIndex(self.dirModel.mapToSource(_index))
        else:
            return self.dirModel.fileInfo(_index)
    
    def urlNavigatorUrlChanged(self, _murl):
        if self.isGoToFromUrlNavigator:
            self.goTo(_murl.pathOrUrl(), True)
        
    def setPlacesUrlChanged(self, _murl):
        self.goTo(_murl.pathOrUrl(), True)
        
    def setMyCurrentIndex(self, _index, _isRemember = True):
        try:
            while 1==1:
                selected = unicode(self.getPathOfIndex(_index), "utf-8")
                if InputOutputs.isDir(selected)==True or InputOutputs.isFile(selected)==True:
                    self.makeRefreshOnlyFileList(_index)
                    break
                else:
                    _index = _index.parent()
            if _index != self.lstvFileManager.rootIndex() and self.getFileInfo(_index).isDir() and self.getFileInfo(_index).isReadable():
                self.goTo(self.getPathOfIndex(_index))
                
            elif _index != self.lstvFileManager.rootIndex() and ~self.getFileInfo(_index).isDir() and self.getFileInfo(_index).isReadable():
                fileName=unicode(self.getPathOfIndex(_index)).encode("utf-8")
                if Universals.tableType==2:
                    for ext in Universals.getListFromStrint(Universals.MySettings["musicExtensions"]):
                        if fileName.split(".")[-1].decode("utf-8").lower() == unicode(ext, "utf-8"):
                            if Universals.MainWindow.PlayerBar.Player.playInBar.isChecked():
                                Universals.MainWindow.PlayerBar.Player.play(fileName)
                            else:
                                from Tables import MusicTable
                                from Details import MusicDetails
                                MusicDetails.MusicDetails(fileName,Universals.MainWindow.Table.isOpenDetailsOnNewWindow.isChecked())
                else:
                    try:
                        from Details import TextDetails
                        TextDetails.TextDetails(fileName,Universals.MainWindow.Table.isOpenDetailsOnNewWindow.isChecked())
                    except:
                        Dialogs.showError(translate("FileManager", "Cannot open file"), 
                                     str(translate("FileManager", "\"%s\" cannot be opened. Please make sure you selected a text file.")) % Organizer.getLink(fileName))
        except:
            error = ReportBug.ReportBug()
            error.show()
    
    def showInTable(self):
        try:
            InputOutputs.currentDirectoryPath = str(self.currentDirectory).replace("file://", "")
            Tables.refreshTable(InputOutputs.currentDirectoryPath)
        except:
            error = ReportBug.ReportBug()
            error.show()
          
          
class BookmarksMenu(MMenu):
    def __init__(self, _parent):
        MMenu.__init__(self)
        self._parent = _parent;
        self.setTitle(translate("BookmarksMenu", "Bookmarks"))
        MObject.connect(self,SIGNAL("triggered(QAction *)"),self.triggered)
        self.makeRefresh()
    
    def makeRefresh(self):
        try:
            self.clear()
            for fav in Settings.bookmarksOfDirectories():
                self.addAction(fav[1].decode("utf-8")).setObjectName(fav[1].decode("utf-8"))
            self.addAction(translate("BookmarksMenu", "Edit Bookmarks")).setObjectName(translate("BookmarksMenu", "Edit Bookmarks"))
        except:
            error = ReportBug.ReportBug()
            error.show()

    def triggered(self, _action):
        try:
            if _action.objectName()==translate("BookmarksMenu", "Edit Bookmarks"):
                Universals.MainWindow.FileManager.bookmarks.makeRefresh()
                Universals.MainWindow.FileManager.bookmarks.show()
                return
            for info in Settings.bookmarksOfDirectories():
                if info[1]==str(_action.objectName()):
                    if InputOutputs.isDir(str(info[2]))==True:
                        Universals.MainWindow.FileManager.goTo(info[2].decode("utf-8"))
                        return
                    else:
                        answer = Dialogs.ask(translate("BookmarksMenu", "Cannot Find Folder"), 
                                            str(translate("BookmarksMenu", "\"%s\" cannot be found.<br>Delete this folder from the bookmarks?")) % Organizer.getLink(info[1]))
                        if answer==Dialogs.Yes:
                            Settings.bookmarksOfDirectories("delete",str(info[0]))
                            self.makeRefresh()
                            Universals.MainWindow.FileManager.bookmarks.makeRefresh()
            Universals.MainWindow.FileManager.makeRefreshOnlyFileList()   
        except:
            error = ReportBug.ReportBug()
            error.show()
        
    
class Bookmarks(MDialog):
    def __init__(self, _parent):
        MDialog.__init__(self)
        self._parent = _parent;
        if Universals.isActivePyKDE4==True:
            self.setButtons(MDialog.None)
        self.setWindowTitle(translate("Bookmarks", "Bookmarks"))
        pbtnDeleteBookmark = MPushButton(translate("Bookmarks", "Delete"))
        pbtnSaveBookmark = MPushButton(translate("Bookmarks", "Save"))
        pbtnClose = MPushButton(translate("Bookmarks", "Close"))
        MObject.connect(pbtnDeleteBookmark, SIGNAL("clicked()"), self.deleteBookmark)
        MObject.connect(pbtnSaveBookmark, SIGNAL("clicked()"), self.saveBookmark)
        MObject.connect(pbtnClose, SIGNAL("clicked()"), self.close)
        self.cbBookmarks = MComboBox()
        self.cbBookmarks.setEditable(True)
        self.pathOfBookmark = MLineEdit()
        pnlMain = MWidget(self)
        hbox = MHBoxLayout()
        hbox.addWidget(self.cbBookmarks)
        hbox.addWidget(pbtnDeleteBookmark)
        hbox1 = MHBoxLayout()
        hbox1.addWidget(self.pathOfBookmark)
        hbox1.addWidget(pbtnSaveBookmark)
        vblMain = MVBoxLayout(pnlMain)
        vblMain.addLayout(hbox)
        vblMain.addLayout(hbox1)
        vblMain.addWidget(pbtnClose)
        if Universals.isActivePyKDE4==True:
            self.setMainWidget(pnlMain)
        else:
            self.setLayout(vblMain)
        self.setFixedSize(300,120)
        MObject.connect(self.cbBookmarks, SIGNAL("currentIndexChanged(int)"), self.bookmarksChanged)
        self.makeRefresh()

    def closeEvent(self, _event):
        Universals.MainWindow.FileManager.bookmarksMenu.makeRefresh()
        
    def bookmarksChanged(self, _index):
        try:
            self.pathOfBookmark.setText(Settings.bookmarksOfDirectories()[self.cbBookmarks.currentIndex()][2].decode("utf-8"))
        except:
            error = ReportBug.ReportBug()
            error.show()
            
    def addBookmark(self):
        try:
            isim=str(InputOutputs.currentDirectoryPath).split("/")
            Settings.bookmarksOfDirectories("add",isim[len(isim)-1],InputOutputs.currentDirectoryPath)
            Universals.MainWindow.FileManager.bookmarksMenu.makeRefresh()
            self.makeRefresh()
        except:
            error = ReportBug.ReportBug()
            error.show()
        
    def saveBookmark(self):
        try:
            info = Settings.bookmarksOfDirectories()[self.cbBookmarks.currentIndex()]
            Settings.bookmarksOfDirectories("update",info[0],self.cbBookmarks.currentText(),self.pathOfBookmark.text())
            self.makeRefresh()
            Universals.MainWindow.FileManager.bookmarksMenu.makeRefresh()
        except:
            error = ReportBug.ReportBug()
            error.show()
            
    def deleteBookmark(self):
        try:
            if self.cbBookmarks.currentIndex()!=-1:
                info = Settings.bookmarksOfDirectories()[self.cbBookmarks.currentIndex()]
                Settings.bookmarksOfDirectories("delete",info[0])
                self.makeRefresh()
                Universals.MainWindow.FileManager.bookmarksMenu.makeRefresh()
        except:
            error = ReportBug.ReportBug()
            error.show()
            
    def makeRefresh(self):
        try:
            self.cbBookmarks.clear()
            for fav in Settings.bookmarksOfDirectories():
                self.cbBookmarks.addItem(fav[1].decode("utf-8")) 
        except:
            error = ReportBug.ReportBug()
            error.show()
            
            
            
            
