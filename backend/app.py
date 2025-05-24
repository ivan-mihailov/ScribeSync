
from flask import Flask, session, redirect
from models.user import db, User
import os
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/scribesync')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.getenv('FLASK_SECRET_KEY')

db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

def refresh_google_token(user):
    credentials = Credentials(
        token=user.google_access_token,
        refresh_token=user.google_refresh_token,
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.getenv('GOOGLE_CLIENT_ID'),
        client_secret=os.getenv('GOOGLE_CLIENT_SECRET')
    )
    
    if credentials.expired:
        credentials.refresh()
        user.google_access_token = credentials.token
        user.token_expiry = datetime.utcnow() + timedelta(seconds=credentials.expiry.seconds)
        db.session.commit()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
