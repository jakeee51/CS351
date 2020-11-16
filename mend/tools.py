from config import Config
import sqlite3 as sql
import smtplib, urllib, json, time, re, os

if Config.RUN_MODE == "dev":
    print(">>>", os.path.basename(__file__))

def send_post(route, data={}):
    url = Config.DOMAIN + '/' + str(route.strip('/'))
    data_encoded = urllib.parse.urlencode(data)
    data_encoded = data_encoded.encode("ascii")
    resp = urllib.request.urlopen(url, data_encoded)
    return resp.read().decode()

def sqlite_query(query, args=(), one=False) -> list: # Returns a list of dictionaries (rows in a table)
   db = sql.connect(Config.DATABASE_URI)
   cur = db.cursor()
   cur = db.execute(query, args); db.commit()
   rv = [dict((cur.description[idx][0], value) for idx, value in enumerate(row)) for row in cur.fetchall()]
   db.close()
   return (rv[0] if rv else None) if one else rv
