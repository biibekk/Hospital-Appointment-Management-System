class AppointmentsModel:
    def __init__(self,appointment_id,patient_id,doctor_id,date,start_time,end_time,status,priority,appointment_cost,problem_description):
        self.appointment_id = appointment_id
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.status = status
        self.priority = priority
        self.appointment_cost = appointment_cost
        self.problem_description = problem_description


    def __str__(self):
        return f"<Appointment id='{self.appointment_id} doctorId='{self.doctor_id} patientId='{self.patient_id}'>"
        # return f"<Appointment id='{self.appointment_id} doctorId='{self.doctor_id} 'date='{self.date}' time='{self.start_time}'>"

    