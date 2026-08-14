import re
from datetime import datetime

from services.appointments_service import AppointmentsService
from services.doctor_service import DoctorService
from services.doctorschedule_service import DoctorScheduleService
from services.patient_service import PatientService

from models.doctor_model import DoctorModel
from models.doctorschedule_model import DoctorSchedule

from helpers.display_help import display
from helpers.validators import Validators

admin_prompt = f"""\n{'-'*29}
     Hospital Admin Menu
{'-'*29}
1. Add Doctor
2. Add Doctor Schedule
3. View Doctors - not added
4. View Schedules - not added
5. Go Back
Enter your choice: """

class HospitalAdminMenu:
    def __init__(self,appointment_s: AppointmentsService,doctor_s: DoctorService,doctorschedule_s: DoctorScheduleService,patient_s: PatientService):
        self.appointment_s = appointment_s
        self.doctor_s = doctor_s
        self.doctorschedule_s = doctorschedule_s
        self.patient_s = patient_s


    def add_doctor(self):
        display("Add Doctor")
        name = Validators.get_non_empty_string("Enter your name: ")
        contact = Validators.get_contact("Enter contact no: ",10)
        spec = Validators.get_non_empty_string("Enter specialisation: ")
        fee = Validators.get_int("Enter consultation fee: ")

        new_doctor = DoctorModel(name,contact,spec,fee)
        result = self.doctor_s.add_doctor(new_doctor)
        display(result['message'])


    def add_doctor_schedule(self):
        display("Add Doctor Schedule")
        doctor_id = Validators.get_int("Enter Doctor ID: ")
        date = Validators.get_future_date("Enter schedule date(yyyy-mm-dd): ")

        start_time = Validators.get_time("Enter start time(24 Hour - HH:MM): ")
        end_time = Validators.get_time("Enter end time(24 Hour - HH:MM): ")

        new_doctor_schedule = DoctorSchedule(doctor_id,date,start_time,end_time)
        result = self.doctorschedule_s.add_doctor_schedule(new_doctor_schedule)
        display(result['message'])
        
    def hospital_admin_menu(self):
        admin_input = input(admin_prompt)
        while admin_input != '5':
            if admin_input == '1':
                self.add_doctor()
            elif admin_input == '2':
                self.add_doctor_schedule()
            elif admin_input == '5':
                break
            else:
                display("Please enter a valid input.")
            admin_input = input(admin_prompt)