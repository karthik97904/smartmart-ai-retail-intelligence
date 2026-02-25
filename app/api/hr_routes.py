from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app.utils.decorators import role_required
from app.services.ingestion_service import handle_upload

hr_bp = Blueprint("hr", __name__)


@hr_bp.route("/dashboard")
@login_required
@role_required("HR")
def dashboard():
    return render_template("hr/dashboard.html")


@hr_bp.route("/upload", methods=["GET", "POST"])
@login_required
@role_required("HR")
def upload():
    if request.method == "POST":
        data_type = request.form.get("data_type")
        file = request.files.get("file")

        success, message, row_count = handle_upload(
            file, data_type, current_user.id
        )

        if success:
            flash(f"✅ {message}", "success")
        else:
            flash(f"❌ {message}", "danger")

        return redirect(url_for("hr.upload"))

    return render_template("hr/upload.html")