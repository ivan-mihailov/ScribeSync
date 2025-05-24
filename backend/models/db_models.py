
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
    
    # Relationships
    documents = db.relationship('Document', backref='user', lazy=True)
    
    def needs_token_refresh(self):
        return datetime.utcnow() >= self.token_expiry

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    version = db.Column(db.String(255), nullable=False)  # filename + datetime
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    pages = db.relationship('Page', backref='document', lazy=True)

class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(db.Integer, db.ForeignKey('document.id'), nullable=False)
    page_number = db.Column(db.Integer, nullable=False)
    page_phash = db.Column(db.String(16))  # 64-bit pHash stored as hex
    intent_flag = db.Column(db.Boolean, default=False)
    extracted_text = db.Column(db.Text)
    events = db.Column(db.JSON)
    todo_list = db.Column(db.JSON)
    notes = db.Column(db.Text)
    ai_notes_summary = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        db.UniqueConstraint('document_id', 'page_number', name='unique_page_per_document'),
    )
