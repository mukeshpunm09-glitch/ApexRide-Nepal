"""Public pages + fleet filtering + booking API."""
from datetime import datetime
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, session
from models import db, Vehicle, Booking
from pricing import price_breakdown

main_bp = Blueprint("main", __name__)

def current_user_id():
    return session.get("user_id")

@main_bp.route("/")
def index():
    featured = Vehicle.query.order_by(Vehicle.daily_price.desc()).limit(6).all()
    return render_template("index.html", featured=featured)

@main_bp.route("/fleet")
def fleet():
    q = Vehicle.query
    vtype = request.args.get("type", "")
    trans = request.args.get("transmission", "")
    fuel = request.args.get("fuel", "")
    tier = request.args.get("tier", "")
    search = request.args.get("q", "").strip()
    min_p = request.args.get("min_price", type=int)
    max_p = request.args.get("max_price", type=int)
    if vtype in ("car", "bike", "cycle"):
        q = q.filter_by(category=vtype)
    if trans in ("Automatic", "Manual"):
        q = q.filter_by(transmission=trans)
    if fuel:
        q = q.filter_by(fuel=fuel)
    if tier in ("standard", "luxury"):
        q = q.filter_by(tier=tier)
    if min_p is not None:
        q = q.filter(Vehicle.daily_price >= min_p)
    if max_p is not None:
        q = q.filter(Vehicle.daily_price <= max_p)
    if search:
        q = q.filter((Vehicle.brand.ilike(f"%{search}%")) | (Vehicle.model.ilike(f"%{search}%")) | (Vehicle.location.ilike(f"%{search}%")))
    vehicles = q.order_by(Vehicle.daily_price.asc()).all()
    return render_template("fleet.html", vehicles=vehicles, args=request.args)

@main_bp.route("/vehicle/<int:vehicle_id>")
def vehicle_detail(vehicle_id):
    v = Vehicle.query.get_or_404(vehicle_id)
    related = Vehicle.query.filter(Vehicle.category == v.category, Vehicle.id != v.id).limit(3).all()
    return render_template("vehicle_detail.html", v=v, related=related)

@main_bp.route("/about")
def about():
    return render_template("about.html")

@main_bp.route("/api/calculate", methods=["POST"])
def calculate():
    data = request.get_json(silent=True) or request.form
    try:
        vehicle = Vehicle.query.get(int(data.get("vehicle_id")))
        start = datetime.strptime(str(data.get("start_date")), "%Y-%m-%d").date()
        end = datetime.strptime(str(data.get("end_date")), "%Y-%m-%d").date()
        days = max(1, (end - start).days + 1)
        if not vehicle:
            return jsonify({"error": "Vehicle not found"}), 404
        return jsonify(price_breakdown(vehicle.daily_price, days, vehicle.category, vehicle.tier))
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@main_bp.route("/book/<int:vehicle_id>", methods=["POST"])
def book(vehicle_id):
    if not current_user_id():
        flash("Please log in to book a vehicle.", "warning")
        return redirect(url_for("auth.login"))
    v = Vehicle.query.get_or_404(vehicle_id)
    try:
        start = datetime.strptime(request.form["start_date"], "%Y-%m-%d").date()
        end = datetime.strptime(request.form["end_date"], "%Y-%m-%d").date()
    except Exception:
        flash("Please choose valid pickup and return dates.", "danger")
        return redirect(url_for("main.vehicle_detail", vehicle_id=vehicle_id))
    if end < start:
        flash("Return date must be after pickup date.", "danger")
        return redirect(url_for("main.vehicle_detail", vehicle_id=vehicle_id))
    days = (end - start).days + 1
    bd = price_breakdown(v.daily_price, days, v.category, v.tier)
    b = Booking(user_id=current_user_id(), vehicle_id=v.id, start_date=start, end_date=end,
                days=days, daily_price=v.daily_price, subtotal=bd["subtotal"],
                service_fee=bd["service_fee"], vat=bd["vat"], deposit=bd["deposit"], total=bd["total"])
    db.session.add(b)
    db.session.commit()
    flash(f"Booking confirmed! {v.display_name} for {days} day(s) — Total Rs. {bd['total']:,} + Rs. {bd['deposit']:,} refundable deposit.", "success")
    return redirect(url_for("auth.dashboard"))
