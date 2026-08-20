import sqlite3
from datetime import datetime
from helpers.logger import dblogger

from repositories.appointments_repo import AppointmentsRepo
from repositories.doctor_repo import DoctorRepo

from services.doctorschedule_service import DoctorScheduleService
from services.doctor_service import DoctorService

from models.doctor_model import DoctorModel
from models.appointments_model import AppointmentsModel

class AppointmentsService:
    def __init__(self,appointment_repo :AppointmentsRepo,doctor_repo: DoctorRepo,
                doc_sched_service: DoctorScheduleService, doctor_s: DoctorService):
        self.appo_repo = appointment_repo
        self.doctor_repo = doctor_repo
        self.doc_sched_s = doc_sched_service
        self.doctor_s = doctor_s


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
            appointment_overlap = self.appo_repo.check_patient_appointment_overlap(appointment)
            if appointment_overlap is not None:
                return {'success': False,'message': "Another appointment exists for same time.",'data': appointment_overlap}

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
            doctor = DoctorModel(doctor_id,None,None,None,None)
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


    def check_for_reschedule(self,selected_date,earliest_slot_is_free):
        # date,doctor_id and start time are unique in appointments
        for id,slot in earliest_slot_is_free.items():
            normal_appointment = self.get_normal_appointment(id,selected_date,slot[0][0],slot[0][1])
            # display(normal_appointment['message'])
            if normal_appointment['success']:
                # normal_appointment['message'] = [normal_appointment['message']]
                normal_appointment['data'] = [id,slot[0]]
                return normal_appointment


    def priority_booking(self,selected_id,selected_service,problem_description):    
            selected_date = datetime.now().date().strftime("%Y-%m-%d")
            selected_time = datetime.now().time()
    
            result = self.doctor_s.get_doctors_from_service(selected_service)

            # there'll always be doctors for a service in hospital
            if(not result['success']): 
                return result
    
            doctors_data,doctor_ids,doctors_choices = result['data']
    
            doctors_slot = {id : self.doc_sched_s.get_doctor_slots(id,selected_date) for id in doctor_ids}
            # print(doctors_slot,"\n")
    
            doctors_free_slot = {id: self.get_doctors_free_slots(doctors_slot[id],id,selected_date)[0] for id in doctors_slot.keys()}
            # print(doctors_free_slot,"\n")
    
            earliest_slot_is_free = {}  # id: [slot, 0/1]
            for id, slots in doctors_slot.items():
                for slot in slots:
                    start_time = datetime.strptime(slot[0],"%H:%M").time()
                    if start_time > selected_time:
                        earliest_slot_is_free[id] = [slot, slot in doctors_free_slot[id]]
                        break
    
            # print(earliest_slot_is_free,"\n")
    
            earliest_free_doctor = []
            for id,slot in earliest_slot_is_free.items():
                if slot[1]:
                    earliest_free_doctor = [id,slot[0]]
                    break
            # print(earliest_free_doctor)
    
            selected_doctor,selected_slot = None,None
            reschedule_message = None

            if len(earliest_free_doctor)==0:
                result = self.check_for_reschedule(selected_date,earliest_slot_is_free)
                if result is None:
                    return {'success':False,'message':"No doctors available currently. All doctors are operating emergency patient."}
                reschedule_message = result['message']
                selected_doctor = result['data'][0]
                selected_slot = result['data'][1]
            else:
                selected_doctor = earliest_free_doctor[0]
                selected_slot = earliest_free_doctor[1]
    
            appointment_cost = doctors_data[selected_doctor][1]
    
            appointment_obj = AppointmentsModel(None,selected_id,selected_doctor,selected_date,selected_slot[0],selected_slot[1],"BOOKED",1,appointment_cost,problem_description)
            
            result = self.book_appointment(appointment_obj)
        
            if result['success']:
                result['reschedule_message'] = reschedule_message
                result['message'] = (f"""Your Appointment ID is {result['data']}.
         Please remember this id for future reference.
         
     Your Appointment Details:
     Doctor ID: {selected_doctor}
     Doctor Name: {doctors_data[selected_doctor][0]}
     Slot: {selected_slot[0]} - {selected_slot[1]}
     Appointment Cost: {appointment_cost}""")
            return result
