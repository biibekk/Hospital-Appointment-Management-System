import sqlite3

from helpers.logger import dblogger
from repositories.appointments_repo import AppointmentsRepo

class AppointmentsService:
    def __init__(self,appointment_repo :AppointmentsRepo):
        self.appo_repo = appointment_repo

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