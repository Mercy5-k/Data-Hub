from flask_marshmallow import Marshmallow
from marshmallow import fields
from models import User, File, Tag, Collection, FileTag

ma = Marshmallow()


class TagSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Tag
        include_fk = True
        load_instance = True


class FileTagSchema(ma.SQLAlchemyAutoSchema):
    tag = fields.Nested(TagSchema(only=("id", "name")))

    class Meta:
        model = FileTag
        include_fk = True
        load_instance = True


class FileSchema(ma.SQLAlchemyAutoSchema):
    tags = fields.List(fields.Nested(TagSchema))
    # Expose association object details
    tags_with_meta = fields.List(fields.Nested(FileTagSchema), attribute='tag_links')

    class Meta:
        model = File
        include_fk = True
        load_instance = True


class CollectionSchema(ma.SQLAlchemyAutoSchema):
    files = fields.List(fields.Nested(FileSchema(only=("id", "filename"))))

    class Meta:
        model = Collection
        include_fk = True
        load_instance = True


class UserSchema(ma.SQLAlchemyAutoSchema):
    files = fields.List(fields.Nested(FileSchema(only=("id", "filename"))))
    collections = fields.List(fields.Nested(CollectionSchema(only=("id", "name"))))

    class Meta:
        model = User
        load_instance = True
        exclude = ("password",)
