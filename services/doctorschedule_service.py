import sqlite3
from helpers.logger import dblogger
from models.doctor_model import DoctorModel
from repositories.doctorschedule_repo import DoctorScheduleRepo   # for function syntax highlight
from repositories.doctor_repo import DoctorRepo

class DoctorScheduleService:
    def __init__(self,schedule_obj: DoctorScheduleRepo,doctor_repo: DoctorRepo):
        self.repo = schedule_obj
        self.doctor_repo = doctor_repo

    def add_doctor_schedule(self,schedule):
        try:
            doctor = DoctorModel(None,None,None,None,schedule.doctor_id)
            if not self.doctor_repo.doctor_exists(doctor):
                return {'success':False,'message':"Doctor Not Found."}

            if self.repo.doctor_schedule_exists(schedule):
                return {'success':False,'message':"Doctor Schedule Already Exists."}

            res = self.repo.add_doctor_schedule(schedule)

            if(res==1):
                return {'success':True,'message':"Doctor Schedule Added Successfully."}
            else:
                return {'success':False,'message':"Doctor Schedule Addition Failed."}
        except sqlite3.Error as e:
            dblogger.error(f"Database error: {e}")
            return {'success': False,'message': "Unable to add doctor schedule. Please try again."}