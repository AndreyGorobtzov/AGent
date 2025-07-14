from app import app, db
from models import User, Listing

with app.app_context():
    db.create_all()
