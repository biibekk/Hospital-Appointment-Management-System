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
        name = input("Enter your name: ")
        dob = input("Enter your DOB(yyyy/mm/dd): ")
        gender = input("Enter your gender(M/F): ")
        contact = input("Enter your contact no: ")

        return PatientModel(None,name,dob,gender,contact)



    def book_appointment(self):
        # get patient id, for now - need to work on registration
        selected_id = Validators.get_int(Prompts.patient_id)
        

        # select hospital service
        selected_service_number = Validators.get_choice(service_prompt,1,max_choice)
        if selected_service_number == max_choice: return
        selected_service = hospital_services[selected_service_number]

        # selected_service = None
        # while True:
        #     try:
        #         service_input = int(input(service_prompt))
        #         if 1 <= service_input <= max_choice:
        #             if service_input == max_choice: return
        #             selected_service = hospital_services[service_input]
        #             break
        #         else:
        #             display(f"Error: Please enter a number between 1 and {max_choice}.")
        #     except ValueError as e:
        #         display("Error: Invalid input! Please enter a whole number")

        result = self.doctor_s.get_doctors_from_service(selected_service)
        if(not result['success']): 
            display(result['message'])
            return

        # select doctor
        selected_doctor = None
        appointment_cost = None

        # move this to service
        doctors_data = {t[0]:(t[1],t[2]) for t in result['data']}
        doctor_ids = [t[0] for t in result['data']]
        doctors_list = '\n'.join([f"{t[0]:<15} {t[1]:<25} {t[2]}" for t in result['data']])

        while True:
            try:
                doctor_input = int(input(Prompts.doctor.format(doctors = doctors_list)))

                if doctor_input in doctor_ids:
                    selected_doctor = doctor_input
                    appointment_cost = doctors_data[selected_doctor][1]
                    break
                else:
                    display("Error: Please enter doctor id from above options: ")

            except ValueError:
                display("Error: Invalid input! Please enter a whole number")


        # date selection
        selected_date = Validators.get_date(Prompts.date)
        # while True:
        #     date_input = input(Prompts.date).strip()
        #     try:
        #         # Validates format AND checks if date exists on calendar
        #         # string -> datetime -> date
        #         selected_date = datetime.strptime(date_input,"%Y-%m-%d").date()

        #         if selected_date < datetime.now().date():
        #             display("Error: Date must be greater than today.\n")
        #             continue

        #         break
        #     except ValueError:
        #         display("Error: Invalid date format or non-existent date! Please use YYYY-MM-DD.\n")

        # selected_date = selected_date.strftime("%Y-%m-%d")


        # SLOT selection
        # get slots for doctor on that date, doctor schedule to find all slots then appointments on that day for subtraction

        slots = self.doctorschedule_s.get_doctor_slots(selected_doctor,selected_date)

        # get busy slots of doctor from appointments on that day
        busy_slots =self.appointment_s.get_booked_doctor_slots(selected_doctor,selected_date)

        free_slots = [slot for slot in slots if slot not in busy_slots]
        slot_choices = '\n'.join([f"{ind:<8} {val[0]:<11} {val[1]}" for ind,val in enumerate(free_slots, start=1)])
        max_slot_choice = len(free_slots)

        if len(free_slots) == 0:
            display(f"No slots available on {selected_date}. Please Try Again.")
            return
        
        selected_slot_number = Validators.get_choice(Prompts.slot.format(slots = slot_choices),1,max_slot_choice) 
        selected_slot = free_slots[selected_slot_number - 1] 
        # while True:
        #     try:
        #         slot_input = int(input(Prompts.slot.format(slots = slot_choices)))
        #         if 1 <= slot_input <= max_slot_choice:
        #             selected_slot = free_slots[slot_input-1]
        #             break
        #         else:
        #             display(f"Error: Please enter a number between 1 and {max_slot_choice}.")

        #     except ValueError:
        #         display("Error: Invalid input! Please enter a whole number")

        # priority selection
        selected_priority = Validators.get_choice(Prompts.priority,1,2)
        # while True:
        #     try:
        #         prioprity_input = int(input(Prompts.priority))
        #         if 1 <= prioprity_input <= 2:
        #             selected_priority = prioprity_input
        #             break
        #         else:
        #             display(f"Error: Please enter 1 or 2.")
        #     except ValueError:
        #         display("Error: Invalid input! Please enter a whole number")

        # problem description selection:
        problem_desc = Validators.get_problem_description(Prompts.problem_description)
        # while True:
        #     problem_input = input(Prompts.problem_description)
        #     if len(problem_input) == 0:
        #         display("Error: Description cannot be empty.")
        #         continue
        #     if len(problem_input) == 10:
        #         display("Error: Description must be of length greater than 10.")
        #         continue
        #     if problem_input.isdigit():
        #         display("Error: Description cannot contain digits only.")
        #         continue

        #     problem_desc = problem_input
        #     break

        appointment_obj = AppointmentsModel(None,selected_id,selected_doctor,selected_date,selected_slot[0],selected_slot[1],"BOOKED",selected_priority,appointment_cost,problem_desc)

        # print(appointment_obj)

        res = self.appointment_s.book_appointment(appointment_obj)
        display(res['message'])
        if res['success']:
            display(f"""Your Appointment ID is {res['data']}.
     Please remember this id for future reference.""")
            # display("Please remember this id for future reference.")
        
    def cancel_appointment(self):
        selected_app_id = Validators.get_int("\nEnter Appointment ID: ")
        # while True:
        #     try:
        #         app_id_input = int(input("\nEnter Appointment ID: "))
        #         selected_app_id = app_id_input
        #         break
        #     except ValueError:
        #         display("Error: Invalid input! Please enter a whole number")

        res = self.appointment_s.cancel_appointment(selected_app_id)
        display(res['message'])

    def reschedule_appointment(self):
        selected_app_id = Validators.get_int("\nEnter Appointment ID: ")
        # while True:
        #     try:
        #         app_id_input = int(input("\nEnter Appointment ID: "))
        #         selected_app_id = app_id_input
        #         break
        #     except ValueError:
        #         display("Error: Invalid input! Please enter a whole number")

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
        selected_date = Validators.get_date(Prompts.date)


        # slot selection
        # get slots for doctor on that date, doctor schedule to find all slots then appointments on that day for subtraction

        slots = self.doctorschedule_s.get_doctor_slots(selected_doctor,selected_date)

        # get busy slots of doctor from appointments on that day
        busy_slots = self.appointment_s.get_booked_doctor_slots(selected_doctor,selected_date)

        free_slots = [slot for slot in slots if slot not in busy_slots]
        slot_choices = '\n'.join([f"{ind:<8} {val[0]:<11} {val[1]}" for ind,val in enumerate(free_slots, start=1)])
        max_slot_choice = len(free_slots)

        if len(free_slots) == 0:
            display(f"No slots available on {selected_date}. Please Try Again.")
            # here it will return to function that called it
        
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
        # patient_input = input(Prompts.patient).strip()
        # while(len(patient_input)==0):
        #     display("Input cannot be empty. Try Again")
        #     patient_input = input(Prompts.patient).strip()

        while patient_input != '7':
            if patient_input == '1':
                patient_obj = self.register_patient()
                res = self.patient_s.register_patient(patient_obj)
                display(res['message'])
                # display patient id as well

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