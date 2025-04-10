import hashlib

from app import db
from app.models import User, Web


def user_exists(username):
    return db.session.query(User).filter_by(username=username).first() is not None


def create_user(name, username, password):  # Da test
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())  # Bâm mật khẩu
    new_user = User(name=name, username=username, password=password)
    db.session.add(new_user)
    db.session.commit()


def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    users = User.query.filter(User.username.__eq__(username.strip()),
                              User.password.__eq__(password.strip()))

    return users.first()


def get_user_by_id(user_id):
    return User.query.get(user_id)


def get_webs_by_user(user_id):
    return Web.query.filter_by(user_id=user_id).all()


def create_web(name, url, user_id):
    new_web = Web(name=name, url=url, user_id=user_id)

    # Thêm vào cơ sở dữ liệu
    db.session.add(new_web)
    db.session.commit()