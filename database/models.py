from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """User model for login/registration"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(15))
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='donor')  # admin, staff, donor
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    staff_info = db.relationship('Staff', backref='user', uselist=False, cascade='all, delete-orphan')
    donations = db.relationship('Donation', backref='donor', lazy=True)
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Orphan(db.Model):
    """Orphan information model"""
    __tablename__ = 'orphans'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    admission_date = db.Column(db.Date, default=datetime.utcnow)
    health_status = db.Column(db.String(50))
    education_level = db.Column(db.String(50))
    photo = db.Column(db.String(255))
    orphanage_id = db.Column(db.Integer, db.ForeignKey('orphanages.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    orphanage = db.relationship('Orphanage', backref='orphans')
    
    def __repr__(self):
        return f'<Orphan {self.name}>'

class Staff(db.Model):
    """Staff information model"""
    __tablename__ = 'staff'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    designation = db.Column(db.String(50), nullable=False)
    orphanage_id = db.Column(db.Integer, db.ForeignKey('orphanages.id'), nullable=False)
    phone = db.Column(db.String(15))
    joining_date = db.Column(db.Date, default=datetime.utcnow)
    
    # Relationship
    orphanage = db.relationship('Orphanage', backref='staff')
    
    def __repr__(self):
        return f'<Staff {self.user_id}>'

class Orphanage(db.Model):
    """Orphanage location and information model"""
    __tablename__ = 'orphanages'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    postal_code = db.Column(db.String(10))
    country = db.Column(db.String(50), default='India')
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    phone = db.Column(db.String(15))
    email = db.Column(db.String(120))
    description = db.Column(db.Text)
    capacity = db.Column(db.Integer)
    current_occupancy = db.Column(db.Integer, default=0)
    founded_year = db.Column(db.Integer)
    photo = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Orphanage {self.name}>'

class Donation(db.Model):
    """Donation tracking model"""
    __tablename__ = 'donations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    orphanage_id = db.Column(db.Integer, db.ForeignKey('orphanages.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    donation_type = db.Column(db.String(50))  # monetary, material, service
    description = db.Column(db.Text)
    donation_date = db.Column(db.DateTime, default=datetime.utcnow)
    payment_method = db.Column(db.String(50))  # card, bank, cash
    transaction_id = db.Column(db.String(100), unique=True)
    status = db.Column(db.String(20), default='completed')  # pending, completed, failed
    receipt_issued = db.Column(db.Boolean, default=False)
    donor_email = db.Column(db.String(120))
    donor_phone = db.Column(db.String(15))
    notes = db.Column(db.Text)
    
    # Relationships
    orphanage = db.relationship('Orphanage', backref='donations')
    
    def __repr__(self):
        return f'<Donation {self.id}>'

class Report(db.Model):
    """Orphanage reports/analytics model"""
    __tablename__ = 'reports'
    
    id = db.Column(db.Integer, primary_key=True)
    orphanage_id = db.Column(db.Integer, db.ForeignKey('orphanages.id'), nullable=False)
    report_type = db.Column(db.String(50))  # monthly, quarterly, annual
    period = db.Column(db.String(50))
    total_orphans = db.Column(db.Integer)
    total_donations_received = db.Column(db.Float)
    total_expenses = db.Column(db.Float)
    content = db.Column(db.Text)
    generated_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    orphanage = db.relationship('Orphanage', backref='reports')
    
    def __repr__(self):
        return f'<Report {self.id}>'
