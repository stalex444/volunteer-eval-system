from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime
from models import db, Volunteer, Evaluation
from config import Config

evaluation_bp = Blueprint('evaluation', __name__)

@evaluation_bp.route('/')
def index():
    """Landing page with link to evaluation form"""
    return render_template('evaluation-form.html')

@evaluation_bp.route('/evaluate', methods=['GET', 'POST'])
def submit_evaluation():
    """Public form for submitting volunteer evaluations"""
    if request.method == 'GET':
        volunteers = Volunteer.query.filter_by(status='active').order_by(Volunteer.last_name, Volunteer.first_name).all()
        return render_template('evaluation-form.html', volunteers=volunteers)
    
    # POST - Process form submission
    try:
        volunteer_id = request.form.get('volunteer_id')
        evaluator_name = request.form.get('evaluator_name')
        event_name = request.form.get('event_name')
        
        # Parse evaluation date
        eval_date_str = request.form.get('evaluation_date')
        eval_date = datetime.strptime(eval_date_str, '%Y-%m-%d').date() if eval_date_str else datetime.utcnow().date()
        
        # Check for duplicate evaluation (same volunteer, evaluator, event, and date)
        existing = Evaluation.query.filter_by(
            volunteer_id=volunteer_id,
            evaluator_name=evaluator_name,
            event_name=event_name,
            evaluation_date=eval_date
        ).first()
        
        if existing:
            flash('⚠️ You have already submitted an evaluation for this volunteer at this event on this date. If you need to update it, please contact an administrator.', 'warning')
            volunteers = Volunteer.query.filter_by(status='active').order_by(Volunteer.last_name, Volunteer.first_name).all()
            return render_template('evaluation-form.html', volunteers=volunteers)
        
        # Generate evaluation ID
        last_eval = Evaluation.query.order_by(Evaluation.id.desc()).first()
        eval_number = (last_eval.id + 1) if last_eval else 1
        evaluation_id = f"EVAL-{eval_number:05d}"
        
        # Create new evaluation
        evaluation = Evaluation(
            evaluation_id=evaluation_id,
            volunteer_id=volunteer_id,
            role_id=None,  # Not using role table, using role_performed text field instead
            date_of_service=datetime.utcnow().date(),
            event_name=request.form.get('event_name'),
            service_month=request.form.get('service_month'),
            service_year=request.form.get('service_year'),
            role_performed=request.form.get('role_performed'),
            evaluation_date=eval_date,
            evaluator_name=request.form.get('evaluator_name'),
            evaluator_email=request.form.get('evaluator_email'),
            evaluator_role=request.form.get('evaluator_role'),
            reliability=int(request.form.get('reliability')),
            quality_of_work=int(request.form.get('quality_of_work')),
            initiative=int(request.form.get('initiative')),
            teamwork=int(request.form.get('teamwork')),
            communication=int(request.form.get('communication')),
            strengths=request.form.get('strengths'),
            areas_for_improvement=request.form.get('areas_for_improvement'),
            additional_comments=request.form.get('additional_comments')
        )
        
        db.session.add(evaluation)
        db.session.commit()
        
        flash('Evaluation submitted successfully! Thank you for your feedback.', 'success')
        return redirect(url_for('evaluation.submit_evaluation'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error submitting evaluation: {str(e)}', 'error')
        return redirect(url_for('evaluation.submit_evaluation'))

@evaluation_bp.route('/api/volunteers')
def get_volunteers():
    """API endpoint to get list of active volunteers"""
    volunteers = Volunteer.query.filter_by(status='active').order_by(Volunteer.name).all()
    return jsonify([{
        'id': v.id,
        'name': v.name,
        'department': v.department,
        'role': v.role
    } for v in volunteers])
