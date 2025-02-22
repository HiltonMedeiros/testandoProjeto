from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# CONFIGURA URI DO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meubanco.db'


db = SQLAlchemy(app)
