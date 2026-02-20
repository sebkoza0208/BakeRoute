# app/routes/__init__.py

def register_blueprints(app):
    from .main import main_bp
    from .bakery import bakery_bp
    from .route import route_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(bakery_bp)
    app.register_blueprint(route_bp)

