from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from models import db, Evaluation, Volunteer, Role, Event
from datetime import datetime

evaluation_bp = Blueprint('evaluation', __name__, url_prefix='/evaluate')

@evaluation_bp.route('/', methods=['GET'])
def evaluation_form():
    """Display the public evaluation form"""
    volunteers = Volunteer.query.filter_by(status='Active').order_by(Volunteer.last_name).all()
    roles = Role.query.all()
    events = Event.query.order_by(Event.event_date.desc()).limit(20).all()
    
    return render_template('evaluation-form.html', 
                         volunteers=volunteers,
                         roles=roles,
                         events=events)

@evaluation_bp.route('/submit', methods=['POST'])
def submit_evaluation():
    """Handle evaluation form submission"""
    try:
        data = request.form
        
        # Generate evaluation ID
        last_eval = Evaluation.query.order_by(Evaluation.id.desc()).first()
        eval_number = (last_eval.id + 1) if last_eval else 1
        evaluation_id = f"EVAL-{eval_number:05d}"
        
        # Create evaluation
        evaluation = Evaluation(
            evaluation_id=evaluation_id,
            volunteer_id=int(data['volunteer_id']),
            role_id=int(data['role_id']),
            event_id=int(data['event_id']) if data.get('event_id') else None,
            date_of_service=datetime.strptime(data['date_of_service'], '%Y-%m-%d').date(),
            reliability=int(data['reliability']),
            quality_of_work=int(data['quality_of_work']),
            initiative=int(data['initiative']),
            teamwork=int(data['teamwork']),
            communication=int(data['communication']),
            strengths=data.get('strengths', ''),
            areas_for_improvement=data.get('areas_for_improvement', ''),
            additional_comments=data.get('additional_comments', ''),
            evaluator_name=data['evaluator_name'],
            evaluator_email=data.get('evaluator_email', '')
        )
        
        db.session.add(evaluation)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Evaluation submitted successfully!',
            'evaluation_id': evaluation_id
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Error submitting evaluation: {str(e)}'
        }), 400

@evaluation_bp.route('/success')
def success():
    """Thank you page after submission"""
    return render_template('success.html')
