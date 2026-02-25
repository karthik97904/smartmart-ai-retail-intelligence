from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_required
from app.services.auth_service import attempt_login, logout_current_user

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect_by_role(current_user)

    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()
        remember = True if request.form.get("remember") else False

        success, message, user = attempt_login(email, password, remember)

        if success:
            return redirect_by_role(user)
        else:
            flash(message, "danger")

    return render_template("auth/login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_current_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))


def redirect_by_role(user):
    if user.role.name == "CEO":
        return redirect(url_for("ceo.dashboard"))
    elif user.role.name == "HR":
        return redirect(url_for("hr.dashboard"))
    else:
        return redirect(url_for("auth.login"))