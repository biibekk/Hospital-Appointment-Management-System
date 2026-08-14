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