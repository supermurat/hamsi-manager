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
import re
import Amarok
import Databases
import Universals

class Commands:
    global getSQLConditionByFilter, getDirectoriesAndValues, changeFilePath, changeDirectoryPath, getDevices, changeTag, getOrInsertArtist, getOrInsertAlbum, getOrInsertYear, getOrInsertGenre, getAllMusicFileValues, getMusicFileValues, getAllMusicFileValuesWithNames, getAllArtistsValues, changeArtistValue, changeArtistWithAnother, getArtistId, deleteArtist, getAllMusicFilePathsByArtistId, getArtistName, getAllMusicFileValuesWithNamesByArtistId, getSQLConditionPartByPartOfFilter, getSQLConditionValues
    
    def getSQLConditionPartByPartOfFilter(_partOfFilterString = "", _isValueTable = True):
        _partOfFilterString = _partOfFilterString.strip()
        while _partOfFilterString.find(" :")!=-1:
            _partOfFilterString=_partOfFilterString.replace(" :",":")
        while _partOfFilterString.find(": ")!=-1:
            _partOfFilterString=_partOfFilterString.replace(": ",":")
        while _partOfFilterString.find(" <")!=-1:
            _partOfFilterString=_partOfFilterString.replace(" <","<")
        while _partOfFilterString.find("< ")!=-1:
            _partOfFilterString=_partOfFilterString.replace("< ","<")
        while _partOfFilterString.find(" >")!=-1:
            _partOfFilterString=_partOfFilterString.replace(" >",">")
        while _partOfFilterString.find("> ")!=-1:
            _partOfFilterString=_partOfFilterString.replace("> ",">")
        _partOfFilterString = _partOfFilterString.replace("\"", "")
        _partOfFilterString = Databases.correctForSql(_partOfFilterString)
        if _partOfFilterString.find("filename:")!=-1:
            filterPart = _partOfFilterString.replace("filename:", "")
            if _isValueTable:
                return " ( LOWER(`valueTable`.`filePath`) LIKE LOWER('%s') ) " % ("%" + filterPart + "%")
            else:
                return " ( LOWER(`urls`.`rpath`) LIKE LOWER('%s') ) " % ("%" + filterPart + "%")
        elif _partOfFilterString.find("title:")!=-1:
            filterPart = _partOfFilterString.replace("title:", "")
            if _isValueTable:
                return " ( LOWER(`valueTable`.`title`) LIKE LOWER('%s') ) " % ("%" + filterPart + "%")
            else:
                return " ( LOWER(`tracks`.`title`) LIKE LOWER('%s') ) " % ("%" + filterPart + "%")
        elif _partOfFilterString.find("artist:")!=-1:
            filterPart = _partOfFilterString.replace("artist:", "")
            if _isValueTable:
                return " ( LOWER(`valueTable`.`artistname`) LIKE LOWER('%s') ) " % ("%" + filterPart + "%")
            else:
                return " ( LOWER(`artists`.`name`) LIKE LOWER('%s') ) " % ("%" + filterPart + "%")
        elif _partOfFilterString.find("album:")!=-1:
            filterPart = _partOfFilterString.replace("album:", "")
            if _isValueTable:
                return " ( LOWER(`valueTable`.`albumname`) LIKE LOWER('%s') ) " % ("%" + filterPart + "%")
            else:
                return " ( LOWER(`albums`.`name`) LIKE LOWER('%s') ) " % ("%" + filterPart + "%")
        elif _partOfFilterString.find("albumartist:")!=-1:
            filterPart = _partOfFilterString.replace("albumartist:", "")
            if _isValueTable:
                return " ( LOWER(`valueTable`.`albumartistname`) LIKE LOWER('%s') ) " % ("%" + filterPart + "%")
            else:
                return " ( LOWER(`albumartists`.`name`) LIKE LOWER('%s') ) " % ("%" + filterPart + "%")
        elif _partOfFilterString.find("genre:")!=-1:
            filterPart = _partOfFilterString.replace("genre:", "")
            if _isValueTable:
                return " ( LOWER(`valueTable`.`genrename`) LIKE LOWER('%s') ) " % ("%" + filterPart + "%")
            else:
                return " ( LOWER(`genres`.`name`) LIKE LOWER('%s') ) " % ("%" + filterPart + "%")
        elif _partOfFilterString.find("comment:")!=-1:
            filterPart = _partOfFilterString.replace("comment:", "")
            if _isValueTable:
                return " ( LOWER(`valueTable`.`comment`) LIKE LOWER('%s') ) " % ("%" + filterPart + "%")
            else:
                return " ( LOWER(`tracks`.`comment`) LIKE LOWER('%s') ) " % ("%" + filterPart + "%")
        elif _partOfFilterString.find("rating:<")!=-1:
            filterPart = _partOfFilterString.replace("rating:<", "").replace(".", ",")
            try: filterPart = int(float(filterPart) * 2)
            except: filterPart = 0
            if _isValueTable:
                return " ( `valueTable`.`rating` < %s ) " % (filterPart)
            else:
                return " ( `statistics`.`rating` < %s ) " % (filterPart)
        elif _partOfFilterString.find("rating:>")!=-1:
            filterPart = _partOfFilterString.replace("rating:>", "").replace(".", ",")
            try: filterPart = int(float(filterPart) * 2)
            except: filterPart = 0
            if _isValueTable:
                return " ( `valueTable`.`rating` > %s ) " % (filterPart)
            else:
                return " ( `statistics`.`rating` > %s ) " % (filterPart)
        elif _partOfFilterString.find("rating:")!=-1:
            filterPart = _partOfFilterString.replace("rating:", "").replace(".", ",")
            try: filterPart = int(float(filterPart) * 2)
            except: filterPart = 0
            if _isValueTable:
                return " ( `valueTable`.`rating` = %s ) " % (filterPart)
            else:
                return " ( `statistics`.`rating` = %s ) " % (filterPart)
        else:
            filterPart = _partOfFilterString
            if _isValueTable:
                return " ( LOWER(`valueTable`.`filePath`) LIKE LOWER('%s') OR LOWER(`valueTable`.`title`) LIKE LOWER('%s') OR LOWER(`valueTable`.`artistname`) LIKE LOWER('%s') OR LOWER(`valueTable`.`albumname`) LIKE LOWER('%s') OR LOWER(`valueTable`.`albumartistname`) LIKE LOWER('%s') OR LOWER(`valueTable`.`genrename`) LIKE LOWER('%s') OR LOWER(`valueTable`.`comment`) LIKE LOWER('%s') ) " % ("%" + filterPart + "%", "%" + filterPart + "%", "%" + filterPart + "%", "%" + filterPart + "%", "%" + filterPart + "%", "%" + filterPart + "%", "%" + filterPart + "%")
            else:
                return " ( LOWER(`urls`.`rpath`) LIKE LOWER('%s') OR LOWER(`tracks`.`title`) LIKE LOWER('%s') OR LOWER(`artists`.`name`) LIKE LOWER('%s') OR LOWER(`albums`.`name`) LIKE LOWER('%s') OR LOWER(`albumartists`.`name`) LIKE LOWER('%s') OR LOWER(`genres`.`name`) LIKE LOWER('%s') OR LOWER(`tracks`.`comment`) LIKE LOWER('%s') ) " % ("%" + filterPart + "%", "%" + filterPart + "%", "%" + filterPart + "%", "%" + filterPart + "%", "%" + filterPart + "%", "%" + filterPart + "%", "%" + filterPart + "%")
        
    def getSQLConditionValues(sqlCondition, _filter, _listOfFilters, _isValueTable = True):
        for f in _listOfFilters:
            _filter.replace(f, "__filter__")
            appendingConditionControl = re.findall(r"((OR|AND)? *__filter__)", _filter) #[('OR __filter__', 'OR')]
            if len(appendingConditionControl)>0:
                appendingCondition = " " + appendingConditionControl[0][1] + " "
                deleteThisFromFilter = appendingConditionControl[0][0]
            else:
                appendingCondition = " AND "
                deleteThisFromFilter = f
            sqlCondition += appendingCondition + getSQLConditionPartByPartOfFilter(f, _isValueTable)
            _filter = _filter.replace(deleteThisFromFilter, " ")
        return sqlCondition, _filter.strip()
    
    def getSQLConditionByFilter(_filter = "", _isValueTable = True, _isAppendWhere = True):
        _filter = str(_filter).strip().replace("\t", " ").replace("\n", " ")
        while _filter.find("  ")!=-1:
            _filter=_filter.replace("  "," ")
        if _filter == "":
            return ""
        if _filter.count("\"") % 2 != 0:
            return "" # Incorrect filter string
        if _isAppendWhere : sqlCondition = " WHERE "
        else: sqlCondition = ""
        listOfSpecialAndQuoted = re.findall(r"([a-zA-Z]* ?: ?\"[ a-zA-Z0-9+_\-\.]*\")", _filter) #['artist:"like this"']
        sqlCondition, _filter = getSQLConditionValues(sqlCondition, _filter, listOfSpecialAndQuoted, _isValueTable)
        listOfSpecial1 = re.findall(r"([a-zA-Z]* ?: ?< ?[a-zA-Z0-9+_\-\.]+)", _filter) #['rating:<likeThis']
        sqlCondition, _filter = getSQLConditionValues(sqlCondition, _filter, listOfSpecial1, _isValueTable)
        listOfSpecial2 = re.findall(r"([a-zA-Z]* ?: ?> ?[a-zA-Z0-9+_\-\.]+)", _filter) #['rating:>likeThis']
        sqlCondition, _filter = getSQLConditionValues(sqlCondition, _filter, listOfSpecial2, _isValueTable)
        listOfSpecial = re.findall(r"([a-zA-Z]* ?: ?[a-zA-Z0-9+_\-\.]+)", _filter) #['artist:likeThis']
        sqlCondition, _filter = getSQLConditionValues(sqlCondition, _filter, listOfSpecial, _isValueTable)
        listOfQuoted = re.findall(r"(\"[ a-zA-Z0-9+_\-\.]*\")", _filter) #['"like this"']
        sqlCondition, _filter = getSQLConditionValues(sqlCondition, _filter, listOfQuoted, _isValueTable)
        listOfFilters = _filter.split(" ")
        if listOfFilters != [""]:
            sqlCondition, _filter = getSQLConditionValues(sqlCondition, _filter, listOfFilters, _isValueTable)
        sqlControl = re.findall(r"(WHERE *(OR|AND)?)", sqlCondition)
        if len(sqlControl)>0:
            sqlCondition = sqlCondition.replace(sqlControl[0][0], "WHERE ")
        return sqlCondition
    
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
        
    def getAllMusicFileValuesWithNames(_filter = ""):
        db = Amarok.checkAndGetDB()
        query = """
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
    `images`.`path`,
    `statistics`.`rating`
    FROM `tracks`
    LEFT JOIN `urls` ON `urls`.`id` = `tracks`.`url`
    LEFT JOIN `devices` ON `devices`.`id` = `urls`.`deviceid`
    LEFT JOIN `artists` ON `artists`.`id` = `tracks`.`artist`
    LEFT JOIN `albums` ON `albums`.`id` = `tracks`.`album`
    LEFT JOIN `artists` `albumartists` ON `albumartists`.`id` = `albums`.`artist`
    LEFT JOIN `years` ON `years`.`id` = `tracks`.`year`
    LEFT JOIN `genres` ON `genres`.`id` = `tracks`.`genre`
    LEFT JOIN `images` ON `images`.`id` = `albums`.`image`
    LEFT JOIN `statistics` ON `statistics`.`url` = `tracks`.`url`
) as `valueTable`
LEFT JOIN `lyrics` ON `lyrics`.`url` = CONCAT('.' , `valueTable`.`filePath`)
""" + getSQLConditionByFilter(_filter)
        Universals.printForDevelopers("Query - getAllMusicFileValuesWithNames : " + query)
        db.query(query)
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
        
    def getAllMusicFileValuesWithNamesByArtistId(_artistId):
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
    WHERE `tracks`.`artist`=""" + _artistId + """ OR `albums`.`artist`=""" + _artistId + """
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
        
    def getAllMusicFilePathsByArtistId(_artistId):
        db = Amarok.checkAndGetDB()
        db.query("""
    SELECT CONVERT(
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
    , char(1000)) AS 'filePath'
    FROM `tracks`
    LEFT JOIN `urls` ON `urls`.`id` = `tracks`.`url`
    LEFT JOIN `devices` ON `devices`.`id` = `urls`.`deviceid`
    WHERE `tracks`.`artist`=""" + _artistId)
        r = db.store_result()
        musicFileValues = []
        rows = r.fetch_row(0)
        for row in rows:
            musicFileValues.append(row[0])
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
""" % Databases.correctForSql(_path))
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
        
    def getAllArtistsValues(_filter = "", _isOnlyArtistFilter = False):
        db = Amarok.checkAndGetDB()
        _filter = str(_filter).strip()
        if _isOnlyArtistFilter:
            if _filter!="":
                db.query("SELECT `id`,`name` FROM `artists` WHERE LOWER(`name`) like LOWER('%s')" % ("%" + _filter + "%"))
            else:
                db.query("SELECT `id`,`name` FROM `artists`")
        else:
            db.query("""
SELECT DISTINCT `artistTable`.`artist`, `artistTable`.`artistname` FROM (
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
        `images`.`path`,
        `statistics`.`rating`
        FROM `tracks`
        LEFT JOIN `urls` ON `urls`.`id` = `tracks`.`url`
        LEFT JOIN `devices` ON `devices`.`id` = `urls`.`deviceid`
        LEFT JOIN `artists` ON `artists`.`id` = `tracks`.`artist`
        LEFT JOIN `albums` ON `albums`.`id` = `tracks`.`album`
        LEFT JOIN `artists` `albumartists` ON `albumartists`.`id` = `albums`.`artist`
        LEFT JOIN `years` ON `years`.`id` = `tracks`.`year`
        LEFT JOIN `genres` ON `genres`.`id` = `tracks`.`genre`
        LEFT JOIN `images` ON `images`.`id` = `albums`.`image`
        LEFT JOIN `statistics` ON `statistics`.`url` = `tracks`.`url`
    ) as `valueTable`
    LEFT JOIN `lyrics` ON `lyrics`.`url` = CONCAT('.' , `valueTable`.`filePath`)
""" + getSQLConditionByFilter(_filter) + """
) as `artistTable`
""")
        r = db.store_result()
        musicFileValues = []
        rows = r.fetch_row(0)
        for row in rows:
            musicFileValues.append({})
            musicFileValues[-1]["id"] = row[0]
            musicFileValues[-1]["name"] = row[1]
        return musicFileValues
        
    def getArtistName(_artistId):
        db = Amarok.checkAndGetDB()
        db.query("SELECT `name` FROM `artists` WHERE `id`=%s" % _artistId)
        r = db.store_result()
        musicFileValues = []
        rows = r.fetch_row(0)
        if len(rows)>0:
            return rows[0][0]
        return None

    def getDevices():
        db = Amarok.checkAndGetDB()
        db.query("SELECT id,lastmountpoint FROM devices")
        r = db.store_result()
        return r.fetch_row(0)
        
    def getArtistId(_artist):
        db = Amarok.checkAndGetDB()
        db.query("SELECT `id` FROM `artists` WHERE `name`='%s'" % (Databases.correctForSql(_artist)))
        r = db.store_result()
        rows = r.fetch_row(0)
        if len(rows)>0:
            return rows[0][0]
        return None
        
    def getOrInsertArtist(_artist):
        db = Amarok.checkAndGetDB()
        for sqlCommand in Databases.getAmendedSQLSelectOrInsertAndSelectQueries("artists", "id", {"name" : "'" + Databases.correctForSql(_artist) + "'"}):
            db.query(sqlCommand)
        r = db.store_result()
        return r.fetch_row(0)[0][0]
        
    def getOrInsertAlbum(_album, _artistId):
        db = Amarok.checkAndGetDB()
        for sqlCommand in Databases.getAmendedSQLSelectOrInsertAndSelectQueries("albums", "id", {"name" : "'" + Databases.correctForSql(_album) + "'", "artist" : "'" + _artistId + "'"}):
            db.query(sqlCommand)
        r = db.store_result()
        return r.fetch_row(0)[0][0]
        
    def getOrInsertYear(_year):
        db = Amarok.checkAndGetDB()
        for sqlCommand in Databases.getAmendedSQLSelectOrInsertAndSelectQueries("years", "id", {"name" : "'" + Databases.correctForSql(_year) + "'"}):
            db.query(sqlCommand)
        r = db.store_result()
        return r.fetch_row(0)[0][0]
        
    def getOrInsertGenre(_genre):
        db = Amarok.checkAndGetDB()
        for sqlCommand in Databases.getAmendedSQLSelectOrInsertAndSelectQueries("genres", "id", {"name" : "'" + Databases.correctForSql(_genre) + "'"}):
            db.query(sqlCommand)
        r = db.store_result()
        return r.fetch_row(0)[0][0]
    
    def changeFilePath(_oldPath, _newPath):
        _oldPath, _newPath = Databases.correctForSql(str(_oldPath)), Databases.correctForSql(str(_newPath))
        _oldPathUrl, _newPathUrl = quote(_oldPath), quote(_newPath)
        withOutDevicePointValues, withOutDeviceValues = [], []
        for devicePoint in getDevices():
            if devicePoint[1] + "/" == _oldPath[:len(devicePoint[1])+1]:
                if devicePoint[1] + "/" == _newPath[:len(devicePoint[1])+1]:
                    withOutDevicePointValues.append({"id":devicePoint[0], 
                                                "oldPath":  _oldPath[len(devicePoint[1]):], 
                                                "newPath": _newPath[len(devicePoint[1]):]
                                                })
                else:
                    withOutDeviceValues.append({"id": devicePoint[0], 
                                        "oldPath":  _oldPath[len(devicePoint[1]):], 
                                        "newPath": _newPath
                                                })
        db = Amarok.checkAndGetDB()
        db.query("UPDATE urls SET rpath='.%s' WHERE rpath='.%s'" % (_newPath, _oldPath))
        for withOutDevice in withOutDeviceValues:
            db.query("UPDATE urls SET rpath='.%s', deviceid = -1 WHERE deviceid = %s and rpath = '.%s' " % (Databases.correctForSql(withOutDevice["newPath"]), withOutDevice["id"], Databases.correctForSql(withOutDevice["oldPath"])))
        for withOutDevicePoint in withOutDevicePointValues:
            db.query("UPDATE urls SET rpath='.%s' WHERE deviceid = %s and rpath = '.%s'" % (Databases.correctForSql(withOutDevicePoint["newPath"]), withOutDevicePoint["id"], Databases.correctForSql(withOutDevicePoint["oldPath"])))
        db.query("UPDATE images SET path='%s' WHERE path='%s'" % (_newPath, _oldPath))
        db.query("UPDATE lyrics SET url='.%s' WHERE url='.%s'" % (_newPath, _oldPath))
        db.query("UPDATE statistics_permanent SET url='file://%s' WHERE url='file://%s'" % (Databases.correctForSql(_newPathUrl), Databases.correctForSql(_oldPathUrl)))
        db.commit()
        return True
        
    def changeDirectoryPath(_oldPath, _newPath):
        _oldPath, _newPath = Databases.correctForSql(str(_oldPath)), Databases.correctForSql(str(_newPath))
        _oldPathUrl, _newPathUrl = quote(_oldPath), quote(_newPath)
        withOutDevicePointValues, withOutDeviceValues = [], []
        for devicePoint in getDevices():
            if devicePoint[1] + "/" == _oldPath[:len(devicePoint[1])+1]:
                if devicePoint[1] + "/" == _newPath[:len(devicePoint[1])+1]:
                    withOutDevicePointValues.append({"id":devicePoint[0], 
                                                "oldPath":  _oldPath[len(devicePoint[1]):], 
                                                "newPath": _newPath[len(devicePoint[1]):]
                                                })
                else:
                    withOutDeviceValues.append({"id": devicePoint[0], 
                                        "oldPath":  _oldPath[len(devicePoint[1]):], 
                                        "newPath": _newPath
                                                })
        db = Amarok.checkAndGetDB()
        db.query("UPDATE directories SET dir=REPLACE(dir, '.%s/', '.%s/')" % (_oldPath, _newPath))
        db.query("UPDATE urls SET rpath=REPLACE(rpath, '.%s/', '.%s/')" % (_oldPath, _newPath))
        for withOutDevice in withOutDeviceValues:
            db.query("UPDATE directories SET dir=REPLACE(dir, '.%s/', '.%s/'), deviceid = -1 WHERE deviceid = %s " % (Databases.correctForSql(withOutDevice["oldPath"]), Databases.correctForSql(withOutDevice["newPath"]), withOutDevice["id"]))
            db.query("UPDATE urls SET rpath=REPLACE(rpath, '.%s/', '.%s/'), deviceid = -1 WHERE deviceid = %s " % (Databases.correctForSql(withOutDevice["oldPath"]), Databases.correctForSql(withOutDevice["newPath"]), withOutDevice["id"]))
        for withOutDevicePoint in withOutDevicePointValues:
            db.query("UPDATE directories SET dir=REPLACE(dir, '.%s/', '.%s/') WHERE deviceid = %s " % (Databases.correctForSql(withOutDevicePoint["oldPath"]), Databases.correctForSql(withOutDevicePoint["newPath"]), withOutDevicePoint["id"]))
            db.query("UPDATE urls SET rpath=REPLACE(rpath, '.%s/', '.%s/') WHERE deviceid = %s " % (Databases.correctForSql(withOutDevicePoint["oldPath"]), Databases.correctForSql(withOutDevicePoint["newPath"]), withOutDevicePoint["id"]))
        db.query("UPDATE images SET path=REPLACE(path, '%s/', '%s/')" % (_oldPath, _newPath))
        db.query("UPDATE lyrics SET url=REPLACE(url, '.%s/', '.%s/')" % (_oldPath, _newPath))
        db.query("UPDATE statistics_permanent SET url=REPLACE(url, '%s/', '%s/')" % (Databases.correctForSql(_oldPathUrl), Databases.correctForSql(_newPathUrl)))
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
                db.query("UPDATE `lyrics` SET `lyrics`='%s' WHERE `url`='.%s'" % (Databases.correctForSql(_values["firstLyrics"]), Databases.correctForSql(path)))
            db.query("UPDATE `tracks` SET `artist`=%s, `title`='%s', `album`=%s, `tracknumber`=%s, `year`=%s, `genre`=%s, `comment`='%s' WHERE `id`=%s" % (artistId, Databases.correctForSql(title), albumId, trackNum, yearId, genreId, Databases.correctForSql(firstComment), trackId))
            db.commit()
        return True
        
    def changeArtistValue(_values):
        if len(_values)>1:
            db = Amarok.checkAndGetDB()
            try:
                db.query("UPDATE `artists` SET `name`='%s' WHERE `id`=%s" % (Databases.correctForSql(_values["name"]), _values["id"]))
                db.commit()
                return [getAllMusicFilePathsByArtistId(_values["id"]), _values["name"]]
            except Amarok.getMySQLModule().IntegrityError as error:
                returnValues = [getAllMusicFilePathsByArtistId(_values["id"]), _values["name"]]
                changeArtistWithAnother(_values["id"], getArtistId(_values["name"]))
                deleteArtist(_values["id"])
                return returnValues
        return None
        
    def changeArtistWithAnother(_currentArtistId, _artistWillBeSelectedId):
        db = Amarok.checkAndGetDB()
        db.query("UPDATE `tracks` SET `artist`=%s WHERE `artist`=%s" % (_artistWillBeSelectedId, _currentArtistId))
        db.query("UPDATE `albums` SET `artist`=%s WHERE `artist`=%s" % (_artistWillBeSelectedId, _currentArtistId))
        db.commit()
        return True
        
    def deleteArtist(_artistId):
        db = Amarok.checkAndGetDB()
        db.query("DELETE FROM `artists` WHERE `id`=%s" % (_artistId))
        db.commit()
        return True
        
        
            

