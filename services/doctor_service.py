import sqlite3
from helpers.logger import dblogger

from repositories.doctor_repo import DoctorRepo

class DoctorService:
    def __init__(self,doctor_repo: DoctorRepo):
        self.doctor_repo = doctor_repo


    def add_doctor(self,doctor):
        try:
            if self.doctor_repo.doctor_exists(doctor):
                return {'success':False,'message':"Doctor Already Exists."}

            res = self.doctor_repo.add_doctor(doctor)
            if(res==1):
                return {'success':True,'message':"Doctor Added Successfully."}
            else:
                return {'success':False,'message':"Failed to Add Doctor."}
        except sqlite3.Error as e:
            dblogger.error(f"Database error: {e}")
            return {'success': False,'message': "Unable to add doctor schedule. Please try again."}


    def get_doctors_from_service(self,service):
        try:
            result = self.doctor_repo.get_doctors_from_service(service)
            if len(result)==0:
                return ({'success':False, 'message':f"No doctor added to {service} service."})
            # if there's a service, there'll be doctors so result can't be empty

            doctors_data = {t[0]:(t[1],t[2]) for t in result}
            doctor_ids = [t[0] for t in result]
            doctors_choices = '\n'.join([f"{t[0]:<15} {t[1]:<25} {t[2]}" for t in result])

            combined_data = (doctors_data,doctor_ids,doctors_choices)

            return {'success':True, 'message': f"Doctors with specialisation{service} fetched successfully.",'data':combined_data}
        except sqlite3.Error as e:
            dblogger(f"Database error: {e}")
            return {'success': False,'message': f"Unable to fetch doctors with specialisation {service}. Please try again."}