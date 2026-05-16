from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from functools import wraps
from database.models import db, Orphan, Orphanage, Staff, User, Donation, Report
from datetime import datetime

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.role not in ['admin', 'staff']:
            flash('Access denied. Admin privileges required.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    """Admin dashboard"""
    orphanages = Orphanage.query.all()
    total_orphans = Orphan.query.count()
    total_donations = db.session.query(db.func.sum(Donation.amount)).scalar() or 0
    total_staff = Staff.query.count()
    
    stats = {
        'orphanages': len(orphanages),
        'orphans': total_orphans,
        'donations': total_donations,
        'staff': total_staff
    }
    
    return render_template('admin/dashboard.html', stats=stats, orphanages=orphanages)

# ==================== ORPHANAGE MANAGEMENT ====================

@admin_bp.route('/orphanages')
@login_required
@admin_required
def list_orphanages():
    """List all orphanages"""
    orphanages = Orphanage.query.all()
    return render_template('admin/orphanages/list.html', orphanages=orphanages)

@admin_bp.route('/orphanages/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_orphanage():
    """Create new orphanage"""
    if request.method == 'POST':
        orphanage = Orphanage(
            name=request.form.get('name'),
            address=request.form.get('address'),
            city=request.form.get('city'),
            state=request.form.get('state'),
            postal_code=request.form.get('postal_code'),
            country=request.form.get('country', 'India'),
            phone=request.form.get('phone'),
            email=request.form.get('email'),
            description=request.form.get('description'),
            capacity=request.form.get('capacity', type=int),
            founded_year=request.form.get('founded_year', type=int)
        )
        
        try:
            db.session.add(orphanage)
            db.session.commit()
            flash('Orphanage created successfully!', 'success')
            return redirect(url_for('admin.list_orphanages'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating orphanage: {str(e)}', 'danger')
    
    return render_template('admin/orphanages/create.html')

@admin_bp.route('/orphanages/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_orphanage(id):
    """Edit orphanage"""
    orphanage = Orphanage.query.get_or_404(id)
    
    if request.method == 'POST':
        orphanage.name = request.form.get('name')
        orphanage.address = request.form.get('address')
        orphanage.city = request.form.get('city')
        orphanage.state = request.form.get('state')
        orphanage.postal_code = request.form.get('postal_code')
        orphanage.phone = request.form.get('phone')
        orphanage.email = request.form.get('email')
        orphanage.description = request.form.get('description')
        orphanage.capacity = request.form.get('capacity', type=int)
        
        try:
            db.session.commit()
            flash('Orphanage updated successfully!', 'success')
            return redirect(url_for('admin.list_orphanages'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating orphanage: {str(e)}', 'danger')
    
    return render_template('admin/orphanages/edit.html', orphanage=orphanage)

@admin_bp.route('/orphanages/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_orphanage(id):
    """Delete orphanage"""
    orphanage = Orphanage.query.get_or_404(id)
    
    try:
        db.session.delete(orphanage)
        db.session.commit()
        flash('Orphanage deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting orphanage: {str(e)}', 'danger')
    
    return redirect(url_for('admin.list_orphanages'))

# ==================== ORPHAN MANAGEMENT ====================

@admin_bp.route('/orphans')
@login_required
@admin_required
def list_orphans():
    """List all orphans"""
    orphans = Orphan.query.all()
    return render_template('admin/orphans/list.html', orphans=orphans)

@admin_bp.route('/orphans/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_orphan():
    """Create new orphan record"""
    orphanages = Orphanage.query.all()
    
    if request.method == 'POST':
        orphan = Orphan(
            name=request.form.get('name'),
            date_of_birth=datetime.strptime(request.form.get('date_of_birth'), '%Y-%m-%d').date(),
            gender=request.form.get('gender'),
            health_status=request.form.get('health_status'),
            education_level=request.form.get('education_level'),
            orphanage_id=request.form.get('orphanage_id', type=int)
        )
        
        try:
            db.session.add(orphan)
            db.session.commit()
            flash('Orphan record created successfully!', 'success')
            return redirect(url_for('admin.list_orphans'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating record: {str(e)}', 'danger')
    
    return render_template('admin/orphans/create.html', orphanages=orphanages)

@admin_bp.route('/orphans/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_orphan(id):
    """Edit orphan record"""
    orphan = Orphan.query.get_or_404(id)
    orphanages = Orphanage.query.all()
    
    if request.method == 'POST':
        orphan.name = request.form.get('name')
        orphan.gender = request.form.get('gender')
        orphan.health_status = request.form.get('health_status')
        orphan.education_level = request.form.get('education_level')
        orphan.orphanage_id = request.form.get('orphanage_id', type=int)
        
        try:
            db.session.commit()
            flash('Orphan record updated successfully!', 'success')
            return redirect(url_for('admin.list_orphans'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating record: {str(e)}', 'danger')
    
    return render_template('admin/orphans/edit.html', orphan=orphan, orphanages=orphanages)

@admin_bp.route('/orphans/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_orphan(id):
    """Delete orphan record"""
    orphan = Orphan.query.get_or_404(id)
    
    try:
        db.session.delete(orphan)
        db.session.commit()
        flash('Orphan record deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting record: {str(e)}', 'danger')
    
    return redirect(url_for('admin.list_orphans'))

# ==================== DONATIONS MANAGEMENT ====================

@admin_bp.route('/donations')
@login_required
@admin_required
def list_donations():
    """List all donations"""
    donations = Donation.query.all()
    return render_template('admin/donations/list.html', donations=donations)
