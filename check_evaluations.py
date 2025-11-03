#!/usr/bin/env python3
"""
Check evaluations in the database
"""

from app_new import create_app
from models import db, Evaluation, Volunteer

def check_evaluations():
    """Display all evaluations"""
    app = create_app()
    
    with app.app_context():
        evaluations = Evaluation.query.all()
        
        print("=" * 80)
        print(f"Total Evaluations: {len(evaluations)}")
        print("=" * 80)
        print()
        
        for eval in evaluations:
            volunteer = Volunteer.query.get(eval.volunteer_id)
            print(f"Evaluation ID: {eval.evaluation_id}")
            print(f"Volunteer: {volunteer.first_name} {volunteer.last_name}")
            print(f"Role Performed: {eval.role_performed}")
            print(f"Event: {eval.event_name}")
            print(f"Service Month/Year: {eval.service_month}/{eval.service_year}")
            print(f"Evaluator: {eval.evaluator_name} ({eval.evaluator_role})")
            print(f"Ratings:")
            print(f"  - Reliability: {eval.reliability}")
            print(f"  - Quality: {eval.quality_of_work}")
            print(f"  - Initiative: {eval.initiative}")
            print(f"  - Teamwork: {eval.teamwork}")
            print(f"  - Communication: {eval.communication}")
            overall = (eval.reliability + eval.quality_of_work + eval.initiative + eval.teamwork + eval.communication) / 5
            print(f"  - Overall: {overall:.1f}")
            print(f"Submitted: {eval.submitted_at}")
            print("-" * 80)
            print()

if __name__ == '__main__':
    check_evaluations()
