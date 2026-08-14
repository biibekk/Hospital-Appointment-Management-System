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