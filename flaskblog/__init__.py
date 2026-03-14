# defines this as a package
# where we initialize our app

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

from dotenv import load_dotenv
import os

# setting up .env
load_dotenv()
app = Flask(
    __name__,
    template_folder = os.getenv('TEMPLATE_FOLDER')
    ) # __name__ lets flask know where to look for templates, etc

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite3' # trying to get this in the .env threw errors, do not recommend

db = SQLAlchemy(app) # also calls db.init_app(app)
# print('Database initialized')

# database is created via python terminal
# from flaskblog import app, db
# app.app_context().push()
# db.create_all()

# to add users, etc:
# db.session.add(etc)
# db.session.commit

# to query our databases:
# User.query.all() / .first() / .filter_by() / db.session.query(User).get(id)

bcrypt = Bcrypt(app)
