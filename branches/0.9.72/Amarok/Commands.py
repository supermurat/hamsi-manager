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
    global getDirectoriesAndValues, changePath, getDevices, changeTag, getOrInsertArtist, getOrInsertAlbum, getOrInsertYear, getOrInsertGenre, getAllMusicFileValues, getMusicFileValues, getAllMusicFileValuesWithNames
    
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
) AS 'dirPath', 
`images`.`path`, 
`artists`.`name`, 
`albums`.`name`, 
`years`.`name`, 
`genres`.`name`
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
        directoriesValues = {}
        rows = r.fetch_row(0)
        for row in rows:
            if row[0] not in directoriesValues:
                directoriesValues[row[0]] = {"coverPath" : [], "artist" : [], "album" : [], "year" : [], "genre" : []}
            directoriesValues[row[0]]["coverPath"].append(row[1])
            directoriesValues[row[0]]["artist"].append(row[2])
            directoriesValues[row[0]]["album"].append(row[3])
            directoriesValues[row[0]]["year"].append(row[4])
            directoriesValues[row[0]]["genre"].append(row[5])
        return directoriesValues
    
    def getAllMusicFileValues():
        db = Amarok.checkAndGetDB()
        db.query("""
SELECT `tracks`.`id`, (
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
`tracks`.`title`, 
`tracks`.`artist`, 
`tracks`.`album`, 
`tracks`.`year`, 
`tracks`.`genre`, 
`tracks`.`tracknumber`, 
`tracks`.`comment`
FROM `tracks`
LEFT JOIN `urls` ON `urls`.`id` = `tracks`.`url`
LEFT JOIN `devices` ON `devices`.`id` = `urls`.`deviceid`
""")
        r = db.store_result()
        musicFileValues = []
        rows = r.fetch_row(0)
        for row in rows:
            musicFileValues.append({})
            musicFileValues[-1]["id"] = row[0]
            musicFileValues[-1]["filePath"] = row[1]
            musicFileValues[-1]["title"] = row[2]
            musicFileValues[-1]["artistId"] = row[3]
            musicFileValues[-1]["albumId"] = row[4]
            musicFileValues[-1]["yearId"] = row[5]
            musicFileValues[-1]["genreId"] = row[6]
            musicFileValues[-1]["tracknumber"] = row[7]
            musicFileValues[-1]["comment"] = row[8]
        return musicFileValues
        
    def getAllMusicFileValuesWithNames():
        db = Amarok.checkAndGetDB()
        db.query("""
SELECT `valueTable`.* , `lyrics`.`lyrics` FROM (
    SELECT `tracks`.`id`, CONVERT(
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
    , char(1000)) AS 'filePath', 
    `tracks`.`title`, 
    `tracks`.`artist`, 
    `tracks`.`album`, 
    `tracks`.`year`, 
    `tracks`.`genre`, 
    `tracks`.`tracknumber`, 
    `tracks`.`comment`,
    `artists`.`name` AS 'artistname',
    `albums`.`name` AS 'albumname',
    `albumartists`.`name` AS 'albumartistname',
    `years`.`name` AS 'yearname',
    `genres`.`name` AS 'genrename',
    `images`.`path`
    FROM `tracks`
    LEFT JOIN `urls` ON `urls`.`id` = `tracks`.`url`
    LEFT JOIN `devices` ON `devices`.`id` = `urls`.`deviceid`
    LEFT JOIN `artists` ON `artists`.`id` = `tracks`.`artist`
    LEFT JOIN `albums` ON `albums`.`id` = `tracks`.`album`
    LEFT JOIN `artists` `albumartists` ON `albumartists`.`id` = `albums`.`artist`
    LEFT JOIN `years` ON `years`.`id` = `tracks`.`year`
    LEFT JOIN `genres` ON `genres`.`id` = `tracks`.`genre`
    LEFT JOIN `images` ON `images`.`id` = `albums`.`image`
) as `valueTable`
LEFT JOIN `lyrics` ON `lyrics`.`url` = CONCAT('.' , `valueTable`.`filePath`)
""")
        r = db.store_result()
        musicFileValues = []
        rows = r.fetch_row(0)
        for row in rows:
            musicFileValues.append({})
            musicFileValues[-1]["id"] = row[0]
            musicFileValues[-1]["filePath"] = row[1]
            musicFileValues[-1]["title"] = row[2]
            musicFileValues[-1]["artistId"] = row[3]
            musicFileValues[-1]["albumId"] = row[4]
            musicFileValues[-1]["yearId"] = row[5]
            musicFileValues[-1]["genreId"] = row[6]
            musicFileValues[-1]["tracknumber"] = row[7]
            musicFileValues[-1]["comment"] = row[8]
            musicFileValues[-1]["artist"] = row[9]
            musicFileValues[-1]["album"] = row[10]
            musicFileValues[-1]["albumartist"] = row[11]
            musicFileValues[-1]["year"] = row[12]
            musicFileValues[-1]["genre"] = row[13]
            musicFileValues[-1]["imagePath"] = row[14]
            musicFileValues[-1]["lyrics"] = row[15]
        return musicFileValues
        
    def getMusicFileValues(_path):
        db = Amarok.checkAndGetDB()
        db.query("""
SELECT * FROM (
    SELECT `tracks`.`id`, CONVERT((
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
    ), char(1000)) AS 'filePath', 
    `tracks`.`title`, 
    `tracks`.`artist`, 
    `tracks`.`album`, 
    `tracks`.`year`, 
    `tracks`.`genre`, 
    `tracks`.`tracknumber`, 
    `tracks`.`comment`
    FROM `tracks`
    LEFT JOIN `urls` ON `urls`.`id` = `tracks`.`url`
    LEFT JOIN `devices` ON `devices`.`id` = `urls`.`deviceid`
) as `valueTable` WHERE `valueTable`.`filePath` = '%s'
""" % _path)
        r = db.store_result()
        musicFileValues = {}
        rows = r.fetch_row(0)
        if len(rows)==0:
            return None
        row = rows[0]
        musicFileValues["id"] = row[0]
        musicFileValues["filePath"] = row[1]
        musicFileValues["title"] = row[2]
        musicFileValues["artistId"] = row[3]
        musicFileValues["albumId"] = row[4]
        musicFileValues["yearId"] = row[5]
        musicFileValues["genreId"] = row[6]
        musicFileValues["tracknumber"] = row[7]
        musicFileValues["comment"] = row[8]
        return musicFileValues
        
    def getDevices():
        db = Amarok.checkAndGetDB()
        db.query("SELECT id,lastmountpoint FROM devices")
        r = db.store_result()
        return r.fetch_row(0)
        
    def getOrInsertArtist(_artist):
        db = Amarok.checkAndGetDB()
        for sqlCommand in Databases.getAmendedSQLSelectOrInsertAndSelectQueries("artists", "id", {"name" : "'" + _artist + "'"}):
            db.query(sqlCommand)
        r = db.store_result()
        return r.fetch_row(0)[0][0]
        
    def getOrInsertAlbum(_album, _artistId):
        db = Amarok.checkAndGetDB()
        for sqlCommand in Databases.getAmendedSQLSelectOrInsertAndSelectQueries("albums", "id", {"name" : "'" + _album + "'", "artist" : "'" + _artistId + "'"}):
            db.query(sqlCommand)
        r = db.store_result()
        return r.fetch_row(0)[0][0]
        
    def getOrInsertYear(_year):
        db = Amarok.checkAndGetDB()
        for sqlCommand in Databases.getAmendedSQLSelectOrInsertAndSelectQueries("years", "id", {"name" : "'" + _year + "'"}):
            db.query(sqlCommand)
        r = db.store_result()
        return r.fetch_row(0)[0][0]
        
    def getOrInsertGenre(_genre):
        db = Amarok.checkAndGetDB()
        for sqlCommand in Databases.getAmendedSQLSelectOrInsertAndSelectQueries("genres", "id", {"name" : "'" + _genre + "'"}):
            db.query(sqlCommand)
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
        if len(_values)>1:
            db = Amarok.checkAndGetDB()
            path = _values["path"]
            oldValues = getMusicFileValues(path)
            if oldValues is None:
                return False
            trackId, artistId, albumId, yearId, genreId = oldValues["id"], oldValues["artistId"], oldValues["albumId"], oldValues["yearId"], oldValues["genreId"]
            title = oldValues["title"]
            trackNum = oldValues["tracknumber"]
            firstComment = oldValues["comment"]
            if "artist" in _values:
                artistId = getOrInsertArtist(_values["artist"])
            if "title" in _values:
                title = _values["title"]
            if "album" in _values:
                albumId = getOrInsertAlbum(_values["album"], artistId)
            if "trackNum" in _values:
                trackNum = _values["trackNum"]
            if "year" in _values:
                yearId = getOrInsertYear(_values["year"])
            if "genre" in _values:
                genreId = getOrInsertGenre(_values["genre"])
            if "firstComment" in _values:
                firstComment = _values["firstComment"]
            if "firstLyrics" in _values:
                db.query("UPDATE lyrics SET lyrics='%s' WHERE url='.%s'" % (_values["firstLyrics"], path))
            db.query("UPDATE tracks SET artist=%s, title='%s', album=%s, tracknumber=%s, year=%s, genre=%s, comment='%s' WHERE id=%s" % (artistId, title, albumId, trackNum, yearId, genreId, firstComment, trackId))
            db.commit()
        return True
        
        
        
        
            

