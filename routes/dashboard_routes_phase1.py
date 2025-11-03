from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Volunteer, Evaluation, Role, Event, User
from sqlalchemy import func, desc
from datetime import datetime, timedelta

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')

@dashboard_bp.route('/')
@login_required
def dashboard():
    """Main leadership dashboard"""
    # Get summary statistics
    total_volunteers = Volunteer.query.filter_by(status='Active').count()
    total_evaluations = Evaluation.query.count()
    recent_evaluations = Evaluation.query.order_by(desc(Evaluation.submitted_at)).limit(10).all()
    
    # Get upcoming events count
    today = datetime.now().date()
    upcoming_events = Event.query.filter(Event.event_date >= today).count()
    
    # Get top performers (overall score >= 8)
    top_performers = []
    for volunteer in Volunteer.query.filter_by(status='Active').all():
        avg_scores = volunteer.get_average_scores()
        if avg_scores and avg_scores['overall'] >= 8.0:
            top_performers.append({
                'volunteer': volunteer,
                'score': avg_scores['overall']
            })
    top_performers = sorted(top_performers, key=lambda x: x['score'], reverse=True)[:10]
    
    # Get volunteers needing attention (overall score < 6)
    needs_attention = []
    for volunteer in Volunteer.query.filter_by(status='Active').all():
        avg_scores = volunteer.get_average_scores()
        if avg_scores and avg_scores['overall'] < 6.0:
            needs_attention.append({
                'volunteer': volunteer,
                'score': avg_scores['overall']
            })
    needs_attention = sorted(needs_attention, key=lambda x: x['score'])
    
    return render_template('dashboard.html',
                         total_volunteers=total_volunteers,
                         total_evaluations=total_evaluations,
                         upcoming_events=upcoming_events,
                         recent_evaluations=recent_evaluations,
                         top_performers=top_performers,
                         needs_attention=needs_attention)

@dashboard_bp.route('/volunteer/<int:volunteer_id>')
@login_required
def volunteer_profile(volunteer_id):
    """Individual volunteer profile page"""
    volunteer = Volunteer.query.get_or_404(volunteer_id)
    evaluations = Evaluation.query.filter_by(volunteer_id=volunteer_id)\
        .order_by(desc(Evaluation.date_of_service)).all()
    
    avg_scores = volunteer.get_average_scores()
    
    return render_template('volunteer-profile.html',
                         volunteer=volunteer,
                         evaluations=evaluations,
                         avg_scores=avg_scores)

@dashboard_bp.route('/evaluations')
@login_required
def all_evaluations():
    """View all evaluations with filtering"""
    page = request.args.get('page', 1, type=int)
    per_page = 50
    
    evaluations = Evaluation.query.order_by(desc(Evaluation.submitted_at))\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template('all-evaluations.html', evaluations=evaluations)

@dashboard_bp.route('/events')
@login_required
def manage_events():
    """View and manage events"""
    events = Event.query.order_by(desc(Event.event_date)).all()
    
    # Event type options
    event_types = [
        {'code': 'WLR', 'name': 'Week Long Retreat'},
        {'code': 'AFU', 'name': 'Advanced Follow Up'},
        {'code': 'Prog', 'name': 'Progressive'},
        {'code': '10-Day', 'name': '10-Day'}
    ]
    
    return render_template('manage-events.html', events=events, event_types=event_types)

@dashboard_bp.route('/events/add', methods=['POST'])
@login_required
def add_event():
    """Add a new event"""
    try:
        event_code = request.form['event_code']
        event_name_map = {
            'WLR': 'Week Long Retreat',
            'AFU': 'Advanced Follow Up',
            'Prog': 'Progressive',
            '10-Day': '10-Day'
        }
        
        event = Event(
            event_name=event_name_map.get(event_code, event_code),
            event_code=event_code,
            location=request.form['location'],
            event_date=datetime.strptime(request.form['event_date'], '%Y-%m-%d').date()
        )
        
        db.session.add(event)
        db.session.commit()
        
        flash('Event added successfully!', 'success')
        return redirect(url_for('dashboard.manage_events'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error adding event: {str(e)}', 'error')
        return redirect(url_for('dashboard.manage_events'))

@dashboard_bp.route('/events/delete/<int:event_id>', methods=['POST'])
@login_required
def delete_event(event_id):
    """Delete an event"""
    try:
        event = Event.query.get_or_404(event_id)
        
        # Check if event has evaluations
        eval_count = Evaluation.query.filter_by(event_id=event_id).count()
        if eval_count > 0:
            flash(f'Cannot delete event with {eval_count} existing evaluations', 'error')
            return redirect(url_for('dashboard.manage_events'))
        
        db.session.delete(event)
        db.session.commit()
        
        flash('Event deleted successfully', 'success')
        return redirect(url_for('dashboard.manage_events'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting event: {str(e)}', 'error')
        return redirect(url_for('dashboard.manage_events'))

@dashboard_bp.route('/users')
@login_required
def manage_users():
    """Manage user accounts (admin only)"""
    # Only admins can manage users
    if current_user.role != 'admin':
        flash('You do not have permission to manage users', 'error')
        return redirect(url_for('dashboard.dashboard'))
    
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('manage-users.html', users=users)

@dashboard_bp.route('/users/add', methods=['POST'])
@login_required
def add_user():
    """Add a new user (admin only)"""
    if current_user.role != 'admin':
        flash('You do not have permission to add users', 'error')
        return redirect(url_for('dashboard.dashboard'))
    
    try:
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        
        # Check if username already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return redirect(url_for('dashboard.manage_users'))
        
        user = User(username=username, role=role)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash(f'User {username} created successfully!', 'success')
        return redirect(url_for('dashboard.manage_users'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error adding user: {str(e)}', 'error')
        return redirect(url_for('dashboard.manage_users'))

@dashboard_bp.route('/users/delete/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    """Delete a user (admin only)"""
    if current_user.role != 'admin':
        flash('You do not have permission to delete users', 'error')
        return redirect(url_for('dashboard.dashboard'))
    
    try:
        user = User.query.get_or_404(user_id)
        
        # Prevent deleting yourself
        if user.id == current_user.id:
            flash('Cannot delete your own account', 'error')
            return redirect(url_for('dashboard.manage_users'))
        
        # Prevent deleting the last admin
        admin_count = User.query.filter_by(role='admin').count()
        if user.role == 'admin' and admin_count <= 1:
            flash('Cannot delete the last admin account', 'error')
            return redirect(url_for('dashboard.manage_users'))
        
        db.session.delete(user)
        db.session.commit()
        
        flash('User deleted successfully', 'success')
        return redirect(url_for('dashboard.manage_users'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting user: {str(e)}', 'error')
        return redirect(url_for('dashboard.manage_users'))

@dashboard_bp.route('/users/change-password/<int:user_id>', methods=['POST'])
@login_required
def change_user_password(user_id):
    """Change a user's password (admin only)"""
    if current_user.role != 'admin':
        flash('You do not have permission to change passwords', 'error')
        return redirect(url_for('dashboard.dashboard'))
    
    try:
        user = User.query.get_or_404(user_id)
        new_password = request.form['new_password']
        
        user.set_password(new_password)
        db.session.commit()
        
        flash(f'Password updated for {user.username}', 'success')
        return redirect(url_for('dashboard.manage_users'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error changing password: {str(e)}', 'error')
        return redirect(url_for('dashboard.manage_users'))
