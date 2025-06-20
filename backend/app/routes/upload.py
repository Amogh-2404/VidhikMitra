import os
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from ..utils.ocr import extract_text
from ..utils.security import redact
from ..utils.qa import answer_question
from ..utils.analytics import log_event

upload_bp = Blueprint('upload', __name__)

"""Routes for file uploads and OCR extraction."""

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@upload_bp.route('/', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    file = request.files['file']
    filename = secure_filename(file.filename)
    path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(path)
    text = extract_text(path)
    log_event('upload', {'filename': filename})
    return jsonify({'text': redact(text)})


@upload_bp.route('/qa', methods=['POST'])
def upload_and_qa():
    """Return answer to query based on uploaded file."""
    if 'file' not in request.files or 'query' not in request.form:
        return jsonify({'error': 'File and query required'}), 400
    file = request.files['file']
    query = request.form['query']
    filename = secure_filename(file.filename)
    path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(path)
    text = extract_text(path)
    answer = answer_question(text, query)
    log_event('upload_qa', {'filename': filename})
    return jsonify({'answer': redact(answer), 'text': redact(text)})
