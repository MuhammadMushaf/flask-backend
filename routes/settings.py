from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import db, Settings
from schemas import SettingsSchema

settings_bp = Blueprint('settings', __name__)
settings_schema = SettingsSchema()
settings_list_schema = SettingsSchema(many=True)

# Get all settings
@settings_bp.route('/settings', methods=['GET'])
@jwt_required()
def get_settings():
    settings = Settings.query.all()
    return jsonify(settings_list_schema.dump(settings)), 200

# Create a new setting
@settings_bp.route('/settings', methods=['POST'])
@jwt_required()
def create_setting():
    data = request.get_json()
    setting = Settings(**data)
    db.session.add(setting)
    db.session.commit()
    return jsonify(settings_schema.dump(setting)), 201
