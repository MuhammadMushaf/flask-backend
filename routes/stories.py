# from flask import Blueprint, request, jsonify
# from flask_jwt_extended import jwt_required
# from models import db, Stories, StoryType, Video
# from services.mux_service import upload_video
# from schemas import StorySchema

# stories_bp = Blueprint('stories', __name__)
# stories_schema = StorySchema()
# stories_list_schema = StorySchema(many=True)

# # Get all stories
# @stories_bp.route('/stories', methods=['GET'])
# @jwt_required()
# def get_stories():
#     stories = Stories.query.all()
#     return jsonify(stories_list_schema.dump(stories)), 200

# # Create a new story
# @stories_bp.route('/stories', methods=['POST'])
# @jwt_required()
# def create_story():
#     data = request.form  # For mixed data and file input
#     video_file = request.files.get('video_file')  # Retrieve the video file

#     # Validate required fields
#     if not data.get('title') or not data.get('type'):
#         return jsonify({"message": "Title and type are required"}), 400
#     if not video_file:
#         return jsonify({"message": "Video file is required"}), 400

#     # Step 1: Upload video to Mux
#     try:
        
#         mux_response = upload_video(video_file)
#         playback_id = mux_response.get('playback_id')
#         video_url = mux_response.get('video_url')
#     except Exception as e:
#         return jsonify({"message": "Failed to upload video to Mux", "error": str(e)}), 500

#     # Step 2: Save video details in Videos table
#     video = Video(mux_playback_id=playback_id, video_url=video_url)
#     db.session.add(video)
#     db.session.commit()

#     # Step 3: Create the story
#     story = Stories(
#         title=data['title'],
#         description=data.get('description'),
#         type=data['type'],
#         video_id=video.id  # Link the video ID
#     )

#     # Step 4: Validate and set fields based on story type
#     if story.type == 'shoppable':
#         if not isinstance(data.getlist('product_ids[]'), list) or not data.getlist('product_ids[]'):
#             return jsonify({"message": "Product IDs must be a non-empty array for shoppable stories"}), 400
#         story.product_ids = data.getlist('product_ids[]')  # Parse product IDs as a list
#     elif story.type == 'cta':
#         if not data.get('cta_text') or not data.get('cta_link'):
#             return jsonify({"message": "CTA stories require cta_text and cta_link"}), 400
#         story.cta_text = data['cta_text']
#         story.cta_link = data['cta_link']
#     else:
#         return jsonify({"message": "Invalid story type"}), 400

#     # Step 5: Save the story
#     db.session.add(story)
#     db.session.commit()

#     return jsonify({"message": "Story created successfully", "story": story.id}), 201


# # Update a story
# @stories_bp.route('/stories/<int:id>', methods=['PUT'])
# @jwt_required()
# def update_story(id):
#     story = Stories.query.get(id)
#     if not story:
#         return jsonify({"msg": "Story not found"}), 404
#     data = request.get_json()
#     story.title = data.get('title', story.title)
#     story.description = data.get('description', story.description)
#     db.session.commit()
#     return jsonify(stories_schema.dump(story)), 200

# # Delete a story
# @stories_bp.route('/stories/<int:id>', methods=['DELETE'])
# @jwt_required()
# def delete_story(id):
#     story = Stories.query.get(id)
#     if not story:
#         return jsonify({"msg": "Story not found"}), 404
#     db.session.delete(story)
#     db.session.commit()
#     return jsonify({"msg": "Story deleted"}), 200




from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from models import Product, db, Stories, Video
from services.mux_service import  create_upload_url, get_asset_id, get_playback_id, upload_video
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
# @stories_bp.route('/stories', methods=['POST'])
# @jwt_required()
# def create_story():
#     data = request.form  # For mixed data and file input
#     video_file = request.files.get('video_file')  # Retrieve the video file

#     # Validate required fields
#     if not data.get('title') or not data.get('type'):
#         return jsonify({"message": "Title and type are required"}), 400
#     if not video_file:
#         return jsonify({"message": "Video file is required"}), 400

#     # Step 1: Upload video to Mux
#     try:
#         mux_response = upload_video(video_file)
#         playback_id = mux_response.get('playback_id')
#         video_url = mux_response.get('video_url')
#     except Exception as e:
#         return jsonify({"message": "Failed to upload video to Mux", "error": str(e)}), 500

#     # Step 2: Save video details in Videos table
#     video = Video(mux_playback_id=playback_id, url=video_url)
#     db.session.add(video)
#     db.session.commit()

#     # Step 3: Create the story
#     story = Stories(
#         title=data['title'],
#         description=data.get('description'),
#         type=data['type'],
#         video=video  # Link the video to the story
#     )

#     # Step 4: Handle the `shoppable` and `cta` types with their respective fields
#     if story.type == 'shoppable':
#         # Validate that product_ids[] is a list and not empty
#         product_ids = data.getlist('product_ids[]')
#         if not isinstance(product_ids, list) or not product_ids:
#             return jsonify({"message": "Product IDs must be a non-empty array for shoppable stories"}), 400
        
#         # Assuming you have a `Product` model and a many-to-many relationship with `Story`
#         products = Product.query.filter(Product.id.in_(product_ids)).all()
#         if len(products) != len(product_ids):  # Ensure all product_ids exist
#             return jsonify({"message": "Some product IDs are invalid"}), 400
        
#         # Link the products to the story (assuming a many-to-many relationship between `Product` and `Story`)
#         story.products = products
#     elif story.type == 'cta':
#         # Validate CTA-related fields
#         if not data.get('cta_text') or not data.get('cta_link'):
#             return jsonify({"message": "CTA stories require cta_text and cta_link"}), 400
#         story.cta_text = data['cta_text']
#         story.cta_link = data['cta_link']
#     else:
#         return jsonify({"message": "Invalid story type"}), 400

#     # Step 5: Save the story
#     db.session.add(story)
#     db.session.commit()

#     return jsonify({"message": "Story created successfully", "story": story.id}), 201


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
        upload_url,upload_id=create_upload_url()
        print(upload_url,upload_id, "hello 1234")
        # upload_response
        if upload_url:
        # Upload the video
            upload_video(upload_url, video_file)
            print("hello",upload_id)
            # if upload_response:
            # asset_id = upload_response.get("data", {}).get("id")
            asset_id=get_asset_id(upload_id)
            print("assset Id",asset_id)
            print("uplaod response", upload_url)

            if asset_id:
                    # Get the playback ID
                get_playback_id(asset_id)
        # mux_response = upload_video_from_api(video_file)
        playback_id = ""
        video_url = ""
        # print(mux_response)

        if not playback_id or not video_url:
            raise ValueError("Failed to receive valid playback_id or video_url from Mux")
    except Exception as e:
        return jsonify({"message": "Failed to upload video to Mux", "error": str(e)}), 500

    # Step 2: Save video details in Videos table
    try:
        video = Video(mux_playback_id=playback_id, url=video_url)
        db.session.add(video)
        db.session.commit()  # Commit the video insert
        db.session.remove()  # Remove session to free resources
    except Exception as e:
        db.session.rollback()  # Rollback in case of error
        return jsonify({"message": "Failed to save video details", "error": str(e)}), 500

    # Step 3: Create the story
    try:
        story = Stories(
            title=data['title'],
            description=data.get('description'),
            type=data['type'],
            video=video  # Link the video to the story
        )

        # Handle the `shoppable` and `cta` types with their respective fields
        if story.type == 'shoppable':
            product_ids = data.getlist('product_ids[]')
            if not product_ids:
                return jsonify({"message": "Product IDs are required for shoppable stories"}), 400
            products = Product.query.filter(Product.id.in_(product_ids)).all()
            if len(products) != len(product_ids):
                return jsonify({"message": "Some product IDs are invalid"}), 400
            story.products = products
        elif story.type == 'cta':
            if not data.get('cta_text') or not data.get('cta_link'):
                return jsonify({"message": "CTA stories require cta_text and cta_link"}), 400
            story.cta_text = data['cta_text']
            story.cta_link = data['cta_link']
        else:
            return jsonify({"message": "Invalid story type"}), 400

        # Step 4: Save the story
        db.session.add(story)
        db.session.commit()  # Commit the story insert
        db.session.remove()  # Remove session to free resources

        return jsonify({"message": "Story created successfully", "story": story.id}), 201

    except Exception as e:
        db.session.rollback()  # Rollback in case of error
        return jsonify({"message": "Failed to create story", "error": str(e)}), 500

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

    # Optional: Update related fields for shoppable and CTA stories
    if story.type == 'shoppable':
        story.product_ids = data.get('product_ids', story.product_ids)
    elif story.type == 'cta':
        story.cta_text = data.get('cta_text', story.cta_text)
        story.cta_link = data.get('cta_link', story.cta_link)

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
