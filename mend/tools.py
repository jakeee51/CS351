from config import Config
import sqlite3 as sql
import smtplib, urllib, json, time, re, os
from random import choices
import hashlib

if Config.RUN_MODE == "dev":
    print(">>>", os.path.basename(__file__))

alphanum = "abcdefghijklmnopqrstuvwxyz0123456789"

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

def make_salt() -> str:
    salt = ""
    random_chars = choices(alphanum, k = 4)
    for char in random_chars:
        salt += char
    return ''.join(random_chars)

def update_chat(file, sent_msg):
    with open(file, 'a') as f:
        f.write(sent_msg + '\n')

def get_chat(file):
    ret = []
    with open(file) as f:
        for msg in f.readlines():
            msg = msg.replace('\n', "<br>")
            ret.append(msg)
    return ret
