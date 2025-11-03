#!/usr/bin/env python3
"""
Update event names to use abbreviations
"""

from app_new import create_app
from models import db, Evaluation

def fix_event_names():
    """Update event names to abbreviations"""
    app = create_app()
    
    with app.app_context():
        # Update Weeklong Retreat to WLR
        evaluations = Evaluation.query.filter_by(event_name='Weeklong Retreat').all()
        
        print("=" * 50)
        print("Updating Event Names")
        print("=" * 50)
        print()
        
        for eval in evaluations:
            print(f"Updating evaluation {eval.evaluation_id}")
            print(f"  Old: Weeklong Retreat")
            print(f"  New: WLR")
            eval.event_name = 'WLR'
        
        db.session.commit()
        
        print()
        print("=" * 50)
        print(f"✅ Updated {len(evaluations)} evaluations")
        print("=" * 50)
        print()

if __name__ == '__main__':
    fix_event_names()
