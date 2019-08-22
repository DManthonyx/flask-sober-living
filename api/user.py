import models
import os
import sys
import secrets
from flask import Blueprint, request, jsonify, url_for, send_file
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user
from playhouse.shortcuts import model_to_dict

user = Blueprint('user', 'user', url_prefix='/user')

@user.route('/signup', methods=["POST"])
def signup():
  print(request, 'this is request')
  print(type(request), 'this is request type')
  payload = request.form.to_dict()
  print(payload, 'this is pay load')
  try:
    models.User.get(models.User.email == payload['email'])
    return jsonify(data={}, status={"code": 401, "message": "A user with that name or email exists"})
  except models.DoesNotExist:
    payload['password'] = generate_password_hash(payload['password'])
    user = models.User.create(**payload)
    print(type(user))
    login_user(user)
    user_dict = model_to_dict(user)
    print(user_dict, 'this is user dict')
    print(type(user_dict), 'this is user dict type')
    del user_dict['password']
    return jsonify(data=user_dict, status={"code": 201, "message": "Success"})

@user.route('/login', methods=["POST"])
def login():
  payload = request.get_json()
  print(payload, '< --- this is playload')
  try:
    user = models.User.get(models.User.email== payload['email'])
    user_dict = model_to_dict(user)
    if(check_password_hash(user_dict['password'], payload['password'])):
      del user_dict['password']
      print(current_user.__dict__, 'current user')
      return jsonify(data=user_dict, status={"code": 200, "message": "Success"})
    else:
      return jsonify(data={}, status={"code": 401, "message": "Username or Password is incorrect"})
  except models.DoesNotExist:
    return jsonify(data={}, status={"code": 401, "message": "Username or Password is incorrect"})


@user.route('/logout')
def logout():
  logout_user()
  print(current_user.__dict__, 'this is current user')
  return jsonify(status={"code": 200, "message": "logout"})
