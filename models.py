from peewee import *
from flask_login import UserMixin 
import datetime # to help deal with datetimes

DATABASE = SqliteDatabase('sober.sqlite')
# sqlite is just a file on your computer
# good for expermintation use mysql postgree for production

class User(UserMixin, Model):
  name = CharField()
  last_name = CharField()
  user_type = CharField()
  re_password = CharField()
  password = CharField()
  age = CharField()
  ethnicity = CharField()
  gender = CharField()
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

  class Meta:
    database = DATABASE

class Events(Model):
  address = CharField()
  long = CharField()
  lat = CharField()
  name = CharField()
  description = CharField()
  image = CharField()

  class Meta:
    database = DATABASE

class Resources(Model):
  address = CharField()
  lat = CharField()
  long = CharField()
  description = CharField()
  title = CharField()
  phone_number = CharField()

  class Meta:
    database = DATABASE

def initialize():
  DATABASE.connect()
  DATABASE.create_tables([User, Events, Resources], safe=True)
  # says look at the tables if they're already created don't do anything
  print("tables created")
  DATABASE.close()
