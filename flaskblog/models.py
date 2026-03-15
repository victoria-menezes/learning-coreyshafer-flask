# from flaskblog import db 
# does not work as it is a circular import
# (flaskblog is importing this, which is importing db from flaskblog, but when it tries to import from flaskblog it tries to import itself , etc...)
# instead we turned out application into a package

from datetime import datetime, timezone
from flaskblog import db, app, login_manager

from flask_login import UserMixin

from itsdangerous import URLSafeTimedSerializer as Serializer

@login_manager.user_loader
def load_user(user_id : int):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(
        db.Integer,
        primary_key = True # if left blank, will be assigned automatically since its the primary key
        )
    username = db.Column(
        db.String(20),
        unique = True,
        nullable = False
    )
    email = db.Column(
        db.String(120),
        unique = True,
        nullable = False
    )
    image_file = db.Column(
        db.String(20),
        nullable = False,
        default = 'default.jpg'
    )
    password = db.Column(
        db.String(60),
        nullable = False
    )
    posts = db.relationship(
        'Post',
        backref = 'author', # lets us access Post.author to get the user object that is the author 
        lazy = True # sqlalchemy will load the data as necessary in one go
    )

    

    def get_reset_token(
            self
    ):
        s = Serializer(app.config['SECRET_KEY'])

        return s.dumps({'user_id':self.id}).decode('utf-8')
    
    @staticmethod # telling python not to expect self as an argument
    def verify_reset_token(
            token
    ):
        MINUTES_TO_RESET = 30

        expires_sec = 60 * MINUTES_TO_RESET

        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token, max_age = expires_sec)['user_id']
        except:
            return None
        return User.query.get(user_id)
        

    def __repr__(self) -> str:
        # how its printed with print()
        return f'User(\'{self.username}\', \'{self.email}\', \'{self.image_file}\')'

class Post(db.Model):
    id = db.Column(
        db.Integer,
        primary_key = True
    )
    title = db.Column(
        db.String(100),
        nullable = False
    )
    date_posted = db.Column(
        db.DateTime,
        nullable = False,
        default = lambda : datetime.now(timezone.utc) # if you just pass the function without lambda, it'll stay static for all of the posts made that session
    )
    content = db.Column(
        db.Text,
        nullable = False
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable = False
    )
    
    def __repr__(self) -> str:
        # how its printed with print()
        return f'Post(\'{self.title}\', \'{self.date_posted}\')'


with app.app_context():
    db.create_all()