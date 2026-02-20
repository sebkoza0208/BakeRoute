import math
from datetime import date

def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate distance (km) between two coordinates."""
    R = 6371  # Earth radius in km

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = (
        math.sin(dlat / 2)**2 +
        math.cos(math.radians(lat1)) *
        math.cos(math.radians(lat2)) *
        math.sin(dlon / 2)**2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c


def compute_freshness(opening_date):
    """Return a value 0-1 where newer bakeries get higher scores."""
    if not opening_date:
        return 0
    days_old = (date.today() - opening_date).days
    return max(0, min(1, 1 - days_old / 2000))  # bakeries under ~5 years get boost


def score_bakery(bakery, start_lat, start_lng, sort_criteria=None):
    """
    Score a bakery based on multiple criteria.
    sort_criteria: list of tuples [(criterion, weight), ...]
    """
    if sort_criteria is None:
        sort_criteria = [("popularity", 1.0)]

    total_score = 0
    for criterion, weight in sort_criteria:
        if criterion == "popularity":
            total_score += (bakery.popularity_score or 0) * weight
        elif criterion == "rating":
            total_score += (bakery.rating or 0) * weight
        elif criterion == "hype":
            total_score += (bakery.hype_score or 0) * weight
        elif criterion == "distance":
            dist = haversine_distance(start_lat, start_lng, bakery.latitude, bakery.longitude)
            total_score += (-dist) * weight  # negative = closer is better
        else:
            pass  # unknown criterion ignored

    return total_score


def order_route(start_lat, start_lng, bakeries):
    """Return bakeries ordered by nearest-neighbor path."""
    unvisited = bakeries.copy()
    route = []
    current_lat = start_lat
    current_lng = start_lng

    while unvisited:
        next_b = min(
            unvisited,
            key=lambda b: haversine_distance(current_lat, current_lng, b.latitude, b.longitude)
        )
        route.append(next_b)
        current_lat = next_b.latitude
        current_lng = next_b.longitude
        unvisited.remove(next_b)

    return route
