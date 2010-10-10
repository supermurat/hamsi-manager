# -*- coding: utf-8 -*-

from os import *
import sys
import InputOutputs
from MyObjects import *
from time import gmtime
import Dialogs
import Organizer
import Universals
import ReportBug
isLoadedMysql = False
isCheckAgain = True
try:
    import _mysql as mdb
    isLoadedMysql = True
except:pass

class Amarok:
    global checkAmarok, connectAndGetDB, checkAndGetDB, getDirectoriesAndValues
    
    def checkAmarok():
        return isLoadedMysql and True
        
    def connectAndGetDB():
        return mdb.connect(host=Universals.MySettings["amarokDBHost"], port=int(Universals.MySettings["amarokDBPort"]), user=Universals.MySettings["amarokDBUser"], passwd=Universals.MySettings["amarokDBPass"], db=Universals.MySettings["amarokDBDB"])
        
    def checkAndGetDB(_isNoAlertIfSuccesfully=True):
        global isCheckAgain
        try:
            db = connectAndGetDB()
            if isCheckAgain:
                db.query("""SELECT component,version FROM admin""")
                r = db.store_result()
                if _isNoAlertIfSuccesfully==False:
                    Dialogs.show(translate("CollectionToDirectory", "Connected To Database"), str(translate("CollectionToDirectory", "Connected succesfully to \"%s\"")) % Universals.MySettings["amarokDBDB"])
            isCheckAgain = False
            return db
        except:
            cla, error, trbk = sys.exc_info()
            if str(error).find("Unknown MySQL server host")!=-1:
                Dialogs.show(translate("CollectionToDirectory", "Not Connected To Database"), str(translate("CollectionToDirectory", "Unknown MySQL server host \"%s\"")) % Universals.MySettings["amarokDBHost"])
            elif str(error).find("Access denied for user")!=-1:
                Dialogs.show(translate("CollectionToDirectory", "Not Connected To Database"), str(translate("CollectionToDirectory", "Access denied for user \"%s\"")) % Universals.MySettings["amarokDBUser"])
            elif str(error).find("Unknown database")!=-1:
                Dialogs.show(translate("CollectionToDirectory", "Not Connected To Database"), str(translate("CollectionToDirectory", "Unknown database \"%s\"")) % Universals.MySettings["amarokDBDB"])
            else:
                error = ReportBug.ReportBug()
                error.show()
            return None
            
    def getDirectoriesAndValues():
        db = checkAndGetDB()
        if db!=None:
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
WHERE `images`.`path` is not null
order by 'realPath'
""")
            directoriesValues = {}
            r = db.store_result()
            rows = r.fetch_row(0)
            for row in rows:
                if row[0] not in directoriesValues:
                    directoriesValues[row[0]] = {"coverPath" : [], "Artist" : [], "Album" : [], "Genre" : [], "Year" : []}
                directoriesValues[row[0]]["coverPath"].append(row[1])
                directoriesValues[row[0]]["Artist"].append(row[2])
                directoriesValues[row[0]]["Album"].append(row[3])
                directoriesValues[row[0]]["Genre"].append(row[4])
                directoriesValues[row[0]]["Year"].append(row[5])
            return directoriesValues
        return None
            
            
            
            
