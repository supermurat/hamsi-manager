# # This file is part of HamsiManager.
# #
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


import FileUtils as fu
from Core import Universals as uni
from Core import Dialogs
from Core.MyObjects import *
from Core import ReportBug
from Core import Organizer
import Databases


class FileManager():
    def __init__(self, _parent):
        self.bookmarks = Bookmarks(self)
        self.history = []
        self.future = []
        getMainWindow().DirOperator = None
        getMainWindow().Browser = None
        getMainWindow().Places = None
        getMainWindow().TreeBrowser = None
        if isActivePyKDE4:
            self.dirModelMain = MDirModel()
            self.dirLister = MDirLister()
            self.dirLister.setAutoUpdate(True)
            self.dirModelMain.setDirLister(self.dirLister)
            self.dirModel = MDirSortFilterProxyModel()
            self.dirModel.setSourceModel(self.dirModelMain)
            self.fpmPlacesModel = MFilePlacesModel()
            self.fpvPlaces = MFilePlacesView()
            self.fpvPlaces.setModel(self.fpmPlacesModel)
            self.dirModelForNavigator = MDirSortFilterProxyModel()
            self.dirModelForNavigator.setSourceModel(self.dirModelMain)
            self.dirModelForTree = QDirModel()
            self.dirModelForTree.setFilter(MDir.AllDirs | MDir.Drives | MDir.Readable | MDir.NoDotAndDotDot)
            self.dirModelForTree.sort(0)
        else:
            self.dirModel = MDirModel()
            self.dirModel.setFilter(MDir.AllEntries | MDir.Readable | MDir.NoDotAndDotDot)
            self.dirModel.sort(0)
            self.dirModelForTree = MDirModel()
            self.dirModelForTree.setFilter(MDir.AllDirs | MDir.Drives | MDir.Readable | MDir.NoDotAndDotDot)
            self.dirModelForTree.sort(0)
            self.dirModelForNavigator = MDirModel()
            self.dirModelForNavigator.setFilter(MDir.AllEntries | MDir.Readable)
            self.dirModelForNavigator.sort(0)
        self.trvFileManager = MTreeView()
        self.lstvFileManager = MListView()
        self.trvFileManager.setModel(self.dirModelForTree)
        self.lstvFileManager.setModel(self.dirModel)
        self.currentDirectory = str(fu.getRealDirName(uni.MySettings["lastDirectory"]))
        if fu.isDir(str(self.currentDirectory)) == False:
            self.currentDirectory = MDir.homePath()
        MObject.connect(self.trvFileManager, SIGNAL("clicked(QModelIndex)"), self.setMyCurrentIndexByTree)
        MObject.connect(self.lstvFileManager, SIGNAL("doubleClicked(QModelIndex)"), self.setMyCurrentIndex)
        tools = MToolBar(_parent)
        actAddBookmark = MAction(MIcon("Images:addBookmark.png"), "", tools)
        actAddBookmark.setToolTip(translate("FileManager", "Add To Bookmarks"))
        self.actBack = MAction(MIcon("Images:back.png"), "", tools)
        self.actBack.setToolTip(translate("FileManager", "Back"))
        self.actForward = MAction(MIcon("Images:forward.png"), "", tools)
        self.actForward.setToolTip(translate("FileManager", "Forward"))
        self.actUp = MAction(MIcon("Images:up.png"), "", tools)
        self.actUp.setToolTip(translate("FileManager", "Up"))
        actRefresh = MAction(MIcon("Images:refresh.png"), "", tools)
        actRefresh.setToolTip(translate("FileManager", "Refresh"))
        actHome = MAction(MIcon("Images:home.png"), "", tools)
        actHome.setToolTip(translate("FileManager", "Home"))
        MObject.connect(self.actBack, SIGNAL("triggered(bool)"), self.goBack)
        MObject.connect(self.actForward, SIGNAL("triggered(bool)"), self.goForward)
        MObject.connect(self.actUp, SIGNAL("triggered(bool)"), self.goUp)
        MObject.connect(actRefresh, SIGNAL("triggered(bool)"), self.makeRefresh)
        MObject.connect(actHome, SIGNAL("triggered(bool)"), self.goHome)
        MObject.connect(actAddBookmark, SIGNAL("triggered(bool)"), self.bookmarks.addBookmark)
        self.bookmarksMenu = BookmarksMenu(self)
        if isActivePyKDE4:
            toolsFull = MToolBar(_parent)
            toolsFull.addAction(self.bookmarksMenu.menuAction())
            self.isGoToFromDirOperator = False
            self.dirOperator = MDirOperator(MUrl(self.currentDirectory), _parent)
            self.dirOperator.setDirLister(self.dirLister)

            kconf = MGlobal.config()
            kconfGroup = MConfigGroup(kconf, "DirectoryOperator")
            self.dirOperator.readConfig(kconfGroup)
            self.dirOperator.setViewConfig(kconfGroup)
            self.dirOperator.setView(MFile.Default)

            self.actCollection = self.dirOperator.actionCollection()
            self.actCollection.readSettings(kconfGroup)
            self.actCollection.associateWidget(toolsFull)

            getMainWindow().DirOperator = MDockWidget(translate("FileManager", "Directory Operator"))
            getMainWindow().DirOperator.setObjectName(translate("FileManager", "Directory Operator"))
            getMainWindow().DirOperator.setWidget(self.dirOperator)
            getMainWindow().DirOperator.setAllowedAreas(Mt.AllDockWidgetAreas)
            getMainWindow().DirOperator.setFeatures(MDockWidget.AllDockWidgetFeatures)
            _parent.addDockWidget(Mt.LeftDockWidgetArea, getMainWindow().DirOperator)
            MObject.connect(self.dirOperator, SIGNAL("urlEntered(KUrl)"), self.dirOperatorUrlChanged)
            self.isGoToFromDirOperator = True
            self.filePlacesModel = MFilePlacesModel()
            self.urlNavigator = MUrlNavigator(self.filePlacesModel, MUrl(self.currentDirectory), self.lstvFileManager)
            self.isGoToFromUrlNavigator = True
            MObject.connect(self.urlNavigator, SIGNAL("urlChanged(KUrl)"), self.urlNavigatorUrlChanged)
            MObject.connect(self.fpvPlaces, SIGNAL("urlChanged(KUrl)"), self.setPlacesUrlChanged)
        self.leNavigator = MLineEdit()
        cmpCompleter = MCompleter()
        cmpCompleter.setModel(self.dirModelForNavigator)
        cmpCompleter.setCaseSensitivity(Mt.CaseInsensitive)
        self.leNavigator.setCompleter(cmpCompleter)
        MObject.connect(self.leNavigator, SIGNAL("returnPressed()"), self.leNavigatorPressed)
        tools.addAction(self.actBack)
        tools.addAction(self.actForward)
        tools.addAction(self.actUp)
        tools.addAction(actRefresh)
        tools.addAction(actHome)
        tools.addAction(self.bookmarksMenu.menuAction())
        tools.addAction(actAddBookmark)
        self.actBack.setEnabled(False)
        self.actForward.setEnabled(False)
        self.goTo(self.currentDirectory)
        self.trvFileManager.setColumnWidth(0, 250)
        if uni.windowMode == uni.windowModeKeys[1]:
            tools.setIconSize(MSize(16, 16))
            self.tbarBrowserTools = MToolBar(_parent)
            self.tbarBrowserTools.setWindowTitle(translate("FileManager", "Browser Tools"))
            self.tbarBrowserTools.setObjectName(translate("FileManager", "Browser Tools"))
            self.tbarBrowserTools.setIconSize(MSize(16, 16))
            self.tbarBrowserTools.addWidget(tools)
            _parent.addToolBar(Mt.TopToolBarArea, self.tbarBrowserTools)
            self.tbarLocationBar = MToolBar(_parent)
            self.tbarLocationBar.setWindowTitle(translate("FileManager", "Location Bar"))
            self.tbarLocationBar.setObjectName(translate("FileManager", "Location Bar"))
            self.tbarLocationBar.setIconSize(MSize(16, 16))
            self.tbarLocationBar.addWidget(self.leNavigator)
            _parent.addToolBar(Mt.TopToolBarArea, self.tbarLocationBar)
            if isActivePyKDE4:
                toolsFull.setIconSize(MSize(16, 16))
                self.tbarBrowserToolsFull = MToolBar(_parent)
                self.tbarBrowserToolsFull.setWindowTitle(translate("FileManager", "Browser Tools (KDE4)"))
                self.tbarBrowserToolsFull.setObjectName(translate("FileManager", "Browser Tools (KDE4)"))
                self.tbarBrowserToolsFull.setIconSize(MSize(16, 16))
                self.tbarBrowserToolsFull.addWidget(toolsFull)
                _parent.addToolBar(Mt.TopToolBarArea, self.tbarBrowserToolsFull)
                self.tbarLocationBar = MToolBar(_parent)
                self.tbarLocationBar.setWindowTitle(translate("FileManager", "Location Bar (KDE4)"))
                self.tbarLocationBar.setObjectName(translate("FileManager", "Location Bar (KDE4)"))
                self.tbarLocationBar.setIconSize(MSize(16, 16))
                self.tbarLocationBar.addWidget(self.urlNavigator)
                _parent.addToolBar(Mt.TopToolBarArea, self.tbarLocationBar)
        else:
            tools.setIconSize(MSize(22, 22))
            self.dckwBrowserTools = MDockWidget(translate("FileManager", "Browser Tools"))
            self.dckwBrowserTools.setObjectName(translate("FileManager", "Browser Tools"))
            self.dckwBrowserTools.setWidget(tools)
            self.dckwBrowserTools.setAllowedAreas(Mt.AllDockWidgetAreas)
            self.dckwBrowserTools.setFeatures(MDockWidget.AllDockWidgetFeatures)
            _parent.addDockWidget(Mt.LeftDockWidgetArea, self.dckwBrowserTools)
            self.tbarLocationBar = MToolBar(_parent)
            self.tbarLocationBar.setWindowTitle(translate("FileManager", "Location Bar"))
            self.tbarLocationBar.setObjectName(translate("FileManager", "Location Bar"))
            self.tbarLocationBar.setIconSize(MSize(16, 16))
            self.tbarLocationBar.addWidget(self.leNavigator)
            _parent.addToolBar(Mt.TopToolBarArea, self.tbarLocationBar)
            if isActivePyKDE4:
                toolsFull.setIconSize(MSize(22, 22))
                self.dckwBrowserToolsFull = MDockWidget(translate("FileManager", "Browser Tools (KDE4)"))
                self.dckwBrowserToolsFull.setObjectName(translate("FileManager", "Browser Tools (KDE4)"))
                self.dckwBrowserToolsFull.setWidget(toolsFull)
                self.dckwBrowserToolsFull.setAllowedAreas(Mt.AllDockWidgetAreas)
                self.dckwBrowserToolsFull.setFeatures(MDockWidget.AllDockWidgetFeatures)
                _parent.addDockWidget(Mt.LeftDockWidgetArea, self.dckwBrowserToolsFull)
                self.tbarLocationBar = MToolBar(_parent)
                self.tbarLocationBar.setWindowTitle(translate("FileManager", "Location Bar (KDE4)"))
                self.tbarLocationBar.setObjectName(translate("FileManager", "Location Bar (KDE4)"))
                self.tbarLocationBar.setIconSize(MSize(16, 16))
                self.tbarLocationBar.addWidget(self.urlNavigator)
                _parent.addToolBar(Mt.TopToolBarArea, self.tbarLocationBar)
        getMainWindow().Browser = MDockWidget(translate("FileManager", "Browser"))
        getMainWindow().Browser.setObjectName(translate("FileManager", "Browser"))
        getMainWindow().Browser.setWidget(self.lstvFileManager)
        getMainWindow().Browser.setAllowedAreas(Mt.AllDockWidgetAreas)
        getMainWindow().Browser.setFeatures(MDockWidget.AllDockWidgetFeatures)
        _parent.addDockWidget(Mt.LeftDockWidgetArea, getMainWindow().Browser)
        getMainWindow().TreeBrowser = MDockWidget(translate("FileManager", "Tree Browser"))
        getMainWindow().TreeBrowser.setObjectName(translate("FileManager", "Tree Browser"))
        getMainWindow().TreeBrowser.setWidget(self.trvFileManager)
        getMainWindow().TreeBrowser.setAllowedAreas(Mt.AllDockWidgetAreas)
        getMainWindow().TreeBrowser.setFeatures(MDockWidget.AllDockWidgetFeatures)
        _parent.addDockWidget(Mt.LeftDockWidgetArea, getMainWindow().TreeBrowser)
        if isActivePyKDE4:
            getMainWindow().Places = MDockWidget(translate("FileManager", "Places"))
            getMainWindow().Places.setObjectName(translate("FileManager", "Places"))
            getMainWindow().Places.setWidget(self.fpvPlaces)
            getMainWindow().Places.setAllowedAreas(Mt.AllDockWidgetAreas)
            getMainWindow().Places.setFeatures(MDockWidget.AllDockWidgetFeatures)
            _parent.addDockWidget(Mt.LeftDockWidgetArea, getMainWindow().Places)
            _parent.tabifyDockWidget(getMainWindow().DirOperator, getMainWindow().Places)
            _parent.tabifyDockWidget(getMainWindow().DirOperator, getMainWindow().TreeBrowser)
            _parent.tabifyDockWidget(getMainWindow().DirOperator, getMainWindow().Browser)

    def goTo(self, _path, _isRemember=True, _isOnlyBrowser=False):
        try:
            _path = fu.checkSource(str(_path))
            if _path is not None:
                if fu.isReadableFileOrDir(_path):
                    if fu.isDir(_path):
                        if _isRemember:
                            self.future = []
                            self.history.append(self.currentDirectory)
                        if _path[-1] == fu.sep: _path = _path[:-1]
                        self.currentDirectory = str(_path)
                        if isActivePyKDE4:
                            self.dirLister.openUrl(MUrl(self.currentDirectory))
                            self.trvFileManager.setCurrentIndex(self.dirModelForTree.index(_path))
                            self.isGoToFromUrlNavigator = False
                            self.urlNavigator.setUrl(MUrl(self.currentDirectory))
                            self.isGoToFromUrlNavigator = True
                            self.isGoToFromDirOperator = False
                            self.dirOperator.setUrl(MUrl(self.currentDirectory), False)
                            self.isGoToFromDirOperator = True
                        else:
                            self.lstvFileManager.setRootIndex(self.dirModel.index(_path))
                            self.trvFileManager.setCurrentIndex(self.dirModelForTree.index(_path))
                        self.actForward.setEnabled(False)
                        if _isOnlyBrowser == False:
                            self.showInTable()
                        self.actBack.setEnabled(True)
                        if str(self.currentDirectory) == fu.sep:
                            self.actUp.setEnabled(False)
                        else:
                            self.actUp.setEnabled(True)
                    elif fu.isFile(_path):
                        isOpened = False
                        for ext in uni.getListValue("musicExtensions"):
                            if str(_path).split(".")[-1].lower() == str(ext).lower():
                                if (
                                            uni.tableType == "2" or uni.tableType == "9") and getMainWindow().PlayerBar.MusicPlayer.playInBar.isChecked():
                                    getMainWindow().PlayerBar.MusicPlayer.play(str(_path))
                                isOpened = True
                        if isOpened == False:
                            from Details import Details

                            Details(str(_path), uni.getBoolValue("isOpenDetailsInNewWindow"))
        except:
            ReportBug.ReportBug()

    def goBack(self):
        try:
            self.future.append(self.currentDirectory)
            self.currentDirectory = self.history.pop()
            self.goTo(self.currentDirectory, False)
            self.actForward.setEnabled(True)
            if len(self.history) == 0:
                self.actBack.setEnabled(False)
        except:
            ReportBug.ReportBug()

    def goForward(self):
        try:
            self.history.append(self.currentDirectory)
            try:
                self.currentDirectory = self.future.pop()
            except:
                pass
            self.goTo(self.currentDirectory, False)
            if len(self.future) == 0:
                self.actForward.setEnabled(False)
        except:
            ReportBug.ReportBug()

    def goUp(self):
        try:
            self.goTo(str(fu.getDirName(self.currentDirectory)))
        except:
            ReportBug.ReportBug()

    def goHome(self):
        try:
            self.goTo(MDir.homePath())
        except:
            ReportBug.ReportBug()

    def makeRefresh(self, _newDirectoryPath="", _isOnlyBrowser=False):
        try:
            if _newDirectoryPath != "" and _newDirectoryPath != True and _newDirectoryPath != False:
                self.goTo(_newDirectoryPath, False)
            else:
                sourcePath = fu.checkSource(str(self.currentDirectory), "directory")
                if sourcePath is not None:
                    if self.currentDirectory != str(sourcePath):
                        self.goTo(sourcePath, False)
                    else:
                        self.makeRefreshOnlyFileList()
                        self.makeRefreshOnlyFileListByTree()
                        if _isOnlyBrowser == False:
                            self.showInTable()
                else:
                    self.goTo(fu.getRealDirName(str(self.currentDirectory)), False)
        except:
            ReportBug.ReportBug()

    def makeRefreshOnlyFileList(self, _index=""):
        if _index == "": _index = self.lstvFileManager.currentIndex()
        if isActivePyKDE4:
            return self.dirModelMain.itemForIndex(self.dirModel.mapToSource(_index)).refresh()
        else:
            return self.dirModel.refresh(_index)

    def makeRefreshOnlyFileListByTree(self, _index=""):
        if _index == "": _index = self.trvFileManager.currentIndex()
        return self.dirModelForTree.refresh(_index)

    def getPathOfIndex(self, _index):
        if isActivePyKDE4:
            return self.dirModelMain.itemForIndex(self.dirModel.mapToSource(_index)).url().pathOrUrl()
        else:
            return self.dirModel.filePath(_index)

    def getPathOfIndexByTree(self, _index):
        return self.dirModelForTree.filePath(_index)

    def getFileInfo(self, _index):
        if isActivePyKDE4:
            return self.dirModelMain.itemForIndex(self.dirModel.mapToSource(_index))
        else:
            return self.dirModel.fileInfo(_index)

    def leNavigatorPressed(self):
        self.goTo(str(fu.joinPath(self.currentDirectory, self.leNavigator.text())))
        self.leNavigator.setText("")

    def urlNavigatorUrlChanged(self, _murl):
        if self.isGoToFromUrlNavigator:
            self.goTo(_murl.pathOrUrl(), True)

    def dirOperatorUrlChanged(self, _murl):
        if self.isGoToFromDirOperator:
            self.goTo(_murl.pathOrUrl(), True)

    def setPlacesUrlChanged(self, _murl):
        self.goTo(_murl.pathOrUrl(), True)

    def setMyCurrentIndex(self, _index):
        try:
            while 1 == 1:
                selected = str(self.getPathOfIndex(_index))
                if fu.isDir(selected) or fu.isFile(selected):
                    self.makeRefreshOnlyFileList(_index)
                    break
                else:
                    _index = _index.parent()
            self.goTo(self.getPathOfIndex(_index))
        except:
            ReportBug.ReportBug()

    def setMyCurrentIndexByTree(self, _index):
        try:
            while 1 == 1:
                selected = str(self.getPathOfIndexByTree(_index))
                if fu.isDir(selected) or fu.isFile(selected):
                    self.makeRefreshOnlyFileListByTree(_index)
                    break
                else:
                    _index = _index.parent()
            self.goTo(self.getPathOfIndexByTree(_index))
        except:
            ReportBug.ReportBug()

    def showInTable(self):
        try:
            if uni.tableType in ["0", "1", "2", "3", "4", "9"]:
                getMainWindow().Table.refresh(self.getCurrentDirectoryPath())
            else:
                getMainWindow().StatusBar.setTableInfo(uni.tableTypesNames[uni.tableType] + str(" : ~ "))
        except:
            ReportBug.ReportBug()

    def getCurrentDirectoryPath(self):
        return str(self.currentDirectory).replace("file://", "")


class BookmarksMenu(MMenu):
    def __init__(self, _parent):
        MMenu.__init__(self)
        self._parent = _parent;
        self.setTitle(translate("BookmarksMenu", "Bookmarks"))
        self.setIcon(MIcon("Images:bookmarks.png"))
        MObject.connect(self, SIGNAL("triggered(QAction *)"), self.triggered)
        self.makeRefresh()

    def makeRefresh(self):
        try:
            self.clear()
            for fav in Databases.BookmarksOfDirectories.fetchAll():
                self.addAction(str(fav[1])).setObjectName(str(fav[1]))
            self.addAction(translate("BookmarksMenu", "Edit Bookmarks")).setObjectName(
                translate("BookmarksMenu", "Edit Bookmarks"))
        except:
            ReportBug.ReportBug()

    def triggered(self, _action):
        try:
            if _action.objectName() == translate("BookmarksMenu", "Edit Bookmarks"):
                getMainWindow().FileManager.bookmarks.makeRefresh()
                getMainWindow().FileManager.bookmarks.show()
                return
            for info in Databases.BookmarksOfDirectories.fetchAll():
                if info[1] == str(_action.objectName()):
                    if fu.isDir(str(info[2])):
                        getMainWindow().FileManager.goTo(str(info[2]))
                        return
                    else:
                        answer = Dialogs.ask(translate("BookmarksMenu", "Cannot Find Folder"),
                                             str(translate("BookmarksMenu",
                                                           "\"%s\" cannot be found.<br>Delete this folder from the bookmarks?")) % Organizer.getLink(
                                                 info[1]))
                        if answer == Dialogs.Yes:
                            Databases.BookmarksOfDirectories.delete(str(info[0]))
                            self.makeRefresh()
                            getMainWindow().FileManager.bookmarks.makeRefresh()
            getMainWindow().FileManager.makeRefreshOnlyFileList()
            getMainWindow().FileManager.makeRefreshOnlyFileListByTree()
        except:
            ReportBug.ReportBug()


class Bookmarks(MDialog):
    def __init__(self, _parent):
        MDialog.__init__(self)
        self._parent = _parent;
        if isActivePyKDE4:
            self.setButtons(MDialog.NoDefault)
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
        if isActivePyKDE4:
            self.setMainWidget(pnlMain)
        else:
            self.setLayout(vblMain)
        self.setFixedSize(300, 120)
        MObject.connect(self.cbBookmarks, SIGNAL("currentIndexChanged(int)"), self.bookmarksChanged)
        self.makeRefresh()

    def closeEvent(self, _event):
        getMainWindow().FileManager.bookmarksMenu.makeRefresh()

    def bookmarksChanged(self, _index):
        try:
            self.pathOfBookmark.setText(
                str(Databases.BookmarksOfDirectories.fetchAll()[self.cbBookmarks.currentIndex()][2]))
        except:
            ReportBug.ReportBug()

    def addBookmark(self):
        try:
            currentPath = getMainWindow().FileManager.getCurrentDirectoryPath()
            Databases.BookmarksOfDirectories.insert(fu.splitPath(currentPath)[-1], currentPath)
            getMainWindow().FileManager.bookmarksMenu.makeRefresh()
            self.makeRefresh()
        except:
            ReportBug.ReportBug()

    def saveBookmark(self):
        try:
            info = Databases.BookmarksOfDirectories.fetchAll()[self.cbBookmarks.currentIndex()]
            Databases.BookmarksOfDirectories.update(info[0], str(self.cbBookmarks.currentText()),
                                                    str(self.pathOfBookmark.text()))
            self.makeRefresh()
            getMainWindow().FileManager.bookmarksMenu.makeRefresh()
        except:
            ReportBug.ReportBug()

    def deleteBookmark(self):
        try:
            if self.cbBookmarks.currentIndex() != -1:
                info = Databases.BookmarksOfDirectories.fetchAll()[self.cbBookmarks.currentIndex()]
                Databases.BookmarksOfDirectories.delete(str(info[0]))
                self.makeRefresh()
                getMainWindow().FileManager.bookmarksMenu.makeRefresh()
        except:
            ReportBug.ReportBug()

    def makeRefresh(self):
        try:
            self.cbBookmarks.clear()
            for fav in Databases.BookmarksOfDirectories.fetchAll():
                self.cbBookmarks.addItem(str(fav[1]))
        except:
            ReportBug.ReportBug()
            
            
            
            
