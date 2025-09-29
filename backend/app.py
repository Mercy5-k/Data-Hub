from flask import Flask
from flask_cors import CORS
from models import db
from schemas import ma
from routes import bp
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")
    
    # Enable CORS
    frontend_url = os.getenv("FRONTEND_URL", "https://data-hdtb3rd3y-mercy5-ks-projects.vercel.app")
    CORS(app, origins=[frontend_url])
    
    # Initialize extensions
    db.init_app(app)
    ma.init_app(app)
    
    # Register blueprints
    app.register_blueprint(bp, url_prefix='/api')
    
    # Create tables
    with app.app_context():
        # Create instance directory if it doesn't exist
        instance_dir = os.path.join(app.root_path, 'instance')
        os.makedirs(instance_dir, exist_ok=True)
        
        # Create uploads directory
        uploads_dir = os.path.join(app.root_path, 'uploads')
        os.makedirs(uploads_dir, exist_ok=True)
        
        db.create_all()
    
    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
