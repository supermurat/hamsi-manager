# -*- coding: utf-8 -*-

import Variables
import Universals

if Variables.MyObjectName=="PyQt4":
    from PyQt4 import QtGui
    for obj in dir(QtGui):
        if obj[0]=="Q":
            exec "M"+obj[1:]+" = QtGui." + obj
        else:
            exec obj + " = QtGui." + obj
    from PyQt4 import QtCore
    for obj in dir(QtCore):
        if obj[0]=="Q":
            exec "M"+obj[1:]+" = QtCore." + obj
        else:
            exec obj + " = QtCore." + obj
    from PyQt4 import QtNetwork
    for obj in dir(QtNetwork):
        if obj[0]=="Q":
            exec "M"+obj[1:]+" = QtNetwork." + obj
        else:
            exec obj + " = QtNetwork." + obj
elif Variables.MyObjectName=="PySide":
    from PySide import QtGui
    for obj in dir(QtGui):
        if obj[0]=="Q":
            exec "M"+obj[1:]+" = QtGui." + obj
        else:
            exec obj + " = QtGui." + obj
    from PySide import QtCore
    for obj in dir(QtCore):
        if obj[0]=="Q":
            exec "M"+obj[1:]+" = QtCore." + obj
        else:
            exec obj + " = QtCore." + obj
    from PySide import QtNetwork
    for obj in dir(QtNetwork):
        if obj[0]=="Q":
            exec "M"+obj[1:]+" = QtNetwork." + obj
        else:
            exec obj + " = QtNetwork." + obj
            
if Variables.MyObjectName=="PyQt4" and Universals.MySettings.keys().count("isActivePyKDE4")>0:
    if Universals.isActivePyKDE4==True:
        try:
            from PyKDE4 import kdeui
            for obj in dir(kdeui):
                if obj[0]=="K":
                    exec "M"+obj[1:]+" = kdeui." + obj
                else:
                    exec obj + " = kdeui." + obj
            from PyKDE4 import kdecore
            for obj in dir(kdecore):
                if obj[0]=="K":
                    exec "M"+obj[1:]+" = kdecore." + obj
                else:
                    exec obj + " = kdecore." + obj
            from PyKDE4 import kio
            for obj in dir(kio):
                if obj[0]=="K":
                    exec "M"+obj[1:]+" = kio." + obj
                else:
                    exec obj + " = kio." + obj
            #this PyKDE4 objects different from PyQt4 objects
            QMessageBox = QtGui.QMessageBox
            QDirModel = QtGui.QDirModel
            QIcon = QtGui.QIcon
            MFileDialog = QtGui.QFileDialog 
            MLocale = QtCore.QLocale
            KFileDialog = kio.KFileDialog
            KLocale = kdecore.KLocale
        except:
            Universals.isActivePyKDE4 = False
else:
    #PySide not using with PyKDE4
    Universals.isActivePyKDE4 = False
    
def translate(_p, _s):
    return MApplication.translate(_p, _s)
    
def getMyObject(_objectName):
    if Variables.MyObjectName=="PySide":
        exec "from PySide import " + _objectName + " as MyObject"
    elif Variables.MyObjectName=="PyQt4":
        exec "from PyQt4 import " + _objectName + " as MyObject"
    else:
        MyObject = None
    return MyObject
            
def getMyDialog():
    try:
        if Universals.MainWindow.objectName()=="RealMainWindow":
            return MDialog, "MDialog", Universals.MainWindow
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
    
Universals.isLoadedMyObjects = True
