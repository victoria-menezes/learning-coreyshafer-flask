# defines this as a package
# where we initialize our app

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
# from flask_mail import Mail # unused

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

# to add users, etc:
# db.session.add(etc)
# db.session.commit

# to query our databases:
# User.query.all() / .first() / .filter_by() / db.session.query(User).get(id)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login' # for the redirection of @login_required
login_manager.login_message_category = 'info' # same categories as the flash messages