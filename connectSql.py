import os
import pymysql

def Connect_To_CloudSQL(dbname):
    db = pymysql.connect(
        "35.232.238.151",
        user="root",
        passwd="k6vjyXC3L7dKT2DKrCTs",
        db=dbname)
    
    return db
