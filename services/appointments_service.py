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

