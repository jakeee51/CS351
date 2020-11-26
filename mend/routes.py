from flask import Flask, session, redirect, url_for, render_template,\
     request, make_response
from mend import application as app
from mend.tools import *
from config import Config
import json, time, re, os

if Config.RUN_MODE == "dev":
    print(">>>", os.path.basename(__file__))

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
                return '0'
            else:
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
            return '0'
        except sql.IntegrityError:
            return '-1'
    return redirect(url_for('login'))

@app.route("/home", methods=["GET", "POST"])
def home():
    if request.referrer != None:
        return render_template("home.html")

@app.route("/index", methods=["GET", "POST"])
def index():
    if request.referrer != None:
        return render_template("index.html")
