from flask import Flask, g
from flask_cors import CORS
from flask_login import LoginManager
import models

# import the blueprint
from api.user import user
from api.api import api
from api.home import home

DEBUG = True
PORT = 8000

login_manager = LoginManager()

app = Flask(__name__, static_url_path="", static_folder="static")
app.secret_key = '123321random STRING'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(userid):
  try:
    print(userid, 'this is user id')
    return models.User.get(models.User.id == userid)
  except models.DoesNotExist:
    return None

CORS(user, origins=['http://localhost:3000'], supports_credentials=True)
CORS(api, origins=['http://localhost:3000'], supports_credentials=True)
CORS(home, origins=['http://localhost:3000'], supports_credentials=True)

app.register_blueprint(user)
app.register_blueprint(api)
app.register_blueprint(home)

@app.before_request 
def before_request():
  """Connect to the database before each request"""
  g.db = models.DATABASE
  g.db.connect()

@app.after_request # given to us by flask @
def after_request(response):
  ###Close the database connection after each request####
  g.db.close()
  return response

# The default URL ends in / ("my-website.com/").
@app.route('/home') #decorator, anything with the @ is a decorator, and its a function
def get_user():
  query.Home.select()
# before a function
def index(): #name this method whatever
  return 'hi' # res.send in express


# Run the app when the program starts! 
if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT) #app.listen in express
