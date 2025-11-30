from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, logout_user, login_required
from models import db, User, Volunteer, Evaluation, Role, Event
from config import Config
from routes.evaluation_routes import evaluation_bp
from routes.dashboard_routes import dashboard_bp
from routes.api_routes import api_bp
import os
import sqlite3
import glob

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Register blueprints
app.register_blueprint(evaluation_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(api_bp)

# Create default admin user if none exists
def create_default_admin():
    """Create default admin user if no users exist"""
    with app.app_context():
        if User.query.count() == 0:
            admin = User(username='admin', role='admin')
            admin.set_password('changeme123')
            db.session.add(admin)
            db.session.commit()
            print('✓ Default admin user created (username: admin, password: changeme123)')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page for leadership dashboard access"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard.index'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    """Logout current user"""
    logout_user()
    flash('You have been logged out successfully', 'success')
    return redirect(url_for('evaluation.index'))

@app.cli.command()
def init_db():
    """Initialize the database"""
    # Create database directory if it doesn't exist
    db_dir = os.path.dirname(app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', ''))
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir)
    
    db.create_all()
    print('Database initialized successfully!')

@app.cli.command()
def create_admin():
    """Create an admin user"""
    username = input('Enter username: ')
    password = input('Enter password: ')
    
    user = User(username=username, role='admin')
    user.set_password(password)
    
    db.session.add(user)
    db.session.commit()
    
    print(f'Admin user {username} created successfully!')

@app.cli.command()
def create_user():
    """Create a user (admin or viewer)"""
    username = input('Enter username: ')
    password = input('Enter password: ')
    role = input('Enter role (admin/viewer) [admin]: ').strip() or 'admin'
    
    if role not in ['admin', 'viewer']:
        print('Error: Role must be either "admin" or "viewer"')
        return
    
    user = User(username=username, role=role)
    user.set_password(password)
    
    db.session.add(user)
    db.session.commit()
    
    print(f'{role.capitalize()} user {username} created successfully!')

@app.cli.command()
def list_users():
    """List all users"""
    users = User.query.order_by(User.created_at).all()
    
    if not users:
        print('No users found. Create one with: flask create-admin')
        return
    
    print('\nSystem Users:')
    print('-' * 70)
    print(f'{"ID":<5} {"Username":<20} {"Role":<10} {"Created"}')
    print('-' * 70)
    
    for user in users:
        created = user.created_at.strftime('%Y-%m-%d') if user.created_at else 'N/A'
        print(f'{user.id:<5} {user.username:<20} {user.role:<10} {created}')
    
    print('-' * 70)
    print(f'Total: {len(users)} users')

@app.cli.command()
def seed_data():
    """Seed database with sample data"""
    import json
    from datetime import date
    
    # Create sample volunteers
    volunteers = [
        Volunteer(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            phone='555-0101',
            date_first_volunteered=date(2024, 1, 15),
            status='Active',
            preferred_roles=json.dumps(['ROLE-001', 'ROLE-005'])  # GL, RR
        ),
        Volunteer(
            first_name='Jane',
            last_name='Smith',
            email='jane@example.com',
            phone='555-0102',
            date_first_volunteered=date(2024, 2, 20),
            status='Active',
            preferred_roles=json.dumps(['ROLE-006', 'ROLE-008'])  # HST, FTVL
        ),
        Volunteer(
            first_name='Bob',
            last_name='Johnson',
            email='bob@example.com',
            phone='555-0103',
            date_first_volunteered=date(2024, 3, 10),
            status='Active',
            preferred_roles=json.dumps(['ROLE-004', 'ROLE-010'])  # Doors, Door Lead
        ),
    ]
    
    for v in volunteers:
        db.session.add(v)
    
    db.session.commit()
    print('Sample data created successfully!')

@app.cli.command()
def run_migrations():
    """Run all SQL migrations in the migrations directory"""
    migrations_dir = 'migrations'
    
    if not os.path.exists(migrations_dir):
        print(f'Error: {migrations_dir} directory not found')
        return
    
    # Get database path
    db_uri = app.config['SQLALCHEMY_DATABASE_URI']
    if not db_uri.startswith('sqlite:///'):
        print('Error: This command currently only supports SQLite databases')
        print('For PostgreSQL, run migrations manually using psql')
        return
    
    db_path = db_uri.replace('sqlite:///', '')
    
    # Ensure database directory exists
    db_dir = os.path.dirname(db_path)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir)
    
    # Get all SQL migration files
    migration_files = sorted(glob.glob(os.path.join(migrations_dir, '*.sql')))
    
    if not migration_files:
        print('No migration files found')
        return
    
    print(f'Found {len(migration_files)} migration file(s)')
    
    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Run each migration
    for migration_file in migration_files:
        print(f'\nRunning migration: {os.path.basename(migration_file)}')
        
        try:
            with open(migration_file, 'r') as f:
                sql = f.read()
            
            # Execute the migration
            cursor.executescript(sql)
            conn.commit()
            print(f'✓ Successfully applied {os.path.basename(migration_file)}')
            
        except Exception as e:
            print(f'✗ Error applying {os.path.basename(migration_file)}: {str(e)}')
            conn.rollback()
    
    conn.close()
    print('\nMigrations complete!')

@app.cli.command()
def list_roles():
    """List all available volunteer roles"""
    roles = Role.query.order_by(Role.role_id).all()
    
    if not roles:
        print('No roles found. Run migrations first: flask run-migrations')
        return
    
    print('\nAvailable Volunteer Roles:')
    print('-' * 80)
    print(f'{"ID":<12} {"Name":<20} {"Interaction":<15} {"Description"}')
    print('-' * 80)
    
    for role in roles:
        desc = role.description[:40] + '...' if role.description and len(role.description) > 40 else role.description or ''
        print(f'{role.role_id:<12} {role.role_name:<20} {role.interaction_level or "N/A":<15} {desc}')
    
    print('-' * 80)
    print(f'Total: {len(roles)} roles')

@app.cli.command()
def list_events():
    """List all events"""
    events = Event.query.order_by(Event.event_date.desc()).all()
    
    if not events:
        print('No events found. Run migrations first: flask run-migrations')
        return
    
    print('\nAvailable Events:')
    print('-' * 100)
    print(f'{"ID":<12} {"Name":<30} {"Date":<12} {"Type":<20} {"Location"}')
    print('-' * 100)
    
    for event in events:
        event_date = event.event_date.strftime('%Y-%m-%d') if event.event_date else 'N/A'
        print(f'{event.event_id:<12} {event.event_name[:28]:<30} {event_date:<12} {event.event_type or "N/A":<20} {event.location or "N/A"}')
    
    print('-' * 100)
    print(f'Total: {len(events)} events')

@app.cli.command()
def generate_evaluation_id():
    """Generate next evaluation ID"""
    last_eval = Evaluation.query.order_by(Evaluation.id.desc()).first()
    
    if last_eval:
        # Extract number from last evaluation_id
        last_num = int(last_eval.evaluation_id.split('-')[1])
        next_num = last_num + 1
    else:
        next_num = 1
    
    next_id = f'EVAL-{next_num:05d}'
    print(f'Next evaluation ID: {next_id}')
    return next_id

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure tables exist
        create_default_admin()  # Create admin if needed
    app.run(debug=True)
