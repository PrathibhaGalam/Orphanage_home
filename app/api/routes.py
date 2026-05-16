from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from database.models import Orphanage, Orphan, Donation
from functools import wraps

api_bp = Blueprint('api', __name__)

def api_auth_required(f):
    """API authentication decorator"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated_function

# ==================== ORPHANAGES API ====================

@api_bp.route('/orphanages', methods=['GET'])
def get_orphanages():
    """Get all orphanages with optional filters"""
    city = request.args.get('city')
    state = request.args.get('state')
    
    query = Orphanage.query.filter_by(is_active=True)
    
    if city:
        query = query.filter_by(city=city)
    if state:
        query = query.filter_by(state=state)
    
    orphanages = query.all()
    
    return jsonify({
        'success': True,
        'data': [{
            'id': o.id,
            'name': o.name,
            'city': o.city,
            'state': o.state,
            'capacity': o.capacity,
            'occupancy': o.current_occupancy,
            'latitude': o.latitude,
            'longitude': o.longitude
        } for o in orphanages]
    })

@api_bp.route('/orphanages/<int:id>', methods=['GET'])
def get_orphanage(id):
    """Get orphanage details"""
    orphanage = Orphanage.query.get(id)
    
    if not orphanage:
        return jsonify({'error': 'Orphanage not found'}), 404
    
    return jsonify({
        'success': True,
        'data': {
            'id': orphanage.id,
            'name': orphanage.name,
            'address': orphanage.address,
            'city': orphanage.city,
            'state': orphanage.state,
            'postal_code': orphanage.postal_code,
            'phone': orphanage.phone,
            'email': orphanage.email,
            'capacity': orphanage.capacity,
            'occupancy': orphanage.current_occupancy,
            'latitude': orphanage.latitude,
            'longitude': orphanage.longitude
        }
    })

# ==================== ORPHANS API ====================

@api_bp.route('/orphanages/<int:orphanage_id>/orphans', methods=['GET'])
def get_orphans(orphanage_id):
    """Get orphans in a specific orphanage"""
    orphanage = Orphanage.query.get(orphanage_id)
    
    if not orphanage:
        return jsonify({'error': 'Orphanage not found'}), 404
    
    orphans = Orphan.query.filter_by(orphanage_id=orphanage_id).all()
    
    return jsonify({
        'success': True,
        'data': [{
            'id': o.id,
            'name': o.name,
            'age': (datetime.now().date() - o.date_of_birth).days // 365,
            'gender': o.gender,
            'education': o.education_level,
            'health_status': o.health_status
        } for o in orphans]
    })

# ==================== DONATIONS API ====================

@api_bp.route('/donations', methods=['POST'])
@api_auth_required
def create_donation():
    """Create a donation via API"""
    data = request.get_json()
    
    try:
        donation = Donation(
            user_id=current_user.id,
            orphanage_id=data['orphanage_id'],
            amount=data['amount'],
            donation_type=data.get('type', 'monetary'),
            description=data.get('description'),
            payment_method=data.get('payment_method'),
            status='completed'
        )
        
        db.session.add(donation)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Donation created successfully',
            'donation_id': donation.id
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@api_bp.route('/donations/<int:donation_id>', methods=['GET'])
@api_auth_required
def get_donation(donation_id):
    """Get donation details"""
    donation = Donation.query.get(donation_id)
    
    if not donation:
        return jsonify({'error': 'Donation not found'}), 404
    
    if donation.user_id != current_user.id and current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    return jsonify({
        'success': True,
        'data': {
            'id': donation.id,
            'amount': donation.amount,
            'type': donation.donation_type,
            'date': donation.donation_date.isoformat(),
            'status': donation.status
        }
    })

# ==================== STATISTICS API ====================

@api_bp.route('/statistics', methods=['GET'])
def get_statistics():
    """Get system statistics"""
    total_orphanages = Orphanage.query.count()
    total_orphans = Orphan.query.count()
    total_donations = Donation.query.count()
    total_amount = sum(d.amount for d in Donation.query.all()) or 0
    
    return jsonify({
        'success': True,
        'data': {
            'orphanages': total_orphanages,
            'orphans': total_orphans,
            'donations': total_donations,
            'total_amount': total_amount
        }
    })

from datetime import datetime
