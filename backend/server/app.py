from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import jwt
import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Simple Flask app setup
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')
app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'

# Initialize CORS
CORS(app, origins=['http://localhost:3000', 'http://localhost:5173', 'http://127.0.0.1:5173'])

# Store active tokens (in production, use Redis or database)
ACTIVE_TOKENS = set()

# Simple login credentials
DEMO_CREDENTIALS = {
    "isro123": {
        "accessCode": "moon@2024",
        "name": "ISRO Mission Control",
        "role": "admin",
        "permissions": ["dashboard", "analytics", "settings"]
    },
    "mission001": {
        "accessCode": "lunar@2024",
        "name": "Lunar Mission Team",
        "role": "user",
        "permissions": ["dashboard", "analytics"]
    },
    "research002": {
        "accessCode": "research@2024",
        "name": "Research Team",
        "role": "researcher",
        "permissions": ["dashboard", "analytics", "data_export"]
    },
    "test001": {
        "accessCode": "test@2024",
        "name": "Test User",
        "role": "user",
        "permissions": ["dashboard"]
    }
}

def validate_credentials(mission_id, access_code):
    """Validate user credentials"""
    user = DEMO_CREDENTIALS.get(mission_id)
    if user and user['accessCode'] == access_code:
        return user
    return None

def get_user_by_mission_id(mission_id):
    """Get user credentials by mission ID"""
    return DEMO_CREDENTIALS.get(mission_id)

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/credentials', methods=['GET'])
def credentials():
    return render_template('login_credentials.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    mission_id = data.get('missionId')
    access_code = data.get('accessCode')

    # Validate user credentials
    user = validate_credentials(mission_id, access_code)
    if user:
        # Generate JWT token
        payload = {
            'missionId': mission_id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24),
            'iat': datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
        ACTIVE_TOKENS.add(token)
        
        return jsonify({
            "success": True, 
            "message": "Login successful!",
            "token": token,
            "user": {
                "missionId": mission_id,
                "name": user['name'],
                "role": user['role'],
                "permissions": user['permissions']
            }
        }), 200
    else:
        return jsonify({"success": False, "message": "Invalid credentials."}), 401

@app.route('/logout', methods=['POST'])
def logout():
    data = request.get_json()
    token = data.get('token')
    
    if token and token in ACTIVE_TOKENS:
        ACTIVE_TOKENS.remove(token)
        return jsonify({"success": True, "message": "Logout successful!"}), 200
    else:
        return jsonify({"success": False, "message": "Invalid token."}), 401

@app.route('/verify-token', methods=['POST'])
def verify_token():
    data = request.get_json()
    token = data.get('token')
    
    if not token:
        return jsonify({"valid": False, "message": "No token provided."}), 401
    
    try:
        # Verify token
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        
        # Check if token is still active
        if token in ACTIVE_TOKENS:
            user_info = get_user_by_mission_id(payload['missionId'])
            if user_info:
                return jsonify({
                    "valid": True, 
                    "user": {
                        "missionId": payload['missionId'],
                        "name": user_info['name'],
                        "role": user_info['role'],
                        "permissions": user_info['permissions']
                    }
                }), 200
            else:
                return jsonify({"valid": False, "message": "User not found."}), 401
        else:
            return jsonify({"valid": False, "message": "Token has been revoked."}), 401
            
    except jwt.ExpiredSignatureError:
        return jsonify({"valid": False, "message": "Token has expired."}), 401
    except jwt.InvalidTokenError:
        return jsonify({"valid": False, "message": "Invalid token."}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
