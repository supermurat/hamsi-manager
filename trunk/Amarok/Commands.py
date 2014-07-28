## This file is part of HamsiManager.
##
## Copyright (c) 2010 - 2014 Murat Demir <mopened@gmail.com>
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
from Core import Universals as uni
import FileUtils as fu


def getSQLConditionPartByPartOfFilter(_partOfFilterString=""):
    _partOfFilterString = _partOfFilterString.strip()
    while _partOfFilterString.find(" :") != -1:
        _partOfFilterString = _partOfFilterString.replace(" :", ":")
    while _partOfFilterString.find(": ") != -1:
        _partOfFilterString = _partOfFilterString.replace(": ", ":")
    while _partOfFilterString.find(" <") != -1:
        _partOfFilterString = _partOfFilterString.replace(" <", "<")
    while _partOfFilterString.find("< ") != -1:
        _partOfFilterString = _partOfFilterString.replace("< ", "<")
    while _partOfFilterString.find(" >") != -1:
        _partOfFilterString = _partOfFilterString.replace(" >", ">")
    while _partOfFilterString.find("> ") != -1:
        _partOfFilterString = _partOfFilterString.replace("> ", ">")
    _partOfFilterString = _partOfFilterString.replace("\"", "")
    _partOfFilterString = Databases.correctForSql(_partOfFilterString)
    if _partOfFilterString.find("filename:") != -1:
        filterPart = _partOfFilterString.replace("filename:", "")
        return (" ( LOWER( \n"
                "REPLACE( \n"
                "CONCAT(CASE WHEN devices.lastmountpoint IS NOT NULL THEN devices.lastmountpoint ELSE '' END, \n"
                "SUBSTRING( urls.rpath , 2 )), \n"
                "CONCAT('/', \n"
                "CONCAT(CASE WHEN devices.lastmountpoint IS NOT NULL THEN devices.lastmountpoint ELSE '' END, \n"
                "SUBSTRING( urls.rpath , 2 ))), '')) LIKE LOWER('%s') ) ") % ("%" + filterPart + "%")
    elif _partOfFilterString.find("title:") != -1:
        filterPart = _partOfFilterString.replace("title:", "")
        return " ( LOWER(tracks.title) LIKE LOWER('%s') ) " % ("%" + filterPart + "%")
    elif _partOfFilterString.find("albumartist:") != -1:
        filterPart = _partOfFilterString.replace("albumartist:", "")
        return " ( LOWER(albumartists.name) LIKE LOWER('%s') ) " % ("%" + filterPart + "%")
    elif _partOfFilterString.find("artist:") != -1:
        filterPart = _partOfFilterString.replace("artist:", "")
        return " ( LOWER(artists.name) LIKE LOWER('%s') ) " % ("%" + filterPart + "%")
    elif _partOfFilterString.find("album:") != -1:
        filterPart = _partOfFilterString.replace("album:", "")
        return " ( LOWER(albums.name) LIKE LOWER('%s') ) " % ("%" + filterPart + "%")
    elif _partOfFilterString.find("genre:") != -1:
        filterPart = _partOfFilterString.replace("genre:", "")
        return " ( LOWER(genres.name) LIKE LOWER('%s') ) " % ("%" + filterPart + "%")
    elif _partOfFilterString.find("comment:") != -1:
        filterPart = _partOfFilterString.replace("comment:", "")
        return " ( LOWER(tracks.comment) LIKE LOWER('%s') ) " % ("%" + filterPart + "%")
    elif _partOfFilterString.find("rating:<") != -1:
        filterPart = _partOfFilterString.replace("rating:<", "").replace(".", ",")
        try: filterPart = int(float(filterPart) * 2)
        except: filterPart = 0
        return " ( statistics.rating < %s ) " % (filterPart)
    elif _partOfFilterString.find("rating:>") != -1:
        filterPart = _partOfFilterString.replace("rating:>", "").replace(".", ",")
        try: filterPart = int(float(filterPart) * 2)
        except: filterPart = 0
        return " ( statistics.rating > %s ) " % (filterPart)
    elif _partOfFilterString.find("rating:") != -1:
        filterPart = _partOfFilterString.replace("rating:", "").replace(".", ",")
        try: filterPart = int(float(filterPart) * 2)
        except: filterPart = 0
        return " ( statistics.rating = %s ) " % (filterPart)
    elif _partOfFilterString.find("year:<") != -1:
        filterPart = _partOfFilterString.replace("year:<", "").replace(".", ",")
        try: filterPart = int(filterPart)
        except: filterPart = 0
        return " ( CAST( years.name AS INT ) < %s ) " % (filterPart)
    elif _partOfFilterString.find("year:>") != -1:
        filterPart = _partOfFilterString.replace("year:>", "").replace(".", ",")
        try: filterPart = int(filterPart)
        except: filterPart = 0
        return " ( CAST( years.name AS INT ) > %s ) " % (filterPart)
    elif _partOfFilterString.find("year:") != -1:
        filterPart = _partOfFilterString.replace("year:", "").replace(".", ",")
        try: filterPart = int(filterPart)
        except: filterPart = 0
        return " ( CAST( years.name AS INT )  = %s ) " % (filterPart)
    else:
        filterPart = _partOfFilterString
        return (" ( LOWER( \n"
                "REPLACE( \n"
                "CONCAT(CASE WHEN devices.lastmountpoint IS NOT NULL THEN devices.lastmountpoint ELSE '' END, \n"
                "SUBSTRING( urls.rpath , 2 )), \n"
                "CONCAT('/', \n"
                "CONCAT(CASE WHEN devices.lastmountpoint IS NOT NULL THEN devices.lastmountpoint ELSE '' END, \n"
                "SUBSTRING( urls.rpath , 2 ))), '')) LIKE LOWER('%s') \n"
                "OR LOWER(tracks.title) LIKE LOWER('%s') \n"
                "OR LOWER(artists.name) LIKE LOWER('%s') \n"
                "OR LOWER(albums.name) LIKE LOWER('%s') \n"
                "OR LOWER(albumartists.name) LIKE LOWER('%s') \n"
                "OR LOWER(genres.name) LIKE LOWER('%s') \n"
                "OR LOWER(tracks.comment) LIKE LOWER('%s') \n"
                "OR LOWER(years.name) LIKE LOWER('%s') ) \n" % (
                "%" + filterPart + "%", "%" + filterPart + "%", "%" + filterPart + "%", "%" + filterPart + "%",
                "%" + filterPart + "%", "%" + filterPart + "%", "%" + filterPart + "%", "%" + filterPart + "%"))


def getSQLConditionValues(sqlCondition, _filter, _listOfFilters):
    for f in _listOfFilters:
        _filter.replace(f, "__filter__")
        appendingConditionControl = re.findall(r"((OR|AND)? *__filter__)", _filter)  # [('OR __filter__', 'OR')]
        if len(appendingConditionControl) > 0:
            appendingCondition = " " + appendingConditionControl[0][1] + " "
            deleteThisFromFilter = appendingConditionControl[0][0]
        else:
            appendingCondition = " AND "
            deleteThisFromFilter = f
        sqlCondition += appendingCondition + getSQLConditionPartByPartOfFilter(f)
        _filter = _filter.replace(deleteThisFromFilter, " ")
    return sqlCondition, _filter.strip()


def getSQLConditionByFilter(_filter="", _isAppendWhere=True):
    _filter = str(_filter).strip().replace("\t", " ").replace("\n", " ")
    while _filter.find("  ") != -1:
        _filter = _filter.replace("  ", " ")
    if _filter == "":
        return ""
    if _filter.count("\"") % 2 != 0:
        return ""  # Incorrect filter string
    if _isAppendWhere: sqlCondition = " WHERE "
    else: sqlCondition = ""
    _filter = uni.trUnicode(_filter)
    listOfSpecialAndQuoted1 = re.findall(r"([a-zA-Z]* ?: ?\'[\w\-\./\s ]*\')", _filter, re.I | re.U)  # ['artist:'like this'']
    sqlCondition, _filter = getSQLConditionValues(sqlCondition, _filter, listOfSpecialAndQuoted1)
    listOfSpecialAndQuoted2 = re.findall(r"([a-zA-Z]* ?: ?\"[\w\-\./\s ]*\")", _filter, re.I | re.U)  # ['artist:"like this"']
    sqlCondition, _filter = getSQLConditionValues(sqlCondition, _filter, listOfSpecialAndQuoted2)
    listOfSpecial1 = re.findall(r"([a-zA-Z]* ?: ?< ?[\w+\-\./]+)", _filter, re.I | re.U)  #['rating:<likeThis']
    sqlCondition, _filter = getSQLConditionValues(sqlCondition, _filter, listOfSpecial1)
    listOfSpecial2 = re.findall(r"([a-zA-Z]* ?: ?> ?[\w+\-\./]+)", _filter, re.I | re.U)  #['rating:>likeThis']
    sqlCondition, _filter = getSQLConditionValues(sqlCondition, _filter, listOfSpecial2)
    listOfSpecial = re.findall(r"([a-zA-Z]* ?: ?[\w+\-\./]+)", _filter, re.I | re.U)  #['artist:likeThis']
    sqlCondition, _filter = getSQLConditionValues(sqlCondition, _filter, listOfSpecial)
    listOfQuoted = re.findall(r"(\"[ \w+\-\./]*\")", _filter, re.I | re.U)  #['"like this"']
    sqlCondition, _filter = getSQLConditionValues(sqlCondition, _filter, listOfQuoted)
    listOfFilters = _filter.split(" ")
    if listOfFilters != [""]:
        sqlCondition, _filter = getSQLConditionValues(sqlCondition, _filter, listOfFilters)
    sqlControl = re.findall(r"(WHERE *(OR|AND)?)", sqlCondition)
    if len(sqlControl) > 0:
        sqlCondition = sqlCondition.replace(sqlControl[0][0], "WHERE ")
    if _isAppendWhere and len(sqlCondition.strip())<7:
        sqlCondition = " "
    return sqlCondition


def getDirectoriesAndValues(_filter=""):
    db = Amarok.checkAndGetDB()
    query = """
SELECT DISTINCT
REPLACE(
    CONCAT(CASE WHEN devices.lastmountpoint IS NOT NULL THEN devices.lastmountpoint ELSE '' END,
        SUBSTRING(urls.rpath , 2)),
    CONCAT('/',
        SUBSTRING_INDEX(
            CONCAT(CASE WHEN devices.lastmountpoint IS NOT NULL THEN devices.lastmountpoint ELSE '' END,
                SUBSTRING(urls.rpath , 2)),
            '/' , -1))
, '') AS 'dirPath',
images.path AS 'imagePath',
artists.name AS 'artistName',
albums.name AS 'albumName',
years.name AS 'yearName',
genres.name AS 'genreName'
FROM tracks
LEFT JOIN urls ON urls.id = tracks.url
LEFT JOIN devices ON devices.id = urls.deviceid
LEFT JOIN artists ON artists.id = tracks.artist
LEFT JOIN albums ON albums.id = tracks.album
LEFT JOIN years ON years.id = tracks.year
LEFT JOIN genres ON genres.id = tracks.genre
LEFT JOIN images ON images.id = albums.image
LEFT JOIN artists albumartists ON albumartists.id = albums.artist
LEFT JOIN statistics ON statistics.url = tracks.url
WHERE images.path IS NOT NULL AND images.path NOT LIKE 'amarok-sqltrackuid:%'
"""
    query += getSQLConditionByFilter(_filter, False) + " ORDER BY dirPath "
    uni.printForDevelopers("Query - getDirectoriesAndValues : " + query)
    db.query(query)
    r = db.store_result()
    directoriesValues = {}
    rows = r.fetch_row(0)
    for row in rows:
        if row[0] not in directoriesValues:
            directoriesValues[row[0]] = {"coverPath": [], "artist": [], "album": [], "year": [], "genre": []}
        directoriesValues[row[0]]["coverPath"].append(row[1])
        directoriesValues[row[0]]["artist"].append(row[2])
        directoriesValues[row[0]]["album"].append(row[3])
        directoriesValues[row[0]]["year"].append(row[4])
        directoriesValues[row[0]]["genre"].append(row[5])
    return directoriesValues


def getAllMusicFileValuesWithNames(_filter="", _artistId=None):
    db = Amarok.checkAndGetDB()
    query = """
SELECT tracks.id,
    REPLACE(
        CONCAT(CASE WHEN devices.lastmountpoint IS NOT NULL THEN devices.lastmountpoint ELSE '' END,
            SUBSTRING( urls.rpath , 2 )),
        CONCAT('/',
                CONCAT(CASE WHEN devices.lastmountpoint IS NOT NULL THEN devices.lastmountpoint ELSE '' END,
                    SUBSTRING( urls.rpath , 2 )))
    , '') AS 'filePath',
tracks.title,
tracks.artist AS 'artistId',
tracks.album AS 'albumId',
albums.artist AS 'albumArtistId',
tracks.year AS 'yearId',
tracks.genre AS 'genreId',
tracks.tracknumber AS 'trackNumber',
tracks.comment AS 'comment',
artists.name AS 'artist',
albums.name AS 'album',
albumartists.name AS 'albumArtist',
years.name AS 'year',
genres.name AS 'genre',
images.path AS 'imagePath',
statistics.rating,
lyrics.lyrics
FROM tracks
INNER JOIN urls ON urls.id = tracks.url
LEFT JOIN devices ON devices.id = urls.deviceid
LEFT JOIN artists ON artists.id = tracks.artist
LEFT JOIN albums ON albums.id = tracks.album
LEFT JOIN artists albumartists ON albumartists.id = albums.artist
LEFT JOIN years ON years.id = tracks.year
LEFT JOIN genres ON genres.id = tracks.genre
LEFT JOIN images ON images.id = albums.image
LEFT JOIN statistics ON statistics.url = tracks.url
LEFT JOIN lyrics ON lyrics.url = urls.id
"""
    isAddWhere = True
    if _artistId:
        query += " WHERE (tracks.artist=" + str(_artistId) + " OR albums.artist=" + str(_artistId) + ") "
        isAddWhere = False
    query += getSQLConditionByFilter(_filter, isAddWhere) + " ORDER BY filePath "
    uni.printForDevelopers("Query - getAllMusicFileValuesWithNames : " + query)
    c = db.cursor(Amarok.getCursors().DictCursor)
    c.execute(query)
    musicFileValues = []
    for rows in c.fetchall():
        musicFileValues.append({})
        for key in rows.keys():
            musicFileValues[-1][key] = Databases.correctForUser(rows[key])
    return musicFileValues


def getAllMusicFilePathsByArtistId(_artistId):
    db = Amarok.checkAndGetDB()
    query = """
SELECT
    REPLACE(
        CONCAT(
            CASE WHEN devices.lastmountpoint IS NOT NULL THEN devices.lastmountpoint ELSE '' END,
            SUBSTRING( urls.rpath , 2 )),
        CONCAT('/',
                CONCAT( CASE WHEN devices.lastmountpoint IS NOT NULL THEN devices.lastmountpoint ELSE '' END,
                    SUBSTRING( urls.rpath , 2 )))
    , '') AS 'filePath'
FROM tracks
INNER JOIN urls ON urls.id = tracks.url
LEFT JOIN devices ON devices.id = urls.deviceid
WHERE tracks.artist=""" + str(_artistId) + " ORDER BY filePath "
    uni.printForDevelopers("Query - getAllMusicFilePathsByArtistId : " + query)
    db.query(query)
    r = db.store_result()
    musicFileValues = []
    rows = r.fetch_row(0)
    for row in rows:
        musicFileValues.append(row[0])
    return musicFileValues


def getAllMusicFilePathsByAlbumArtistId(_artistId):
    db = Amarok.checkAndGetDB()
    query = """
SELECT
    REPLACE(
        CONCAT(
            CASE WHEN devices.lastmountpoint IS NOT NULL THEN devices.lastmountpoint ELSE '' END,
            SUBSTRING( urls.rpath , 2 )),
        CONCAT('/',
                CONCAT( CASE WHEN devices.lastmountpoint IS NOT NULL THEN devices.lastmountpoint ELSE '' END,
                    SUBSTRING( urls.rpath , 2 )))
    , '') AS 'filePath'
FROM tracks
INNER JOIN urls ON urls.id = tracks.url
LEFT JOIN devices ON devices.id = urls.deviceid
LEFT JOIN albums ON albums.id = tracks.album
LEFT JOIN artists albumartists ON albumartists.id = albums.artist
WHERE albums.artist=""" + str(_artistId) + " ORDER BY filePath "
    uni.printForDevelopers("Query - getAllMusicFilePathsByArtistId : " + query)
    db.query(query)
    r = db.store_result()
    musicFileValues = []
    rows = r.fetch_row(0)
    for row in rows:
        musicFileValues.append(row[0])
    return musicFileValues


def getAllArtistsValues(_filter=""):
    db = Amarok.checkAndGetDB()
    _filter = str(_filter).strip()
    query = """
SELECT DISTINCT
artists.id,
artists.name
FROM tracks
INNER JOIN urls ON urls.id = tracks.url
LEFT JOIN devices ON devices.id = urls.deviceid
LEFT JOIN artists ON artists.id = tracks.artist
LEFT JOIN albums ON albums.id = tracks.album
LEFT JOIN artists albumartists ON albumartists.id = albums.artist
LEFT JOIN years ON years.id = tracks.year
LEFT JOIN genres ON genres.id = tracks.genre
LEFT JOIN images ON images.id = albums.image
LEFT JOIN statistics ON statistics.url = tracks.url
LEFT JOIN lyrics ON lyrics.url = urls.id
"""
    query += getSQLConditionByFilter(_filter, True) + " ORDER BY artists.name "
    uni.printForDevelopers("Query - getAllArtistsValues : " + query)
    db.query(query)
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
    query = "SELECT name FROM artists WHERE id=%s" % _artistId
    uni.printForDevelopers("Query - getArtistName : " + query)
    db.query(query)
    r = db.store_result()
    musicFileValues = []
    rows = r.fetch_row(0)
    if len(rows) > 0:
        return str(rows[0][0])
    return None


def getDevices():
    db = Amarok.checkAndGetDB()
    query = "SELECT id,lastmountpoint FROM devices"
    uni.printForDevelopers("Query - getDevices : " + query)
    db.query(query)
    r = db.store_result()
    return r.fetch_row(0)


def getArtistId(_artist):
    db = Amarok.checkAndGetDB()
    query = "SELECT id FROM artists WHERE name='%s'" % (Databases.correctForSql(_artist))
    uni.printForDevelopers("Query - getArtistId : " + query)
    db.query(query)
    r = db.store_result()
    rows = r.fetch_row(0)
    if len(rows) > 0:
        return str(rows[0][0])
    return None


def getOrInsertArtist(_artist):
    db = Amarok.checkAndGetDB()
    for sqlCommand in Databases.getAmendedSQLSelectOrInsertAndSelectQueries("artists", "id", {
        "name": "'" + Databases.correctForSql(_artist) + "'"}):
        uni.printForDevelopers("Query - getOrInsertArtist : " + sqlCommand)
        db.query(sqlCommand)
    r = db.store_result()
    return str(r.fetch_row(0)[0][0])


def getOrInsertAlbum(_album, _artistId):
    db = Amarok.checkAndGetDB()
    for sqlCommand in Databases.getAmendedSQLSelectOrInsertAndSelectQueries("albums", "id", {
        "name": "'" + Databases.correctForSql(_album) + "'", "artist": "'" + _artistId + "'"}):
        uni.printForDevelopers("Query - getOrInsertAlbum : " + sqlCommand)
        db.query(sqlCommand)
    r = db.store_result()
    return str(r.fetch_row(0)[0][0])


def getOrInsertYear(_year):
    db = Amarok.checkAndGetDB()
    for sqlCommand in Databases.getAmendedSQLSelectOrInsertAndSelectQueries("years", "id", {
        "name": "'" + Databases.correctForSql(_year) + "'"}):
        uni.printForDevelopers("Query - getOrInsertYear : " + sqlCommand)
        db.query(sqlCommand)
    r = db.store_result()
    return str(r.fetch_row(0)[0][0])


def getOrInsertGenre(_genre):
    db = Amarok.checkAndGetDB()
    for sqlCommand in Databases.getAmendedSQLSelectOrInsertAndSelectQueries("genres", "id", {
        "name": "'" + Databases.correctForSql(_genre) + "'"}):
        uni.printForDevelopers("Query - getOrInsertGenre : " + sqlCommand)
        db.query(sqlCommand)
    r = db.store_result()
    return str(r.fetch_row(0)[0][0])


def getOrInsertDirectory(_directory, _deviceId):
    _deviceId = str(_deviceId)
    if _directory[-1] != "/": _directory = _directory + "/"
    if _directory[0] != ".": _directory = "." + _directory
    db = Amarok.checkAndGetDB()
    sqlSelectCommand = "SELECT id FROM directories WHERE deviceid=" + _deviceId + " AND dir='" + Databases.correctForSql(
        _directory) + "'"
    uni.printForDevelopers("Query - getOrInsertDirectory - sqlSelectCommand - 1 : " + sqlSelectCommand)
    db.query(sqlSelectCommand)
    r = db.store_result()
    rows = r.fetch_row(0)
    if len(rows) == 0:
        sqlInsertCommand = "INSERT INTO directories(deviceid,dir) VALUES (" + _deviceId + ",'" + Databases.correctForSql(
            _directory) + "')"
        uni.printForDevelopers("Query - getOrInsertDirectory - sqlInsertCommand : " + sqlInsertCommand)
        db.query(sqlInsertCommand)
        uni.printForDevelopers("Query - getOrInsertDirectory - sqlSelectCommand - 2 : " + sqlSelectCommand)
        db.query(sqlSelectCommand)
        r = db.store_result()
        rows = r.fetch_row(0)
    return rows[0][0]


def changeFilePath(_oldPath, _newPath):
    _oldPath, _newPath = str(_oldPath), str(_newPath)
    withOutDevicePointValues, withOutDeviceValues = [], []
    for devicePoint in getDevices():
        if devicePoint[1] + "/" == _oldPath[:len(devicePoint[1]) + 1]:
            if devicePoint[1] + "/" == _newPath[:len(devicePoint[1]) + 1]:
                withOutDevicePointValues.append({"id": devicePoint[0],
                                                 "oldPath": Databases.correctForSql(_oldPath[len(devicePoint[1]):]),
                                                 "newPath": Databases.correctForSql(_newPath[len(devicePoint[1]):])
                })
            else:
                withOutDeviceValues.append({"id": devicePoint[0],
                                            "oldPath": Databases.correctForSql(_oldPath[len(devicePoint[1]):]),
                                            "newPath": Databases.correctForSql(_newPath)
                })
    _oldPath, _newPath = Databases.correctForSql(_oldPath), Databases.correctForSql(_newPath)
    _oldPathUrl, _newPathUrl = Databases.correctForSql(quote(_oldPath)), Databases.correctForSql(quote(_newPath))
    db = Amarok.checkAndGetDB()
    db.query("UPDATE urls SET rpath='.%s' WHERE rpath='.%s'" % (_newPath, _oldPath))
    for withOutDevice in withOutDeviceValues:
        directoryID = getOrInsertDirectory(fu.getDirName(withOutDevice["newPath"]), "-1")
        db.query("UPDATE urls SET rpath='.%s', directory=%s, deviceid = -1 WHERE deviceid = %s and rpath = '.%s' " % (
            withOutDevice["newPath"], directoryID, withOutDevice["id"], withOutDevice["oldPath"]))
    for withOutDevicePoint in withOutDevicePointValues:
        directoryID = getOrInsertDirectory(fu.getDirName(withOutDevicePoint["newPath"]), withOutDevicePoint["id"])
        db.query("UPDATE urls SET rpath='.%s', directory=%s WHERE deviceid = %s and rpath = '.%s'" % (
            withOutDevicePoint["newPath"], directoryID, withOutDevicePoint["id"], withOutDevicePoint["oldPath"]))
    db.query("UPDATE images SET path='%s' WHERE path='%s'" % (_newPath, _oldPath))
    db.query("UPDATE lyrics SET url='.%s' WHERE url='.%s'" % (_newPath, _oldPath))
    db.query("UPDATE statistics_permanent SET url='file://%s' WHERE url='file://%s'" % (_newPathUrl, _oldPathUrl))
    db.commit()
    return True


def changeDirectoryPath(_oldPath, _newPath):
    _oldPath, _newPath = str(_oldPath), str(_newPath)
    withOutDevicePointValues, withOutDeviceValues = [], []
    for devicePoint in getDevices():
        if devicePoint[1] + "/" == _oldPath[:len(devicePoint[1]) + 1]:
            if devicePoint[1] + "/" == _newPath[:len(devicePoint[1]) + 1]:
                withOutDevicePointValues.append({"id": devicePoint[0],
                                                 "oldPath": Databases.correctForSql(_oldPath[len(devicePoint[1]):]),
                                                 "newPath": Databases.correctForSql(_newPath[len(devicePoint[1]):])
                })
            else:
                withOutDeviceValues.append({"id": devicePoint[0],
                                            "oldPath": Databases.correctForSql(_oldPath[len(devicePoint[1]):]),
                                            "newPath": Databases.correctForSql(_newPath)
                })
    _oldPath, _newPath = Databases.correctForSql(_oldPath), Databases.correctForSql(_newPath)
    _oldPathUrl, _newPathUrl = Databases.correctForSql(quote(_oldPath)), Databases.correctForSql(quote(_newPath))
    db = Amarok.checkAndGetDB()
    db.query("UPDATE directories SET dir=REPLACE(dir, '.%s/', '.%s/')" % (_oldPath, _newPath))
    db.query("UPDATE urls SET rpath=REPLACE(rpath, '.%s/', '.%s/')" % (_oldPath, _newPath))
    for withOutDevice in withOutDeviceValues:
        db.query("UPDATE directories SET dir=REPLACE(dir, '.%s/', '.%s/'), deviceid = -1 WHERE deviceid = %s " % (
            withOutDevice["oldPath"], withOutDevice["newPath"], withOutDevice["id"]))
        db.query("UPDATE urls SET rpath=REPLACE(rpath, '.%s/', '.%s/'), deviceid = -1 WHERE deviceid = %s " % (
            withOutDevice["oldPath"], withOutDevice["newPath"], withOutDevice["id"]))
    for withOutDevicePoint in withOutDevicePointValues:
        db.query("UPDATE directories SET dir=REPLACE(dir, '.%s/', '.%s/') WHERE deviceid = %s " % (
            withOutDevicePoint["oldPath"], withOutDevicePoint["newPath"], withOutDevicePoint["id"]))
        db.query("UPDATE urls SET rpath=REPLACE(rpath, '.%s/', '.%s/') WHERE deviceid = %s " % (
            withOutDevicePoint["oldPath"], withOutDevicePoint["newPath"], withOutDevicePoint["id"]))
    db.query("UPDATE images SET path=REPLACE(path, '%s/', '%s/')" % (_oldPath, _newPath))
    db.query("UPDATE statistics_permanent SET url=REPLACE(url, '%s/', '%s/')" % (_oldPathUrl, _newPathUrl))
    db.commit()
    return True


def changeTag(_values):
    if len(_values) > 1:
        path = _values["path"]
        db = Amarok.checkAndGetDB()
        querySelect = """
        SELECT trackId,albumArtistId,urlId FROM (
            SELECT tracks.id AS 'trackId',
                REPLACE(
                    CONCAT(CASE WHEN devices.lastmountpoint IS NOT NULL THEN devices.lastmountpoint ELSE '' END,
                        SUBSTRING( urls.rpath , 2 )),
                    CONCAT('/',
                            CONCAT(CASE WHEN devices.lastmountpoint IS NOT NULL THEN devices.lastmountpoint ELSE '' END,
                                SUBSTRING( urls.rpath , 2 )))
                , '') AS 'filePath',
            albums.artist AS 'albumArtistId',
            urls.id AS 'urlId'
            FROM tracks
            INNER JOIN urls ON urls.id = tracks.url
            LEFT JOIN devices ON devices.id = urls.deviceid
            LEFT JOIN albums ON albums.id = tracks.album
            LEFT JOIN artists albumartists ON albumartists.id = albums.artist
        ) as valueTable WHERE filePath = '%s'
        """ % Databases.correctForSql(path)
        uni.printForDevelopers("Query - changeTag - querySelect : " + querySelect)
        db.query(querySelect)
        r = db.store_result()
        rows = r.fetch_row(0)
        if len(rows) == 0:
            return None
        trackId = str(rows[0][0])
        albumArtistId = str(rows[0][1])
        urlId = str(rows[0][2])
        db = Amarok.checkAndGetDB()
        query = " "
        if "artist" in _values:
            query += ", artist=" + getOrInsertArtist(_values["artist"])
        if "albumArtist" in _values:
            albumArtistId = getOrInsertArtist(_values["albumArtist"])
            query += ", artist=" + albumArtistId
        if "title" in _values:
            query += ", title='" + Databases.correctForSql(_values["title"]) + "' "
        if "album" in _values:
            query += ", album=" + getOrInsertAlbum(_values["album"], albumArtistId)
        if "trackNum" in _values:
            query += ", tracknumber=" + Databases.correctForSql(_values["trackNum"], "int")
        if "year" in _values:
            query += ", year=" + getOrInsertYear(_values["year"])
        if "genre" in _values:
            query += ", genre=" + getOrInsertGenre(_values["genre"])
        if "firstComment" in _values:
            query += ", comment='" + Databases.correctForSql(_values["firstComment"]) + "' "
        if "firstLyrics" in _values:
            lyricQuery = ("INSERT INTO lyrics(url,lyrics) VALUES (" + urlId + ",'" + Databases.correctForSql(
                 _values["firstLyrics"]) + "') ON DUPLICATE KEY UPDATE lyrics=VALUES(lyrics) ")
            uni.printForDevelopers("Query - changeTag - lyricQuery : " + lyricQuery)
            db.query(lyricQuery)
        if query.strip() != "":
            query = query[2:] # for first ","
            queryUpdate = "UPDATE tracks SET %s WHERE id=%s" % (query, trackId)
            uni.printForDevelopers("Query - changeTag - queryUpdate : " + queryUpdate)
            db.query(queryUpdate)
        db.commit()
    return True


def changeArtistValue(_values):
    if len(_values) > 1:
        db = Amarok.checkAndGetDB()
        try:
            queryUpdate = "UPDATE artists SET name='%s' WHERE id=%s" % (
                Databases.correctForSql(_values["name"]), _values["id"])
            uni.printForDevelopers("Query - changeArtistValue : " + queryUpdate)
            db.query(queryUpdate)
            db.commit()
            return [_values["name"],
                    getAllMusicFilePathsByArtistId(_values["id"]),
                    getAllMusicFilePathsByAlbumArtistId(_values["id"])]
        except Amarok.getMySQLModule().IntegrityError as error:
            returnValues = [_values["name"],
                            getAllMusicFilePathsByArtistId(_values["id"]),
                            getAllMusicFilePathsByAlbumArtistId(_values["id"])]
            changeArtistWithAnother(_values["id"], getArtistId(_values["name"]))
            deleteArtist(_values["id"])
            return returnValues
    return None


def changeArtistWithAnother(_currentArtistId, _artistWillBeSelectedId):
    db = Amarok.checkAndGetDB()
    queryUpdate1 = "UPDATE tracks SET artist=%s WHERE artist=%s" % (_artistWillBeSelectedId, _currentArtistId)
    uni.printForDevelopers("Query - changeArtistWithAnother - queryUpdate1 : " + queryUpdate1)
    db.query(queryUpdate1)
    db.commit()
    try:
        db = Amarok.checkAndGetDB()
        queryUpdate2 = "UPDATE albums SET artist=%s WHERE artist=%s" % (_artistWillBeSelectedId, _currentArtistId)
        uni.printForDevelopers("Query - changeArtistWithAnother - queryUpdate2 : " + queryUpdate2)
        db.query(queryUpdate2)

        db.commit()
    except Amarok.getMySQLModule().IntegrityError as error:
        db = Amarok.checkAndGetDB()
        db.query("SELECT * FROM albums WHERE name IN (SELECT name FROM albums WHERE artist=%s) AND artist=%s" % (
                _artistWillBeSelectedId, _currentArtistId))
        r = db.store_result()
        rows = r.fetch_row(0)
        for row in rows:
            currentAlbumId = row[0]
            currentAlbumName = row[1]
            db = Amarok.checkAndGetDB()
            db.query("SELECT * FROM albums WHERE name='%s' AND artist=%s" % (currentAlbumName, _artistWillBeSelectedId))
            r = db.store_result()
            srows = r.fetch_row(0)
            if len(srows) > 0:
                albumWillBeSelectedId = srows[0][0]
                changeAlbumWithAnother(currentAlbumId, albumWillBeSelectedId)
                deleteAlbum(currentAlbumId)
    return True


def changeAlbumWithAnother(_currentAlbumId, _albumWillBeSelectedId):
    db = Amarok.checkAndGetDB()
    queryUpdate = "UPDATE tracks SET album=%s WHERE album=%s" % (_albumWillBeSelectedId, _currentAlbumId)
    uni.printForDevelopers("Query - changeAlbumWithAnother : " + queryUpdate)
    db.query(queryUpdate)
    db.commit()


def deleteArtist(_artistId):
    db = Amarok.checkAndGetDB()
    queryUpdate = "DELETE FROM artists WHERE id=%s" % (_artistId)
    uni.printForDevelopers("Query - deleteArtist : " + queryUpdate)
    db.query(queryUpdate)
    db.commit()
    return True


def deleteAlbum(_albumId):
    db = Amarok.checkAndGetDB()
    queryUpdate = "DELETE FROM albums WHERE id=%s" % (_albumId)
    uni.printForDevelopers("Query - deleteAlbum : " + queryUpdate)
    db.query(queryUpdate)
    db.commit()
    return True

        
            

