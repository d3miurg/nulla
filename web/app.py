from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import cfg
from flask_script import Manager

app = Flask(__name__)
app.config.from_object(cfg)

db = SQLAlchemy(app)