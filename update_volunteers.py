#!/usr/bin/env python3
"""
Update volunteers list - keep Stephanie, replace others
"""

from app_new import create_app
from models import db, Volunteer

def update_volunteers():
    """Remove old volunteers and add new ones"""
    app = create_app()
    
    with app.app_context():
        # Delete all volunteers except Stephanie Alexander
        volunteers_to_delete = Volunteer.query.filter(
            Volunteer.email != 'salexander442@gmail.com'
        ).all()
        
        for vol in volunteers_to_delete:
            print(f"🗑️  Deleting: {vol.first_name} {vol.last_name}")
            db.session.delete(vol)
        
        db.session.commit()
        print()
        
        # New volunteers to add
        new_volunteers = [
            {
                'first_name': 'Neal',
                'last_name': 'Smith',
                'email': 'neal.smith@example.com',
                'phone': '+1 555-0201',
                'status': 'active'
            },
            {
                'first_name': 'Jim',
                'last_name': 'Aversa',
                'email': 'jim.aversa@example.com',
                'phone': '+1 555-0202',
                'status': 'active'
            },
            {
                'first_name': 'Gabby',
                'last_name': 'Edigio',
                'email': 'gabby.edigio@example.com',
                'phone': '+1 555-0203',
                'status': 'active'
            },
            {
                'first_name': 'Erika',
                'last_name': 'Rodriguez',
                'email': 'erika.rodriguez@example.com',
                'phone': '+1 555-0204',
                'status': 'active'
            },
            {
                'first_name': 'Anne',
                'last_name': 'Mehn',
                'email': 'anne.mehn@example.com',
                'phone': '+1 555-0205',
                'status': 'active'
            },
            {
                'first_name': 'Paola',
                'last_name': 'London',
                'email': 'paola.london@example.com',
                'phone': '+1 555-0206',
                'status': 'active'
            },
            {
                'first_name': 'Leon',
                'last_name': 'Fascovich',
                'email': 'leon.fascovich@example.com',
                'phone': '+1 555-0207',
                'status': 'active'
            },
            {
                'first_name': 'Ari',
                'last_name': 'Lopez',
                'email': 'ari.lopez@example.com',
                'phone': '+1 555-0208',
                'status': 'active'
            }
        ]
        
        # Add new volunteers
        for vol_data in new_volunteers:
            volunteer = Volunteer(**vol_data)
            db.session.add(volunteer)
            print(f"✅ Added: {vol_data['first_name']} {vol_data['last_name']}")
        
        db.session.commit()
        
        print()
        print("=" * 50)
        print("✅ Volunteers updated successfully!")
        print("=" * 50)
        print()
        
        # Show final list
        all_volunteers = Volunteer.query.order_by(Volunteer.last_name, Volunteer.first_name).all()
        print("Current volunteers in database:")
        for i, vol in enumerate(all_volunteers, 1):
            print(f"  {i}. {vol.first_name} {vol.last_name} - {vol.email}")
        
        print()
        print(f"Total: {len(all_volunteers)} volunteers")
        print()

if __name__ == '__main__':
    update_volunteers()
