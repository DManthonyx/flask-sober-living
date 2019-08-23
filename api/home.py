import models
import os
import sys
import secrets
from PIL import Image
from flask import Blueprint, request, jsonify, url_for, send_file
from playhouse.shortcuts import model_to_dict

home = Blueprint('home', 'home', url_prefix='/home')

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    f_name, f_ext = os.path.splitext(form_picture.filename)
    picture_name = random_hex + f_ext
    file_path_for_avatar = os.path.join(os.getcwd(), 'static/profile_pics/' + picture_name)
    output_size = (125, 175)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(file_path_for_avatar) 
    return picture_name

@home.route('/<id>/createhome', methods=["POST"])
def create_home(id):
    pay_file = request.files
    # print(pay_file, 'this is home')
    payload = request.form.to_dict()
    # print(payload, 'this is home')
    dict_file = pay_file.to_dict()
    try:
        models.Home.get(models.Home.longitude == payload['longitude'] and models.Home.latitude == payload['latitude'])
        return jsonify(data={}, status={"code": 401, "message": "address aleady used"})
    except models.DoesNotExist: # boolean on the model
        file_picture_path = save_picture(dict_file['file'])
        payload['user'] = id
        payload['image'] = file_picture_path
        home = models.Home.create(**payload)
        # we can't send back a class we can only send back dicts, lists
        home_dict = model_to_dict(home)
        print(home_dict)

        return jsonify(data=home_dict, status={"code": 201, "message": "Success"})

@home.route('/', methods=["GET"])
def get_homes():
  try:
    homes = [model_to_dict(home) for home in models.Home.select()]
    return jsonify(data=homes, status={"code": 200, "message": "Success"})
  except models.DoesNotExist:
    return jsonify(data={}, status={"code": 401, "message": "There was an error getting the resource"})
 