import overpy
from app import create_app, db
from app.models import Bakery
import random

app = create_app()
api = overpy.Overpass()

boxes = [
    (55.59, 12.53, 55.65, 12.58),
    (55.59, 12.58, 55.65, 12.63),
    (55.65, 12.53, 55.72, 12.58),
    (55.65, 12.58, 55.72, 12.63),
]

all_bakeries = []

print("Querying OpenStreetMap for bakeries in Copenhagen...")

for i, (lat_min, lon_min, lat_max, lon_max) in enumerate(boxes, start=1):
    print(f"Querying box {i}/{len(boxes)}: {lat_min},{lon_min} → {lat_max},{lon_max}")
    query = f"""
    node["shop"="bakery"]({lat_min},{lon_min},{lat_max},{lon_max});
    out;
    """
    try:
        result = api.query(query)
        for node in result.nodes:
            bakery_data = {
                "osm_id": str(node.id),
                "name": node.tags.get("name", "Unknown Bakery"),
                "address": node.tags.get("addr:street", "") + " " + node.tags.get("addr:housenumber", ""),
                "latitude": float(node.lat),
                "longitude": float(node.lon),
                "rating": round(random.uniform(3.5, 5.0), 1),
                "popularity_score": random.randint(50, 100),
                "hype_score": random.randint(30, 100),
            }
            all_bakeries.append(bakery_data)
        print(f"  Found {len(result.nodes)} bakeries in this box.")
    except overpy.exception.OverpassTooManyRequests:
        print("  Too many requests. Try again later or slow down your queries.")
    except overpy.exception.OverpassGatewayTimeout:
        print("  Overpass API timeout. Skipping this box.")

print(f"Total bakeries found: {len(all_bakeries)}")

# Seed/update database
with app.app_context():
    for b in all_bakeries:
        existing = Bakery.query.filter_by(osm_id=b["osm_id"]).first()
        if existing:
            # Update existing bakery
            existing.name = b["name"]
            existing.address = b["address"]
            existing.latitude = b["latitude"]
            existing.longitude = b["longitude"]
            existing.rating = b["rating"]
            existing.popularity_score = b["popularity_score"]
            existing.hype_score = b["hype_score"]
        else:
            # Add new bakery
            bakery = Bakery(**b)
            db.session.add(bakery)
    db.session.commit()

print("Database updated successfully.")
