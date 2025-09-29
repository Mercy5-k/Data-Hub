from flask import Flask
from flask_cors import CORS
from models import db
from routes import bp
import os
from sqlalchemy import text
from flask_migrate import Migrate


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object("config.Config")

    # Ensure instance folder exists
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass

    CORS(app)
    db.init_app(app)
    Migrate(app, db)

    # Register blueprints
    app.register_blueprint(bp, url_prefix="/api")

    # Create tables if not exists (dev convenience) and run light migrations for SQLite
    with app.app_context():
        db.create_all()

        # Lightweight migration: ensure file_tags.created_at exists (older DBs won't have it)
        try:
            engine = db.engine
            with engine.connect() as conn:
                # Check existing columns
                result = conn.execute(text("PRAGMA table_info(file_tags)"))
                cols = {row[1] for row in result}  # row[1] is column name
                if 'created_at' not in cols:
                    conn.execute(text("ALTER TABLE file_tags ADD COLUMN created_at DATETIME"))
        except Exception:
            # Best-effort; ignore if database is not SQLite or alterations are unsupported
            pass

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
