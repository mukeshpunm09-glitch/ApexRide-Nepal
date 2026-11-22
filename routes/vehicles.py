"""Owner vehicle listing — multi-step wizard, 7 photos, rigid pricing."""
import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from werkzeug.utils import secure_filename
from models import db, Vehicle
from pricing import get_daily_price, validate_price, deposit_for
from routes.auth import login_required, ALLOWED_IMG, ALLOWED_VIDEO

veh_bp = Blueprint("vehicles", __name__)
PHOTO_LABELS = ["Front Exterior", "Rear Exterior", "Side Profile Left", "Side Profile Right",
                "Interior Cockpit & Dashboard", "Interior Rear Seats", "Boot / Engine Compartment"]

@veh_bp.route("/list-vehicle", methods=["GET", "POST"])
@login_required
def list_vehicle():
    if session.get("user_role") != "owner":
        flash("Only Vehicle Owners can list a vehicle. Register as an Owner (List & Earn) to continue.", "warning")
        return redirect(url_for("auth.register"))
    if request.method == "POST":
        category = request.form.get("category", "")
        tier = request.form.get("tier", "")
        try:
            daily_price = int(request.form.get("daily_price", 0))
        except ValueError:
            daily_price = 0
        expected = get_daily_price(category, tier)
        if expected is None:
            flash("Choose a valid category and tier.", "danger")
            return render_template("list_vehicle.html", labels=PHOTO_LABELS)
        if not validate_price(category, tier, daily_price):
            flash(f"Price mismatch: {category.title()} / {tier.title()} must be Rs. {expected:,}/day. Submitted Rs. {daily_price:,}. Price is locked by ApexRide policy.", "danger")
            return render_template("list_vehicle.html", labels=PHOTO_LABELS)
        if not request.form.get("return_policy"):
            flash("You must accept the Return Policy (fuel replacement, damage deposit, return inspection).", "danger")
            return render_template("list_vehicle.html", labels=PHOTO_LABELS)
        photos = []
        for i in range(1, 8):
            f = request.files.get(f"photo_{i}")
            if f and f.filename and "." in f.filename and f.filename.rsplit(".", 1)[1].lower() in ALLOWED_IMG:
                fn = secure_filename(f"v_{session['user_id']}_{i}_{f.filename}")
                f.save(os.path.join(current_app.config["UPLOAD_FOLDER"], fn))
                photos.append(f"uploads/{fn}")
            else:
                photos.append("")
        # Require at least the front photo; missing slots fall back to a placeholder image
        if not photos[0]:
            flash("Please upload at least the Front Exterior photo (Photo 1). All 7 slots are required for a complete listing.", "danger")
            return render_template("list_vehicle.html", labels=PHOTO_LABELS)
        video_path = None
        vf = request.files.get("walkaround_video")
        if vf and vf.filename and "." in vf.filename and vf.filename.rsplit(".", 1)[1].lower() in ALLOWED_VIDEO:
            fn = secure_filename(f"walk_{session['user_id']}_{vf.filename}")
            vf.save(os.path.join(current_app.config["UPLOAD_FOLDER"], fn))
            video_path = f"uploads/{fn}"
        v = Vehicle(
            brand=request.form.get("brand", "").strip(), model=request.form.get("model", "").strip(),
            year=int(request.form.get("year", 2023)), mileage_km=int(request.form.get("mileage_km", 0) or 0),
            transmission=request.form.get("transmission", "Automatic"), fuel=request.form.get("fuel", "Petrol"),
            category=category, tier=tier, cc=int(request.form.get("cc", 0) or 0),
            seats=int(request.form.get("seats", 5) or 5), daily_price=expected,
            deposit=deposit_for(category, tier), location=request.form.get("location", "Kathmandu"),
            description=request.form.get("description", ""), video=video_path,
            owner_id=session["user_id"], status="Available")
        # Fill any empty photo slots with the cover image so the 7-photo gallery always renders
        cover = photos[0]
        v.photos = [p or cover for p in photos]
        db.session.add(v)
        db.session.commit()
        flash(f"Your {v.display_name} is listed at Rs. {expected:,}/day! It will appear in the fleet once verified.", "success")
        return redirect(url_for("auth.dashboard"))
    return render_template("list_vehicle.html", labels=PHOTO_LABELS)
