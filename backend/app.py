from flask import Flask, jsonify     
from flask_cors import CORS
from models import db
from schemas import ma
from routes import bp
import os

def create_app():
    app = Flask(__name__)
    # ✅ corrected module path for config
    app.config.from_object("backend.config.Config")

    # Enable CORS
    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
    allowed_origins = [
        frontend_url,
        "https://data-hdtb3rd3y-mercy5-ks-projects.vercel.app",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]
    CORS(app, origins=allowed_origins, supports_credentials=True)

    # Initialize extensions
    db.init_app(app)
    ma.init_app(app)

    # Register blueprints
    app.register_blueprint(bp, url_prefix="/api")

    # Root route
    @app.route("/")
    def root():
        return jsonify({
            "message": "Data Hub API is running",
            "version": "1.0.0",
            "endpoints": {
                "health": "/api/health",
                "files": "/api/files",
                "collections": "/api/collections",
                "tags": "/api/tags",
                "users": "/api/users",
            },
        })

    # Create tables & ensure folders exist
    with app.app_context():
        instance_dir = os.path.join(app.root_path, "instance")
        os.makedirs(instance_dir, exist_ok=True)

        uploads_dir = os.path.join(app.root_path, "uploads")
        os.makedirs(uploads_dir, exist_ok=True)

        db.create_all()

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
