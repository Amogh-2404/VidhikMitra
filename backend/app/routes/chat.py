from flask import Blueprint, request, jsonify
import jwt
from ..models.language_model import load_model, generate_answer
from ..utils.moderation import moderate_query
from ..utils.security import redact
from ..utils.analytics import log_event
from ..config import Config

chat_bp = Blueprint('chat', __name__)

"""Chat routes handling user questions and returning answers."""
model = load_model()

# simple chat history store
CHAT_HISTORY = {}

@chat_bp.route('/', methods=['POST'])
def chat():
    token = request.headers.get('Authorization')
    user_id = 'anon'
    if token:
        try:
            payload = jwt.decode(token, Config.JWT_SECRET, algorithms=['HS256'])
            user_id = payload.get('email', 'anon')
        except jwt.PyJWTError:
            return jsonify({'error': 'Invalid token'}), 401
    data = request.json or {}
    query = data.get('query')
    if not query:
        return jsonify({'error': 'Query required'}), 400
    if not moderate_query(query):
        return jsonify({'error': 'Query violates policy'}), 400
    response = generate_answer(model, query)
    CHAT_HISTORY.setdefault(user_id, []).append({'q': redact(query), 'a': redact(response)})
    log_event('chat', {'user': user_id})
    return jsonify({'response': response})

@chat_bp.route('/history', methods=['GET'])
def history():
    token = request.headers.get('Authorization')
    user_id = 'anon'
    if token:
        try:
            payload = jwt.decode(token, Config.JWT_SECRET, algorithms=['HS256'])
            user_id = payload.get('email', 'anon')
        except jwt.PyJWTError:
            return jsonify({'error': 'Invalid token'}), 401
    log_event('history', {'user': user_id})
    return jsonify(CHAT_HISTORY.get(user_id, []))
