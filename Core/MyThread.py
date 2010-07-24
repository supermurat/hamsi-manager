# -*- coding: utf-8 -*-

from MyObjects import *
import Universals
import ReportBug
import Dialogs
import time
from threading import Thread

class MyThread(MThread):
    
    def __init__(self, action, callback, args=[], kwargs={}):
        MThread.__init__(self, Universals.activeWindow())
        self.action = action
        self.callback = callback
        self.args = args
        self.kwargs = kwargs
        self.data = None
        
    def run(self):
        self.data = self.action(*self.args, **self.kwargs)
        self.callback(self.data)
        
    def get(self):
        return self.data

        
