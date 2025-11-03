#!/usr/bin/env python3
"""
Create an admin user for the Volunteer Evaluation System
Run this script to create your first admin account
"""

from app_new import create_app
from models import db, User

def create_admin_user():
    """Create an admin user"""
    app = create_app()
    
    with app.app_context():
        # Check if admin already exists
        existing_admin = User.query.filter_by(username='admin').first()
        
        if existing_admin:
            print("❌ Admin user already exists!")
            print(f"   Username: admin")
            print(f"   Role: {existing_admin.role}")
            return
        
        # Create new admin user
        admin = User(
            username='admin',
            role='admin'
        )
        admin.set_password('admin123')  # Change this password after first login!
        
        db.session.add(admin)
        db.session.commit()
        
        print("✅ Admin user created successfully!")
        print()
        print("=" * 50)
        print("LOGIN CREDENTIALS:")
        print("=" * 50)
        print("Username: admin")
        print("Password: admin123")
        print("=" * 50)
        print()
        print("🔐 IMPORTANT: Change this password after first login!")
        print()
        print("📍 Login at: http://localhost:5001/login")
        print()

if __name__ == '__main__':
    create_admin_user()
