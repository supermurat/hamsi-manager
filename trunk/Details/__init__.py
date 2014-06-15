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

from Core import Variables
import FileUtils as fu
from Core.MyObjects import *
from Core import Dialogs
from Core import Organizer
from Core import Universals
from Core import ReportBug

class Details():
    
    def __init__(self,_filePath, _isOpenDetailsOnNewWindow):
        try:
            if Universals.getBoolValue("isForceOpenWithDefaultApplication"):
                _path = fu.checkSource(_filePath)
                from Core import Execute
                Execute.openWith([_path])
            else:
                _path = fu.checkSource(_filePath, "file", False)
                if _path is not None:
                    isOpened = False
                    type = fu.getMimeType(_path)
                    if type[0] != None:
                        if type[0].split("/")[0] == "text":
                            from Details import TextDetails
                            TextDetails.TextDetails(_path,_isOpenDetailsOnNewWindow)
                            isOpened = True
                        elif type[0].split("/")[0] == "audio":
                            import Taggers
                            if Taggers.getTagger(True)!=None:
                                from Details import MusicDetails
                                MusicDetails.MusicDetails(_path,_isOpenDetailsOnNewWindow)
                                isOpened = True
                        elif type[0].split("/")[0] == "image":
                            from Details import ImageDetails
                            ImageDetails.ImageDetails(_path, "file", _isOpenDetailsOnNewWindow)    
                            isOpened = True
                        elif fu.isBinary(_path)==False:
                            from Details import TextDetails
                            TextDetails.TextDetails(_path,_isOpenDetailsOnNewWindow)
                            isOpened = True
                    else:
                        if fu.isBinary(_path)==False:
                            from Details import TextDetails
                            TextDetails.TextDetails(_path,_isOpenDetailsOnNewWindow)
                            isOpened = True
                    if isOpened == False:
                        if Universals.getBoolValue("isOpenWithDefaultApplication"):
                            from Core import Execute
                            Execute.openWith([_path])
                        else:
                            Dialogs.showError(translate("Details", "File Is Not Supported"), 
                                 str(translate("Details", "\"%s\" couldn't opened. This file is not supported.")) % Organizer.getLink(str(_path)))
                elif fu.isDir(_filePath):
                    if Universals.getBoolValue("isOpenWithDefaultApplication"):
                        from Core import Execute
                        Execute.openWith([_filePath])
                    else:
                        Dialogs.showError(translate("Details", "Directories Is Not Supported"), 
                                 str(translate("Details", "\"%s\" couldn't opened. Directories is not supported to show details.")) % Organizer.getLink(str(_filePath)))
                else:
                    Dialogs.showError(translate("Details", "File Is Not Exist"), 
                                 str(translate("Details", "\"%s\" couldn't opened. This file is not exist.")) % Organizer.getLink(str(_filePath)))
        except:
            answer = Dialogs.askSpecial(translate("Details", "File Couldn't Opened"),
                        str(translate("Details", "\"%s\" couldn't opened. This file may is not supported. <br>If you think this is a bug, please report us.")) % Organizer.getLink(str(_filePath)), 
                        translate("QuickMake", "Report This Bug"), translate("QuickMake", "OK"), None)
            if answer==translate("QuickMake", "Report This Bug"):
                ReportBug.ReportBug()
        
 
