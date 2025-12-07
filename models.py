from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    review_text = db.Column(db.Text, nullable=False)

    ai_user_response = db.Column(db.Text, nullable=False)
    ai_admin_summary = db.Column(db.Text)
    ai_recommended_action = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

