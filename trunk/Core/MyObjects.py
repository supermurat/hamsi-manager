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


from Core import Variables
from Core import Universals

MStringList = None

from PyQt4 import QtGui
for obj in dir(QtGui):
    if obj[0]=="Q":
        exec ("M"+obj[1:]+" = QtGui." + obj)
    else:
        exec (obj + " = QtGui." + obj)
from PyQt4 import QtCore
for obj in dir(QtCore):
    if obj[0]=="Q":
        exec ("M"+obj[1:]+" = QtCore." + obj)
    else:
        exec (obj + " = QtCore." + obj)
from PyQt4 import QtNetwork
for obj in dir(QtNetwork):
    if obj[0]=="Q":
        exec ("M"+obj[1:]+" = QtNetwork." + obj)
    else:
        exec (obj + " = QtNetwork." + obj)
            
if Universals.isActivePyKDE4==True:
    try:
        from PyKDE4 import kdeui
        for obj in dir(kdeui):
            if obj[0]=="K":
                exec ("M"+obj[1:]+" = kdeui." + obj)
            else:
                exec (obj + " = kdeui." + obj)
        from PyKDE4 import kdecore
        for obj in dir(kdecore):
            if obj[0]=="K":
                exec ("M"+obj[1:]+" = kdecore." + obj)
            else:
                exec (obj + " = kdecore." + obj)
        from PyKDE4 import kio
        for obj in dir(kio):
            if obj[0]=="K":
                exec ("M"+obj[1:]+" = kio." + obj)
            else:
                exec (obj + " = kio." + obj)
    except:
        Universals.isActivePyKDE4 = False
    
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
    
def trForUI(_s):
    _s = str(_s)
    return _s
    
def getMyObject(_objectName):
    MyObject = __import__("PyQt4." + _objectName, globals(), locals(), [_objectName], -1)
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
    
def setCompleter(_object, _objectName=None):
    if Universals.getBoolValue("isShowAllForCompleter"):
        _objectName = "%*%"
    from Databases import CompleterTable
    if _objectName==None:
        _objectName = _object.objectName()
    _objectName = str(_objectName)
    cmpCompleter = MCompleter(CompleterTable.fetchAllByObjectName(_objectName))
    cmpCompleter.setCaseSensitivity(Mt.CaseInsensitive)
    _object.setCompleter(cmpCompleter)

Universals.isLoadedMyObjects = True
