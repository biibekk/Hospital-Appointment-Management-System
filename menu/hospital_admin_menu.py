import re
from datetime import datetime

from services.appointments_service import AppointmentsService
from services.doctor_service import DoctorService
from services.doctorschedule_service import DoctorScheduleService
from services.patient_service import PatientService

from models.doctor_model import DoctorModel
from models.doctorschedule_model import DoctorSchedule

from helpers.display_help import display

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
        name = input("Enter your name: ")
        contact = input("Enter contact no: ")
        spec = input("Enter specialisation: ")
        fee = input("Enter consultation fee: ")

        return DoctorModel(name,contact,spec,fee)


    def add_doctor_schedule(self):
        display("Add Doctor Schedule")
        doctor_id = input("Enter doctor id: ")
        date = input("Enter date(yyyy-mm-dd): ").strip()
        date = datetime.strptime(date,"%Y-%m-%d").date()
        start_time = None
        while True:
            time_input = input("Enter start time(24 Hour - HH:MM): ")
            if not re.fullmatch(r"\d{2}:\d{2}", time_input):
                display("Please enter time as HH:MM, e.g. 01:00 or 13:00")
                continue

            try:
                time_obj = datetime.strptime(time_input,"%H:%M").time()
                start_time = time_obj.strftime("%H:%M")
                break

            except ValueError:
                display("Invalid time. Please use HH:MM.")

        end_time = input("Enter end time(hh:mm): ")

        return DoctorSchedule(doctor_id,date,start_time,end_time)
        
    def hospital_admin_menu(self):
        admin_input = input(admin_prompt)
        while admin_input != '5':
            if admin_input == '1':
                new_doctor = self.add_doctor()
                res = self.doctor_s.add_doctor(new_doctor)
                display(res['message'])
            elif admin_input == '2':
                new_doctor_schedule = self.add_doctor_schedule()
                res = self.doctorschedule_s.add_doctor_schedule(new_doctor_schedule)
                display(res['message'])
            elif admin_input == '5':
                break
            else:
                display("Please enter a valid input.")
            admin_input = input(admin_prompt)