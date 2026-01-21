"""
Database models for Medicine Reminder System
Defines all the tables: users, patients, doctors, medicines, reminders
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize SQLAlchemy (will be configured in app.py)
db = SQLAlchemy()

class User(db.Model):
    """User model for authentication"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship with patients (one user can have multiple patients)
    patients = db.relationship('Patient', backref='user', lazy=True, cascade='all, delete-orphan')

    def set_password(self, password):
        """Hash and set the user's password"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check if provided password matches the hash"""
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        """Convert user object to dictionary (for JSON responses)"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Patient(db.Model):
    """Patient model - stores patient information"""
    __tablename__ = 'patients'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    address = db.Column(db.Text)
    medical_history = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship with medicines (one patient can have multiple medicines)
    medicines = db.relationship('Medicine', backref='patient', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        """Convert patient object to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'phone': self.phone,
            'address': self.address,
            'medical_history': self.medical_history,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Doctor(db.Model):
    """Doctor model - stores doctor information"""
    __tablename__ = 'doctors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    specialization = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(120))
    hospital = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship with medicines (one doctor can prescribe multiple medicines)
    medicines = db.relationship('Medicine', backref='doctor', lazy=True)

    def to_dict(self):
        """Convert doctor object to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'specialization': self.specialization,
            'phone': self.phone,
            'email': self.email,
            'hospital': self.hospital,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Medicine(db.Model):
    """Medicine model - stores medicine prescriptions"""
    __tablename__ = 'medicines'

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    medicine_name = db.Column(db.String(200), nullable=False)
    dosage = db.Column(db.String(100), nullable=False)  # e.g., "500mg", "2 tablets"
    frequency = db.Column(db.String(100), nullable=False)  # e.g., "3 times a day", "Every 8 hours"
    time = db.Column(db.String(100))  # e.g., "Morning, Afternoon, Night"
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    status = db.Column(db.String(20), default='active')  # active, completed, discontinued
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship with reminders (one medicine can have multiple reminders)
    reminders = db.relationship('Reminder', backref='medicine', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        """Convert medicine object to dictionary"""
        return {
            'id': self.id,
            'patient_id': self.patient_id,
            'patient_name': self.patient.name if self.patient else None,
            'doctor_id': self.doctor_id,
            'doctor_name': self.doctor.name if self.doctor else None,
            'medicine_name': self.medicine_name,
            'dosage': self.dosage,
            'frequency': self.frequency,
            'time': self.time,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Reminder(db.Model):
    """Reminder model - stores individual medicine reminders"""
    __tablename__ = 'reminders'

    id = db.Column(db.Integer, primary_key=True)
    medicine_id = db.Column(db.Integer, db.ForeignKey('medicines.id'), nullable=False)
    reminder_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, completed, missed
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)

    def to_dict(self):
        """Convert reminder object to dictionary"""
        return {
            'id': self.id,
            'medicine_id': self.medicine_id,
            'medicine_name': self.medicine.medicine_name if self.medicine else None,
            'dosage': self.medicine.dosage if self.medicine else None,
            'patient_name': self.medicine.patient.name if self.medicine and self.medicine.patient else None,
            'reminder_time': self.reminder_time.isoformat() if self.reminder_time else None,
            'status': self.status,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }
