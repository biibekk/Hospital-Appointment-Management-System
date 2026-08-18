from services.appointments_service import AppointmentsService
from services.doctor_service import DoctorService
from services.doctorschedule_service import DoctorScheduleService
from services.patient_service import PatientService

from models.patient_model import PatientModel
from models.appointments_model import AppointmentsModel

from helpers.display_help import display
from helpers.prompts import Prompts
from helpers.validators import Validators


hospital_services = {1:'Physician', 2:'Dermatology', 3:'Cardiology', 4:'Orthopedics', 5:'Dental', 6:'Surgeon'}
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
        dob = Validators.get_past_date("Enter your DOB(yyyy-mm-dd): ")
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
        

    def priority_booking(self,selected_id):
        selected_service_number = Validators.get_choice(service_prompt,1,max_choice)
        if selected_service_number == max_choice: return
        selected_service = hospital_services[selected_service_number]

        problem_description = Validators.get_problem_description(Prompts.problem_description)

        result = self.appointment_s.priority_booking(selected_id,selected_service,problem_description)

        if result['success']:
            display(result['reschedule_message'])
        display(result['message'])

        

    def book_appointment(self):
        # get patient id, for now - need to work on registration
        selected_pid = Validators.get_int(Prompts.patient_id)
        result = self.patient_s.patient_exists(PatientModel(selected_pid,None,None,None,None))
        if not result['success']:
            display(result['message'])
            return

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
        elif 'data' in res:
            display("Existing appointment details.")
            res['data'].display_header()
            print(res['data'])


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
        selected_pid = Validators.get_int("\nEnter Patient ID: ")
        result = self.patient_s.patient_exists(PatientModel(selected_pid,None,None,None,None))
        if not result['success']:
            display(result['message'])
            return

        result = self.appointment_s.view_appointment_history(selected_pid)
        if not result['success']:
            display(result['message'])
            return
        display(f"Appointments History of Patient {selected_pid}")
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