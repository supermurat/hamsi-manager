## This file is part of HamsiManager.
## 
## Copyright (c) 2010 Murat Demir <mopened@gmail.com>      
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
from Core import Universals

class MyThread(MThread):
    
    def __init__(self, action, callback=None, args=[], kwargs={}):
        MThread.__init__(self, Universals.activeWindow())
        self.action = action
        self.callback = callback
        self.args = args
        self.kwargs = kwargs
        self.data = None
        self.connect(self, SIGNAL("startedCallback"), self.startCallback)
        
    def run(self):
        if len(self.args)==0:
            self.data = self.action(**self.kwargs)
        else:
            self.data = self.action(*self.args, **self.kwargs)
        self.emit(SIGNAL("startedCallback"))
        
    def startCallback(self):
        if self.callback!=None:
            self.callback(self.data)

        
