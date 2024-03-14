#!/usr/bin/python3
""" """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State, City


@app_views.route('/states/<state_id>/cities',
                 strict_slashes=False, methods=["GET"])
def get_cities(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities4state = []
    for cty in state.cities:
        cities4state.append(cty.to_dict())
    return jsonify(cities4state)


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=["GET"])
def get_city_id(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>',
                 strict_slashes=False, methods=["DELETE"])
def del_city(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities',
                 strict_slashes=False, methods=["POST"])
def create_city(state_id):

    state = storage.get(State, state_id)
    if not state:
        abort(404)

    if not request.get_json():
        abort(400, "Not a JSON")

    if "name" not in request.get_json():
        abort(400, "Missing name")

    city = City(state_id=state_id, **request.get_json())
    storage.new(city)
    storage.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=["PUT"])
def update_city(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data_json = request.get_json()
    if type(data_json) is not dict:
        abort(400, "Nota JSON")
    setattr(city, "name", data_json.get("name"))
    city.save()
    return jsonify(city.to_dict()), 200
