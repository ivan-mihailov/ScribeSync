
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Subscription related
    stripe_customer_id = db.Column(db.String(120), unique=True)
    subscription_status = db.Column(db.String(50))
    subscription_end_date = db.Column(db.DateTime)
    
    # OAuth tokens
    google_access_token = db.Column(db.String(255))
    google_refresh_token = db.Column(db.String(255))
    token_expiry = db.Column(db.DateTime)
    
    def needs_token_refresh(self):
        return datetime.utcnow() >= self.token_expiry
