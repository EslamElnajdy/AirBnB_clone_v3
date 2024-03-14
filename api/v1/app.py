#!/usr/bin/python3
""" """

from flask import Flask, Blueprint, make_response, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, origins="0.0.0.0")

api_host = getenv("HBNB_API_HOST", "0.0.0.0")
api_port = getenv("HBNB_API_PORT", 5000)


@app.teardown_appcontext
def teardown(self):
    """close the database connection"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    app.run(host=api_host, port=api_port, threaded=True)
