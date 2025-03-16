import random
import string
from flask import Blueprint, request, jsonify
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash

key_blueprint = Blueprint('key', __name__)

mongo = None  # Global variable for MongoDB

def init_mongo(app):
    """Initialize MongoDB connection with Flask app."""
    global mongo
    if mongo is None:  # ✅ Ensure MongoDB is only initialized once
        mongo = PyMongo(app)

def generate_unique_key():
    """Generate a random 10-digit unique key."""
    return ''.join(random.choices(string.digits, k=10))

@key_blueprint.route('/generate_key', methods=['POST'])
def generate_key():
    """Generate and store a 10-digit key for a user upon login."""
    global mongo  

    if mongo is None:  
        return jsonify({"message": "Database not initialized"}), 500

    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({"message": "Email is required"}), 400

    unique_key = generate_unique_key()
    hashed_key = generate_password_hash(unique_key)

    try:
        mongo.db.users.update_one(
            {"email": email},
            {"$set": {"unique_key": hashed_key}},
            upsert=True
        )
        return jsonify({"message": "Key generated successfully", "key": unique_key}), 200
    except Exception as e:
        return jsonify({"message": f"Database error: {e}"}), 500
