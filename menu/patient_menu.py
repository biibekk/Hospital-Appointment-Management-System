from datetime import datetime

from services.appointments_service import AppointmentsService
from services.doctor_service import DoctorService
from services.doctorschedule_service import DoctorScheduleService
from services.patient_service import PatientService

from models.patient_model import PatientModel
from models.appointments_model import AppointmentsModel

from helpers.display_help import display
from helpers.prompts import Prompts
from helpers.validators import Validators


hospital_services = {1:'General Physician', 2:'Dermatology', 3:'Cardiology', 4:'Orthopedics', 5:'Pediatrics', 6:'Surgeon'}
hostpital_services_list = "\n".join([f"{key}. {val}" for key,val in hospital_services.items()])
max_choice = len(hospital_services) + 1

service_prompt = f"""\n{'-'*24}
     Select Service
{'-'*24}
{hostpital_services_list}
{max_choice}. Cancel
Enter your choice: """

class PatientMenu():
    def __init__(self,appointment_s: AppointmentsService,doctor_s: DoctorService,doctorschedule_s: DoctorScheduleService,patient_s: PatientService):
        self.appointment_s = appointment_s
        self.doctor_s = doctor_s
        self.doctorschedule_s = doctorschedule_s
        self.patient_s = patient_s


    def register_patient(self):
        display("Patient Registration")
        name = Validators.get_non_empty_string("Enter your name: ")
        dob = Validators.get_past_date("Enter your DOB(yyyy/mm/dd): ")
        gender = Validators.get_single_charater("Enter your gender(M/F): ", ('M','F'))
        contact = Validators.get_contact("Enter your contact no: ",10)

        patient_obj = PatientModel(None,name,dob,gender,contact)
        result = self.patient_s.register_patient(patient_obj)
        display(result['message'])
        if result['success']:
            display(f"""Your Patient ID is {result['data']}.
     Please remember this id for future reference.""")


    def get_doctors_free_slots(self,doctor_id,date):
        doctor_day_slots = self.doctorschedule_s.get_doctor_slots(doctor_id,date)

        return self.appointment_s.get_doctors_free_slots(doctor_day_slots,doctor_id,date)

    def check_for_reschedule(self,selected_date,earliest_slot_is_free):
        # date,doctor_id and start time are unique in appointments
        for id,slot in earliest_slot_is_free.items():
            normal_appointment = self.appointment_s.get_normal_appointment(id,selected_date,slot[0][0],slot[0][1])
            display(normal_appointment['message'])
            if normal_appointment['success']:
                # print(normal_appointment['data'])
                return [id,slot[0]]
        

    def priority_booking(self,selected_id):
        selected_service_number = Validators.get_choice(service_prompt,1,max_choice)
        if selected_service_number == max_choice: return
        selected_service = hospital_services[selected_service_number]

        selected_date = datetime.now().date().strftime("%Y-%m-%d")
        selected_time = datetime.now().time()

        result = self.doctor_s.get_doctors_from_service(selected_service)
        
        if(not result['success']): 
            display(result['message'])
            return

        doctors_data,doctor_ids,doctors_choices = result['data']

        doctors_slot = {id : self.doctorschedule_s.get_doctor_slots(id,selected_date) for id in doctor_ids}
        # print(doctors_slot,"\n")

        doctors_free_slot = {id: self.appointment_s.get_doctors_free_slots(doctors_slot[id],id,selected_date)[0] for id in doctors_slot.keys()}
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

        problem_description = Validators.get_problem_description(Prompts.problem_description)

        selected_doctor,selected_slot = None,None
        if len(earliest_free_doctor)==0:
            result = self.check_for_reschedule(selected_date,earliest_slot_is_free)
            if result is None:
                return
            selected_doctor = result[0]
            selected_slot = result[1]
        else:
            selected_doctor = earliest_free_doctor[0]
            selected_slot = earliest_free_doctor[1]

        appointment_cost = doctors_data[selected_doctor][1]

        appointment_obj = AppointmentsModel(None,selected_id,selected_doctor,selected_date,selected_slot[0],selected_slot[1],"BOOKED",1,appointment_cost,problem_description)
        
        res = self.appointment_s.book_appointment(appointment_obj)
        display(res['message'])
        if res['success']:
            display(f"""Your Appointment ID is {res['data']}.
     Please remember this id for future reference.
     
     Your Appointment Details:
     Doctor ID: {selected_doctor}
     Doctor Name: {doctors_data[selected_doctor][0]}
     Slot: {selected_slot[0]} - {selected_slot[1]}
     Appointment Cost: {appointment_cost}""")


    def book_appointment(self):
        # get patient id, for now - need to work on registration
        selected_pid = Validators.get_int(Prompts.patient_id)

        # priority selection
        selected_priority = Validators.get_choice(Prompts.priority,1,2)

        if selected_priority == 1:
            return self.priority_booking(selected_pid)

        # select hospital service
        selected_service_number = Validators.get_choice(service_prompt,1,max_choice)
        if selected_service_number == max_choice: 
            return
        selected_service = hospital_services[selected_service_number]

        result = self.doctor_s.get_doctors_from_service(selected_service)

        if(not result['success']): 
            display(result['message'])
            return

        # select doctor
        doctors_data,doctor_ids,doctors_choices = result['data']
        selected_doctor = Validators.get_choice_from_list(Prompts.doctor.format(doctors = doctors_choices),doctor_ids,"doctor")
        appointment_cost = doctors_data[selected_doctor][1]

        # date selection
        selected_date = Validators.get_future_date(Prompts.date)

        # SLOT selection
        free_slots,slot_choices = self.get_doctors_free_slots(selected_doctor,selected_date)
        max_slot_choice = len(free_slots)

        if max_slot_choice == 0:
            display(f"No slots available on {selected_date}. Please Try Again.")
            return
        
        selected_slot_number = Validators.get_choice(Prompts.slot.format(slots = slot_choices),1,max_slot_choice) 
        selected_slot = free_slots[selected_slot_number - 1] 

        # problem description selection:
        problem_desc = Validators.get_problem_description(Prompts.problem_description)

        appointment_obj = AppointmentsModel(None,selected_pid,selected_doctor,selected_date,selected_slot[0],selected_slot[1],"BOOKED",selected_priority,appointment_cost,problem_desc)

        res = self.appointment_s.book_appointment(appointment_obj)
        display(res['message'])
        if res['success']:
            display(f"""Your Appointment ID is {res['data']}.
     Please remember this id for future reference.""")


    def cancel_appointment(self):
        selected_app_id = Validators.get_int("\nEnter Appointment ID: ")

        res = self.appointment_s.cancel_appointment(selected_app_id)
        display(res['message'])


    def reschedule_appointment(self):
        selected_app_id = Validators.get_int("\nEnter Appointment ID: ")

        res = self.appointment_s.get_appointment_details(selected_app_id)
        selected_doctor = None
        if not res['success']:
            display(res['message'])
            return
        else:
            res['data'].display_header()
            print(res['data'])
            selected_doctor = res['data'].doctor_id

        # date selection
        selected_date = Validators.get_future_date(Prompts.date)

        free_slots,slot_choices = self.get_doctors_free_slots(selected_doctor,selected_date)
        max_slot_choice = len(free_slots)

        if max_slot_choice == 0:
            display(f"No slots available on {selected_date}. Please Try Again.")
            return
        
        selected_slot_number = Validators.get_choice(Prompts.slot.format(slots = slot_choices),1,max_slot_choice) 
        selected_slot = free_slots[selected_slot_number - 1] 

        # maybe ask final confirmation [Y/N]
        result = self.appointment_s.reschedule_appointment(selected_date,selected_slot[0],selected_slot[1],selected_app_id)
        display(result['message'])


    def get_appointment_status(self):
        selected_app_id = Validators.get_int("\nEnter Appointment ID: ")

        res = self.appointment_s.get_appointment_details(selected_app_id)
        selected_doctor = None
        if not res['success']:
            display(res['message'])
            return
        else: 
            status = res['data'].status
            date = res['data'].date
            start_time,end_time = res['data'].start_time, res['data'].end_time
            message = f"""Your appointment is {status}.
     Date: {date}
     Slot: {start_time} - {end_time}"""
            display(message)


    def view_appointment_history(self):
        selected_patient_id = Validators.get_int("\nEnter Patient ID: ")

        result = self.appointment_s.view_appointment_history(selected_patient_id)
        if not result['success']:
            display(result['message'])
            return
        display(f"Appointments History of Patient {selected_patient_id}")
        result['data'][0].display_header()    # header for table display from AppointmentsModel
        for appointment in result['data']:
            print(appointment)
    

    def patient_menu(self):
        patient_input = Validators.get_non_empty_string(Prompts.patient_menu)

        while patient_input != '7':
            if patient_input == '1':
                self.register_patient()
            elif patient_input == '2':
                self.book_appointment()
            elif patient_input == '3':
                self.cancel_appointment()
            elif patient_input == '4':
                self.reschedule_appointment()
            elif patient_input == '5':
                self.get_appointment_status()
            elif patient_input == '6':
                self.view_appointment_history()
            elif patient_input == '7':
                break
            else:
                display("Please enter a valid input.")
            patient_input = input(Prompts.patient_menu)