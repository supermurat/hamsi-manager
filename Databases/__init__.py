# -*- coding: utf-8 -*-

import sys
if float(sys.version[:3])>=2.6:
    import sqlite3 as sqlite
else:
    from pysqlite2 import dbapi2 as sqlite
import Universals
    
class Databases:
    global correctForSql, getDefaultConnection
    
    def correctForSql(_string):
        return str(_string).replace("'", "''")
        
    def getDefaultConnection():
        return sqlite.connect(Universals.pathOfSettingsDirectory + "/database.sqlite")
    
    
        



