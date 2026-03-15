# where we initialize our app

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
# from flask_mail import Mail # unused
from flaskblog.config import Config

from dotenv import load_dotenv
import os

# setting up .env
load_dotenv()

db = SQLAlchemy() # also calls db.init_app(app)
# print('Database initialized')

# to add users, etc:
# db.session.add(etc)
# db.session.commit

# to query our databases:
# User.query.all() / .first() / .filter_by() / db.session.query(User).get(id)

bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'login' # for the redirection of @login_required
login_manager.login_message_category = 'info' # same categories as the flash messages


def create_app(config_class=Config):
    app = Flask(
        __name__,
        template_folder = os.getenv('TEMPLATE_FOLDER')
        )
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    
    # has to be at the bottom to avoid circularity
    from flaskblog.users.routes import users # importing blueprint instance
    from flaskblog.main.routes import main # importing blueprint instance
    from flaskblog.posts.routes import posts # importing blueprint instance
    app.register_blueprint(users)
    app.register_blueprint(main)
    app.register_blueprint(posts)

    with app.app_context():
        db.create_all()
    
    return app