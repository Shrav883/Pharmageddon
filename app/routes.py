from flask import Blueprint, request, jsonify, app
from app.models import Patient
from app.utils import convert_objectid
from flask_pymongo import PyMongo
#from app import mongo
from  app import mongo
from flask import Flask, jsonify
from flask_pymongo import PyMongo
from bson import json_util
import json
from flask import render_template, request, redirect, url_for

main = Blueprint('main', __name__)
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    return jsonify({"message": "Welcome to the API!"})


@main.route('/test_db')
def test_db():
    try:
        mongo.db.command('ping')
        return jsonify({"message": "Connected successfully to MongoDB!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route('/api/patients', methods=['GET'])
def get_patients():
    patients = Patient.get_all_patients()
    return jsonify([{**p, '_id': convert_objectid(p['_id'])} for p in patients])

@main.route('/api/patients', methods=['POST'])
def add_patient():
    patient_data = request.json
    patient_id = Patient.add_patient(patient_data)
    return jsonify({"message": "Patient added successfully", "id": patient_id}), 201

@main.route('/api/patients/<patient_id>', methods=['GET'])
def get_patient(patient_id):
    patient = Patient.get_patient(patient_id)
    if patient:
        patient['_id'] = convert_objectid(patient['_id'])
        return jsonify(patient)
    return jsonify({"message": "Patient not found"}), 404

@main.route('/api/patients/<patient_id>/visits', methods=['POST'])
def add_visit(patient_id):
    visit_data = request.json
    if Patient.add_visit(patient_id, visit_data):
        return jsonify({"message": "Visit added successfully"}), 200
    return jsonify({"message": "Patient not found"}), 404


@main.route('/api/summary', methods=['GET'])
def get_summary():
    patients = Patient.get_summary_data()

    symptom_counts = {"Diarrhea": 0, "Headache": 0, "Rashes": 0}
    total_visits = 0

    for patient in patients:
        for visit in patient['Visits']:
            total_visits += 1
            for symptom, value in visit['Symptoms'].items():
                if value:
                    symptom_counts[symptom] += 1

    symptom_percentages = {symptom: (count / total_visits) * 100 for symptom, count in symptom_counts.items()}

    return jsonify({
        'symptom_percentages': symptom_percentages,
        'total_visits': total_visits
    })

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/new_patient')
def new_patient():
    return render_template('new_patient.html')

@main.route('/add_patient', methods=['POST'])
def add_patient():
    # Process form data and add patient to database
    # Redirect to index page after adding
    return redirect(url_for('index'))

@main.route('/existing_patient')
def existing_patient():
    return render_template('existing_patient.html')

@main.route('/add_visit', methods=['POST'])
def add_visit():
    # Process form data and add visit to database
    # Redirect to index page after adding
    return redirect(url_for('index'))

@main.route('/charts')
def charts():
    # Fetch and process data for charts
    success_fail_data = [60, 40]  # Example data
    symptoms_data = [30, 20, 10]  # Example data
    doses_labels = [1, 2, 3]
    doses_impact_data = [0.6, 0.7, 0.5]  # Example data

    return render_template('charts.html',
                           success_fail_data=success_fail_data,
                           symptoms_data=symptoms_data,
                           doses_labels=doses_labels,
                           doses_impact_data=doses_impact_data)