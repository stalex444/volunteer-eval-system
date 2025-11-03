#!/usr/bin/env python3
"""
Add real volunteers to the database
Run this after creating a fresh database
"""

from app_new import create_app
from models import db, Volunteer

def add_volunteers():
    """Add real volunteer data"""
    app = create_app()
    
    with app.app_context():
        # Real volunteers data
        volunteers_data = [
            {
                'first_name': 'Stephanie',
                'last_name': 'Alexander',
                'email': 'salexander442@gmail.com',
                'phone': '+1 850-459-9999',
                'status': 'active'
            },
            {
                'first_name': 'John',
                'last_name': 'Smith',
                'email': 'john.smith@example.com',
                'phone': '+1 555-0101',
                'status': 'active'
            },
            {
                'first_name': 'Sarah',
                'last_name': 'Johnson',
                'email': 'sarah.j@example.com',
                'phone': '+1 555-0102',
                'status': 'active'
            },
            {
                'first_name': 'Michael',
                'last_name': 'Chen',
                'email': 'mchen@example.com',
                'phone': '+1 555-0103',
                'status': 'active'
            },
            {
                'first_name': 'Emily',
                'last_name': 'Davis',
                'email': 'emily.davis@example.com',
                'phone': '+1 555-0104',
                'status': 'active'
            },
            {
                'first_name': 'David',
                'last_name': 'Rodriguez',
                'email': 'drodriguez@example.com',
                'phone': '+1 555-0105',
                'status': 'active'
            },
            {
                'first_name': 'Lisa',
                'last_name': 'Kim',
                'email': 'lisa.kim@example.com',
                'phone': '+1 555-0106',
                'status': 'active'
            },
            {
                'first_name': 'James',
                'last_name': 'Wilson',
                'email': 'jwilson@example.com',
                'phone': '+1 555-0107',
                'status': 'active'
            },
            {
                'first_name': 'Maria',
                'last_name': 'Garcia',
                'email': 'maria.g@example.com',
                'phone': '+1 555-0108',
                'status': 'active'
            },
            {
                'first_name': 'Robert',
                'last_name': 'Taylor',
                'email': 'rtaylor@example.com',
                'phone': '+1 555-0109',
                'status': 'active'
            }
        ]
        
        # Add volunteers to database
        added_count = 0
        for vol_data in volunteers_data:
            # Check if volunteer already exists
            existing = Volunteer.query.filter_by(email=vol_data['email']).first()
            if existing:
                print(f"⚠️  {vol_data['first_name']} {vol_data['last_name']} already exists, skipping...")
                continue
            
            volunteer = Volunteer(**vol_data)
            db.session.add(volunteer)
            added_count += 1
            print(f"✅ Added: {vol_data['first_name']} {vol_data['last_name']}")
        
        db.session.commit()
        
        print()
        print("=" * 50)
        print(f"✅ Successfully added {added_count} volunteers!")
        print("=" * 50)
        print()
        print("Total volunteers in database:", Volunteer.query.count())
        print()
        print("🎉 You can now:")
        print("   1. Go to http://localhost:5001/evaluate")
        print("   2. Select volunteers from the dropdown")
        print("   3. Submit evaluations")
        print("   4. View results in the dashboard")
        print()

if __name__ == '__main__':
    add_volunteers()
