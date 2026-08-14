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
        return (
            f"{self.appointment_id:<20}"
            f"{self.patient_id:<12}"
            f"{self.doctor_id:<12}"
            f"{self.date:<15}"
            f"{self.start_time:<12}"
            f"{self.end_time:<12}"
            f"{self.status:<12}"
            f"{self.priority:<10}"
            f"{self.appointment_cost:<18}"
            f"{self.problem_description:<30}"
        )
    def display_header(self):
        print(
            f"{'Appointment ID':<20}"
            f"{'Patient ID':<12}"
            f"{'Doctor ID':<12}"
            f"{'Date':<15}"
            f"{'Start':<12}"
            f"{'End':<12}"
            f"{'Status':<12}"
            f"{'Priority':<10}"
            f"{'Cost':<18}"
            f"{'Problem':<30}"
        )

        print("-" * 136)