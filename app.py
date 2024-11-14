from flask import Flask
from models import db
from config import Config
from flask_jwt_extended import JWTManager

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    JWTManager(app)
    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
