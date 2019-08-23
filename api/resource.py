import models
from flask import Blueprint, request, jsonify, url_for, send_file
from playhouse.shortcuts import model_to_dict

resource = Blueprint('resource', 'resource', url_prefix='/resource')

@resource.route('/', methods=["POST"])
def create_resource():
  payload = request.form.to_dict()
  try:
    models.Resource.get(models.Resource.name == payload['name'])
    return jsonify(data={}, status={"code": 401, "message": "A resource with that name exists"})
  except models.DoesNotExist:
    resource = models.Resource.create(**payload)
    print(type(resource))
    resource_dict = model_to_dict(resource)
    print(resource_dict, 'this is user dict')
    return jsonify(data=resource_dict, status={"code": 201, "message": "Success"})

@resource.route('/', methods=["GET"])
def get_resource():
  try:
    resources = [model_to_dict(resource) for resource in models.Resource.select()]
    return jsonify(data=resources, status={"code": 200, "message": "Success"})
  except models.DoesNotExist:
    return jsonify(data={}, status={"code": 401, "message": "There was an error getting the resource"})
 