"""
SafeGuard Women's Safety App - Flask API Backend
This file provides REST APIs for the frontend
"""

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN

# Initialize Flask
app = Flask(__name__)
CORS(app)  # Allow frontend to call APIs

app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///safety_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ==================== DATABASE MODELS ====================

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    medical_profile = db.relationship('MedicalProfile', backref='user', uselist=False)
    contacts = db.relationship('EmergencyContact', backref='user', lazy=True)
    sos_alerts = db.relationship('SOSAlert', backref='user', lazy=True)
    incident_reports = db.relationship('IncidentReport', backref='user', lazy=True)

class MedicalProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    full_name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    blood_group = db.Column(db.String(5))
    height = db.Column(db.Float)
    weight = db.Column(db.Float)
    allergies = db.Column(db.Text)
    medications = db.Column(db.Text)
    conditions = db.Column(db.Text)
    emergency_notes = db.Column(db.Text)
    insurance = db.Column(db.String(200))

class EmergencyContact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120))
    relation = db.Column(db.String(50))
    priority = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class SOSAlert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    address = db.Column(db.String(200))
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    resolved_at = db.Column(db.DateTime)

class IncidentReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    incident_type = db.Column(db.String(50))
    description = db.Column(db.Text)
    severity = db.Column(db.Integer)
    time_of_incident = db.Column(db.DateTime, default=datetime.utcnow)
    reported_at = db.Column(db.DateTime, default=datetime.utcnow)

# ==================== HOMEPAGE ====================

@app.route('/')
def home():
    """API Homepage"""
    return jsonify({
        'app': 'SafeGuard Women Safety API',
        'version': '1.0',
        'status': 'running',
        'message': 'Backend is ready!',
        'endpoints': {
            'contacts': '/api/contacts',
            'medical': '/api/medical',
            'sos': '/api/sos',
            'analytics': '/api/analytics/overview',
            'hotspots': '/api/analytics/hotspots',
            'risk': '/api/analytics/risk-score'
        }
    })

# ==================== EMERGENCY CONTACTS API ====================

@app.route('/api/contacts', methods=['GET', 'POST'])
def manage_contacts():
    """Get all contacts or add new contact"""
    # demo user id (for frontend demo); in production use auth
    user_id = 1

    if request.method == 'POST':
        data = request.json or {}
        # Validate required fields
        name = data.get('name')
        phone = data.get('phone')
        relation = data.get('relation', '')
        email = data.get('email')

        if not name or not phone:
            return jsonify({'error': 'name and phone are required'}), 400

        # Check max 10 contacts
        contact_count = EmergencyContact.query.filter_by(user_id=user_id).count()
        if contact_count >= 10:
            return jsonify({'error': 'Maximum 10 contacts allowed'}), 400

        # Create contact
        contact = EmergencyContact(
            user_id=user_id,
            name=name,
            phone=phone,
            email=email,
            relation=relation,
            priority=contact_count + 1
        )
        db.session.add(contact)
        db.session.commit()

        return jsonify({
            'message': 'Contact added successfully',
            'contact': {
                'id': contact.id,
                'name': contact.name,
                'phone': contact.phone,
                'relation': contact.relation
            }
        }), 201

    # GET - return all contacts
    contacts = EmergencyContact.query.filter_by(user_id=user_id).order_by(EmergencyContact.priority).all()
    return jsonify([{
        'id': c.id,
        'name': c.name,
        'phone': c.phone,
        'email': c.email,
        'relation': c.relation,
        'priority': c.priority
    } for c in contacts])

@app.route('/api/contacts/<int:contact_id>', methods=['DELETE'])
def delete_contact(contact_id):
    """Delete specific contact"""
    contact = EmergencyContact.query.get_or_404(contact_id)
    db.session.delete(contact)
    db.session.commit()
    return jsonify({'message': 'Contact deleted successfully'})

# ==================== MEDICAL PROFILE API ====================

@app.route('/api/medical', methods=['GET', 'POST'])
def manage_medical():
    """Get or update medical profile"""
    user_id = 1

    if request.method == 'POST':
        data = request.json or {}
        medical = MedicalProfile.query.filter_by(user_id=user_id).first()

        if not medical:
            # create new if not exists
            medical = MedicalProfile(user_id=user_id)
            db.session.add(medical)

        # assign fields defensively
        medical.full_name = data.get('full_name')
        medical.age = data.get('age')
        medical.blood_group = data.get('blood_group')
        medical.height = data.get('height')
        medical.weight = data.get('weight')
        medical.allergies = data.get('allergies')
        medical.medications = data.get('medications')
        medical.conditions = data.get('conditions')
        medical.emergency_notes = data.get('emergency_notes')
        medical.insurance = data.get('insurance')

        db.session.commit()
        return jsonify({'message': 'Medical profile updated successfully'})

    # GET
    medical = MedicalProfile.query.filter_by(user_id=user_id).first()
    if not medical:
        return jsonify({'message': 'No medical profile found'}), 404

    return jsonify({
        'full_name': medical.full_name,
        'age': medical.age,
        'blood_group': medical.blood_group,
        'height': medical.height,
        'weight': medical.weight,
        'allergies': medical.allergies,
        'medications': medical.medications,
        'conditions': medical.conditions,
        'emergency_notes': medical.emergency_notes,
        'insurance': medical.insurance
    })

# ==================== SOS ALERT API ====================

@app.route('/api/sos', methods=['POST'])
def trigger_sos():
    """Trigger emergency SOS"""
    user_id = 1
    data = request.json or {}

    # Validate coordinates
    try:
        lat = float(data.get('latitude'))
        lon = float(data.get('longitude'))
    except (TypeError, ValueError):
        return jsonify({'error': 'latitude and longitude are required and must be numbers'}), 400

    address = data.get('address', 'Unknown location')

    # Create SOS alert
    sos_alert = SOSAlert(
        user_id=user_id,
        latitude=lat,
        longitude=lon,
        address=address
    )
    db.session.add(sos_alert)
    db.session.commit()

    # Get contacts and medical
    contacts = EmergencyContact.query.filter_by(user_id=user_id).all()
    medical = MedicalProfile.query.filter_by(user_id=user_id).first()

    # Simulate sending alerts
    notifications = [{
        'name': c.name,
        'phone': c.phone,
        'status': 'sent'
    } for c in contacts]

    return jsonify({
        'message': 'SOS alert triggered successfully',
        'alert_id': sos_alert.id,
        'contacts_notified': len(notifications),
        'location': {
            'latitude': sos_alert.latitude,
            'longitude': sos_alert.longitude,
            'maps_url': f"https://www.google.com/maps?q={sos_alert.latitude},{sos_alert.longitude}"
        },
        'medical_shared': {
            'blood_group': medical.blood_group if medical else 'N/A',
            'allergies': medical.allergies if medical else 'N/A'
        }
    })

# ==================== DATA SCIENCE / ML APIs ====================

@app.route('/api/analytics/overview')
def analytics_overview():
    """Get analytics overview"""
    incidents = IncidentReport.query.all()

    if not incidents:
        return jsonify({
            'total_incidents': 0,
            'message': 'No data yet'
        })

    # Build DataFrame safely
    rows = []
    for i in incidents:
        rows.append({
            'severity': None if i.severity is None else int(i.severity),
            'incident_type': None if i.incident_type is None else str(i.incident_type)
        })
    df = pd.DataFrame(rows)

    # handle missing values
    if df['severity'].dropna().empty:
        avg_sev = None
        high_risk_count = 0
        severity_dist = {}
    else:
        avg_sev = round(df['severity'].dropna().mean(), 2)
        high_risk_count = int((df['severity'] >= 4).sum())
        severity_dist = df['severity'].value_counts().to_dict()

    # incident type distribution
    type_dist = df['incident_type'].dropna().value_counts().to_dict()
    most_common = None
    if len(df['incident_type'].dropna()) > 0:
        most_common = df['incident_type'].mode().iloc[0]

    return jsonify({
        'total_incidents': int(len(df)),
        'average_severity': avg_sev,
        'high_risk_count': high_risk_count,
        'most_common_type': most_common,
        'severity_distribution': severity_dist,
        'type_distribution': type_dist
    })

@app.route('/api/analytics/hotspots')
def analytics_hotspots():
    """ML: DBSCAN clustering to identify hotspots"""
    incidents = IncidentReport.query.all()

    if len(incidents) < 3:
        return jsonify({
            'hotspots': [],
            'message': 'Need at least 3 incidents for clustering'
        })

    df = pd.DataFrame([{
        'latitude': float(i.latitude) if i.latitude is not None else None,
        'longitude': float(i.longitude) if i.longitude is not None else None,
        'severity': None if i.severity is None else int(i.severity),
        'incident_type': None if i.incident_type is None else str(i.incident_type)
    } for i in incidents])

    # Ensure coords are numeric and drop invalid rows
    df = df.dropna(subset=['latitude', 'longitude'])
    if df.empty:
        return jsonify({'hotspots': [], 'message': 'No valid location data'})

    coords = df[['latitude', 'longitude']].values
    # Use min_samples=3 to avoid tiny noisy clusters
    clustering = DBSCAN(eps=0.01, min_samples=3).fit(coords)
    df['cluster'] = clustering.labels_

    hotspots = []
    for cluster_id in sorted(df[df['cluster'] != -1]['cluster'].unique()):
        cluster_data = df[df['cluster'] == cluster_id]
        hotspots.append({
            'cluster_id': int(cluster_id),
            'latitude': float(cluster_data['latitude'].mean()),
            'longitude': float(cluster_data['longitude'].mean()),
            'incident_count': int(len(cluster_data)),
            'average_severity': float(cluster_data['severity'].dropna().mean()) if not cluster_data['severity'].dropna().empty else None,
            'most_common_type': cluster_data['incident_type'].mode().iloc[0] if not cluster_data['incident_type'].dropna().empty else None
        })

    return jsonify({
        'hotspots': hotspots,
        'total_clusters': len(hotspots)
    })

@app.route('/api/analytics/risk-score', methods=['POST'])
def calculate_risk():
    """Calculate risk score for location"""
    data = request.json or {}
    try:
        lat = float(data.get('latitude'))
        lon = float(data.get('longitude'))
    except (TypeError, ValueError):
        return jsonify({'error': 'latitude and longitude are required and must be numbers'}), 400

    radius = 0.01  # degrees ~1km (approx)

    incidents = IncidentReport.query.all()
    if not incidents:
        return jsonify({'risk_score': 0, 'nearby_incidents': 0, 'interpretation': 'Safe', 'message': 'No data'})

    df = pd.DataFrame([{
        'latitude': float(i.latitude) if i.latitude is not None else None,
        'longitude': float(i.longitude) if i.longitude is not None else None,
        'severity': None if i.severity is None else int(i.severity),
        'time': i.time_of_incident
    } for i in incidents])

    # Ensure time column is datetime
    df['time'] = pd.to_datetime(df['time'], errors='coerce')

    # Basic bounding-box filter (fast). Later replace with Haversine for accuracy.
    nearby = df[
        (df['latitude'].notna()) & (df['longitude'].notna()) &
        (df['latitude'].between(lat - radius, lat + radius)) &
        (df['longitude'].between(lon - radius, lon + radius))
    ]

    if nearby.empty:
        return jsonify({
            'risk_score': 0,
            'nearby_incidents': 0,
            'interpretation': 'Safe'
        })

    # compute components
    severity_vals = nearby['severity'].dropna()
    severity_weight = float(severity_vals.mean()) * 10 if not severity_vals.empty else 0
    frequency_weight = int(len(nearby)) * 2

    now = pd.to_datetime(datetime.utcnow())
    # create days_ago safely (coerce invalid times to large number)
    nearby['days_ago'] = (now - nearby['time']).dt.days.fillna(9999).astype(int)
    recent = nearby[nearby['days_ago'] <= 30]
    recency_weight = int(len(recent)) * 5

    risk_score = min(100, severity_weight + frequency_weight + recency_weight)

    if risk_score >= 70:
        interpretation = 'High Risk'
    elif risk_score >= 40:
        interpretation = 'Moderate'
    else:
        interpretation = 'Safe'

    return jsonify({
        'risk_score': round(float(risk_score), 2),
        'nearby_incidents': int(len(nearby)),
        'recent_incidents': int(len(recent)),
        'interpretation': interpretation
    })

# ==================== RUN SERVER ====================

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🛡️  SafeGuard API Server Starting...")
    print("="*60)
    print("\n📡 You can now call these APIs:")
    print("   GET  /api/contacts")
    print("   POST /api/contacts")
    print("   GET  /api/medical")
    print("   POST /api/medical")
    print("   POST /api/sos")
    print("   GET  /api/analytics/overview")
    print("   GET  /api/analytics/hotspots")
    print("   POST /api/analytics/risk-score")
    print("\n🌐 Server: http://localhost:5000")
    print("="*60 + "\n")
    
    app.run(debug=True, port=5000)
