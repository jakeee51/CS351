import sqlite3 as sql
import pandas as pd

'''
# To set the revision in the database to the head, without performing any migrations.
  You can change head to the required change you want.
$ flask db stamp head

# To detect automatically all the changes.
$ flask db migrate

# To apply all the changes.
$ flask db upgrade
'''

db_path = "database/database.db"
conn = sql.connect(db_path)


def sqlite_query(query, args=(), one=False):
   cur = conn.cursor()
   cur = conn.execute(query, args); conn.commit()
   rv = [dict((cur.description[idx][0], value)
              for idx, value in enumerate(row)) for row in cur.fetchall()]
   return (rv[0] if rv else None) if one else rv

def show_columns(table):
   cur = conn.cursor()
   query = f"PRAGMA table_info('{table}')"
   cur.execute(query); conn.commit()
   rows = cur.fetchall(); cols = ["| Field\t| Type\t\t| Null\t| Key\t| Default |", "+-------------------------------------------------+"]
   for row in rows:
      c_name = row[1][:7]
      c_type = row[2]
      if len(c_type) < 7:
         c_type = row[2] + "      "
      col = f"{c_name}\t| {c_type}\t| {row[3]}\t| {row[5]}\t| {row[4]}"
      cols.append(col)
   return cols

def show_data(table):
   print(f"{table} TABLE")
   records = 0
   for row in sqlite_query(f"SELECT * FROM {table}"):
      print(row)
      records += 1
      if records == 300:
         break
   if records == 0:
      print("Empty Table (no records)")
   else:
      print(records ,"total records")
   print("\n__________")

def populate_orgs():
   cur = conn.cursor()
   to_db = []
   with open("friends_metadata.txt") as f:
      for row in f.readlines():
         entry = row.strip('\n').split('|')
         season = entry[0][:2]; episode = entry[0][2:]
         tupe = tuple()
         tupe += tuple((entry[0],))
         tupe += tuple((season,)); tupe += tuple((episode,))
         tupe += tuple((entry[1],))
         tupe += tuple(("N/A",))
         tupe += tuple((entry[2],))
         to_db.append(tupe)
   query = "INSERT INTO Friends VALUES(?,?,?,?,?,?)"
   cur.executemany(query, to_db)
   conn.commit()

'''CREATE'''
##query = "CREATE TABLE Users(id INTEGER PRIMARY KEY AUTOINCREMENT,"\
##        "user VARCHAR(32) UNIQUE NOT NULL,"\
##        "password VARCHAR(128) NOT NULL,"\
##        "salt VARCHAR(4) NOT NULL)"
##conn.execute(query)
##query = "CREATE TABLE Friends(user VARCHAR(32) NOT NULL PRIMARY KEY,"\
##        "friends TEXT NOT NULL)"
##conn.execute(query)
##query = "CREATE TABLE Messages(channel VARCHAR(8) NOT NULL,"\
##        "user VARCHAR(32) NOT NULL, log TEXT NULL)"
##conn.execute(query)

'''INSERT'''
##populate_orgs()
##query = "INSERT INTO Users(user,password,salt) VALUES(?,?,?)"
##sqlite_query(query, ("abc123", "secret", "salt"))

'''UPDATE'''
##query = "UPDATE Users SET episode_name='The Last One, Part 2' WHERE id='1018'"
##conn.execute(query)
##print("Record updated!")

'''DELETE'''
##sqlite_query("DELETE FROM Users WHERE id=?", ('1',))
##print("Record deleted!")

'''DROP'''
##sqlite_query("DROP TABLE Users")
##print("Table deleted!")

'''SELECT'''
show_data("Users")

'''SHOW COLUMNS'''
##for column in show_columns('Users'):
##   print(column)


conn.close()
