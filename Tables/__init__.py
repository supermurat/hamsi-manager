## This file is part of HamsiManager.
##
## Copyright (c) 2010 - 2014 Murat Demir <mopened@gmail.com>
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


from Core import Dialogs
from Core import Universals as uni
import FileUtils as fu
from Core import Organizer
from Core.MyObjects import *
from Core import ReportBug
from Options import TableQuickOptions


class Tables():
    def __init__(self, _parent):
        self.setTable(_parent)
        self.Table.initByTable()

    @staticmethod
    def getThisTableType(_tableType):
        if _tableType in uni.tableTypesNames:
            return _tableType
        else:
            for x, name in uni.tableTypesNames.items():
                if str(name) == str(_tableType):
                    return x
        return "1"

    def setTable(self, _parent):
        if uni.tableType == "0":
            from Tables import FolderTable

            self.Table = FolderTable.FolderTable(_parent)
        elif uni.tableType == "1":
            from Tables import FileTable

            self.Table = FileTable.FileTable(_parent)
        elif uni.tableType == "2":
            import Taggers

            if Taggers.getTagger(True) is not None:
                from Tables import MusicTable

                self.Table = MusicTable.MusicTable(_parent)
            else:
                uni.tableType = "1"
                from Tables import FileTable

                self.Table = FileTable.FileTable(_parent)
        elif uni.tableType == "3":
            from Tables import SubFolderTable

            self.Table = SubFolderTable.SubFolderTable(_parent)
        elif uni.tableType == "4":
            if uni.isActiveDirectoryCover:
                from Tables import CoverTable

                self.Table = CoverTable.CoverTable(_parent)
            else:
                Dialogs.showError(translate("Tables", "Directory Cover Not Usable"),
                                  translate("Tables",
                                            "Any icon can not set to any directory. This feature is not usable in your system."))
                uni.tableType = "1"
                from Tables import FileTable

                self.Table = FileTable.FileTable(_parent)
        elif uni.tableType == "5":
            import Amarok

            if Amarok.checkAmarok(True, False):
                uni.tableType = "5"
                import AmarokCoverTable

                self.Table = AmarokCoverTable.AmarokCoverTable(_parent)
            else:
                uni.tableType = "1"
                from Tables import FileTable

                self.Table = FileTable.FileTable(_parent)
        elif uni.tableType == "6":
            import Taggers, Amarok

            if Taggers.getTagger(True) is not None and Amarok.checkAmarok(True, False):
                import AmarokMusicTable

                self.Table = AmarokMusicTable.AmarokMusicTable(_parent)
            else:
                uni.tableType = "1"
                from Tables import FileTable

                self.Table = FileTable.FileTable(_parent)
        elif uni.tableType == "7":
            import Amarok

            if Amarok.checkAmarok(True, False):
                import AmarokArtistTable

                self.Table = AmarokArtistTable.AmarokArtistTable(_parent)
            else:
                uni.tableType = "1"
                from Tables import FileTable

                self.Table = FileTable.FileTable(_parent)
        elif uni.tableType == "8":
            import Taggers, Amarok

            if Taggers.getTagger(True) is not None and Amarok.checkAmarok(True, False):
                import AmarokCopyTable

                self.Table = AmarokCopyTable.AmarokCopyTable(_parent)
            else:
                uni.tableType = "1"
                from Tables import FileTable

                self.Table = FileTable.FileTable(_parent)
        elif uni.tableType == "9":
            import Taggers

            if Taggers.getTagger(True) is not None:
                from Tables import SubFolderMusicTable

                self.Table = SubFolderMusicTable.SubFolderMusicTable(_parent)
            else:
                uni.tableType = "1"
                from Tables import FileTable

                self.Table = FileTable.FileTable(_parent)


class CoreTable(MTableWidget):
    def __init__(self, _parent):
        MTableWidget.__init__(self, _parent)
        self.tableColumns = []
        self.tableColumnsKey = []
        self.tableReadOnlyColumnsKey = []
        self.isAskShowHiddenColumn = True
        self.currentDirectoryPath = ""
        self.newDirectoryPath = ""
        self.values = []
        self.changedValueNumber = 0
        self.history = []
        self.future = []
        self.setAlternatingRowColors(True)
        self.setWordWrap(False)
        self.setVerticalScrollMode(self.ScrollPerPixel)
        self.setHorizontalScrollMode(self.ScrollPerPixel)
        # self.setEditTriggers(MAbstractItemView.CurrentChanged) # TODO: make this an option
        MObject.connect(self, SIGNAL("cellClicked(int,int)"), self.cellClicked)
        MObject.connect(self, SIGNAL("itemChanged(QTableWidgetItem *)"), self.itemChanged)
        MObject.connect(self, SIGNAL("cellDoubleClicked(int,int)"), self.cellDoubleClicked)
        self.pbtnSave = MPushButton(translate("Tables", "Write To Disc"))
        self.pbtnSave.setObjectName("pbtnSave")
        self.pbtnSave.setIcon(MIcon("Images:save.png"))
        self.pbtnShowDetails = MPushButton(translate("Tables", "Details"))
        self.pbtnTableQuickOptions = MPushButton(translate("Tables", "Options"))
        self.mTableQuickOptions = TableQuickOptions.TableQuickOptions(self)
        self.pbtnTableQuickOptions.setMenu(self.mTableQuickOptions)
        self.tbCorrect = MToolButton()
        self.tbCorrect.setToolTip(translate("Tables", "Re Correct"))
        self.tbCorrect.setIcon(MIcon("Images:correct.png"))
        self.tbCorrect.setAutoRaise(True)
        MObject.connect(self.pbtnShowDetails, SIGNAL("clicked()"), self.showDetails)
        self.actRefresh = MToolButton()
        self.actRefresh.setToolTip(translate("Tables", "Refresh"))
        self.actRefresh.setIcon(MIcon("Images:refresh.png"))
        self.actRefresh.setAutoRaise(True)
        MObject.connect(self.actRefresh, SIGNAL("clicked()"), self.refresh)
        self.tbGoBack = MToolButton()
        self.tbGoForward = MToolButton()
        self.tbCreateHistoryPoint = MToolButton()
        self.tbGoBack.setToolTip(translate("Tables", "Go To Previous Action"))
        self.tbGoForward.setToolTip(translate("Tables", "Perform Next Action"))
        self.tbCreateHistoryPoint.setToolTip(translate("Tables", "Create An Action Point"))
        self.tbGoBack.setIcon(MIcon("Images:edit-undo.png"))
        self.tbGoForward.setIcon(MIcon("Images:edit-redo.png"))
        self.tbCreateHistoryPoint.setIcon(MIcon("Images:createHistoryPoint.png"))
        self.tbGoBack.setAutoRaise(True)
        self.tbGoForward.setAutoRaise(True)
        self.tbCreateHistoryPoint.setAutoRaise(True)
        MObject.connect(self.pbtnSave, SIGNAL("clicked()"), self.save)
        MObject.connect(self.tbGoBack, SIGNAL("clicked()"), self.goBack)
        MObject.connect(self.tbGoForward, SIGNAL("clicked()"), self.goForward)
        MObject.connect(self.tbCreateHistoryPoint, SIGNAL("clicked()"), self.createHistoryPoint)
        MObject.connect(self.tbCorrect, SIGNAL("clicked()"), self.correct)
        _parent.MainLayout.addWidget(self, 10)
        self.mContextMenu = MMenu(self)
        self.hblBoxMain = MHBoxLayout()
        self.vblBoxOptionsAndTools = MVBoxLayout()
        self.hblBoxOptions = MHBoxLayout()
        self.vblBoxOptionsAndTools.addLayout(self.hblBoxOptions)
        self.hblBoxTools = MHBoxLayout()
        self.hblBoxTools.addWidget(self.actRefresh)
        self.hblBoxTools.addWidget(self.tbGoBack)
        self.hblBoxTools.addWidget(self.tbCreateHistoryPoint)
        self.hblBoxTools.addWidget(self.tbGoForward)
        self.hblBoxTools.addWidget(self.tbCorrect)
        self.hblBoxTools.addWidget(self.pbtnTableQuickOptions)
        self.vblBoxOptionsAndTools.addLayout(self.hblBoxTools)
        self.hblBoxMain.addLayout(self.vblBoxOptionsAndTools, 5)
        self.vblBoxSourceAndTarget = MVBoxLayout()
        self.hblBoxMain.addLayout(self.vblBoxSourceAndTarget)
        self.hblBoxMain.addWidget(self.pbtnSave, 1)
        _parent.MainLayout.addLayout(self.hblBoxMain)
        if uni.tableType in ["0", "1", "3"]:
            self.hblBoxTools.addWidget(self.pbtnShowDetails)
        elif uni.tableType in ["8"]:
            self.hblBoxTools.addWidget(self.pbtnShowDetails)
            self.pbtnSave.setMinimumHeight(55)
        else:
            self.hblBoxOptions.addWidget(self.pbtnShowDetails)
            self.pbtnSave.setMinimumHeight(55)

    def initByTable(self):
        self.hiddenTableColumns = uni.getListValue(self.hiddenTableColumnsSettingKey)
        self.mContextMenuColumns = MMenu()
        self.mContextMenuColumns.setTitle(translate("Tables", "Show Fields"))
        self.mContextMenuOpenWith = MMenu()
        self.mContextMenuOpenWith.setTitle(translate("Tables", "Open With"))
        self.refreshForColumns()
        self.mContextMenuActionNames = [translate("Tables", "Cut"),
                                        translate("Tables", "Copy"),
                                        translate("Tables", "Paste"),
                                        translate("Tables", "Replace"),
                                        translate("Tables", "Remove From System")]
        for actName in self.mContextMenuActionNames:
            self.mContextMenu.addAction(actName).setObjectName(actName)
        self.mContextMenuOpenWithNames = [translate("Tables", "File Manager"),
                                          translate("Tables", "Default Application")]
        if uni.isWindows is False:
            self.mContextMenuOpenWithNames.append(translate("Tables", "Konsole"))
        for actName in self.mContextMenuOpenWithNames:
            self.mContextMenuOpenWith.addAction(actName).setObjectName(actName)
        self.mContextMenu.addMenu(self.mContextMenuColumns)
        self.mContextMenu.addAction(translate("Tables", "Open Details")).setObjectName(
            translate("Tables", "Open Details"))
        self.mContextMenu.addMenu(self.mContextMenuOpenWith)
        self.checkActionsStates()
        self.fillSelectionInfo()

    def getColumnKeyFromName(self, _nameWithMark):
        for x, name in enumerate(self.tableColumns):
            if str(name) == str(_nameWithMark).replace("&", ""):
                return self.tableColumnsKey[x]
        return _nameWithMark

    def getColumnNameFromName(self, _nameWithMark):
        for x, name in enumerate(self.tableColumns):
            if str(name) == str(_nameWithMark).replace("&", ""):
                return self.tableColumns[x]
        return _nameWithMark

    def getColumnNameFromKey(self, _keyName):
        for x, name in enumerate(self.tableColumnsKey):
            if str(name) == str(_keyName):
                return self.tableColumns[x]
        return _keyName

    def showDetails(self):
        try:
            rowNo = self.currentRow()
            if rowNo != -1:
                self.showTableDetails(rowNo, self.currentColumn())
            else:
                Dialogs.toast(translate("Tables", "Please Select A Row"),
                             translate("Tables", "Please select a row to show details."))
        except:
            ReportBug.ReportBug()

    def correct(self):
        try:
            self.correctTable()
        except:
            ReportBug.ReportBug()

    def goBack(self):
        self.future.append(self.createHistoryPoint(True))
        self.goActionPoint(self.history.pop())
        self.checkActionsStates()

    def goForward(self):
        self.history.append(self.createHistoryPoint(True))
        self.goActionPoint(self.future.pop())
        self.checkActionsStates()

    def createHistoryPoint(self, _isReturn=False):
        point = []
        for rowNo in range(self.rowCount()):
            point.append([])
            for columnNo in range(self.columnCount()):
                item = self.item(rowNo, columnNo)
                if item is not None:
                    point[-1].append(item.text())
                else:
                    point[-1].append("")
            point[-1].append(self.isRowHidden(rowNo))
        if _isReturn is False:
            self.future = []
            self.history.append(point)
            self.checkActionsStates()
        else:
            return point

    def goActionPoint(self, _actionPoint):
        for rowNo, row in enumerate(_actionPoint):
            for columnNo, column in enumerate(row[:-1]):
                item = self.item(rowNo, columnNo)
                if item is not None:
                    item.setText(column)
            if row[-1]:
                self.hideRow(rowNo)
            else:
                self.showRow(rowNo)

    def checkActionsStates(self):
        if len(self.history) == 0:
            self.tbGoBack.setEnabled(False)
        else:
            self.tbGoBack.setEnabled(True)
        if len(self.future) == 0:
            self.tbGoForward.setEnabled(False)
        else:
            self.tbGoForward.setEnabled(True)

    def clearHistoryPoints(self):
        self.history = []
        self.future = []
        self.checkActionsStates()

    def contextMenuEvent(self, _event):
        try:
            currentItem = self.currentItem()
            if currentItem is not None:
                self.mContextMenu.setGeometry(_event.globalX(), _event.globalY(), 1, 1)
                selectedItem = self.mContextMenu.exec_()
                if selectedItem is not None:
                    if selectedItem.objectName() == self.mContextMenuActionNames[0]:
                        self.createHistoryPoint()
                        MApplication.clipboard().setText(currentItem.text())
                        currentItem.setText("")
                    elif selectedItem.objectName() == self.mContextMenuActionNames[1]:
                        MApplication.clipboard().setText(currentItem.text())
                    elif selectedItem.objectName() == self.mContextMenuActionNames[2]:
                        self.createHistoryPoint()
                        currentItem.setText(MApplication.clipboard().text())
                    elif selectedItem.objectName() == self.mContextMenuActionNames[3]:
                        self.editItem(currentItem)
                    elif selectedItem.objectName() == self.mContextMenuActionNames[4]:
                        self.createHistoryPoint()
                        for rowNo in self.getSelectedRows():
                            self.hideRow(rowNo)
                    elif selectedItem.objectName() == translate("Tables", "Open Details"):
                        self.showDetails()
                    elif selectedItem.objectName() == self.mContextMenuOpenWithNames[0]:
                        from Core import Execute

                        Execute.openWith([fu.getRealDirName(self.values[currentItem.row()]["path"])])
                    elif selectedItem.objectName() == self.mContextMenuOpenWithNames[1]:
                        from Core import Execute

                        Execute.openWith([self.values[currentItem.row()]["path"]])
                    elif uni.isWindows is False and selectedItem.objectName() == self.mContextMenuOpenWithNames[2]:
                        from Core import Execute

                        Execute.execute(["konsole", "--workdir",
                                         fu.getRealDirName(self.values[currentItem.row()]["path"])])
        except:
            ReportBug.ReportBug()

    def getSelectedRows(self):
        sr = []
        for item in self.selectedItems():
            if sr.count(item.row()) == 0:
                sr.append(item.row())
        return sr

    def getSelectedColumns(self):
        sc = []
        for item in self.selectedItems():
            if sc.count(item.column()) == 0:
                sc.append(item.column())
        return sc

    def refreshShowedAndHiddenColumns(self):
        self.hiddenTableColumns = []
        for x, act in enumerate(self.mContextMenuColumnsActions):
            if act.isChecked() is False:
                self.hiddenTableColumns.append(str(act.objectName()))
        for columnNo, columnKey in enumerate(self.tableColumnsKey):
            if self.hiddenTableColumns.count(columnKey) > 0:
                self.hideColumn(columnNo)
            else:
                self.showColumn(columnNo)

    def cellClicked(self, _row, _column):
        try:
            self.cellClickedTable(_row, _column)
            # self.editItem(self.item(_row, _column)) # TODO: make this an option
        except:
            ReportBug.ReportBug()

    def cellDoubleClicked(self, _row, _column):
        try:
            self.cellDoubleClickedTable(_row, _column)
        except:
            ReportBug.ReportBug()

    def refreshForColumns(self):
        self.mContextMenuColumns.clear()
        self.refreshColumns()
        self.mContextMenuColumnsActions = []
        for columnKey in self.tableColumnsKey:
            act = MAction(self.getColumnNameFromKey(columnKey), self.mContextMenuColumns)
            act.setObjectName(columnKey)
            self.mContextMenuColumnsActions.append(act)
            act.setCheckable(True)
            if self.hiddenTableColumns.count(columnKey) == 0:
                act.setChecked(True)
            self.mContextMenuColumns.addAction(act)
            MObject.connect(act, SIGNAL("triggered(bool)"), self.refreshShowedAndHiddenColumns)
        self.refreshShowedAndHiddenColumns()

    def setCurrentDirectory(self, _path):
        if _path == "":
            if hasattr(getMainWindow(), "FileManager") and getMainWindow().FileManager is not None:
                _path = getMainWindow().FileManager.getCurrentDirectoryPath()
            else:
                _path = fu.userDirectoryPath
        self.currentDirectoryPath = _path
        self.newDirectoryPath = _path

    def setNewDirectory(self, _path):
        if _path == "":
            _path = self.currentDirectoryPath
        if _path == "":
            if hasattr(getMainWindow(), "FileManager") and getMainWindow().FileManager is not None:
                _path = getMainWindow().FileManager.getCurrentDirectoryPath()
            else:
                _path = fu.userDirectoryPath
        self.newDirectoryPath = _path

    def refresh(self, _path=""):
        self.setCurrentDirectory(_path)
        self.isAskShowHiddenColumn = True
        self.clearHistoryPoints()
        self.clear()
        self.setColumnCount(len(self.tableColumns))
        self.setHorizontalHeaderLabels(self.tableColumns)
        columnWidth = (getMainWindow().CentralWidget.width() - 90) / len(self.tableColumns)
        if columnWidth > 110:
            for x in range(len(self.tableColumns)):
                self.setColumnWidth(x, columnWidth)
        from Core import MyThread

        myProcs = MyThread.MyThread(self.refreshTable, self.continueRefresh, [self.currentDirectoryPath])
        myProcs.run()

    def continueRefresh(self, _returned=None):
        for rowNo in range(self.rowCount()):
            if self.isRowHidden(rowNo):
                self.showRow(rowNo)
        self.refreshShowedAndHiddenColumns()
        if uni.getBoolValue("isResizeTableColumnsToContents"):
            self.resizeColumnsToContents()
        getMainWindow().StatusBar.setTableInfo(
            uni.tableTypesNames[uni.tableType] + str(" : ") + str(str(self.rowCount())))

    def save(self):
        try:
            from Core import Records

            Records.setTitle(uni.tableTypesNames[uni.tableType])
            fu.activateSmartCheckIcon()
            fu.activateSmartCheckEmptyDirectories()
            from Core import MyThread

            myProcs = MyThread.MyThread(self.saveTable, self.continueSave)
            myProcs.run()
        except:
            ReportBug.ReportBug()

    def continueSave(self, _returned=None):
        try:
            if _returned:
                from Core import Records

                if uni.tableType in ["0", "1", "2", "3", "4", "9"]:
                    if uni.getBoolValue("isClearEmptyDirectoriesWhenSave"):
                        fu.checkEmptyDirectories(self.currentDirectoryPath, True, True,
                                                    uni.getBoolValue("isAutoCleanSubFolderWhenSave"))
                fu.completeSmartCheckEmptyDirectories(True, True)
                isDirStillExist = fu.isDir(self.currentDirectoryPath)
                if uni.tableType in ["0", "1", "2", "3", "9"]:
                    if uni.isActiveDirectoryCover and uni.getBoolValue(
                        "isActiveAutoMakeIconToDirectory") and uni.getBoolValue(
                        "isAutoMakeIconToDirectoryWhenSave"):
                        if isDirStillExist:
                            fu.checkIcon(self.currentDirectoryPath)
                        if self.currentDirectoryPath != self.newDirectoryPath:
                            fu.checkIcon(self.newDirectoryPath)
                fu.completeSmartCheckIcon()
                Records.saveAllRecords()
                if self.changedValueNumber == 0:
                    Dialogs.show(translate("Tables", "Did Not Change Any Things"),
                                 translate("Tables",
                                           "Did not change any things in this table.Please check the criteria you select."))
                else:
                    if uni.getBoolValue("isShowTransactionDetails"):
                        Dialogs.show(translate("Tables", "Transaction Details"),
                                     str(translate("Tables", "%s value(s) changed.")) % self.changedValueNumber)
                if not isDirStillExist and self.currentDirectoryPath == self.newDirectoryPath:
                    getMainWindow().FileManager.goUp()
                elif not isDirStillExist and self.currentDirectoryPath != self.newDirectoryPath:
                    getMainWindow().FileManager.makeRefresh(self.newDirectoryPath)
                else:
                    getMainWindow().FileManager.makeRefresh("")
                    if uni.tableType in ["5", "6", "7", "8"]:
                        self.refresh(self.newDirectoryPath)
        except:
            ReportBug.ReportBug()

    def fillSelectionInfo(self):
        if uni.getBoolValue("isChangeAll"):
            self.pbtnSave.setText(translate("Tables", "Write To Disc"))
            self.pbtnSave.setToolTip(translate("Tables", "All informations will be changed"))
        else:
            self.pbtnSave.setText(str(" ! " + translate("Tables", "Write To Disc") + " ! "))
            if uni.getBoolValue("isChangeSelected"):
                self.pbtnSave.setToolTip(translate("Tables", "Just selected informations will be changed"))
            else:
                self.pbtnSave.setToolTip(translate("Tables", "Just unselected informations will be changed"))

    def isChangeableItem(self, _rowNo, _columnNo, _checkLikeThis=None, isCanBeEmpty=True, _isCheckLike=True):
        item = self.item(_rowNo, _columnNo)
        if item is not None:
            if item.isReadOnly is False:
                if self.isColumnHidden(_columnNo) is not True and item.isSelected() == uni.getBoolValue(
                    "isChangeSelected") or uni.getBoolValue("isChangeAll"):
                    if _isCheckLike and _checkLikeThis is not None:
                        if str(_checkLikeThis) != str(item.text()):
                            if isCanBeEmpty is False:
                                if str(item.text()).strip() != "":
                                    return True
                                return False
                            else:
                                return True
                        return False
                    else:
                        if isCanBeEmpty is False:
                            if str(item.text()).strip() != "":
                                return True
                            return False
                        else:
                            return True
        return False

    def createItem(self, _rowNo, _columnNo, _columnKey, _newValue, _currentValue=None, _isReadOnly=False):
        item = MyTableWidgetItem(_currentValue)
        item.isReadOnly = _isReadOnly
        item.columnKey = _columnKey
        if not item.isReadOnly:
            if item.columnKey in self.tableReadOnlyColumnsKey:
                item.isReadOnly = True
        if item.isReadOnly:
            item.setToolTip(translate("Tables", "This value is NOT changeable!"))
            item.setFlags(Mt.ItemIsSelectable | Mt.ItemIsEnabled)
            item.setText("! " + str(_newValue))
        else:
            item.setText(str(_newValue))
        self.setItem(_rowNo, _columnNo, item)
        return item

    def itemChanged(self, _item):
        if _item.text() != _item.currentText and _item.isReadOnly is False:
            _item.setToolTip(_item.currentText)
            _item.setBackground(MBrush(MColor(142, 199, 255)))

    def checkUnSavedValues(self, _isForceToCheck=False):
        if uni.getBoolValue("isCheckUnSavedValues") or _isForceToCheck:
            isClose = True
            for rowNo in range(self.rowCount()):
                if isClose is False:
                    break
                if self.isRowHidden(rowNo):
                    isClose = False
                    break
                for columnNo in range(len(self.tableColumns)):
                    if self.isColumnHidden(columnNo) is False:
                        if self.item(rowNo, columnNo) is not None:
                            if self.item(rowNo, columnNo).background() == MBrush(MColor(142, 199, 255)):
                                isClose = False
                                break
                        else: break
            if isClose is False:
                answer = Dialogs.ask(translate("Tables", "There Are Unsaved Values"),
                                     translate("Tables",
                                               "Do you want to save these values?<br>If you click to Yes : Table will be saved without any other question or option.<br>If you click to No : Application will be closed without doing any process.<br>If you click to Cancel : Application won't be closed."),
                                     True)
                if answer == Dialogs.Yes:
                    self.save()
                elif answer == Dialogs.Cancel:
                    return False
        return True

    def checkFileExtensions(self, _columnNo, _fileNameKeyOrDestinationColumnNo, _isCheckFile=False):
        destinationParameterType = "fileNameKey"
        if type(_fileNameKeyOrDestinationColumnNo) == type(0):
            destinationParameterType = "destinationColumnNo"
        isYesToAll, isNoToAll = False, False
        for rowNo in range(self.rowCount()):
            if _isCheckFile:
                if fu.isFile(self.values[rowNo]["path"]) is False:
                    continue
            if destinationParameterType == "fileNameKey":
                sFileExt = fu.getFileExtension(self.values[rowNo][_fileNameKeyOrDestinationColumnNo])
                sFilePath = self.values[rowNo]["path"]
            else:
                sFileExt = fu.getFileExtension(str(self.item(rowNo, _fileNameKeyOrDestinationColumnNo).text()))
                sFilePath = str(self.item(rowNo, _fileNameKeyOrDestinationColumnNo).text())
            cFileName = str(self.item(rowNo, _columnNo).text())
            if sFileExt != "":
                if fu.getFileExtension(cFileName) != sFileExt:
                    if isYesToAll:
                        answer = Dialogs.Yes
                    elif isNoToAll:
                        answer = Dialogs.No
                    else:
                        answer = Dialogs.askSpecial(translate("Tables", "Incorrect File Extension"),
                                                    str(translate("Tables",
                                                                  "\"%s\": the file extension is different from the source file extension.<br>Do you want to set the source file extension?<br><b>Source file : </b>\"%s\"")) % (
                                                        cFileName, sFilePath),
                                                    translate("Dialogs", "Yes"),
                                                    translate("Dialogs", "No"),
                                                    translate("Dialogs", "Yes To All"),
                                                    translate("Dialogs", "No To All"))
                    if answer == translate("Dialogs", "Yes To All"):
                        isYesToAll = True
                        answer = Dialogs.Yes
                    elif answer == translate("Dialogs", "No To All"):
                        isNoToAll = True
                        answer = Dialogs.No
                    if answer == Dialogs.Yes or answer == translate("Dialogs", "Yes"):
                        self.item(rowNo, _columnNo).setText(str(cFileName + "." + sFileExt))

    def askHiddenColumn(self, _columnNo, _isYesToAll=True):
        if _isYesToAll is False:
            self.isAskShowHiddenColumn = True
        if self.isAskShowHiddenColumn:
            if _isYesToAll:
                answer = Dialogs.askSpecial(translate("Tables", "Hidden Field"),
                                            str(translate("Tables",
                                                          "\"%s\": you have hidden this field in the table.<br>Do you want to activate this field and perform the action?")) % (
                                                self.tableColumns[_columnNo]),
                                            translate("Dialogs", "Yes"),
                                            translate("Dialogs", "No"),
                                            translate("Dialogs", "Yes To All"))
            else:
                answer = Dialogs.ask(translate("Tables", "Hidden Field"),
                                     str(translate("Tables",
                                                   "\"%s\": you have hidden this field in the table.<br>Do you want to activate this field and perform the action?")) % (
                                         self.tableColumns[_columnNo]))
            if answer == Dialogs.No or answer == translate("Dialogs", "No"):
                Dialogs.showError(translate("Tables", "Action Cancelled"),
                                  translate("Tables",
                                            "You have cancelled the action.<br>You can make the necessary changes and reperform the action."))
                return False
            elif answer == translate("Dialogs", "Yes To All"):
                self.isAskShowHiddenColumn = False
        self.mContextMenuColumnsActions[_columnNo].setChecked(True)
        self.refreshShowedAndHiddenColumns()
        return True

    def checkHiddenColumn(self, _columnNo, _isYesToAll=True):
        if self.isColumnHidden(_columnNo):
            return self.askHiddenColumn(_columnNo, _isYesToAll)
        return True

    def checkReadOnlyColumn(self, _columnKey, _isAlert=True):
        if _columnKey in self.tableReadOnlyColumnsKey:
            if _isAlert:
                Dialogs.show(translate("Tables", "Read Only Column"),
                             str(translate("Tables", "%s is read only so you can't change it.")) % self.tableColumns[
                                 self.tableColumnsKey.index(_columnKey)])
            return False
        return True


    def exportValues(self, _actionType="return", _formatType="html", _extInfo="no"):
        import os

        info = ""
        if _formatType == "html":
            if _extInfo == "no":
                pass
            elif _extInfo == "title":
                info += " \n<h3>%s : </h3>" % (str(translate("Tables", "Table Contents")))
            info += " \n<table border=1> \n<tr> \n<td>*</td> \n"
            for columnNo in range(self.columnCount()):
                if self.isColumnHidden(columnNo) is False:
                    info += "<td><b>"
                    info += str(self.tableColumns[columnNo])
                    info += "</b></td> \n"
            info += "</tr> \n"
            for rowNo in range(self.rowCount()):
                if self.isRowHidden(rowNo) is False:
                    info += " \n<tr> \n<td>" + str(rowNo + 1) + "</td> \n"
                    for columnNo in range(self.columnCount()):
                        if self.isColumnHidden(columnNo) is False:
                            info += "<td>"
                            info += str(str(self.item(rowNo, columnNo).text()))
                            info += "</td> \n"
                    info += "</tr> \n"
            info += "</table> \n"
        elif _formatType == "plainText":
            if _extInfo == "no":
                pass
            elif _extInfo == "title":
                info += " %s : \n" % (str(translate("Tables", "Table Contents")))
            info += "*\t"
            for columnNo in range(self.columnCount()):
                if self.isColumnHidden(columnNo) is False:
                    info += str(self.tableColumns[columnNo])
                    info += "\t"
            info += "\n"
            for rowNo in range(self.rowCount()):
                info += str(rowNo + 1) + "\t"
                if self.isRowHidden(rowNo) is False:
                    for columnNo in range(self.columnCount()):
                        if self.isColumnHidden(columnNo) is False:
                            info += str(str(self.item(rowNo, columnNo).text()))
                            info += "\t"
                    info += "\n"
        if _actionType == "return":
            return info
        elif _actionType == "file":
            fileExt = None
            formatTypeName = None
            if _formatType == "html":
                if _extInfo != "no":
                    strHeader = ("<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Strict//EN\" \n" +
                                 "\"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd\"> \n" +
                                 "<html xmlns=\"http://www.w3.org/1999/xhtml\" xml:lang=\"tr\" lang=\"tr\" dir=\"ltr\"> \n" +
                                 "<head> \n<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" /> \n</head> \n<body> \n")
                    strFooter = " \n</body> \n</html>"
                    info = strHeader + info + strFooter
                formatTypeName = translate("Tables", "HTML")
                fileExt = "html"
            elif _formatType == "plainText":
                formatTypeName = translate("Tables", "Plain Text")
                fileExt = "txt"
            filePath = Dialogs.getSaveFileName(translate("Tables", "Save As"),
                                               fu.joinPath(fu.userDirectoryPath,
                                                           fu.getBaseName(self.currentDirectoryPath) + "." + fileExt),
                                               formatTypeName + " (*." + fileExt + ")", 2)
            if filePath is not None:
                if _formatType == "html" and filePath[-5:] != ".html":
                    filePath += ".html"
                elif _formatType == "plainText" and filePath[-4:] != ".txt":
                    filePath += ".txt"
                fu.writeToFile(filePath, info)
                Dialogs.show(translate("Tables", "Table Exported"),
                             str(translate("Tables",
                                           "Table contents are exported to file: \"%s\".")) % Organizer.getLink(
                                 filePath))
        elif _actionType == "dialog":
            dDialog = MDialog(getMainWindow())
            if isActivePyKDE4:
                dDialog.setButtons(MDialog.NoDefault)
            dDialog.setWindowTitle(translate("Tables", "Table Contents"))
            mainPanel = MWidget(dDialog)
            vblMain = MVBoxLayout(mainPanel)
            if _formatType == "html":
                QtWebKit = getMyObject("QtWebKit")
                wvWeb = QtWebKit.QWebView()
                wvWeb.setHtml(str(info))
                vblMain.addWidget(wvWeb)
            elif _formatType == "plainText":
                teContent = MTextEdit()
                teContent.setPlainText(str(info))
                vblMain.addWidget(teContent)
            pbtnClose = MPushButton(translate("Tables", "OK"))
            MObject.connect(pbtnClose, SIGNAL("clicked()"), dDialog.close)
            vblMain.addWidget(pbtnClose)
            if isActivePyKDE4:
                dDialog.setMainWidget(mainPanel)
            else:
                dDialog.setLayout(vblMain)
            dDialog.setMinimumWidth(600)
            dDialog.setMinimumHeight(400)
            dDialog.show()
        elif _actionType == "clipboard":
            MApplication.clipboard().setText(str(info))


class MyTableWidgetItem(MTableWidgetItem):
    def __init__(self, _value):
        MTableWidgetItem.__init__(self, str(_value))
        self.currentText = str(_value)
        self.isReadOnly = False
        self.columnKey = None



