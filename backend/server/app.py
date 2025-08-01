from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import jwt
import datetime
import os
import sys
import numpy as np
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# Add boulder_detection to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'boulder_detection'))

# Import boulder detection modules
try:
    from detector import BoulderDetector
    from gradcam import GradCAMVisualizer
    from measurements import PhysicalCalculator, ObjectMeasurements
    from main import BoulderDetectionController
    BOULDER_DETECTION_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Boulder detection modules not available: {e}")
    BOULDER_DETECTION_AVAILABLE = False

# Load environment variables
load_dotenv()

# Simple Flask app setup
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')
app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'

# File upload configuration
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff'}

# Create uploads directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize CORS
CORS(app, origins=['http://localhost:3000', 'http://localhost:5173', 'http://127.0.0.1:5173'])

# Store active tokens (in production, use Redis or database)
ACTIVE_TOKENS = set()

# Boulder detection controller
boulder_controller = None

def init_boulder_detection():
    """Initialize boulder detection system"""
    global boulder_controller
    print(f"🔍 BOULDER_DETECTION_AVAILABLE: {BOULDER_DETECTION_AVAILABLE}")
    if BOULDER_DETECTION_AVAILABLE:
        try:
            print("🔄 Starting boulder detection initialization...")
            # Change to boulder_detection directory
            boulder_dir = os.path.join(os.path.dirname(__file__), '..', 'boulder_detection')
            print(f"📁 Boulder directory: {boulder_dir}")
            os.chdir(boulder_dir)
            print(f"📁 Current directory after change: {os.getcwd()}")
            
            # Initialize controller
            print("🚀 Creating BoulderDetectionController...")
            boulder_controller = BoulderDetectionController()
            print("✅ Boulder detection system initialized successfully!")
            
            # Change back to server directory
            os.chdir(os.path.dirname(__file__))
            print(f"📁 Back to server directory: {os.getcwd()}")
            
        except Exception as e:
            print(f"❌ Error initializing boulder detection: {e}")
            import traceback
            traceback.print_exc()
            boulder_controller = None
    else:
        print("⚠️ Boulder detection modules not available")

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Simple login credentials
DEMO_CREDENTIALS = {
    "isro123": {
        "accessCode": "moon@2024",
        "name": "ISRO Mission Control",
        "role": "admin",
        "permissions": ["dashboard", "analytics", "settings", "boulder_detection"]
    },
    "mission001": {
        "accessCode": "lunar@2024",
        "name": "Lunar Mission Team",
        "role": "user",
        "permissions": ["dashboard", "analytics", "boulder_detection"]
    },
    "research002": {
        "accessCode": "research@2024",
        "name": "Research Team",
        "role": "researcher",
        "permissions": ["dashboard", "analytics", "data_export", "boulder_detection"]
    },
    "test001": {
        "accessCode": "test@2024",
        "name": "Test User",
        "role": "user",
        "permissions": ["dashboard", "boulder_detection"]
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

@app.route('/boulder-detection', methods=['GET'])
def boulder_detection():
    """Serve the boulder detection HTML interface"""
    return render_template('boulder_detection.html')

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

# Boulder Detection API Endpoints

@app.route('/api/boulder/upload', methods=['POST'])
def upload_image():
    """Upload image for boulder detection"""
    if 'image' not in request.files:
        return jsonify({"success": False, "message": "No image file provided"}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({"success": False, "message": "No file selected"}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        return jsonify({
            "success": True,
            "message": "Image uploaded successfully",
            "filename": filename,
            "filepath": filepath
        }), 200
    else:
        return jsonify({"success": False, "message": "Invalid file type"}), 400

@app.route('/api/boulder/analyze', methods=['POST'])
def analyze_boulder():
    """Analyze uploaded image for boulder detection"""
    if not BOULDER_DETECTION_AVAILABLE:
        return jsonify({
            "success": False, 
            "message": "Boulder detection system not available"
        }), 503
    
    if not boulder_controller:
        return jsonify({
            "success": False, 
            "message": "Boulder detection system not initialized"
        }), 503
    
    data = request.get_json()
    filepath = data.get('filepath')
    analysis_type = data.get('analysisType', 'basic')
    
    if not filepath or not os.path.exists(filepath):
        return jsonify({"success": False, "message": "Image file not found"}), 400
    
    try:
        # Change to boulder_detection directory for model loading
        boulder_dir = os.path.join(os.path.dirname(__file__), '..', 'boulder_detection')
        os.chdir(boulder_dir)
        
        # Convert relative filepath to absolute path
        if not os.path.isabs(filepath):
            server_dir = os.path.dirname(__file__)
            absolute_filepath = os.path.join(server_dir, filepath)
        else:
            absolute_filepath = filepath
            
        print(f"🔍 Original filepath: {filepath}")
        print(f"🔍 Absolute filepath: {absolute_filepath}")
        print(f"🔍 File exists: {os.path.exists(absolute_filepath)}")
        
        # Detect boulders
        detected_objects = boulder_controller.detect_boulders(absolute_filepath)
        
        if not detected_objects:
            return jsonify({
                "success": False,
                "message": "No boulders detected in the image"
            }), 200
        
        # Prepare results
        results = {
            "success": True,
            "message": f"Detected {len(detected_objects)} objects",
            "detected_objects": [],
            "analysis_type": analysis_type,
            "additional_files": []
        }
        
        # Convert objects to serializable format
        for obj in detected_objects:
            obj_data = {
                "class_name": obj.class_name,
                "confidence": float(obj.confidence),
                "width_real": float(obj.width_real),
                "height_real": float(obj.height_real),
                "diameter_real": float(obj.diameter_real),
                "area_real": float(obj.area_real),
                "volume_real": float(obj.volume_real),
                "circularity": float(obj.circularity),
                "elongation": float(obj.elongation),
                "degradation_state": obj.degradation_state,
                "estimated_depth": float(obj.estimated_depth) if obj.estimated_depth else None
            }
            results["detected_objects"].append(obj_data)
        
        # Perform additional analysis based on type
        if analysis_type in ['advanced', 'full']:
            # Calculate measurements
            detected_objects = boulder_controller.calculate_measurements(detected_objects)
        
        if analysis_type in ['gradcam', 'full']:
            # Generate Grad-CAM
            gradcam_path = boulder_controller.generate_gradcam(absolute_filepath, detected_objects)
            if gradcam_path:
                results["additional_files"].append({
                    "type": "gradcam",
                    "path": gradcam_path
                })
        
        if analysis_type in ['visualization', 'full']:
            # Create visualization
            viz_path = boulder_controller.create_visualization(absolute_filepath, detected_objects)
            if viz_path:
                results["additional_files"].append({
                    "type": "visualization",
                    "path": viz_path
                })
        
        # Calculate density analysis
        density_analysis = boulder_controller.calculate_density_analysis(detected_objects, absolute_filepath)
        results["density_analysis"] = density_analysis
        
        # Change back to server directory
        os.chdir(os.path.dirname(__file__))
        
        return jsonify(results), 200
        
    except Exception as e:
        # Change back to server directory
        os.chdir(os.path.dirname(__file__))
        return jsonify({
            "success": False,
            "message": f"Error during analysis: {str(e)}"
        }), 500

@app.route('/api/boulder/status', methods=['GET'])
def boulder_status():
    """Check boulder detection system status"""
    return jsonify({
        "available": BOULDER_DETECTION_AVAILABLE,
        "initialized": boulder_controller is not None,
        "models_loaded": boulder_controller is not None
    }), 200

if __name__ == '__main__':
    # Initialize boulder detection system
    init_boulder_detection()
    
    app.run(host='0.0.0.0', port=5000, debug=True)
