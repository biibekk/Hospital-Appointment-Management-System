from datetime import datetime,date
import re

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
from models.appointments_model import AppointmentsModel

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


def add_doctor():
    display("Add Doctor")
    name = input("Enter your name: ")
    contact = input("Enter contact no: ")
    spec = input("Enter specialisation: ")
    fee = input("Enter consultation fee: ")

    return DoctorModel(name,contact,spec,fee)



def add_doctor_schedule():
    display("Add Doctor Schedule")
    doctor_id = input("Enter doctor id: ")
    date = input("Enter date(yyyy-mm-dd): ").strip()
    date = datetime.strptime(date,"%Y-%m-%d").date()
    start_time = None
    while True:
        time_input = input("Enter start time(24 Hour - HH:MM): ")
        if not re.fullmatch(r"\d{2}:\d{2}", time_input):
            display("Please enter time as HH:MM, e.g. 01:00 or 13:00")
            continue

        try:
            time_obj = datetime.strptime(time_input,"%H:%M").time()
            start_time = time_obj.strftime("%H:%M")
            break

        except ValueError:
            display("Invalid time. Please use HH:MM.")

    end_time = input("Enter end time(hh:mm): ")

    return DoctorSchedule(doctor_id,date,start_time,end_time)

# ds = add_doctor_schedule()
# response = doctorschedule_s.add_doctor_schedule(ds)
# display(response['message'])


# CHECKING SQL ERROR CATCH AND LOGGING METHOD
# print(doctor_r.add_error_check(1,"demo",1234,"demo",1000))     this is bypassing the service with direct call to repo
# response = doctor_s.add_error_check(1,"demo",1234,"demo",1000)
# display(response['message'])


menu_prompt = f"""\n{'-'*37}
     Hospital Appointment System
{'-'*37}
1. Hospital Admin
2. Doctor
3. Patient
4. Quit
Enter your choice: """

patient_prompt = f"""\n{'-'*23}
     Patient Menu
{'-'*23}
1. Register Patient
2. Book Appointment
3. Cancel Appointment
4. Reschedule Appointment
5. Check Appointment Status
6. View Appointment History
7. Go Back
Enter your choice: """

admin_prompt = f"""\n{'-'*29}
     Hospital Admin Menu
{'-'*29}
1. Add Doctor
2. Add Doctor Schedule
3. View Doctors
4. View Schedules
5. Go Back
Enter your choice: """

hospital_services = {1:'General Physician', 2:'Dermatology', 3:'Cardiology', 4:'Orthopedics', 5:'Pediatrics', 6:'Surgeon'}
hostpital_services_list = "\n".join([f"{key}. {val}" for key,val in hospital_services.items()])
max_choice = len(hospital_services) + 1


patient_id_prompt = f"""{'-'*20}
     Patient ID
{'-'*20}
Enter Patient ID no: """

service_prompt = f"""\n{'-'*24}
     Select Service
{'-'*24}
{hostpital_services_list}
{max_choice}. Cancel
Enter your choice: """

doctor_prompt = """\n---------------------
     Select Doctor
----------------------

Doctor Id       Name                     Consultation Fee
{doctors}

Enter Doctor Id: """

date_prompt = f"""\n{'-'*31}
     Select Appointment Date
{'-'*31}
Enter date(yyyy-mm-dd): """

slot_prompt = """\n---------------------
     Select Slot
---------------------

S.No.  Start Time   End Time
{slots}

Enter Slot No: """


priority_prompt = f"""\n{'-'*24}
     Select Priority
{'-'*24}
1. Emergency
2. Normal
Enter your choice:"""


problem_des_prompt = f"""\n{'-'*28}
     Problem Description
{'-'*28}
Describe your problem in few words: """

def hospital_admin_menu():
    admin_input = input(admin_prompt)
    while admin_input != '5':
        if admin_input == '1':
            new_doctor = add_doctor()
            res = doctor_s.add_doctor(new_doctor)
            display(res['message'])
        elif admin_input == '2':
            new_doctor_schedule = add_doctor_schedule()
            res = doctorschedule_s.add_doctor_schedule(new_doctor_schedule)
            display(res['message'])
        elif admin_input == '5':
            break
        else:
            display("Please enter a valid input.")
        admin_input = input(admin_prompt)

def get_doctor_for_date():
    pass

def book_appointment():
    # get patient id, for now - need to work on registration
    selected_id = None
    while True:
        try:
            id_input = int(input(patient_id_prompt))

            # need to add id validation or something
            selected_id = id_input
            break

        except ValueError:
            display("Error: Invalid input! Please enter a whole number")
    

    # select hospital service
    selected_service = None
    while True:
        try:
            service_input = int(input(service_prompt))
            if 1 <= service_input <= max_choice:
                if service_input == max_choice: return
                selected_service = hospital_services[service_input]
                break
            else:
                display(f"Error: Please enter a number between 1 and {max_choice}.")
        except ValueError as e:
            display("Error: Invalid input! Please enter a whole number")

    result = doctor_s.get_doctors_from_service(selected_service)
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
            doctor_input = int(input(doctor_prompt.format(doctors = doctors_list)))

            if doctor_input in doctor_ids:
                selected_doctor = doctor_input
                appointment_cost = doctors_data[selected_doctor][1]
                break
            else:
                display("Error: Please enter doctor id from above options: ")

        except ValueError:
            display("Error: Invalid input! Please enter a whole number")


    # date selection
    selected_date = None
    while True:
        date_input = input(date_prompt).strip()
        try:
            # Validates format AND checks if date exists on calendar
            # string -> datetime -> date
            selected_date = datetime.strptime(date_input,"%Y-%m-%d").date()

            if selected_date < datetime.now().date():
                display("Error: Date must be greater than today.\n")
                continue

            break
        except ValueError:
            display("Error: Invalid date format or non-existent date! Please use YYYY-MM-DD.\n")

    print(selected_date)  # datetime.date
    selected_date = selected_date.strftime("%Y-%m-%d")
    print(type(selected_date))


    # slot selection
    # get slots for doctor on that date, doctor schedule to find all slots then appointments on that day for subtraction

    slots = doctorschedule_s.get_doctor_slots(selected_doctor,selected_date)

    # get busy slots of doctor from appointments on that day
    busy_slots = appointment_s.get_booked_doctor_slots(selected_doctor,selected_date)

    free_slots = [slot for slot in slots if slot not in busy_slots]
    slot_choices = '\n'.join([f"{ind:<8} {val[0]:<11} {val[1]}" for ind,val in enumerate(free_slots, start=1)])
    max_slot_choice = len(free_slots)

    if len(free_slots) == 0:
        display(f"No slots available on {selected_date}. Please Try Again.")
        # here it will return to function that called it
    
    selected_slot = None
    while True:
        try:
            slot_input = int(input(slot_prompt.format(slots = slot_choices)))
            if 1 <= slot_input <= max_slot_choice:
                selected_slot = free_slots[slot_input-1]
                break
            else:
                display(f"Error: Please enter a number between 1 and {max_slot_choice}.")

        except ValueError:
            display("Error: Invalid input! Please enter a whole number")

    # priority selection
    selected_priority = None
    while True:
        try:
            prioprity_input = int(input(priority_prompt))
            if 1 <= prioprity_input <= 2:
                selected_priority = prioprity_input
                break
            else:
                display(f"Error: Please enter 1 or 2.")
        except ValueError:
            display("Error: Invalid input! Please enter a whole number")

    # problem description selection:
    problem_desc = None
    while True:
        problem_input = input(problem_des_prompt)
        if len(problem_input) == 0:
            display("Error: Description cannot be empty.")
            continue
        if len(problem_input) == 10:
            display("Error: Description must be of length greater than 10.")
            continue
        if problem_input.isdigit():
            display("Error: Description cannot contain digits only.")
            continue

        problem_desc = problem_input
        break

    appointment_obj = AppointmentsModel(None,selected_id,selected_doctor,selected_date,selected_slot[0],selected_slot[1],"BOOKED",selected_priority,appointment_cost,problem_desc)

    # print(appointment_obj)

    res = appointment_s.book_appointment(appointment_obj)
    display(res['message'])
    if res['success']:
        display(f"""Your Appointment ID is {res['data']}.
     Please remember this id for future reference.""")
        # display("Please remember this id for future reference.")
    
def cancel_appointment():
    selected_app_id = None
    while True:
        try:
            app_id_input = int(input("\nEnter Appointment ID: "))
            selected_app_id = app_id_input
            break
        except ValueError:
            display("Error: Invalid input! Please enter a whole number")

    res = appointment_s.cancel_appointment(selected_app_id)
    display(res['message'])

def reschedule_appointment():
    selected_app_id = None
    while True:
        try:
            app_id_input = int(input("\nEnter Appointment ID: "))
            selected_app_id = app_id_input
            break
        except ValueError:
            display("Error: Invalid input! Please enter a whole number")

    res = appointment_s.get_appointment_details(selected_app_id)
    selected_doctor = None
    if not res['success']:
        display(res['message'])
        return
    else: 
        print(res['data'])
        selected_doctor = res['data'].doctor_id

    # date selection
    selected_date = None
    while True:
        date_input = input(date_prompt).strip()
        try:
            # Validates format AND checks if date exists on calendar
            # string -> datetime -> date
            selected_date = datetime.strptime(date_input,"%Y-%m-%d").date()

            if selected_date < datetime.now().date():
                display("Error: Date must be greater than today.\n")
                continue

            break
        except ValueError:
            display("Error: Invalid date format or non-existent date! Please use YYYY-MM-DD.\n")

    # print(selected_date)  # datetime.date
    selected_date = selected_date.strftime("%Y-%m-%d")
    # print(type(selected_date))


    # slot selection
    # get slots for doctor on that date, doctor schedule to find all slots then appointments on that day for subtraction

    slots = doctorschedule_s.get_doctor_slots(selected_doctor,selected_date)

    # get busy slots of doctor from appointments on that day
    busy_slots = appointment_s.get_booked_doctor_slots(selected_doctor,selected_date)

    free_slots = [slot for slot in slots if slot not in busy_slots]
    slot_choices = '\n'.join([f"{ind:<8} {val[0]:<11} {val[1]}" for ind,val in enumerate(free_slots, start=1)])
    max_slot_choice = len(free_slots)

    if len(free_slots) == 0:
        display(f"No slots available on {selected_date}. Please Try Again.")
        # here it will return to function that called it
    
    selected_slot = None
    while True:
        try:
            slot_input = int(input(slot_prompt.format(slots = slot_choices)))
            if 1 <= slot_input <= max_slot_choice:
                selected_slot = free_slots[slot_input-1]
                break
            else:
                display(f"Error: Please enter a number between 1 and {max_slot_choice}.")

        except ValueError:
            display("Error: Invalid input! Please enter a whole number")

    # maybe ask final confirmation [Y/N]
    result = appointment_s.reschedule_appointment(selected_date,selected_slot[0],selected_slot[1],selected_app_id)
    display(result['message'])
    

def patient_menu():
    patient_input = input(patient_prompt).strip()
    while(len(patient_input)==0):
        display("Input cannot be empty. Try Again")
        patient_input = input(patient_prompt).strip()

    while patient_input != '7':
        if patient_input == '1':
            patient_obj = register_patient()
            res = patient_s.register_patient(patient_obj)
            display(res['message'])

        elif patient_input == '2':
            book_appointment()
        elif patient_input == '3':
            cancel_appointment()
        elif patient_input == '4':
            reschedule_appointment()
        elif patient_input == '7':
            break
        else:
            display("Please enter a valid input.")
        patient_input = input(patient_prompt)
    

def main():
    user_input = input(menu_prompt).strip()
    while len(user_input)==0:
        display("Input cannot be empty. Try Again")
        user_input = input(menu_prompt).strip()

    while user_input != '4':
        if user_input == '1':
            hospital_admin_menu()

        elif user_input == '2':
            pass

        elif user_input == '3':
            patient_menu()
        elif user_input == '4':
            break
        else:
            display("Please enter a valid input.")
        user_input = input(menu_prompt)

main()