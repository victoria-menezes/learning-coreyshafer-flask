# FLASK_APP = run.py

from flaskblog import app

# has to be at the bottom of init or here to avoid circularity
from flaskblog.users.routes import users # importing blueprint instance
from flaskblog.main.routes import main # importing blueprint instance
from flaskblog.posts.routes import posts # importing blueprint instance

app.register_blueprint(users)
app.register_blueprint(main)
app.register_blueprint(posts)

# importing runs the code inside, by importing routes we are creating all of the routes in the module
# routes also imports models

# alternate way of running the application via the python script
# not recommended over just `flask run` in the terminal

if __name__ == '__main__':
    app.run(debug = True)