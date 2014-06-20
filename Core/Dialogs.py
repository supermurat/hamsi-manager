# # This file is part of HamsiManager.
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


from Core.MyObjects import *
from Core import Universals as uni
import FileUtils as fu
from datetime import datetime
import time


Ok, Cancel, Yes, No, Continue = 1, 2, 3, 4, 5
lastInfoTime = (datetime.now().microsecond / 60000)


def show(_title="Hamsi Manager", _detail="", _btnString=translate("Dialogs", "OK")):
    MApplication.processEvents()
    if _detail == "":
        _detail = _title
        _title = "Hamsi Manager"
    if len(uni.MySettings) > 0 and isActivePyKDE4:
        MMessageBox.information(getActiveWindow(), str("<b>" + str(_title) + " : </b><br>" + str(_detail)),
                                str(str(_title) + "!.."))
    else:
        MMessageBox.information(getActiveWindow(), str(str(_title) + "!.."),
                                str("<b>" + str(_title) + " : </b><br>" + str(_detail)), _btnString)
    return True


def showError(_title="Hamsi Manager", _detail="", _btnString=translate("Dialogs", "OK")):
    MApplication.processEvents()
    if _detail == "":
        _detail = _title
        _title = "Hamsi Manager"
    if len(uni.MySettings) > 0 and isActivePyKDE4:
        MMessageBox.error(getActiveWindow(), str("<b>" + str(_title) + " : </b><br>" + str(_detail)),
                          str(str(_title) + "!.."))
    else:
        MMessageBox.critical(getActiveWindow(), str(str(_title) + "!.."),
                             str("<b>" + str(_title) + " : </b><br>" + str(_detail)), _btnString)
    return True


def ask(_title="Hamsi Manager", _detail="", _isShowCancel=False, _showAgainKeyName=""):
    MApplication.processEvents()
    if _detail == "":
        _detail = _title
        _title = "Hamsi Manager"
    if len(uni.MySettings) > 0 and isActivePyKDE4:
        if _isShowCancel:
            if _showAgainKeyName != "":
                return MMessageBox.messageBox(getActiveWindow(),
                                              MMessageBox.QuestionYesNoCancel,
                                              str("<b>" + str(_title) + " : </b><br>" + str(_detail)),
                                              str(_title),
                                              MStandardGuiItem.yes(), MStandardGuiItem.no(), MStandardGuiItem.cancel(),
                                              str(_showAgainKeyName),
                                              MMessageBox.AllowLink)
            else:
                return MMessageBox.questionYesNoCancel(getActiveWindow(),
                                                       str("<b>" + str(_title) + " : </b><br>" + str(_detail)),
                                                       str(_title),
                                                       MStandardGuiItem.yes(), MStandardGuiItem.no(),
                                                       MStandardGuiItem.cancel(), "",
                                                       MMessageBox.AllowLink)
        else:
            if _showAgainKeyName != "":
                return MMessageBox.messageBox(getActiveWindow(),
                                              MMessageBox.QuestionYesNo,
                                              str("<b>" + str(_title) + " : </b><br>" + str(_detail)),
                                              str(_title),
                                              MStandardGuiItem.yes(), MStandardGuiItem.no(), MStandardGuiItem.cancel(),
                                              str(_showAgainKeyName),
                                              MMessageBox.AllowLink)
            else:
                return MMessageBox.questionYesNo(getActiveWindow(),
                                                 str("<b>" + str(_title) + " : </b><br>" + str(_detail)),
                                                 str(_title),
                                                 MStandardGuiItem.yes(), MStandardGuiItem.no(), "",
                                                 MMessageBox.AllowLink)
    else:
        if _isShowCancel:
            try: mboxDialog = MMessageBox(getActiveWindow())
            except: mboxDialog = MMessageBox(None)
            mboxDialog.setWindowTitle(str(_title))
            mboxDialog.setText(str("<b>" + str(_title) + " : </b><br>" + str(_detail)))
            mboxDialog.setStandardButtons(MMessageBox.Yes | MMessageBox.No | MMessageBox.Cancel)
            pressedButtonNo = mboxDialog.exec_()
        else:
            try: mboxDialog = MMessageBox(getActiveWindow())
            except: mboxDialog = MMessageBox(None)
            mboxDialog.setWindowTitle(str(_title))
            mboxDialog.setText(str("<b>" + str(_title) + " : </b><br>" + str(_detail)))
            mboxDialog.setStandardButtons(MMessageBox.Yes | MMessageBox.No)
            pressedButtonNo = mboxDialog.exec_()
        if pressedButtonNo == 16384: return Yes
        elif pressedButtonNo == 65536: return No
        elif pressedButtonNo == 4194304: return Cancel
        else: return Cancel


def askSpecial(_title="Hamsi Manager", _detail="", _btnString=translate("Dialogs", "Yes"),
               _btnString1=translate("Dialogs", "No"), _btnString2=translate("Dialogs", "Cancel"), _btnString3=None):
    MApplication.processEvents()
    MyMessageBox = MMessageBox
    if len(uni.MySettings) > 0 and isActivePyKDE4:
        MyMessageBox = QMessageBox
    try: mboxDialog = MyMessageBox(getActiveWindow())
    except: mboxDialog = MyMessageBox(None)
    mboxDialog.setWindowTitle(str(_title))
    mboxDialog.setText(str("<b>" + str(_title) + " : </b><br>" + str(_detail)))
    btn = btn1 = btn2 = btn3 = None
    btn = mboxDialog.addButton(_btnString, MyMessageBox.ActionRole)
    if _btnString2 != None:
        btn2 = mboxDialog.addButton(_btnString2, MyMessageBox.ActionRole)
    btn1 = mboxDialog.addButton(_btnString1, MyMessageBox.ActionRole)
    if _btnString3 != None:
        btn3 = mboxDialog.addButton(_btnString3, MyMessageBox.ActionRole)
    else:
        btn3 = None
    mboxDialog.exec_()
    if mboxDialog.clickedButton() == btn:
        return _btnString
    elif mboxDialog.clickedButton() == btn1:
        return _btnString1
    elif mboxDialog.clickedButton() == btn2:
        return _btnString2
    elif mboxDialog.clickedButton() == btn3:
        return _btnString3
    else:
        if btn3 != None:
            return _btnString3
        elif btn2 != None:
            return _btnString2
        elif btn1 != None:
            return _btnString1
        elif btn != None:
            return _btnString


def showState(_title, _value=0, _maxValue=100, _isShowCancel=False, _connectToCancel=None, _isCheckLastShowTime=True):
    global lastInfoTime
    if _isCheckLastShowTime:
        if lastInfoTime == (datetime.now().microsecond / 60000) and _maxValue != _value:
            return None
        else:
            lastInfoTime = (datetime.now().microsecond / 60000)
    if uni.windowMode == uni.windowModeKeys[1] and uni.isCanBeShowOnMainWindow:
        return getMainWindow().StatusBar.showState(_title, _value, _maxValue, _isShowCancel, _connectToCancel)
    MApplication.processEvents()
    if getMainWindow().StateDialog == None:
        getMainWindow().StateDialogStateBar = MProgressBar()
        HBoxs = []
        if uni.getBoolValue("isMinimumWindowMode") and uni.isCanBeShowOnMainWindow:
            if getMainWindow().isLockedMainForm == False:
                getMainWindow().lockForm()
            getMainWindow().StateDialog = MDockWidget(translate("Dialogs", "Progress Bar"))
            getMainWindow().StateDialog.setObjectName(translate("Dialogs", "Progress Bar"))
            pnlState2 = MWidget(getMainWindow().StateDialog)
            getMainWindow().StateDialogTitle = MLabel()
            HBoxs.append(MHBoxLayout(pnlState2))
            HBoxs[0].addWidget(getMainWindow().StateDialogTitle)
            HBoxs[0].addWidget(getMainWindow().StateDialogStateBar)
            getMainWindow().StateDialog.setWidget(pnlState2)
            getMainWindow().StateDialog.setAllowedAreas(Mt.AllDockWidgetAreas)
            getMainWindow().StateDialog.setFeatures(MDockWidget.AllDockWidgetFeatures)
            getMainWindow().addDockWidget(Mt.TopDockWidgetArea, getMainWindow().StateDialog)
            getMainWindow().StateDialog.setMaximumHeight(60)
        else:
            getMainWindow().StateDialog = MDialog(getMainWindow())
            if len(uni.MySettings) > 0 and isActivePyKDE4:
                getMainWindow().StateDialog.setButtons(MDialog.NoDefault)
            getMainWindow().StateDialog.setModal(True)
            getMainWindow().StateDialog.setMinimumWidth(500)
            pnlMain = MWidget(getMainWindow().StateDialog)
            HBoxs.append(MHBoxLayout(pnlMain))
            HBoxs[0].addWidget(getMainWindow().StateDialogStateBar)
            if len(uni.MySettings) > 0 and isActivePyKDE4:
                getMainWindow().StateDialog.setMainWidget(pnlMain)
            else:
                getMainWindow().StateDialog.setLayout(HBoxs[0])
            getMainWindow().StateDialog.show()
        if _isShowCancel:
            pbtnCancel = MPushButton(translate("Dialogs", "Cancel"), getMainWindow().StateDialog)
            if _connectToCancel == None:
                MObject.connect(pbtnCancel, SIGNAL("clicked()"), uni.cancelThreadAction)
            else:
                MObject.connect(pbtnCancel, SIGNAL("clicked()"), _connectToCancel)
            HBoxs[0].addWidget(pbtnCancel)
    getMainWindow().StateDialogStateBar.setRange(0, _maxValue)
    getMainWindow().StateDialogStateBar.setValue(_value)
    if uni.getBoolValue("isMinimumWindowMode") and uni.isCanBeShowOnMainWindow:
        getMainWindow().StateDialog.setVisible(True)
        getMainWindow().StateDialogTitle.setText(_title + " ( " + str(_value) + " / " + str(_maxValue) + " )")
    else:
        getMainWindow().StateDialog.open()
        getMainWindow().StateDialog.setModal(True)
        getMainWindow().StateDialog.setWindowTitle(_title + " ( " + str(_value) + " / " + str(_maxValue) + " )")
    if _value == _maxValue:
        if uni.getBoolValue("isMinimumWindowMode") and uni.isCanBeShowOnMainWindow:
            if getMainWindow().isLockedMainForm:
                getMainWindow().unlockForm()
            getMainWindow().StateDialog.setVisible(False)
            getMainWindow().removeDockWidget(getMainWindow().StateDialog)
        else:
            getMainWindow().StateDialog.setModal(False)
            getMainWindow().StateDialog.close()
        getMainWindow().StateDialog = None


def sleep(_title, _value=0, _isShowCancel=False):
    maxTime = _value * 4
    step = 0
    while step <= maxTime:
        showState(_title, step, maxTime, _isShowCancel)
        step += 1
        time.sleep(0.25)


def getItem(_title="Hamsi Cover", _detail="", _itemList=[""], _currentItem=0):
    if _detail == "":
        _detail = _title
        _title = "Hamsi Cover"
    if len(uni.MySettings) > 0 and isActivePyKDE4:
        selectedValue, isSelected = MInputDialog.getItem(str(str(_title) + "!.."), str(str(_detail)),
                                                         [str(str(x)) for x in _itemList], _currentItem, False)
    else:
        selectedValue, isSelected = MInputDialog.getItem(getActiveWindow(), str(str(_title) + "!.."), str(str(_detail)),
                                                         [str(str(x)) for x in _itemList], _currentItem, False)
    if isSelected == False:
        return None
    return str(selectedValue)


def getText(_title="Hamsi Cover", _detail="", _default=""):
    if _detail == "":
        _detail = _title
        _title = "Hamsi Cover"
    if len(uni.MySettings) > 0 and isActivePyKDE4:
        selectedValue, isSelected = MInputDialog.getText(str(str(_title) + "!.."), str(str(_detail)), str(_default))
    else:
        selectedValue, isSelected = MInputDialog.getText(getActiveWindow(), str(str(_title) + "!.."), str(str(_detail)),
                                                         MLineEdit.Normal, str(_default))
    if isSelected == False:
        return None
    return str(selectedValue)


def getSaveFileName(_caption, _directory, _filter=None, _isUseLastPathKeyType=1, _lastPathKey=None):
    if _filter is None:
        if fu.isFile(_directory):
            fileExt = fu.getFileExtension(_directory)
            if fileExt != "":
                _filter = "*.%s (*.%s)" % (fileExt, fileExt)
            else:
                _filter = "*.* (*.*)"
        else:
            _filter = "*.* (*.*)"
    pathKey = uni.getLastPathKey(_caption, _directory, _filter, _isUseLastPathKeyType, _lastPathKey)
    if pathKey is not None: _directory = uni.getLastPathByEvent(pathKey, _directory)
    filePath = QFileDialog.getSaveFileName(getActiveWindow(), str(_caption),
                                           str(_directory), str(_filter))
    if filePath == "":
        return None
    if pathKey is not None: uni.setLastPathByEvent(pathKey, str(filePath))
    return str(filePath)


def getOpenFileName(_caption, _directory, _filter, _isUseLastPathKeyType=1, _lastPathKey=None):
    pathKey = uni.getLastPathKey(_caption, _directory, _filter, _isUseLastPathKeyType, _lastPathKey)
    if pathKey is not None: _directory = uni.getLastPathByEvent(pathKey, _directory)
    filePath = QFileDialog.getOpenFileName(getActiveWindow(), str(_caption),
                                           str(_directory), str(_filter))
    if filePath == "":
        return None
    if pathKey is not None: uni.setLastPathByEvent(pathKey, str(filePath))
    return str(filePath)


def getOpenFileNames(_caption, _directory, _filter, _isUseLastPathKeyType=1, _lastPathKey=None):
    pathKey = uni.getLastPathKey(_caption, _directory, _filter, _isUseLastPathKeyType, _lastPathKey)
    if pathKey is not None: _directory = uni.getLastPathByEvent(pathKey, _directory)
    filePaths = QFileDialog.getOpenFileNames(getActiveWindow(), str(_caption),
                                             str(_directory), str(_filter))
    if filePaths == []:
        return None
    if pathKey is not None: uni.setLastPathByEvent(pathKey, str(filePaths[-1]))
    return list(filePaths)


def getExistingDirectory(_caption, _directory, _isUseLastPathKeyType=1, _lastPathKey=None):
    pathKey = uni.getLastPathKey(_caption, _directory, "", _isUseLastPathKeyType, _lastPathKey)
    if pathKey is not None: _directory = uni.getLastPathByEvent(pathKey, _directory)
    filePath = QFileDialog.getExistingDirectory(getActiveWindow(), str(_caption),
                                                str(_directory))
    if filePath == "":
        return None
    if pathKey is not None: uni.setLastPathByEvent(pathKey, str(filePath))
    return str(filePath)


class MyStateDialog(MDialog):
    def __init__(self, _title="", _isShowCancel=False, _connectToCancel=None, _isCheckLastShowTime=True):
        MDialog.__init__(self, getMainWindow())
        if len(uni.MySettings) > 0 and isActivePyKDE4:
            self.setButtons(MDialog.NoDefault)
        self.title = _title
        self.isShowCancel = _isShowCancel
        self.connectToCancel = _connectToCancel
        self.isCheckLastShowTime = _isCheckLastShowTime
        self.connect(self, SIGNAL("setState"), self.setState)

    def setTitle(self, _title):
        self.title = _title

    def setState(self, _value=0, _maxValue=100):
        showState(self.title, _value, _maxValue, self.isShowCancel, self.connectToCancel, self.isCheckLastShowTime)
        
        
        
        
        
        
        
        
        
