from datetime import datetime
from flask import current_app
from flask_login import login_user, logout_user
from app.repositories.user_repo import get_user_by_email
from app import db


def attempt_login(email: str, password: str, remember: bool = False):
    if not email or not password:
        return False, "Email and password are required.", None

    user = get_user_by_email(email)

    if not user:
        current_app.logger.warning(f"Login failed - user not found: {email}")
        return False, "Invalid email or password.", None

    if not user.is_active:
        current_app.logger.warning(f"Login failed - inactive user: {email}")
        return False, "Your account is disabled. Contact admin.", None

    if not user.check_password(password):
        current_app.logger.warning(f"Login failed - wrong password: {email}")
        return False, "Invalid email or password.", None

    user.last_login = datetime.utcnow()
    db.session.commit()

    login_user(user, remember=remember)
    current_app.logger.info(f"Login success: {email} | Role: {user.role.name}")
    return True, "Login successful.", user


def logout_current_user():
    logout_user()