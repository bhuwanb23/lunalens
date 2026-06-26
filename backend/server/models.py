from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import json

db = SQLAlchemy()

class User(db.Model):
    """User model for authentication and permissions"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    mission_id = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='user')
    password_hash = db.Column(db.String(256), nullable=False)
    permissions = db.Column(db.Text, default='[]')  # JSON string of permissions
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)

    # Relationships
    analyses = db.relationship('Analysis', backref='user', lazy=True)

    def set_password(self, password):
        """Hash and set the user's password"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verify a password against the stored hash"""
        return check_password_hash(self.password_hash, password)

    def get_permissions(self):
        """Get permissions as a list"""
        try:
            return json.loads(self.permissions)
        except (json.JSONDecodeError, TypeError):
            return []

    def set_permissions(self, permissions_list):
        """Set permissions from a list"""
        self.permissions = json.dumps(permissions_list)

    def has_permission(self, permission):
        """Check if user has specific permission"""
        return permission in self.get_permissions()

class Analysis(db.Model):
    """Main analysis record"""
    __tablename__ = 'analyses'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    analysis_type = db.Column(db.String(50), nullable=False, default='basic')
    image_filename = db.Column(db.String(255), nullable=False)
    image_path = db.Column(db.String(500), nullable=False)
    processing_time = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='completed')  # pending, processing, completed, failed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Analysis results
    total_objects = db.Column(db.Integer, default=0)
    boulder_count = db.Column(db.Integer, default=0)
    average_confidence = db.Column(db.Float, default=0.0)
    average_diameter = db.Column(db.Float, default=0.0)
    average_area = db.Column(db.Float, default=0.0)
    total_volume = db.Column(db.Float, default=0.0)
    average_circularity = db.Column(db.Float, default=0.0)
    average_elongation = db.Column(db.Float, default=0.0)
    
    # File paths
    visualization_path = db.Column(db.String(500))
    gradcam_path = db.Column(db.String(500))
    
    # Relationships
    detected_objects = db.relationship('DetectedObject', backref='analysis', lazy=True, cascade='all, delete-orphan')
    density_analysis = db.relationship('DensityAnalysis', backref='analysis', lazy=True, uselist=False, cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert analysis to dictionary for API response"""
        return {
            'id': self.id,
            'analysis_type': self.analysis_type,
            'image_filename': self.image_filename,
            'processing_time': self.processing_time,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'total_objects': self.total_objects,
            'boulder_count': self.boulder_count,
            'average_confidence': self.average_confidence,
            'average_diameter': self.average_diameter,
            'average_area': self.average_area,
            'total_volume': self.total_volume,
            'average_circularity': self.average_circularity,
            'average_elongation': self.average_elongation,
            'visualization_path': self.visualization_path,
            'gradcam_path': self.gradcam_path,
            'user': {
                'mission_id': self.user.mission_id,
                'name': self.user.name,
                'role': self.user.role
            } if self.user else None
        }

class DetectedObject(db.Model):
    """Individual detected object details"""
    __tablename__ = 'detected_objects'
    
    id = db.Column(db.Integer, primary_key=True)
    analysis_id = db.Column(db.Integer, db.ForeignKey('analyses.id'), nullable=False)
    object_index = db.Column(db.Integer, nullable=False)  # Order in detection
    
    # Object properties
    class_name = db.Column(db.String(50), nullable=False)  # boulder, etc.
    confidence = db.Column(db.Float, nullable=False)
    degradation_state = db.Column(db.String(50), default='N/A')
    
    # Real measurements (in meters)
    width_real = db.Column(db.Float, default=0.0)
    height_real = db.Column(db.Float, default=0.0)
    diameter_real = db.Column(db.Float, default=0.0)
    area_real = db.Column(db.Float, default=0.0)
    volume_real = db.Column(db.Float, default=0.0)
    estimated_depth = db.Column(db.Float)
    
    # Shape properties
    circularity = db.Column(db.Float, default=0.0)
    elongation = db.Column(db.Float, default=0.0)
    
    # Bounding box (stored as JSON)
    bounding_box = db.Column(db.Text)  # JSON: {"x1": 100, "y1": 200, "x2": 300, "y2": 400}
    
    # Pixel measurements
    pixel_measurements = db.Column(db.Text)  # JSON: {"width_px": 100, "height_px": 200, "area_px": 20000}
    
    def get_bounding_box(self):
        """Get bounding box as dictionary"""
        try:
            return json.loads(self.bounding_box) if self.bounding_box else None
        except (json.JSONDecodeError, TypeError):
            return None
    
    def set_bounding_box(self, bbox_dict):
        """Set bounding box from dictionary"""
        self.bounding_box = json.dumps(bbox_dict) if bbox_dict else None
    
    def get_pixel_measurements(self):
        """Get pixel measurements as dictionary"""
        try:
            return json.loads(self.pixel_measurements) if self.pixel_measurements else None
        except (json.JSONDecodeError, TypeError):
            return None
    
    def set_pixel_measurements(self, pixel_dict):
        """Set pixel measurements from dictionary"""
        self.pixel_measurements = json.dumps(pixel_dict) if pixel_dict else None
    
    def to_dict(self):
        """Convert object to dictionary for API response"""
        return {
            'id': self.id,
            'object_index': self.object_index,
            'class_name': self.class_name,
            'confidence': self.confidence,
            'degradation_state': self.degradation_state,
            'width_real': self.width_real,
            'height_real': self.height_real,
            'diameter_real': self.diameter_real,
            'area_real': self.area_real,
            'volume_real': self.volume_real,
            'estimated_depth': self.estimated_depth,
            'circularity': self.circularity,
            'elongation': self.elongation,
            'bounding_box': self.get_bounding_box(),
            'pixel_measurements': self.get_pixel_measurements()
        }

class DensityAnalysis(db.Model):
    """Density analysis results"""
    __tablename__ = 'density_analyses'
    
    id = db.Column(db.Integer, primary_key=True)
    analysis_id = db.Column(db.Integer, db.ForeignKey('analyses.id'), nullable=False, unique=True)
    
    # Density calculations
    total_area = db.Column(db.Float, default=0.0)  # Total image area in m²
    boulder_density = db.Column(db.Float, default=0.0)  # boulders per m²
    overall_density = db.Column(db.Float, default=0.0)  # objects per m²
    
    def to_dict(self):
        """Convert density analysis to dictionary"""
        return {
            'id': self.id,
            'total_area': self.total_area,
            'boulder_density': self.boulder_density,
            'overall_density': self.overall_density
        }

class AnalysisSession(db.Model):
    """Track analysis sessions for monitoring"""
    __tablename__ = 'analysis_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    session_id = db.Column(db.String(100), unique=True, nullable=False)
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    status = db.Column(db.String(50), default='active')  # active, completed, failed
    analysis_count = db.Column(db.Integer, default=0)
    
    # Relationships
    user = db.relationship('User', backref='sessions')

class SystemLog(db.Model):
    """System logs for monitoring and debugging"""
    __tablename__ = 'system_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    level = db.Column(db.String(20), nullable=False)  # INFO, WARNING, ERROR, DEBUG
    category = db.Column(db.String(50), nullable=False)  # auth, analysis, system, etc.
    message = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    analysis_id = db.Column(db.Integer, db.ForeignKey('analyses.id'))
    additional_data = db.Column(db.Text)  # JSON string for additional context
    
    def get_additional_data(self):
        """Get additional data as dictionary"""
        try:
            return json.loads(self.additional_data) if self.additional_data else {}
        except (json.JSONDecodeError, TypeError):
            return {}
    
    def set_additional_data(self, data_dict):
        """Set additional data from dictionary"""
        self.additional_data = json.dumps(data_dict) if data_dict else None 