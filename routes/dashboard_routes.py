from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, Response
from flask_login import login_required, current_user
from sqlalchemy import func
from models import db, Volunteer, Evaluation, User
from utils.analytics import calculate_volunteer_stats, get_department_summary, get_trend_data
from datetime import datetime, timedelta
import csv
from io import StringIO

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard_bp.route('/qr-generator')
@login_required
def qr_generator():
    """QR code generator page"""
    eval_url = url_for('evaluation.submit_evaluation', _external=True)
    return render_template('qr-generator.html', eval_url=eval_url)

@dashboard_bp.route('/')
@login_required
def index():
    """Main leadership dashboard"""
    # Get summary statistics
    total_volunteers = Volunteer.query.filter_by(status='active').count()
    total_evaluations = Evaluation.query.count()
    
    # Recent evaluations
    recent_evaluations = Evaluation.query.order_by(
        Evaluation.submitted_at.desc()
    ).limit(10).all()
    
    # Top performers - calculate from individual ratings
    top_performers = []
    needs_attention = []
    
    # Get all volunteers with evaluations
    volunteers_with_evals = Volunteer.query.join(Evaluation).distinct().all()
    
    for volunteer in volunteers_with_evals:
        evals = Evaluation.query.filter_by(volunteer_id=volunteer.id).all()
        if evals:
            # Calculate average of all 5 ratings
            total_score = 0
            for eval in evals:
                avg = (eval.reliability + eval.quality_of_work + eval.initiative + 
                       eval.teamwork + eval.communication) / 5.0
                total_score += avg
            overall_avg = total_score / len(evals)
            
            if overall_avg >= 8.0:
                top_performers.append({'volunteer': volunteer, 'score': overall_avg})
            elif overall_avg < 6.0:
                needs_attention.append({'volunteer': volunteer, 'score': overall_avg})
    
    # Sort lists
    top_performers = sorted(top_performers, key=lambda x: x['score'], reverse=True)[:10]
    needs_attention = sorted(needs_attention, key=lambda x: x['score'])
    
    # Upcoming events (placeholder)
    upcoming_events = 0
    
    return render_template(
        'dashboard.html',
        total_volunteers=total_volunteers,
        total_evaluations=total_evaluations,
        recent_evaluations=recent_evaluations,
        top_performers=top_performers,
        needs_attention=needs_attention,
        upcoming_events=upcoming_events
    )

@dashboard_bp.route('/volunteer/<int:volunteer_id>')
@login_required
def volunteer_profile(volunteer_id):
    """Detailed view of individual volunteer performance"""
    volunteer = Volunteer.query.get_or_404(volunteer_id)
    stats = calculate_volunteer_stats(volunteer_id)
    trend_data = get_trend_data(volunteer_id)
    
    # Get evaluations ordered by date
    evaluations = Evaluation.query.filter_by(volunteer_id=volunteer_id).order_by(
        Evaluation.submitted_at.desc()
    ).all()
    
    return render_template(
        'volunteer-profile.html',
        volunteer=volunteer,
        stats=stats,
        trend_data=trend_data,
        evaluations=evaluations
    )

@dashboard_bp.route('/volunteers')
@login_required
def volunteers_list():
    """List all volunteers with filtering options"""
    search_query = request.args.get('search', '').strip()
    status = request.args.get('status', 'active')
    
    query = Volunteer.query
    
    # Apply search filter
    if search_query:
        search_pattern = f'%{search_query}%'
        query = query.filter(
            db.or_(
                Volunteer.first_name.ilike(search_pattern),
                Volunteer.last_name.ilike(search_pattern)
            )
        )
    
    # Apply status filter
    if status:
        query = query.filter_by(status=status)
    
    volunteers = query.order_by(Volunteer.last_name, Volunteer.first_name).all()
    
    return render_template(
        'volunteers-list.html',
        volunteers=volunteers,
        search_query=search_query,
        selected_status=status
    )

@dashboard_bp.route('/volunteers/add', methods=['GET', 'POST'])
@login_required
def add_volunteer():
    """Add new volunteer"""
    if request.method == 'POST':
        try:
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            status = request.form.get('status', 'active')
            
            if not first_name or not last_name:
                flash('First name and last name are required', 'error')
                return redirect(url_for('dashboard.add_volunteer'))
            
            # Create volunteer
            volunteer = Volunteer(
                first_name=first_name.strip(),
                last_name=last_name.strip(),
                status=status
            )
            db.session.add(volunteer)
            db.session.commit()
            
            flash(f'Volunteer "{first_name} {last_name}" added successfully!', 'success')
            return redirect(url_for('dashboard.volunteers_list'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding volunteer: {str(e)}', 'error')
            return redirect(url_for('dashboard.add_volunteer'))
    
    return render_template('add-volunteer.html')

@dashboard_bp.route('/volunteer/<int:volunteer_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_volunteer(volunteer_id):
    """Edit volunteer information"""
    volunteer = Volunteer.query.get_or_404(volunteer_id)
    
    if request.method == 'POST':
        try:
            volunteer.first_name = request.form.get('first_name')
            volunteer.last_name = request.form.get('last_name')
            volunteer.status = request.form.get('status')
            
            db.session.commit()
            flash('Volunteer information updated successfully!', 'success')
            return redirect(url_for('dashboard.volunteer_profile', volunteer_id=volunteer_id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating volunteer: {str(e)}', 'error')
    
    return render_template('edit-volunteer.html', volunteer=volunteer)

@dashboard_bp.route('/volunteers_old')
@login_required
def volunteers_list_old():
    """List all volunteers with filtering options"""
    department = request.args.get('department')
    status = request.args.get('status', 'active')
    
    query = Volunteer.query
    
    if department:
        query = query.filter_by(department=department)
    if status:
        query = query.filter_by(status=status)
    
    volunteers = query.order_by(Volunteer.name).all()
    
    # Add stats for each volunteer
    volunteers_with_stats = []
    for v in volunteers:
        volunteers_with_stats.append({
            'volunteer': v,
            'stats': calculate_volunteer_stats(v.id)
        })
    
    return render_template(
        'volunteers-list.html',
        volunteers=volunteers_with_stats,
        selected_department=department,
        selected_status=status
    )

@dashboard_bp.route('/api/stats')
@login_required
def get_stats():
    """API endpoint for dashboard statistics"""
    period = request.args.get('period', '30')  # days
    
    try:
        days = int(period)
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Get evaluations in period
        evaluations = Evaluation.query.filter(
            Evaluation.created_at >= start_date
        ).all()
        
        # Calculate statistics
        if evaluations:
            avg_overall = sum(e.overall_rating for e in evaluations) / len(evaluations)
            avg_reliability = sum(e.reliability_rating for e in evaluations) / len(evaluations)
            avg_communication = sum(e.communication_rating for e in evaluations) / len(evaluations)
            avg_teamwork = sum(e.teamwork_rating for e in evaluations) / len(evaluations)
            avg_initiative = sum(e.initiative_rating for e in evaluations) / len(evaluations)
            avg_quality = sum(e.quality_rating for e in evaluations) / len(evaluations)
        else:
            avg_overall = avg_reliability = avg_communication = 0
            avg_teamwork = avg_initiative = avg_quality = 0
        
        return jsonify({
            'period_days': days,
            'evaluation_count': len(evaluations),
            'averages': {
                'overall': round(avg_overall, 2),
                'reliability': round(avg_reliability, 2),
                'communication': round(avg_communication, 2),
                'teamwork': round(avg_teamwork, 2),
                'initiative': round(avg_initiative, 2),
                'quality': round(avg_quality, 2)
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@dashboard_bp.route('/admin')
@login_required
def admin_panel():
    """Admin panel for user management"""
    # Only admins can access
    if current_user.role != 'admin':
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('dashboard.index'))
    
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin-panel.html', users=users)

@dashboard_bp.route('/admin/add-user', methods=['POST'])
@login_required
def add_user():
    """Add new user"""
    if current_user.role != 'admin':
        return jsonify({'success': False, 'message': 'Access denied'}), 403
    
    try:
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')
        
        # Validate
        if not username or not password or not role:
            flash('All fields are required', 'error')
            return redirect(url_for('dashboard.admin_panel'))
        
        if len(password) < 6:
            flash('Password must be at least 6 characters', 'error')
            return redirect(url_for('dashboard.admin_panel'))
        
        # Check if user exists
        existing = User.query.filter_by(username=username).first()
        if existing:
            flash(f'User "{username}" already exists', 'error')
            return redirect(url_for('dashboard.admin_panel'))
        
        # Create user
        user = User(username=username, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash(f'User "{username}" created successfully!', 'success')
        return redirect(url_for('dashboard.admin_panel'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error creating user: {str(e)}', 'error')
        return redirect(url_for('dashboard.admin_panel'))

@dashboard_bp.route('/admin/reset-password', methods=['POST'])
@login_required
def reset_password():
    """Reset user password"""
    if current_user.role != 'admin':
        return jsonify({'success': False, 'message': 'Access denied'}), 403
    
    try:
        user_id = request.form.get('user_id')
        new_password = request.form.get('new_password')
        
        if not user_id or not new_password:
            flash('User ID and password are required', 'error')
            return redirect(url_for('dashboard.admin_panel'))
        
        if len(new_password) < 6:
            flash('Password must be at least 6 characters', 'error')
            return redirect(url_for('dashboard.admin_panel'))
        
        user = User.query.get(user_id)
        if not user:
            flash('User not found', 'error')
            return redirect(url_for('dashboard.admin_panel'))
        
        user.set_password(new_password)
        db.session.commit()
        
        flash(f'Password reset for "{user.username}" successfully!', 'success')
        return redirect(url_for('dashboard.admin_panel'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error resetting password: {str(e)}', 'error')
        return redirect(url_for('dashboard.admin_panel'))

@dashboard_bp.route('/admin/delete-user', methods=['POST'])
@login_required
def delete_user():
    """Delete user"""
    if current_user.role != 'admin':
        return jsonify({'success': False, 'message': 'Access denied'}), 403
    
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        
        if not user_id:
            return jsonify({'success': False, 'message': 'User ID required'}), 400
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({'success': False, 'message': 'User not found'}), 404
        
        # Prevent deleting admin account
        if user.username == 'admin':
            return jsonify({'success': False, 'message': 'Cannot delete default admin account'}), 400
        
        # Prevent deleting yourself
        if user.id == current_user.id:
            return jsonify({'success': False, 'message': 'Cannot delete your own account'}), 400
        
        username = user.username
        db.session.delete(user)
        db.session.commit()
        
        return jsonify({'success': True, 'message': f'User "{username}" deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@dashboard_bp.route('/evaluation/<int:evaluation_id>')
@login_required
def view_evaluation(evaluation_id):
    """View full evaluation details"""
    evaluation = Evaluation.query.get_or_404(evaluation_id)
    return render_template('view-evaluation.html', evaluation=evaluation)

@dashboard_bp.route('/evaluation/<int:evaluation_id>/delete', methods=['POST'])
@login_required
def delete_evaluation(evaluation_id):
    """Delete an evaluation (admin only)"""
    if current_user.role != 'admin':
        return jsonify({'success': False, 'message': 'Access denied. Admin privileges required.'}), 403
    
    try:
        evaluation = Evaluation.query.get_or_404(evaluation_id)
        volunteer_name = f"{evaluation.volunteer.first_name} {evaluation.volunteer.last_name}"
        
        db.session.delete(evaluation)
        db.session.commit()
        
        return jsonify({'success': True, 'message': f'Evaluation for {volunteer_name} deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@dashboard_bp.route('/volunteer/<int:volunteer_id>/delete', methods=['POST'])
@login_required
def delete_volunteer(volunteer_id):
    """Delete a volunteer (admin only)"""
    if current_user.role != 'admin':
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('dashboard.volunteers_list'))
    
    try:
        volunteer = Volunteer.query.get_or_404(volunteer_id)
        volunteer_name = f"{volunteer.first_name} {volunteer.last_name}"
        
        # Delete all associated evaluations first
        Evaluation.query.filter_by(volunteer_id=volunteer_id).delete()
        
        db.session.delete(volunteer)
        db.session.commit()
        
        flash(f'Volunteer {volunteer_name} and all associated evaluations deleted successfully', 'success')
        return redirect(url_for('dashboard.volunteers_list'))
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting volunteer: {str(e)}', 'error')
        return redirect(url_for('dashboard.volunteers_list'))

@dashboard_bp.route('/export/evaluations')
@login_required
def export_evaluations():
    """Export all evaluations to CSV"""
    # Get all evaluations
    evaluations = Evaluation.query.order_by(Evaluation.submitted_at.desc()).all()
    
    # Create CSV in memory
    output = StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow([
        'Volunteer First Name',
        'Volunteer Last Name',
        'Evaluator Name',
        'Event Name',
        'Role Performed',
        'Evaluation Date',
        'Submitted At',
        'Reliability',
        'Communication',
        'Teamwork',
        'Initiative',
        'Quality of Work',
        'Overall Average',
        'Strengths',
        'Areas for Improvement',
        'Additional Comments'
    ])
    
    # Write data
    for eval in evaluations:
        overall = (eval.reliability + eval.communication + eval.teamwork + 
                  eval.initiative + eval.quality_of_work) / 5.0
        
        writer.writerow([
            eval.volunteer.first_name,
            eval.volunteer.last_name,
            eval.evaluator_name,
            eval.event_name or '',
            eval.role_performed or '',
            eval.evaluation_date.strftime('%Y-%m-%d') if eval.evaluation_date else '',
            eval.submitted_at.strftime('%Y-%m-%d %H:%M:%S'),
            eval.reliability,
            eval.communication,
            eval.teamwork,
            eval.initiative,
            eval.quality_of_work,
            f'{overall:.2f}',
            eval.strengths or '',
            eval.areas_for_improvement or '',
            eval.additional_comments or ''
        ])
    
    # Create response
    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={
            'Content-Disposition': f'attachment; filename=evaluations_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        }
    )
