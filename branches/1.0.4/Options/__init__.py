## This file is part of HamsiManager.
## 
## Copyright (c) 2010 - 2012 Murat Demir <mopened@gmail.com>      
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

class MyComboBox(MComboBox):
    
    def __init__(self, _parent, _items, _defaultItemIndex=0, _settingKey = None, _currentIndexChanged = None):
        MComboBox.__init__(self, _parent)
        self.items = _items
        self.settingKey = _settingKey
        self.currentIndexChanged = _currentIndexChanged
        self.addItems(_items)
        if _settingKey is not None:
            self.setCurrentIndex(_items.index(Universals.MySettings[self.settingKey]))
        else:
            self.setCurrentIndex(_defaultItemIndex)
        if _currentIndexChanged is not None or _settingKey is not None:
            MObject.connect(self, SIGNAL("currentIndexChanged(int)"), self.cbMCurrentIndexChanged)
            
    def cbMCurrentIndexChanged(self, _index = None):
        if self.settingKey is not None:
            Universals.setMySetting(self.settingKey, self.items[self.currentIndex()])
        if self.currentIndexChanged is not None:
            self.currentIndexChanged()
        
class MyCheckBox(MCheckBox):
    
    def __init__(self, _parent, _text, _defaultState=0, _settingKey = None, _stateChanged = None):
        MCheckBox.__init__(self, _text, _parent)
        self.settingKey = _settingKey
        self.stateChanged = _stateChanged
        if _settingKey is not None:
            if Universals.getBoolValue(_settingKey):
                self.setCheckState(Mt.Checked)
            else:
                self.setCheckState(Mt.Unchecked)
        else:
            self.setCheckState(_defaultState)
        if _stateChanged is not None or _settingKey is not None:
            MObject.connect(self, SIGNAL("stateChanged(int)"), self.cckbMStateChanged)
            
    def cckbMStateChanged(self, _index = None):
        if self.settingKey is not None:
            if self.checkState() == Mt.Checked:
                Universals.setMySetting(self.settingKey, True)
            else:
                Universals.setMySetting(self.settingKey, False)
        if self.stateChanged is not None:
            self.stateChanged()
        
        
        
        
        
        
