from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_message = db.Column(db.Text, nullable=False)
    ai_response = db.Column(db.Text, nullable=False)
    admin_summary = db.Column(db.Text)
    admin_action = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
