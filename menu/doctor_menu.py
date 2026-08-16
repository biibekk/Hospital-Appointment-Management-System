from datetime import datetime

from services.appointments_service import AppointmentsService
from services.doctor_service import DoctorService
from services.doctorschedule_service import DoctorScheduleService
from services.patient_service import PatientService


from helpers.display_help import display
from helpers.validators import Validators

doctor_prompt = f"""\n{'-'*21}
     Doctor's Menu
{'-'*21}
1. Get today's appointments
2. Get patient information
3. Get patient history
4. Go Back
Enter your choice: """

class DoctorMenu:
    def __init__(self,appointment_s: AppointmentsService,doctor_s: DoctorService,doctorschedule_s: DoctorScheduleService,patient_s: PatientService):
        self.appointment_s = appointment_s
        self.doctor_s = doctor_s
        self.doctorschedule_s = doctorschedule_s
        self.patient_s = patient_s

    def get_doctor_appointments_today(self):
        selected_doctor_id = Validators.get_int("Enter Doctor ID: ")

        date = datetime.now().date().strftime("%Y-%m-%d")
        # date = "2026-08-15"

        result = self.appointment_s.get_doctor_appointments_today(selected_doctor_id, date)
        if not result['success']:
            display(result['message'])
            return

        display(f"Today's Appointments for Doctor {selected_doctor_id}")
        result['data'][0].display_header()    # header for table display from AppointmentsModel
        for appointment in result['data']:
            print(appointment)

    def get_patient_info(self):
        selected_patient_id = Validators.get_int("Enter Patient ID: ")

        result = self.patient_s.get_patient_info(selected_patient_id)
        if not result['success']:
            display(result['message'])
            return

        result['data'].display_header()
        print(result['data'])

    def get_patient_history(self):
            selected_patient_id = Validators.get_int("Enter Patient ID: ")
    
            result = self.appointment_s.view_appointment_history(selected_patient_id)
            if not result['success']:
                display(result['message'])
                return
            display(f"Appointments History of Patient {selected_patient_id}")
            result['data'][0].display_header()    # header for table display from AppointmentsModel
            for appo in result['data']:
                print(appo)

    def doctor_menu(self):
        doctor_input = input(doctor_prompt)
        while doctor_input != '4':
            if doctor_input == '1':
                self.get_doctor_appointments_today()
            elif doctor_input == '2':
                self.get_patient_info()
            elif doctor_input == '3':
                self.get_patient_history()
            elif doctor_input == '4':
                break
            else:
                display("Please enter a valid input.")
            doctor_input = input(doctor_prompt)