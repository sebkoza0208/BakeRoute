"""Main HTTP routes / controllers for the app.


Keep logic thin in routes: they should validate input, call services, and return responses.
Business logic should go into a separate `services/` module.
"""
from flask import current_app as app, request, jsonify
from flask import Blueprint, render_template
from ..models import Bakery
from .. import db


main_bp = Blueprint("main", __name__)




#@main_bp.route("/", methods=["GET"]) # home page for quick manual testing
#def index():
#    return "Bakery Route App — API running"


@main_bp.route("/")
def index():
    """Homepage showing bakery route map."""
    return render_template("map.html")



@main_bp.route("/bakeries", methods=["GET"])
def list_bakeries():
    """List bakeries with optional basic filters: limit, min_rating"""
    limit = int(request.args.get("limit", 50))
    min_rating = float(request.args.get("min_rating", 0.0))

    query = Bakery.query.filter(Bakery.rating >= min_rating).limit(limit)
    results = [b.to_dict() for b in query]
    return jsonify(results)



@main_bp.route("/bakeries", methods=["POST"])
def create_bakery():
    """Create a bakery (simple example - no auth). In production you'd validate and authenticate."""
    payload = request.get_json() or {}
    name = payload.get("name")
    lat = payload.get("latitude")
    lng = payload.get("longitude")

    if not name or lat is None or lng is None:
        return jsonify({"error": "name, latitude and longitude are required"}), 400

    bakery = Bakery(name=name, latitude=float(lat), longitude=float(lng))
    db.session.add(bakery)
    db.session.commit()


    return jsonify(bakery.to_dict()), 201