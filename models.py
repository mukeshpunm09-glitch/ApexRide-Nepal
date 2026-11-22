"""SQLAlchemy models for ApexRide Nepal."""
from datetime import datetime
import json
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(20), nullable=False, default="customer")  # customer | owner
    full_name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(15), nullable=False)  # 10-digit Nepal format
    email = db.Column(db.String(160), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    nagarikta_no = db.Column(db.String(60))
    national_id_no = db.Column(db.String(60))
    licence_no = db.Column(db.String(60))
    licence_photo = db.Column(db.String(255))
    selfie_photo = db.Column(db.String(255))
    bluebook_photo = db.Column(db.String(255))
    walkaround_video = db.Column(db.String(255))
    verification_status = db.Column(db.String(20), default="Pending")  # Pending | Approved
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    vehicles = db.relationship("Vehicle", backref="owner", lazy=True)
    bookings = db.relationship("Booking", backref="user", lazy=True)

    def set_password(self, pw):
        self.password_hash = generate_password_hash(pw)

    def check_password(self, pw):
        return check_password_hash(self.password_hash, pw)


class Vehicle(db.Model):
    __tablename__ = "vehicles"
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(80), nullable=False)
    model = db.Column(db.String(120), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    mileage_km = db.Column(db.Integer, nullable=False, default=0)
    transmission = db.Column(db.String(20), nullable=False)  # Automatic | Manual
    fuel = db.Column(db.String(20), nullable=False)          # Petrol | Diesel | Electric | Hybrid
    category = db.Column(db.String(20), nullable=False)      # cycle | bike | car
    tier = db.Column(db.String(20), nullable=False)          # standard | luxury
    cc = db.Column(db.Integer, default=0)
    seats = db.Column(db.Integer, default=2)
    daily_price = db.Column(db.Integer, nullable=False)  # enforced vs pricing.PRICE_MAP
    deposit = db.Column(db.Integer, nullable=False, default=15000)
    location = db.Column(db.String(120), default="Kathmandu")
    description = db.Column(db.Text, default="")
    _photos = db.Column("photos", db.Text, default="[]")  # JSON list of 7 URLs/paths
    video = db.Column(db.String(255))
    status = db.Column(db.String(20), default="Available")
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    bookings = db.relationship("Booking", backref="vehicle", lazy=True)

    @property
    def photos(self):
        try:
            return json.loads(self._photos or "[]")
        except Exception:
            return []

    @photos.setter
    def photos(self, value):
        self._photos = json.dumps(list(value or []))

    @property
    def cover(self):
        p = self.photos
        return p[0] if p else "https://images.unsplash.com/photo-1503376780353-7e6692767b70?q=80&w=1200&auto=format&fit=crop"

    @property
    def display_name(self):
        return f"{self.brand} {self.model}"

    def price_label(self):
        return f"Rs. {self.daily_price:,}/day"


class Booking(db.Model):
    __tablename__ = "bookings"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey("vehicles.id"), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    days = db.Column(db.Integer, nullable=False)
    daily_price = db.Column(db.Integer, nullable=False)
    subtotal = db.Column(db.Integer, nullable=False)
    service_fee = db.Column(db.Integer, nullable=False, default=0)
    vat = db.Column(db.Integer, nullable=False, default=0)
    deposit = db.Column(db.Integer, nullable=False, default=0)
    total = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default="Confirmed")  # Confirmed | Completed | Cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
