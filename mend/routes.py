from flask import Flask, session, redirect, url_for, render_template,\
     request, make_response
from mend import application as app
from mend.tools import *
from config import Config
import json, time, re, os

if Config.RUN_MODE == "dev":
    print(">>>", os.path.basename(__file__))

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form["user"]
        pas = request.form["pass"]
        # Query Database
        if user.lower() == "abc123" and pas.lower() == "password":
            return redirect(url_for("home"))
    return render_template("index.html")

@app.route("/home", methods=["GET", "POST"])
def home():
    if request.referrer != None:
        return render_template("home.html")

@app.route("/index", methods=["GET", "POST"])
def index():
    if request.referrer != None:
        return redirect(url_for('home'))
