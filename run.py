"""Development entrypoint. Keep it simple so beginners can run the app easily.
Run with: python run.py
"""
from app import create_app
app = create_app()
if __name__ == "__main__":
    # debug=True for development only — never enable in production
    app.run(host="127.0.0.1", port=5000, debug=True)
