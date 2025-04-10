from flask import Flask
from urllib.parse import quote

from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# from app import index  # Import routes

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/wafdb?charset=utf8mb4" % quote( "Admin@123")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.secret_key = "##%#%FGE~EBb$enb?jn##3323290!!@vdv;vd.;ư"

db = SQLAlchemy(app=app)

login = LoginManager(app)