from flask import request, jsonify, Blueprint
from app.models import Bakery
from app.services.route_services import score_bakery, order_route

# Blueprint WITH a proper prefix:
route_bp = Blueprint("route", __name__, url_prefix="/api/route")

# -------------------------------
# GET /api/route
# -------------------------------
@route_bp.route("", methods=["GET"])
def generate_route():
    try:
        start_lat = float(request.args.get("start_lat"))
        start_lng = float(request.args.get("start_lng"))
    except:
        return jsonify({"error": "start_lat and start_lng are required"}), 400

    count = int(request.args.get("count", 5))
    sort_param = request.args.get("sort", "popularity")
    sort_criteria = sort_param.split(",")  # handle multiple criteria

    bakeries = Bakery.query.all()
    if not bakeries:
        return jsonify({"error": "No bakeries available"}), 404

    # Compute a combined score
    scored = []
    for b in bakeries:
        score = 0
        for criterion in sort_criteria:
            if criterion == "popularity":
                score += b.popularity_score or 0
            elif criterion == "rating":
                score += b.rating or 0
            elif criterion == "hype":
                score += b.hype_score or 0
            elif criterion == "distance":
                # simple negative distance score
                score -= ((b.latitude - start_lat)**2 + (b.longitude - start_lng)**2)**0.5
        scored.append((b, score))

    top_bakeries = [b for b, s in sorted(scored, key=lambda x: x[1], reverse=True)[:count]]

    # Sort into an ordered route (geographically)
    ordered = order_route(start_lat, start_lng, top_bakeries)

    result = [
        {
            "id": b.id,
            "name": b.name,
            "address": b.address,
            "latitude": b.latitude,
            "longitude": b.longitude,
            "rating": b.rating,
            "popularity_score": b.popularity_score,
            "hype_score": b.hype_score,
        }
        for b in ordered
    ]

    return jsonify(result)




