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
        for sEngine in Variables.getSearchEnginesNames():
            exec ("from " + sEngine + " import pluginName")
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
        MObject.connect(self,SIGNAL("triggered(QAction *)"),self.triggered)

    def triggered(self, _action):
        try:
            if self.parent().rowCount()!=0:
                selectedSearchDepth = 3
                if str(_action.objectName()).find("-MusicBrainz-")!=-1:
                    info = _action.objectName().split("-")
                    engine = Variables.getSearchEnginesNames()[int(info[0])]
                    selectedSearchDepth = info[2]
                else:
                    engine = Variables.getSearchEnginesNames()[int(_action.objectName())]
                exec ("from " + engine + " import Search")
                Search.Search(self.parent(), self.isCheckSingleFile, selectedSearchDepth)
            else:
                Dialogs.show(translate("SearchEngines", "Table Is Empty"), 
                            translate("SearchEngines", "Nothing to be done because the table is empty."))
        except:
            error = ReportBug.ReportBug()
            error.show()
        
        
