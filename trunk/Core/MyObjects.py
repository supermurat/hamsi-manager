# -*- coding: utf-8 -*-

#tr(self,"File")
#myTr("File")
#translate("HamsiManager","File")

import Universals
isPySide = False
if Universals.MySettings.keys().count("NeededObjectsName")>0:
    if Universals.MySettings["NeededObjectsName"]=="PySide":
        isPySide = True
        from PySide import QtWebKit
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
                
if isPySide==False:
    from PyQt4 import QtWebKit
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
  
def tr(_p, _s):
    return _p.tr(_s)
    
def myTr(_s):
    return MApplication.translate("HamsiManager", _s)
        
def translate(_p, _s):
    return MApplication.translate(_p, _s)

if Universals.MySettings.keys().count("isActivePyKDE4")>0:
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
            from PyKDE4.kio import *
            from PyKDE4 import kio
            for obj in dir(kio):
                if obj[0]=="K":
                    exec "M"+obj[1:]+" = kio." + obj
                else:
                    exec obj + " = kio." + obj
            #this PyKDE4 objects different from PyQt4 objects
            QMessageBox = QtGui.QMessageBox
            QDirModel = QtGui.QDirModel
            MFileDialog = QtGui.QFileDialog 
            MLocale = QtCore.QLocale
            
            KFileDialog = kio.KFileDialog
            KLocale = kdecore.KLocale
        except:
            Universals.isActivePyKDE4 = False
            
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
