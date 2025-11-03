#!/usr/bin/env python3
"""
Reset the admin password
"""

from app_new import create_app
from models import db, User

def reset_admin_password():
    """Reset admin password to admin123"""
    app = create_app()
    
    with app.app_context():
        # Find admin user
        admin = User.query.filter_by(username='admin').first()
        
        if not admin:
            print("❌ Admin user not found! Creating new admin...")
            admin = User(username='admin', role='admin')
            db.session.add(admin)
        
        # Reset password
        admin.set_password('admin123')
        db.session.commit()
        
        print("✅ Admin password reset successfully!")
        print()
        print("=" * 50)
        print("LOGIN CREDENTIALS:")
        print("=" * 50)
        print("Username: admin")
        print("Password: admin123")
        print("=" * 50)
        print()
        print("📍 Login at: http://localhost:5001/login")
        print()

if __name__ == '__main__':
    reset_admin_password()
