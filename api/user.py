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
    print(user, "<== THIS IS THE LOGIN USER")
    login_user(user)
    print(current_user.__dict__, "<== THIS IS THE CURRENT_USER DICT")
    print(current_user.is_active, "<== THIS SHOULD BE TRUE")
    print(current_user.get_id(), "<== THIS SHOULD BE 1")
    print(current_user.is_authenticated, "THIS SHOULD BE TRUE")
    print(current_user.is_anonymous, "THIS SHOULD BE FALSE")
    if(check_password_hash(user_dict['password'], payload['password'])):
      del user_dict['password']
      return jsonify(data=user_dict, session=login_user(user), status={"code": 200, "message": "Success"})
    else:
      return jsonify(data={}, status={"code": 401, "message": "Username or Password is incorrect"})
  except models.DoesNotExist:
    return jsonify(data={}, status={"code": 401, "message": "Username or Password is incorrect"})

@user.route('/logout')
def logout():
  logout_user()
  return jsonify(status={"code": 200, "message": "logged out"})

@user.route('/', methods=["GET"])
def get_users():
  try:
    users = [model_to_dict(user) for user in models.User.select()]
    return jsonify(data=users, status={"code": 200, "message": "Success"})
  except models.DoesNotExist:
    return jsonify(data={}, status={"code": 401, "message": "There was an error getting the resource"})

@user.route('/<id>/delete', methods=["DELETE"])
def delete_user(id):
  query = models.User.delete().where(models.User.id == id)
  query.execute()

  return jsonify(data="resource successfully deleted", status={"code": 200, "message": "User deleted"})