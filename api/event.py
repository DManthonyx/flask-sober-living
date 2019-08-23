import models
import os
import sys
import secrets
from PIL import Image
from flask import Blueprint, request, jsonify, url_for, send_file
from playhouse.shortcuts import model_to_dict

event = Blueprint('event', 'event', url_prefix='/event')

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

@event.route('/', methods=["POST"])
def create_home():
    pay_file = request.files
    print(pay_file, 'this is event')
    payload = request.form.to_dict()
    print(payload, 'this is event')
    dict_file = pay_file.to_dict()

    file_picture_path = save_picture(dict_file['file'])
    # payload['user'] = id
    payload['image'] = file_picture_path
    event = models.Event.create(**payload)
    # we can't send back a class we can only send back dicts, lists
    event_dict = model_to_dict(event)
    print(event_dict)

    return jsonify(data=event_dict, status={"code": 201, "message": "Success"})

@event.route('/', methods=["GET"])
def get_events():
  try:
    events = [model_to_dict(event) for event in models.Event.select()]
    return jsonify(data=events, status={"code": 200, "message": "Success"})
  except models.DoesNotExist:
    return jsonify(data={}, status={"code": 401, "message": "There was an error getting the resource"})
 