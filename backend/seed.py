from app import app
from models import db, User, File, Tag, Collection, FileTag
from sqlalchemy.exc import IntegrityError


def get_or_create_user(username: str, password: str) -> User:
    user = User.query.filter_by(username=username).first()
    if user:
        return user
    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    return user


def get_or_create_tag(name: str) -> Tag:
    tag = Tag.query.filter_by(name=name).first()
    if tag:
        return tag
    tag = Tag(name=name)
    db.session.add(tag)
    db.session.commit()
    return tag


def create_file(owner: User, filename: str, description: str = "", tag_names=None, added_by=None) -> File:
    f = File(filename=filename, description=description, user_id=owner.id)
    db.session.add(f)
    db.session.flush()  # get id
    tag_names = tag_names or []
    for name in tag_names:
        t = get_or_create_tag(name)
        f.tag_links.append(FileTag(tag=t, added_by=(added_by or owner.id)))
    db.session.commit()
    return f


def create_collection(owner: User, name: str, files=None) -> Collection:
    c = Collection(name=name, user_id=owner.id)
    db.session.add(c)
    db.session.flush()
    files = files or []
    c.files.extend(files)
    db.session.commit()
    return c


def seed():
    with app.app_context():
        # Basic users
        alice = get_or_create_user("alice", "password")
        bob = get_or_create_user("bob", "password")
        carol = get_or_create_user("carol", "password")

        # Common tags
        finance = get_or_create_tag("finance")
        health = get_or_create_tag("health")
        personal = get_or_create_tag("personal")
        data = get_or_create_tag("data")

        # Files
        f1 = File.query.filter_by(filename="q3_report.pdf", user_id=alice.id).first() or create_file(
            owner=alice, filename="q3_report.pdf", description="Q3 financials", tag_names=["finance", "data"], added_by=alice.id
        )
        f2 = File.query.filter_by(filename="insurance.txt", user_id=bob.id).first() or create_file(
            owner=bob, filename="insurance.txt", description="Health insurance notes", tag_names=["health", "personal"], added_by=bob.id
        )
        f3 = File.query.filter_by(filename="resume.docx", user_id=carol.id).first() or create_file(
            owner=carol, filename="resume.docx", description="Updated CV", tag_names=["personal"], added_by=carol.id
        )

        # Collections
        col1 = Collection.query.filter_by(name="Team Finance", user_id=alice.id).first() or create_collection(
            owner=alice, name="Team Finance", files=[f1]
        )
        col2 = Collection.query.filter_by(name="Personal Docs", user_id=bob.id).first() or create_collection(
            owner=bob, name="Personal Docs", files=[f2, f3]
        )
        col3 = Collection.query.filter_by(name="Data Room", user_id=carol.id).first() or create_collection(
            owner=carol, name="Data Room", files=[f1, f2]
        )

        print("Seed complete: users, files, tags, collections populated.")


if __name__ == "__main__":
    seed()
