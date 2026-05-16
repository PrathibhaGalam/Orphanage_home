import os
from flask import Flask, send_from_directory
from flask_login import LoginManager
from database.models import db, User
from config import config

login_manager = LoginManager()

def create_app(config_name='development'):
    """Application factory"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    
    # Register user loader
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Create tables (handle connection errors gracefully)
    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            app.logger.warning(f'Database connection failed: {e}')
    
    # Register blueprints
    from app.auth.routes import auth_bp
    from app.admin.routes import admin_bp
    from app.donor.routes import donor_bp
    from app.api.routes import api_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(donor_bp, url_prefix='/donor')
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Home route
    @app.route('/')
    def index():
        """Serve the static front page from the Public folder."""
        public_dir = os.path.abspath(os.path.join(app.root_path, '..', 'Public'))
        return send_from_directory(public_dir, 'index.html')
    
    return app
