# ApexRide Nepal — Luxury Vehicle Rental Platform 🇳🇵

A complete, production-ready Flask vehicle rental platform for Nepal — dark luxury design, glassmorphism, verified KYC, rigid NPR pricing, and a 7-photo vehicle gallery.

**Founders: Mr. Bikalpa Khanal & Madhu Pun** — ApexRide Nepal Pvt. Ltd., Durbarmarg, Kathmandu, Nepal.

## Quick Start

```bash
pip install -r requirements.txt
python app.py
```

Open **http://127.0.0.1:5000** — the SQLite database (`instance/apexride.db`) is created and seeded automatically on first run.

## Demo Accounts

| Role | Email | Password |
|---|---|---|
| Owner | owner@apexride.com.np | apexride123 |
| Customer | customer@apexride.com.np | apexride123 |

## Fixed Pricing (Rs. / day, enforced server-side in `pricing.py`)

| Vehicle | Standard | Luxury / High CC |
|---|---|---|
| Cycle | Rs. 500 | Rs. 2,000 |
| Bike | Rs. 2,000 | Rs. 7,000 |
| Car | Rs. 7,000 | Rs. 15,000 |

Booking breakdown: subtotal + 5% service fee + 13% VAT + refundable security deposit (Cycle Rs. 5,000 / Bike Rs. 15,000 / Car Rs. 30,000; doubled for Luxury).

Any vehicle submission whose price does not match the map is **rejected** (`validate_price` in `pricing.py`); the tier selector in the listing wizard locks the price field read-only.

## Pages

- `/` — Home: cinematic hero, drifting-car animation, categories, featured fleet with live price calculator, trust badges, founders, testimonials
- `/fleet` — Search & filters (type, transmission, fuel, tier, price), quick-preview modal
- `/vehicle/<id>` — 7-photo gallery (swipe + lightbox), specs grid, date-picker booking widget with automated breakdown
- `/list-vehicle` — Owner multi-step wizard (Basics → 7 Photos → Video & Pricing → Review & Policy), login + owner only
- `/register` — Role selector (Customer "Rent a Vehicle" vs Owner "List & Earn") with dynamic KYC forms: Nagarikta / Citizenship + National ID, driving licence + photo, selfie, Bluebook, 360° walkaround video
- `/login`, `/logout`, `/dashboard` — Tabbed dashboard: Bookings, My Vehicles, Verification (Pending/Approved), Earnings, Rental Agreements
- `/about` — Founders' story, Kathmandu office, 24/7 emergency road assistance (+977-9845857209), FAQ accordion
- `POST /book/<id>`, `POST /api/calculate` — booking + price calculation

## KYC Rules

- **Customer:** full name, 10-digit Nepal phone (`^(98|97)\d{8}$`), email, password, Nagarikta **OR** National ID, Driving Licence No. + licence photo, selfie.
- **Owner:** same, plus Nagarikta **AND** National ID, selfie, Bluebook / registration document, 360° walkaround video.

## Project Structure

```
app.py  models.py  pricing.py  seed.py  requirements.txt
routes/  main.py  auth.py  vehicles.py
templates/  base.html  index.html  fleet.html  vehicle_detail.html
            list_vehicle.html  register.html  login.html  dashboard.html  about.html
static/css/style.css  static/js/main.js
uploads/  instance/apexride.db (auto-created)
```

## Tech

Python 3.10+ · Flask · Flask-SQLAlchemy (SQLite) · Werkzeug password hashing · Tailwind CDN (supplement) + custom CSS (glassmorphism, `clamp()` typography, IntersectionObserver reveals, canvas/CSS drift animation with `prefers-reduced-motion` support) · Vanilla JS.

## Emergency Contact

24/7 Road Assistance: **+977-9845857209** · Khanal2061@gmail.com
