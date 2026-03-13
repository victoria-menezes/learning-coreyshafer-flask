from flask import Flask
from dotenv import load_dotenv
import os
app = Flask(__name__) # __name__ lets flask know where to look for templates, etc

# setting up .env
load_dotenv()

# will make the server show changes without restarting, will work with a simple refresh of the page

# @ = decorator, adds functionality to existing functions
@app.route('/') # what we type to go to different pages, etc (/posts, /user, etc)
@app.route('/home') # multiple routes can be used for the same function
def hello():
    return '<h1>Homepage</h1>'

@app.route('/about')
def about():
    return '<h1>About</h1>'


# alternate way of running the application via the python script
# not recommended over just `flask run` in the terminal
# if __name__ == '__main__':
#     app.run(debug = True)