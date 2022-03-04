
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPTokenAuth

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '*\xad\xf0\x1dU\x1e\xb7\xb2\xa2\xd2\x03\\ov\x8f)\xe8\xcf\xbf\xc4\x88\xde0K'

db = SQLAlchemy(app)
auth = HTTPTokenAuth(scheme='Bearer')