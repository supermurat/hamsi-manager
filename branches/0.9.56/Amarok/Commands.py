# -*- coding: utf-8 -*-
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


import Amarok


class Commands:
    global getDirectoriesAndValues
    
    def getDirectoriesAndValues():
        db = Amarok.checkAndGetDB()
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
            
            
            
            

