"""Seed data: 9 vehicles, each with 7 Unsplash photos, + demo accounts."""
from models import db, User, Vehicle
from pricing import get_daily_price, deposit_for

U = "https://images.unsplash.com/{}?q=80&w=1200&auto=format&fit=crop"

def photos(*ids):
    return [U.format(i) for i in ids]

CAR_EXT = [
    "photo-1503376780353-7e6692767b70", "photo-1555215695-3004980ad54e",
    "photo-1552519507-da3b142c6e3d", "photo-1583121274602-3e2820c69888",
    "photo-1503736334956-4c8f8e92946d", "photo-1549317661-bd32c8ce0db2",
    "photo-1494976388531-d1058494cdd8",
]
SUV = [
    "photo-1568605117036-5fe5e7bab0b7", "photo-1519641471654-76ce0107ad1b",
    "photo-1533473359331-0135ef1b58bf", "photo-1542362567-b07e54358753",
    "photo-1553440569-bcc63803a83d", "photo-1580273916550-e323be2ae537",
    "photo-1605559424843-9e4c228bf1c2",
]
SEDAN = [
    "photo-1618843479313-40f8afb4b4d8", "photo-1617531653332-bd46c24f2068",
    "photo-1617814076367-b759c7d7e738", "photo-1606664515524-ed2f786a0bd6",
    "photo-1555215695-3004980ad54e", "photo-1549399542-7e3f8b79c341",
    "photo-1792813045699-7b75386f8410",
]
HATCH = [
    "photo-1549317661-bd32c8ce0db2", "photo-1471479917193-f00955256257",
    "photo-1502877338535-766e1452684a", "photo-1493238792000-8113da705763",
    "photo-1511919884226-fd3cad34687c", "photo-1525609004556-c46c7d6cf023",
    "photo-1552519507-da3b142c6e3d",
]
BIKE = [
    "photo-1558981403-c5f9899a28bc", "photo-1568772585407-9361f9bf3a87",
    "photo-1591637333184-19aa84b3e01f", "photo-1609630875171-b1321377ee65",
    "photo-1449426468159-d96dbf08f19f", "photo-1547549082-6bc09f2049ae",
    "photo-1763244737839-220b4cd0259e",
]
SCOOTER = [
    "photo-1591370874773-6702e8f12fd8", "photo-1571068316344-75bc76f77890",
    "photo-1558981403-c5f9899a28bc", "photo-1568772585407-9361f9bf3a87",
    "photo-1591637333184-19aa84b3e01f", "photo-1609630875171-b1321377ee65",
    "photo-1449426468159-d96dbf08f19f",
]
CYCLE = [
    "photo-1485965120184-e220f721d03e", "photo-1532298229144-0ec0c57515c7",
    "photo-1507035895480-2b3156c31fc8", "photo-1471506480208-91b3a4cc78be",
    "photo-1517649763962-0c623066013b", "photo-1534787238916-9ba6764efd4f",
    "photo-1576435728678-68d0fbf94e91",
]

VEHICLES = [
    dict(brand="Toyota", model="Land Cruiser Prado", year=2023, mileage_km=18400, transmission="Automatic", fuel="Diesel", category="car", tier="luxury", cc=2755, seats=7, location="Kathmandu", photos=photos(*SUV), description="Flagship luxury SUV — leather, 4WD, perfect for Himalayan highways and family expeditions."),
    dict(brand="Toyota", model="Fortuner 4x4", year=2023, mileage_km=16800, transmission="Automatic", fuel="Diesel", category="car", tier="luxury", cc=2755, seats=7, location="Kathmandu", photos=photos(*SUV[2:] + SUV[:2]), description="Nepal's favourite luxury SUV — 4WD, high ground clearance, built for Himalayan highways and Mustang trails."),
    dict(brand="Hyundai", model="Creta SX", year=2022, mileage_km=31200, transmission="Automatic", fuel="Petrol", category="car", tier="standard", cc=1497, seats=5, location="Pokhara", photos=photos(*HATCH), description="Reliable compact SUV — sunroof, touchscreen, ideal for city and lakeside drives."),
    dict(brand="Suzuki", model="Swift ZXi", year=2022, mileage_km=27800, transmission="Manual", fuel="Petrol", category="car", tier="standard", cc=1197, seats=5, location="Ghorahi", photos=photos(*CAR_EXT), description="Nimble, fuel-efficient city car — easy parking, low running cost, great for daily rental."),
    dict(brand="Royal Enfield", model="Classic 350", year=2023, mileage_km=8600, transmission="Manual", fuel="Petrol", category="bike", tier="luxury", cc=349, seats=2, location="Pokhara", photos=photos(*BIKE), description="Iconic thump, chrome detailing — the classic choice for Mustang and lakeside rides."),
    dict(brand="Yamaha", model="FZ-S Fi V4", year=2023, mileage_km=5400, transmission="Manual", fuel="Petrol", category="bike", tier="luxury", cc=149, seats=2, location="Kathmandu", photos=photos(*BIKE[2:] + BIKE[:5]), description="Sporty street bike with muscular styling, Bluetooth console and sharp handling."),
    dict(brand="Honda", model="Dio 110", year=2022, mileage_km=12400, transmission="Automatic", fuel="Petrol", category="bike", tier="standard", cc=109, seats=2, location="Ghorahi", photos=photos(*SCOOTER), description="Light, easy commuter scooter — perfect for Kathmandu traffic and short trips."),
    dict(brand="Trek", model="Marlin 7 Mountain", year=2023, mileage_km=1200, transmission="Manual", fuel="Electric", category="cycle", tier="luxury", cc=0, seats=1, location="Pokhara", photos=photos(*CYCLE), description="High-end mountain bike with hydraulic disc brakes and front suspension — built for Himalayan trails."),
    dict(brand="Hero", model="Sprint City Cycle", year=2022, mileage_km=3400, transmission="Manual", fuel="Electric", category="cycle", tier="standard", cc=0, seats=1, location="Kathmandu", photos=photos(*CYCLE[3:] + CYCLE[:4]), description="Comfortable standard city cycle — light frame, easy gears, ideal for daily rides and fitness."),
]

def seed():
    if User.query.first():
        return
    demo_owner = User(role="owner", full_name="Bikalpa Khanal", phone="9845857209",
                      email="owner@apexride.com.np", nagarikta_no="12-34-56-78901",
                      national_id_no="NID-100200300", verification_status="Approved")
    demo_owner.set_password("apexride123")
    demo_customer = User(role="customer", full_name="Madhu Pun", phone="9845857209",
                         email="customer@apexride.com.np", nagarikta_no="22-33-44-55667",
                         licence_no="DL-03-123456", verification_status="Approved")
    demo_customer.set_password("apexride123")
    db.session.add_all([demo_owner, demo_customer])
    db.session.flush()
    for v in VEHICLES:
        price = get_daily_price(v["category"], v["tier"])
        veh = Vehicle(owner_id=demo_owner.id, daily_price=price,
                      deposit=deposit_for(v["category"], v["tier"]), **v)
        db.session.add(veh)
    db.session.commit()
    print("Seeded 9 vehicles + 2 demo accounts.")
