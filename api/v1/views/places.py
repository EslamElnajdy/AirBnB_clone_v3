#!/usr/bin/python3
""" """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False, methods=["GET"])
def get_places(city_id):
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    result = [place.to_dict() for place in city.places]
    return jsonify(result)


@app_views.route('/places/<place_id>',
                 strict_slashes=False, methods=["GET"])
def get__place_id(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>',
                 strict_slashes=False, methods=["DELETE"])
def del_place(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    storage.delete(place)
    storage.save()
    return jsonify({})


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False, methods=["POST"])
def create_place(city_id):

    if not storage.get(City, city_id):
        abort(404)

    if not request.get_json():
        abort(400, "Not a JSON")

    if "user_id" not in request.get_json():
        abort(400, "Missing user_id")

    if not storage.get(User, request.get_json()['user_id']):
        abort(404)

    if "name" not in request.get_json():
        abort(400, "Missing name")

    place = Place(city_id=city_id, **request.get_json())
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>',
                 strict_slashes=False, methods=["PUT"])
def update_place(place_id):
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data_json = request.get_json()
    if type(data_json) is not dict:
        abort(400, "Not a JSON")
    for key, value in data_json.items():
        if key in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            continue
        setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200
