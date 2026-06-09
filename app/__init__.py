import os
from flask import Flask, send_from_directory
from flask_login import LoginManager
from sqlalchemy import inspect, text
from database.models import db, User
from config import config

login_manager = LoginManager()

def ensure_schema():
    inspector = inspect(db.engine)
    with db.engine.begin() as conn:
        if 'users' in inspector.get_table_names():
            users_cols = [col['name'] for col in inspector.get_columns('users')]
            if 'phone' not in users_cols:
                conn.execute(text('ALTER TABLE users ADD COLUMN phone VARCHAR(15)'))
        if 'donations' in inspector.get_table_names():
            donations_cols = [col['name'] for col in inspector.get_columns('donations')]
            if 'donor_email' not in donations_cols:
                conn.execute(text('ALTER TABLE donations ADD COLUMN donor_email VARCHAR(120)'))
            if 'donor_phone' not in donations_cols:
                conn.execute(text('ALTER TABLE donations ADD COLUMN donor_phone VARCHAR(15)'))


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
    
    # Create tables and ensure new columns exist (handle connection errors gracefully)
    with app.app_context():
        try:
            db.create_all()
            ensure_schema()
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
    
    # Static files routes for Public folder
    @app.route('/CSS/<path:filename>')
    def serve_css(filename):
        public_dir = os.path.abspath(os.path.join(app.root_path, '..', 'Public'))
        return send_from_directory(os.path.join(public_dir, 'CSS'), filename)
    
    @app.route('/JS/<path:filename>')
    def serve_js(filename):
        public_dir = os.path.abspath(os.path.join(app.root_path, '..', 'Public'))
        return send_from_directory(os.path.join(public_dir, 'JS'), filename)
    
    @app.route('/images/<path:filename>')
    def serve_images(filename):
        public_dir = os.path.abspath(os.path.join(app.root_path, '..', 'Public'))
        return send_from_directory(os.path.join(public_dir, 'images'), filename)
    
    # Serve other public HTML files
    @app.route('/<path:filename>.html')
    def serve_public_html(filename):
        public_dir = os.path.abspath(os.path.join(app.root_path, '..', 'Public'))
        return send_from_directory(public_dir, f'{filename}.html')
    
    return app
