import os
from pathlib import Path
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from database import (
    init_db,
    get_all_contacts,
    get_contact_by_id,
    create_contact,
    update_contact,
    delete_contact,
)


app = Flask(__name__)
CORS(app)

FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"

# Initialise database tables on server start
with app.app_context():
    init_db()

@app.route('/', methods=['GET'])
def home():
    return send_from_directory(str(FRONTEND_DIR), 'index.html')

@app.route('/<path:path>', methods=['GET'])
def serve_frontend(path):
    file_path = FRONTEND_DIR / path
    if file_path.exists():
        return send_from_directory(str(FRONTEND_DIR), path)
    return send_from_directory(str(FRONTEND_DIR), 'index.html')

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "message": "Flask server is connected to PostgreSQL"}), 200

@app.route('/api/contacts', methods=['GET'])
def list_contacts():
    return jsonify(get_all_contacts()), 200

@app.route('/api/contacts/<int:contact_id>', methods=['GET'])
def get_contact(contact_id):
    contact = get_contact_by_id(contact_id)
    if not contact:
        return jsonify({"error": "Contact not found"}), 404
    return jsonify(contact), 200

@app.route('/api/contacts', methods=['POST'])
def add_contact():
    payload = request.get_json() or {}
    result = create_contact(payload)
    if result.get('error'):
        return jsonify(result), 400
    return jsonify(result), 201

@app.route('/api/contacts/<int:contact_id>', methods=['PUT'])
def edit_contact(contact_id):
    payload = request.get_json() or {}
    result = update_contact(contact_id, payload)
    if result.get('error'):
        return jsonify(result), result.get('status', 400)
    return jsonify(result), 200

@app.route('/api/contacts/<int:contact_id>', methods=['DELETE'])
def remove_contact(contact_id):
    result = delete_contact(contact_id)
    if result.get('error'):
        return jsonify(result), result.get('status', 400)
    return jsonify(result), 200

if __name__ == '__main__':
    port = int(os.getenv('PORT', '5000'))
    app.run(debug=True, host='0.0.0.0', port=port)
    
