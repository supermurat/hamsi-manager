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
import Databases

class Commands:
    global getDirectoriesAndValues, changePath, getDevices, changeTag, getOrSetArtist, getOrSetAlbum, getOrSetYear, getOrSetGenre, getAllMusicFileValues, getMusicFileValues
    
    def getDirectoriesAndValues():
        db = Amarok.checkAndGetDB()
        db.query("""
SELECT DISTINCT (
    REPLACE(
        CONCAT(
            CASE WHEN `devices`.`lastmountpoint` IS NOT NULL
                THEN `devices`.`lastmountpoint`
            ELSE 
                ''
            END, 
            SUBSTRING( `urls`.`rpath` , 2 )
        ),
        CONCAT("/", 
            SUBSTRING_INDEX(
                CONCAT(
                    CASE WHEN `devices`.`lastmountpoint` IS NOT NULL
                        THEN `devices`.`lastmountpoint`
                    ELSE 
                        ''
                    END, 
                    SUBSTRING( `urls`.`rpath` , 2 )
                ), 
                "/" , -1)
        )
    , "")
) AS 'dirPath', `images`.`path` AS 'coverPath', 
`artists`.`name` as 'Artist', 
`albums`.`name` as 'Album', 
`years`.`name` as 'Year', 
`genres`.`name` as 'Genre'
FROM `tracks`
LEFT JOIN `urls` ON `urls`.`id` = `tracks`.`url`
LEFT JOIN `devices` ON `devices`.`id` = `urls`.`deviceid`
LEFT JOIN `artists` ON `artists`.`id` = `tracks`.`artist`
LEFT JOIN `albums` ON `albums`.`id` = `tracks`.`album`
LEFT JOIN `years` ON `years`.`id` = `tracks`.`year`
LEFT JOIN `genres` ON `genres`.`id` = `tracks`.`genre`
LEFT JOIN `images` ON `images`.`id` = `albums`.`image`
WHERE `images`.`path` IS NOT NULL and `images`.`id` NOT IN (SELECT `id` FROM `images` WHERE path not like '/%') 
order by 'dirPath'
""")
        r = db.store_result()
        return r.fetch_row(0)
    
    def getAllMusicFileValues():
        db = Amarok.checkAndGetDB()
        db.query("""
SELECT (
    REPLACE(
        CONCAT(
            CASE WHEN `devices`.`lastmountpoint` IS NOT NULL
                THEN `devices`.`lastmountpoint`
            ELSE 
                ''
            END, 
            SUBSTRING( `urls`.`rpath` , 2 )
        ),
        CONCAT("/", 
                CONCAT(
                    CASE WHEN `devices`.`lastmountpoint` IS NOT NULL
                        THEN `devices`.`lastmountpoint`
                    ELSE 
                        ''
                    END, 
                    SUBSTRING( `urls`.`rpath` , 2 )
                )
        )
    , "")
) AS 'filePath', 
`tracks`.`title` as 'Title', 
`tracks`.`artist` as 'Artist', 
`tracks`.`album` as 'Album', 
`tracks`.`year` as 'Year', 
`tracks`.`genre` as 'Genre'
FROM `tracks`
LEFT JOIN `urls` ON `urls`.`id` = `tracks`.`url`
LEFT JOIN `devices` ON `devices`.`id` = `urls`.`deviceid`
""")
        r = db.store_result()
        return r.fetch_row(0)
        
    def getMusicFileValues(_path):
        db = Amarok.checkAndGetDB()
        db.query("""
SELECT * FROM (
    SELECT `tracks`.`id` as 'id', (
        REPLACE(
            CONCAT(
                CASE WHEN `devices`.`lastmountpoint` IS NOT NULL
                    THEN `devices`.`lastmountpoint`
                ELSE 
                    ''
                END, 
                SUBSTRING( `urls`.`rpath` , 2 )
            ),
            CONCAT("/", 
                    CONCAT(
                        CASE WHEN `devices`.`lastmountpoint` IS NOT NULL
                            THEN `devices`.`lastmountpoint`
                        ELSE 
                            ''
                        END, 
                        SUBSTRING( `urls`.`rpath` , 2 )
                    )
            )
        , "")
    ) AS 'filePath', 
    `tracks`.`title` as 'Title', 
    `tracks`.`artist` as 'Artist', 
    `tracks`.`album` as 'Album', 
    `tracks`.`year` as 'Year', 
    `tracks`.`genre` as 'Genre'
    FROM `tracks`
    LEFT JOIN `urls` ON `urls`.`id` = `tracks`.`url`
    LEFT JOIN `devices` ON `devices`.`id` = `urls`.`deviceid`
) as valueTable WHERE filePath = '%s'
""" % _path)
        r = db.store_result()
        return r.fetch_row(0)[0]
        
    def getDevices():
        db = Amarok.checkAndGetDB()
        db.query("SELECT id,lastmountpoint FROM devices")
        r = db.store_result()
        return r.fetch_row(0)
        
    def getOrSetArtist(_artist):
        db = Amarok.checkAndGetDB()
        db.query(Databases.getAmendedSQLSelectOrInsertAndSelectQueries("artists", "id", {"name" : "'" + _artist + "'"}))
        r = db.store_result()
        return r.fetch_row(0)[0][0]
        
    def getOrSetAlbum(_album, _artistId):
        db = Amarok.checkAndGetDB()
        db.query(Databases.getAmendedSQLSelectOrInsertAndSelectQueries("albums", "id", {"name" : "'" + _album + "'", "artist" : "'" + _artistId + "'"}))
        r = db.store_result()
        return r.fetch_row(0)[0][0]
        
    def getOrSetYear(_year):
        db = Amarok.checkAndGetDB()
        db.query(Databases.getAmendedSQLSelectOrInsertAndSelectQueries("years", "id", {"name" : "'" + _year + "'"}))
        r = db.store_result()
        return r.fetch_row(0)[0][0]
        
    def getOrSetGenre(_genre):
        db = Amarok.checkAndGetDB()
        db.query(Databases.getAmendedSQLSelectOrInsertAndSelectQueries("genres", "id", {"name" : "'" + _genre + "'"}))
        r = db.store_result()
        return r.fetch_row(0)[0][0]
    
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
        
    def changeTag(_values):
        #FIXME: complate this 
        pass
        sqlQuery = ""
        if len(_values)>1:
            db = Amarok.checkAndGetDB()
            path = _values["path"]
            oldValues = getMusicFileValues(path)
            trackId, artistId, albumId, yearId, genreId = oldValues[0], oldValues[3], oldValues[4], oldValues[5], oldValues[6]
            if "Artist" in _values:
                artistId = getOrSetArtist(_values["Artist"])
            if "Title" in _values:
                pass
            if "Album" in _values:
                albumId = getOrSetAlbum(_values["Album"], artistId)
            if "TrackNum" in _values:
                pass
            if "Year" in _values:
                yearId = getOrSetYear(_values["Year"])
            if "Genre" in _values:
                genreId = getOrSetGenre(_values["Genre"])
            if "FirstComment" in _values:
                pass
            if "FirstLyrics" in _values:
                pass
            db.commit()
        return True
        
        
        
        
            

