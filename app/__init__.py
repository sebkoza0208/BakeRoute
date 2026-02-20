"""App factory pattern + extensions initialization.
This file creates and configures the Flask app. Using an app factory is a best
practice:
- It makes testing easier (create isolated apps in tests).
- It avoids global state during imports.
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    db.init_app(app)
    Migrate(app, db)
   
    # Import blueprints *after* app + db are initialized
    from .routes import register_blueprints 
    register_blueprints(app)

    return app



