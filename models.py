from peewee import *
from flask_login import UserMixin 
import os
from playhouse.db_url import connect
# from playhouse.postgres_ext import PostgresqlExtDatabase
# from playhouse.postgres_ext import ArrayField



import datetime # to help deal with datetimes

# DATABASE = connect(os.environ.get('DATABASE_URL'))

# working locally
DATABASE = SqliteDatabase('sober.sqlite')

# sqlite is just a file on your computer
# good for expermintation use mysql postgree for production

class User(UserMixin, Model):
  # user_id = IntegerField(primary_key=True)
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
  image_1 = CharField()
  image_2 = CharField()
  description = CharField()
  phone_number = CharField()
  email = CharField()
  link = CharField()
  user = ForeignKeyField(User, backref='home') 

  class Meta:
    database = DATABASE


def initialize():
  DATABASE.connect()
  DATABASE.create_tables([User, Home], safe=True)
  # says look at the tables if they're already created don't do anything
  print("tables created")
  DATABASE.close()
