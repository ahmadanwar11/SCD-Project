"""
Database Initialization Script
Run this file to create all database tables
Command: python init_db.py
"""

from app import app, db
from models import User, Patient, Doctor, Medicine, Reminder

def init_database():
    """Initialize the database and create all tables"""
    with app.app_context():
        # Drop all existing tables (optional - uncomment if you want fresh start)
        # db.drop_all()
        # print("Dropped all existing tables")

        # Create all tables
        db.create_all()
        print("[OK] Database tables created successfully!")
        print("\nTables created:")
        print("  - users")
        print("  - patients")
        print("  - doctors")
        print("  - medicines")
        print("  - reminders")
        print("\nDatabase is ready to use!")
        print(f"Database location: {app.config['SQLITE_DB_PATH']}")


if __name__ == '__main__':
    print("Initializing Medicine Reminder System Database...")
    print("=" * 50)
    init_database()
    print("=" * 50)
    print("\nYou can now start the application with: python app.py")
