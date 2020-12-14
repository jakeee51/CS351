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

def edit_file(file, value):
    with open(file, 'r+') as f:
        lines = f.readlines()
        f.seek(0); found = False
        for line in lines:
            line = line.strip('\n')
            user = line.split(' ')[0]
            if str(value).lower() != user.lower():
                f.write(line + '\n')
            else:
                found = True
        f.truncate()
        return found

def get_public_key(to_user):
    with open("mend/public_keys.txt") as f:
        for line in f.readlines():
            line = line.strip('\n').split(' ')
            if line[0] == to_user:
                return line[1]

def make_salt() -> str:
    salt = ""
    random_chars = choices(alphanum, k = 4)
    for char in random_chars:
        salt += char
    return ''.join(random_chars)

def update_chat(file, sent_msg, from_user):
    with open(file, 'a') as f:
        f.write(f"{from_user}: {sent_msg}\n")

def get_chat(file):
    ret = []
    with open(file) as f:
        for msg in f.readlines():
            msg = msg.strip('\n')
            ret.append(msg)
    return ret
