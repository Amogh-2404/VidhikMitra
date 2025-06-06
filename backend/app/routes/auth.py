from flask import Blueprint, request, jsonify
import hashlib
import jwt
from google.oauth2 import id_token
from google.auth.transport import requests
from ..config import Config
from ..utils.analytics import log_event

auth_bp = Blueprint('auth', __name__)

# simple in-memory store for example purposes
USERS = {}

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json or {}
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify({'error': 'Email and password required'}), 400
    if email in USERS:
        return jsonify({'error': 'User exists'}), 400
    hashed = hashlib.sha256(password.encode()).hexdigest()
    USERS[email] = hashed
    log_event('register', {'email': email})
    return jsonify({'message': 'Registered'})

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json or {}
    email = data.get('email')
    password = data.get('password')
    hashed = hashlib.sha256(password.encode()).hexdigest()
    if USERS.get(email) != hashed:
        return jsonify({'error': 'Invalid credentials'}), 401
    token = jwt.encode({'email': email}, Config.JWT_SECRET, algorithm='HS256')
    log_event('login', {'email': email})
    return jsonify({'token': token})


@auth_bp.route('/google', methods=['POST'])
def google_login():
    data = request.json or {}
    token = data.get('id_token')
    if not token:
        return jsonify({'error': 'id_token required'}), 400
    try:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), Config.GOOGLE_OAUTH_CLIENT_ID)
        email = idinfo['email']
    except Exception:
        return jsonify({'error': 'Invalid Google token'}), 401
    if email not in USERS:
        USERS[email] = 'google'
    jwt_token = jwt.encode({'email': email}, Config.JWT_SECRET, algorithm='HS256')
    log_event('google_login', {'email': email})
    return jsonify({'token': jwt_token})
