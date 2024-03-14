#!/usr/bin/python3
""" """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states', strict_slashes=False, methods=["GET"])
def get_states():
    return jsonify([state.to_dict() for state in storage.all(State).values()])


@app_views.route('/states/<state_id>', strict_slashes=False, methods=["GET"])
def get_state_id(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>',
                 strict_slashes=False, methods=["DELETE"])
def del_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    storage.delete(state)
    storage.save()
    return jsonify({})


@app_views.route('/states', strict_slashes=False, methods=["POST"])
def create_state():
    if not request.get_json():
        abort(400, "Not a JSON")
    if "name" not in request.get_json():
        abort(400, "Missing name")
    state = State(**request.get_json())
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', strict_slashes=False, methods=["PUT"])
def update_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    data_json = request.get_json()
    if type(data_json) is not dict:
        abort(400, "Nota JSON")
    setattr(state, "name", data_json.get("name"))
    state.save()
    return jsonify(state.to_dict()), 200
