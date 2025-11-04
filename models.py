from datetime import datetime
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model, UserMixin):
    """User model for authentication"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='viewer')  # admin, viewer
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Flask-Login required properties
    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_active(self):
        return True
    
    @property
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self.id)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'


class Volunteer(db.Model):
    """Volunteer information"""
    __tablename__ = 'volunteers'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    date_first_volunteered = db.Column(db.Date)
    status = db.Column(db.String(20), default='Active')  # Active, Inactive
    preferred_roles = db.Column(db.Text)  # JSON array of role IDs
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    evaluations = db.relationship('Evaluation', backref='volunteer', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Volunteer {self.full_name}>'
    
    @property
    def full_name(self):
        """Get full name"""
        return f'{self.first_name} {self.last_name}'
    
    @property
    def evaluation_count(self):
        """Get total number of evaluations"""
        return self.evaluations.count()
    
    def get_preferred_roles(self):
        """Parse preferred_roles JSON string to list"""
        if not self.preferred_roles:
            return []
        try:
            import json
            return json.loads(self.preferred_roles)
        except:
            return []
    
    def set_preferred_roles(self, role_ids):
        """Set preferred_roles from list to JSON string"""
        import json
        self.preferred_roles = json.dumps(role_ids) if role_ids else None
    
    def get_average_scores(self):
        """Calculate average scores across all evaluations"""
        if not self.evaluations or self.evaluations.count() == 0:
            return None
        
        metrics = ['reliability', 'quality_of_work', 'initiative', 'teamwork', 'communication']
        averages = {}
        
        for metric in metrics:
            scores = [getattr(e, metric) for e in self.evaluations if getattr(e, metric)]
            averages[metric] = round(sum(scores) / len(scores), 1) if scores else 0
        
        averages['overall'] = round(sum(averages.values()) / len(metrics), 1)
        return averages


class Event(db.Model):
    """Events where volunteers serve"""
    __tablename__ = 'events'
    
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(200))
    event_code = db.Column(db.String(50))  # WLR, AFU, Prog, 10-Day
    location = db.Column(db.String(200))
    event_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    evaluations = db.relationship('Evaluation', backref='event', lazy=True)
    
    def __repr__(self):
        return f'<Event {self.event_code}: {self.location}>'


class Evaluation(db.Model):
    """Performance evaluations submitted by staff"""
    __tablename__ = 'evaluations'
    
    id = db.Column(db.Integer, primary_key=True)
    evaluation_id = db.Column(db.String(20), unique=True, nullable=False)  # e.g., EVAL-00001
    volunteer_id = db.Column(db.Integer, db.ForeignKey('volunteers.id'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    date_of_service = db.Column(db.Date, nullable=False)
    
    # Performance metrics (1-10 scale)
    reliability = db.Column(db.Integer)
    quality_of_work = db.Column(db.Integer)
    initiative = db.Column(db.Integer)
    teamwork = db.Column(db.Integer)
    communication = db.Column(db.Integer)
    
    # Qualitative feedback
    strengths = db.Column(db.Text)
    areas_for_improvement = db.Column(db.Text)
    additional_comments = db.Column(db.Text)
    
    # Event and service details
    event_name = db.Column(db.String(100))
    service_month = db.Column(db.String(2))  # Format: 01-12
    service_year = db.Column(db.String(4))   # Format: YYYY
    role_performed = db.Column(db.String(100))
    evaluation_date = db.Column(db.Date)
    
    # Metadata
    evaluator_name = db.Column(db.String(100))
    evaluator_email = db.Column(db.String(120))
    evaluator_role = db.Column(db.String(100))
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Evaluation {self.evaluation_id}>'
    
    def get_overall_score(self):
        """Calculate overall score from all metrics"""
        scores = [
            self.reliability,
            self.quality_of_work,
            self.initiative,
            self.teamwork,
            self.communication
        ]
        valid_scores = [s for s in scores if s is not None]
        return round(sum(valid_scores) / len(valid_scores), 1) if valid_scores else 0


class Role(db.Model):
    """Volunteer roles/positions with requirements"""
    __tablename__ = 'roles'
    
    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.String(20), unique=True, nullable=False)  # e.g., ROLE-001
    role_name = db.Column(db.String(100), nullable=False)  # GL, GLA, GG, etc.
    description = db.Column(db.Text)
    key_skills = db.Column(db.Text)
    interaction_level = db.Column(db.String(20))  # High, Medium, Low
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    evaluations = db.relationship('Evaluation', backref='role', lazy='dynamic')
    
    def __repr__(self):
        return f'<Role {self.role_name}>'


class EvaluationPeriod(db.Model):
    """Define evaluation periods for tracking"""
    __tablename__ = 'evaluation_periods'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<EvaluationPeriod {self.name}>'
