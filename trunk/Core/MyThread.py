# -*- coding: utf-8 -*-

from MyObjects import *
import Universals

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

        
