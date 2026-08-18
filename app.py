from database.dbconnection import DatabaseConnection

from services.appointments_service import AppointmentsService
from services.doctor_service import DoctorService
from services.doctorschedule_service import DoctorScheduleService
from services.patient_service import PatientService

from repositories.appointments_repo import AppointmentsRepo
from repositories.doctor_repo import DoctorRepo
from repositories.doctorschedule_repo import DoctorScheduleRepo
from repositories.patient_repo import PatientRepo

from helpers.display_help import display
from menu.patient_menu import PatientMenu
from menu.hospital_admin_menu import HospitalAdminMenu
from menu.doctor_menu import DoctorMenu

db_obj = DatabaseConnection("app.db")
connection = db_obj.connection

appointment_r = AppointmentsRepo(connection)
doctor_r = DoctorRepo(connection)
doctorschedule_r = DoctorScheduleRepo(connection)
patient_r = PatientRepo(connection)

doctor_s = DoctorService(doctor_r)
doctorschedule_s = DoctorScheduleService(doctorschedule_r,doctor_r)
patient_s = PatientService(patient_r)
appointment_s = AppointmentsService(appointment_r,doctor_r,doctorschedule_s,doctor_s)

patient = PatientMenu(appointment_s,doctor_s,doctorschedule_s,patient_s)
admin = HospitalAdminMenu(appointment_s,doctor_s,doctorschedule_s,patient_s)
doctor = DoctorMenu(appointment_s,doctor_s,doctorschedule_s,patient_s)

from helpers.prompts import Prompts
from helpers.validators import Validators

user_input = Validators.get_non_empty_string(Prompts.menu_prompt)

while user_input != '4':
    if user_input == '1':
        admin.hospital_admin_menu()
    elif user_input == '2':
        doctor.doctor_menu()
    elif user_input == '3':
        patient.patient_menu()
    elif user_input == '4':
        break
    else:
        display("Please enter a valid input.")
    user_input = input(Prompts.menu_prompt)
