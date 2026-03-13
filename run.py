# FLASK_APP = run.py

from flaskblog import app
from flaskblog import routes # has to be at the bottom of init or here to avoid circularity
# importing runs the code inside, by importing routes we are creating all of the routes in the module

# alternate way of running the application via the python script
# not recommended over just `flask run` in the terminal
if __name__ == '__main__':
    app.run(debug = True)