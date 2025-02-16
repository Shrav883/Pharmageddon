from app import mongo
from bson import ObjectId

class Patient:
    @staticmethod
    def add_patient(patient_data):
        patient_data['Visits']=[]
        result = mongo.db.patients.insert_one(patient_data)
        return str(result.inserted_id)

    @staticmethod
    def add_visit(patient_id, visit_data):
        result = mongo.db.patients.update_one(
            {"_id": ObjectId(patient_id)},
            {"$push": {"Visits": visit_data}, "$inc":{"Number of Visits":1}}
        )
        return result.modified_count > 0

    @staticmethod
    def get_all_patients():
        return list(mongo.db.patients.find())

    @staticmethod
    def get_patient(patient_id):
        return mongo.db.patients.find_one({"_id": ObjectId(patient_id)})

    @staticmethod
    def get_summary_data():
        patients = list(mongo.db.patients.find({}, {'_id': 0, 'Visits': 1}))
        return patients
