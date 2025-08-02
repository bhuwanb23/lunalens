from flask import Flask, request, jsonify, render_template, send_from_directory
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
CORS(app, supports_credentials=True, origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:3000"])

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
        print(f"🔍 Starting boulder detection for: {absolute_filepath}")
        detected_objects = boulder_controller.detect_boulders(absolute_filepath)
        print(f"🔍 Detection completed. Found {len(detected_objects) if detected_objects else 0} objects")
        
        if not detected_objects:
            return jsonify({
                "success": False,
                "message": "No boulders detected in the image"
            }), 200
        
        # Prepare results
        print(f"🔍 Preparing results for {len(detected_objects)} objects")
        results = {
            "success": True,
            "message": f"Detected {len(detected_objects)} objects",
            "detected_objects": [],
            "analysis_type": analysis_type,
            "additional_files": []
        }
        
        # Convert objects to serializable format
        for i, obj in enumerate(detected_objects):
            print(f"🔍 Processing object {i+1}/{len(detected_objects)}")
            try:
                obj_data = {
                    "class_name": getattr(obj, 'class_name', 'unknown'),
                    "confidence": float(getattr(obj, 'confidence', 0.0)),
                    "width_real": float(getattr(obj, 'width_real', 0.0)),
                    "height_real": float(getattr(obj, 'height_real', 0.0)),
                    "diameter_real": float(getattr(obj, 'diameter_real', 0.0)),
                    "area_real": float(getattr(obj, 'area_real', 0.0)),
                    "volume_real": float(getattr(obj, 'volume_real', 0.0)),
                    "circularity": float(getattr(obj, 'circularity', 0.0)),
                    "elongation": float(getattr(obj, 'elongation', 0.0)),
                    "degradation_state": getattr(obj, 'degradation_state', 'N/A'),
                    "estimated_depth": float(getattr(obj, 'estimated_depth', 0.0)) if getattr(obj, 'estimated_depth', None) else None
                }
                
                # Add bounding box if available
                if hasattr(obj, 'bbox') and obj.bbox is not None:
                    obj_data["bounding_box"] = {
                        "x1": int(obj.bbox[0]),
                        "y1": int(obj.bbox[1]),
                        "x2": int(obj.bbox[2]),
                        "y2": int(obj.bbox[3])
                    }
                
                # Add pixel measurements if available
                if hasattr(obj, 'width_px') and hasattr(obj, 'height_px') and hasattr(obj, 'area_px'):
                    obj_data["pixel_measurements"] = {
                        "width_px": int(obj.width_px),
                        "height_px": int(obj.height_px),
                        "area_px": int(obj.area_px)
                    }
                
                results["detected_objects"].append(obj_data)
                print(f"✅ Object {i+1} processed successfully")
                
            except Exception as e:
                print(f"❌ Error processing object {i+1}: {e}")
                # Add a minimal object data if processing fails
            obj_data = {
                    "class_name": "unknown",
                    "confidence": 0.0,
                    "width_real": 0.0,
                    "height_real": 0.0,
                    "diameter_real": 0.0,
                    "area_real": 0.0,
                    "volume_real": 0.0,
                    "circularity": 0.0,
                    "elongation": 0.0,
                    "degradation_state": "N/A",
                    "estimated_depth": None
            }
            results["detected_objects"].append(obj_data)
        
        # Add comprehensive analysis summary
        total_objects = len(detected_objects)
        boulders = [obj for obj in detected_objects if getattr(obj, 'class_name', '') == 'boulder']
        craters = [obj for obj in detected_objects if getattr(obj, 'class_name', '') == 'crater']
        
        try:
            results["analysis_summary"] = {
                "total_objects": total_objects,
                "boulder_count": len(boulders),
                "crater_count": len(craters),
                "average_confidence": float(sum(getattr(obj, 'confidence', 0.0) for obj in detected_objects) / total_objects) if total_objects > 0 else 0,
                "average_diameter": float(sum(getattr(obj, 'diameter_real', 0.0) for obj in detected_objects) / total_objects) if total_objects > 0 else 0,
                "average_area": float(sum(getattr(obj, 'area_real', 0.0) for obj in detected_objects) / total_objects) if total_objects > 0 else 0,
                "total_volume": float(sum(getattr(obj, 'volume_real', 0.0) for obj in detected_objects)),
                "average_circularity": float(sum(getattr(obj, 'circularity', 0.0) for obj in detected_objects) / total_objects) if total_objects > 0 else 0,
                "average_elongation": float(sum(getattr(obj, 'elongation', 0.0) for obj in detected_objects) / total_objects) if total_objects > 0 else 0,
                "processing_time": 2.4,  # This would be calculated from actual processing time
                "analysis_type": analysis_type,
                "image_filename": os.path.basename(absolute_filepath)
            }
        except Exception as e:
            print(f"❌ Error calculating analysis summary: {e}")
            results["analysis_summary"] = {
                "total_objects": total_objects,
                "boulder_count": len(boulders),
                "crater_count": len(craters),
                "average_confidence": 0.0,
                "average_diameter": 0.0,
                "average_area": 0.0,
                "total_volume": 0.0,
                "average_circularity": 0.0,
                "average_elongation": 0.0,
                "processing_time": 2.4,
                "analysis_type": analysis_type,
                "image_filename": os.path.basename(absolute_filepath)
            }
        
        # Perform additional analysis based on type
        if analysis_type in ['advanced', 'full']:
            # Calculate measurements
            detected_objects = boulder_controller.calculate_measurements(detected_objects)
        
        if analysis_type in ['gradcam', 'full']:
            # Generate Grad-CAM
            print(f"🔍 Generating Grad-CAM for analysis type: {analysis_type}")
            gradcam_path = boulder_controller.generate_gradcam(absolute_filepath, detected_objects)
            print(f"🔍 Grad-CAM path returned: {gradcam_path}")
            if gradcam_path:
                # Move/copy the Grad-CAM image to uploads folder
                import shutil
                uploads_dir = os.path.join(os.path.dirname(__file__), 'uploads')
                gradcam_filename = os.path.basename(gradcam_path)
                uploads_gradcam_path = os.path.join(uploads_dir, gradcam_filename)
                print(f"🔍 Uploads directory: {uploads_dir}")
                print(f"🔍 Grad-CAM filename: {gradcam_filename}")
                print(f"🔍 Uploads Grad-CAM path: {uploads_gradcam_path}")
                if os.path.abspath(gradcam_path) != os.path.abspath(uploads_gradcam_path):
                    shutil.copyfile(gradcam_path, uploads_gradcam_path)
                    print(f"✅ Grad-CAM file copied to uploads folder")
                # Return the path as /uploads/filename for frontend
                results["additional_files"].append({
                    "type": "gradcam",
                    "path": f"/uploads/{gradcam_filename}"
                })
                print(f"✅ Grad-CAM added to results with path: /uploads/{gradcam_filename}")
            else:
                print("❌ Grad-CAM generation failed - no path returned")
        
        # Always create detection visualization
        viz_path = boulder_controller.create_visualization(absolute_filepath, detected_objects)
        if viz_path:
            # Move/copy the visualization image to uploads folder
            import shutil
            uploads_dir = os.path.join(os.path.dirname(__file__), 'uploads')
            viz_filename = os.path.basename(viz_path)
            uploads_viz_path = os.path.join(uploads_dir, viz_filename)
            if os.path.abspath(viz_path) != os.path.abspath(uploads_viz_path):
                shutil.copyfile(viz_path, uploads_viz_path)
            # Return the path as /uploads/filename for frontend
            results["additional_files"].append({
                "type": "visualization",
                "path": f"/uploads/{viz_filename}"
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
        print(f"❌ Error during analysis: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "success": False,
            "message": f"Error during analysis: {str(e)}",
            "error_details": str(e)
        }), 500

@app.route('/uploads/<filename>')
def serve_upload(filename):
    """Serve uploaded files"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

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
