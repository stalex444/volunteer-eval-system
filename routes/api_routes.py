from flask import Blueprint, jsonify, request
from flask_login import login_required
from models import db, Volunteer, Evaluation
from datetime import datetime

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/volunteers', methods=['GET'])
@login_required
def get_volunteers():
    """Get all volunteers with optional filtering"""
    status = request.args.get('status')
    department = request.args.get('department')
    
    query = Volunteer.query
    
    if status:
        query = query.filter_by(status=status)
    if department:
        query = query.filter_by(department=department)
    
    volunteers = query.all()
    
    return jsonify([{
        'id': v.id,
        'name': v.name,
        'email': v.email,
        'department': v.department,
        'role': v.role,
        'status': v.status,
        'average_rating': v.average_rating,
        'evaluation_count': v.evaluation_count
    } for v in volunteers])

@api_bp.route('/volunteers/<int:volunteer_id>', methods=['GET'])
@login_required
def get_volunteer(volunteer_id):
    """Get detailed information about a specific volunteer"""
    volunteer = Volunteer.query.get_or_404(volunteer_id)
    
    return jsonify({
        'id': volunteer.id,
        'name': volunteer.name,
        'email': volunteer.email,
        'phone': volunteer.phone,
        'department': volunteer.department,
        'role': volunteer.role,
        'status': volunteer.status,
        'start_date': volunteer.start_date.isoformat() if volunteer.start_date else None,
        'average_rating': volunteer.average_rating,
        'evaluation_count': volunteer.evaluation_count,
        'evaluations': [{
            'id': e.id,
            'evaluator_name': e.evaluator_name,
            'overall_rating': e.overall_rating,
            'evaluation_date': e.evaluation_date.isoformat(),
            'created_at': e.created_at.isoformat()
        } for e in volunteer.evaluations.order_by(Evaluation.evaluation_date.desc()).all()]
    })

@api_bp.route('/evaluations', methods=['GET'])
@login_required
def get_evaluations():
    """Get all evaluations with optional filtering"""
    volunteer_id = request.args.get('volunteer_id', type=int)
    limit = request.args.get('limit', type=int, default=50)
    
    query = Evaluation.query
    
    if volunteer_id:
        query = query.filter_by(volunteer_id=volunteer_id)
    
    evaluations = query.order_by(Evaluation.created_at.desc()).limit(limit).all()
    
    return jsonify([{
        'id': e.id,
        'volunteer_id': e.volunteer_id,
        'volunteer_name': e.volunteer.name,
        'evaluator_name': e.evaluator_name,
        'overall_rating': e.overall_rating,
        'reliability_rating': e.reliability_rating,
        'communication_rating': e.communication_rating,
        'teamwork_rating': e.teamwork_rating,
        'initiative_rating': e.initiative_rating,
        'quality_rating': e.quality_rating,
        'evaluation_date': e.evaluation_date.isoformat(),
        'created_at': e.created_at.isoformat()
    } for e in evaluations])

@api_bp.route('/evaluations/<int:evaluation_id>', methods=['GET'])
@login_required
def get_evaluation(evaluation_id):
    """Get detailed information about a specific evaluation"""
    evaluation = Evaluation.query.get_or_404(evaluation_id)
    
    return jsonify({
        'id': evaluation.id,
        'volunteer': {
            'id': evaluation.volunteer.id,
            'name': evaluation.volunteer.name
        },
        'evaluator_name': evaluation.evaluator_name,
        'evaluator_email': evaluation.evaluator_email,
        'evaluator_role': evaluation.evaluator_role,
        'ratings': {
            'reliability': evaluation.reliability_rating,
            'communication': evaluation.communication_rating,
            'teamwork': evaluation.teamwork_rating,
            'initiative': evaluation.initiative_rating,
            'quality': evaluation.quality_rating,
            'overall': evaluation.overall_rating
        },
        'feedback': {
            'strengths': evaluation.strengths,
            'areas_for_improvement': evaluation.areas_for_improvement,
            'additional_comments': evaluation.additional_comments
        },
        'evaluation_date': evaluation.evaluation_date.isoformat(),
        'created_at': evaluation.created_at.isoformat()
    })

@api_bp.route('/departments', methods=['GET'])
@login_required
def get_departments():
    """Get list of all departments"""
    departments = db.session.query(Volunteer.department).distinct().all()
    return jsonify([d[0] for d in departments if d[0]])
