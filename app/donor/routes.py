from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from database.models import db, Orphanage, Donation, Orphan
from datetime import datetime

donor_bp = Blueprint('donor', __name__)

@donor_bp.route('/dashboard')
@login_required
def dashboard():
    """Donor dashboard"""
    donations = Donation.query.filter_by(user_id=current_user.id).all()
    orphanages = Orphanage.query.filter_by(is_active=True).all()
    
    total_donated = sum(d.amount for d in donations) if donations else 0
    total_donations = len(donations)
    
    stats = {
        'total_donated': total_donated,
        'total_donations': total_donations,
        'orphanages_count': len(orphanages)
    }
    
    return render_template('donor/dashboard.html', stats=stats, donations=donations)

@donor_bp.route('/orphanages')
@login_required
def view_orphanages():
    """View all orphanages"""
    page = request.args.get('page', 1, type=int)
    orphanages = Orphanage.query.filter_by(is_active=True).paginate(page=page, per_page=9)
    return render_template('donor/orphanages.html', orphanages=orphanages)

@donor_bp.route('/orphanages/<int:id>')
@login_required
def orphanage_detail(id):
    """View orphanage details"""
    orphanage = Orphanage.query.get_or_404(id)
    orphans = Orphan.query.filter_by(orphanage_id=id).all()
    donations = Donation.query.filter_by(orphanage_id=id).all()
    
    total_donations = sum(d.amount for d in donations) if donations else 0
    
    context = {
        'orphanage': orphanage,
        'orphans': orphans,
        'total_donations': total_donations,
        'donation_count': len(donations)
    }
    
    return render_template('donor/orphanage_detail.html', **context)

@donor_bp.route('/donate/<int:orphanage_id>', methods=['GET', 'POST'])
@login_required
def donate(orphanage_id):
    """Make a donation"""
    orphanage = Orphanage.query.get_or_404(orphanage_id)
    
    if request.method == 'POST':
        amount = request.form.get('amount', type=float)
        donation_type = request.form.get('donation_type', 'monetary')
        description = request.form.get('description')
        payment_method = request.form.get('payment_method')
        
        if not amount or amount <= 0:
            flash('Please enter a valid amount!', 'danger')
            return redirect(url_for('donor.donate', orphanage_id=orphanage_id))
        
        donation = Donation(
            user_id=current_user.id,
            orphanage_id=orphanage_id,
            amount=amount,
            donation_type=donation_type,
            description=description,
            payment_method=payment_method,
            status='completed'
        )
        
        try:
            db.session.add(donation)
            db.session.commit()
            flash('Thank you for your donation!', 'success')
            return redirect(url_for('donor.dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error processing donation: {str(e)}', 'danger')
    
    return render_template('donor/donate.html', orphanage=orphanage)

@donor_bp.route('/my-donations')
@login_required
def my_donations():
    """View my donations"""
    donations = Donation.query.filter_by(user_id=current_user.id).all()
    return render_template('donor/my_donations.html', donations=donations)
