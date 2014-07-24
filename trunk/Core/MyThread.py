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


from Core.MyObjects import *
from Core import Universals as uni
from Core import Dialogs
import time


class MyThread(MThread):
    def __init__(self, action, callback=None, args=[], kwargs={}):
        MThread.__init__(self, getActiveWindow())
        self.action = action
        self.callback = callback
        self.args = args
        self.kwargs = kwargs
        self.data = None
        self.connect(self, SIGNAL("startedCallback"), self.startCallback)

    def run(self):
        if len(self.args) == 0:
            self.data = self.action(**self.kwargs)
        else:
            self.data = self.action(*self.args, **self.kwargs)
        self.emit(SIGNAL("startedCallback"))

    def startCallback(self):
        if self.callback is not None:
            if type(self.callback) is list:
                for cb in self.callback:
                    cb(self.data)
            else:
                self.callback(self.data)


class MyTarPackStateThread(MThread):
    def __init__(self, _tarFile, _maxMembers, _dlgState):
        MThread.__init__(self, getActiveWindow())
        self.isFinished = False
        self.tarFile = _tarFile
        self.maxMembers = _maxMembers
        self.dlgState = _dlgState

    def run(self):
        while self.isFinished is False:
            self.dlgState.emit(SIGNAL("setState"), len(self.tarFile.members), self.maxMembers)
            time.sleep(0.05)

    def finish(self, _returnValue=None):
        self.isFinished = True


class MyWaitThread(MThread):
    def __init__(self, _title):
        MThread.__init__(self, getActiveWindow())
        self.isFinished = False
        self.dlgState = Dialogs.MyStateDialog(_title, False, None, False)

    def run(self):
        i = 0
        while self.isFinished is False:
            if i > 9:
                i = 0
            self.dlgState.emit(SIGNAL("setState"), i, 10)
            time.sleep(0.05)
            i += 1
        self.dlgState.emit(SIGNAL("setState"), 10, 10)

    def finish(self, _returnValue=None):
        self.isFinished = True

