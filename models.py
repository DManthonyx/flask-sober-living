from peewee import *
from flask_login import UserMixin 
import datetime # to help deal with datetimes



DATABASE = connect(os.environ.get('DATABASE_URL'))
# DATABASE = SqliteDatabase('sober.sqlite')
# sqlite is just a file on your computer
# good for expermintation use mysql postgree for production

class User(UserMixin, Model):
  name = CharField()
  last_name = CharField()
  user_type = CharField()
  re_password = CharField()
  password = CharField()
  phone_number = CharField()
  email = CharField()


  class Meta:
  # when the class object creates an object
  # we can give it instructions
    database = DATABASE

class Home(Model):
  address = CharField()
  longitude = CharField()
  latitude = CharField()
  title = CharField()
  city = CharField()
  image = CharField()
  description = CharField()
  phone_number = CharField()
  email = CharField()
  link = CharField()
  user = ForeignKeyField(User, backref='home') 

  class Meta:
    database = DATABASE

class Event(Model):
  city = CharField()
  address = CharField()
  longitude = CharField()
  latitude = CharField()
  name = CharField()
  description = CharField()
  image = CharField()
  phone_number = CharField()
  link = CharField()

  class Meta:
    database = DATABASE

class Resource(Model):
  city = CharField()
  address = CharField()
  latitude = CharField()
  longitude = CharField()
  description = CharField()
  name = CharField()
  phone_number = CharField()
  link = CharField()

  class Meta:
    database = DATABASE

def initialize():
  DATABASE.connect()
  DATABASE.create_tables([User, Event, Resource, Home], safe=True)
  # says look at the tables if they're already created don't do anything
  print("tables created")
  DATABASE.close()
