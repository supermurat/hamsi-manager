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

from urllib import unquote, quote
import Amarok

class Commands:
    global getDirectoriesAndValues, changePath, getDevices
    
    def getDirectoriesAndValues():
        db = Amarok.checkAndGetDB()
        db.query("""
SELECT DISTINCT (
REPLACE(
CONCAT(
CASE WHEN `devices`.`lastmountpoint` IS NOT NULL
THEN `devices`.`lastmountpoint`
ELSE ''
END , SUBSTRING( `urls`.`rpath` , 2 ))
,
CONCAT("/", SUBSTRING_INDEX(
CONCAT(
CASE WHEN `devices`.`lastmountpoint` IS NOT NULL
THEN `devices`.`lastmountpoint`
ELSE ''
END , SUBSTRING( `urls`.`rpath` , 2 ))
, "/" , -1))
, "")
) AS 'dirPath', `images`.`path` AS 'coverPath', 
`artists`.`name` as 'Artist', 
`albums`.`name` as 'Album', 
`genres`.`name` as 'Genre', 
`years`.`name` as 'Year'
FROM `tracks`
LEFT JOIN `urls` ON `urls`.`id` = `tracks`.`url`
LEFT JOIN `devices` ON `devices`.`id` = `urls`.`deviceid`
LEFT JOIN `albums` ON `albums`.`id` = `tracks`.`album`
LEFT JOIN `genres` ON `genres`.`id` = `tracks`.`genre`
LEFT JOIN `years` ON `years`.`id` = `tracks`.`year`
LEFT JOIN `artists` ON `artists`.`id` = `tracks`.`artist`
LEFT JOIN `images` ON `images`.`id` = `albums`.`image`
WHERE `images`.`path` IS NOT NULL and `images`.`id` NOT IN (SELECT `id` FROM `images` WHERE path not like '/%') 
order by 'realPath'
""")
        r = db.store_result()
        return r.fetch_row(0)
        
    def getDevices():
        db = Amarok.checkAndGetDB()
        db.query("SELECT id,lastmountpoint FROM devices")
        r = db.store_result()
        return r.fetch_row(0)
    
    def changePath(_oldPath, _newPath):
        _oldPath, _newPath = str(_oldPath), str(_newPath)
        _oldPathUrl, _newPathUrl = quote(_oldPath), quote(_newPath)
        withOutDevicePoints, withOutDevice = [], []
        for devicePoint in getDevices():
            if devicePoint[1] + "/" == _oldPath[:len(devicePoint[1])+1]:
                if devicePoint[1] + "/" == _newPath[:len(devicePoint[1])+1]:
                    withOutDevicePoints.append({"id":devicePoint[0], 
                                                "oldPath":  _oldPath[len(devicePoint[1]):], 
                                                "newPath": _newPath[len(devicePoint[1]):]
                                                })
                else:
                    withOutDevice.append({"id": devicePoint[0], 
                                        "oldPath":  _oldPath[len(devicePoint[1]):], 
                                        "newPath": _newPath
                                                })
        db = Amarok.checkAndGetDB()
        db.query("UPDATE directories SET dir=REPLACE(dir, '.%s/', '.%s/')" % (_oldPath, _newPath))
        db.query("UPDATE urls SET rpath='.%s' WHERE rpath='.%s'" % (_newPath, _oldPath))
        for withOutDevice in withOutDevice:
            db.query("UPDATE directories SET dir='.%s/', deviceid = -1 WHERE deviceid = %s and dir = '.%s/' " % (withOutDevice["newPath"], withOutDevice["id"], withOutDevice["oldPath"]))
            db.query("UPDATE urls SET rpath='.%s/', deviceid = -1 WHERE deviceid = %s and rpath = '.%s/' " % (withOutDevice["newPath"], withOutDevice["id"], withOutDevice["oldPath"]))
        for withOutDevicePoint in withOutDevicePoints:
            db.query("UPDATE directories SET dir='.%s/' WHERE deviceid = %s and dir = '.%s/'" % (withOutDevicePoint["newPath"], withOutDevicePoint["id"], withOutDevicePoint["oldPath"]))
            db.query("UPDATE urls SET rpath='.%s/' WHERE deviceid = %s and rpath = '.%s/'" % (withOutDevicePoint["newPath"], withOutDevicePoint["id"], withOutDevicePoint["oldPath"]))
        db.query("UPDATE images SET path='%s' WHERE path='%s'" % (_newPath, _oldPath))
        db.query("UPDATE lyrics SET url='.%s' WHERE url='.%s'" % (_newPath, _oldPath))
        db.query("UPDATE statistics_permanent SET url='file://%s' WHERE url='file://%s'" % (_newPathUrl, _oldPathUrl))
        db.commit()
        return True
        
            
            
            

