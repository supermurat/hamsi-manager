# -*- coding: utf-8 -*-

import Variables
from MyObjects import *
import Dialogs
import ReportBug

class SearchEngines(MMenu):
    def __init__(self,  _parent, _isCheckSingleFile=False):
        self.isCheckSingleFile = _isCheckSingleFile
        MMenu.__init__(self, _parent)
        self.setTitle(translate("SearchEngines", "Verify On The Internet"))
        self.actions, self.searchDepths = [], []
        self.searchEnginesNames = Variables.getSearchEnginesNames()
        isAnyAvailable = False
        for sEngine in self.searchEnginesNames:
            exec ("from " + sEngine + " import isAvailable,pluginName")
            if isAvailable:
                isAnyAvailable = True
                self.actions.append(MAction(pluginName.decode("utf-8"), self))
                self.actions[-1].setObjectName(str(len(self.actions)-1))
                self.addAction(self.actions[-1])
                if pluginName=="MusicBrainz":
                    self.mSearchDepth = MMenu()
                    self.mSearchDepth.setTitle(translate("SearchEngines", "MusicBrainz (Choose Search Depth)"))
                    for no in range(1, 12):
                        self.searchDepths.append(MAction(str(no), self.mSearchDepth))
                        self.searchDepths[-1].setObjectName(str(len(self.actions)-1)+"-MusicBrainz-"+str(no))
                        self.mSearchDepth.addAction(self.searchDepths[-1])
                    self.addMenu(self.mSearchDepth )
        if isAnyAvailable==False:
            self.actions.append(MAction(translate("SearchEngines", "You Have Not Any Search Engine"), self))
            self.actions[-1].setObjectName(translate("SearchEngines", "You Have Not Any Search Engine"))
            self.addAction(self.actions[-1])
        MObject.connect(self,SIGNAL("triggered(QAction *)"),self.triggered)

    def triggered(self, _action):
        try:
            if _action.objectName()==translate("SearchEngines", "You Have Not Any Search Engine"):
                Dialogs.show(translate("SearchEngines", "You Have Not Any Search Engine"), 
                                translate("SearchEngines", "Not found any search engine in your system. Please install a search engine module. Now supporting only musicbrainz module (python-musicbrainz2)."))
            else:
                if self.parent().rowCount()!=0:
                    selectedSearchDepth = 3
                    if str(_action.objectName()).find("-MusicBrainz-")!=-1:
                        info = _action.objectName().split("-")
                        engine = self.searchEnginesNames[int(info[0])]
                        selectedSearchDepth = info[2]
                    else:
                        engine = self.searchEnginesNames[int(_action.objectName())]
                    exec ("from " + engine + " import Search")
                    Search(self.parent(), self.isCheckSingleFile, selectedSearchDepth)
                else:
                    Dialogs.show(translate("SearchEngines", "Table Is Empty"), 
                                translate("SearchEngines", "Nothing to be done because the table is empty."))
        except:
            error = ReportBug.ReportBug()
            error.show()
        
        
