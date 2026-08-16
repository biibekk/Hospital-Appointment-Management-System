import sqlite3

from helpers.logger import dblogger
from repositories.appointments_repo import AppointmentsRepo
from repositories.doctor_repo import DoctorRepo
from repositories.doctorschedule_repo import DoctorScheduleRepo
from services.doctorschedule_service import DoctorScheduleService

from models.doctor_model import DoctorModel

class AppointmentsService:
    def __init__(self,appointment_repo :AppointmentsRepo,doctor_repo: DoctorRepo, doc_sched_repo: DoctorScheduleRepo, doc_sched_service: DoctorScheduleService):
        self.appo_repo = appointment_repo
        self.doctor_repo = doctor_repo
        self.doc_sched_repo = doc_sched_repo
        self.doc_sched_s = doc_sched_service


    def get_booked_doctor_slots(self,doctor_id,date):
        try:
            result = self.appo_repo.get_booked_doctor_slots(doctor_id,date)
            busy_slots = []

            for st,et in result:
                busy_slots.append((st,et))

            return busy_slots
        except sqlite3.Error as e:
            dblogger.error(f"Database Error: {e}")
            return {'success': False,'message': f"Unable to fetch booked slots for doctor id {doctor_id}. Please try again."}


    def get_doctors_free_slots(self,doctor_day_slots,doctor_id,date):
        try:
            busy_slots = self.appo_repo.get_booked_doctor_slots(doctor_id,date)

            free_slots = [slot for slot in doctor_day_slots if slot not in busy_slots]
            slot_choices = '\n'.join([f"{ind:<8} {val[0]:<11} {val[1]}" for ind,val in enumerate(free_slots, start=1)])

            return (free_slots, slot_choices)
        except sqlite3.Error as e:
            dblogger.error(f"Database Error: {e}")
            return {'success': False,'message': "Unable to get doctors free slot. Please try again."}


    def book_appointment(self,appointment):
        try:
            result = self.appo_repo.book_appointment(appointment)
            return {'success':True,'message':"Appointment Booked Successfully.",'data':result}
        except sqlite3.Error as e:
            dblogger.error(f"Database Error: {e}")
            return {'success': False,'message': "Unable to book appointment. Please try again."}


    def cancel_appointment(self,appointment_id):
        try:
            result = self.appo_repo.cancel_appointment(appointment_id)

            if(result):
                return {'success':True,'message':"Appointment Cancelled Successfully."}
            
            return {'success':False,'message':f"Appointment with ID {appointment_id} doesn't exists."}
        except sqlite3.Error as e:
            dblogger.error(f"Database Error: {e}")
            return {'success': False,'message': "Unable to cancel appointment. Please try again."}


    def get_appointment_details(self,appointment_id):
        try:
            result = self.appo_repo.get_appointment_details(appointment_id)
            if result is None:
                return {'success':False,'message':f"Appointment with ID {appointment_id} doesn't exists."}

            return {'success':True,'message':"Appointment Details Fetched Successfully.",'data':result}

        except sqlite3.Error as e:
            dblogger.error(f"Database Error: {e}")
            return {'success': False,'message': "Unable to fetch appointment details. Please try again."}


    def reschedule_appointment(self,date,start_time,end_time,appointment_id):
        try:
            result = self.appo_repo.reschedule_appointment(date,start_time,end_time,appointment_id)
            return {'success':True,'message':"Appointment Rescheduled Successfully."}
        except sqlite3.Error as e:
            dblogger.error(f"Database Error: {e}")
            return {'success': False,'message': "Unable to reschedule appointment. Please try again."}


    def view_appointment_history(self,patient_id):
        # patient registers and i have his id which is passed here so no need to verify if patient exists
        try:
            all_appointments = self.appo_repo.view_appointment_history(patient_id)

            success = False if all_appointments is None else True
            message = f"No Appointments exists for patient {patient_id}." if all_appointments is None else \
                "Appointments history fetched successfully."
            return {'success':success, 'message':message,'data':all_appointments}
        except sqlite3.Error as e:
            dblogger.error(f"Database Error: {e}")
            return {'success': False,'message': "Unable to fetch appointments history. Please try again."}


    def get_doctor_appointments_today(self,doctor_id,date):
        try:
            doctor = DoctorModel(None,None,None,None,doctor_id)
            if not self.doctor_repo.doctor_exists(doctor):
                return {'success':False,'message':f"Doctor with ID {doctor_id} not found."}
            
            all_appointments = self.appo_repo.get_doctor_appointments_today(doctor_id,date)

            success = False if all_appointments is None else True
            message = f"No Appointments today for doctor {doctor_id}." if all_appointments is None else \
                            "Today's Appointments fetched successfully,"
            return {'success':success, 'message':message,'data':all_appointments}
        except sqlite3.Error as e:
            dblogger.error(f"Database Error: {e}")
            return {'success': False,'message': "Unable to fetch today's appointments. Please try again."}


    def get_normal_appointment(self,doctor_id,date,start_time,end_time):
        try:
            result = self.appo_repo.get_normal_appointment(doctor_id,date,start_time)

            if result is None:
                return {'success':False,'message':"Normal Appointmens not found."}
            
            return self.reschedule_normal_appointment(result)

            # return {'success':True,'message':"Normal appointment found.",'data':result}
        except sqlite3.Error as e:
            dblogger.error(f"Database Error: {e}")
            return {'success': False,'message': "Unable to fetch today's appointments. Please try again."}


    def reschedule_normal_appointment(self,normal):
        try:
            doctor_day_slots = self.doc_sched_s.get_doctor_slots(normal.doctor_id,normal.date)

            free_slots,slot_choices = self.get_doctors_free_slots(doctor_day_slots,normal.doctor_id,normal.date)

            if(len(free_slots) == 0):
                return {'success':False,'message':'No free slot to reschedule appointment.'}

            start_time,end_time = free_slots[0]

            result = self.reschedule_appointment(normal.date,start_time,end_time,normal.appointment_id)

            message = f"""Appointment with id {normal.appointment_id} rescheduled.
        New Slot: {start_time} - {end_time}"""
            if not result['success']:
                message = result['message']

            return {'success':result['success'],'message':message}
        except sqlite3.Error as e:
            dblogger.error(f"Database Error: {e}")
            return {'success': False,'message': f"Unable to reschedule appointment {normal.appointment_id}. Please try again."}
        