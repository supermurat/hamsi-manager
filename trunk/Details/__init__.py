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

import FileUtils as fu
from Core.MyObjects import *
from Core import Dialogs
from Core import Organizer
from Core import Universals as uni
from Core import ReportBug
from Core import Execute
import Taggers
from Details import MusicDetails, TextDetails, CoverDetails, ImageDetails, AmarokArtistDetails, HtmlDetails


class Details():
    def __init__(self, _filePath, _isOpenDetailsOnNewWindow):
        try:
            if uni.getBoolValue("isForceOpenWithDefaultApplication"):
                _path = fu.checkSource(_filePath)
                Execute.openWith([_path])
            else:
                _path = fu.checkSource(_filePath, "file", False)
                if _path is not None:
                    isOpened = False
                    mtype = fu.getMimeType(_path)
                    if mtype[0] is not None:
                        if mtype[0].split("/")[0] == "text":
                            TextDetails.TextDetails(_path, _isOpenDetailsOnNewWindow)
                            isOpened = True
                        elif mtype[0].split("/")[0] == "audio":
                            if Taggers.getTagger(True) is not None:
                                MusicDetails.MusicDetails(_path, _isOpenDetailsOnNewWindow)
                                isOpened = True
                        elif mtype[0].split("/")[0] == "image":
                            ImageDetails.ImageDetails(_path, "file", _isOpenDetailsOnNewWindow)
                            isOpened = True
                        elif fu.isBinary(_path) is False:
                            TextDetails.TextDetails(_path, _isOpenDetailsOnNewWindow)
                            isOpened = True
                    else:
                        if fu.isBinary(_path) is False:
                            TextDetails.TextDetails(_path, _isOpenDetailsOnNewWindow)
                            isOpened = True
                    if isOpened is False:
                        if uni.getBoolValue("isOpenWithDefaultApplication"):
                            Execute.openWith([_path])
                        else:
                            Dialogs.showError(translate("Details", "File Is Not Supported"),
                                              str(translate("Details",
                                                            "\"%s\" couldn't opened. This file is not supported.")) % Organizer.getLink(
                                                  str(_path)))
                elif fu.isDir(_filePath):
                    if uni.getBoolValue("isOpenWithDefaultApplication"):
                        Execute.openWith([_filePath])
                    else:
                        Dialogs.showError(translate("Details", "Directories Is Not Supported"),
                                          str(translate("Details",
                                                        "\"%s\" couldn't opened. Directories is not supported to show details.")) % Organizer.getLink(
                                              str(_filePath)))
                else:
                    Dialogs.showError(translate("Details", "File Is Not Exist"),
                                      str(translate("Details",
                                                    "\"%s\" couldn't opened. This file is not exist.")) % Organizer.getLink(
                                          str(_filePath)))
        except:
            answer = Dialogs.askSpecial(translate("Details", "File Couldn't Opened"),
                                        str(translate("Details",
                                                      "\"%s\" couldn't opened. This file may is not supported. <br>If you think this is a bug, please report us.")) % Organizer.getLink(
                                            str(_filePath)),
                                        translate("QuickMake", "Report This Bug"), translate("QuickMake", "OK"), None)
            if answer == translate("QuickMake", "Report This Bug"):
                ReportBug.ReportBug()


def closeAllDialogs():
    for dialog in MusicDetails.currentDialogs:
        try:
            if dialog.isVisible():
                dialog.player.stop()
                dialog.close()
                MusicDetails.currentDialogs.remove(dialog)
        except:
            continue
    for dialog in AmarokArtistDetails.currentDialogs:
        try:
            if dialog.isVisible():
                dialog.close()
                AmarokArtistDetails.currentDialogs.remove(dialog)
        except:
            continue
    for dialog in CoverDetails.currentDialogs:
        try:
            if dialog.isVisible():
                dialog.close()
                CoverDetails.currentDialogs.remove(dialog)
        except:
            continue
    for dialog in HtmlDetails.currentDialogs:
        try:
            if dialog.isVisible():
                dialog.close()
                HtmlDetails.currentDialogs.remove(dialog)
        except:
            continue
    for dialog in TextDetails.currentDialogs:
        try:
            if dialog.isVisible():
                dialog.close()
                TextDetails.currentDialogs.remove(dialog)
        except:
            continue
    for dialog in ImageDetails.currentDialogs:
        try:
            if dialog.isVisible():
                dialog.close()
                ImageDetails.currentDialogs.remove(dialog)
        except:
            continue
