from flask_marshmallow import Marshmallow
from models import User, Product, Stories, Video, Bubble

ma = Marshmallow()

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product

class StorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Stories

class VideoSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Video

class BubbleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Bubble
