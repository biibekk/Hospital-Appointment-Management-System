class DoctorScheduleRepo:
    def __init__(self,connection):
        self.connection = connection
        self.cursor = connection.cursor()


    def doctor_schedule_exists(self,schedule):
        query = """select * from doctorschedule where doctor_id = ? and date = ? and start_time = ?"""
        args = (schedule.doctor_id,schedule.date,schedule.start_time)

        self.cursor.execute(query,args)

        return self.cursor.fetchone()

    def add_doctor_schedule(self,schedule):
        query = """insert into doctorschedule(doctor_id,date,start_time,end_time,slot_duration)
        values(?, ?, ?, ?, ?)"""
        args = (schedule.doctor_id,schedule.date,schedule.start_time,schedule.end_time,schedule.slot_duration)

        with self.connection:
            self.cursor.execute(query,args)

        return self.cursor.rowcount

    def get_doctor_slots(self,doctor_id,date):
        query = """
            select schedule_id,start_time,end_time,slot_duration from doctorschedule 
            where doctor_id = ? and date = ?
            """
        with self.connection:
            self.cursor.execute(query,(doctor_id,date))

        return self.cursor.fetchall()

    def get_doctor_schedule(self,doctor_id):
        query = """
        select * from doctorschedule where doctor_id = ?"""
        with self.connection:
            self.cursor.execute(query,(doctor_id,))

        return self.cursor.fetchall()

    def delete_schedule(self):
        query = "delete from doctorschedule"
        with self.connection:
            self.cursor.execute(query)
