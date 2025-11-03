#!/usr/bin/env python3
"""
Add a GL viewer (read-only access)
Usage: python add_viewer.py
"""

from app_new import create_app
from models import db, User

def add_viewer():
    """Add a new viewer user (GL with read-only access)"""
    app = create_app()
    
    with app.app_context():
        print("=" * 50)
        print("Add New GL Viewer (Read-Only Access)")
        print("=" * 50)
        print()
        
        username = input("Enter username (e.g., 'john_gl'): ")
        password = input("Enter password: ")
        
        # Check if user already exists
        existing = User.query.filter_by(username=username).first()
        if existing:
            print(f"❌ User '{username}' already exists!")
            return
        
        # Create new viewer user
        user = User(username=username, role='viewer')
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        print()
        print("=" * 50)
        print(f"✅ Viewer user '{username}' created successfully!")
        print("=" * 50)
        print()
        print("This user can:")
        print("  ✓ View dashboard")
        print("  ✓ View volunteer profiles")
        print("  ✓ View all evaluations")
        print("  ✗ Cannot edit volunteers")
        print("  ✗ Cannot delete data")
        print()
        print(f"Login at: http://localhost:5001/login")
        print(f"Username: {username}")
        print(f"Password: {password}")
        print()

if __name__ == '__main__':
    add_viewer()
