#!/usr/bin/python3
"""States views"""
from flask import jsonify, make_response, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.review import Review
from models.user import User


@app.route('/api/v1/places/<place_id>/reviews', methods=['GET'])
def get_reviews(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)

@app.route('/api/v1/reviews/<review_id>', methods=['GET'])
def get_review(review_id):
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())

@app.route('/api/v1/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200

@app.route('/api/v1/places/<place_id>/reviews', methods=['POST'])
def create_review(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    json_data = request.get_json()
    if not json_data:
        abort(400, "Not a JSON")
    if 'user_id' not in json_data:
        abort(400, "Missing user_id")
    user = storage.get(User, json_data['user_id'])
    if not user:
        abort(404)
    if 'text' not in json_data:
        abort(400, "Missing text")
    json_data['place_id'] = place_id
    new_review = Review(**json_data)
    storage.new(new_review)
    storage.save()
    return jsonify(new_review.to_dict()), 201

@app.route('/api/v1/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    json_data = request.get_json()
    if not json_data:
        abort(400, "Not a JSON")
    for key, value in json_data.items():
        if key not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict()), 200
