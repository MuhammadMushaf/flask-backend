from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import db, Stories, StoryType, Video
from services.mux_service import upload_video
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
    data = request.form  # For mixed data and file input
    video_file = request.files.get('video_file')  # Retrieve the video file

    # Validate required fields
    if not data.get('title') or not data.get('type'):
        return jsonify({"message": "Title and type are required"}), 400
    if not video_file:
        return jsonify({"message": "Video file is required"}), 400

    # Step 1: Upload video to Mux
    try:
        
        mux_response = upload_video(video_file)
        playback_id = mux_response.get('playback_id')
        video_url = mux_response.get('video_url')
    except Exception as e:
        return jsonify({"message": "Failed to upload video to Mux", "error": str(e)}), 500

    # Step 2: Save video details in Videos table
    video = Video(playback_id=playback_id, video_url=video_url)
    db.session.add(video)
    db.session.commit()

    # Step 3: Create the story
    story = Stories(
        title=data['title'],
        description=data.get('description'),
        type=data['type'],
        video_id=video.id  # Link the video ID
    )

    # Step 4: Validate and set fields based on story type
    if story.type == 'shoppable':
        if not isinstance(data.getlist('product_ids[]'), list) or not data.getlist('product_ids[]'):
            return jsonify({"message": "Product IDs must be a non-empty array for shoppable stories"}), 400
        story.product_ids = data.getlist('product_ids[]')  # Parse product IDs as a list
    elif story.type == 'cta':
        if not data.get('cta_text') or not data.get('cta_link'):
            return jsonify({"message": "CTA stories require cta_text and cta_link"}), 400
        story.cta_text = data['cta_text']
        story.cta_link = data['cta_link']
    else:
        return jsonify({"message": "Invalid story type"}), 400

    # Step 5: Save the story
    db.session.add(story)
    db.session.commit()

    return jsonify({"message": "Story created successfully", "story": story.id}), 201


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
