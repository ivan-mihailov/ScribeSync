
from flask import Flask, session, redirect, url_for, request, jsonify
from models.user import db, User
import os
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from functools import wraps

SCOPES = [
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/tasks',
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/gmail.modify'
]

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

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/auth/google')
def google_auth():
    flow = Flow.from_client_secrets_file(
        'client_secrets.json',
        scopes=SCOPES,
        redirect_uri=url_for('oauth2callback', _external=True)
    )
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    session['state'] = state
    return redirect(authorization_url)

@app.route('/auth/google/callback')
def oauth2callback():
    state = session['state']
    flow = Flow.from_client_secrets_file(
        'client_secrets.json',
        scopes=SCOPES,
        state=state,
        redirect_uri=url_for('oauth2callback', _external=True)
    )
    
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)
    credentials = flow.credentials

    # Get user email from Google
    import google.oauth2.credentials
    import google.auth.transport.requests
    import requests
    
    session_credentials = google.oauth2.credentials.Credentials(**credentials_to_dict(credentials))
    user_info = requests.get(
        'https://www.googleapis.com/oauth2/v2/userinfo',
        headers={'Authorization': f'Bearer {session_credentials.token}'}
    ).json()
    
    # Create or update user
    user = User.query.filter_by(email=user_info['email']).first()
    if not user:
        user = User(email=user_info['email'])
    
    user.google_access_token = credentials.token
    user.google_refresh_token = credentials.refresh_token
    user.token_expiry = datetime.utcnow() + timedelta(seconds=credentials.expiry.seconds)
    
    db.session.add(user)
    db.session.commit()
    
    session['user_id'] = user.id
    return redirect('/')

@app.route('/auth/logout')
def logout():
    session.clear()
    return redirect('/')

def credentials_to_dict(credentials):
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
