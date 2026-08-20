import sqlite3
from datetime import datetime, timedelta
from helpers.logger import dblogger
from models.doctor_model import DoctorModel
from repositories.doctorschedule_repo import DoctorScheduleRepo   # for function syntax highlight
from repositories.doctor_repo import DoctorRepo

class DoctorScheduleService:
    def __init__(self,schedule_obj: DoctorScheduleRepo,doctor_repo: DoctorRepo):
        self.schedule_repo = schedule_obj
        self.doctor_repo = doctor_repo

    def add_doctor_schedule(self,schedule):
        try:
            doctor = DoctorModel(schedule.doctor_id,None,None,None,None)
            if not self.doctor_repo.doctor_exists(doctor):
                return {'success':False,'message':"Doctor Not Found."}

            if self.schedule_repo.doctor_schedule_exists(schedule):
                return {'success':False,'message':"Doctor Schedule Already Exists."}

            res = self.schedule_repo.add_doctor_schedule(schedule)

            if(res==1):
                return {'success':True,'message':"Doctor Schedule Added Successfully."}
        except sqlite3.Error as e:
            dblogger.error(f"Database error: {e}")
            return {'success': False,'message': "Unable to add doctor schedule. Please try again."}

    def get_doctor_slots(self,doctor_id,date):
        try: 
            result = self.schedule_repo.get_doctor_slots(doctor_id,date)
            selected_date = datetime.strptime(date,"%Y-%m-%d").date()
            slots = []
            today_date = datetime.now().date()
            current_time = datetime.now()
            
            for id,st,et,sd in result:
                start_time = datetime.strptime(st,"%H:%M").time()   # gives 1901 as dummy date
                end_time = datetime.strptime(et,"%H:%M").time()

                # add selected date to time
                start_time = datetime.combine(selected_date, start_time)
                end_time = datetime.combine(selected_date,end_time)
                slot_duration = int(sd)
                duration = timedelta(minutes=slot_duration)
                current = start_time
                while current + duration <= end_time:
                    if selected_date == today_date and current <= current_time:
                        current += duration
                        continue
                    slots.append((
                        current.strftime("%H:%M"),
                        (current+duration).strftime("%H:%M")
                    ))
                    current += duration

            return slots
        except sqlite3.Error as e:
            dblogger.error(f"Database error: {e}")
            return {'success': False,'message': "Unable to get doctor slots. Please try again."}