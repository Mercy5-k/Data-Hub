from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from models import db, User, File, Tag, Collection, FileTag
from schemas import ma, UserSchema, FileSchema, TagSchema, CollectionSchema
import os

bp = Blueprint('api', __name__)

# Initialize Marshmallow with app context later in app factory


@bp.record
def record_params(setup_state):
    app = setup_state.app
    ma.init_app(app)


# Auth endpoints (simple MVP, not secure for production)
@bp.post('/register')
def register():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify({"error": "username and password required"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "username already exists"}), 409

    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    return UserSchema().jsonify(user), 201


@bp.post('/login')
def login():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username, password=password).first()
    if not user:
        return jsonify({"error": "invalid credentials"}), 401
    return UserSchema().jsonify(user), 200


# Basic reads for Users and Tags; create Tag
@bp.get('/users')
def list_users():
    users = User.query.order_by(User.created_at.asc()).all()
    return UserSchema(many=True).jsonify(users), 200


@bp.get('/tags')
def list_tags():
    tags = Tag.query.order_by(Tag.name.asc()).all()
    return TagSchema(many=True).jsonify(tags), 200


@bp.post('/tags')
def create_tag():
    data = request.get_json() or {}
    name = (data.get('name') or '').strip()
    if not name:
        return jsonify({"error": "name is required"}), 400
    existing = Tag.query.filter_by(name=name).first()
    if existing:
        return TagSchema().jsonify(existing), 200
    tag = Tag(name=name)
    db.session.add(tag)
    db.session.commit()
    return TagSchema().jsonify(tag), 201


# Files CRUD
@bp.get('/files')
def list_files():
    files = File.query.order_by(File.created_at.desc()).all()
    return FileSchema(many=True).jsonify(files), 200


@bp.post('/files')
def create_file():
    # Support multipart form for upload or JSON for metadata-only
    user_id = request.form.get('user_id') or (request.json or {}).get('user_id')
    description = request.form.get('description') or (request.json or {}).get('description')
    tags = request.form.get('tags')  # comma-separated string for MVP
    json_payload = request.get_json(silent=True) or {}
    tags_list = json_payload.get('tags') if isinstance(json_payload, dict) else None  # optional list[str]
    tags_with_meta = json_payload.get('tags_with_meta') if isinstance(json_payload, dict) else None  # optional list[obj]

    if not user_id:
        return jsonify({"error": "user_id is required"}), 400

    file_record = File(filename="", user_id=int(user_id), description=description)

    # Handle file upload if present
    upload_folder = os.path.join(current_app.instance_path, 'uploads')
    os.makedirs(upload_folder, exist_ok=True)

    uploaded = None
    if 'file' in request.files:
        uploaded = request.files['file']
        if uploaded.filename:
            filename = secure_filename(uploaded.filename)
            save_path = os.path.join(upload_folder, filename)
            uploaded.save(save_path)
            file_record.filename = filename
            file_record.path = save_path
            file_record.url = None
    else:
        # JSON payload with filename only
        json_data = json_payload or {}
        filename = json_data.get('filename')
        if not filename:
            return jsonify({"error": "filename or file upload is required"}), 400
        file_record.filename = filename

    # Tags handling
    # Preferred: tags_with_meta overrides others
    if tags_with_meta and isinstance(tags_with_meta, list):
        for item in tags_with_meta:
            if not isinstance(item, dict):
                continue
            name = (item.get('name') or '').strip()
            if not name:
                continue
            added_by = item.get('added_by')
            tag = Tag.query.filter_by(name=name).first()
            if not tag:
                tag = Tag(name=name)
            file_record.tag_links.append(FileTag(tag=tag, added_by=added_by))
    else:
        # Fallbacks: list of tag names or comma string
        names = []
        if isinstance(tags_list, list):
            names.extend([str(x).strip() for x in tags_list if str(x).strip()])
        if tags:
            names.extend([t.strip() for t in tags.split(',') if t.strip()])
        for name in names:
            tag = Tag.query.filter_by(name=name).first()
            if not tag:
                tag = Tag(name=name)
            file_record.tags.append(tag)

    db.session.add(file_record)
    db.session.commit()

    return FileSchema().jsonify(file_record), 201


@bp.get('/files/<int:file_id>')
def get_file(file_id):
    f = File.query.get_or_404(file_id)
    return FileSchema().jsonify(f), 200


@bp.patch('/files/<int:file_id>')
def update_file(file_id):
    f = File.query.get_or_404(file_id)
    data = request.get_json() or {}
    if 'filename' in data:
        f.filename = data['filename']
    if 'description' in data:
        f.description = data['description']
    # tags_with_meta takes precedence if provided
    if 'tags_with_meta' in data and isinstance(data['tags_with_meta'], list):
        f.tag_links.clear()
        for item in data['tags_with_meta']:
            if not isinstance(item, dict):
                continue
            name = (item.get('name') or '').strip()
            if not name:
                continue
            added_by = item.get('added_by')
            tag = Tag.query.filter_by(name=name).first()
            if not tag:
                tag = Tag(name=name)
            f.tag_links.append(FileTag(tag=tag, added_by=added_by))
    elif 'tags' in data and isinstance(data['tags'], list):
        f.tags.clear()
        for name in data['tags']:
            tag = Tag.query.filter_by(name=name).first()
            if not tag:
                tag = Tag(name=name)
            f.tags.append(tag)
    db.session.commit()
    return FileSchema().jsonify(f), 200


@bp.delete('/files/<int:file_id>')
def delete_file(file_id):
    f = File.query.get_or_404(file_id)
    db.session.delete(f)
    db.session.commit()
    return jsonify({"message": "deleted"}), 204


# Collections GET/POST
@bp.get('/collections')
def list_collections():
    collections = Collection.query.order_by(Collection.created_at.desc()).all()
    return CollectionSchema(many=True).jsonify(collections), 200


@bp.post('/collections')
def create_collection():
    data = request.get_json() or {}
    name = data.get('name')
    user_id = data.get('user_id')
    file_ids = data.get('file_ids', [])

    if not name or not user_id:
        return jsonify({"error": "name and user_id are required"}), 400

    col = Collection(name=name, user_id=int(user_id))
    if file_ids:
        files = File.query.filter(File.id.in_(file_ids)).all()
        col.files.extend(files)

    db.session.add(col)
    db.session.commit()

    return CollectionSchema().jsonify(col), 201


@bp.get('/collections/<int:collection_id>')
def get_collection(collection_id):
    col = Collection.query.get_or_404(collection_id)
    return CollectionSchema().jsonify(col), 200


@bp.patch('/collections/<int:collection_id>')
def update_collection(collection_id):
    col = Collection.query.get_or_404(collection_id)
    data = request.get_json() or {}
    if 'name' in data:
        col.name = data['name']
    if 'file_ids' in data and isinstance(data['file_ids'], list):
        # Replace collection files with provided list
        col.files.clear()
        if data['file_ids']:
            files = File.query.filter(File.id.in_(data['file_ids'])).all()
            col.files.extend(files)
    db.session.commit()
    return CollectionSchema().jsonify(col), 200


@bp.delete('/collections/<int:collection_id>')
def delete_collection(collection_id):
    col = Collection.query.get_or_404(collection_id)
    db.session.delete(col)
    db.session.commit()
    return jsonify({"message": "deleted"}), 204
