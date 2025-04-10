from sqlalchemy.orm import relationship

from app import app as my_app, db
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, ForeignKey


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    username = Column(String(225), nullable=False, unique=True)
    password = Column(String(50), nullable=False)

    # Thiết lập quan hệ một-nhiều với bảng Web
    web = relationship('Web', backref='user', lazy=True)

    def __str__(self):
        return self.name  # Chỉnh sửa từ self.ten thành self.name


class Web(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)  # Nên thêm nullable=False để bắt buộc phải có IP
    url = Column(String(255), nullable=False)  # Nên thêm nullable=False để bắt buộc phải có IP
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)  # Sửa key đối chiếu với table name

    def __str__(self):
        return f"Web {self.id} (IP: {self.ip})"



if __name__ == "__main__":
    with my_app.app_context():

        # db.drop_all()
        db.create_all()

        db.session.commit()