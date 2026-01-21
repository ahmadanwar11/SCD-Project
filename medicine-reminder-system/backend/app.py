"""
Main Flask Application for Medicine Reminder System
This file contains all API endpoints for the application
"""

from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import datetime, timedelta
from config import Config
from models import db, User, Patient, Doctor, Medicine, Reminder
import logging
import traceback

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "allow_headers": ["Content-Type", "Authorization"],
        "expose_headers": ["Content-Type", "Authorization"],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    }
})  # Enable Cross-Origin Resource Sharing
db.init_app(app)  # Initialize database
jwt = JWTManager(app)  # Initialize JWT for authentication

# ==================== JWT ERROR HANDLERS ====================

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    """Handle expired JWT tokens"""
    return jsonify({'error': 'Token has expired', 'message': 'Please login again'}), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    """Handle invalid JWT tokens"""
    return jsonify({'error': 'Invalid token', 'message': 'Please login again'}), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    """Handle missing JWT tokens"""
    return jsonify({'error': 'Authorization required', 'message': 'Please login to access this resource'}), 401

# ==================== AUTHENTICATION ENDPOINTS ====================

@app.route('/api/register', methods=['POST'])
def register():
    """Register a new user"""
    try:
        data = request.get_json()

        # Validate required fields
        if not data or not data.get('username') or not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Username, email, and password are required'}), 400

        # Check if user already exists
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Username already exists'}), 409

        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already exists'}), 409

        # Create new user
        new_user = User(
            username=data['username'],
            email=data['email']
        )
        new_user.set_password(data['password'])

        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            'message': 'User registered successfully',
            'user': new_user.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/login', methods=['POST'])
def login():
    """Login user and return JWT token"""
    try:
        data = request.get_json()

        # Validate required fields
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({'error': 'Username and password are required'}), 400

        # Find user
        user = User.query.filter_by(username=data['username']).first()

        # Check credentials
        if not user or not user.check_password(data['password']):
            return jsonify({'error': 'Invalid username or password'}), 401

        # Create JWT token (identity must be a string)
        access_token = create_access_token(identity=str(user.id))

        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'user': user.to_dict()
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/user/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get current logged-in user details"""
    try:
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)

        if not user:
            return jsonify({'error': 'User not found'}), 404

        return jsonify({'user': user.to_dict()}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== PATIENT ENDPOINTS ====================

@app.route('/api/patients', methods=['GET'])
@jwt_required()
def get_patients():
    """Get all patients for the logged-in user"""
    try:
        user_id = int(get_jwt_identity())
        patients = Patient.query.filter_by(user_id=user_id).all()

        return jsonify({
            'patients': [patient.to_dict() for patient in patients]
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/patients/<int:patient_id>', methods=['GET'])
@jwt_required()
def get_patient(patient_id):
    """Get a specific patient by ID"""
    try:
        user_id = int(get_jwt_identity())
        patient = Patient.query.filter_by(id=patient_id, user_id=user_id).first()

        if not patient:
            return jsonify({'error': 'Patient not found'}), 404

        return jsonify({'patient': patient.to_dict()}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/patients', methods=['POST'])
@jwt_required()
def create_patient():
    """Create a new patient"""
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json()

        # Log the request
        logger.info(f"Creating patient for user {user_id}")
        logger.debug(f"Request data: {data}")

        # Validate required fields
        required_fields = ['name', 'age', 'gender', 'phone']
        for field in required_fields:
            if not data.get(field):
                logger.warning(f"Missing required field: {field}")
                return jsonify({'error': f'{field} is required'}), 400

        # Create new patient
        new_patient = Patient(
            user_id=user_id,
            name=data['name'],
            age=data['age'],
            gender=data['gender'],
            phone=data['phone'],
            address=data.get('address', ''),
            medical_history=data.get('medical_history', '')
        )

        db.session.add(new_patient)
        db.session.commit()

        logger.info(f"Patient created successfully: {new_patient.id}")
        return jsonify({
            'message': 'Patient created successfully',
            'patient': new_patient.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating patient: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'error': str(e), 'details': 'Check server logs for more information'}), 500


@app.route('/api/patients/<int:patient_id>', methods=['PUT'])
@jwt_required()
def update_patient(patient_id):
    """Update a patient"""
    try:
        user_id = int(get_jwt_identity())
        patient = Patient.query.filter_by(id=patient_id, user_id=user_id).first()

        if not patient:
            return jsonify({'error': 'Patient not found'}), 404

        data = request.get_json()

        # Update fields
        if data.get('name'):
            patient.name = data['name']
        if data.get('age'):
            patient.age = data['age']
        if data.get('gender'):
            patient.gender = data['gender']
        if data.get('phone'):
            patient.phone = data['phone']
        if 'address' in data:
            patient.address = data['address']
        if 'medical_history' in data:
            patient.medical_history = data['medical_history']

        db.session.commit()

        return jsonify({
            'message': 'Patient updated successfully',
            'patient': patient.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/patients/<int:patient_id>', methods=['DELETE'])
@jwt_required()
def delete_patient(patient_id):
    """Delete a patient"""
    try:
        user_id = int(get_jwt_identity())
        patient = Patient.query.filter_by(id=patient_id, user_id=user_id).first()

        if not patient:
            return jsonify({'error': 'Patient not found'}), 404

        db.session.delete(patient)
        db.session.commit()

        return jsonify({'message': 'Patient deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ==================== DOCTOR ENDPOINTS ====================

@app.route('/api/doctors', methods=['GET'])
@jwt_required()
def get_doctors():
    """Get all doctors"""
    try:
        doctors = Doctor.query.all()

        return jsonify({
            'doctors': [doctor.to_dict() for doctor in doctors]
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/doctors/<int:doctor_id>', methods=['GET'])
@jwt_required()
def get_doctor(doctor_id):
    """Get a specific doctor by ID"""
    try:
        doctor = Doctor.query.get(doctor_id)

        if not doctor:
            return jsonify({'error': 'Doctor not found'}), 404

        return jsonify({'doctor': doctor.to_dict()}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/doctors', methods=['POST'])
@jwt_required()
def create_doctor():
    """Create a new doctor"""
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json()

        # Log the request
        logger.info(f"Creating doctor for user {user_id}")
        logger.debug(f"Request data: {data}")

        # Validate required fields
        required_fields = ['name', 'specialization', 'phone']
        for field in required_fields:
            if not data.get(field):
                logger.warning(f"Missing required field: {field}")
                return jsonify({'error': f'{field} is required'}), 400

        # Create new doctor
        new_doctor = Doctor(
            name=data['name'],
            specialization=data['specialization'],
            phone=data['phone'],
            email=data.get('email', ''),
            hospital=data.get('hospital', '')
        )

        db.session.add(new_doctor)
        db.session.commit()

        logger.info(f"Doctor created successfully: {new_doctor.id}")
        return jsonify({
            'message': 'Doctor created successfully',
            'doctor': new_doctor.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating doctor: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'error': str(e), 'details': 'Check server logs for more information'}), 500


@app.route('/api/doctors/<int:doctor_id>', methods=['PUT'])
@jwt_required()
def update_doctor(doctor_id):
    """Update a doctor"""
    try:
        doctor = Doctor.query.get(doctor_id)

        if not doctor:
            return jsonify({'error': 'Doctor not found'}), 404

        data = request.get_json()

        # Update fields
        if data.get('name'):
            doctor.name = data['name']
        if data.get('specialization'):
            doctor.specialization = data['specialization']
        if data.get('phone'):
            doctor.phone = data['phone']
        if 'email' in data:
            doctor.email = data['email']
        if 'hospital' in data:
            doctor.hospital = data['hospital']

        db.session.commit()

        return jsonify({
            'message': 'Doctor updated successfully',
            'doctor': doctor.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/doctors/<int:doctor_id>', methods=['DELETE'])
@jwt_required()
def delete_doctor(doctor_id):
    """Delete a doctor"""
    try:
        doctor = Doctor.query.get(doctor_id)

        if not doctor:
            return jsonify({'error': 'Doctor not found'}), 404

        db.session.delete(doctor)
        db.session.commit()

        return jsonify({'message': 'Doctor deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ==================== MEDICINE ENDPOINTS ====================

@app.route('/api/medicines', methods=['GET'])
@jwt_required()
def get_medicines():
    """Get all medicines for the logged-in user's patients"""
    try:
        user_id = int(get_jwt_identity())
        # Get all patients of this user
        patients = Patient.query.filter_by(user_id=user_id).all()
        patient_ids = [p.id for p in patients]

        # Get all medicines for these patients
        medicines = Medicine.query.filter(Medicine.patient_id.in_(patient_ids)).all()

        return jsonify({
            'medicines': [medicine.to_dict() for medicine in medicines]
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/medicines/<int:medicine_id>', methods=['GET'])
@jwt_required()
def get_medicine(medicine_id):
    """Get a specific medicine by ID"""
    try:
        user_id = int(get_jwt_identity())
        medicine = Medicine.query.get(medicine_id)

        if not medicine:
            return jsonify({'error': 'Medicine not found'}), 404

        # Check if this medicine belongs to user's patient
        if medicine.patient.user_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403

        return jsonify({'medicine': medicine.to_dict()}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/medicines', methods=['POST'])
@jwt_required()
def create_medicine():
    """Create a new medicine prescription"""
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json()

        # Validate required fields
        required_fields = ['patient_id', 'doctor_id', 'medicine_name', 'dosage', 'frequency', 'start_date']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400

        # Verify patient belongs to user
        patient = Patient.query.filter_by(id=data['patient_id'], user_id=user_id).first()
        if not patient:
            return jsonify({'error': 'Patient not found'}), 404

        # Verify doctor exists
        doctor = Doctor.query.get(data['doctor_id'])
        if not doctor:
            return jsonify({'error': 'Doctor not found'}), 404

        # Parse dates
        start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
        end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date() if data.get('end_date') else None

        # Create new medicine
        new_medicine = Medicine(
            patient_id=data['patient_id'],
            doctor_id=data['doctor_id'],
            medicine_name=data['medicine_name'],
            dosage=data['dosage'],
            frequency=data['frequency'],
            time=data.get('time', ''),
            start_date=start_date,
            end_date=end_date,
            status=data.get('status', 'active')
        )

        db.session.add(new_medicine)
        db.session.commit()

        return jsonify({
            'message': 'Medicine created successfully',
            'medicine': new_medicine.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/medicines/<int:medicine_id>', methods=['PUT'])
@jwt_required()
def update_medicine(medicine_id):
    """Update a medicine"""
    try:
        user_id = int(get_jwt_identity())
        medicine = Medicine.query.get(medicine_id)

        if not medicine:
            return jsonify({'error': 'Medicine not found'}), 404

        # Check if this medicine belongs to user's patient
        if medicine.patient.user_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403

        data = request.get_json()

        # Update fields
        if data.get('medicine_name'):
            medicine.medicine_name = data['medicine_name']
        if data.get('dosage'):
            medicine.dosage = data['dosage']
        if data.get('frequency'):
            medicine.frequency = data['frequency']
        if 'time' in data:
            medicine.time = data['time']
        if data.get('start_date'):
            medicine.start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
        if 'end_date' in data and data['end_date']:
            medicine.end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
        if data.get('status'):
            medicine.status = data['status']

        db.session.commit()

        return jsonify({
            'message': 'Medicine updated successfully',
            'medicine': medicine.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/medicines/<int:medicine_id>', methods=['DELETE'])
@jwt_required()
def delete_medicine(medicine_id):
    """Delete a medicine"""
    try:
        user_id = int(get_jwt_identity())
        medicine = Medicine.query.get(medicine_id)

        if not medicine:
            return jsonify({'error': 'Medicine not found'}), 404

        # Check if this medicine belongs to user's patient
        if medicine.patient.user_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403

        db.session.delete(medicine)
        db.session.commit()

        return jsonify({'message': 'Medicine deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ==================== REMINDER ENDPOINTS ====================

@app.route('/api/reminders', methods=['GET'])
@jwt_required()
def get_reminders():
    """Get all reminders for the logged-in user"""
    try:
        user_id = int(get_jwt_identity())
        # Get all patients of this user
        patients = Patient.query.filter_by(user_id=user_id).all()
        patient_ids = [p.id for p in patients]

        # Get all medicines for these patients
        medicines = Medicine.query.filter(Medicine.patient_id.in_(patient_ids)).all()
        medicine_ids = [m.id for m in medicines]

        # Get all reminders for these medicines
        reminders = Reminder.query.filter(Reminder.medicine_id.in_(medicine_ids)).order_by(Reminder.reminder_time).all()

        return jsonify({
            'reminders': [reminder.to_dict() for reminder in reminders]
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/reminders/<int:reminder_id>', methods=['GET'])
@jwt_required()
def get_reminder(reminder_id):
    """Get a specific reminder by ID"""
    try:
        user_id = int(get_jwt_identity())
        reminder = Reminder.query.get(reminder_id)

        if not reminder:
            return jsonify({'error': 'Reminder not found'}), 404

        # Check if this reminder belongs to user's patient
        if reminder.medicine.patient.user_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403

        return jsonify({'reminder': reminder.to_dict()}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/reminders', methods=['POST'])
@jwt_required()
def create_reminder():
    """Create a new reminder"""
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json()

        # Validate required fields
        if not data.get('medicine_id') or not data.get('reminder_time'):
            return jsonify({'error': 'medicine_id and reminder_time are required'}), 400

        # Verify medicine belongs to user's patient
        medicine = Medicine.query.get(data['medicine_id'])
        if not medicine or medicine.patient.user_id != user_id:
            return jsonify({'error': 'Medicine not found'}), 404

        # Parse reminder time
        reminder_time = datetime.strptime(data['reminder_time'], '%Y-%m-%dT%H:%M')

        # Create new reminder
        new_reminder = Reminder(
            medicine_id=data['medicine_id'],
            reminder_time=reminder_time,
            status=data.get('status', 'pending'),
            notes=data.get('notes', '')
        )

        db.session.add(new_reminder)
        db.session.commit()

        return jsonify({
            'message': 'Reminder created successfully',
            'reminder': new_reminder.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/reminders/<int:reminder_id>', methods=['PUT'])
@jwt_required()
def update_reminder(reminder_id):
    """Update a reminder"""
    try:
        user_id = int(get_jwt_identity())
        reminder = Reminder.query.get(reminder_id)

        if not reminder:
            return jsonify({'error': 'Reminder not found'}), 404

        # Check if this reminder belongs to user's patient
        if reminder.medicine.patient.user_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403

        data = request.get_json()

        # Update fields
        if data.get('reminder_time'):
            reminder.reminder_time = datetime.strptime(data['reminder_time'], '%Y-%m-%dT%H:%M')
        if data.get('status'):
            reminder.status = data['status']
            if data['status'] == 'completed':
                reminder.completed_at = datetime.utcnow()
        if 'notes' in data:
            reminder.notes = data['notes']

        db.session.commit()

        return jsonify({
            'message': 'Reminder updated successfully',
            'reminder': reminder.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/reminders/<int:reminder_id>', methods=['DELETE'])
@jwt_required()
def delete_reminder(reminder_id):
    """Delete a reminder"""
    try:
        user_id = int(get_jwt_identity())
        reminder = Reminder.query.get(reminder_id)

        if not reminder:
            return jsonify({'error': 'Reminder not found'}), 404

        # Check if this reminder belongs to user's patient
        if reminder.medicine.patient.user_id != user_id:
            return jsonify({'error': 'Unauthorized'}), 403

        db.session.delete(reminder)
        db.session.commit()

        return jsonify({'message': 'Reminder deleted successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ==================== DASHBOARD ENDPOINT ====================

@app.route('/api/dashboard', methods=['GET'])
@jwt_required()
def get_dashboard():
    """Get dashboard data - patients, doctors, today's medicines"""
    try:
        user_id = int(get_jwt_identity())
        logger.info(f"Loading dashboard for user {user_id}")

        # Get all patients
        patients = Patient.query.filter_by(user_id=user_id).all()
        patient_ids = [p.id for p in patients]
        logger.debug(f"Found {len(patients)} patients")

        # Get all medicines (only if there are patients)
        medicines = []
        if patient_ids:
            medicines = Medicine.query.filter(Medicine.patient_id.in_(patient_ids)).all()
        logger.debug(f"Found {len(medicines)} medicines")

        # Get today's reminders (only if there are medicines)
        today_reminders = []
        if medicines:
            today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            today_end = datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999)

            medicine_ids = [m.id for m in medicines]
            today_reminders = Reminder.query.filter(
                Reminder.medicine_id.in_(medicine_ids),
                Reminder.reminder_time >= today_start,
                Reminder.reminder_time <= today_end
            ).order_by(Reminder.reminder_time).all()
        logger.debug(f"Found {len(today_reminders)} reminders for today")

        # Get unique doctors from medicines
        doctor_ids = list(set([m.doctor_id for m in medicines])) if medicines else []
        doctors = Doctor.query.filter(Doctor.id.in_(doctor_ids)).all() if doctor_ids else []
        logger.debug(f"Found {len(doctors)} doctors")

        return jsonify({
            'patients': [patient.to_dict() for patient in patients],
            'doctors': [doctor.to_dict() for doctor in doctors],
            'today_reminders': [reminder.to_dict() for reminder in today_reminders],
            'total_medicines': len(medicines)
        }), 200

    except Exception as e:
        logger.error(f"Error loading dashboard: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({'error': str(e), 'details': 'Check server logs for more information'}), 500


# ==================== HEALTH CHECK ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Simple health check endpoint"""
    return jsonify({'status': 'OK', 'message': 'Medicine Reminder API is running'}), 200


# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    db.session.rollback()
    return jsonify({'error': 'Internal server error'}), 500


# ==================== RUN APPLICATION ====================

if __name__ == '__main__':
    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")

    # Run the application
    print("Starting Medicine Reminder System API...")
    print("API is running on http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
