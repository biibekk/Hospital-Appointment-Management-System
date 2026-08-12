from models.doctor_model import DoctorModel
from helpers.display_help import display

class DoctorScheduleService:
    def __init__(self,schedule_obj,doctor_repo):
        self.repo = schedule_obj
        self.doctor_repo = doctor_repo

    def add_doctor_schedule(self,schedule):
        doctor = DoctorModel(None,None,None,None,schedule.doctor_id)
        if not self.doctor_repo.doctor_exists(doctor):
            display("Doctor Not Found.")
            return
        elif self.repo.doctor_schedule_exists(schedule):
            display("Doctor Schedule Already Exists.")
            return

        res = self.repo.add_doctor_schedule(schedule)

        if(res==1):
            display("Doctor Schedule Added Successfully.")
        else:
            display("Doctor Schedule Addition Failed.")

