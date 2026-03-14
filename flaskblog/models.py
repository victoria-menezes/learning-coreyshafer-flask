# from flaskblog import db 
# does not work as it is a circular import
# (flaskblog is importing this, which is importing db from flaskblog, but when it tries to import from flaskblog it tries to import itself , etc...)
# instead we turned out application into a package

from datetime import datetime, timezone
from flaskblog import db, app

class User(db.Model):
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
        default = datetime.now(timezone.utc)
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
    # print('Models initialized', db.Model.__subclasses__())