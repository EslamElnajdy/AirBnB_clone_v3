#!/usr/bin/python3
""" """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', strict_slashes=False, methods=["GET"])
def get_amenities():
    result = [amenity.to_dict() for amenity in storage.all(Amenity).values()]
    return jsonify(result)


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False, methods=["GET"])
def get__am_id(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False, methods=["DELETE"])
def del_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    storage.delete(amenity)
    storage.save()
    return jsonify({})


@app_views.route('/amenities', strict_slashes=False, methods=["POST"])
def create_amenity():
    if not request.get_json():
        abort(400, "Not a JSON")
    if "name" not in request.get_json():
        abort(400, "Missing name")
    amenity = Amenity(**request.get_json())
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False, methods=["PUT"])
def update_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    data_json = request.get_json()
    if type(data_json) is not dict:
        abort(400, "Nota JSON")
    setattr(amenity, "name", data_json.get("name"))
    amenity.save()
    return jsonify(amenity.to_dict()), 200
