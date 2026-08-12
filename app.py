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

db_obj = DatabaseConnection("project_data.db")
connection = db_obj.connection

r_appointment = AppointmentsRepo(connection)
r_doctor = DoctorRepo(connection)
r_doctorschedule = DoctorScheduleRepo(connection)
r_patient = PatientRepo(connection)

s_appointment = AppointmentsService(r_appointment)
s_doctor = DoctorService(r_doctor)
s_doctorschedule = DoctorScheduleService(r_doctorschedule)
s_patient = PatientService(r_patient)


p = PatientModel("abcd","2004/1/1","male","1234","abcd",1)
print(s_patient.register_patient(p))
