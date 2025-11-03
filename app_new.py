from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import LoginManager, login_user, logout_user, current_user
from models import db, User
from config import Config
from whitenoise import WhiteNoise
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Ensure database directory exists BEFORE initializing db
    db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
    db_dir = os.path.dirname(db_path)
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)
    
    # Initialize database
    db.init_app(app)
    
    # Initialize login manager
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Create database tables
    with app.app_context():
        db.create_all()
        
        # Create default admin user if none exists
        if User.query.count() == 0:
            admin = User(username='admin', role='admin')
            admin.set_password('changeme123')  # CHANGE THIS!
            db.session.add(admin)
            db.session.commit()
            print("Created default admin user - username: admin, password: changeme123")
    
    # Register blueprints
    from routes.evaluation_routes import evaluation_bp
    from routes.dashboard_routes import dashboard_bp
    from routes.api_routes import api_bp
    
    app.register_blueprint(evaluation_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(api_bp)
    
    # Home route
    @app.route('/')
    def index():
        return redirect(url_for('dashboard.index'))
    
    # Login route
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard.index'))
        
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            
            user = User.query.filter_by(username=username).first()
            
            if user and user.check_password(password):
                login_user(user)
                flash('Login successful!', 'success')
                return redirect(url_for('dashboard.index'))
            else:
                flash('Invalid username or password', 'error')
        
        return render_template('login.html')
    
    # Logout route
    @app.route('/logout')
    def logout():
        logout_user()
        flash('You have been logged out', 'success')
        return redirect(url_for('login'))
    
    return app

# Create app instance for gunicorn
app = create_app()

# Wrap with WhiteNoise for static file serving
app.wsgi_app = WhiteNoise(
    app.wsgi_app,
    root=os.path.join(os.path.dirname(__file__), 'static'),
    prefix='static/'
)

if __name__ == '__main__':
    # app is already created above
    print("\n" + "="*60)
    print("🚀 Volunteer Evaluation System Starting...")
    print("="*60)
    print(f"✅ Database: Initialized")
    print(f"✅ Admin user: admin / changeme123")
    print(f"🌐 Open your browser to: http://localhost:5001")
    print("="*60 + "\n")
    app.run(debug=True, port=5001, host='127.0.0.1')
