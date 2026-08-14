from repositories.appointments_repo import AppointmentsRepo

class AppointmentsService:
    def __init__(self,appointment_repo :AppointmentsRepo):
        self.appo_repo = appointment_repo

    def get_booked_doctor_slots(self,doctor_id,date):
        result = self.appo_repo.get_booked_doctor_slots(doctor_id,date)
        busy_slots = []

        for st,et in result:
            busy_slots.append((st,et))

        return busy_slots
