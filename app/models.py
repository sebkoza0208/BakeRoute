"""Database models (SQLAlchemy). Keep models small and well documented.
This example includes a minimal `Bakery` model to get started.
"""
from datetime import datetime
from . import db

class Bakery(db.Model):
    __tablename__ = "bakeries"

    id = db.Column(db.Integer, primary_key=True)
    osm_id = db.Column(db.String, unique=True, index=True)  # NEW
    name = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(200))
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    rating = db.Column(db.Float)
    popularity_score = db.Column(db.Integer)
    hype_score = db.Column(db.Integer)

    # For "new bakery" filtering
    opening_date = db.Column(db.Date, nullable=True)

    # Extra optional info
    description = db.Column(db.Text, nullable=True)
    website = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f"<Bakery {self.name}>"