import models

from flask import Blueprint, request, jsonify
from playhouse.shortcuts import model_to_dict


api = Blueprint('api', 'api', url_prefix='/api')

@api.route('/info', methods=["GET"])
def get_info():
  try:
    users = [model_to_dict(user) for user in models.User.select()]
    
    return jsonify(data=users,  status={"code": 200, "message": "Success"})
  except models.DoesNotExist:
    return jsonify(data={}, status={"code": 401, "message": "There was an error getting Home"})
