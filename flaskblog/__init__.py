# defines this as a package
# where we initialize our app

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from dotenv import load_dotenv
import os

# setting up .env
load_dotenv()
app = Flask(__name__,
    template_folder = os.getenv('TEMPLATE_FOLDER')
    ) # __name__ lets flask know where to look for templates, etc

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')

db = SQLAlchemy(app)
# database is created via python terminal
# from flaskblog import app, db
# app.app_context().push()
# db.create_all()

# to add users, etc:
# db.session.add(etc)
# db.session.commit

# to query our databases:
# User.query.all() / .first() / .filter_by() / db.session.query(User).get(id)
