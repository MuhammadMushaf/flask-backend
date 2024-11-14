from app import create_app
from routes.auth import auth_bp
from models import db

app = create_app()

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix='/api')

# Create database tables if they don't exist
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
