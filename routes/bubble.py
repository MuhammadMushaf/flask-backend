from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import db, Bubble
from schemas import BubbleSchema

bubbles_bp = Blueprint('bubbles', __name__)
bubble_schema = BubbleSchema()
bubble_list_schema = BubbleSchema(many=True)

# Get all bubbles
@bubbles_bp.route('/bubbles', methods=['GET'])
@jwt_required()
def get_bubbles():
    bubbles = Bubble.query.all()
    return jsonify(bubble_list_schema.dump(bubbles)), 200

# Create a new bubble
@bubbles_bp.route('/bubbles', methods=['POST'])
@jwt_required()
def create_bubble():
    data = request.get_json()
    bubble = Bubble(**data)
    db.session.add(bubble)
    db.session.commit()
    return jsonify(bubble_schema.dump(bubble)), 201
