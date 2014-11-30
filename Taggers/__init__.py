# This file is part of HamsiManager.
#
# Copyright (c) 2010 - 2014 Murat Demir <mopened@gmail.com>
#
# Hamsi Manager is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Hamsi Manager is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with HamsiManager; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA


from Core.MyObjects import *
from Core import Universals as uni
from Core import Dialogs
from Core import ReportBug

taggersNames = []
loaddedTagger = None


def getTagger(_isAlertIfNotExist=False, _isReloadAgain=False):
    global taggersNames, loaddedTagger
    try:
        if not _isReloadAgain and loaddedTagger is not None:
            return loaddedTagger
        if len(taggersNames) == 0:
            taggersNames = uni.getTaggersNames()
        # TODO: make people to select their options # default should be mutagen!
        # if taggersNames.index("mutagenTagger"):
        #     taggersNames = ["mutagen3Tagger"]
        for tagger in taggersNames:
            taggerModule = __import__("Taggers." + tagger, globals(), locals(), ["isAvailable", "Tagger", tagger], 0)
            if taggerModule.isAvailable:
                loaddedTagger = taggerModule.Tagger()
                return loaddedTagger
        if _isAlertIfNotExist:
            Dialogs.show(translate("Taggers", "You Have Not Any Tagger"),
                         translate("Taggers", "Not found any tagger in your system. "
                                              "Please install a tagger module. "
                                              "Now supporting only eyeD3 module (python-eyed3)."))
        return None
    except:
        ReportBug.ReportBug()
