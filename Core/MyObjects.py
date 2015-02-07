# This file is part of HamsiManager.
#
# Copyright (c) 2010 - 2014 Murat Demir <mopened@gmail.com>
#
# Hamsi Manager is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Hamsi Manager is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with HamsiManager; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import sys

MStringList = None
isActivePyKDE4 = None
isPython3k = float(sys.version[:3]) >= 3.0
MainWindowUseGetMainWindow = None
HamsiManagerAppUseGetApplication = None

# region Just for make PyCharm let me free :-)
MDial = MDialog = MGroupBox = MHBox = MHBoxLayout = MIcon = MLabel = MLine = MLineEdit = MPushButton = MTextEdit = None
MVBox = MVBoxLayout = MWidget = SIGNAL = MApplication = MMainWindow = MComboBox = MObject = MSize = MToolBar = None
MWidgetAction = MMessage = MMessageBox = Mt = MAction = MMenu = MMenuBar = MProgressBar = MStatusBar = None
MActionGroup = MDockWidget = MInputDialog = MStandardGuiItem = MCompleter = MConfig = MConfigGroup = MDir = None
MDirLister = MDirModel = MDirOperator = MDirSortFilterProxyModel = MFile = MFilePlacesModel = MFilePlacesView = None
MGlobal = MListView = MTreeView = MUrl = MUrlNavigator = MThread = MTabWidget = MTextOption = None
MNetworkAccessManager = MNetworkReply = MNetworkRequest = MT_VERSION = MT_VERSION_STR = PYQT_VERSION = None
PYQT_VERSION_STR = kdecore = QtCore = QtGui = kdeui = MFileInfo = MSpinBox = MTableWidget = MTableWidgetItem = None
MCheckBox = MListWidget = MListWidgetItem = MPixmap = MPlainTextEdit = MState = MGlobalSettings = MShared = None
MSharedConfig = MEditListBox = MFormLayout = MToolBox = MFrame = MMovie = MScrollArea = MToolButton = MGridLayout = None
MTime = MTimer = MByteArray = MBrush = MColor = MAboutData = MCmdLineArgs = MCmdLineOptions = MLocale = MString = None
MTextCodec = MTranslator = i18n = ki18n = MCursor = MPalette = MTextBrowser = MFont = MRect = None
MGraphicsOpacityEffect = MPropertyAnimation = MEasingCurve = MAbstractAnimation = None
# endregion

from PyQt4 import QtGui

for obj in dir(QtGui):
    if obj[0] == "Q":
        exec ("M" + obj[1:] + " = QtGui." + obj)
    else:
        exec (obj + " = QtGui." + obj)
from PyQt4 import QtCore

for obj in dir(QtCore):
    if obj[0] == "Q":
        exec ("M" + obj[1:] + " = QtCore." + obj)
    elif obj is not "oct":
        exec (obj + " = QtCore." + obj)
from PyQt4 import QtNetwork

for obj in dir(QtNetwork):
    if obj[0] == "Q":
        exec ("M" + obj[1:] + " = QtNetwork." + obj)
    else:
        exec (obj + " = QtNetwork." + obj)

MQtGui, MQtCore = QtGui, QtCore

# noinspection PyCallByClass
MQtCore.QTextCodec.setCodecForCStrings(MQtCore.QTextCodec.codecForName("utf-8"))
# noinspection PyCallByClass
MQtCore.QTextCodec.setCodecForTr(MQtCore.QTextCodec.codecForName("utf-8"))

try:
    from PyKDE4 import kdeui

    for obj in dir(kdeui):
        if obj[0] == "K":
            exec ("M" + obj[1:] + " = kdeui." + obj)
        else:
            exec (obj + " = kdeui." + obj)
    from PyKDE4 import kdecore

    for obj in dir(kdecore):
        if obj[0] == "K":
            exec ("M" + obj[1:] + " = kdecore." + obj)
        else:
            exec (obj + " = kdecore." + obj)
    from PyKDE4 import kio

    for obj in dir(kio):
        if obj[0] == "K":
            exec ("M" + obj[1:] + " = kio." + obj)
        else:
            exec (obj + " = kio." + obj)
    isActivePyKDE4 = True
except:
    isActivePyKDE4 = False

#this PyKDE4 objects different from PyQt4 objects
QLocale = QtCore.QLocale
QFileDialog = QtGui.QFileDialog
QMessageBox = QtGui.QMessageBox
QDirModel = QtGui.QDirModel
QIcon = QtGui.QIcon

if MStringList is None:
    def MStringList(_s):
        return [_s]


def translate(_p, _s):
    return str(MApplication.translate(_p, _s))


def trStr(_s):
    if isPython3k:
        return _s
    return _s.toString()


def trQVariant(_s):
    if isPython3k:
        return _s
    return MQtCore.QVariant(str(_s))


def clearAllChildren(_object, _isClearThis=False):
    children = _object.children()
    for child in children:
        clearAllChildren(child, True)
    if _isClearThis:
        try:
            _object.hide()
            _object.deleteLater()
        except: pass


def getAllChildren(_object, _objectName=None):
    children = _object.children()
    if _objectName is not None:
        selectedChildren = []
        for child in children:
            if str(child.objectName()).find(_objectName) > -1:
                selectedChildren.append(child)
        return selectedChildren
    return children


def getChild(_object, _objectName):
    children = getAllChildren(_object)
    for child in children:
        if str(child.objectName()) == str(_objectName):
            return child
    return None


def getMyObject(_objectName):
    MyObject = __import__("PyQt4." + _objectName, globals(), locals(), [_objectName], 0)
    return MyObject


def getMyDialog():
    try:
        if getMainWindow().objectName() == "RealMainWindow":
            return MDialog, "MDialog", getMainWindow()
        else:
            return MMainWindow, "MMainWindow", None
    except:
        return MMainWindow, "MMainWindow", None


def moveToCenter(_dialog):
    scrn = 0
    if MApplication.desktop().isVirtualDesktop():
        scrn = MApplication.desktop().screenNumber(MCursor.pos())
    else:
        scrn = MApplication.desktop().screenNumber(_dialog)
    desk = MApplication.desktop().availableGeometry(scrn)
    _dialog.move(int((desk.width() - _dialog.width()) / 2),
                 int((desk.height() - _dialog.height()) / 2))


def setCompleter(_object, _objectName=None):
    from Core import Universals as uni

    if uni.getBoolValue("isShowAllForCompleter"):
        _objectName = "%*%"
    from Databases import CompleterTable

    if _objectName is None:
        _objectName = _object.objectName()
    _objectName = str(_objectName)
    cmpCompleter = MCompleter(CompleterTable.fetchAllByObjectName(_objectName))
    cmpCompleter.setCaseSensitivity(Mt.CaseInsensitive)
    _object.setCompleter(cmpCompleter)


def setApplication(_app):
    global HamsiManagerAppUseGetApplication
    HamsiManagerAppUseGetApplication = _app


def getApplication(_app):
    return HamsiManagerAppUseGetApplication


def setMainWindow(_mainWindow):
    global MainWindowUseGetMainWindow
    MainWindowUseGetMainWindow = _mainWindow
    MainWindowUseGetMainWindow.StateDialog = None
    MainWindowUseGetMainWindow.StateDialogStateBar = None
    MainWindowUseGetMainWindow.StateDialogTitle = None
    MainWindowUseGetMainWindow.Menu = None
    MainWindowUseGetMainWindow.Bars = None
    MainWindowUseGetMainWindow.StatusBar = None
    MainWindowUseGetMainWindow.ToolsBar = None
    MainWindowUseGetMainWindow.TableToolsBar = None
    MainWindowUseGetMainWindow.FileManager = None
    MainWindowUseGetMainWindow.CentralWidget = None


def getMainWindow():
    return MainWindowUseGetMainWindow


def getActiveWindow():
    if MApplication.activeModalWidget() is not None:
        return MApplication.activeModalWidget()
    else:
        return getMainWindow()


def getMainTable():
    return MainWindowUseGetMainWindow.Table


def setMainTable(_table):
    MainWindowUseGetMainWindow.Table = _table


class MyComboBox(MComboBox):
    def __init__(self):
        MComboBox.__init__(self)

    def currentData(self):
        return trStr(self.itemData(self.currentIndex()))

    def addDataItems(self, _keys, _names):
        for x, key in enumerate(_keys):
            self.addItem(_names[x], trQVariant(key))
