from datetime import datetime, timedelta

from flask_migrate import Migrate
from sqlalchemy import inspect, text

from models import Analysis, DensityAnalysis, DetectedObject, SystemLog, User, db

migrate = Migrate()

def init_db(app):
    """Initialize database with Flask app"""
    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        db.create_all()
        ensure_user_email_column()
        init_demo_users()

        print("✅ Database initialized successfully!")

def ensure_user_email_column():
    """Add email column to users table if missing (SQLite backfill)."""
    inspector = inspect(db.engine)
    if 'users' not in inspector.get_table_names():
        return

    columns = {column['name'] for column in inspector.get_columns('users')}
    if 'email' not in columns:
        with db.engine.begin() as connection:
            connection.execute(text('ALTER TABLE users ADD COLUMN email VARCHAR(120)'))
        print("✅ Added email column to users table")

def init_demo_users():
    """Initialize demo users for testing. Password format: {mission_id}@2024"""
    demo_users = [
        {
            'mission_id': 'isro123',
            'email': 'isro123@lunalens.app',
            'name': 'ISRO Mission Control',
            'role': 'admin',
            'password': 'isro123@2024',
            'permissions': ['dashboard', 'analytics', 'settings', 'boulder_detection']
        },
        {
            'mission_id': 'mission001',
            'email': 'mission001@lunalens.app',
            'name': 'Lunar Mission Team',
            'role': 'user',
            'password': 'mission001@2024',
            'permissions': ['dashboard', 'analytics', 'boulder_detection']
        },
        {
            'mission_id': 'research002',
            'email': 'research002@lunalens.app',
            'name': 'Research Team',
            'role': 'researcher',
            'password': 'research002@2024',
            'permissions': ['dashboard', 'analytics', 'data_export', 'boulder_detection']
        },
        {
            'mission_id': 'test001',
            'email': 'test001@lunalens.app',
            'name': 'Test User',
            'role': 'user',
            'password': 'test001@2024',
            'permissions': ['dashboard', 'boulder_detection']
        }
    ]

    for user_data in demo_users:
        existing_user = User.query.filter_by(mission_id=user_data['mission_id']).first()
        if not existing_user:
            user = User(
                mission_id=user_data['mission_id'],
                email=user_data['email'],
                name=user_data['name'],
                role=user_data['role']
            )
            user.set_password(user_data['password'])
            user.set_permissions(user_data['permissions'])
            db.session.add(user)
        elif not existing_user.email:
            existing_user.email = user_data['email']

    for user in User.query.filter(User.email.is_(None)).all():
        user.email = f"{user.mission_id}@lunalens.app"

    try:
        db.session.commit()
        print("✅ Demo users initialized successfully!")
    except Exception as e:
        print(f"❌ Error initializing demo users: {e}")
        db.session.rollback()

def create_analysis_record(user_id, analysis_data):
    """Create a new analysis record in the database"""
    try:
        analysis = Analysis(
            user_id=user_id,
            analysis_type=analysis_data.get('analysis_type', 'basic'),
            image_filename=analysis_data.get('image_filename'),
            image_path=analysis_data.get('image_path'),
            processing_time=analysis_data.get('processing_time', 0.0),
            status='completed',
            total_objects=analysis_data.get('total_objects', 0),
            boulder_count=analysis_data.get('boulder_count', 0),
            average_confidence=analysis_data.get('average_confidence', 0.0),
            average_diameter=analysis_data.get('average_diameter', 0.0),
            average_area=analysis_data.get('average_area', 0.0),
            total_volume=analysis_data.get('total_volume', 0.0),
            average_circularity=analysis_data.get('average_circularity', 0.0),
            average_elongation=analysis_data.get('average_elongation', 0.0),
            visualization_path=analysis_data.get('visualization_path'),
            gradcam_path=analysis_data.get('gradcam_path')
        )

        db.session.add(analysis)
        db.session.flush()  # Get the analysis ID

        # Add detected objects
        detected_objects = analysis_data.get('detected_objects', [])
        for i, obj_data in enumerate(detected_objects):
            detected_obj = DetectedObject(
                analysis_id=analysis.id,
                object_index=i + 1,
                class_name=obj_data.get('class_name', 'unknown'),
                confidence=obj_data.get('confidence', 0.0),
                degradation_state=obj_data.get('degradation_state', 'N/A'),
                width_real=obj_data.get('width_real', 0.0),
                height_real=obj_data.get('height_real', 0.0),
                diameter_real=obj_data.get('diameter_real', 0.0),
                area_real=obj_data.get('area_real', 0.0),
                volume_real=obj_data.get('volume_real', 0.0),
                estimated_depth=obj_data.get('estimated_depth'),
                circularity=obj_data.get('circularity', 0.0),
                elongation=obj_data.get('elongation', 0.0)
            )

            # Set bounding box if available
            if obj_data.get('bounding_box'):
                detected_obj.set_bounding_box(obj_data['bounding_box'])

            # Set pixel measurements if available
            if obj_data.get('pixel_measurements'):
                detected_obj.set_pixel_measurements(obj_data['pixel_measurements'])

            db.session.add(detected_obj)

        # Add density analysis if available
        density_data = analysis_data.get('density_analysis')
        if density_data:
            density_analysis = DensityAnalysis(
                analysis_id=analysis.id,
                total_area=density_data.get('total_area', 0.0),
                boulder_density=density_data.get('boulder_density', 0.0),
                overall_density=density_data.get('density', 0.0)
            )
            db.session.add(density_analysis)

        db.session.commit()
        return analysis

    except Exception as e:
        db.session.rollback()
        print(f"❌ Error creating analysis record: {e}")
        raise

def get_user_analyses(user_id, limit=50, offset=0):
    """Get analyses for a specific user"""
    return Analysis.query.filter_by(user_id=user_id)\
        .order_by(Analysis.created_at.desc())\
        .limit(limit)\
        .offset(offset)\
        .all()

def get_analysis_with_details(analysis_id):
    """Get analysis with all related data"""
    analysis = Analysis.query.get(analysis_id)
    if not analysis:
        return None

    # Convert to dictionary with all details
    analysis_dict = analysis.to_dict()

    # Add detected objects
    analysis_dict['detected_objects'] = [obj.to_dict() for obj in analysis.detected_objects]

    # Add density analysis
    if analysis.density_analysis:
        analysis_dict['density_analysis'] = analysis.density_analysis.to_dict()

    return analysis_dict

def log_system_event(level, category, message, user_id=None, analysis_id=None, additional_data=None):
    """Log system events"""
    try:
        log_entry = SystemLog(
            level=level,
            category=category,
            message=message,
            user_id=user_id,
            analysis_id=analysis_id
        )

        if additional_data:
            log_entry.set_additional_data(additional_data)

        db.session.add(log_entry)
        db.session.commit()

    except Exception as e:
        print(f"❌ Error logging system event: {e}")
        db.session.rollback()

def get_analytics_summary():
    """Get analytics summary for dashboard"""
    try:
        total_analyses = Analysis.query.count()
        total_users = User.query.count()
        recent_analyses = Analysis.query.filter(
            Analysis.created_at >= datetime.utcnow() - timedelta(days=7)
        ).count()

        # Get top users by analysis count
        top_users = db.session.query(
            User.mission_id,
            User.name,
            db.func.count(Analysis.id).label('analysis_count')
        ).join(Analysis).group_by(User.id).order_by(
            db.func.count(Analysis.id).desc()
        ).limit(5).all()

        return {
            'total_analyses': total_analyses,
            'total_users': total_users,
            'recent_analyses': recent_analyses,
            'top_users': [
                {
                    'mission_id': user.mission_id,
                    'name': user.name,
                    'analysis_count': user.analysis_count
                }
                for user in top_users
            ]
        }

    except Exception as e:
        print(f"❌ Error getting analytics summary: {e}")
        return {
            'total_analyses': 0,
            'total_users': 0,
            'recent_analyses': 0,
            'top_users': []
        }
