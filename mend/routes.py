from flask import Flask, session, redirect, url_for, render_template,\
     request, make_response
from mend import application as app
from mend.tools import *
from config import Config
import json, time, re, os

if Config.RUN_MODE == "dev":
    print(">>>", os.path.basename(__file__))

@app.route('/logout', methods=["GET"])
def logout(): # Logout Handler
    session.pop("username", None)
    resp = make_response(redirect(url_for("login")))
    return resp

@app.route("/", methods=["GET"])
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["user"]
        pas = request.form["pass"]
        query = "SELECT user,password,salt FROM Users"
        users = sqlite_query(query)
        for row in users:
            hash_pass = hashlib.sha256((pas + row["salt"]).encode()).hexdigest()
            if row["user"] == user and row["password"] == hash_pass:
                session["username"] = user
                return '0'
        return '-1'
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])    
def register():
    if request.method == "POST":
        user = request.form["user"]
        pas = request.form["pass"]
        salt = make_salt()
        hash_pass = hashlib.sha256((pas + salt).encode()).hexdigest()
        try:
            query = "INSERT INTO Users(user,password,salt) VALUES(?,?,?)"
            sqlite_query(query, (user,hash_pass,salt))
            session["username"] = user
            return '0'
        except sql.IntegrityError:
            return '-1'
    return redirect(url_for('login'))

@app.route("/home", methods=["GET", "POST"])
def home():
    user = session["username"]; dms = []
    if request.referrer != None:
        query = "SELECT from_user,to_user FROM Messages"
        results = sqlite_query(query)
        for row in results:
            if row["from_user"] == user:
                dms.append(row["to_user"])
        return render_template("home.html", dms = dms)

@app.route('/create', methods=["GET", "POST"])
def create(): # Create new chat channel
    if request.referrer != None:
        to_user = request.form["user"]
        user = session["username"]
        if to_user == user:
            return '-1'
        query = "SELECT user FROM Users"
        users = sqlite_query(query)
        for row in users:
            if row["user"] == to_user:
                query = "SELECT to_user FROM Messages WHERE from_user=? AND to_user=?"
                result = sqlite_query(query, (user, to_user), one=True)
                if result == None:
                    with open("mend/next_channel.txt", 'r') as f:
                        channel = f.read().strip('\n')
                    with open("mend/next_channel.txt", 'w') as f:
                        next_channel = int(channel) + 1
                        f.write(str(next_channel))
                    with open(f"mend/chat_logs/{channel}.txt", 'w') as f:
                        f.write("Beginning Of Chat\n")
                    query = "INSERT INTO Messages(channel,from_user,to_user) VALUES(?,?,?)"
                    sqlite_query(query, (channel, user, to_user))
                    return channel
                else:
                    return '0'
        return '-1'

@app.route("/get_channel", methods=["POST"])
def get_channel(): # Retrieve channel ID
    if request.referrer != None:
        user = session["username"]
        to_user = request.form["user"]
        query = "SELECT channel FROM Messages WHERE from_user=? AND to_user=?"
        results = sqlite_query(query, (user, to_user), one=True)
        return results["channel"]
    return '-1'

@app.route("/channel/<channel_id>", methods=["GET"])
def channel(channel_id):
    if request.referrer != None:
        file_path = f"mend/chat_logs/{channel_id}.txt"
        user = session["username"]
        query = "SELECT from_user,to_user FROM Messages WHERE channel=?"
        results = sqlite_query(query, (channel_id,))
        for row in results:
            if row["from_user"] == user or row["to_user"] == user:
                chat_log = get_chat(file_path)
                return render_template("chat.html",
                                       channel = channel_id,
                                       log = chat_log)
    return "404 - Page Not Found!"

@app.route("/send", methods=["POST"])
def send(): # Send message and add to database log
    if request.referrer != None:
        msg = request.form["msg"]
        channel = request.form["channel"]
        file_path = f"mend/chat_logs/{channel}.txt"
        update_chat(file_path, msg)
        return '0'
    return '-1'

@app.route("/index", methods=["GET", "POST"])
def index():
    if request.referrer != None:
        return render_template("index.html")
