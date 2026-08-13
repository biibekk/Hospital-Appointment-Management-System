import sqlite3
from helpers.logger import dblogger

from repositories.doctor_repo import DoctorRepo

class DoctorService:
    def __init__(self,doctor_repo: DoctorRepo):
        self.repo = doctor_repo

    def add_doctor(self,doctor):
        try:
            if self.repo.doctor_exists(doctor):
                return {'success':False,'message':"Doctor Already Exists."}

            res = self.repo.add_doctor(doctor)
            if(res==1):
                return {'success':True,'message':"Doctor Added Successfully."}
            else:
                return {'success':False,'message':"Failed to Add Doctor."}
        except sqlite3.Error as e:
            dblogger.error(f"Database error: {e}")
            return {'success': False,'message': "Unable to add doctor schedule. Please try again."}

    def add_error_check(self,*args):
        try:
            self.repo.add_error_check(*args)
        except sqlite3.Error as e:
            dblogger.error(f"Database error: {e}")
            return {'success': False,'message': "Unable to add doctor schedule. Please try again."}