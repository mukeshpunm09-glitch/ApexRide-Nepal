"""Auth: register (Customer/Owner KYC), login, logout, dashboard."""
import os, re
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from werkzeug.utils import secure_filename
from models import db, User, Vehicle, Booking
from pricing import price_breakdown

auth_bp = Blueprint("auth", __name__)
PHONE_RE = re.compile(r"^(98|97)\d{8}$")
ALLOWED_IMG = {"png", "jpg", "jpeg", "webp"}
ALLOWED_VIDEO = {"mp4", "mov", "webm"}

def allowed(name, kinds):
    return "." in name and name.rsplit(".", 1)[1].lower() in kinds

def save_file(field, kinds):
    f = request.files.get(field)
    if f and f.filename and allowed(f.filename, kinds):
        fn = secure_filename(f.filename)
        path = os.path.join(current_app.config["UPLOAD_FOLDER"], fn)
        f.save(path)
        return f"uploads/{fn}"
    return None

def login_required(fn):
    from functools import wraps
    @wraps(fn)
    def wrap(*a, **kw):
        if not session.get("user_id"):
            flash("Please log in first.", "warning")
            return redirect(url_for("auth.login"))
        return fn(*a, **kw)
    return wrap

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        role = request.form.get("role", "customer")
        full_name = request.form.get("full_name", "").strip()
        phone = request.form.get("phone", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        nagarikta = request.form.get("nagarikta_no", "").strip()
        national_id = request.form.get("national_id_no", "").strip()
        licence = request.form.get("licence_no", "").strip()
        if not full_name or not PHONE_RE.match(phone):
            flash("Enter your full name and a valid 10-digit Nepal phone (98xxxxxxxx / 97xxxxxxxx).", "danger")
            return render_template("register.html")
        if User.query.filter_by(email=email).first():
            flash("An account with this email already exists. Please log in.", "danger")
            return render_template("register.html")
        if len(password) < 6:
            flash("Password must be at least 6 characters.", "danger")
            return render_template("register.html")
        if role == "customer" and not (nagarikta or national_id):
            flash("Customers must provide a Nagarikta (Citizenship) Number OR a National ID Number.", "danger")
            return render_template("register.html")
        if role == "owner" and not (nagarikta and national_id):
            flash("Owners must provide BOTH Nagarikta Number AND National ID Number.", "danger")
            return render_template("register.html")
        if role == "customer" and not licence:
            flash("Customers must provide a Driving Licence Number.", "danger")
            return render_template("register.html")
        u = User(role=role, full_name=full_name, phone=phone, email=email,
                 nagarikta_no=nagarikta or None, national_id_no=national_id or None,
                 licence_no=licence or None,
                 licence_photo=save_file("licence_photo", ALLOWED_IMG),
                 selfie_photo=save_file("selfie_photo", ALLOWED_IMG),
                 bluebook_photo=save_file("bluebook_photo", ALLOWED_IMG),
                 walkaround_video=save_file("walkaround_video", ALLOWED_VIDEO),
                 verification_status="Pending")
        u.set_password(password)
        db.session.add(u)
        db.session.commit()
        session["user_id"] = u.id
        session["user_name"] = u.full_name
        session["user_role"] = u.role
        flash(f"Welcome to ApexRide Nepal, {u.full_name}! Your KYC verification is Pending — our team will review your documents within 24 hours.", "success")
        return redirect(url_for("auth.dashboard"))
    return render_template("register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        u = User.query.filter_by(email=email).first()
        if u and u.check_password(request.form.get("password", "")):
            session["user_id"] = u.id
            session["user_name"] = u.full_name
            session["user_role"] = u.role
            flash(f"Welcome back, {u.full_name}!", "success")
            return redirect(url_for("auth.dashboard"))
        flash("Invalid email or password.", "danger")
    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("main.index"))

@auth_bp.route("/dashboard")
@login_required
def dashboard():
    u = User.query.get(session["user_id"])
    bookings = Booking.query.filter_by(user_id=u.id).order_by(Booking.created_at.desc()).all()
    my_vehicles = Vehicle.query.filter_by(owner_id=u.id).all()
    earnings = 0
    for b in Booking.query.join(Vehicle, Booking.vehicle_id == Vehicle.id).filter(Vehicle.owner_id == u.id).all():
        earnings += b.total
    return render_template("dashboard.html", user=u, bookings=bookings, my_vehicles=my_vehicles, earnings=earnings)
