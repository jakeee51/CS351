import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = ""
    DATABASE_URI = os.environ.get("DATABASE_URL", os.path.join(basedir, "database/database.db"))
    ADMINS = []
    DEBUG = False if int(os.environ.get("FLASK_DEBUG", 0)) == 0 else True
    ENVIRONMENT = os.environ.get("FLASK_ENV")
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = ""
    MAIL_PASSWORD = ""
    RUN_MODE = "dev" # "dev" -> development | "prod" -> production
