from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.ext.associationproxy import association_proxy


db = SQLAlchemy()

class FileTag(db.Model):
    __tablename__ = 'file_tags'

    file_id = db.Column(db.Integer, db.ForeignKey('files.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)
    added_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    file = db.relationship('File', back_populates='tag_links')
    tag = db.relationship('Tag', back_populates='file_links')

# Association table between Collection and File
collection_files = db.Table(
    'collection_files',
    db.Column('collection_id', db.Integer, db.ForeignKey('collections.id'), primary_key=True),
    db.Column('file_id', db.Integer, db.ForeignKey('files.id'), primary_key=True),
)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    files = db.relationship('File', backref='user', lazy=True, cascade="all, delete-orphan")
    collections = db.relationship('Collection', backref='user', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.username}>"


class File(db.Model):
    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    path = db.Column(db.String(512), nullable=True)  # local storage path for MVP
    url = db.Column(db.String(512), nullable=True)
    description = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Association object pattern for tags
    tag_links = db.relationship('FileTag', back_populates='file', cascade="all, delete-orphan")
    tags = association_proxy('tag_links', 'tag', creator=lambda tag: FileTag(tag=tag))

    def __repr__(self):
        return f"<File {self.filename}>"


class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    file_links = db.relationship('FileTag', back_populates='tag', cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Tag {self.name}>"


class Collection(db.Model):
    __tablename__ = 'collections'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    files = db.relationship('File', secondary=collection_files, backref=db.backref('collections', lazy='dynamic'))

    def __repr__(self):
        return f"<Collection {self.name}>"
