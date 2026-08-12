from database.dbconnection import DatabaseConnection

from services.appointments_service import AppointmentsService
from services.doctor_service import DoctorService
from services.doctorschedule_service import DoctorScheduleService
from services.patient_service import PatientService

from repositories.appointments_repo import AppointmentsRepo
from repositories.doctor_repo import DoctorRepo
from repositories.doctorschedule_repo import DoctorScheduleRepo
from repositories.patient_repo import PatientRepo

from models.patient_model import PatientModel

from helpers.display_help import display

db_obj = DatabaseConnection("app.db")
connection = db_obj.connection

appointment_r = AppointmentsRepo(connection)
doctor_r = DoctorRepo(connection)
doctorschedule_r = DoctorScheduleRepo(connection)
patient_r = PatientRepo(connection)

appointment_s = AppointmentsService(appointment_r)
doctor_s = DoctorService(doctor_r)
doctorschedule_s = DoctorScheduleService(doctorschedule_r)
patient_s = PatientService(patient_r)


display("Patient Registration")
def register_patient():
    name = input("Enter your name: ")
    dob = input("Enter your DOB(yyyy/mm/dd): ")
    gender = input("Enter your gender(M/F): ")
    contact = input("Enter your contact no: ")

    return PatientModel(name,dob,gender,contact)


p = register_patient()

patient_s.register_patient(p)
