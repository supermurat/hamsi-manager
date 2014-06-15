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


from Core.MyObjects import *
from Core import Universals as uni
from Core import Dialogs
from Core import ReportBug

class SearchEngines(MMenu):
    def __init__(self,  _parent, _isCheckSingleFile=False):
        self.isCheckSingleFile = _isCheckSingleFile
        MMenu.__init__(self, _parent)
        self.setTitle(translate("SearchEngines", "Verify On The Internet"))
        self.actions, self.searchDepths = [], []
        self.searchEnginesNames = uni.getSearchEnginesNames()
        isAnyAvailable = False
        for sEngine in self.searchEnginesNames:
            sEngineModule = __import__("SearchEngines." + sEngine, globals(), locals(), ["isAvailable", "pluginName"], 0)
            if sEngineModule.isAvailable:
                isAnyAvailable = True
                self.actions.append(MAction(str(sEngineModule.pluginName), self))
                self.actions[-1].setObjectName(str(len(self.actions)-1))
                self.addAction(self.actions[-1])
                if sEngineModule.pluginName=="MusicBrainz":
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
                    sEngineModule = __import__("SearchEngines." + engine, globals(), locals(), ["Search"], 0)
                    sEngineModule.Search(self.parent(), self.isCheckSingleFile, selectedSearchDepth)
                else:
                    Dialogs.show(translate("SearchEngines", "Table Is Empty"), 
                                translate("SearchEngines", "Nothing to be done because the table is empty."))
        except:
            ReportBug.ReportBug()
        
        
