#!/usr/bin/python3
""" """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from models.review import Review


@app_views.route('/places/<place_id>/reviews',
                 strict_slashes=False, methods=["GET"])
def get_places_review(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    result = [review.to_dict() for review in place.reviews]
    return jsonify(result)


@app_views.route('/reviews/<review_id>',
                 strict_slashes=False, methods=["GET"])
def get__place_id_review(review_id):
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>',
                 strict_slashes=False, methods=["DELETE"])
def del_place_review(review_id):
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    storage.delete(review)
    storage.save()
    return jsonify({})


@app_views.route('/places/<place_id>/reviews',
                 strict_slashes=False, methods=["POST"])
def create_place_review(place_id):

    if not storage.get(Place, place_id):
        abort(404)

    if not request.get_json():
        abort(400, "Not a JSON")

    if "user_id" not in request.get_json():
        abort(400, "Missing user_id")

    if not storage.get(User, request.get_json()['user_id']):
        abort(404)

    if "text" not in request.get_json():
        abort(400, "Missing text")

    review = Review(place_id=place_id, **request.get_json())
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>',
                 strict_slashes=False, methods=["PUT"])
def update_place_review(review_id):
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    data_json = request.get_json()
    if type(data_json) is not dict:
        abort(400, "Not a JSON")
    for key, value in data_json.items():
        if key in ["id", "user_id", "place_id", "created_at", "updated_at"]:
            continue
        setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
