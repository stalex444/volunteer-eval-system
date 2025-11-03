#!/usr/bin/env python3
"""
Add a new admin user
Usage: python add_admin.py
"""

from app_new import create_app
from models import db, User

def add_admin():
    """Add a new admin user"""
    app = create_app()
    
    with app.app_context():
        print("=" * 50)
        print("Add New Admin User")
        print("=" * 50)
        print()
        
        username = input("Enter username: ")
        password = input("Enter password: ")
        
        # Check if user already exists
        existing = User.query.filter_by(username=username).first()
        if existing:
            print(f"❌ User '{username}' already exists!")
            return
        
        # Create new admin user
        user = User(username=username, role='admin')
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        print()
        print("=" * 50)
        print(f"✅ Admin user '{username}' created successfully!")
        print("=" * 50)
        print()
        print(f"Login at: http://localhost:5001/login")
        print(f"Username: {username}")
        print(f"Password: {password}")
        print()

if __name__ == '__main__':
    add_admin()
