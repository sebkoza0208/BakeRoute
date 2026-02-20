from app import create_app, db
from app.models import Bakery
from datetime import date

app = create_app()

# Sample bakery data
sample_bakeries = [
    {
        "name": "Andersen Bakery",
        "address": "Nørrebrogade 45, Copenhagen",
        "latitude": 55.688,
        "longitude": 12.555,
        "rating": 4.5,
        "popularity_score": 82,
        "hype_score": 67,
        "opening_date": date(2020, 5, 10),
        "description": "Famous for Danish pastries",
        "website": "https://andersenbakery.dk"
    },
    {
        "name": "La Glace",
        "address": "Skoubogade 3, Copenhagen",
        "latitude": 55.683,
        "longitude": 12.580,
        "rating": 4.8,
        "popularity_score": 95,
        "hype_score": 88,
        "opening_date": date(1870, 1, 1),
        "description": "Historic bakery with classic cakes",
        "website": "https://laglace.dk"
    },
    {
        "name": "Meyers Bageri",
        "address": "Jægersborggade 9, Copenhagen",
        "latitude": 55.689,
        "longitude": 12.568,
        "rating": 4.7,
        "popularity_score": 90,
        "hype_score": 75,
        "opening_date": date(2008, 3, 15),
        "description": "Organic bread and pastries",
        "website": "https://meyers.dk"
    }
]

# Use app context to access the database
with app.app_context():
    for b in sample_bakeries:
        existing = Bakery.query.filter_by(name=b["name"], address=b["address"]).first()
        if not existing:
            bakery = Bakery(**b)
            db.session.add(bakery)
    db.session.commit()
