from flask import Blueprint, request, jsonify
from .. import db
from ..models import Bakery

bakery_bp = Blueprint("bakery", __name__, url_prefix="/api/bakeries")

# -------------------------------
# POST /api/bakeries
# -------------------------------
@bakery_bp.route("/", methods=["POST"])
def create_bakery():
    data = request.get_json()

    # Validate required fields
    required = ["name", "address", "latitude", "longitude"]
    missing = [field for field in required if field not in data]

    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    # Create bakery object
    bakery = Bakery(
        name=data["name"],
        address=data["address"],
        latitude=float(data["latitude"]),
        longitude=float(data["longitude"]),
        rating=data.get("rating"),
        popularity_score=data.get("popularity_score"),
        hype_score=data.get("hype_score"),
        opening_date=data.get("opening_date"),
        description=data.get("description"),
        website=data.get("website")
    )

    # Save to DB
    db.session.add(bakery)
    db.session.commit()

    return jsonify({
        "message": "Bakery created successfully",
        "bakery": {
            "id": bakery.id,
            "name": bakery.name,
            "address": bakery.address,
            "latitude": bakery.latitude,
            "longitude": bakery.longitude,
            "rating": bakery.rating,
            "popularity_score": bakery.popularity_score,
            "hype_score": bakery.hype_score,
            "opening_date": str(bakery.opening_date) if bakery.opening_date else None,
            "description": bakery.description,
            "website": bakery.website
        }
    }), 201


# -------------------------------
# GET /api/bakeries
# -------------------------------
@bakery_bp.route("/", methods=["GET"])
def get_bakeries():
    # Query all bakeries from the database
    bakeries = Bakery.query.all()

    # Convert each bakery object into a dictionary
    bakery_list = []
    for b in bakeries:
        bakery_list.append({
            "id": b.id,
            "name": b.name,
            "address": b.address,
            "latitude": b.latitude,
            "longitude": b.longitude,
            "rating": b.rating,
            "popularity_score": b.popularity_score,
            "hype_score": b.hype_score,
            "opening_date": str(b.opening_date) if b.opening_date else None,
            "description": b.description,
            "website": b.website
        })

    # Return JSON response
    return {"bakeries": bakery_list}, 200

# -------------------------------
# GET /api/bakeries/<id>
# -------------------------------
@bakery_bp.route("/<int:bakery_id>", methods=["GET"])
def get_bakery(bakery_id):
    # Find bakery by ID
    bakery = Bakery.query.get(bakery_id)

    if not bakery:
        return {"error": "Bakery not found"}, 404

    # Convert to dictionary
    bakery_data = {
        "id": bakery.id,
        "name": bakery.name,
        "address": bakery.address,
        "latitude": bakery.latitude,
        "longitude": bakery.longitude,
        "rating": bakery.rating,
        "popularity_score": bakery.popularity_score,
        "hype_score": bakery.hype_score,
        "opening_date": str(bakery.opening_date) if bakery.opening_date else None,
        "description": bakery.description,
        "website": bakery.website
    }

    return {"bakery": bakery_data}, 200

# -------------------------------
# GET /api/route
# -------------------------------

