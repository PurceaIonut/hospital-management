from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital.db'
app.config['JWT_SECRET_KEY'] = 'hospital_management'
jwt = JWTManager(app)


db = SQLAlchemy()
db.init_app(app)


class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    role = db.Column(db.String(50))


class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(50))

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(50))
    doctor_id = db.Column(db.Integer(), db.ForeignKey('doctor.id') )
    assistant_id = db.Column(db.Integer(), db.ForeignKey('assistant.id'))

class Assistant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(50))
    doctor_id = db.Column(db.Integer(), db.ForeignKey('doctor.id') )

class Treatment(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.String(255))
    doctor_id = db.Column(db.Integer(), db.ForeignKey('doctor.id'))
    assistant_id = db.Column(db.Integer(), db.ForeignKey('assistant.id'))
    patient_id = db.Column(db.Integer(), db.ForeignKey('patient.id'))


#Register Admin
@app.route('/register/admin', methods=['GET'])
def admin():
    admin = User(email= 'general_manager@example.com', password = 'password', role= 'General Manager')
    db.session.add(admin)
    db.session.commit()
    return 'Admin has been created'

#This line should be called just first time to make General Manager User


#Login Route
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({'message': 'User not found'}), 404

    if not user.password == password:
        return jsonify({'message': 'Incorrect password'}), 401

    # create access token
    access_token = create_access_token(identity=user.id)
    return jsonify({'access_token': access_token}), 200

#Doctor Management
#Add new doctor
@app.route('/doctor', methods=['POST'])
@jwt_required()
def create_doctor():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    if current_user.role == 'General Manager':
        data = request.get_json()
        doctor = Doctor(email= data['email'],name = data['name'], password = data['password'])
        new_user = User(email=data['email'],password = data['password'], role = 'Doctor')
        db.session.add(doctor)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message:' : 'New doctor added'})
    else:
        return jsonify({'message': 'Unauthorized access'}), 401


#Get all doctors
@app.route('/doctors', methods=['GET'])
@jwt_required()
def get_all_doctors():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    if current_user.role == 'General Manager':
        all_doctros = Doctor.query.all()
        return jsonify([{'id': doctor.id, 'email': doctor.email,'name': doctor.name, 'password': doctor.password} for doctor in all_doctros])
    else:
        return jsonify({'message': 'Unauthorized access'}), 401
    
    
#Delete a doctor by ID
@app.route('/doctor/<id>', methods=['DELETE'])
@jwt_required()
def delete_doctor(id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    if current_user.role == 'General Manager':
        doctor = Doctor.query.get(id)
        user = User.query.filter_by(email=doctor.email).first()
        db.session.delete(doctor)
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'Doctor has been deleted'})
    else:
        return jsonify({'message': 'Unauthorized access'}), 401

#Patient management

#Add new patient
@app.route('/patient', methods=['POST'])
@jwt_required()
def crate_patient():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    if current_user.role == 'General Manager' or current_user.role == 'Doctor':
        data = request.get_json()
        patient = Patient(email= data['email'], name = data['name'], password = data['password'])
        new_user = User(email=data['email'],password = data['password'], role = 'Patient')
        db.session.add(patient)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'New patient added'})
    else:
        return jsonify({'message': 'Unauthorized access'}), 401

#Get all patients
@app.route('/patients', methods=['GET'])
@jwt_required()
def get_all_patients():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    if current_user.role == 'General Manager' or current_user.role == 'Doctor':
        all_patients= Patient.query.all()
        return jsonify([{'id': patient.id, 'email': patient.email, 'name': patient.name, 'password': patient.password} for patient in all_patients])
    else:
        return jsonify({'message': 'Unauthorized access'}), 401
    

#Delete a pacient
@app.route('/patient/<id>',methods=['DELETE'])
@jwt_required()
def delete_patient(id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    if current_user.role == 'General Manager' or current_user.role == 'Doctor':
        patient = Patient.query.get(id)
        user = User.query.filter_by(email=patient.email).first()
        db.session.delete(patient)
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'Patient has been deleted'})
    else:
        return jsonify({'message': 'Unauthorized access'}), 401


#Assistant management

#Add new assistant
@app.route('/assistant', methods=['POST'])
@jwt_required()
def create_assistant():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    if current_user.role == 'General Manager':
        data = request.get_json()
        assistant = Assistant(email= data['email'], name = data['name'], password = data['password'])
        new_user = User(email=data['email'],password = data['password'], role = 'Assistant')
        db.session.add(assistant)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'New assistent added'})
    else:
        return jsonify({'message': 'Unauthorized access'}), 401

#Get all assistants
@app.route('/assistants', methods=['GET'])
@jwt_required()
def get_all_assistants():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    if current_user.role == 'General Manager':
        all_assistants = Assistant.query.all()
        return jsonify([{'id': assistant.id,'email': assistant.email, 'name': assistant.name, 'doctor_id': assistant.doctor_id} for assistant in all_assistants])
    else:
        return jsonify({'message': 'Unauthorized access'}), 401

#Delete assistant
@app.route('/assistant/<id>', methods=['DELETE'])
@jwt_required()
def delete_assistant(id):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    if current_user.role == 'General Manager':
        assistant = Assistant.query.get(id)
        user = User.query.filter_by(email=assistant.email).first()
        db.session.delete(assistant)
        db.session.delete(user)
        db.session.commit()
        return jsonify({'Message': 'Assistent has been deleted'})
    else:
        return jsonify({'message': 'Unauthorized access'}), 401


#The treatment recommended by a doctor to a Patient
@app.route('/treatment/patient/assign', methods=['POST'])
@jwt_required()
def doctor_treatment():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    if current_user.role == 'Doctor':
        data = request.get_json()
        treatment = Treatment(name=data['name'], description=data['description'], patient_id = data['patient_id'], doctor_id = data['doctor_id'])
        db.session.add(treatment)
        db.session.commit()
        return jsonify({'message': 'Treatment assigned to patient'})
    else:
        return jsonify({'message': 'Unauthorized access'}), 401


# Patient assignment to a Assistant
@app.route('/patient/<string:patient_name>/assign', methods=['POST'])
@jwt_required()
def assign_patient(patient_name):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    if current_user.role == 'General Manager' or current_user.role == 'Doctor':
        data = request.get_json()
        assistant_id = data['assistant_id']
        patient = Patient.query.filter_by(name=patient_name).first()
        if not patient:
            return jsonify({'message': 'Patient not found'}), 404
        patient.assistant_id = assistant_id
        db.session.commit()
        return jsonify({'message': 'Patient assigned to Assistant!'})
    else:
        return jsonify({'message': 'Unauthorized access'}), 401

#Treatment applied by an Assistant
@app.route('/treatment/patient/assign', methods=['POST'])
@jwt_required()
def assistant_treatment():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    if current_user.role == 'Assistant':
        data = request.get_json()
        treatment = Treatment(name=data['name'], description=data['description'], patient_id = data['patient_id'], assistant_id = data['assistant_id'])
        db.session.add(treatment)
        db.session.commit()
        return jsonify({'message': 'Treatment assigned to patient'})
    else:
        return jsonify({'message': 'Unauthorized access'}), 401

#Report containing the list of all the Doctors and the associated patients
@app.route('/report/', methods=['GET'])
@jwt_required()
def report_doctors():
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    if current_user.role == 'General Manager':
        doctors = Doctor.query.all()
        report = []
        for doctor in doctors:
            patients = Patient.query.filter_by(doctor_id=doctor.id).all()
            report.append({'doctor': doctor.name, 'patients': [{'id': patient.id, 'name': patient.name, 'email': patient.email} for patient in patients]})
        statistics = {'total_doctors': len(doctors), 'total_patients': len(Patient.query.all()), 'total_treatments': len(Treatment.query.all())}
        return jsonify({'report': report, 'statistics': statistics})
    else:
        return jsonify({'message': 'Unauthorized access'}), 401
    
# Report with all the treatments applied to a Patient (JSON)
@app.route('/patient/<string:patient_name>/treatments', methods=['GET'])
@jwt_required()
def get_patient_treatments(patient_name):
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    if current_user.role == 'General Manager' or current_user.role == 'Doctor':
        patient = Patient.query.filter_by(name=patient_name).first()
        if patient:
            treatments = Treatment.query.filter_by(patient_id=patient.id).all()
            treatment_list = []
            for treatment in treatments:
                t = {
                    'name': treatment.name,
                    'description': treatment.description,
                }
                treatment_list.append(t)
            return jsonify(treatment_list)
        else:
            return jsonify({'message': 'Patient not found'}), 404
    else:
        return jsonify({'message': 'Unauthorized access'}), 401

with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)
