import os
rom flask import Flask, g
from flask_cors import CORS
from flask_login import LoginManager, login_user, current_user, logout_user
import models

# import the blueprint
from api.user import user
from api.api import api
from api.home import home
from api.resource import resource
from api.event import event

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
CORS(resource, origins=['http://localhost:3000'], supports_credentials=True)
CORS(event, origins=['http://localhost:3000'], supports_credentials=True)

app.register_blueprint(user)
app.register_blueprint(api)
app.register_blueprint(home)
app.register_blueprint(resource)
app.register_blueprint(event)

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


@app.route('/', methods=["GET"])
def get_homes():
  try:
    print('this is landing page')
    homes = [model_to_dict(home) for home in models.Home.select()]
    return jsonify(data=homes, status={"code": 200, "message": "Success"})
  except models.DoesNotExist:
    return jsonify(data={}, status={"code": 401, "message": "There was an error getting the resource"})

@app.route('/logout')
def logout():
  logout_user()
  return jsonify(status={"code": 200, "message": "logged out"})
 
# before a function
# def index(): #name this method whatever
#   return 'hi' # res.send in express

if 'ON_HEROKU' in os.environ:
    print('hitting ')
    models.initialize()

# Run the app when the program starts! 
if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT) #app.listen in express
