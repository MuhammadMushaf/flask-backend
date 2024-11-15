from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import db, Stories
from schemas import StorySchema

stories_bp = Blueprint('stories', __name__)
stories_schema = StorySchema()
stories_list_schema = StorySchema(many=True)

# Get all stories
@stories_bp.route('/stories', methods=['GET'])
@jwt_required()
def get_stories():
    stories = Stories.query.all()
    return jsonify(stories_list_schema.dump(stories)), 200

# Create a new story
@stories_bp.route('/stories', methods=['POST'])
@jwt_required()
def create_story():
    data = request.get_json()
    story = Stories(**data)
    db.session.add(story)
    db.session.commit()
    return jsonify(stories_schema.dump(story)), 201

# Update a story
@stories_bp.route('/stories/<int:id>', methods=['PUT'])
@jwt_required()
def update_story(id):
    story = Stories.query.get(id)
    if not story:
        return jsonify({"msg": "Story not found"}), 404
    data = request.get_json()
    story.title = data.get('title', story.title)
    story.description = data.get('description', story.description)
    db.session.commit()
    return jsonify(stories_schema.dump(story)), 200

# Delete a story
@stories_bp.route('/stories/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_story(id):
    story = Stories.query.get(id)
    if not story:
        return jsonify({"msg": "Story not found"}), 404
    db.session.delete(story)
    db.session.commit()
    return jsonify({"msg": "Story deleted"}), 200
