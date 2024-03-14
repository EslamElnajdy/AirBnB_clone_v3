#!/usr/bin/python3
""" """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users', strict_slashes=False, methods=["GET"])
def get_users():
    result = [user.to_dict() for user in storage.all(User).values()]
    return jsonify(result)


@app_views.route('/users/<user_id>',
                 strict_slashes=False, methods=["GET"])
def get__user_id(user_id):
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>',
                 strict_slashes=False, methods=["DELETE"])
def del_user(user_id):
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    storage.delete(user)
    storage.save()
    return jsonify({})


@app_views.route('/users', strict_slashes=False, methods=["POST"])
def create_user():
    if not request.get_json():
        abort(400, "Not a JSON")
    if "email" not in request.get_json():
        abort(400, "Missing email")
    if "password" not in request.get_json():
        abort(400, "Missing password")
    user = User(**request.get_json())
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>',
                 strict_slashes=False, methods=["PUT"])
def update_user(user_id):
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    data_json = request.get_json()
    if type(data_json) is not dict:
        abort(400, "Not a JSON")
    for key, value in data_json.items():
        if key in ["id", "email", "created_at", "updated_at"]:
            continue
        setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
