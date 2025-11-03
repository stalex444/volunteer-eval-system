from models import db, Volunteer, Evaluation
from sqlalchemy import func
from datetime import datetime, timedelta
import numpy as np

def calculate_volunteer_stats(volunteer_id):
    """Calculate comprehensive statistics for a volunteer"""
    volunteer = Volunteer.query.get(volunteer_id)
    if not volunteer:
        return None
    
    evaluations = volunteer.evaluations.all()
    
    if not evaluations:
        return {
            'evaluation_count': 0,
            'average_overall': None,
            'average_by_category': {},
            'trend': None,
            'recent_performance': None
        }
    
    # Calculate averages from the 5 individual ratings
    avg_reliability = sum(e.reliability for e in evaluations) / len(evaluations)
    avg_communication = sum(e.communication for e in evaluations) / len(evaluations)
    avg_teamwork = sum(e.teamwork for e in evaluations) / len(evaluations)
    avg_initiative = sum(e.initiative for e in evaluations) / len(evaluations)
    avg_quality = sum(e.quality_of_work for e in evaluations) / len(evaluations)
    
    # Calculate overall average from the 5 categories
    avg_overall = (avg_reliability + avg_communication + avg_teamwork + avg_initiative + avg_quality) / 5
    
    # Calculate trend (comparing recent vs older evaluations)
    trend = None
    if len(evaluations) >= 4:
        sorted_evals = sorted(evaluations, key=lambda e: e.evaluation_date if e.evaluation_date else e.submitted_at)
        half = len(sorted_evals) // 2
        
        # Calculate average for older half
        older_scores = []
        for e in sorted_evals[:half]:
            score = (e.reliability + e.quality_of_work + e.initiative + e.teamwork + e.communication) / 5
            older_scores.append(score)
        older_avg = sum(older_scores) / len(older_scores)
        
        # Calculate average for recent half
        recent_scores = []
        for e in sorted_evals[half:]:
            score = (e.reliability + e.quality_of_work + e.initiative + e.teamwork + e.communication) / 5
            recent_scores.append(score)
        recent_avg = sum(recent_scores) / len(recent_scores)
        
        trend = 'improving' if recent_avg > older_avg else 'declining' if recent_avg < older_avg else 'stable'
    
    # Recent performance (last 30 days)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    recent_evals = [e for e in evaluations if e.submitted_at >= thirty_days_ago]
    recent_performance = None
    if recent_evals:
        recent_scores = [(e.reliability + e.quality_of_work + e.initiative + e.teamwork + e.communication) / 5 for e in recent_evals]
        recent_performance = sum(recent_scores) / len(recent_scores)
    
    return {
        'evaluation_count': len(evaluations),
        'average_overall': round(avg_overall, 2),
        'average_by_category': {
            'reliability': round(avg_reliability, 2),
            'communication': round(avg_communication, 2),
            'teamwork': round(avg_teamwork, 2),
            'initiative': round(avg_initiative, 2),
            'quality': round(avg_quality, 2)
        },
        'trend': trend,
        'recent_performance': round(recent_performance, 2) if recent_performance else None,
        'recent_evaluation_count': len(recent_evals)
    }

def get_department_summary():
    """Get summary statistics by department"""
    # Since we don't have department field, return empty list
    return []

def get_trend_data(volunteer_id, months=6):
    """Get monthly trend data for a volunteer"""
    volunteer = Volunteer.query.get(volunteer_id)
    if not volunteer:
        return []
    
    start_date = datetime.utcnow() - timedelta(days=months * 30)
    evaluations = volunteer.evaluations.filter(
        Evaluation.submitted_at >= start_date
    ).order_by(Evaluation.submitted_at).all()
    
    # Group by month
    monthly_data = {}
    for eval in evaluations:
        date_to_use = eval.evaluation_date if eval.evaluation_date else eval.submitted_at
        month_key = date_to_use.strftime('%Y-%m')
        if month_key not in monthly_data:
            monthly_data[month_key] = []
        # Calculate overall rating from 5 categories
        overall = (eval.reliability + eval.quality_of_work + eval.initiative + eval.teamwork + eval.communication) / 5
        monthly_data[month_key].append(overall)
    
    # Calculate monthly averages
    trend_data = []
    for month, ratings in sorted(monthly_data.items()):
        trend_data.append({
            'month': month,
            'average_rating': round(sum(ratings) / len(ratings), 2),
            'evaluation_count': len(ratings)
        })
    
    return trend_data

def identify_top_performers(limit=10, min_evaluations=3):
    """Identify top performing volunteers"""
    # Calculate averages manually since we don't have overall_rating field
    top_performers = []
    volunteers = Volunteer.query.all()
    
    for vol in volunteers:
        evals = vol.evaluations.all()
        if len(evals) >= min_evaluations:
            total = 0
            for e in evals:
                total += (e.reliability + e.quality_of_work + e.initiative + e.teamwork + e.communication) / 5
            avg = total / len(evals)
            top_performers.append({
                'volunteer': vol,
                'average_rating': round(avg, 2),
                'evaluation_count': len(evals)
            })
    
    # Sort by average rating descending
    top_performers.sort(key=lambda x: x['average_rating'], reverse=True)
    return top_performers[:limit]

def identify_needs_attention(threshold=6.0, min_evaluations=2):
    """Identify volunteers who may need additional support"""
    needs_attention = []
    volunteers = Volunteer.query.all()
    
    for vol in volunteers:
        evals = vol.evaluations.all()
        if len(evals) >= min_evaluations:
            total = 0
            for e in evals:
                total += (e.reliability + e.quality_of_work + e.initiative + e.teamwork + e.communication) / 5
            avg = total / len(evals)
            if avg < threshold:
                needs_attention.append({
                    'volunteer': vol,
                    'average_rating': round(avg, 2),
                    'evaluation_count': len(evals)
                })
    
    # Sort by average rating ascending (worst first)
    needs_attention.sort(key=lambda x: x['average_rating'])
    return needs_attention

def calculate_category_correlations(volunteer_id):
    """Calculate correlations between rating categories"""
    volunteer = Volunteer.query.get(volunteer_id)
    if not volunteer:
        return None
    
    evaluations = volunteer.evaluations.all()
    
    if len(evaluations) < 3:
        return None
    
    # Extract ratings into arrays
    reliability = [e.reliability for e in evaluations]
    communication = [e.communication for e in evaluations]
    teamwork = [e.teamwork for e in evaluations]
    initiative = [e.initiative for e in evaluations]
    quality = [e.quality_of_work for e in evaluations]
    
    # Calculate correlation matrix
    data = np.array([reliability, communication, teamwork, initiative, quality])
    correlation_matrix = np.corrcoef(data)
    
    categories = ['reliability', 'communication', 'teamwork', 'initiative', 'quality']
    
    return {
        'categories': categories,
        'correlation_matrix': correlation_matrix.tolist()
    }
