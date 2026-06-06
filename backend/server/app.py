from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import jwt
import datetime
import json
import os
import sys
import time
import numpy as np
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import traceback

# Import database components
from models import db, User, Analysis, DetectedObject, DensityAnalysis, AnalysisSession, SystemLog
from database import (
    init_db,
    create_analysis_record,
    get_user_analyses,
    get_analysis_with_details,
    log_system_event,
    get_analytics_summary as db_get_analytics_summary,
)
from config import config

# Import security configuration
try:
    from security_config import NETWORK_SECURITY, SECURITY_HEADERS, get_server_config, print_security_status
except ImportError:
    # Fallback security configuration if security_config.py is not available
    NETWORK_SECURITY = {
        'allow_external_access': False,
        'allowed_hosts': ['127.0.0.1', 'localhost', '::1'],
        'blocked_ips': set(),
        'require_https': False,
        'host': '127.0.0.1',
        'port': 5000,
        'allowed_origins': ["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:3000"]
    }
    SECURITY_HEADERS = {}
    
    def get_server_config():
        return {'host': '127.0.0.1', 'port': 5000}
    
    def print_security_status():
        print("✅ Server configured for localhost-only access (fallback config)")

# Add boulder_detection to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'boulder_detection'))

# Import boulder detection modules
try:
    # Add the boulder_detection directory to the path
    boulder_detection_path = os.path.join(os.path.dirname(__file__), '..', 'boulder_detection')
    if boulder_detection_path not in sys.path:
        sys.path.insert(0, boulder_detection_path)
    
    from main import BoulderDetectionController
    BOULDER_DETECTION_AVAILABLE = True
    print("✅ Boulder detection modules imported successfully")
except ImportError as e:
    print(f"Warning: Boulder detection modules not available: {e}")
    BOULDER_DETECTION_AVAILABLE = False

# Load environment variables
load_dotenv()



# Create Flask app
app = Flask(__name__)

# Load configuration
config_name = os.environ.get('FLASK_CONFIG', 'development')
app.config.from_object(config[config_name])

# Initialize database
init_db(app)

# Initialize CORS with security-aware origins
CORS(app, supports_credentials=True, origins=NETWORK_SECURITY['allowed_origins'])

# Security middleware to enforce localhost-only access
@app.before_request
def enforce_localhost_access():
    """Enforce localhost-only access for security"""
    # Skip check for login endpoint to allow initial access
    if request.path == '/login':
        return None
    
    # Check if external access is explicitly allowed
    if NETWORK_SECURITY['allow_external_access']:
        return None
    
    # Enforce localhost-only access
    if not is_localhost_request():
        print(f"🚫 Blocked external access from {request.remote_addr} to {request.path}")
        return jsonify({
            "success": False,
            "message": "Access denied. This server only accepts localhost connections.",
            "error": "EXTERNAL_ACCESS_BLOCKED"
        }), 403
    
    return None

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
            original_dir = os.getcwd()
            os.chdir(boulder_dir)
            print(f"📁 Current directory after change: {os.getcwd()}")
            
            # Initialize controller
            print("🚀 Creating BoulderDetectionController...")
            boulder_controller = BoulderDetectionController()
            if not getattr(boulder_controller, 'is_ready', False):
                print("⚠️ Boulder detection models not loaded; /api/boulder/* will return 503 until models are available.")
                boulder_controller = None
            else:
                print("✅ Boulder detection system initialized successfully!")
            
            # Change back to server directory
            os.chdir(original_dir)
            print(f"📁 Back to server directory: {os.getcwd()}")
            
        except Exception as e:
            print(f"❌ Error initializing boulder detection: {e}")
            import traceback
            traceback.print_exc()
            boulder_controller = None
            # Change back to server directory in case of error
            try:
                os.chdir(original_dir)
            except:
                pass
    else:
        print("⚠️ Boulder detection modules not available")

def is_localhost_request():
    """Check if request is from localhost"""
    client_ip = request.remote_addr
    host_header = request.headers.get('Host', '')
    
    # Check if IP is localhost
    if client_ip in ['127.0.0.1', '::1', 'localhost']:
        return True
    
    # Check if Host header contains localhost
    if 'localhost' in host_header or '127.0.0.1' in host_header:
        return True
    
    # Check if request is from allowed hosts
    if client_ip in NETWORK_SECURITY['allowed_hosts']:
        return True
    
    return False

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def validate_credentials(mission_id, access_code):
    """Validate user credentials from database"""
    user = User.query.filter_by(mission_id=mission_id).first()
    if user and user.is_active:
        # In a real system, you'd hash the access code
        # For demo purposes, we'll use a simple check
        if access_code == f"{mission_id}@2024":
            return user
    return None

def get_user_by_mission_id(mission_id):
    """Get user by mission ID from database"""
    return User.query.filter_by(mission_id=mission_id).first()

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    mission_id = data.get('missionId')
    access_code = data.get('accessCode')

    # Validate user credentials
    user = validate_credentials(mission_id, access_code)
    if user:
        # Update last login
        user.last_login = datetime.datetime.utcnow()
        db.session.commit()
        
        # Generate JWT token
        payload = {
            'missionId': mission_id,
            'user_id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24),
            'iat': datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
        ACTIVE_TOKENS.add(token)
        
        # Log login event
        log_system_event('INFO', 'auth', f'User {mission_id} logged in successfully', user.id)
        
        return jsonify({
            "success": True, 
            "message": "Login successful!",
            "token": token,
            "user": {
                "missionId": mission_id,
                "name": user.name,
                "role": user.role,
                "permissions": user.get_permissions()
            }
        }), 200
    else:
        log_system_event('WARNING', 'auth', f'Failed login attempt for mission_id: {mission_id}')
        return jsonify({"success": False, "message": "Invalid credentials."}), 401

@app.route('/logout', methods=['POST'])
def logout():
    data = request.get_json()
    token = data.get('token')
    
    if token and token in ACTIVE_TOKENS:
        ACTIVE_TOKENS.remove(token)
        log_system_event('INFO', 'auth', 'User logged out successfully')
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
            if user_info and user_info.is_active:
                return jsonify({
                    "valid": True, 
                    "user": {
                        "missionId": payload['missionId'],
                        "name": user_info.name,
                        "role": user_info.role,
                        "permissions": user_info.get_permissions()
                    }
                }), 200
            else:
                return jsonify({"valid": False, "message": "User not found or inactive."}), 401
        else:
            return jsonify({"valid": False, "message": "Token has been revoked."}), 401
            
    except jwt.ExpiredSignatureError:
        return jsonify({"valid": False, "message": "Token has expired."}), 401
    except jwt.InvalidTokenError:
        return jsonify({"valid": False, "message": "Invalid token."}), 401

# Database API Endpoints

@app.route('/api/analytics/summary', methods=['GET'])
def analytics_summary():
    """Get analytics summary for dashboard"""
    try:
        summary = db_get_analytics_summary()
        return jsonify({
            "success": True,
            "data": summary
        }), 200
    except Exception as e:
        log_system_event('ERROR', 'analytics', f'Error getting analytics summary: {str(e)}')
        return jsonify({
            "success": False,
            "message": "Error retrieving analytics data"
        }), 500

@app.route('/api/analyses', methods=['GET'])
def get_analyses():
    """Get all analyses with pagination"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        user_id = request.args.get('user_id', type=int)
        
        query = Analysis.query
        
        if user_id:
            query = query.filter_by(user_id=user_id)
        
        analyses = query.order_by(Analysis.created_at.desc())\
            .paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            "success": True,
            "data": {
                "analyses": [analysis.to_dict() for analysis in analyses.items],
                "total": analyses.total,
                "pages": analyses.pages,
                "current_page": page,
                "per_page": per_page
            }
        }), 200
        
    except Exception as e:
        log_system_event('ERROR', 'api', f'Error getting analyses: {str(e)}')
        return jsonify({
            "success": False,
            "message": "Error retrieving analyses"
        }), 500

@app.route('/api/analyses/<int:analysis_id>', methods=['GET'])
def get_analysis_details(analysis_id):
    """Get detailed analysis with all related data"""
    try:
        analysis_data = get_analysis_with_details(analysis_id)
        
        if not analysis_data:
            return jsonify({
                "success": False,
                "message": "Analysis not found"
            }), 404
        
        return jsonify({
            "success": True,
            "data": analysis_data
        }), 200
        
    except Exception as e:
        log_system_event('ERROR', 'api', f'Error getting analysis {analysis_id}: {str(e)}')
        return jsonify({
            "success": False,
            "message": "Error retrieving analysis details"
        }), 500

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
    
    # Get user from token
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    user = None
    if token:
        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            user = get_user_by_mission_id(payload['missionId'])
        except:
            pass
    
    if not filepath or not os.path.exists(filepath):
        return jsonify({"success": False, "message": "Image file not found"}), 400
    
    try:
        # Log analysis start
        if user:
            log_system_event('INFO', 'analysis', f'Starting {analysis_type} analysis for {filepath}', user.id)
        
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
        analysis_start_time = time.time()
        detected_objects = boulder_controller.detect_boulders(absolute_filepath)
        analysis_processing_time = round(time.time() - analysis_start_time, 3)
        print(f"🔍 Detection completed in {analysis_processing_time}s. Found {len(detected_objects) if detected_objects else 0} objects")
        
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
        
        # Keep original objects for boulder detection functions, convert to dicts for response
        original_objects = detected_objects.copy()
        
        # Convert objects to serializable format for response
        processed_objects = []
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
                
                # Only add objects with meaningful data (confidence > 0 and valid measurements)
                if obj_data["confidence"] > 0.0 and obj_data["diameter_real"] > 0.0:
                    processed_objects.append(obj_data)
                    print(f"✅ Object {i+1} processed successfully")
                else:
                    print(f"⚠️ Object {i+1} skipped - no meaningful data (confidence: {obj_data['confidence']}, diameter: {obj_data['diameter_real']})")
                
            except Exception as e:
                print(f"❌ Error processing object {i+1}: {e}")
                # Skip this object instead of adding empty data
                continue
        
        results["detected_objects"] = processed_objects
        
        # Add comprehensive analysis summary
        total_objects = len(results["detected_objects"])  # Use filtered results
        boulders = [obj for obj in results["detected_objects"] if obj.get('class_name', '') == 'boulder']
        
        try:
            results["analysis_summary"] = {
                "total_objects": total_objects,
                "boulder_count": len(boulders),
                "average_confidence": float(sum(obj.get('confidence', 0.0) for obj in results["detected_objects"]) / total_objects) if total_objects > 0 else 0,
                "average_diameter": float(sum(obj.get('diameter_real', 0.0) for obj in results["detected_objects"]) / total_objects) if total_objects > 0 else 0,
                "average_area": float(sum(obj.get('area_real', 0.0) for obj in results["detected_objects"]) / total_objects) if total_objects > 0 else 0,
                "total_volume": float(sum(obj.get('volume_real', 0.0) for obj in results["detected_objects"])),
                "average_circularity": float(sum(obj.get('circularity', 0.0) for obj in results["detected_objects"]) / total_objects) if total_objects > 0 else 0,
                "average_elongation": float(sum(obj.get('elongation', 0.0) for obj in results["detected_objects"]) / total_objects) if total_objects > 0 else 0,
                "processing_time": analysis_processing_time,
                "analysis_type": analysis_type,
                "image_filename": os.path.basename(absolute_filepath)
            }
        except Exception as e:
            print(f"❌ Error calculating analysis summary: {e}")
            results["analysis_summary"] = {
                "total_objects": total_objects,
                "boulder_count": len(boulders),
                "average_confidence": 0.0,
                "average_diameter": 0.0,
                "average_area": 0.0,
                "total_volume": 0.0,
                "average_circularity": 0.0,
                "average_elongation": 0.0,
                "processing_time": analysis_processing_time,
                "analysis_type": analysis_type,
                "image_filename": os.path.basename(absolute_filepath)
            }
        
        # Perform additional analysis based on type
        if analysis_type in ['advanced', 'full']:
            # Calculate measurements
            results["detected_objects"] = boulder_controller.calculate_measurements(results["detected_objects"])
        
        if analysis_type in ['gradcam', 'full']:
            # Generate Grad-CAM
            print(f"🔍 Generating Grad-CAM for analysis type: {analysis_type}")
            gradcam_path = boulder_controller.generate_gradcam(absolute_filepath, original_objects)
            print(f"🔍 Grad-CAM path returned: {gradcam_path}")
            if gradcam_path:
                # Move/copy the Grad-CAM image to uploads folder
                import shutil
                uploads_dir = os.path.join(os.path.dirname(__file__), 'uploads')
                gradcam_filename = os.path.basename(gradcam_path)
                uploads_gradcam_path = os.path.join(uploads_dir, gradcam_filename)
                
                # Make sure the gradcam path is absolute
                if not os.path.isabs(gradcam_path):
                    # If it's relative, it's relative to the boulder_detection directory
                    boulder_dir = os.path.join(os.path.dirname(__file__), '..', 'boulder_detection')
                    gradcam_path = os.path.join(boulder_dir, gradcam_path)
                
                print(f"🔍 Original gradcam_path: {gradcam_path}")
                print(f"🔍 Uploads gradcam_path: {uploads_gradcam_path}")
                print(f"🔍 Gradcam path exists: {os.path.exists(gradcam_path)}")
                
                if os.path.exists(gradcam_path) and os.path.abspath(gradcam_path) != os.path.abspath(uploads_gradcam_path):
                    shutil.copyfile(gradcam_path, uploads_gradcam_path)
                    print(f"✅ Grad-CAM file copied to uploads folder")
                elif os.path.exists(gradcam_path):
                    print(f"✅ Grad-CAM file already in uploads folder")
                else:
                    print(f"❌ Grad-CAM file not found at: {gradcam_path}")
                # Return the path as /uploads/filename for frontend
                results["additional_files"].append({
                    "type": "gradcam",
                    "path": f"/uploads/{gradcam_filename}"
                })
                results["gradcam_path"] = f"/uploads/{gradcam_filename}"
                print(f"✅ Grad-CAM added to results with path: /uploads/{gradcam_filename}")
                print(f"🔍 Grad-CAM full URL would be: http://localhost:5000{results['gradcam_path']}")
            else:
                print("❌ Grad-CAM generation failed - no path returned")
        
        # Always create detection visualization
        viz_path = boulder_controller.create_visualization(absolute_filepath, original_objects)
        if viz_path:
            # Move/copy the visualization image to uploads folder
            import shutil
            uploads_dir = os.path.join(os.path.dirname(__file__), 'uploads')
            viz_filename = os.path.basename(viz_path)
            uploads_viz_path = os.path.join(uploads_dir, viz_filename)
            
            # Make sure the visualization path is absolute
            if not os.path.isabs(viz_path):
                # If it's relative, it's relative to the boulder_detection directory
                boulder_dir = os.path.join(os.path.dirname(__file__), '..', 'boulder_detection')
                viz_path = os.path.join(boulder_dir, viz_path)
            
            print(f"🔍 Original viz_path: {viz_path}")
            print(f"🔍 Uploads viz_path: {uploads_viz_path}")
            print(f"🔍 Viz path exists: {os.path.exists(viz_path)}")
            
            if os.path.exists(viz_path) and os.path.abspath(viz_path) != os.path.abspath(uploads_viz_path):
                shutil.copyfile(viz_path, uploads_viz_path)
                print(f"✅ Visualization file copied to uploads folder")
            elif os.path.exists(viz_path):
                print(f"✅ Visualization file already in uploads folder")
            else:
                print(f"❌ Visualization file not found at: {viz_path}")
            
            # Return the path as /uploads/filename for frontend
            results["additional_files"].append({
                "type": "visualization",
                "path": f"/uploads/{viz_filename}"
            })
            results["visualization_path"] = f"/uploads/{viz_filename}"
            print(f"🔍 Visualization path set to: {results['visualization_path']}")
            print(f"🔍 Full URL would be: http://localhost:5000{results['visualization_path']}")
            print(f"🔍 Additional files: {results['additional_files']}")
        else:
            print("❌ Visualization creation failed - no path returned")
        
        # Calculate density analysis
        density_analysis = boulder_controller.calculate_density_analysis(original_objects, absolute_filepath)
        results["density_analysis"] = density_analysis
        
        # Save to database if user is authenticated
        if user:
            try:
                # Prepare data for database
                db_data = {
                    'analysis_type': analysis_type,
                    'image_filename': os.path.basename(absolute_filepath),
                    'image_path': absolute_filepath,
                    'processing_time': results["analysis_summary"]["processing_time"],
                    'total_objects': results["analysis_summary"]["total_objects"],
                    'boulder_count': results["analysis_summary"]["boulder_count"],
                    'average_confidence': results["analysis_summary"]["average_confidence"],
                    'average_diameter': results["analysis_summary"]["average_diameter"],
                    'average_area': results["analysis_summary"]["average_area"],
                    'total_volume': results["analysis_summary"]["total_volume"],
                    'average_circularity': results["analysis_summary"]["average_circularity"],
                    'average_elongation': results["analysis_summary"]["average_elongation"],
                    'visualization_path': results.get("visualization_path"),
                    'gradcam_path': results.get("gradcam_path"),
                    'detected_objects': results["detected_objects"],
                    'density_analysis': results["density_analysis"]
                }
                
                analysis_record = create_analysis_record(user.id, db_data)
                results["analysis_id"] = analysis_record.id
                
                # Log successful analysis
                log_system_event('INFO', 'analysis', f'Analysis completed successfully. ID: {analysis_record.id}', user.id, analysis_record.id)
                
            except Exception as e:
                print(f"❌ Error saving to database: {e}")
                log_system_event('ERROR', 'database', f'Error saving analysis to database: {str(e)}', user.id)
        
        return jsonify(results), 200
        
    except Exception as e:
        print(f"❌ Error during analysis: {str(e)}")
        import traceback
        traceback.print_exc()
        
        # Log error
        if user:
            log_system_event('ERROR', 'analysis', f'Analysis failed: {str(e)}', user.id)
        
        return jsonify({
            "success": False,
            "message": f"Error during analysis: {str(e)}",
            "error_details": str(e)
        }), 500

@app.route('/uploads/<filename>')
def serve_upload(filename):
    """Serve uploaded files"""
    uploads_dir = os.path.join(os.path.dirname(__file__), app.config['UPLOAD_FOLDER'])
    print(f"🔍 Serving file: {filename} from directory: {uploads_dir}")
    print(f"🔍 File exists: {os.path.exists(os.path.join(uploads_dir, filename))}")
    
    # Set proper headers for images
    response = send_from_directory(uploads_dir, filename)
    
    # Set proper content type for images
    if filename.lower().endswith('.png'):
        response.headers['Content-Type'] = 'image/png'
    elif filename.lower().endswith('.jpg') or filename.lower().endswith('.jpeg'):
        response.headers['Content-Type'] = 'image/jpeg'
    elif filename.lower().endswith('.gif'):
        response.headers['Content-Type'] = 'image/gif'
    
    return response

@app.route('/api/boulder/status', methods=['GET'])
def boulder_status():
    """Check boulder detection system status"""
    return jsonify({
        "available": BOULDER_DETECTION_AVAILABLE,
        "initialized": boulder_controller is not None,
        "models_loaded": boulder_controller is not None
    }), 200

@app.route('/api/test/files', methods=['GET'])
def test_files():
    """Test endpoint to list available files"""
    uploads_dir = os.path.join(os.path.dirname(__file__), app.config['UPLOAD_FOLDER'])
    files = []
    if os.path.exists(uploads_dir):
        for filename in os.listdir(uploads_dir):
            file_path = os.path.join(uploads_dir, filename)
            if os.path.isfile(file_path):
                files.append({
                    "filename": filename,
                    "path": f"/uploads/{filename}",
                    "full_url": f"http://localhost:5000/uploads/{filename}",
                    "size": os.path.getsize(file_path)
                })
    return jsonify({
        "uploads_directory": uploads_dir,
        "files": files
    }), 200

@app.route('/api/test/image/<filename>', methods=['GET'])
def test_image(filename):
    """Test endpoint to serve a specific image with debugging"""
    uploads_dir = os.path.join(os.path.dirname(__file__), app.config['UPLOAD_FOLDER'])
    file_path = os.path.join(uploads_dir, filename)
    
    print(f"🔍 Testing image: {filename}")
    print(f"🔍 Full path: {file_path}")
    print(f"🔍 File exists: {os.path.exists(file_path)}")
    
    if os.path.exists(file_path):
        response = send_from_directory(uploads_dir, filename)
        if filename.lower().endswith('.png'):
            response.headers['Content-Type'] = 'image/png'
        return response
    else:
        return jsonify({"error": "File not found", "path": file_path}), 404

@app.route('/api/lunar-analysis', methods=['POST', 'OPTIONS'])
def run_lunar_analysis():
    print(f"🔍 Lunar analysis endpoint called with method: {request.method}")
    
    # Handle preflight OPTIONS request
    if request.method == 'OPTIONS':
        return ('', 204)
    
    # Handle actual POST request
    print("🔍 Handling POST request for lunar analysis")
    import subprocess
    from pathlib import Path
    import traceback

    # Optionally get DEM path from request
    data = request.get_json() or {}
    dem_path = data.get('dem_path', None)
    print(f"🔍 Received data: {data}")
    print(f"🔍 DEM path: {dem_path}")
    
    # Path to lunar_main.py (adjust if needed)
    script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'detection_qgis', 'processed', 'lunar_main.py'))
    qgis_python = os.environ.get('QGIS_PYTHON', r'C:\Program Files\QGIS 3.40.9\bin\python-qgis-ltr.bat')
    lunalens_dem_dir = os.environ.get(
        'LUNALENS_DEM_DIR',
        os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'dem'))
    )
    
    # Build command with proper path handling
    cmd = [qgis_python, script_path]
    if dem_path:
        # Handle different path scenarios
        original_dem_path = dem_path
        
        # If it's just a filename, try to find it in common locations
        if not os.path.dirname(dem_path) or os.path.dirname(dem_path) == '.':
            possible_paths = [
                os.path.abspath(dem_path),
                os.path.join(os.path.dirname(__file__), dem_path),
                os.path.join(os.path.dirname(__file__), '..', '..', dem_path),
                os.path.join(lunalens_dem_dir, dem_path),
                os.path.join(os.getcwd(), dem_path),
            ]
            
            print(f"🔍 Searching for file '{dem_path}' in common locations...")
            for path in possible_paths:
                print(f"🔍 Checking: {path}")
                if os.path.exists(path):
                    dem_path = path
                    print(f"✅ Found file at: {dem_path}")
                    break
            else:
                # File not found in common locations
                return jsonify({
                    "success": False,
                    "error": f"DEM file '{original_dem_path}' not found. Please provide the full path to the file.",
                    "dem_path": original_dem_path,
                    "searched_locations": possible_paths
                }), 400
        else:
            # It's a full path, use as-is
            dem_path = os.path.abspath(dem_path)
            print(f"🔍 Using full DEM path: {dem_path}")
            print(f"🔍 DEM file exists: {os.path.exists(dem_path)}")
            
            # Check if file exists
            if not os.path.exists(dem_path):
                return jsonify({
                    "success": False,
                    "error": f"DEM file not found at the specified path: {dem_path}",
                    "dem_path": dem_path
                }), 400
        
        print(f"✅ File found at: {dem_path}")
        cmd.append(dem_path)

    # Run the analysis script
    try:
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        
        # Change to the script directory so it can find the modules
        script_dir = os.path.dirname(script_path)
        
        print(f"🔍 Running command: {cmd}")
        print(f"🔍 This may take several hours for a 15GB file...")
        
        # For large files, run in background and provide progress updates
        if dem_path and os.path.exists(dem_path):
            file_size_gb = os.path.getsize(dem_path) / (1024**3)
            if file_size_gb > 5:  # Large file threshold
                print(f"🔍 Large file detected ({file_size_gb:.1f}GB) - processing will take several hours")
                print(f"🔍 Estimated time: 3-6 hours based on file size")
                print(f"🔍 Progress will be saved to progress_info.json")
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            encoding='utf-8',
            check=True,
            env=env,
            cwd=script_dir,
            shell=False,
        )
        print(f"Script stdout: {result.stdout}")
        print(f"Script stderr: {result.stderr}")
    except subprocess.CalledProcessError as e:
        print(f"Script stdout: {e.stdout}")
        print(f"Script stderr: {e.stderr}")
        return jsonify({
            "success": False, 
            "error": e.stderr or "Script failed with no error message",
            "stdout": e.stdout,
            "stderr": e.stderr,
            "traceback": traceback.format_exc()
        }), 500
    except Exception as e:
        return jsonify({
            "success": False, 
            "error": str(e), 
            "traceback": traceback.format_exc()
        }), 500

    # Read all JSON results
    try:
        json_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'detection_qgis', 'processed', 'json_results'))
        results = {}
        for fname in os.listdir(json_dir):
            if fname.endswith('.json'):
                fpath = os.path.join(json_dir, fname)
                try:
                    with open(fpath, 'r', encoding='utf-8') as f:
                        results[fname] = json.load(f)
                except Exception as ex:
                    results[fname] = {"error": f"Could not parse: {str(ex)}"}
        return jsonify({"success": True, "results": results})

    except Exception as e:
        return jsonify({
            "success": False, 
            "error": str(e), 
            "traceback": traceback.format_exc()
        }), 500

@app.route('/api/lunar-analysis/progress', methods=['GET'])
def get_lunar_analysis_progress():
    """Get progress information for lunar analysis"""
    try:
        json_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'detection_qgis', 'processed', 'json_results'))
        progress_file = os.path.join(json_dir, 'progress_info.json')
        
        if os.path.exists(progress_file):
            with open(progress_file, 'r', encoding='utf-8') as f:
                progress_data = json.load(f)
            
            return jsonify({
                "success": True,
                "progress": progress_data
            })
        else:
            return jsonify({
                "success": False,
                "message": "No progress information available"
            }), 404
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

if __name__ == '__main__':
    # Initialize boulder detection system
    init_boulder_detection()
    
    # Get server configuration from security settings
    server_config = get_server_config()
    
    # Print security status
    print_security_status()
    
    # Start server with security configuration
    print(f"🚀 Starting Flask server on {server_config['host']}:{server_config['port']}")
    print(f"🔒 Access URL: http://localhost:{server_config['port']}")
    
    app.run(
        host=server_config['host'], 
        port=server_config['port'], 
        debug=True
    )
