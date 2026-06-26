#!/usr/bin/env python3
"""
Database setup script for LunaLens Backend Server
"""

import os
import sys

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def setup_database():
    """Initialize database and create demo data"""
    try:
        from app import app
        from database import init_demo_users
        from models import db

        print("🚀 Setting up LunaLens Database...")

        with app.app_context():
            # Create all tables
            print("📊 Creating database tables...")
            db.create_all()
            print("✅ Database tables created successfully!")

            # Initialize demo users
            print("👥 Initializing demo users...")
            init_demo_users()
            print("✅ Demo users initialized successfully!")

            # Create logs directory
            logs_dir = os.path.join(os.path.dirname(__file__), 'logs')
            os.makedirs(logs_dir, exist_ok=True)
            print("✅ Logs directory created!")

            print("\n🎉 Database setup completed successfully!")
            print("\n📋 Demo Users:")
            print("  - isro123 / isro123@2024 (Admin)")
            print("  - mission001 / mission001@2024 (Mission Team)")
            print("  - research002 / research002@2024 (Research Team)")
            print("  - test001 / test001@2024 (Test User)")

    except Exception as e:
        print(f"❌ Error setting up database: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

def check_database_connection():
    """Check if database connection is working"""
    try:
        from app import app
        from models import db

        with app.app_context():
            # Try to connect to database
            from sqlalchemy import text
            with db.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("✅ Database connection successful!")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def reset_database():
    """Reset database (drop all tables and recreate)"""
    try:
        from app import app
        from models import db

        print("⚠️  WARNING: This will delete all data!")
        response = input("Are you sure you want to reset the database? (y/N): ")

        if response.lower() != 'y':
            print("❌ Database reset cancelled.")
            return

        with app.app_context():
            print("🗑️  Dropping all tables...")
            db.drop_all()
            print("📊 Recreating tables...")
            db.create_all()
            print("✅ Database reset completed!")

    except Exception as e:
        print(f"❌ Error resetting database: {e}")
        import traceback
        traceback.print_exc()

def show_database_info():
    """Show database information"""
    try:
        from app import app
        from models import Analysis, AnalysisSession, DensityAnalysis, DetectedObject, SystemLog, User

        with app.app_context():
            print("📊 Database Information:")
            print(f"  - Users: {User.query.count()}")
            print(f"  - Analyses: {Analysis.query.count()}")
            print(f"  - Detected Objects: {DetectedObject.query.count()}")
            print(f"  - Density Analyses: {DensityAnalysis.query.count()}")
            print(f"  - Sessions: {AnalysisSession.query.count()}")
            print(f"  - System Logs: {SystemLog.query.count()}")

    except Exception as e:
        print(f"❌ Error getting database info: {e}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="LunaLens Database Setup")
    parser.add_argument("--check", action="store_true", help="Check database connection")
    parser.add_argument("--reset", action="store_true", help="Reset database (drop all tables)")
    parser.add_argument("--info", action="store_true", help="Show database information")

    args = parser.parse_args()

    if args.check:
        check_database_connection()
    elif args.reset:
        reset_database()
    elif args.info:
        show_database_info()
    else:
        setup_database()
