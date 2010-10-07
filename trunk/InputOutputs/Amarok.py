# -*- coding: utf-8 -*-

import InputOutputs
from MyObjects import *
from time import gmtime
from os import *
import Dialogs
import Organizer
import Universals
isLoadedMysql = False
try:
    import _mysql
    isLoadedMysql = True
except:pass

class Amarok():
    
    def checkAmarok(self):
        return isLoadedMysql and True
        
    def connectAndGetDB(self):
        return _mysql.connect(host=Universals.MySettings["amarokDBHost"], port=int(Universals.MySettings["amarokDBPort"]), user=Universals.MySettings["amarokDBUser"], passwd=Universals.MySettings["amarokDBPass"], db=Universals.MySettings["amarokDBDB"])
        
    def checkAndGetDB(self, _isNoAlertIfSuccesfully=True):
        try:
            db = self.connectAndGetDB()
            db.query("""SELECT component,version FROM admin""")
            r = db.store_result()
            if _isNoAlertIfSuccesfully==False:
                Dialogs.show(translate("CollectionToDirectory", "Connected To Database"), str(translate("CollectionToDirectory", "Connected succesfully to \"%s\"")) % Universals.MySettings["amarokDBDB"])
            return db
        except:
            cla, error, trbk = sys.exc_info()
            if str(error).find("Unknown MySQL server host")!=-1:
                Dialogs.show(translate("CollectionToDirectory", "Not Connected To Database"), str(translate("CollectionToDirectory", "Unknown MySQL server host \"%s\"")) % Universals.MySettings["amarokDBHost"])
            elif str(error).find("Access denied for user")!=-1:
                Dialogs.show(translate("CollectionToDirectory", "Not Connected To Database"), str(translate("CollectionToDirectory", "Access denied for user \"%s\"")) % Universals.MySettings["amarokDBUser"])
            else:
                self.error = ReportBug.ReportBug()
                self.error.show()
            return None
            
    def getDirectoriesAndCovers(self):
        db = self.checkAndGetDB()
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
) AS 'realPath', `images`.`path`, 
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

order by 'realPath'
""")
            r = db.store_result()
            return str(r.fetch_row(1))
        return None
            
            
            
            
            
            
