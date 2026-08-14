from models.appointments_model import AppointmentsModel

class AppointmentsRepo:
    def __init__(self,connection):
        self.connection = connection
        self.cursor = connection.cursor()


    def get_booked_doctor_slots(self,doctor_id,date):
        query = """select start_time,end_time from appointments
        where doctor_id = ? and date = ?"""

        with self.connection:
            self.cursor.execute(query,(doctor_id,date))

        return self.cursor.fetchall()

    def book_appointment(self,appo):
        query = """insert into appointments(patient_id,doctor_id,date,start_time,end_time,status,priority,appointment_cost,problem_description)
        values(?,?,?,?,?,?,?,?,?)"""
        args = (appo.patient_id,appo.doctor_id,appo.date,appo.start_time,appo.end_time,appo.status,appo.priority,appo.appointment_cost,
                appo.problem_description)
        with self.connection:
            self.cursor.execute(query,args)

        return self.cursor.lastrowid

    def cancel_appointment(self,appointment_id):
        query = """delete from appointments
        where appointment_id = ?"""

        with self.connection:
            self.cursor.execute(query,(appointment_id,))

        return self.cursor.rowcount

    def get_appointment_details(self,appointment_id):
        query = """select * from appointments
        where appointment_id = ?"""

        with self.connection:
            self.cursor.execute(query,(appointment_id,))

        result = self.cursor.fetchone()
        return None if result is None else AppointmentsModel(*result)

    def reschedule_appointment(self,*args):
        query = """update appointments
        set date = ?, start_time = ?, end_time = ?
        where appointment_id = ?"""

        with self.connection:
            self.cursor.execute(query,args)

        return self.cursor.rowcount

    def view_appointment_history(self,patient_id):
        query = """select * from appointments
        where patient_id = ?"""

        with self.connection:
            self.cursor.execute(query,(patient_id,))

        rows = self.cursor.fetchall()
        all_appointments = []

        for row in rows:
            all_appointments.append(AppointmentsModel(*row))

        return None if len(rows) == 0 else all_appointments

    def get_doctor_appointments_today(self,doctor_id,date):
        query = """select * from appointments
        where doctor_id = ? and date = ?"""

        with self.connection:
            self.cursor.execute(query,(doctor_id,date))

        rows = self.cursor.fetchall()  # returns empty list if not found
        all_appointments = []

        for row in rows:
            all_appointments.append(AppointmentsModel(*row))

        return None if len(rows) == 0 else all_appointments