import sqlite3
from helpers.logger import dblogger

from repositories.patient_repo import PatientRepo

class PatientService:
    def __init__(self,patient_repo_obj: PatientRepo):
        self.patient_repo = patient_repo_obj

    def patient_exists(self,patient):
        try:
            result = self.patient_repo.patient_exists(patient)

            if result is None:
                return {'success': False,'message': f"Patient with id {patient.patient_id} Not Found"}
            return {'success': True,'message': f"Patient Account Already exists with ID {result}"}
        except sqlite3.Error as e:
            dblogger.error(f"Database error: {e}")
            return {'success': False,'message': "Unable to check if patient exists. Please try again."}

    def register_patient(self,patient):
        try:
            result = self.patient_exists(patient)

            if not result['success']:
                patient_id = self.patient_repo.register_patient(patient)
                if(patient_id):
                    return {'success':True,'message':"Patient Registration Successfully.",'data':patient_id}
            else:
                return {'success':False,'message':result['message']}
        except sqlite3.Error as e:
            dblogger.error(f"Database error: {e}")
            return {'success': False,'message': "Unable to register patient. Please try again."}

    def get_patient_info(self,patient_id):
        try:
            result = self.patient_repo.get_patient_info(patient_id)
            if result is None:
                return {'success':False,'message':f"Patient with ID {patient_id} Not Found."}
            
            return {'success':True,'message':"Patient information fetched successfully.",'data':result}
        except sqlite3.Error as e:
            dblogger.error(f"Database error: {e}")
            return {'success': False,'message': "Unable to fetch patient information. Please try again."}
