from app.models.user import User
from app.models.role import Role
from app.extensions import db


def get_user_by_email(email: str):
    return User.query.filter_by(email=email).first()


def get_user_by_id(user_id: int):
    return User.query.get(user_id)


def get_role_by_name(name: str):
    return Role.query.filter_by(name=name).first()


def create_role(name: str, description: str):
    role = Role(name=name, description=description)
    db.session.add(role)
    db.session.commit()
    return role


def create_user(full_name: str, email: str, password: str, role_id: int):
    user = User(full_name=full_name, email=email, role_id=role_id)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user