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
from models.doctor_model import DoctorModel
from models.doctorschedule_model import DoctorSchedule

from helpers.display_help import display

db_obj = DatabaseConnection("app.db")
connection = db_obj.connection

appointment_r = AppointmentsRepo(connection)
doctor_r = DoctorRepo(connection)
doctorschedule_r = DoctorScheduleRepo(connection)
patient_r = PatientRepo(connection)

appointment_s = AppointmentsService(appointment_r)
doctor_s = DoctorService(doctor_r)
doctorschedule_s = DoctorScheduleService(doctorschedule_r,doctor_r)
patient_s = PatientService(patient_r)


def register_patient():
    display("Patient Registration")
    name = input("Enter your name: ")
    dob = input("Enter your DOB(yyyy/mm/dd): ")
    gender = input("Enter your gender(M/F): ")
    contact = input("Enter your contact no: ")

    return PatientModel(name,dob,gender,contact)


# p = register_patient()
# patient_s.register_patient(p)


def add_doctor():
    display("Add Doctor")
    name = input("Enter your name: ")
    contact = input("Enter contact no: ")
    spec = input("Enter specialisation: ")
    fee = input("Enter consultation fee: ")

    return DoctorModel(name,contact,spec,fee)

# d = add_doctor()
# doctor_s.add_doctor(d)


def add_doctor_schedule():
    display("Add Doctor Schedule")
    doctor_id = input("Enter doctor id: ")
    date = input("Enter date(yyyy/mm/dd): ")
    start_time = input("Enter start time(hh:mm): ")
    end_time = input("Enter end time(hh:mm): ")

    return DoctorSchedule(doctor_id,date,start_time,end_time)

ds = add_doctor_schedule()
doctorschedule_s.add_doctor_schedule(ds)
